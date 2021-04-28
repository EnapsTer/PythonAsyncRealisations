import socket
from select import select  # checks changes in fd's and returns their args (read write errors)


# accept client and add client socket to monitoring list
def accept_client(server_socket: socket.socket, monitoring_sockets: list) -> None:
    client_socket, addr = server_socket.accept()
    monitoring_sockets.append(client_socket)


# send received message to the client and close client socket if request not received
def send_message_to_client(client_socket: socket.socket) -> None:
    request = client_socket.recv(2048)

    if request:
        response = f'Hello {request.decode()}'.encode()
        client_socket.send(response)
    else:
        client_socket.close()

# start event loop and call server functions
def event_loop(server_socket: socket.socket, monitoring_sockets: list) -> None:
    while True:
        ready_sockets, _, _ = select(monitoring_sockets, [], [])

        for sock in ready_sockets:
            if sock is server_socket:
                accept_client(server_socket, monitoring_sockets)
            else:
                send_message_to_client(sock)


def main():
    monitoring_sockets = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    monitoring_sockets.append(server_socket)
    event_loop(server_socket, monitoring_sockets)


if __name__ == '__main__':
    main()
