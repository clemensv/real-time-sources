@echo off
echo Installing ticketmaster_amqp_producer_amqp_producer...

REM Check if poetry is installed
where poetry >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Poetry is not installed. Installing Poetry...
    powershell -Command "& {(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -}"
)

REM Install dependencies
poetry install

echo Installation complete!
echo Run 'poetry run pytest' to run tests