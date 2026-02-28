# DinoMerge

A dinosaur army merging game built with Python and Pygame.

## How to Play

### Setup
```bash
pip install pygame
python main.py
```

### Gameplay

**Goal**: Build the strongest dinosaur army and defeat all 10 enemy levels!

**Merging**: Drag one dinosaur onto another of the same level to merge them into a stronger dinosaur. Two Level 1s become a Level 2, two Level 2s become a Level 3, etc.

**Front Lines**: The right 2 columns of your grid (left 2 columns of enemy grid) are your front lines. Units on the front lines receive 1.5x defense bonus.

**Battle**: Click BATTLE to fight the enemy army. Battles are automatic - watch as your dinosaurs attack!

**Shop**: Purchase new dinosaurs with tokens earned from battles.

### Dinosaur Types

| Level | Name | HP | Attack |
|-------|------|-----|--------|
| 1 | Dryosaurus | 20 | 5 |
| 2 | Styracosaurus | 40 | 10 |
| 3 | Triceratops | 80 | 20 |
| 4 | Ankylosaurus | 160 | 30 |
| 5 | Stegosaurus | 250 | 45 |
| 6 | Spinosaurus | 400 | 70 |
| 7 | Brachiosaurus | 650 | 90 |
| 8 | Diplodicus | 900 | 120 |
| 9 | Tarbosaurus | 1200 | 180 |
| 10 | Tyrannosaurus | 2000 | 300 |

### Controls
- **Click and drag** dinosaurs to move or merge them
- **Click shop buttons** to purchase new dinosaurs
- **Click BATTLE** to start a battle
- **Click** after victory/defeat to return to army screen
