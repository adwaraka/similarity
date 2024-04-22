FROM python:3.10.0-alpine

WORKDIR /code
ADD similarity.py .

RUN pip install numpy pyinflect
CMD ["python3", "similarity.py"]
