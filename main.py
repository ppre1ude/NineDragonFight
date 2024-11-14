
import play_game
if __name__ == "__main__":
    print("유저 vs AI 모드 : 1")
    print("규칙 AI vs 규칙 AI 모드 : 2")
    print("규칙 AI vs QLearning 모드 : 3")
    print("규칙 AI vs TreeAI 모드 : 4")

    n = int(input("모드를 입력하세요 : "))
    if n == 1: 
        play_game.user_vs_ai_play_game()
    elif n == 2: 
        k = int(input("match 수 입력 : "))
        play_game.ai_vs_ai_play_game(k)
    elif n == 3:
        k = int(input("match 수 입력 : "))
        play_game.ai_vs_QLearningAI_play_game(k)
    elif n == 4:
        k = int(input("match 수 입력 : "))
        play_game.ai_vs_TreeAI_play_game(k)