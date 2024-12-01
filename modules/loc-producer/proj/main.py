from concurrent import futures
import grpc
import loc_pb2
import loc_pb2_grpc
from kafka import KafkaProducer as KProducer
import json

kafka_server = "kafka-service:9092"
kafka_topic_name = "locations"
kafka_client = KProducer(bootstrap_servers=kafka_server)

class LocationHandler(loc_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        data = {
            "person_id": int(request.person_id),
            "latitude": float(request.latitude),
            "longitude": float(request.longitude)
        }

        kafka_data = json.dumps(data).encode()
        kafka_client.send(kafka_topic_name, kafka_data)
        kafka_client.flush()
        return loc_pb2.LocMessage(**data)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

loc_pb2_grpc.add_LocationServiceServicer_to_server(
    LocationHandler(), server
)

server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()