FROM python:3.8.10

LABEL key="Elias"

RUN apt-get update

RUN pip install -r requirements.txt

CMD ["python", "california_housing.ipynb"]
