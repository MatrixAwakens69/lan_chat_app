import socket
import threading
import argparse
from blowfish import BlowfishEncryption
from gui import ChatGUI

class Peer:
    def __init__(self, host, port, key):
        self.host = host
        self.port = port
        self.key = key
        self.encryption = BlowfishEncryption(key)
        self.peers = []

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            self.peers.append(client_socket)
            threading.Thread(target=self.handle_peer, args=(client_socket,)).start()

    def handle_peer(self, peer_socket):
        while True:
            try:
                message = peer_socket.recv(1024)
                if message:
                    decrypted_message = self.encryption.decrypt(message)
                    self.gui.display_message(decrypted_message.decode())
                else:
                    self.peers.remove(peer_socket)
                    peer_socket.close()
                    break
            except:
                self.peers.remove(peer_socket)
                peer_socket.close()
                break

    def connect_to_peer(self, peer_host, peer_port):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_host, peer_port))
        self.peers.append(peer_socket)
        threading.Thread(target=self.handle_peer, args=(peer_socket,)).start()

    def send_message(self, message):
        encrypted_message = self.encryption.encrypt(message.encode())
        for peer in self.peers:
            peer.send(encrypted_message)

    def start(self):
        threading.Thread(target=self.start_server).start()
        self.gui = ChatGUI(self)
        self.gui.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P Chat Application")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the server')
    parser.add_argument('--port', type=int, required=True, help='Port to bind the server')
    args = parser.parse_args()

    key = b'16bytepassword!!'  # Must be 16, 24, or 32 bytes long
    peer = Peer(args.host, args.port, key)
    peer.start()