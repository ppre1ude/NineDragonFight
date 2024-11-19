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