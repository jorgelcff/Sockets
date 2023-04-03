import socket


def get_file(filename):
    
    file_path = f'ServidorHTTP/files/{filename}'
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return None


def handle_request(request):
    req = request.split(' ')
    method, path = req[0], req[1]
    if method != 'GET':
        return 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
    filename = path[1:]
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.svg'):
        file_content = get_file(filename)
        if file_content is not None:
            response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\n\r\n'.format(filename)
            response = response_headers.encode() + file_content
        else:
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
    else:
        response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
    return response


HOST = 'localhost'
PORT = 8000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen()
while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024).decode()
    response = handle_request(request)
    client_socket.send(response)
    client_socket.close()
