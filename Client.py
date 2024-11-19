import socket

def run_client():
    host = '192.168.84.252'  # 서버 IP 주소 (필요에 따라 변경)
    port = 5555         # 서버 포트 번호 (서버와 동일해야 함)

    # 서버에 연결
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("서버에 연결되었습니다. 게임을 시작합니다!")

    try:
        while True:
            # 서버로부터 메시지 수신
            message = client_socket.recv(1024).decode()
            print(message)

            # 서버가 입력 요청 시 사용자 입력 전송
            if "타일 번호" in message:
                choice = input(">> ")
                client_socket.sendall(choice.encode())
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()