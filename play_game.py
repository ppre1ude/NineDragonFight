import HumanPlayer, AIPlayer
import random 
import os
import socket, threading
from colorama import init, Fore, Style 
from prettytable import PrettyTable

init()
    
def determine_winner(tile1, tile2):
    if tile1.number == tile2.number: 
        return None  
    if tile1.number == 1 and tile2.number == 9: 
        return tile1
    elif tile1.number == 9 and tile2.number == 1:
        return tile2
    return tile1 if tile1.number > tile2.number else tile2

def user_vs_user_play_game():
    # 플레이어 생성
    server_player = HumanPlayer.Player()
    server_player.name = "Player 1 (Server)"
    client_player = HumanPlayer.Player()
    client_player.name = "Player 2 (Client)"

    # 게임 변수 초기화
    max_rounds = 9
    current_round = 1
    is_server_player_first = True
    round_records = [["-" for _ in range(max_rounds)] for _ in range(2)]  # [0]: Server, [1]: Client
    round_results = ["-" for _ in range(max_rounds)]
    match_log = []

    # 소켓 서버 설정
    host = '192.168.84.252'
    port = 5555
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("서버가 열렸습니다. 클라이언트 접속을 기다립니다...")
    conn, addr = server_socket.accept()
    print(f"클라이언트 접속 완료: {addr}")

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_board(server_points, client_points, current_round, first_player):
        # 보드 출력
        table = PrettyTable()
        field_names = ["Player", "Score"] + [f"Round {i}" for i in range(1, max_rounds + 1)]
        table.field_names = field_names

        server_row = [server_player.name, server_points] + round_records[0]
        client_row = [client_player.name, client_points] + round_records[1]

        table.add_row(server_row)
        table.add_row(client_row)

        clear_screen()
        print("\n" + "=" * 60)
        print(f"             ⚔  ROUND {current_round}/{max_rounds} ⚔")
        print(Style.BRIGHT, Fore.YELLOW, f"    First Player: {first_player}  ", Style.RESET_ALL)
        print("=" * 60)
        print(table)
        print("=" * 60)

        print("Round Results: ", end="")
        for result in round_results:
            print(result, end=" ")
        print("\n" + "=" * 60)

    def handle_client_input(player, conn):
        conn.sendall("타일 번호(1-9)를 선택하세요: ".encode())
        choice = int(conn.recv(1024).decode())
        chosen_tile = next(tile for tile in player.tiles if tile.number == choice)
        player.tiles.remove(chosen_tile)
        return chosen_tile

    # 게임 진행
    while current_round <= max_rounds and server_player.tiles and client_player.tiles:
        display_board(
            server_player.round_points,
            client_player.round_points,
            current_round,
            first_player=server_player.name if is_server_player_first else client_player.name
        )

        # 타일 선택
        if is_server_player_first:
            print(f"[{server_player.name}의 차례]")
            server_tile = server_player.choose_tile()

            print(f"[{client_player.name}의 차례]")
            client_tile = handle_client_input(client_player, conn)
        else:
            print(f"[{client_player.name}의 차례]")
            client_tile = handle_client_input(client_player, conn)

            print(f"[{server_player.name}의 차례]")
            server_tile = server_player.choose_tile()

        # 타일 기록 업데이트
        round_records[0][current_round - 1] = str(server_tile)
        round_records[1][current_round - 1] = str(client_tile)

        # 승자 결정
        winner_tile = determine_winner(server_tile, client_tile)
        if winner_tile == server_tile:
            server_player.round_points += 1
            round_results[current_round - 1] = Fore.BLUE + "W" + Style.RESET_ALL
            is_server_player_first = True
        elif winner_tile == client_tile:
            client_player.round_points += 1
            round_results[current_round - 1] = Fore.RED + "L" + Style.RESET_ALL
            is_server_player_first = False
        else:
            round_results[current_round - 1] = Fore.GREEN + "D" + Style.RESET_ALL

        match_log.append(
            f"Round {current_round}: {server_player.name} - {server_tile}, {client_player.name} - {client_tile}"
        )
        current_round += 1

    # 게임 종료
    display_board(
        server_player.round_points,
        client_player.round_points,
        current_round - 1,
        first_player=server_player.name if is_server_player_first else client_player.name
    )
    print("\n게임 종료!")
    if server_player.round_points > client_player.round_points:
        print(f"{server_player.name} 승리!")
    elif server_player.round_points < client_player.round_points:
        print(f"{client_player.name} 승리!")
    else:
        print("무승부!")

    print("\n최종 경기 기록:")
    for log in match_log:
        print(log)

    conn.close()
    server_socket.close()

def user_vs_ai_play_game(): 
    human_player = HumanPlayer.Player()
    ai_player = AIPlayer.MinimaxAI()

    is_human_player_first = True
    match_log = []  # 전체 경기 로그
    current_round = 1
    max_rounds = 9

    # 각 라운드 타일 기록 (색상만 표시)
    round_records = [["-" for _ in range(max_rounds)] for _ in range(2)]  # [0]: Human, [1]: AI
    round_results = ["-" for _ in range(max_rounds)]  # 라운드 결과 색상 정보

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_board(human_points, ai_points, current_round, first_player):
        # 격자형 보드판 생성
        table = PrettyTable()
        field_names = ["Player", "Score"] + [f"Round {i}" for i in range(1, max_rounds + 1)]
        table.field_names = field_names

        # 플레이어 데이터 입력
        human_row = [human_player.name, human_points] + round_records[0]
        ai_row = [ai_player.name, ai_points] + round_records[1]

        table.add_row(human_row)
        table.add_row(ai_row)

        # 보드판 출력
        clear_screen()
        print("\n" + "=" * 60)
        print(f"             ⚔  ROUND {current_round}/{max_rounds} ⚔")
        print(Style.BRIGHT, Fore.YELLOW, f"    First Player: {first_player}  ", Style.RESET_ALL)
        print("=" * 60)
        print(table)
        print("=" * 60)

        # 라운드 결과 색상 출력
        print("Round Results: ", end="")
        for result in round_results:
            print(result, end=" ")
        print("\n" + "=" * 60)

    while current_round <= max_rounds and human_player.tiles and ai_player.tiles:
        display_board(
            human_player.round_points,
            ai_player.round_points,
            current_round,
            first_player=human_player.name if is_human_player_first else ai_player.name
        )

        # 타일 고르기
        if is_human_player_first:
            print(f"\n[{human_player.name}의 차례]")
            human_player_tile = human_player.choose_tile()
            ai_player_tile = ai_player.choose_tile()
        else:
            print(f"\n[{ai_player.name}의 차례]")
            ai_player_tile = ai_player.choose_tile()
            if ai_player_tile.color == "black":
                print(f"{ai_player.name}이 낸 색상 : ⚫️")
            else:
                print(f"{ai_player.name}이 낸 색상 : ⚪️")
            human_player_tile = human_player.choose_tile()

        # 타일 기록 업데이트
        round_records[0][current_round - 1] = "⚫️" if human_player_tile.color == "black" else "⚪️"
        round_records[1][current_round - 1] = "⚫️" if ai_player_tile.color == "black" else "⚪️"

        # 승자 결정
        winner_tile = determine_winner(human_player_tile, ai_player_tile)
        if winner_tile == human_player_tile:
            human_player.round_points += 1
            round_results[current_round - 1] = Fore.BLUE + "W" + Style.RESET_ALL  # 승리
            is_human_player_first = True
        elif winner_tile == ai_player_tile:
            ai_player.round_points += 1
            round_results[current_round - 1] = Fore.RED + "L" + Style.RESET_ALL  # 패배
            is_human_player_first = False
        else:
            round_results[current_round - 1] = Fore.GREEN + "D" + Style.RESET_ALL  # 무승부

        # MinimaxAI의 트리 구조 업데이트
        if ai_player.name == "Minimax AI":
                if winner_tile == ai_player_tile:
                    ai_player.update_possible_opponent_tiles(ai_player_tile.number, 'lose')
                elif winner_tile == ai_player_tile:
                    ai_player.update_possible_opponent_tiles(ai_player_tile.number, 'win')
                else:
                    ai_player.update_possible_opponent_tiles(ai_player_tile.number, 'draw')

        # 매치 로그 추가
        match_log.append(f"Round {current_round}: {human_player.name} - {human_player_tile}, {ai_player.name} - {ai_player_tile}")

        current_round += 1

    # 게임 종료
    clear_screen()
    print("\n" + "=" * 60)
    print(Style.BRIGHT, Fore.YELLOW, "                  게임 종료!", Style.RESET_ALL)

    if human_player.round_points > ai_player.round_points: print(Style.BRIGHT, Fore.YELLOW, f"{human_player.name}의 승리!", Style.RESET_ALL)
    elif human_player.round_points <ai_player.round_points: print(Style.BRIGHT, Fore.YELLOW, f"{ai_player.name}의 승리!", Style.RESET_ALL)
    else: print(Style.BRIGHT, Fore.YELLOW, f"무승부!", Style.RESET_ALL)

    print(f"최종 점수: {human_player.name}: {human_player.round_points}, {ai_player.name}: {ai_player.round_points}")
    print("\n경기 기록: ")
    print("=" * 60)
    for log in match_log:
        print(log)
    print("=" * 60)

def ai_vs_ai_play_game(k):
    ai_player1 = AIPlayer.SmallFirstAI()
    ai_player2 = AIPlayer.MinimaxAI()

    ai_player1_winning_count = 0
    ai_player2_winning_count = 0
    draw_count = 0 

    """게임 시작"""
    while(k > 0): 
        # 1라운드 선 플레이어는 랜덤으로 설정
        is_ai_player1_first = random.choice([True, False])

        # 게임마다 타일 리필 
        ai_player1.reset_tiles()
        ai_player2.reset_tiles()

        ai_player1_played_tiles = []
        ai_player2_played_tiles = []

        current_round = 1

        """라운드 시작"""
        while ai_player1.tiles and ai_player2.tiles:

            # 타일 고르기 
            if is_ai_player1_first:
                ai_player1_tile = ai_player1.choose_tile()
                ai_player2_tile = ai_player2.choose_tile()
            else:
                ai_player2_tile = ai_player2.choose_tile()
                ai_player1_tile = ai_player1.choose_tile()

            # 무슨 타일을 골랐는지 기록
            ai_player1_played_tiles.append(ai_player1_tile)
            ai_player2_played_tiles.append(ai_player2_tile)

            # 승자 결정 
            winner_tile = determine_winner(ai_player1_tile, ai_player2_tile)

            if winner_tile == ai_player1_tile:
                ai_player1.round_points += 1
                is_ai_player1_first = True 
            elif winner_tile == ai_player2_tile:
                ai_player2.round_points += 1
                is_ai_player1_first = False 
            else: pass 
        """라운드 종료"""

        if ai_player1.round_points > ai_player2.round_points:
            ai_player1_winning_count += 1
        elif ai_player1.round_points < ai_player2.round_points:
            ai_player2_winning_count += 1
        else:
            draw_count += 1

        k -= 1 
    """게임 종료"""

    #경기 결과 출력 
    print("\n모든 게임 종료!")
    total = ai_player1_winning_count + ai_player2_winning_count + draw_count
    print(f"{ai_player1.name}'s winning count = {ai_player1_winning_count}, 승률 = {round(ai_player1_winning_count / total * 100)}%")
    print(f"{ai_player2.name}'s winning count = {ai_player2_winning_count}, 승률 = {round(ai_player2_winning_count / total * 100)}%")
    print(f"무승부 횟수 = {draw_count}, 무승부율 = {round(draw_count / total * 100)}%")

def ai_vs_QLearningAI_play_game(k):
    """게임 초기 세팅"""
    ai_player = AIPlayer.BigFirstAI() 
    q_player = AIPlayer.DaehanQLearning()

    ai_player_winning_count = 0
    q_player_winning_count = 0
    draw_count = 0
    
    """게임 시작"""
    while k > 0:
        # 1라운드 선 플레이어는 랜덤으로 설정
        is_ai_player_first = random.choice([True, False])

        # 게임마다 타일 리필
        ai_player.reset_tiles()
        q_player.reset_tiles()
        
        ai_player_played_tiles = [] 
        q_played_tiles = [] 

        current_round = 1

        """라운드 시작"""
        while ai_player.tiles and q_player.tiles:

            # 타일 고르기 
            if is_ai_player_first:
                ai_player_tile = ai_player.choose_tile()
                q_player_tile = q_player.choose_tile(current_round)
            else:
                q_player_tile = q_player.choose_tile(current_round)
                ai_player_tile = ai_player.choose_tile()

            # 무슨 타일을 골랐는지 기록
            ai_player_played_tiles.append(ai_player_tile)
            q_played_tiles.append(q_player_tile)

            # 승자 결정
            winner_tile = determine_winner(ai_player_tile, q_player_tile)

            if winner_tile == ai_player_tile:
                ai_player.round_points += 1
                is_ai_player_first = True 
            elif winner_tile == q_player_tile:
                q_player.round_points += 1
                is_ai_player_first = False 
            else: pass 

            current_round += 1
        """라운드 끝"""

        # 게임 종료 후 승자 집계
        if ai_player.round_points > q_player.round_points:
            ai_player_winning_count += 1
            game_result = -1
        elif ai_player.round_points < q_player.round_points:
            q_player_winning_count += 1
            game_result = 1
        else:
            draw_count += 1
            game_result = 0
        
        # 게임 종료 후 큐 테이블 업데이트
        q_player.update_q_table(q_played_tiles, ai_player_played_tiles, game_result)

        # 다음 게임 진행 
        k -= 1
    """게임 끝 """

    """최종 큐 테이블 출력"""
    q_player.display_q_table()

    """모든 게임 종료"""
    # 게임 결과 출력
    print("\n모든 게임 종료!")
    total = ai_player_winning_count + q_player_winning_count + draw_count
    print(f"{ai_player.name}'s winning count = {ai_player_winning_count}, 승률 = {round(ai_player_winning_count / total * 100)}%")
    print(f"{q_player.name}'s winning count = {q_player_winning_count}, 승률 = {round(q_player_winning_count / total * 100)}%")
    print(f"무승부 횟수 = {draw_count}, 무승부율 = {round(draw_count / total * 100)}%")