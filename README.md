# pathbase

## Instructions
- Download the repo with "git clone https://github.com/ParsaShemirani/pathbase.git"
- Create a virtual environment in the folder with 'python3 -m venv .venv'
- Activate the venv via "source .venv/bin/activate"
- Download package dependencies via "pip install -r requirements.txt"
- Create a file ".env" where the variable "DATABASE_PATH" is set.
- Create the database via "python create_db.py"
- Run with fastapi dev app.py --host 0.0.0.0

### Sample .env file:
DATABASE_PATH=/Users/jameswebb/pathbase.db

## Analysis scripts
To get the output from the analysis scripts,
define 'ANALYSIS_OUTPUT_DIRECTORY' in the .env file.