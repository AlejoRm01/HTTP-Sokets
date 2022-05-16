from socket import gethostbyname, socket, AF_INET, SOCK_STREAM
from parser import MyHTMLParser 
import urllib.request 
import os

HTTP_HEADER_DELIMITER = b'\r\n\r\n'
CONTENT_LENGTH_FIELD = b'Content-Length:'
HTTP_PORT = 80
ONE_BYTE_LENGTH = 1

def request(host, path, method='GET'):
    
    r =  '{} {} HTTP/1.1\nHost: {}\r\n\r\n'.format(method, path, host)

    return r.encode()
    
def response(sock):

    header = bytes() 
    chunk = bytes()

    try:
        while HTTP_HEADER_DELIMITER not in header:
            chunk = sock.recv(ONE_BYTE_LENGTH)
            if not chunk:
                break
            else:
                header += chunk
    except socket.timeout:
        pass

    return header  

def content_length(header):

    for line in header.split(b'\r\n'):
        if CONTENT_LENGTH_FIELD in line:
            return int(line[len(CONTENT_LENGTH_FIELD):])
    return 0

def get_body(sock, length):

    body = bytes()
    data = bytes()

    while True:
        data = sock.recv(length)
        if len(data)<=0:
            break
        else:
            body += data

    return body 

def write_body(name_file, extension, body):

    if not(os.path.exists('Files')): 
        os.mkdir('Files')

    try:
        file = open('Files/{}.{}'.format(name_file, extension), 'w+')
        file.write(body.decode('latin-1'))
        file.close()
    except:
        return 0
    return 1

def parser_body(body):
    
    parser = MyHTMLParser()
    parser.feed(body.decode('latin-1'))

def main():
    
    host = input('\nIngresa el host: ')
    path = input('Ingresa el Path : ')
    
    extension = path.rfind('.')
    extension = path[extension+1:]
    
    print(f'> Extension del archivo que descargaras: {extension}')
    
    name_file = 'file_html'
    
    print(f'\n# Recibiendo informacion de http://{host}{path}')
    ip_address = gethostbyname(host)
    print(f'> Servidor remoto {host} direccion ip {ip_address}')

    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip_address, 80))
    print(f'> Conexion TCP con {ip_address}:{80} establecida')

    http_get_request = request(host, path)
    urllib.request.urlretrieve('http://{}{}'.format(host, path), 'Files/{}.{}'.format(name_file, extension))
    print('\n# HTTP request ({} bytes)'.format(len(http_get_request)))
    print(http_get_request)     
    sock.sendall(http_get_request)
 
    header = response(sock)
    print(type(header))
    print('\n# HTTP Response cabecera ({} bytes)'.format(len(header)))
    print(header)

    length = content_length(header)
    print('\n# Largo del cuerpo')
    print(f"{length} bytes")

    body = get_body(sock, length)

    if(len(body) > 1):

        print('\n# Cuerpo ({} bytes)'.format(len(body)))
        print(body)

        wfile = write_body(name_file, 'html', body)

        if wfile == 1: 
            print('\n# Archivo guardado')
            print(f'\n>  Parser del html')
            print('\n')
            parser_body(body)
        else: 
            print('\n# Error guardando el archivo') 
        
            
    else:
        print('\n# El archivo no tiene cuerpo ({} bytes)'.format(len(body)))



if __name__ == '__main__':
    main()
