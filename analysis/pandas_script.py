import pandas as pd


df = pd.read_csv("/Users/parsahome/Downloads/segments_2025-11-05.csv")

LOCAL_TIME_ZONE = "America/Los_Angeles"
TIME_FRAME_START = pd.Timestamp(2025, 11, 4, 00, tz=LOCAL_TIME_ZONE)
TIME_FRAME_END   = pd.Timestamp(2025, 11, 4, 23, tz=LOCAL_TIME_ZONE)

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

display_df = df[["name", "display_duration", "display_local_start_at"]]
print("JAMIE")
print(display_df.head())
html = display_df.to_html()


styled_html = f"""
<style>
  body {{
    background-color: black;
    color: white;
  }}
  table {{
    background-color: black;
    color: white;
    border-color: white;
  }}
  th, td {{
    border-color: white !important;
  }}
</style>
{html}
"""
with open("jamietest.html", "w") as f:
    f.write(styled_html)


display_df.to_csv("jamietest.csv")
