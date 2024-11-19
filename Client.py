import socket
import pickle

class GameClient:
    def __init__(self):
        self.host = input("Enter the server IP address: ")  # 서버 IP 주소 입력
        self.port = int(input("Enter the server port: "))   # 서버 포트 입력

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            print("Connected to the game server!")

            while True:
                # 서버로부터 메시지 수신
                data = pickle.loads(client_socket.recv(1024))
                if data["type"] == "request_tile":
                    # 타일 선택 요청
                    print(data["message"])
                    print(f"Your tiles: {data['tiles']}")
                    tile = int(input("Enter your tile: "))
                    client_socket.send(pickle.dumps({"tile": tile}))

                elif data["type"] == "round_result":
                    # 라운드 결과 수신
                    print(f"Round {data['round']} results:")
                    print(f"Player 0 chose: {data['chosen_tiles'][0]}")
                    print(f"Player 1 chose: {data['chosen_tiles'][1]}")
                    winner = data["winner"]
                    if winner is not None:
                        print(f"Winner: Player {winner}")
                    else:
                        print("Draw!")
                    print(f"Scores: Player 0 - {data['scores'][0]}, Player 1 - {data['scores'][1]}")

                elif data["type"] == "game_over":
                    # 게임 종료 메시지 수신
                    print("Game over!")
                    print(f"Final scores: Player 0 - {data['scores'][0]}, Player 1 - {data['scores'][1]}")
                    break


if __name__ == "__main__":
    GameClient().start()
