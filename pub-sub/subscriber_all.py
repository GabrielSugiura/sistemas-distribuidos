import zmq

context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.setsockopt_string(zmq.SUBSCRIBE, "")  # string vazia = recebe todos os topicos
sub.connect("tcp://proxy:5556")

while True:
    message = sub.recv_string()
    print(f"message: {message}", flush=True)

sub.close()
context.close()
