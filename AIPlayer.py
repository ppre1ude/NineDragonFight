import random 
import time 
from Tile import Tile
from abc import ABC, abstractmethod
from collections import Counter

class BaseAI(ABC):
    def __init__(self, name):
        self.name = name
        self.tiles = [Tile(i) for i in range(1, 10)]
        self.round_points = 0
        
    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
        self.tiles = [Tile(i) for i in range(1, 10)]
        self.round_points = 0  

    @abstractmethod
    def choose_tile(self):
        pass   

class RandomAI(BaseAI):
    def __init__(self):
        super().__init__("Random AI")

    def choose_tile(self):
        random.seed(time.time_ns())
        random.shuffle(self.tiles)
        chosen_tile = random.choice(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile
    
class BigFirstAI(BaseAI):
    def __init__(self):
        super().__init__("Big First AI")

    def choose_tile(self):
        chosen_tile = max(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile 
    
class SmallFirstAI(BaseAI):
    def __init__(self):
        super().__init__("Small First AI")

    def choose_tile(self):
        chosen_tile = min(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile 

class MiddleFirstAI(BaseAI):
    def __init__(self):
        super().__init__("Middle First AI")

    def choose_tile(self):
        # 중앙값에 가까운 타일 선택
        sorted_tiles = sorted(self.tiles, key=lambda x: x.number)
        mid_index = len(sorted_tiles) // 2
        chosen_tile = sorted_tiles[mid_index]
        
        self.tiles.remove(chosen_tile)
        return chosen_tile

class BigSmallShuffleAI(BaseAI):
    def __init__(self):
        super().__init__("Big Small Shuffle AI")
        self.use_high_tile = True

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

class MaintainPointsAI(BaseAI):
    def __init__(self):
        super().__init__("Maintain Points AI")

    def choose_tile(self):
        if self.round_points > 4:
            # 이미 높은 포인트를 획득했으면 작은 타일을 내며 포인트 유지 전략
            chosen_tile = min(self.tiles)
        else:
            # 포인트가 낮을 경우 큰 타일을 내어 승리 가능성 높이기
            chosen_tile = max(self.tiles)
        
        self.tiles.remove(chosen_tile)
        return chosen_tile
        
class SieunAI(BaseAI):
    def __init__(self):
        super().__init__("SieunAI")
        self.opponent_tile_distribution = Counter(range(1, 10))  # 상대 타일 초기 분포

    def reset_tiles(self):
        """타일과 점수를 초기화하고 상대의 타일 분포도 리셋."""
        super().reset_tiles()
        self.opponent_tile_distribution = Counter(range(1, 10))

    def update_opponent_distribution_after_loss(self, my_tile):
        """패배 시 상대의 타일 분포 업데이트 (큰 타일의 확률 증가)."""
        for value in range(my_tile.number + 1, 10):
            self.opponent_tile_distribution[value] += 1

    def update_opponent_distribution_after_draw(self, drawn_tile):
        """무승부 시 해당 타일의 분포 감소."""
        if self.opponent_tile_distribution[drawn_tile.number] > 0:
            self.opponent_tile_distribution[drawn_tile.number] -= 1

    def calculate_win_chance(self, my_tile):
        """내 타일이 상대 타일을 이길 확률 계산."""
        win_chance = 0.0
        total_possible = sum(self.opponent_tile_distribution.values())

        # 상대 타일을 기준으로 승리 확률 계산
        for opponent_tile_value, count in self.opponent_tile_distribution.items():
            if (my_tile.number == 1 and opponent_tile_value == 9) or my_tile.number > opponent_tile_value:
                win_chance += count / total_possible

        return win_chance

    def choose_tile(self):
        """최적의 타일 선택 (승리 확률이 높은 타일)."""
        best_tile = None
        max_win_chance = -1

        for tile in self.tiles:
            win_chance = self.calculate_win_chance(tile)
            if win_chance > max_win_chance:
                best_tile = tile
                max_win_chance = win_chance

        # 선택한 타일 제거
        if best_tile:
            self.tiles.remove(best_tile)
        return best_tile

class DaehanQLearning(BaseAI):
    def __init__(self):
        super().__init__("Daehan - Q Learning AI")
        self.q_table = {round : {key : 0 for key in range(1, 10)} for round in range(1, 10)}
        self.epsilon = 1.0
        self.epsilon_decay = 0.95
        self.min_epsilon = 0.1

    def display_q_table(self):
        """Q Table을 전체 라운드를 포함한 9x9 표로 출력하는 메서드."""
        
        # 열 헤더 출력
        print("\t\t" + " ".join([f"Tile {i:<2}     " for i in range(1, 10)]))
        print("        " + "-" * 120)  # 구분선

        # 9x9 매트릭스 형태로 구성하여 출력
        for round in range(1, 10):  # 라운드가 1부터 9까지 있다고 가정
            row = []
            for tile in range(1, 10):
                # 각 라운드의 각 타일 Q 값을 가져오고 없는 값은 0으로 설정
                q_value = self.q_table.get(round, {}).get(tile, 0)
                row.append(f"{q_value:10.2f}")  # 소수점 2자리로 정렬하여 출력, 칸 간격 10칸으로 설정
            print(f"Round {round:<2} | " + " | ".join(row))  # 라운드 번호와 값 출력

        print("        " + "-" * 120)  # 마지막 구분선
    
    def choose_tile(self, current_round):
        """타일을 고르는 메서드"""
        random.seed(time.time_ns())

        # 탐험 
        if random.uniform(0,1) <= self.epsilon:
            random.shuffle(self.tiles)
            chosen_tile = random.choice(self.tiles)
            self.tiles.remove(chosen_tile)
            return chosen_tile
        # 이용 -> 현재 라운드의 큐 테이블 값이 최댓값인 타일 선택 
        else:
            # 현재 라운드 큐 테이블
            current_round_q_table = self.q_table[current_round]

            # 내림차순 정렬된 현재 라운드 큐 테이블 <-- 안 써도 될 듯? 최적화 필요 
            sorted_current_round_q_table = sorted(
                current_round_q_table.items(),
                key = lambda x : x[1],
                reverse = True 
            )
            
            """최대 q 값이 손패에 없다면 랜덤으로 선택하는 로직"""
            for tile_number, q_value in sorted_current_round_q_table:
                max_tile = Tile(tile_number)
                if max_tile in self.tiles:
                    self.tiles.remove(max_tile)
                    return max_tile
                else:
                    random.shuffle(self.tiles)
                    chosen_tile = random.choice(self.tiles)
                    self.tiles.remove(chosen_tile)
                    return chosen_tile                
                
    # 한 경기가 끝나고 큐 테이블을 업데이트 해줘야 함 
    def update_q_table(self,q_learning_played_tiles, opponent_played_tiles, game_result):      
        for round in range(1, 10):
            q_tile = q_learning_played_tiles[round-1].number
            opponent_tile = opponent_played_tiles[round-1].number
            
            tile_diff = abs(q_tile - opponent_tile)
            
            # 상대와 동일한 타일을 냈다면 큐값 업데이트 x
            if tile_diff == 0:
                continue  
            
            old_q_value = self.q_table[round][q_tile]

            """더 큰 포인트차로 이기도록 유도할 순 없을까"""
            # 게임 승리 -> 한 라운드에서 이긴다면 작은 차이로 이기는 것이 더 좋다
            if game_result > 0:
                self.q_table[round][q_tile] += 1 / tile_diff
            elif game_result == 0: pass 
            # 게임 패배 -> 진다면 큰 차이로 지는 것이 더 좋다
            else:
                 self.q_table[round][q_tile] -= 1 / tile_diff
        
        # epsilon 감소
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.min_epsilon)