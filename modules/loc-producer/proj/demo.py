
import grpc
import loc_pb2
import loc_pb2_grpc

# Use local access
channel = grpc.insecure_channel("localhost:5005")
stub = loc_pb2_grpc.LocationServiceStub(channel)

# Create any usr
user_location = loc_pb2.LocationMessage(
    person_id=2,
    latitude=21,
    longitude=7
)
# push it through
response = stub.Create(user_location)