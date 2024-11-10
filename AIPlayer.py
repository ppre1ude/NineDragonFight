import random
import play_game
import time 

class RandomAI:
    def __init__(self):
        self.name = "RamdomAI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 라운드 포인트 
        self.round_log = []  # 각 라운드마다의 기록
        
    def choose_tile(self):
        # 랜덤하게 고르는 AI
        random.seed(time.time_ns())
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

class MiddleFirstAI:
    def __init__(self):
        self.name = "중간부터 내는 AI" 
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0

    def choose_tile(self):
        # 중앙값에 가까운 타일 선택
        sorted_tiles = sorted(self.tiles, key=lambda x: x.number)
        mid_index = len(sorted_tiles) // 2
        chosen_tile = sorted_tiles[mid_index]
        
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

class BasedProbabilityAI:
    def __init__(self):
        self.name = "확률 기반 AI" 
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0
        self.round_count = 0

    def choose_tile(self):
        self.round_count += 1
        win_probability = 1 - (self.round_count / 9)  # 남은 라운드에 따라 승리 확률 조정
        
        if win_probability > 0.5:
            # 승리 확률이 높으면 큰 타일 선택
            chosen_tile = max(self.tiles)
        else:
            # 승리 확률이 낮으면 작은 타일 선택
            chosen_tile = min(self.tiles)
        
        self.tiles.remove(chosen_tile)
        return chosen_tile

class CalculateOpponentTileAI:
    def __init__(self):
        self.name = "상대방 타일 추정 AI" 
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0
        self.opponent_high_tiles_played = 0
        self.opponent_low_tiles_played = 0

    def update_opponent_tile(self, opponent_tile):
        if opponent_tile.number > 5:
            self.opponent_high_tiles_played += 1
        else:
            self.opponent_low_tiles_played += 1

    def choose_tile(self):
        if self.opponent_high_tiles_played > self.opponent_low_tiles_played:
            # 상대가 높은 타일을 주로 냈으면 작은 타일로 대응
            chosen_tile = min(self.tiles)
        else:
            # 상대가 낮은 타일을 주로 냈으면 큰 타일로 대응
            chosen_tile = max(self.tiles)
        
        self.tiles.remove(chosen_tile)
        return chosen_tile

class MaintainPointsAI:
    def __init__(self):
        self.name = "라운드 포인트 유지 AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0

    def choose_tile(self):
        if self.round_points > 4:
            # 이미 높은 포인트를 획득했으면 작은 타일을 내며 포인트 유지 전략
            chosen_tile = min(self.tiles)
        else:
            # 포인트가 낮을 경우 큰 타일을 내어 승리 가능성 높이기
            chosen_tile = max(self.tiles)
        
        self.tiles.remove(chosen_tile)
        return chosen_tile
        
class QLearningAI:
    def __init__(self, epsilon=0.1, alpha=0.8, gamma=0.9, epsilon_decay=0.995, min_epsilon=0.01):
        self.name = "Q-Learning AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일
        self.q_table = {}  # Q-테이블 (상태 -> 행동)
        self.epsilon = epsilon  # 탐험 비율
        self.alpha = alpha  # 학습률
        self.gamma = gamma  # 할인율
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.round_points = 0
    
    def get_state(self):
        return tuple(sorted([tile.number for tile in self.tiles]))
    
    def choose_tile(self):
        random.seed(time.time())
        state = self.get_state()
        
        # Q-테이블에서 현재 상태에 대한 행동 선택
        if random.uniform(0, 1) < self.epsilon:
            tile = random.choice(self.tiles)
        else:
            # 이용 (Exploitation): Q값이 최대인 행동 선택
            if state not in self.q_table:
                self.q_table[state] = {tile.number: 0 for tile in self.tiles}  # 초기화
            
            # Q-값이 가장 큰 타일을 선택
            tile_number = max(self.q_table[state], key=self.q_table[state].get)
            
            # 해당 타일이 self.tiles에 존재하는지 확인하고 선택
            tile = next((t for t in self.tiles if t.number == tile_number), None)
        
        if tile:
            self.tiles.remove(tile)
            return tile
        else:
            # 만약 타일을 찾을 수 없다면, 리스트에서 랜덤하게 선택
            tile = random.choice(self.tiles)
            self.tiles.remove(tile)
            return tile
    
    def learn(self, previous_state, action, reward, next_state):
        if action is None:
            return
        
        # Q-테이블에서 이전 상태와 행동에 대한 Q-값을 업데이트
        if previous_state not in self.q_table:
            self.q_table[previous_state] = {tile.number: 0 for tile in self.tiles}  # 초기화
        
        # Q-값 업데이트 공식
        old_q_value = self.q_table[previous_state].get(action.number, 0)
        future_q_value = max(self.q_table.get(next_state, {}).values(), default=0)
        new_q_value = old_q_value + self.alpha * (reward + self.gamma * future_q_value - old_q_value)
        
        # Q-값을 새로운 값으로 업데이트
        self.q_table[previous_state][action.number] = new_q_value
        # epsilon 값을 점차 감소시킴
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.min_epsilon)  # epsilon이 최소값 아래로 내려가지 않게 함





        
            