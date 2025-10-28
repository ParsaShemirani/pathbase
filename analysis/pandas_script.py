import pandas as pd

from server.env_vars import DATABASE_PATH, ANALYSIS_OUTPUT_DIR

df = pd.read_csv(DATABASE_PATH)

LOCAL_TIME_ZONE = "America/Los_Angeles"
TIME_FRAME_START = pd.Timestamp(2025, 10, 27, 00, tz=LOCAL_TIME_ZONE)
TIME_FRAME_END   = pd.Timestamp(2025, 10, 27, 23, tz=LOCAL_TIME_ZONE)

df = df.dropna()

df['dt_start_at'] = pd.to_datetime(df['str_start_at'], utc=True)
df['dt_end_at'] = pd.to_datetime(df['str_end_at'], utc=True)

df['duration'] = df['dt_end_at'] - df['dt_start_at']

df['local_dt_start_at'] = df['dt_start_at'].dt.tz_convert(LOCAL_TIME_ZONE)
df['local_dt_end_at'] = df['dt_end_at'].dt.tz_convert(LOCAL_TIME_ZONE)

df['display_local_start_at'] = df['local_dt_start_at'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['display_local_end_at'] = df['local_dt_end_at'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['display_duration'] = df['duration'].apply(lambda x: (str(x)[7:])[:8])

df = df[df['local_dt_end_at'] >= TIME_FRAME_START]
df = df[df['local_dt_start_at'] <= TIME_FRAME_END]

display_df = df[["action_name", "display_local_start_at", "display_duration"]]
print("JAMIE")
print(display_df.head())
display_df.to_html(ANALYSIS_OUTPUT_DIR / "jamietest.html")