import requests
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from config import API_TEMPLATE, REGION_COORDS

def retrieve_json(url: str):
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()

def ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def save_json(obj: dict, path: str):
    ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"), indent=2)

def hourly_json_to_dataframe(obj: dict, region: str) -> pd.DataFrame:
    """
    Flatten the 'hourly' payload into a DataFrame and attach metadata.
    Assumes all hourly arrays have the same length and align with 'time'.
    """
    hourly = obj.get("hourly", {})
    if "time" not in hourly:
        raise ValueError("JSON payload has no 'hourly.time' field")

    df = pd.DataFrame(hourly)
    # parse timestamps
    df["time"] = pd.to_datetime(df["time"])

    # attach useful metadata columns
    df["region"] = region
    df["latitude"] = obj.get("latitude")
    df["longitude"] = obj.get("longitude")
    df["timezone"] = obj.get("timezone")
    df["utc_offset_seconds"] = obj.get("utc_offset_seconds")

    # put time first
    cols = ["time", "region", "latitude", "longitude", "timezone", "utc_offset_seconds"]
    other = [c for c in df.columns if c not in cols]
    df = df[cols + other]

    return df

def save_csv(df: pd.DataFrame, path: str):
    ensure_dir(path)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")

    for region, (latitude, longitude) in REGION_COORDS.items():
        url = API_TEMPLATE.format(latitude=latitude, longitude=longitude,
                                  start_date=start_date, end_date=end_date)

        # file paths
        base = f"data/{region}_{start_date}_to_{end_date}"
        json_path = f"{base}.json"
        csv_path = f"{base}.csv"

        try:
            obj = retrieve_json(url)
            save_json(obj, json_path)
            df = hourly_json_to_dataframe(obj, region)
            save_csv(df, csv_path)
            print(f"Saved {json_path} and {csv_path}")
        except Exception as e:
            print(f"[{region}] failed: {e}")
