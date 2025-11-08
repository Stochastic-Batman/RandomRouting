import socket
import threading
import json
from typing import Optional, Callable
from tarjimani.lang2lang import create_models, translate


class TranslationChat:
    def __init__(self, my_language: str, port: int = 5035):
        self.my_language = my_language
        self.peer_language: Optional[str] = None
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.connection: Optional[socket.socket] = None
        self.models = None
        self.running = False
        self.on_message: Optional[Callable[[str, str], None]] = None

    def start_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(1)
        print(f"Waiting for connection on port {self.port}...")

        self.connection, addr = self.socket.accept()
        self._exchange_languages()
        self._start_receiving()

    def connect_to_peer(self, host: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.connection = self.socket
        self._exchange_languages()
        self._start_receiving()

    def _exchange_languages(self):
        self._send_raw(json.dumps({"type": "lang", "language": self.my_language}))

        data = self.connection.recv(1024).decode('utf-8')
        msg = json.loads(data)
        if msg["type"] == "lang":
            self.peer_language = msg["language"]

        result = create_models(self.my_language, self.peer_language)
        if result == "<unsupported_language_pair>":
            print("Unsupported language pair!")
            self.close()
            return

        (self.tokenizer_send, self.model_send), (self.tokenizer_recv, self.model_recv) = result
        print(f"{self.my_language} ↹ {self.peer_language}")

    def _send_raw(self, data: str):
        if self.connection:
            self.connection.sendall(data.encode('utf-8'))

    def _start_receiving(self):
        self.running = True
        thread = threading.Thread(target=self._receive_loop, daemon=True)
        thread.start()

    def _receive_loop(self):
        buffer = ""
        while self.running:
            try:
                data = self.connection.recv(4096).decode('utf-8')
                if not data:
                    print("\nConnection closed by peer")
                    self.running = False
                    break

                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if line:
                        self._handle_message(line)
            except Exception as e:
                print(f"\nError receiving: {e}")
                self.running = False
                break

    def _handle_message(self, data: str):
        try:
            msg = json.loads(data)
            if msg["type"] == "chat":
                if self.on_message:
                    self.on_message(msg["text"], msg["text"])
                else:
                    print(f"\n⥺ {msg['text']}")
                    print("⟴ ", end="", flush=True)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"\nInvalid message: {e}")
            print("⟴ ", end="", flush=True)

    def send_message(self, text: str):
        if not self.connection or not self.running:
            print("Not connected")
            return

        if not text.strip():
            return

        translated = translate(text, self.tokenizer_send, self.model_send)
        msg = json.dumps({"type": "chat", "text": translated}, ensure_ascii=False) + "\n"
        self._send_raw(msg)

    def close(self):
        self.running = False
        if self.connection:
            self.connection.close()
        if self.socket:
            self.socket.close()


def main():
    import sys

    if len(sys.argv) < 3:
        print("Usage:")
        print("  Server: python networking.py server <your_language> [port]")
        print("  Client: python networking.py client <your_language> <host> [port]")
        print("Example: python networking.py server ka 5000")
        print("Example: python networking.py client en localhost 5000")
        return

    mode = sys.argv[1]
    my_lang = sys.argv[2]

    if mode == "server":
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
        chat = TranslationChat(my_lang, port)
        chat.start_server()
    elif mode == "client":
        if len(sys.argv) < 4:
            print("Client mode requires host")
            return
        host = sys.argv[3]
        port = int(sys.argv[4]) if len(sys.argv) > 4 else 5000
        chat = TranslationChat(my_lang)
        chat.connect_to_peer(host, port)
    else:
        print("Invalid mode. Use 'server' or 'client'")
        return

    print("\nChat ready! Type your messages (Ctrl+C to exit):\n")
    try:
        while chat.running:
            msg = input("⟴ ")
            if msg:
                chat.send_message(msg)
    except KeyboardInterrupt:
        print("\nClosing chat...")
    finally:
        chat.close()


if __name__ == "__main__":
    main()