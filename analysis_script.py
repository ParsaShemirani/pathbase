import os
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import csv
import copy

from sqlalchemy import select
from sqlalchemy.orm import load_only
from dotenv import load_dotenv

from connection import Session
from models import ActionSegment

### Modify these variables:
local_zoneinfo = ZoneInfo("America/Los_Angeles")

local_timeframe_start = datetime(year=2025, month=10, day=9, hour=0, tzinfo=local_zoneinfo)
local_timeframe_end = datetime(year=2025, month=10, day=10, hour=0, tzinfo=local_zoneinfo)

###

load_dotenv()
ANALYSIS_OUTPUT_DIRECTORY = os.getenv("ANALYSIS_OUTPUT_DIRECTORY")
if ANALYSIS_OUTPUT_DIRECTORY is None:
    raise(ValueError("Analysis output directory not found from .env"))
ANALYSIS_OUTPUT_DIRECTORY_PATH = Path(ANALYSIS_OUTPUT_DIRECTORY)

@dataclass
class Display_Row:
    id: int
    action_name: str
    start_at: str
    end_at: str
    duration: str



def format_hms(td: timedelta) -> str:
    total = int(td.total_seconds())
    h, r = divmod(total, 3600)
    m, s = divmod(r, 60)
    return f"{h:02}:{m:02}:{s:02}"

display_rows: list[Display_Row] = []
start_times: list[datetime] = []
end_times: list[datetime] = []
timeframe_recorded_duration = timedelta()

with Session() as session:
    rows = session.scalars(
        select(ActionSegment)
    ).all()

    if rows[-1].end_at is None:
        del rows[-1]

    #timeframe_start_at = rows[0].start_at
    #timeframe_end_at = rows[-1].end_at

    for row in rows:
        naive_utc_start_at = row.start_at
        naive_utc_end_at = row.end_at

        aware_utc_start_at = naive_utc_start_at.replace(tzinfo=timezone.utc)
        aware_utc_end_at = naive_utc_end_at.replace(tzinfo=timezone.utc)

        local_start_at = aware_utc_start_at.astimezone(tz=ZoneInfo("America/Los_Angeles"))
        local_end_at = aware_utc_end_at.astimezone(tz=ZoneInfo("America/Los_Angeles"))

        if local_start_at < local_timeframe_start and local_end_at < local_timeframe_start:
            continue
        if local_end_at > local_timeframe_end and local_start_at > local_timeframe_end:
            continue
        
        start_times.append(local_start_at)
        end_times.append(local_end_at)

        start_at_str = local_start_at.strftime("%Y-%m-%dT%H:%M:%S")
        end_at_str = local_end_at.strftime("%Y-%m-%dT%H:%M:%S")
        
        duration = aware_utc_end_at - aware_utc_start_at
        duration_str = str(duration)
        timeframe_recorded_duration += duration
        
        display_row = Display_Row(
            id=row.id,
            action_name=row.action_name,
            start_at=start_at_str,
            end_at=end_at_str,
            duration=duration_str,
        )
        display_rows.append(display_row)

# Find next available file number
base_name = "output"
extension = ".csv"
counter = 1
while True:
    candidate = ANALYSIS_OUTPUT_DIRECTORY_PATH / f"{base_name}{counter}{extension}"

    if not candidate.exists():
        output_file_path = candidate
        break
    counter += 1

# CSV output
with open(output_file_path, 'w', newline='') as csvfile:
    fieldnames = ['id', 'action_name', 'start_at', 'end_at', 'duration']
    writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for dr in display_rows:
        writer.writerow(rowdict=asdict(dr))

timeframe_total_duration = max(end_times) - min(start_times)
timeframe_unrecorded_duration = timeframe_total_duration - timeframe_recorded_duration
timeframe_percentage_recorded = 100 * (timeframe_recorded_duration.total_seconds() / timeframe_total_duration.total_seconds())
timeframe_percentage_unrecorded = 100 * (timeframe_unrecorded_duration.total_seconds() / timeframe_total_duration.total_seconds())

recorded_stats = ""
recorded_stats += f"""\
Timeframe total duration: {format_hms(td=timeframe_total_duration)}
Timeframe recorded duration: {format_hms(td=timeframe_recorded_duration)}
Timeframe unrecorded duration: {format_hms(td=timeframe_unrecorded_duration)}

Timeframe recorded percentage: {timeframe_percentage_recorded}%
Timeframe unrecorded percentage: {timeframe_percentage_unrecorded}%
"""

with open(output_file_path, "a") as f:
    f.write(3*"\n")
    f.write(recorded_stats)