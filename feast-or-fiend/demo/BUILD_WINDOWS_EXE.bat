@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  set "PY=py -3"
) else (
  set "PY=python"
)
%PY% --version >nul 2>nul
if errorlevel 1 (
  echo Install Python 3.10+ first, or download the prebuilt EXE from GitHub Actions.
  pause
  exit /b 1
)
%PY% -m pip install --upgrade pyinstaller
if errorlevel 1 (
  echo Could not install PyInstaller. Check your internet connection.
  pause
  exit /b 1
)
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name FeastOrFiend --add-data "game\artpack.b64;." game\main.py
if errorlevel 1 (
  echo EXE build failed.
  pause
  exit /b 1
)
echo.
echo Standalone game created at dist\FeastOrFiend.exe
pause