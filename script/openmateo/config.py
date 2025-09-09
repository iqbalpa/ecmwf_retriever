API_TEMPLATE = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,precipitation,rain,snowfall,wind_speed_10m,wind_speed_100m&models=ecmwf_ifs025&start_date={start_date}&end_date={end_date}&timezone=auto"

REGION_COORDS = {
    "hokkaido": (43.432, 142.9347),
    "tohoku": (35.8188, 139.5714),
    "tokyo": (35.6895, 139.6917),
    "chubu": (35.4338, 140.2797),
    "hokuriku": (37.92, 139.04),
    "kansai": (34.68, 135.65),
    "chugoku": (35.04, 132.27),
    "shikoku": (33.75, 133.5),
    "kyushu": (32.4294, 130.991),
}
