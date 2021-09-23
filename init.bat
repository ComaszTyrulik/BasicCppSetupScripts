@set cwd=%~dp0

python -m venv "%cwd%.env"
 "%cwd%.env\Scripts\activate.bat"^
 & python -m pip install -r "%cwd%requirements.txt"^
 & python -m pip install --upgrade pip^
 & conan remote add -i 0 conancenter https://center.conan.io
 & python "%cwd%init_project.py"^
 & "%cwd%.env\Scripts\deactivate.bat"
