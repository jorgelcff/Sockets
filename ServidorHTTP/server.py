import socket
import os

def response_ok(body, mimetype):
    """Retorna uma mensagem de resposta com o código 200 OK e o corpo fornecido."""
    return (
        'HTTP/1.1 200 OK\r\n'
        f'Content-Type: {mimetype}\r\n'
        'Connection: close\r\n'
        f'Content-Length: {len(body)}\r\n'
        '\r\n'
        f'{body}'
    )

def response_error(status_code):
    """Retorna uma mensagem de resposta com o código de status fornecido."""
    if status_code == 400:
        return (
            'HTTP/1.1 400 Bad Request\r\n'
            'Connection: close\r\n'
            '\r\n'
            '<html><body><h1>400 Bad Request</h1></body></html>'
        )
    elif status_code == 403:
        return (
            'HTTP/1.1 403 Forbidden\r\n'
            'Connection: close\r\n'
            '\r\n'
            '<html><body><h1>403 Forbidden</h1></body></html>'
        )
    elif status_code == 404:
        return (
            'HTTP/1.1 404 Not Found\r\n'
            'Connection: close\r\n'
            '\r\n'
            '<html><body><h1>404 Not Found</h1></body></html>'
        )
    elif status_code == 505:
        return (
            'HTTP/1.1 505 Version Not Supported\r\n'
            'Connection: close\r\n'
            '\r\n'
            '<html><body><h1>505 Version Not Supported</h1></body></html>'
        )
    else:
        return None

def handle_request(request):
    """Lida com uma requisição HTTP recebida e retorna uma mensagem de resposta."""
    method, path, version = request.split('\r\n')[0].split(' ')
    
    if method != 'GET':
        return response_error(400)

    # Obter o caminho do arquivo solicitado removendo o primeiro caractere '/'

    file_path = f'files/{path[1:]}'
    # Verificar se o arquivo existe e é acessível
    if not os.path.isfile(file_path):
        return response_error(404)

    # Obter o tipo MIME do arquivo
    _, extension = os.path.splitext(file_path)
    mime_types = {
        '.html': 'text/html',
        '.htm': 'text/html',
        '.css': 'text/css',
        '.js': 'text/javascript',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.svg': 'image/svg+xml',
    }
    mimetype = mime_types.get(extension.lower(), 'application/octet-stream')

    # Ler o conteúdo do arquivo
    with open(file_path, 'r') as file:
        body = file.read()

    # Retornar a resposta com o conteúdo do arquivo
    return response_ok(body, mimetype)


def get_file(filename):  
    file_path = f'files/{filename}'
    try:
        with open(file_path, 'rb') as f:
            print(file_path, ' encontrado')
            return f.read()
    except FileNotFoundError:
        print(file_path, ' não encontrado')
        return None

def handle_request_img(request):
    req = request.split(' ')
    method, path = req[0], req[1]
    if method != 'GET':
        return 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
    filename = path[1:]
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.svg'):
        file_content = get_file(filename)
        if file_content is not None:
            response_headers = f'HTTP/1.1 200 OK\r\nContent-Type: {filename}\r\n\r\n'
            response = response_headers.encode() + file_content
        else:
            response = response_error(404).encode()
    else:
        response = response_error(400).encode()
    return response



def run_server(port):
    """Executa um servidor HTTP simples que escuta em um determinado número de porta."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', port))
        s.listen()

        print(f'Servidor rodando em http://localhost:{port}')

        i = 0

        while True:
            i += 1
            conn, addr = s.accept()
            print(f'Conexão de [{i}]{addr[0]}:{addr[1]}')

            request_data = conn.recv(1024)
            req = request_data.decode("utf-8")
            
            try:
                #consultas vazias
                type = req.split()[1]    
                
                if type.endswith('.html') or type.endswith('.htm') or type.endswith('.css') or type.endswith('.js'):
                    msg = handle_request(req).encode()
                elif type.endswith('.png') or type.endswith('.jpg') or type.endswith('.jpeg') or type.endswith('.svg'):
                    msg = handle_request_img(req)
                else:
                    msg = response_error(404).encode()

                conn.sendall(msg)
                print('mensagem enviada:', msg)
            except IndexError:
                pass

            conn.close()

run_server(9999) 