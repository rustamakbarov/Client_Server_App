import socket
import threading
from datetime import date, datetime

HEADER = 64
PORT = 1234
FORMAT = "utf-8"

def generate_dynamic_html():
    # Burada istediğiniz dinamik HTML içeriğini oluşturabilirsiniz.
    dynamic_content = f"<html><body><h1>Merhaba Dünya!</h1><p>{datetime.now()}</p></body></html>"
    return dynamic_content.encode(FORMAT)

def handle_request(client_socket, client_address):
    try:
        rd = client_socket.recv(1000).decode()
        pieces = rd.split("\n")
        if len(pieces) > 0:
            print(pieces)
            data = b"HTTP/1.1 200 OK\r\n"
            data += b"Content-Type: text/html; charset=utf-8\r\n"
            str_today = date.today().strftime("%d/%m/%Y")
            str_now = datetime.now().strftime("%H:%M:%S")
            str_date = str_today + " " + str_now + " GMT+3"
            print(str_date)
            data += str_date.encode(FORMAT)
            data += b"\r\n"

            document = pieces[0].split()[1]
            if document == '/':
                # Eğer URL "/" ise, dinamik HTML içeriğini gönder
                data += generate_dynamic_html()
                client_socket.sendall(data)
            else:
                with open("hello.txt", "rb") as file1:
                     data_static = file1.read()
                    # data += file1.read()
                     client_socket.sendall(data_static)
            client_socket.shutdown(socket.SHUT_WR)
    except OSError as e:
        print("ERR_404")
        data = b"HTTP/1.1 404 Not Found\r\n"
        data += b"Content-Type: text/html; charset=utf-8\r\n"
        data += b"Date: Wed, 21 Oct 2015 07:28:00 GMT\r\n"
        data += b"\r\n"
        with open("files/" + "404.html", "rb") as file1:
            data += file1.read()
        client_socket.sendall(data)
        client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        print("\nShutting down...\n")
    except Exception as exc:
        print("Error:\n")
        print(exc)

class Server:
    time = 0

    def __init__(self, time):
        self.time = time

    def __str__(self):
        return f"{self.time}"

    def start_server(self):
        server_ip = socket.gethostbyname(socket.gethostname())
        server_addr = (server_ip, PORT)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(server_addr)
        server_socket.listen(5)

        print(f"[LISTENING] Server is listening on {server_ip}")
        print(f'Access http://{server_ip}:{PORT}')
        while 1:
            (client_socket, client_address) = server_socket.accept()
            thread = threading.Thread(target=handle_request, args=(client_socket, client_address))
            thread.start()

server = Server(0)
server.start_server()