"""
Cliente do gerenciador de tarefas.

Responsável por toda a interação com o usuário. Envia as ações
(adicionar, remover, listar) para o servidor através do broker,
usando um socket REQ.
"""

import os
import json
import zmq


FRONTEND_ADDRESS = os.environ.get("BROKER_FRONTEND", "tcp://broker:5559")


def exibe_menu():
    print("1. Adicionar tarefa")
    print("2. Remover tarefa")
    print("3. Listar tarefas")
    print("4. Sair")
    return input("Escolha uma opção: ").strip()


def exibe_resposta(resposta):
    if resposta.get("status") != "ok":
        print(f"Erro: {resposta.get('mensagem', 'erro desconhecido')}")
        return

    if "tarefas" in resposta:
        tarefas = resposta["tarefas"]
        if tarefas:
            print("\nTarefas cadastradas:")
            for task_id, descricao in tarefas.items():
                print(f"  [{task_id}] {descricao}")
        else:
            print("Nenhuma tarefa cadastrada.")
    else:
        print(resposta.get("mensagem", "ok"))


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(FRONTEND_ADDRESS)

    print(f"Cliente conectado ao broker em {FRONTEND_ADDRESS}")

    while True:
        opcao = exibe_menu()

        if opcao == "1":
            descricao = input("Descrição da tarefa: ")
            request = {"action": "add", "descricao": descricao}

        elif opcao == "2":
            task_id_str = input("ID da tarefa a remover: ").strip()
            if not task_id_str.isdigit():
                print("ID inválido.")
                continue
            request = {"action": "remove", "id": int(task_id_str)}

        elif opcao == "3":
            request = {"action": "list"}

        elif opcao == "4":
            print("Encerrando cliente...")
            break

        else:
            print("Opção inválida.")
            continue

        socket.send_string(json.dumps(request))
        resposta = json.loads(socket.recv_string())
        exibe_resposta(resposta)

    socket.close()
    context.term()


if __name__ == "__main__":
    main()
