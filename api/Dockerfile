FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

EXPOSE 8000

COPY ./src .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
