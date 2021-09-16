@set cwd=%~dp0
@%cwd%.env\Scripts\activate.bat & %* & %cwd%.env\Scripts\deactivate.bat
