import random
import play_game 
import time 

class RandomAI:
    def __init__(self, name):
        self.name = name
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 라운드 포인트 
        self.round_log = []  # 각 라운드마다의 기록
        
    def choose_tile(self):
        # 랜덤하게 고르는 AI
        random.seed(time.time())
        chosen_tile = random.choice(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile