import zmq
import random
from time import sleep

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

TOPIC = "numero"

while True:
    numero = random.randint(1, 6)
    message = f"{TOPIC} {numero}"
    print(f"message: {message}", flush=True)
    pub.send_string(message)
    sleep(1)

pub.close()
context.close()
