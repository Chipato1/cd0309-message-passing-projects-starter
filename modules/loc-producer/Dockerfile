# newer image because of gcc, g++
FROM python:3.9-alpine


WORKDIR /proj

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

ENTRYPOINT [ "python", "proj/main.py" ]