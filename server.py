import socket
import threading
import struct



server_ip = '127.0.0.1'
server_port = 23333

def create_thread(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((server_ip, server_port))
        socket_server.listen(99)
        print(f"服务器正在运行在 {server_ip}:{server_port}")
        print("正在等待客户端连接...")
        num = 0
        while True:
            num += 1
            try:
                conn, address = socket_server.accept()
            except socket.error as e:
                print(f"接受连接失败: {e}")
                continue
            print(f"服务端已接受到客户端 {num}号 的连接请求，客户端信息：{address}")
            client_thread = threading.Thread(target=client, args=(conn, address, num))
            client_thread.start()

def client(conn, address, num):
    try:
        while True:
            type_length = conn.recv(6)
            if len(type_length) < 6:
                print("接收到不完整的头部数据")
                break

            type_, length = struct.unpack('>HI', type_length)
            if type_ == 1:
                conn.sendall(struct.pack('>H', 2))
                print(f"收到1请求,一共{length}块,回复2")
                continue
            elif type_ == 3:
                data = conn.recv(length).decode()
                if len(data) != length:
                    print("接收到的数据长度不匹配")
                    break
                print(f"客户端 {num}号:{address}发来的消息是：{data}")
                # 发送消息到客户端
                response_data = data[::-1]
                conn.sendall(struct.pack('>HI', 4, len(response_data)) + response_data.encode())
            else:
                print(f"非法消息")
                break
    except Exception as e:
        print(f"处理客户端连接时发生错误: {e}")
    finally:
        conn.close()
        print(f"客户端 {num}号:{address} 连接已关闭")

if __name__ == '__main__':
    create_thread(server_ip, server_port)