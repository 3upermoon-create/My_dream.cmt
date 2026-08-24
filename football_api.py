import requests
from datetime import date
from config import API_KEY, API_URL

def api_get(endpoint, params=None):
    if not API_KEY:
        raise RuntimeError("API_FOOTBALL_KEY is missing. Add it in Render Environment Variables.")
    r = requests.get(f"{API_URL}/{endpoint}",
        headers={"x-apisports-key": API_KEY},
        params=params or {}, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("errors"):
        raise RuntimeError(str(data["errors"]))
    return data

def get_today_fixtures(timezone="Africa/Dar_es_Salaam"):
    return api_get("fixtures", {"date": date.today().isoformat(), "timezone": timezone})

def get_predictions(fixture_id):
    return api_get("predictions", {"fixture": fixture_id})

def get_odds(fixture_id):
    return api_get("odds", {"fixture": fixture_id})

def get_injuries(fixture_id):
    return api_get("injuries", {"fixture": fixture_id})

def get_lineups(fixture_id):
    return api_get("fixtures/lineups", {"fixture": fixture_id})

def get_statistics(fixture_id):
    return api_get("fixtures/statistics", {"fixture": fixture_id})
