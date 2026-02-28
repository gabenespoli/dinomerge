from src.constants import GRID_WIDTH, GRID_HEIGHT, GRID_OFFSET_X, GRID_OFFSET_Y, SLOT_SIZE
from src.dinosaur import Dinosaur


class Grid:
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.slots: list[list[Dinosaur | None]] = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.dragging = None
        self.drag_start = None
    
    def get_slot_at(self, x: int, y: int) -> tuple[int, int] | None:
        for row in range(self.height):
            for col in range(self.width):
                slot_x = GRID_OFFSET_X + col * SLOT_SIZE
                slot_y = GRID_OFFSET_Y + row * SLOT_SIZE
                if (slot_x <= x <= slot_x + SLOT_SIZE and 
                    slot_y <= y <= slot_y + SLOT_SIZE):
                    return (row, col)
        return None
    
    def get_dinosaur_at(self, row: int, col: int) -> Dinosaur | None:
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.slots[row][col]
        return None
    
    def place_dinosaur(self, row: int, col: int, dinosaur: Dinosaur):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.slots[row][col] = dinosaur
            dinosaur.grid_x = col
            dinosaur.grid_y = row
    
    def remove_dinosaur(self, row: int, col: int) -> Dinosaur | None:
        if 0 <= row < self.height and 0 <= col < self.width:
            dino = self.slots[row][col]
            if dino:
                dino.grid_x = None
                dino.grid_y = None
            self.slots[row][col] = None
            return dino
        return None
    
    def move_dinosaur(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        if (0 <= from_row < self.height and 0 <= from_col < self.width and
            0 <= to_row < self.height and 0 <= to_col < self.width):
            
            source_dino = self.slots[from_row][from_col]
            target_dino = self.slots[to_row][to_col]
            
            if source_dino is None:
                return False
            
            if target_dino is None:
                self.slots[to_row][to_col] = source_dino
                self.slots[from_row][from_col] = None
                source_dino.grid_x = to_col
                source_dino.grid_y = to_row
                return True
            
            if (target_dino.level == source_dino.level and 
                target_dino.level < 10):
                new_level = target_dino.level + 1
                new_dino = Dinosaur(new_level)
                self.slots[to_row][to_col] = new_dino
                new_dino.grid_x = to_col
                new_dino.grid_y = to_row
                self.slots[from_row][from_col] = None
                return True
            
            return False
        return False
    
    def get_all_dinosaurs(self) -> list[Dinosaur]:
        dinos = []
        for row in range(self.height):
            for col in range(self.width):
                if self.slots[row][col]:
                    dinos.append(self.slots[row][col])
        return dinos
    
    def get_alive_dinosaurs(self) -> list[Dinosaur]:
        return [d for d in self.get_all_dinosaurs() if d.alive]
    
    def count_empty_slots(self) -> int:
        count = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.slots[row][col] is None:
                    count += 1
        return count
    
    def get_front_line_dinosaurs(self) -> list[Dinosaur]:
        dinos = []
        for col in range(self.width):
            if self.slots[0][col]:
                dinos.append(self.slots[0][col])
            if self.slots[1][col]:
                dinos.append(self.slots[1][col])
        return [d for d in dinos if d.alive]
    
    def get_back_line_dinosaurs(self) -> list[Dinosaur]:
        dinos = []
        for row in range(2, self.height):
            for col in range(self.width):
                if self.slots[row][col]:
                    dinos.append(self.slots[row][col])
        return [d for d in dinos if d.alive]
    
    def clear(self):
        self.slots = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def copy_from(self, other: 'Grid'):
        self.clear()
        for row in range(self.height):
            for col in range(self.width):
                other_dino = other.slots[row][col]
                if other_dino:
                    dino = Dinosaur(other_dino.level)
                    dino.current_hp = other_dino.current_hp
                    dino.alive = other_dino.alive
                    self.place_dinosaur(row, col, dino)
