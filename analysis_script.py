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

display_rows: list[Display_Row] = []

with Session() as session:
    rows = session.scalars(
        select(ActionSegment)
    ).all()
  
    for row in rows:
        naive_utc_start_at = row.start_at
        naive_utc_end_at = row.end_at

        aware_utc_start_at = naive_utc_start_at.replace(tzinfo=timezone.utc)
        la_start_at = aware_utc_start_at.astimezone(tz=ZoneInfo("America/Los_Angeles"))
        start_at_str = la_start_at.strftime("%Y-%m-%d %H:%M:%S")

        duration_str = ""

        if naive_utc_end_at is None:
            la_end_at = None
        else:
            aware_utc_end_at = naive_utc_end_at.replace(tzinfo=timezone.utc)
            la_end_at = aware_utc_end_at.astimezone(tz=ZoneInfo("America/Los_Angeles"))
            end_at_str = la_end_at.strftime("%Y-%m-%d %H:%M:%S")
            duration = aware_utc_end_at - aware_utc_start_at
            duration_str = str(duration)
        
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

