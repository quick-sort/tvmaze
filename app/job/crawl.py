import argparse
import sys
import httpx
from collections import deque
from sqlalchemy import delete
import asyncio
from app.utils import flat_object
from app.utils import get_logger, send_email
import app.db.models as models
import datetime
from app.db import models
from app.db.session import SessionLocal
import json
from app.db.session import engine

logger = get_logger(__name__) 

async def request_tvmaze(url, retry=False):
    async with httpx.AsyncClient() as client:
        logger.info(f'{"retry" if retry else ""} fetch {url}')
        try:
            resp = await client.get(url, timeout=60)
            logger.info(f'got {resp.status_code} {url}')
            if resp.status_code == 200:
                return resp.json()
            else:
                await asyncio.sleep(60)
                return await request_tvmaze(url, retry=True)
        except Exception as e:
            logger.error(f'error {e} {url}')
            logger.error(f'waiting 60 seconds')
            await asyncio.sleep(60)
            return await request_tvmaze(url, retry=True)

async def crawl(job_id):
    with SessionLocal() as db:
        job = db.get(models.Job, job_id)
        if not job:
            return
        logger.info(f"processing job {job_id}")
        job.status = models.JobStatus.running
        job.start_time = datetime.datetime.now()
        db.add(job)
        db.commit()
        db.refresh(job)
        try:
            results = await _crawl(db, job.date, job.country)
            job.msg = json.dumps(results)
            job.status = models.JobStatus.done
        except Exception as e:
            job.msg = str(e)
            job.status = models.JobStatus.failed
        job.end_time = datetime.datetime.now()
        db.add(job)
        db.commit()
        db.refresh(job)
        send_email(
            subject=f'job {job_id} is {job.status}'
        )
        logger.info(f"processing job {job_id} done")
        return job
    

async def _crawl(db, date, country):
    from app.db import models
    from app.db.session import SessionLocal
    results = {'show': 0, 'episode': 0, 'guestcast': 0}
    
    data = await request_tvmaze(f'https://api.tvmaze.com/schedule?country={country}&date={date}')
    
    for item in data:
        show_id = item['show']['id']
        show = db.get(models.TVShow, show_id)
        logger.info(f"sync {date} {country} show:{show_id}")
        if not show:
            network =item['show']['network']
            if network:
                network = db.get(models.TVNetwork, item['show']['network']['id'])
                if not network:
                    network = models.TVNetwork(**flat_object(item['show']['network']))
                    db.add(network)
                    db.commit()
                    db.refresh(network)
            del item['show']['network']
            web_channel = item['show']['webChannel']
            if web_channel:
                web_channel = db.get(models.TVWebChannel, item['show']['webChannel']['id'])
                if not web_channel:
                    web_channel = models.TVWebChannel(**flat_object(item['show']['webChannel']))
                    db.add(web_channel)
                    db.commit()
                    db.refresh(web_channel)
            del item['show']['webChannel']
            show = models.TVShow(
                **flat_object(item['show']), 
                network_id=network.id if network else None, 
                webChannel_id=web_channel.id if web_channel else None
            )
            results['show'] += 1
            db.add(show)
            db.commit()
            db.refresh(show)
        del item['show']
        episode = db.get(models.TVEpisode, item['id'])
        logger.info(f'sync {date} {country} episode:{item["id"]}')
        if not episode:
            episode = models.TVEpisode(**flat_object(item), show_id=show.id)
            results['episode'] += 1
            db.add(episode)
            db.commit()
            db.refresh(episode)
        guestcast = await request_tvmaze(f'https://api.tvmaze.com/episodes/{episode.id}/guestcast')
        db.execute(
            delete(models.TVEpisodeGuestcast).where(
                models.TVEpisodeGuestcast.episode_id ==  episode.id
            )
        )
        for item in guestcast:
            person_id = item['person']['id']
            person = db.get(models.TVPeople, person_id)
            if not person:
                person = models.TVPeople(**flat_object(item['person']))
                db.add(person)
                db.commit()
                db.refresh(person)
            del item['person']
            character_id = item['character']['id']
            character = db.get(models.TVCharacter, character_id)
            if not character:
                character = models.TVCharacter(**flat_object(item['character']))
                db.add(character)
                db.commit()
                db.refresh(character)
            db.add(models.TVEpisodeGuestcast(episode_id=episode.id, person_id=person.id,   character_id=character.id, self_=item['self'], voice=item['voice']))
        db.commit()
        results['guestcast'] = len(guestcast)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cli tools for app')
    parser.add_argument('--date', action='store', help='date to fetch data')
    parser.add_argument('--country', action='store', help='country to fetch data')
    args = parser.parse_args(sys.argv[1:])
    with SessionLocal() as db:
        models.Base.metadata.create_all(bind=engine, checkfirst=True)
        asyncio.run(_crawl(db, args.date, args.country))