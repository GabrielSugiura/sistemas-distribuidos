import os
import json
import zmq


BACKEND_ADDRESS = os.environ.get("BROKER_BACKEND", "tcp://broker:5560")


def processa_requisicao(request, tasks, next_id):
    """Processa uma requisição do cliente e devolve (resposta, next_id)."""

    action = request.get("action")

    if action == "add":
        descricao = request.get("descricao", "").strip()
        if not descricao:
            return {"status": "erro", "mensagem": "Descrição vazia"}, next_id

        task_id = next_id
        tasks[task_id] = descricao
        next_id += 1
        resposta = {
            "status": "ok",
            "mensagem": f"Tarefa {task_id} adicionada com sucesso",
            "id": task_id,
        }

    elif action == "remove":
        task_id = request.get("id")
        if task_id in tasks:
            del tasks[task_id]
            resposta = {"status": "ok", "mensagem": f"Tarefa {task_id} removida"}
        else:
            resposta = {"status": "erro", "mensagem": f"Tarefa {task_id} não encontrada"}

    elif action == "list":
        resposta = {"status": "ok", "tarefas": tasks}

    else:
        resposta = {"status": "erro", "mensagem": f"Ação desconhecida: {action}"}

    return resposta, next_id


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect(BACKEND_ADDRESS)

    print(f"Servidor conectado ao broker em {BACKEND_ADDRESS}")

    tasks = {}
    next_id = 1

    while True:
        mensagem = socket.recv_string()

        try:
            request = json.loads(mensagem)
        except json.JSONDecodeError:
            socket.send_string(json.dumps(
                {"status": "erro", "mensagem": "Requisição inválida (JSON malformado)"}
            ))
            continue

        resposta, next_id = processa_requisicao(request, tasks, next_id)
        socket.send_string(json.dumps(resposta))


if __name__ == "__main__":
    main()