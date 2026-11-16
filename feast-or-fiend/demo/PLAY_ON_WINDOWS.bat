@echo off
setlocal
cd /d "%~dp0game"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 main.py
  goto :end
)
where python >nul 2>nul
if not errorlevel 1 (
  python main.py
  goto :end
)
echo Python was not found. Install Python 3.10+ from python.org with Tkinter enabled.
echo Or download the standalone EXE from this repository's GitHub Actions artifacts.
pause
:end