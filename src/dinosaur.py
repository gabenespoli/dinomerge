import uuid
from src.constants import DINOSAURS


class Dinosaur:
    def __init__(self, level: int):
        self.id = str(uuid.uuid4())
        self.level = level
        self.stats = DINOSAURS[level]
        self.name = self.stats['name']
        self.max_hp = self.stats['hp']
        self.current_hp = self.max_hp
        self.attack = self.stats['attack']
        self.speed = self.stats['speed']
        self.color = self.stats['color']
        self.shape = self.stats['shape']
        self.grid_x: int | None = None
        self.grid_y: int | None = None
        self.is_enemy = False
        self.alive = True
    
    @property
    def is_front_line(self) -> bool:
        if self.grid_y is not None:
            return self.grid_y < 2
        return False
    
    def take_damage(self, damage: float):
        if self.is_front_line:
            damage = damage / 1.5
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            self.alive = False
    
    def clone(self):
        new_dino = Dinosaur(self.level)
        new_dino.current_hp = self.current_hp
        new_dino.alive = self.alive
        return new_dino
    
    def copy_from(self, other: 'Dinosaur'):
        self.level = other.level
        self.stats = other.stats
        self.name = other.name
        self.max_hp = other.max_hp
        self.current_hp = other.current_hp
        self.attack = other.attack
        self.speed = other.speed
        self.color = other.color
        self.shape = other.shape
        self.alive = other.alive
