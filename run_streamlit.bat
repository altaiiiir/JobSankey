@echo off
:: Activate the virtual environment if one exists in the current directory
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo No virtual environment detected. Make sure Streamlit is installed in your global Python environment or activate your virtual environment manually.
)

:: Check if Streamlit is installed
python -m streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Streamlit is not installed in the current environment. Please install it first with 'pip install streamlit'.
    exit /b
)

:: Run the Streamlit app in reload mode from the current directory
echo Starting the Streamlit app in reload mode...
python -m streamlit run "%cd%\main.py" --server.runOnSave true
