from enum import Enum
from src.grid import Grid
from src.dinosaur import Dinosaur
from src.constants import MAX_LEVEL, GRID_WIDTH, FRONT_LINE_COLS


class GameState(Enum):
    MENU = "menu"
    ARMY = "army"
    BATTLE = "battle"
    VICTORY = "victory"
    DEFEAT = "defeat"
    SHOP = "shop"


class DinoMergeGame:
    def __init__(self):
        self.state = GameState.ARMY
        self.tokens = 0
        self.current_level = 1
        self.grid = Grid()
        self.enemy_grid = Grid()
        self.battle_result = None
        self.initialize_starting_army()
        self.generate_enemy_army(self.current_level)
    
    def initialize_starting_army(self):
        front_col_start = GRID_WIDTH - FRONT_LINE_COLS
        for i in range(4):
            col = front_col_start + (i % FRONT_LINE_COLS)
            row = i // FRONT_LINE_COLS
            dino = Dinosaur(1)
            self.grid.place_dinosaur(row, col, dino)
    
    def buy_dinosaur(self, level: int, price: int) -> bool:
        if self.tokens >= price and self.grid.count_empty_slots() > 0:
            for row in range(self.grid.height):
                for col in range(self.grid.width):
                    if self.grid.get_dinosaur_at(row, col) is None:
                        dino = Dinosaur(level)
                        self.grid.place_dinosaur(row, col, dino)
                        self.tokens -= price
                        return True
        return False
    
    def generate_enemy_army(self, level: int):
        from src.constants import ENEMY_ARMIES, FRONT_LINE_COLS
        self.enemy_grid.clear()
        enemy_levels = ENEMY_ARMIES.get(level, [level])
        
        for i, level in enumerate(enemy_levels):
            col = i % FRONT_LINE_COLS
            row = i // FRONT_LINE_COLS
            dino = Dinosaur(level)
            dino.is_enemy = True
            self.enemy_grid.place_dinosaur(row, col, dino)
    
    def get_reward(self):
        from src.constants import REWARD_TOKENS
        return REWARD_TOKENS.get(self.current_level, 75)
    
    def next_level(self):
        if self.current_level < MAX_LEVEL:
            self.current_level += 1
            self.generate_enemy_army(self.current_level)
        else:
            self.current_level = MAX_LEVEL
    
    def reset_to_level(self, level: int):
        self.current_level = level
    
    def is_game_won(self) -> bool:
        return self.current_level >= MAX_LEVEL
