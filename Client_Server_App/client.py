import tkinter as tk
from tkinter import messagebox
import socket
from threading import Thread

HEADER = 64
PORT = 12345
FORMAT = "utf-8"


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Viewer")

        self.label = tk.Label(root, text="Server IP:")
        self.label.pack(pady=10)

        self.server_ip_entry = tk.Entry(root)
        self.server_ip_entry.pack(pady=10)

        self.port_label = tk.Label(root, text="Port:")
        self.port_label.pack(pady=10)

        self.port_entry = tk.Entry(root)
        self.port_entry.pack(pady=10)

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=10)

        self.html_text = tk.Text(root, height=20, width=50)
        self.html_text.pack(pady=10)

    def connect_to_server(self):
        server_ip = self.server_ip_entry.get()
        port = int(self.port_entry.get()) if self.port_entry.get() else PORT

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_addr = (server_ip, port)
            self.client_socket.connect(server_addr)

            # Burda / işaretini sorguya ekleyip çıkararak get istegimizi dynamic ya da ststic yapıyoruz
            request = f"GET / HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
            self.client_socket.sendall(request.encode(FORMAT))

            html_page = self.receive_html_page()



            # HTML sayfasını Tkinter Text widget'ına ekleme
            self.html_text.delete(1.0, tk.END)
            self.html_text.insert(tk.END, html_page.decode(FORMAT))

        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")

    def receive_html_page(self):
        full_html = b""
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            full_html += data
        return full_html


def main():
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()