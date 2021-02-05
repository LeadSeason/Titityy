@echo off
:Start
git pull
TIMEOUT /T 1
py bot.py
TIMEOUT /T 1
GOTO:Start§