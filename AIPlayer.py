import random
import math 
import play_game
import time 
from collections import Counter

class RandomAI:
    def __init__(self):
        self.name = "RamdomAI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 라운드 포인트 
        self.round_log = []  # 각 라운드마다의 기록

    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0        
        
    def choose_tile(self):
        # 랜덤하게 고르는 AI
        random.seed(time.time_ns())
        random.shuffle(self.tiles) # shuffle 코드를 추가 하냐 안 하냐의 차이가 이렇게 크다고???? 
        chosen_tile = random.choice(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile
    
class BigFirstAI:
    def __init__(self):
        self.name = "큰 숫자부터 내는 AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 현재 라운드 포인트 

    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0

    def choose_tile(self):
        chosen_tile = max(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile 
    
class SmallFirstAI:
    def __init__(self):
        self.name = "작은 숫자부터 내는 AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0  # 현재 라운드 포인트 

    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0

    def choose_tile(self):
        chosen_tile = min(self.tiles)
        self.tiles.remove(chosen_tile)
        return chosen_tile 

class MiddleFirstAI:
    def __init__(self):
        self.name = "중간부터 내는 AI" 
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일 
        self.round_points = 0

    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
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

    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0
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

"""로직 수정 필요해 보임"""
class BasedProbabilityAI:
    def __init__(self):
        self.name = "확률 기반 AI" 
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0

    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0

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

"""로직 자체가 잘못됨. 사용 안 함"""
# class CalculateOpponentTileAI:
#     def __init__(self):
#         self.name = "상대방 타일 추정 AI" 
#         self.tiles = [play_game.Tile(i) for i in range(1, 10)]
#         self.round_points = 0
#         self.opponent_high_tiles_played = 0
#         self.opponent_low_tiles_played = 0
    
#     def reset_tiles(self):
#         """타일과 점수를 초기화하는 메서드."""
#         self.tiles = [play_game.Tile(i) for i in range(1, 10)]
#         self.round_points = 0

#     def update_opponent_tile(self, opponent_tile):
#         if opponent_tile.number > 5:
#             self.opponent_high_tiles_played += 1
#         else:
#             self.opponent_low_tiles_played += 1

#     def choose_tile(self):
#         if self.opponent_high_tiles_played > self.opponent_low_tiles_played:
#             # 상대가 높은 타일을 주로 냈으면 작은 타일로 대응
#             chosen_tile = min(self.tiles)
#         else:
#             # 상대가 낮은 타일을 주로 냈으면 큰 타일로 대응
#             chosen_tile = max(self.tiles)
        
#         self.tiles.remove(chosen_tile)
#         return chosen_tile

class MaintainPointsAI:
    def __init__(self):
        self.name = "라운드 포인트 유지 AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0

    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
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
        
class SieunAI:
    def __init__(self):
        self.name = "전략적 확률 예측 AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0
        self.opponent_tile_distribution = Counter(range(1, 10))

    def reset_tiles(self):
        """타일과 점수를 초기화하고 상대의 타일 분포를 초기 상태로 리셋합니다."""
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0
        self.opponent_tile_distribution = Counter(range(1, 10))

    def update_opponent_distribution_after_loss(self, my_tile):
        """
        패배 시 큰 타일 확률을 높이고 작은 타일도 약간 반영
        """
        for value in range(my_tile.number + 1, 10):
            self.opponent_tile_distribution[value] += 1
        for value in range(1, my_tile.number):
            self.opponent_tile_distribution[value] += 0.5

    def update_opponent_distribution_after_draw(self, drawn_tile):
        """무승부 시 상대의 해당 타일을 제거합니다."""
        if self.opponent_tile_distribution[drawn_tile.number] > 0:
            self.opponent_tile_distribution[drawn_tile.number] -= 1

    def choose_tile(self):
        """상대의 패를 예측하여 최적의 타일을 선택하거나 전략적으로 큰 차이로 패배를 고려합니다."""
        best_tile = None
        max_win_chance = -1

        for tile in self.tiles:
            win_chance = self.calculate_win_chance(tile)

            # 큰 차이로 패배할 전략적 선택지를 고려
            if self.should_lose_big(tile):
                win_chance *= 0.5  # 전략적 손실이므로 승리 확률을 낮게 설정해 강하게 유도

            if win_chance > max_win_chance:
                best_tile = tile
                max_win_chance = win_chance

        self.tiles.remove(best_tile)
        
        return best_tile

    def calculate_win_chance(self, my_tile):
        """내 타일이 상대 타일에 대해 이길 확률을 계산합니다."""
        win_chance = 0.0
        total_possible = sum(self.opponent_tile_distribution.values())
        
        for opponent_tile_value, count in self.opponent_tile_distribution.items():
            if (my_tile.number == 1 and opponent_tile_value == 9) or my_tile.number > opponent_tile_value:
                win_chance += count / total_possible

        return win_chance

    def should_lose_big(self, my_tile):
        """특정 상황에서 큰 차이로 지도록 유도할지를 판단합니다. << 대체 왜 있는진 모르겠는데 승률 6할의 비결"""
        # 특정 타일(예: 8)로 패배하여 상대의 더 작은 타일을 남기는 전략을 사용할지 결정
        high_risk_tiles = [8, 7]  # 예시: 큰 차이로 지기 위해 주로 사용할 타일
        return my_tile.number in high_risk_tiles

"""
엡실론 (ε): 탐험과 이용의 균형을 조절하는 값. 값이 클수록 탐험을 많이 하며, 값이 작을수록 이미 알고 있는 행동을 자주 선택.
알파 (α): 학습률. 값이 클수록 새로운 경험에 따라 Q-값이 빠르게 갱신되고, 값이 작을수록 이전 정보에 영향을 더 받음.
감마 (γ): 할인율. 미래 보상의 중요도를 조절. 값이 크면 장기적인 목표를, 작으면 단기적인 목표를 중시.
"""
class QLearningAI:
    def __init__(self, epsilon=1, alpha=0.3, gamma=0.9, epsilon_decay=0.95, min_epsilon=0.5):
        self.name = "Q-Learning AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  # 1 ~ 9 까지의 타일
        self.q_table = {}  # Q-테이블 (상태 -> 행동)
        self.epsilon = epsilon  # 탐험 비율
        self.alpha = alpha  # 학습률
        self.gamma = gamma  # 할인율    
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.round_points = 0
        self.탐험횟수 = 0
        self.이용횟수 = 0 
    
    def get_state(self):
        return tuple(sorted([tile.number for tile in self.tiles]))
    
    def choose_tile(self):
        random.seed(time.time_ns())
        state = self.get_state()
        
        # Q-테이블에서 현재 상태에 대한 행동 선택
        if random.uniform(0, 1) <= self.epsilon:
            self.탐험횟수 += 1
            tile = random.choice(self.tiles)
        else:
            self.이용횟수 += 1
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
    
    def reset_tiles(self):
        # 1부터 9까지 타일을 다시 할당
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0

    def learn(self, q_learning_played_tile, reward):
        # 게임 결과 기반 학습 진행
        for tile in q_learning_played_tile:
            state = self.get_state()
            # Q-테이블에서 이전 상태와 행동에 대한 Q-값을 업데이트
            if state not in self.q_table:
                self.q_table[state] = {tile.number: 0 for tile in self.tiles}  # 초기화
            
            old_q_value = self.q_table[state].get(tile.number, 0)
            future_q_value = max(self.q_table.get(state, {}).values(), default=0)
            new_q_value = old_q_value + self.alpha * (reward + self.gamma * future_q_value - old_q_value)
            
            # Q-값을 새로운 값으로 업데이트
            self.q_table[state][tile.number] = new_q_value
        # epsilon 값을 점차 감소시킴
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.min_epsilon)  # epsilon이 최소값 아래로 내려가지 않게 함

class DaehanQLearning:
    def __init__(self):
        self.name = "Daehan - Q Learning AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]  
        self.round_points = 0
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
     
    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0  
    
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

            """최대 q 값이 손패에 없다면 다음 최대 q 값을 선택하는 로직(안 쓰는게 더 좋음)"""
            # for tile_number, q_value in sorted_current_round_q_table:
            #     max_tile = play_game.Tile(tile_number)
            #     if max_tile in self.tiles:
            #         self.tiles.remove(max_tile)
            #         return max_tile
            
            """최대 q 값이 손패에 없다면 랜덤으로 선택하는 로직"""
            for tile_number, q_value in sorted_current_round_q_table:
                max_tile = play_game.Tile(tile_number)
                if max_tile in self.tiles:
                    self.tiles.remove(max_tile)
                    return max_tile
                else:
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

"""트리 노드"""
class TreeNode:
    def __init__(self, remaining_tiles, used_tiles):
        self.remaining_tiles = remaining_tiles  # 남은 타일 리스트
        self.used_tiles = used_tiles  # 사용된 타일 리스트
        self.children = []  # 자식 노드들

    def add_child(self, child_node):
        """자식 노드를 추가"""
        self.children.append(child_node)

    def expand(self, opponent_tile):
        """현재 노드에서 가능한 타일 조합으로 트리 확장"""
        new_children = []
        for tile in self.remaining_tiles:
            if tile > opponent_tile:  # Tile 객체의 __lt__ 비교 연산자 사용
                # 타일 선택 후, 새로운 남은 타일과 사용된 타일 리스트 생성
                new_remaining = [t for t in self.remaining_tiles if t != tile]  # 리스트 내포 사용
                new_used = self.used_tiles + [tile]
                child_node = TreeNode(new_remaining, new_used)
                new_children.append(child_node)
                self.add_child(child_node)
        return new_children

"""트리 AI"""
class TreeAI:
    def __init__(self):
        self.name = "Tree AI"
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0
        self.root = TreeNode(self.tiles, [])  # 초기 루트 노드
        self.current_node = self.root  # 현재 탐색 중인 노드

    def reset_tiles(self):
        """타일과 점수를 초기화하는 메서드."""
        self.tiles = [play_game.Tile(i) for i in range(1, 10)]
        self.round_points = 0
        self.root = TreeNode(self.tiles, [])
        self.current_node = self.root

    def update_possible_opponent_tiles(self, opponent_tile, result):
        """상대가 낸 타일을 기준으로 가능한 트리 조합을 확장"""
        if result == 'win':
            self.current_node = next(
                (child for child in self.current_node.children if opponent_tile in [t.number for t in child.used_tiles]),
                None
            )
        elif result == 'lose':
            self.current_node = next(
                (child for child in self.current_node.children if opponent_tile not in [t.number for t in child.used_tiles]),
                None
            )
        
        if self.current_node is None:
            self.current_node = self.root

    def minimax(self, node, depth, maximizing_player, opponent_tiles):
        """미니맥스 알고리즘을 통해 최적의 타일 선택 경로를 평가."""
        if depth == 0 or not node.remaining_tiles:
            return self.evaluate(node, opponent_tiles)

        if maximizing_player:
            max_eval = -math.inf
            for my_tile in node.remaining_tiles:
                new_remaining = [t for t in node.remaining_tiles if t != my_tile]
                child_node = TreeNode(new_remaining, node.used_tiles + [my_tile])
                node.add_child(child_node)

                opponent_tile = opponent_tiles[0] if opponent_tiles else None
                if opponent_tile and my_tile.number > opponent_tile.number:
                    eval = self.minimax(child_node, depth - 1, False, opponent_tiles[1:])
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for opp_tile in opponent_tiles:
                new_remaining = [t for t in node.remaining_tiles if t.number > opp_tile.number]
                child_node = TreeNode(new_remaining, node.used_tiles + [opp_tile])
                node.add_child(child_node)

                eval = self.minimax(child_node, depth - 1, True, opponent_tiles[1:])
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(self, node, opponent_remaining_tiles):
        """상대 타일과의 비교를 통해 더 전략적인 평가 함수."""
        score = 0

        # 1. 승리 가능한 타일 수에 따라 점수 추가
        for my_tile in node.remaining_tiles:
            win_count = sum(1 for opp_tile in opponent_remaining_tiles if my_tile.number > opp_tile.number)
            score += win_count * 2  # 승리 가능한 타일마다 점수를 부여
        
        # 2. 상대 타일과의 숫자 차이에 따른 점수
        for my_tile in node.remaining_tiles:
            for opp_tile in opponent_remaining_tiles:
                if my_tile.number > opp_tile.number:
                    score += (my_tile.number - opp_tile.number)  # 타일 간의 차이가 클수록 더 높은 점수

        # 3. 미래 라운드를 위한 타일 유리성 점수
        future_win_potential = sum(
            1 for my_tile in node.remaining_tiles if any(my_tile.number > opp_tile.number for opp_tile in opponent_remaining_tiles)
        )
        score += future_win_potential * 3  # 미래 승리 가능성이 높은 경우 추가 점수

        return score

    def choose_tile(self):
        """미래 라운드를 고려해 최적의 타일을 선택."""
        best_score = -math.inf
        best_tile = None

        for tile in self.tiles:
            new_remaining = [t for t in self.tiles if t != tile]
            root_node = TreeNode(new_remaining, [tile])
            score = self.minimax(root_node, depth=3, maximizing_player=False, opponent_tiles=[t for t in self.tiles])

            if score > best_score:
                best_score = score
                best_tile = tile

        if best_tile in self.tiles:
            self.tiles.remove(best_tile)
        return best_tile



