import random
from src.grid import Grid
from src.dinosaur import Dinosaur


class Battle:
    def __init__(self, player_grid: Grid, enemy_grid: Grid):
        self.player_grid = player_grid
        self.enemy_grid = enemy_grid
        self.battle_log = []
        self.turn_count = 0
        self.max_turns = 100
        self.last_attack = None
    
    def get_all_combatants(self) -> list[Dinosaur]:
        player_dinos = self.player_grid.get_all_dinosaurs()
        enemy_dinos = self.enemy_grid.get_all_dinosaurs()
        return [d for d in player_dinos + enemy_dinos if d.alive]
    
    def get_alive_player_dinos(self) -> list[Dinosaur]:
        return [d for d in self.player_grid.get_all_dinosaurs() if d.alive]
    
    def get_alive_enemy_dinos(self) -> list[Dinosaur]:
        return [d for d in self.enemy_grid.get_all_dinosaurs() if d.alive]
    
    def is_battle_over(self) -> bool:
        player_alive = len(self.get_alive_player_dinos()) > 0
        enemy_alive = len(self.get_alive_enemy_dinos()) > 0
        
        if not player_alive:
            return True
        if not enemy_alive:
            return True
        if self.turn_count >= self.max_turns:
            return True
        
        return False
    
    def get_winner(self) -> str | None:
        if not self.get_alive_enemy_dinos():
            return "player"
        if not self.get_alive_player_dinos():
            return "enemy"
        if self.turn_count >= self.max_turns:
            return "draw"
        return None
    
    def execute_turn(self):
        self.turn_count += 1
        combatants = self.get_all_combatants()
        combatants.sort(key=lambda d: d.speed, reverse=True)
        
        for attacker in combatants:
            if not attacker.alive:
                continue
            
            if attacker.is_enemy:
                targets = self.get_alive_player_dinos()
            else:
                targets = self.get_alive_enemy_dinos()
            
            if not targets:
                break
            
            target = random.choice(targets)
            damage = attacker.attack
            target.take_damage(damage)
            
            self.last_attack = {
                'attacker': attacker,
                'target': target,
                'damage': damage,
                'attacker_hp': attacker.current_hp,
                'target_hp': target.current_hp,
            }
            
            self.battle_log.append({
                'turn': self.turn_count,
                'attacker': attacker.name,
                'target': target.name,
                'damage': damage,
                'attacker_level': attacker.level,
                'target_level': target.level,
            })
            
            if not target.alive:
                continue
            
            if self.is_battle_over():
                break
    
    def run_battle(self) -> str:
        while not self.is_battle_over():
            self.execute_turn()
        
        winner = self.get_winner()
        return winner if winner else "draw"
