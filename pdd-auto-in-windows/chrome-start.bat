@echo off
setlocal

echo Checking Chrome path...

set "chrome32=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
set "chrome64=C:\Program Files\Google\Chrome\Application\chrome.exe"

if exist "%chrome32%" (
    set "chrome=%chrome32%"
) else if exist "%chrome64%" (
    set "chrome=%chrome64%"
) else (
    echo Chrome executable not found in standard locations.
    pause
    exit /b 1
)

echo Starting Chrome (with remote debugging port 9222)...

start "" "%chrome%" ^
--remote-debugging-port=9222 ^
--user-data-dir="C:/Users/OrekiYuta/AppData/Local/Google/Chrome/User Data/"

echo Chrome has started. Selenium can connect to 127.0.0.1:9222
pause
