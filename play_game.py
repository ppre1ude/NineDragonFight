import HumanPlayer
import AIPlayer
import random 

class Tile:
    def __init__(self, number):
        self.number = number
        self.color = 'white' if number % 2 == 0 else 'black'

    def __str__(self):
        emoji = "⚪️" if self.color == 'white' else "⚫️"  # 이모지로 색상 표현
        return f"{emoji} {self.number}"

def determine_winner(tile1, tile2):
    if tile1.number == tile2.number: # 무승부 
        return None  
    if tile1.number == 1 and tile2.number == 9: 
        return tile1
    elif tile1.number == 9 and tile2.number == 1:
        return tile2
    return tile1 if tile1.number > tile2.number else tile2

def play_game():
    player = HumanPlayer.Player("User")
    ai_player = AIPlayer.RandomAI("RandomAI")
    current_player = random.choice([player, ai_player])
    match_log = [] 

    while player.tiles and ai_player.tiles:
        print(f"\n{current_player.name}의 차례")
        
        tile1 = current_player.choose_tile()
        if current_player == ai_player: 
            if tile1.color == 'black':
                print("AI가 낸 색상 : ⚫️")
            else:
                print("AI가 낸 색상 : ⚪️")

        other_player = ai_player if current_player == player else player
        tile2 = other_player.choose_tile()
        if current_player == player: 
            if tile2.color == 'black':
                print("AI가 낸 색상 : ⚫️")
            else:
                print("AI가 낸 색상 : ⚪️")


        # 승자 결정 
        winner = determine_winner(tile1, tile2)

        # 유지 
        if current_player == player and winner == tile1:
            print("======User의 승리======")
            current_player.round_points += 1
            match_log.append(f"{current_player.name} : {tile1} , {other_player.name} : {tile2}.")
            current_player, other_player = player, ai_player

        # 변경 
        elif current_player == player and winner == tile2:
            print("======AI의 승리======")
            other_player.round_points += 1   
            match_log.append(f"{current_player.name} : {tile1} , {other_player.name} : {tile2}.")
            current_player, other_player = ai_player, player

        # 유지 
        elif current_player == ai_player and winner == tile1:
            print("======AI의 승리======")
            current_player.round_points += 1
            match_log.append(f"{current_player.name} : {tile1} , {other_player.name} : {tile2}.")
            current_player, other_player = ai_player, player

        # 변경
        elif current_player == ai_player and winner == tile2:
            print("======User의 승리======")
            other_player.round_points += 1
            match_log.append(f"{current_player.name} : {tile1} , {other_player.name} : {tile2}.")
            current_player, other_player = player, ai_player

        else:
            print("무승부!")
            match_log.append(f"무승부 : {tile1} vs. {tile2}.")

        # Print round points for both players
        print(f"라운드 포인트 : {player.name}: {player.round_points}, {ai_player.name}: {ai_player.round_points}")
        print("====================================================================================")

    # 경기 결과 출력 
    print("\n게임 종료!")
    print(f"최종 라운드 포인트 : {player.name}: {player.round_points}, {ai_player.name}: {ai_player.round_points}")
    print("\n경기 기록: ")
    print("=" * 30)  
    for i, log in enumerate(match_log):
        print(f"Round {i + 1}:")
        print(f" - {log}")
        print("-" * 30)  
    print("=" * 30)  