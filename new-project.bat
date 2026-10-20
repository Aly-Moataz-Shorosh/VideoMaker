@echo off
chcp 65001 >nul
echo.
echo   1 = reel-h        (horizontal reel from your EDITED video)
echo   2 = youtube       (full YouTube video from your EDITED video, any length)
echo   3 = shorts        (shorts from an EDITED long video or a YouTube link)
echo   4 = shorts-raw    (shorts from RAW footage: Claude cuts silences and mistakes too)
echo   5 = faceless      (voice only, no face)
echo.
set /p T=Type number (1-5): 
if "%T%"=="1" set TYPE=reel-h
if "%T%"=="2" set TYPE=youtube
if "%T%"=="3" set TYPE=shorts
if "%T%"=="4" set TYPE=shorts-raw
if "%T%"=="5" set TYPE=faceless
if "%TYPE%"=="" (echo Wrong number & pause & exit /b)
set /p NAME=Short name in English (example: genjutsu): 
if "%NAME%"=="" set NAME=video
for /f %%d in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set D=%%d
set P=%~dp0projects\%D% %TYPE% %NAME%
xcopy "%~dp0projects\_template" "%P%\" /E /I /Q >nul
echo Created: %P%
explorer "%P%"
