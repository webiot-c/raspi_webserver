from websocket_server import WebsocketServer
import socket
import threadiang

### 変数
HOST = "localhost"
PORT = 12345

MAX_CON_COUNT  = 8
MAX_MSG_LENGTH = 128

server = None

def websocket_main():
    global server

    server = WebsocketServer(port, host=host_name)
    server.run_forever()


def main():
    websocket_thread = threading.Thread(target=websocket_main)
    websocket_thread.start()
    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, POST))
    sock.listen(MAX_MSG_LENGTH)

    while True:
        try:
            conn, addr = sock.accept()
            req = conn.recv(MAX_MSG_LENGTH).decode('utf-8')
            conn.close()

            server.send_message_to_all(req)
        except:
            print("Connection error!")
    
if __name__ == "__main__":
    main()
