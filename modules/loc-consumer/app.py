import psycopg2
from kafka import KafkaConsumer
import os
import json

k_url = "kafka-service:9092"
k_topic = "locations"

db_user = os.environ["DB_USERNAME"]
db_pass = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_name = os.environ["DB_NAME"]

k_consumer = KafkaConsumer(k_topic, bootstrap_servers=k_url)


def save_loc_to_db(loc):
    conn = psycopg2.connect(
        dbname=db_name,
        port=db_port,
        user=db_user,
        password=db_pass,
        host=db_host,
    )
    cur = conn.cursor()
    p_id = int(loc["person_id"])
    lat, lon = int(loc["latitude"]), int(loc["longitude"])
    qry = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(
        p_id, lat, lon
    )
    cur.execute(qry)
    conn.commit()
    cur.close()
    conn.close()


for msg in k_consumer:
    print(msg)
    m = msg.value.decode("utf-8")
    loc_data = json.loads(m)
    save_loc_to_db(loc_data)
