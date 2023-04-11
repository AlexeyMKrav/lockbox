python -m venv venv
./venv/Scripts/Activate.ps1
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
Get-Command python
#pip freeze > requirements.txt