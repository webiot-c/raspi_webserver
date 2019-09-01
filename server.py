from websocket_server import WebsocketServer
from socket import socket, AF_INET, SOCK_STREAM
import threading

### 変数
SKT_HOST = "localhost"
SKT_PORT = 12345
WS_HOST = "0.0.0.0"
WS_PORT = 6789

MAX_CON_COUNT  = 8
MAX_MSG_LENGTH = 128

server = None

def websocket_main():
    global server

    server = WebsocketServer(WS_PORT, host=WS_HOST)
    server.run_forever()


def main():
    websocket_thread = threading.Thread(target=websocket_main)
    websocket_thread.start()
    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((SKT_HOST, SKT_PORT))
    sock.listen(MAX_MSG_LENGTH)

    while True:
        try:
            conn, addr = sock.accept()
            req = conn.recv(MAX_MSG_LENGTH).decode('utf-8')
            conn.close()
            
            print("received; ")
            print(req)

            server.send_message_to_all(req)
        except:
            # HAX: 2回 Ctrl-c を叩く必要がある。プロセス停止の方法がわからない！
            print("Connection Error, may be keyboard interruption?")
            print("Program will be terminated.")
            break
    
if __name__ == "__main__":
    main()
