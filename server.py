import socket
import threading
import pickle
from prettytable import PrettyTable
from colorama import init, Fore, Style
from play_game import determine_winner

init()


class GameServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.clients = []  # 연결된 클라이언트 소켓
        self.scores = {0: 0, 1: 0}  # 두 플레이어의 점수
        self.tiles = {0: [i for i in range(1, 10)], 1: [i for i in range(1, 10)]}  # 각 플레이어의 타일
        self.round = 1
        self.max_rounds = 9
        self.is_self_player = False  # 서버가 클라이언트로 참여하는지 여부

    def clear_screen(self):
        """화면을 정리."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_board(self, player1_name, player2_name):
        """보드판을 출력."""
        table = PrettyTable()
        table.field_names = ["Player", "Score", "Remaining Tiles"]

        table.add_row([player1_name, self.scores[0], ", ".join(map(str, self.tiles[0]))])
        table.add_row([player2_name, self.scores[1], ", ".join(map(str, self.tiles[1]))])

        self.clear_screen()
        print("\n" + "=" * 60)
        print(f"             ⚔  ROUND {self.round} ⚔")
        print(Style.BRIGHT + Fore.YELLOW + "       Game Board" + Style.RESET_ALL)
        print("=" * 60)
        print(table)
        print("=" * 60)

    def handle_client(self, client, player_id, player_names):
        try:
            while self.round <= self.max_rounds:
                # 보드판 출력
                self.display_board(player_names[0], player_names[1])

                # 타일 요청 메시지
                if client == "self":  # 서버 자신이 참여하는 경우
                    print(f"{player_names[player_id]}'s turn")
                    print(f"Your tiles: {self.tiles[player_id]}")
                    tile = int(input("Enter your tile: "))
                    self.tiles[player_id].remove(tile)
                    setattr(self, f"client_{player_id}_tile", tile)
                else:
                    client.send(pickle.dumps({
                        "type": "request_tile",
                        "message": f"{player_names[player_id]}'s turn! Choose a tile for Round {self.round}",
                        "round_number": self.round,
                        "player1_name": player_names[0],
                        "player2_name": player_names[1],
                        "player1_points": self.scores[0],
                        "player2_points": self.scores[1],
                        "player1_tiles": self.tiles[0],
                        "player2_tiles": self.tiles[1]
                    }))

                    # 클라이언트로부터 선택된 타일 받기
                    data = pickle.loads(client.recv(1024))
                    chosen_tile = data["tile"]
                    self.tiles[player_id].remove(chosen_tile)
                    setattr(self, f"client_{player_id}_tile", chosen_tile)

                # 두 플레이어의 타일이 모두 선택되었을 때 결과 계산
                if hasattr(self, "client_0_tile") and hasattr(self, "client_1_tile"):
                    winner_tile = determine_winner(self.client_0_tile, self.client_1_tile)
                    if winner_tile == self.client_0_tile:
                        self.scores[0] += 1
                        winner = player_names[0]
                    elif winner_tile == self.client_1_tile:
                        self.scores[1] += 1
                        winner = player_names[1]
                    else:
                        winner = "Draw"

                    # 라운드 결과 출력
                    print(f"\nRound {self.round} results:")
                    print(f"{player_names[0]} chose: {self.client_0_tile}")
                    print(f"{player_names[1]} chose: {self.client_1_tile}")
                    if winner == "Draw":
                        print(Fore.YELLOW + "It's a draw!" + Style.RESET_ALL)
                    else:
                        print(Fore.BLUE + f"Winner: {winner}" + Style.RESET_ALL)

                    # 라운드 진행
                    delattr(self, "client_0_tile")
                    delattr(self, "client_1_tile")
                    self.round += 1

            # 게임 종료 메시지 출력
            self.display_board(player_names[0], player_names[1])
            print("\n" + "=" * 60)
            print(Style.BRIGHT + Fore.GREEN + "                GAME OVER!" + Style.RESET_ALL)
            print(f"Final scores: {player_names[0]} - {self.scores[0]}, {player_names[1]} - {self.scores[1]}")
            print("=" * 60)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if client != "self":
                client.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(2)
            print("Game Server started. Waiting for players...")

            # 첫 번째 플레이어 연결
            print(f"Waiting for player 0 to connect...")
            client, addr = server_socket.accept()
            print(f"Player 0 connected from {addr}")
            self.clients.append(client)
            player_names = ["Player 0", "Player 1"]

            # 서버 참여 여부 확인
            participate = input("Do you want to participate as Player 1? (yes/no): ").strip().lower()
            if participate == "yes":
                print("You are now Player 1!")
                self.is_self_player = True
                self.clients.append("self")  # 서버를 클라이언트로 등록
            else:
                print(f"Waiting for player 1 to connect...")
                client, addr = server_socket.accept()
                print(f"Player 1 connected from {addr}")
                self.clients.append(client)

            # 각 플레이어의 스레드 시작
            for i, client in enumerate(self.clients):
                threading.Thread(target=self.handle_client, args=(client, i, player_names)).start()


if __name__ == "__main__":
    GameServer().start()