@set cwd=%~dp0
@%cwd%.env\Scripts\activate.bat & python %* & %cwd%.env\Scripts\deactivate.bat