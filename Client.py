import socket
import pickle
from prettytable import PrettyTable
from colorama import init, Fore, Style

init()


class GameClient:
    def __init__(self):
        self.host = input("Enter the server IP address: ").strip()  # 서버 IP 주소 입력
        self.port = int(input("Enter the server port: ").strip())  # 서버 포트 입력

    def clear_screen(self):
        """화면을 정리."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_board(self, player1_name, player2_name, player1_points, player2_points, player1_tiles, player2_tiles, round_number):
        """보드판을 출력."""
        table = PrettyTable()
        table.field_names = ["Player", "Score", "Remaining Tiles"]

        table.add_row([player1_name, player1_points, ", ".join(map(str, player1_tiles))])
        table.add_row([player2_name, player2_points, ", ".join(map(str, player2_tiles))])

        self.clear_screen()
        print("\n" + "=" * 60)
        print(f"             ⚔  ROUND {round_number} ⚔")
        print(Style.BRIGHT + Fore.YELLOW + "       Game Board" + Style.RESET_ALL)
        print("=" * 60)
        print(table)
        print("=" * 60)

    def start(self):
        """클라이언트 메인 실행 함수."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                # 서버에 연결
                client_socket.connect((self.host, self.port))
                print(Fore.GREEN + "Connected to the game server!" + Style.RESET_ALL)

                while True:
                    # 서버로부터 메시지 수신
                    data = pickle.loads(client_socket.recv(1024))

                    if data["type"] == "request_tile":
                        # 보드판 출력
                        self.display_board(
                            player1_name=data["player1_name"],
                            player2_name=data["player2_name"],
                            player1_points=data["player1_points"],
                            player2_points=data["player2_points"],
                            player1_tiles=data["player1_tiles"],
                            player2_tiles=data["player2_tiles"],
                            round_number=data["round_number"]
                        )

                        # 타일 선택 요청
                        print(Fore.BLUE + f"{data['message']}" + Style.RESET_ALL)
                        tile = int(input("Enter your tile: "))
                        client_socket.send(pickle.dumps({"tile": tile}))

                    elif data["type"] == "round_result":
                        # 라운드 결과 출력
                        print(f"\nRound {data['round']} results:")
                        print(f"{data['player1_name']} chose: {data['player1_tile']}")
                        print(f"{data['player2_name']} chose: {data['player2_tile']}")
                        winner = data["winner"]
                        if winner == "Draw":
                            print(Fore.YELLOW + "It's a draw!" + Style.RESET_ALL)
                        else:
                            print(Fore.BLUE + f"Winner: {winner}" + Style.RESET_ALL)

                    elif data["type"] == "game_over":
                        # 게임 종료 메시지 출력
                        self.display_board(
                            player1_name=data["player1_name"],
                            player2_name=data["player2_name"],
                            player1_points=data["player1_points"],
                            player2_points=data["player2_points"],
                            round_number=data["round_number"]
                        )
                        print("\n" + "=" * 60)
                        print(Style.BRIGHT + Fore.GREEN + "                GAME OVER!" + Style.RESET_ALL)
                        print(f"Final scores: {data['player1_name']} - {data['player1_points']}, {data['player2_name']} - {data['player2_points']}")
                        print("=" * 60)
                        break

            except Exception as e:
                print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    GameClient().start()
