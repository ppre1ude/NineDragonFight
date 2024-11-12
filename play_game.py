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
    player = HumanPlayer.Player()
    ai_player = AIPlayer.BasedProbabilityAI()
    current_player = random.choice([player, ai_player])
    match_log = [] 
    round = 1

    while player.tiles and ai_player.tiles:
        print()
        print(Style.BRIGHT, Fore.YELLOW, f"※ {round} 라운드 시작 ※ ", Style.RESET_ALL)
        round+=1
        print(f"\n[{current_player.name}의 차례]")
        
        tile1 = current_player.choose_tile()
        if current_player == ai_player: 
            if tile1.color == 'black':
                print("AI가 낸 색상 : ⚫️\n")
            else:
                print("AI가 낸 색상 : ⚪️\n")

        other_player = ai_player if current_player == player else player
        tile2 = other_player.choose_tile()
        if current_player == player: 
            if tile2.color == 'black':
                print("AI가 낸 색상 : ⚫️\n")
            else:
                print("AI가 낸 색상 : ⚪️\n")


        # 승자 결정 
        winner = determine_winner(tile1, tile2)

        # 유지 
        if current_player == player and winner == tile1:
            print(Style.BRIGHT, Fore.BLUE, "\n !!!User의 승리!!!", Style.RESET_ALL)
            current_player.round_points += 1
            match_log.append(f"{current_player.name} : {tile1} , {other_player.name} : {tile2}.")
            current_player, other_player = player, ai_player

        # 변경 
        elif current_player == player and winner == tile2:
            print(Style.BRIGHT, Fore.RED, "\n !!!AI의 승리!!!", Style.RESET_ALL)
            other_player.round_points += 1   
            match_log.append(f"{current_player.name} : {tile1} , {other_player.name} : {tile2}.")
            current_player, other_player = ai_player, player

        # 유지 
        elif current_player == ai_player and winner == tile1:
            print(Style.BRIGHT, Fore.RED, "\n !!!AI의 승리!!!", Style.RESET_ALL)
            current_player.round_points += 1
            match_log.append(f"{current_player.name} : {tile1} , {other_player.name} : {tile2}.")
            current_player, other_player = ai_player, player

        # 변경
        elif current_player == ai_player and winner == tile2:
            print(Style.BRIGHT, Fore.BLUE, "\n !!!User의 승리!!!", Style.RESET_ALL)
            other_player.round_points += 1
            match_log.append(f"{current_player.name} : {tile1} , {other_player.name} : {tile2}.")
            current_player, other_player = player, ai_player

        else:
            print(Style.BRIGHT, Fore.GREEN, "\n !!!무승부!!!", Style.RESET_ALL)
            match_log.append(f"무승부 : {tile1} vs. {tile2}.")

        # Print round points for both players
        print(Style.BRIGHT, Fore.YELLOW, f"라운드 포인트 : {player.name}: {player.round_points}, {ai_player.name}: {ai_player.round_points}", Style.RESET_ALL)
        print("=" * 30)

    # 경기 결과 출력 
    print(Style.BRIGHT, Fore.YELLOW, "\n게임 종료!", Style.RESET_ALL)
    print(f"최종 라운드 포인트 : {player.name}: {player.round_points}, {ai_player.name}: {ai_player.round_points}")
    print("\n경기 기록: ")
    print("=" * 30)  
    for i, log in enumerate(match_log):
        print(f"Round {i + 1}:")
        print(f" - {log}")
        print("-" * 30)  
    print("=" * 30)  

def ai_vs_ai_play_game(k):
    ai_player1_winning_count = 0
    ai_player2_winning_count = 0
    draw_count = 0 

    ai_player1 = AIPlayer.RandomAI()
    ai_player2 = AIPlayer.SmallFirstAI()
    while(k > 0): 
        ai_player1.reset_tiles()
        ai_player2.reset_tiles()
        current_player = random.choice([ai_player1, ai_player2])

        while ai_player1.tiles and ai_player2.tiles:
            
            tile1 = current_player.choose_tile()
            other_player = ai_player2 if current_player == ai_player1 else ai_player1
            tile2 = other_player.choose_tile()

            # 승자 결정 
            winner = determine_winner(tile1, tile2)

            # 유지 
            if current_player == ai_player1 and winner == tile1:
                current_player.round_points += 1
                current_player, other_player = ai_player1, ai_player2

            # 변경 
            elif current_player == ai_player1 and winner == tile2:
                other_player.round_points += 1   
                current_player, other_player = ai_player2, ai_player1

            # 유지 
            elif current_player == ai_player2 and winner == tile1:
                current_player.round_points += 1
                current_player, other_player = ai_player2, ai_player1

            # 변경
            elif current_player == ai_player2 and winner == tile2:
                other_player.round_points += 1
                current_player, other_player = ai_player1, ai_player2

        if ai_player1.round_points > ai_player2.round_points:
            ai_player1_winning_count += 1
        elif ai_player1.round_points < ai_player2.round_points:
            ai_player2_winning_count += 1
        else:
            draw_count += 1

        k -= 1 
    
    #경기 결과 출력 
    print("\n게임 종료!")
    total = ai_player1_winning_count + ai_player2_winning_count + draw_count
    print(f"{ai_player1.name}'s winning count = {ai_player1_winning_count}, 승률 = {round(ai_player1_winning_count / total * 100)}%")
    print(f"{ai_player2.name}'s winning count = {ai_player2_winning_count}, 승률 = {round(ai_player2_winning_count / total * 100)}%")
    print(f"무승부 횟수 = {draw_count}, 무승부율 = {round(draw_count / total * 100)}%")

def ai_vs_RLAI_play_game(k):
    ai_player = AIPlayer.MaintainPointsAI() 
    q_player = AIPlayer.DaehanQLearning()

    ai_player_winning_count = 0
    q_player_winning_count = 0
    draw_count = 0

    while k > 0:
        is_ai_player_first = random.choice([True, False])

        # 게임마다 타일 초기화
        ai_player.reset_tiles()
        q_player.reset_tiles()
        
        
        q_learning_played_tile = [] 
        ai_player_played_tile = [] 
        current_round = 1

        """게임 시작"""
        while ai_player.tiles and q_player.tiles:

            # 타일 고르기 
            if is_ai_player_first:
                ai_player_tile = ai_player.choose_tile()
                q_player_tile = q_player.choose_tile(current_round)
            else:
                q_player_tile = q_player.choose_tile(current_round)
                ai_player_tile = ai_player.choose_tile()

            # 무슨 타일을 골랐는지 기록
            ai_player_played_tile.append(ai_player_tile)
            q_learning_played_tile.append(q_player_tile)

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
        """게임 끝"""

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
        q_player.update_q_table(q_learning_played_tile, ai_player_played_tile, game_result)

        # 다음 게임진행 
        k -= 1

    """모든 게임 종료"""
    # 게임 결과 출력
    print("\n게임 종료!")
    total = ai_player_winning_count + q_player_winning_count + draw_count
    print(f"{ai_player.name}'s winning count = {ai_player_winning_count}, 승률 = {round(ai_player_winning_count / total * 100)}%")
    print(f"{q_player.name}'s winning count = {q_player_winning_count}, 승률 = {round(q_player_winning_count / total * 100)}%")
    print(f"무승부 횟수 = {draw_count}, 무승부율 = {round(draw_count / total * 100)}%")

    """최종 큐 테이블 출력"""
    q_player.display_q_table()


