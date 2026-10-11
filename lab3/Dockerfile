FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pyzmq

COPY . .

# O comando efetivo (broker.py, servidor.py ou cliente.py) é
# definido em docker-compose.yaml para cada serviço.
CMD ["python", "broker.py"]
