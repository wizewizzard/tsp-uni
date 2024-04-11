python --version 2>NUL
if errorlevel 1 goto errorNoPython

mkdir .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

echo.
echo Successfully initialized environment and installed all dependencies.

:errorNoPython
echo.
echo Error^: Python not installed