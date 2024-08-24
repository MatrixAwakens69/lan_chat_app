import tkinter as tk
from tkinter import scrolledtext, filedialog

class ChatGUI:
    def __init__(self, peer):
        self.peer = peer
        self.window = tk.Tk()
        self.window.title("LAN Chat Application")

        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(self.window)
        self.message_entry.pack(padx=10, pady=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.file_button = tk.Button(self.window, text="Send File", command=self.send_file)
        self.file_button.pack(padx=10, pady=10)

        self.connect_button = tk.Button(self.window, text="Connect to Peer", command=self.connect_to_peer)
        self.connect_button.pack(padx=10, pady=10)

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            self.peer.send_message(message)
            self.display_message(f"You: {message}")
            self.message_entry.delete(0, tk.END)

    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                self.peer.send_message(f"FILE:{file_path.split('/')[-1]}")
                self.peer.send_message(file_data.decode('latin1'))

    def connect_to_peer(self):
        peer_host = tk.simpledialog.askstring("Connect to Peer", "Enter peer host:")
        peer_port = tk.simpledialog.askinteger("Connect to Peer", "Enter peer port:")
        if peer_host and peer_port:
            self.peer.connect_to_peer(peer_host, peer_port)

    def display_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def run(self):
        self.window.mainloop()