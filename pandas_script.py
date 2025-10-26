import pandas as pd
df = pd.read_csv("pathbase_2025-10-25.csv")

LOCAL_TIME_ZONE = "America/Los_Angeles"
TIME_FRAME_START = pd.Timestamp(2025, 10, 25, 00, tz=LOCAL_TIME_ZONE)
TIME_FRAME_END   = pd.Timestamp(2025, 10, 25, 23, tz=LOCAL_TIME_ZONE)

df = df.dropna()

df['start_at'] = pd.to_datetime(df['start_at'])
df['end_at'] = pd.to_datetime(df['end_at'])

df['start_at'] = df['start_at'].dt.tz_localize("UTC")
df['end_at'] = df['end_at'].dt.tz_localize("UTC")

df['duration'] = df['end_at'] - df['start_at']

df['local_start_at'] = df['start_at'].dt.tz_convert(LOCAL_TIME_ZONE)
df['local_end_at'] = df['end_at'].dt.tz_convert(LOCAL_TIME_ZONE)

df['display_local_start_at'] = df['local_start_at'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['display_local_end_at'] = df['local_end_at'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['display_duration'] = df['duration'].apply(lambda x: (str(x)[7:])[:8])

df = df[df['local_end_at'] >= TIME_FRAME_START]
df = df[df['local_start_at'] <= TIME_FRAME_END]

display_df = df[["action_name", "display_local_start_at", "display_duration"]]

display_df.to_html("jamietest.html")