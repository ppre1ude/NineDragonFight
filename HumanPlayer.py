import play_game 

class Player:
    def __init__(self):
        self.name = "User"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 라운드 포인트 
        self.round_log = []  # 각 라운드마다의 기록

    def choose_tile(self):
        print(f"{self.name}, 손 패 : {[str(tile) for tile in self.tiles]}")
        choice = int(input(f"{self.name}, 패 선택 (1-9): "))
        chosen_tile = next(tile for tile in self.tiles if tile.number == choice)
        self.tiles.remove(chosen_tile)
        return chosen_tile