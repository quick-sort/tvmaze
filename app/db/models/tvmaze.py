from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, ForeignKey, DateTime, Text
import datetime
from typing import Optional, List
from .base import Base

class TVWebChannel(Base):
    __tablename__ = "tv_web_channel"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(128))
    country_name: Mapped[Optional[str]] = mapped_column(String(128))
    country_code: Mapped[Optional[str]] = mapped_column(String(128))
    country_timezone: Mapped[Optional[str]] = mapped_column(String(128))
    officialSite: Mapped[Optional[str]] = mapped_column(String(1024))
    
class TVNetwork(Base):
    __tablename__ = "tv_network"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    country_name: Mapped[Optional[str]] = mapped_column(String(128))
    country_code: Mapped[Optional[str]] = mapped_column(String(128))
    country_timezone: Mapped[Optional[str]] = mapped_column(String(128))
    officialSite: Mapped[Optional[str]] = mapped_column(String(1024))

class TVCharacter(Base):
    __tablename__ = 'tv_character'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[Optional[str]] = mapped_column(String(1024))
    name: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    image_medium: Mapped[Optional[str]] = mapped_column(String(1024))
    image_original: Mapped[Optional[str]] = mapped_column(String(1024))
    links_self_href: Mapped[Optional[str]] = mapped_column(String(1024))
    guestcast: Mapped[List['TVEpisodeGuestcast']] = relationship(back_populates="character")

class TVPeople(Base):
    __tablename__ = "tv_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[Optional[str]] = mapped_column(String(1024))
    name: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    country_name: Mapped[Optional[str]] = mapped_column(String(128))
    country_code: Mapped[Optional[str]] = mapped_column(String(128))
    country_timezone: Mapped[Optional[str]] = mapped_column(String(128))
    birthday: Mapped[Optional[str]]
    deathday: Mapped[Optional[str]]
    gender: Mapped[Optional[str]] = mapped_column(String(128))
    image_medium: Mapped[Optional[str]] = mapped_column(String(1024))
    image_original: Mapped[Optional[str]] = mapped_column(String(1024))
    links_self_href: Mapped[Optional[str]] = mapped_column(String(1024))
    updated: Mapped[Optional[str]]
    guestcast: Mapped[List['TVEpisodeGuestcast']] = relationship(back_populates="person")


class TVEpisodeGuestcast(Base):
    __tablename__ = "tv_episode_guest_cast"

    id: Mapped[int] = mapped_column(primary_key=True)
    episode_id: Mapped[int] = mapped_column(ForeignKey('tv_episode.id'), index=True)
    episode: Mapped["TVEpisode"] = relationship(back_populates="guestcast")
    person_id: Mapped[int] = mapped_column(ForeignKey('tv_people.id'), index=True)
    person: Mapped['TVPeople'] = relationship(back_populates="guestcast")
    character_id: Mapped[int] = mapped_column(ForeignKey('tv_character.id'), index=True)
    character: Mapped['TVCharacter'] = relationship(back_populates="guestcast")
    voice: Mapped[bool] = mapped_column(default=False)
    self_: Mapped[bool] = mapped_column(default=False)

class TVShow(Base):
    __tablename__ = "tv_show"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[Optional[str]] = mapped_column(String(1024))
    name: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    type: Mapped[Optional[str]] = mapped_column(String(128))
    language: Mapped[Optional[str]] = mapped_column(String(128))
    genres: Mapped[Optional[str]] = mapped_column(String(1024))
    status: Mapped[Optional[str]] = mapped_column(String(128))
    runtime: Mapped[Optional[int]]
    averageRuntime: Mapped[Optional[int]]
    premiered: Mapped[Optional[str]]
    ended: Mapped[Optional[str]]
    officialSite: Mapped[Optional[str]] = mapped_column(String(1024))
    schedule_time: Mapped[Optional[str]]
    schedule_days: Mapped[Optional[str]] = mapped_column(String(1024))
    rating_average: Mapped[Optional[float]]
    weight: Mapped[Optional[int]]
    network_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tv_network.id"))
    webChannel_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tv_web_channel.id"))
    dvdCountry_name: Mapped[Optional[str]] = mapped_column(String(128))
    dvdCountry_code: Mapped[Optional[str]] = mapped_column(String(12))
    dvdCountry_timezone: Mapped[Optional[str]] = mapped_column(String(32))
    externals_tvrage: Mapped[Optional[int]]
    externals_thetvdb: Mapped[Optional[int]]
    externals_imdb: Mapped[Optional[str]] = mapped_column(String(128))
    image_medium: Mapped[Optional[str]] = mapped_column(String(1024))
    image_original: Mapped[Optional[str]] = mapped_column(String(1024))
    summary: Mapped[Optional[str]] = mapped_column(Text)
    updated: Mapped[Optional[str]]
    links_self_href: Mapped[Optional[str]] = mapped_column(String(1024))
    links_previousepisode_href: Mapped[Optional[str]] = mapped_column(String(1024))
    links_nextepisode_href: Mapped[Optional[str]] = mapped_column(String(1024))
    episodes: Mapped[List["TVEpisode"]] = relationship(back_populates="show")


class TVEpisode(Base):
    __tablename__ = "tv_episode"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[Optional[str]] = mapped_column(String(1024))
    name: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    season: Mapped[Optional[int]]
    number: Mapped[Optional[int]] 
    type: Mapped[Optional[str]] = mapped_column(String(128))
    airdate: Mapped[Optional[str]] = mapped_column(index=True)
    airtime: Mapped[Optional[str]]
    airstamp: Mapped[Optional[str]]
    runtime: Mapped[Optional[int]]
    rating_average: Mapped[Optional[float]]
    image_medium: Mapped[Optional[str]] = mapped_column(String(1024))
    image_original: Mapped[Optional[str]] = mapped_column(String(1024))
    summary: Mapped[Optional[str]] = mapped_column(Text)
    links_self_href: Mapped[Optional[str]] = mapped_column(String(1024))
    links_show_href: Mapped[Optional[str]] = mapped_column(String(1024))
    show_id: Mapped[int] = mapped_column(ForeignKey("tv_show.id"), index=True)
    show: Mapped["TVShow"] = relationship(back_populates="episodes")
    likes: Mapped[Optional[int]] = mapped_column(default=0)
    guestcast: Mapped[List['TVEpisodeGuestcast']] = relationship(back_populates="episode")