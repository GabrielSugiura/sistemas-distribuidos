import zmq
from time import time, sleep

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

TOPIC = "hora"

while True:
    hora = str(time())
    message = f"{TOPIC} {hora}"
    print(f"message: {message}", flush=True)
    pub.send_string(message)
    sleep(1)

pub.close()
context.close()
