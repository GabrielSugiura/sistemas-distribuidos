import zmq


FRONTEND_PORT = 5559  # porta onde os clientes se conectam (REQ)
BACKEND_PORT = 5560   # porta onde os servidores se conectam (REP)


def main():
    context = zmq.Context()

    frontend = context.socket(zmq.ROUTER)
    frontend.bind(f"tcp://*:{FRONTEND_PORT}")

    backend = context.socket(zmq.DEALER)
    backend.bind(f"tcp://*:{BACKEND_PORT}")

    print(f"Broker rodando: frontend=tcp://*:{FRONTEND_PORT} "
          f"backend=tcp://*:{BACKEND_PORT}")

    try:
        zmq.proxy(frontend, backend)
    except KeyboardInterrupt:
        pass
    finally:
        frontend.close()
        backend.close()
        context.term()


if __name__ == "__main__":
    main()