from app.utils import flat_object
import json

def test_flat_object():
    obj = {
        "id": 1,
        "url": "https://www.tvmaze.com/people/1/mike-vogel",
        "name": "Mike Vogel",
        "schedule": {
            "time": "16:00",
            "days": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ]
        },
        "country": {
            "name": "United States",
            "code": "US",
            "timezone": "America/New_York"
        },
        "birthday": "1979-07-17",
        "deathday": None,
        "gender": "Male",
        "image": {
            "medium": "https://static.tvmaze.com/uploads/images/medium_portrait/0/1815.jpg",
            "original": "https://static.tvmaze.com/uploads/images/original_untouched/0/1815.jpg"
        },
        "updated": 1700438025,
        "_links": {
            "self": {
                "href": "https://api.tvmaze.com/people/1"
            }
        },
        "self": False,
    }
    flat_obj = flat_object(obj)
    assert flat_obj['schedule_time'] == '16:00'
    assert flat_obj['schedule_days'] == json.dumps(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"])
    assert flat_obj['country_name'] == 'United States'
    assert flat_obj['country_code'] == 'US'
    assert flat_obj['links_self_href'] == 'https://api.tvmaze.com/people/1'
    assert flat_obj['self_'] == False