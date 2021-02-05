@echo off
IF Exist "shutdown" (
    del shutdown
)

:Start
IF Exist "shutdown" GOTO:exit
git pull
py bot.py
GOTO:Start
:exit