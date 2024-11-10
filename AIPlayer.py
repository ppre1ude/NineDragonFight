import random
import play_game
import time 

class RandomAI:
    def __init__(self):
        self.name = "RamdomAI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 라운드 포인트 
        self.round_log = []  # 각 라운드마다의 기록
        self.seed = time.time()
        
    def choose_tile(self):
        # 랜덤하게 고르는 AI
        random.seed(self.seed)
        chosen_tile = random.choice(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile

class BigFirstAI:
    def __init__(self):
        self.name = "큰 숫자부터 내는 AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 현재 라운드 포인트 

    def choose_tile(self):
        chosen_tile = max(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile 
    
class SmallFirstAI:
    def __init__(self):
        self.name = "작은 숫자부터 내는 AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 현재 라운드 포인트 

    def choose_tile(self):
        chosen_tile = min(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile 

class BigSmallShuffleAI:
    def __init__(self):
        self.name = "큰 숫자, 작은 숫자 번갈아 내는 AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 현재 라운드 포인트
        self.use_high_tile = True  # 첫 라운드는 큰 타일부터 시작

    def choose_tile(self):
        if self.use_high_tile:
            # 남은 타일 중 가장 큰 타일 선택
            chosen_tile = max(self.tiles)
        else:
            # 남은 타일 중 가장 작은 타일 선택
            chosen_tile = min(self.tiles)
        
        # 선택한 타일은 사용 후 목록에서 제거
        self.tiles.remove(chosen_tile)
        
        # 다음 라운드는 반대 크기의 타일을 선택하도록 플래그 변경
        self.use_high_tile = not self.use_high_tile
        
        return chosen_tile


        



        
            