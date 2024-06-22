import struct
import socket
import random
import os
import argparse

num = 0 #记录收到的反转块数

# 添加解析命令行参数的函数
def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP Socket programming")
    parser.add_argument("--server_ip", type=str, default="192.168.159.128", help="服务器的IP地址")
    parser.add_argument("--server_port", type=int, default=23333, help="服务器的端口号")
    parser.add_argument("--Lmin", type=int, default=8, help="数据块的最小长度")
    parser.add_argument("--Lmax", type=int, default=128, help="数据块的最大长度")
    return parser.parse_args()
def create_client(server_ip, server_port,Lmin,Lmax):
    global num
    if not os.path.exists('read.txt'):
        print("读取的文件不存在")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
        try:
            socket_client.connect((server_ip, server_port))
            read_file = open('read.txt', 'r')
            write_file = open('write.txt', 'w')
            try:
                List = []
                s = random.randint(Lmin, Lmax)
                while True:
                    data = read_file.read(s)
                    s = random.randint(Lmin, Lmax)
                    if not data:
                        break
                    List.append(data)
                length = len(List)
                print(f"一共有{length}块")
                # 发送、接受数据
                message = struct.pack('>HI', 1, length)   # 构造报文
                socket_client.sendall(message)

                response = socket_client.recv(2)
                if len(response) < 2:
                    print("接收到不完整的响应类型")
                    return

                response_type, = struct.unpack('>H', response)
                print(f"接收到的响应类型为：{response_type}")
                if response_type == 2:
                    for data in List:
                        message = struct.pack('>HI', 3, len(data)) + data.encode()
                        socket_client.sendall(message)
                        response_type_length = socket_client.recv(6)
                        if len(response_type_length) < 6:
                            print("接收到不完整的响应类型和长度")
                            return

                        type_, length = struct.unpack('>HI', response_type_length)
                        if type_ == 4:
                            response_data = socket_client.recv(length).decode()
                            write_file.write(response_data)
                            num += 1
                            print(f"第{num}块反转的文本：{response_data}")
                else:
                    print('未收到确认回复')
            finally:
                read_file.close()
                write_file.close()
        except socket.error as e:
            print(f"网络操作失败：{e}")
        except IOError as e:
            print(f"文件操作失败：{e}")

if __name__ == '__main__':
    # 解析命令行参数
    args = parse_arguments()
    server_ip = args.server_ip
    server_port = args.server_port
    Lmin = args.Lmin
    Lmax = args.Lmax

    # 调用客户端创建函数，传入解析得到的参数
    create_client(server_ip, server_port, Lmin, Lmax)