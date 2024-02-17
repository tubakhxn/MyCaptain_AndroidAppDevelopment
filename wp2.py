import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ChatApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Application")
        
        self.chat_box = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_box.pack(expand=True, fill=tk.BOTH)
        
        self.message_entry = tk.Entry(master)
        self.message_entry.pack(expand=True, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.start_listening()
    
    def start_listening(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', 12345))
        self.server_socket.listen(5)
        
        threading.Thread(target=self.accept_connections).start()
    
    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
    
    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.display_message(message)
            except ConnectionResetError:
                break
        client_socket.close()
    
    def send_message(self, event=None):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.display_message("You: " + message)
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 12345))
        client_socket.send(message.encode())
        client_socket.close()
    
    def display_message(self, message):
        self.chat_box.configure(state=tk.NORMAL)
        self.chat_box.insert(tk.END, message + '\n')
        self.chat_box.configure(state=tk.DISABLED)
        self.chat_box.see(tk.END)

def main():
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
