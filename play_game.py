import HumanPlayer
import AIPlayer
import random 
import time 
from colorama import init, Fore, Style 

init()

class Tile:
    def __init__(self, number):
        self.number = number
        self.color = 'white' if number % 2 == 0 else 'black'

    def __str__(self):
        emoji = "⚪️" if self.color == 'white' else "⚫️"  # 이모지로 색상 표현
        return f"{emoji} {self.number}"
    
    def __lt__(self, other):
        return self.number < other.number
    
    # max_tile in self.tiles 하기 위해서 필요함
    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.number == other.number
        return False
    
def determine_winner(tile1, tile2):
    if tile1.number == tile2.number: 
        return None  
    if tile1.number == 1 and tile2.number == 9: 
        return tile1
    elif tile1.number == 9 and tile2.number == 1:
        return tile2
    return tile1 if tile1.number > tile2.number else tile2

def user_vs_ai_play_game():
    human_player = HumanPlayer.Player()
    ai_player = AIPlayer.RandomAI()

    is_human_player_first = True 
    match_log = [] 
    current_round = 1

    while human_player.tiles and ai_player.tiles:
        print()
        print(Style.BRIGHT, Fore.YELLOW, f"※ {current_round} 라운드 시작 ※ ", Style.RESET_ALL)
        
        # 타일 고르기
        if is_human_player_first:
            print(f"\n[{human_player.name}의 차례]")
            human_player_tile = human_player.choose_tile()
            ai_player_tile = ai_player.choose_tile()
            print(f"{ai_player.name}이 낸 색상 : ⚪️")
        else:
            print(f"\n[{ai_player.name}의 차례]")
            ai_player_tile = ai_player.choose_tile() 
            if ai_player_tile.color == "black": print(f"{ai_player.name}이 낸 색상 : ⚫️")
            else: print(f"{ai_player.name}이 낸 색상 : ⚪️")
            human_player_tile = human_player.choose_tile()

        # 승자 결정 
        winner_tile = determine_winner(human_player_tile, ai_player_tile)

        if winner_tile == human_player_tile:
            print(Style.BRIGHT, Fore.BLUE, "\n !!!User의 승리!!!", Style.RESET_ALL)
            human_player.round_points += 1
            is_human_player_first = True
        elif winner_tile == ai_player_tile:
            print(Style.BRIGHT, Fore.RED, "\n !!!AI의 승리!!!", Style.RESET_ALL)
            ai_player.round_points += 1
            is_human_player_first = False
        else:
            print(Style.BRIGHT, Fore.GREEN, "\n !!!무승부!!!", Style.RESET_ALL)

        # 매치 로그 추가 
        match_log.append(f"{human_player.name} : {human_player_tile} , {ai_player.name} : {ai_player_tile}.")
        
        current_round+=1

        # 라운드 포인트 출력
        print(Style.BRIGHT, Fore.YELLOW, f"라운드 포인트 : {human_player.name}: {human_player.round_points}, {ai_player.name}: {ai_player.round_points}", Style.RESET_ALL)
        print("=" * 30)

    # 경기 결과 출력 
    print(Style.BRIGHT, Fore.YELLOW, "\n게임 종료!", Style.RESET_ALL)
    print(f"최종 라운드 포인트 : {human_player.name}: {human_player.round_points}, {ai_player.name}: {ai_player.round_points}")
    print("\n경기 기록: ")
    print("=" * 30)  
    for i, log in enumerate(match_log):
        print(f"Round {i + 1}:")
        print(f" - {log}")
        print("-" * 30)  
    print("=" * 30)  

def ai_vs_ai_play_game(k):
    ai_player1 = AIPlayer.RandomAI()
    ai_player2 = AIPlayer.SieunAI()

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
    ai_player = AIPlayer.RandomAI() 
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

def ai_vs_TreeAI_play_game(k):
    """Random AI와 Tree AI 간의 게임 시뮬레이션"""
    ai_player = AIPlayer.SmallFirstAI() 
    tree_ai = AIPlayer.TreeAI()  # 트리 구조 기반 AI

    ai_player_winning_count = 0
    tree_ai_winning_count = 0
    draw_count = 0
    
    """게임 시작"""
    while k > 0:
        # 1라운드 선 플레이어는 랜덤으로 설정
        is_ai_player_first = random.choice([True, False])

        # 게임마다 타일 리필
        ai_player.reset_tiles()
        tree_ai.reset_tiles()
        
        ai_player_played_tiles = [] 
        tree_ai_played_tiles = [] 
        current_round = 1

        """라운드 시작"""
        while ai_player.tiles and tree_ai.tiles:
            # 타일 고르기 
            if is_ai_player_first:
                ai_player_tile = ai_player.choose_tile()
                tree_ai_tile = tree_ai.choose_tile()
            else:
                tree_ai_tile = tree_ai.choose_tile()
                ai_player_tile = ai_player.choose_tile()

            # 무슨 타일을 골랐는지 기록
            ai_player_played_tiles.append(ai_player_tile)
            tree_ai_played_tiles.append(tree_ai_tile)

            # 승자 결정
            winner_tile = determine_winner(ai_player_tile, tree_ai_tile)

            if winner_tile == ai_player_tile:
                ai_player.round_points += 1
                is_ai_player_first = True 
            elif winner_tile == tree_ai_tile:
                tree_ai.round_points += 1
                is_ai_player_first = False 
            else:
                # 무승부일 경우 선 플레이어 변경 없이 다음 라운드 진행
                is_ai_player_first = not is_ai_player_first

            # Tree AI의 트리 구조 업데이트
            if winner_tile == ai_player_tile:
                tree_ai.update_possible_opponent_tiles(ai_player_tile.number, 'lose')
            elif winner_tile == tree_ai_tile:
                tree_ai.update_possible_opponent_tiles(ai_player_tile.number, 'win')
            else:
                tree_ai.update_possible_opponent_tiles(ai_player_tile.number, 'draw')

            current_round += 1
        """라운드 끝"""

        # 게임 종료 후 승자 집계
        if ai_player.round_points > tree_ai.round_points:
            ai_player_winning_count += 1
        elif ai_player.round_points < tree_ai.round_points:
            tree_ai_winning_count += 1
        else:
            draw_count += 1

        # 다음 게임 진행 
        k -= 1

    """게임 끝 """

    """모든 게임 종료"""
    # 게임 결과 출력
    print("\n모든 게임 종료!")
    total = ai_player_winning_count + tree_ai_winning_count + draw_count
    print(f"{ai_player.name}'s winning count = {ai_player_winning_count}, 승률 = {round(ai_player_winning_count / total * 100)}%")
    print(f"{tree_ai.name}'s winning count = {tree_ai_winning_count}, 승률 = {round(tree_ai_winning_count / total * 100)}%")
    print(f"무승부 횟수 = {draw_count}, 무승부율 = {round(draw_count / total * 100)}%")
