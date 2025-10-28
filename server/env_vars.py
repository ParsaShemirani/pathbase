import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = Path(os.getenv("DATABASE_PATH"))
ANALYSIS_OUTPUT_DIR = Path(os.getenv("ANALYSIS_OUTPUT_DIR"))