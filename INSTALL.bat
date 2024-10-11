@echo off

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Copying .env-example to .env...
copy .env-example .env

echo Please edit the .env file to add your TG_BOT_TOKEN and CHAT_ID.
echo Make sure that you create session file in /sessions folder before starting the bot.
pause