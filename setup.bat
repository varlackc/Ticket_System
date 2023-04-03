: @echo OFF

: Explain the configurations to the user
echo setup the virtual environment

echo Python 3.7 is expected
echo Current version of python:
python.exe --version

: Create the local environment
echo Create the local environment 
python.exe -m venv localEnv

: Activate the local environment
echo Activate the local environment
CALL localEnv\Scripts\activate.bat

: Install the requirements for the project
echo Install the required dependencies for the project
pip install -r requirements.txt