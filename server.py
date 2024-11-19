import socket
import threading
import pickle
from play_game import determine_winner

class GameServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.clients = []  # 연결된 클라이언트 소켓
        self.scores = {0: 0, 1: 0}  # 두 플레이어의 점수
        self.tiles = {0: [i for i in range(1, 10)], 1: [i for i in range(1, 10)]}  # 각 플레이어의 타일
        self.round = 1
        self.max_rounds = 9

    def handle_client(self, client, player_id):
        try:
            while self.round <= self.max_rounds:
                # 타일 요청
                client.send(pickle.dumps({
                    "type": "request_tile",
                    "message": f"Choose a tile for Round {self.round}",
                    "tiles": self.tiles[player_id]
                }))

                # 클라이언트로부터 선택된 타일 받기
                data = pickle.loads(client.recv(1024))
                chosen_tile = data["tile"]
                self.tiles[player_id].remove(chosen_tile)

                # 결과 계산
                if player_id == 0:
                    self.client_0_tile = chosen_tile
                else:
                    self.client_1_tile = chosen_tile

                if hasattr(self, "client_0_tile") and hasattr(self, "client_1_tile"):
                    # 두 플레이어의 타일이 모두 선택되었을 때 결과 계산
                    winner_tile = determine_winner(self.client_0_tile, self.client_1_tile)
                    if winner_tile == self.client_0_tile:
                        self.scores[0] += 1
                        winner = 0
                    elif winner_tile == self.client_1_tile:
                        self.scores[1] += 1
                        winner = 1
                    else:
                        winner = None

                    # 결과 전송
                    for i, c in enumerate(self.clients):
                        c.send(pickle.dumps({
                            "type": "round_result",
                            "round": self.round,
                            "chosen_tiles": [self.client_0_tile, self.client_1_tile],
                            "winner": winner,
                            "scores": self.scores
                        }))

                    # 라운드 진행
                    delattr(self, "client_0_tile")
                    delattr(self, "client_1_tile")
                    self.round += 1

            # 게임 종료
            for c in self.clients:
                c.send(pickle.dumps({
                    "type": "game_over",
                    "scores": self.scores
                }))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(2)
            print("Game Server started. Waiting for players...")

            while len(self.clients) < 2:
                client, addr = server_socket.accept()
                print(f"Player {len(self.clients)} connected from {addr}")
                self.clients.append(client)

            for i, client in enumerate(self.clients):
                threading.Thread(target=self.handle_client, args=(client, i)).start()


if __name__ == "__main__":
    GameServer().start()
