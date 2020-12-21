python -m venv .env
 .env\Scripts\activate.bat^
 & python -m pip install -r requirements.txt^
 & python -m pip install --upgrade pip^
 & python init_project.py^
 & .env\Scripts\deactivate.bat
