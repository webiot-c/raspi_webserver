# "websocket-server" パッケージが必要
from websocket_server import WebsocketServer

### 変数
port = 12345
host_name = "localhost"

### イベントハンドラ

'''
ラズパイ側から受信したデータと同一のものを配信する。
'''
def receivedNew(client, server, message):
    print("New message: " + message)
    server.send_message_to_all(message)


def main():
    server = WebsocketServer(port, host=host_name)
    server.set_fn_message_received(receivedNew)
    server.run_forever()

if __name__ == "__main__":
    main()
