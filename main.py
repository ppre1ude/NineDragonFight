import play_game
if __name__ == "__main__":
    print("유저 vs AI 모드 : 1")
    print("AI vs AI 모드 : 2")

    n = int(input())
    if n == 1: 
        play_game.user_vs_ai_play_game()
    else : 
        k = int(input("match 수 입력 : "))
        play_game.ai_vs_ai_play_game(k)