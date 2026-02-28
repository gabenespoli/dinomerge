import pygame

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800
GRID_WIDTH = 5
GRID_HEIGHT = 8
GRID_OFFSET_X = 40
GRID_OFFSET_Y = 100
SLOT_SIZE = 60

COLORS = {
    'background': (30, 30, 40),
    'grid_slot': (50, 50, 60),
    'grid_slot_hover': (70, 70, 80),
    'front_line': (60, 50, 50),
    'back_line': (40, 40, 50),
    'ui_panel': (45, 45, 55),
    'text': (220, 220, 220),
    'text_dark': (150, 150, 150),
    'button': (80, 120, 200),
    'button_hover': (100, 140, 220),
    'button_disabled': (60, 60, 70),
    'victory': (100, 200, 100),
    'defeat': (200, 80, 80),
    'highlight': (255, 200, 100),
}

DINOSAURS = {
    1: {'name': 'Dryosaurus', 'hp': 20, 'attack': 5, 'speed': 10, 'color': (100, 200, 100), 'shape': 'triangle_small'},
    2: {'name': 'Styracosaurus', 'hp': 40, 'attack': 10, 'speed': 9, 'color': (150, 180, 220), 'shape': 'triangle'},
    3: {'name': 'Triceratops', 'hp': 80, 'attack': 20, 'speed': 7, 'color': (120, 200, 180), 'shape': 'triangle_large'},
    4: {'name': 'Ankylosaurus', 'hp': 160, 'attack': 30, 'speed': 5, 'color': (160, 140, 100), 'shape': 'rectangle'},
    5: {'name': 'Stegosaurus', 'hp': 250, 'attack': 45, 'speed': 4, 'color': (180, 100, 100), 'shape': 'rectangle'},
    6: {'name': 'Spinosaurus', 'hp': 400, 'attack': 70, 'speed': 8, 'color': (200, 150, 50), 'shape': 'diamond'},
    7: {'name': 'Brachiosaurus', 'hp': 650, 'attack': 90, 'speed': 3, 'color': (140, 160, 200), 'shape': 'rectangle_large'},
    8: {'name': 'Diplodicus', 'hp': 900, 'attack': 120, 'speed': 4, 'color': (160, 180, 140), 'shape': 'rectangle_long'},
    9: {'name': 'Tarbosaurus', 'hp': 1200, 'attack': 180, 'speed': 6, 'color': (180, 60, 60), 'shape': 'triangle_large'},
    10: {'name': 'Tyrannosaurus', 'hp': 2000, 'attack': 300, 'speed': 5, 'color': (220, 200, 50), 'shape': 'triangle_large'},
}

PRICES = {
    1: 75,
    2: 150,
    3: 300,
    4: 600,
    5: 1200,
    6: 2400,
    7: 4800,
    8: 9600,
    9: 19200,
    10: 38400,
}

ENEMY_ARMIES = {
    1: [1, 1],
    2: [1, 2],
    3: [2, 2, 3],
    4: [3, 3, 3, 4],
    5: [4, 4, 5, 5],
    6: [5, 5, 5, 6, 6],
    7: [6, 6, 7, 7, 7],
    8: [7, 7, 7, 7, 8, 8],
    9: [8, 8, 9, 9, 9],
    10: [9, 9, 9, 9, 9, 10, 10],
}

REWARD_TOKENS = {
    1: 75,
    2: 150,
    3: 300,
    4: 600,
    5: 1200,
    6: 2400,
    7: 4800,
    8: 9600,
    9: 19200,
    10: 38400,
}

FRONT_LINE_ROWS = 2
BACK_LINE_ROWS = 6
FRONT_LINE_DEFENSE_BONUS = 1.5

MAX_LEVEL = 10
