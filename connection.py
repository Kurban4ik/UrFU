import socket

host = "192.168.1.1"
port = 2001

def create_connection(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    return connection

def send_command(connection, command):
    try:
        connection.sendall(command)
        return True
    except socket.error as e:
        print(f"Ошибка сокета: {e}")
        return False

def close_connection(connection):
    connection.close()
