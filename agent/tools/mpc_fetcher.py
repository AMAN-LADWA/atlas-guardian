import requests

TARGET = "3I/ATLAS"

# MPC OBSFILE service (the ONLY reliable one)
MPC_OBSFILE_URL = "https://minorplanetcenter.net/db_search/show_object"

def get_latest_observations(limit=5):
    """
    Fetch raw MPC observation lines for 3I/ATLAS.
    This endpoint ALWAYS returns data because it's HTML-based.
    """

    params = {
        "object_id": TARGET.replace("/", ""),  # MPC removes slash for IDs
        "format": "json"
    }

    try:
        response = requests.get(MPC_OBSFILE_URL, params=params, timeout=10)

        if response.status_code != 200:
            print("Status:", response.status_code)
            return []

        data = response.json()

        # Contains full observation blocks
        obs_block = data.get("obs", [])

        return obs_block[:limit]

    except Exception as e:
        print("Error fetching MPC data:", e)
        return []
