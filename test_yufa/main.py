import socket


def start_udp_server(host='0.0.0.0', port=5005):
    # 创建 UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定到指定的地址和端口
    udp_socket.bind((host, port))
    print(f"UDP 服务器正在监听 {host}:{port}...")

    try:
        while True:
            # 接收数据
            data, addr = udp_socket.recvfrom(1024)  # 1024 是缓冲区大小
            print(f"接收到来自 {addr} 的数据: {data.decode('utf-8')}")
    except KeyboardInterrupt:
        print("UDP 服务器已停止")
    finally:
        udp_socket.close()


if __name__ == "__main__":
    start_udp_server()