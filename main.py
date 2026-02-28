import pygame
import sys
from src.constants import *
from src.game_state import DinoMergeGame, GameState
from src.battle import Battle
from src.renderer import Renderer
from src.shop import Shop


class DinoMergeApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("DinoMerge")
        self.clock = pygame.time.Clock()
        
        self.game = DinoMergeGame()
        self.renderer = Renderer(self.screen)
        self.shop = Shop()
        
        self.battle = None
        self.battle_timer = 0
        self.battle_speed = 500
        
        self.dragging_dino = None
        self.drag_from_pos = None
        
        self.hovered_slot = None
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_click(event.pos)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.handle_release(event.pos)
    
    def handle_click(self, pos):
        if self.game.state == GameState.ARMY:
            self.handle_army_click(pos)
        elif self.game.state == GameState.VICTORY:
            self.handle_victory_click()
        elif self.game.state == GameState.DEFEAT:
            self.handle_defeat_click()
    
    def handle_army_click(self, pos):
        player_offset_x = 40
        player_offset_y = 120
        slot = self.game.grid.get_slot_at(pos[0], pos[1], player_offset_x, player_offset_y)
        
        if slot:
            row, col = slot
            dino = self.game.grid.get_dinosaur_at(row, col)
            if dino:
                self.dragging_dino = dino
                self.drag_from_pos = slot
        
        shop_x = 50
        shop_y = 120 + GRID_HEIGHT * SLOT_SIZE + 30 + 35
        for level in range(1, 11):
            btn_x = shop_x + ((level - 1) % 5) * 130
            btn_y = shop_y + ((level - 1) // 5) * 70
            btn_rect = pygame.Rect(btn_x, btn_y, 120, 60)
            
            if btn_rect.collidepoint(pos):
                price = self.shop.get_price(level)
                if self.game.tokens >= price:
                    self.game.buy_dinosaur(level, price)
        
        battle_btn = pygame.Rect(SCREEN_WIDTH - 160, 20, 140, 40)
        if battle_btn.collidepoint(pos):
            self.start_battle()
    
    def handle_release(self, pos):
        if self.dragging_dino and self.drag_from_pos:
            player_offset_x = 40
            player_offset_y = 120
            slot = self.game.grid.get_slot_at(pos[0], pos[1], player_offset_x, player_offset_y)
            if slot:
                from_row, from_col = self.drag_from_pos
                to_row, to_col = slot
                if (from_row, from_col) != (to_row, to_col):
                    self.game.grid.move_dinosaur(from_row, from_col, to_row, to_col)
        
        self.dragging_dino = None
        self.drag_from_pos = None
    
    def start_battle(self):
        self.game.generate_enemy_army(self.game.current_level)
        self.battle = Battle(self.game.grid, self.game.enemy_grid)
        self.game.state = GameState.BATTLE
        self.battle_timer = pygame.time.get_ticks()
    
    def update_battle(self):
        if self.game.state == GameState.BATTLE and self.battle:
            current_time = pygame.time.get_ticks()
            if current_time - self.battle_timer >= self.battle_speed:
                self.battle_timer = current_time
                self.battle.execute_turn()
                
                if self.battle.is_battle_over():
                    winner = self.battle.get_winner()
                    if winner == "player":
                        self.game.tokens += self.game.get_reward()
                        self.game.next_level()
                        self.game.state = GameState.VICTORY
                    else:
                        self.game.state = GameState.DEFEAT
    
    def handle_victory_click(self):
        if self.game.is_game_won():
            self.game.state = GameState.ARMY
        else:
            self.game.state = GameState.ARMY
    
    def handle_defeat_click(self):
        self.game.state = GameState.ARMY
    
    def update(self):
        self.update_battle()
        
        pos = pygame.mouse.get_pos()
        self.hovered_slot = self.game.grid.get_slot_at(pos[0], pos[1])
    
    def draw(self):
        if self.game.state == GameState.ARMY:
            self.renderer.draw_army_view(self.game)
            
            if self.dragging_dino:
                pygame.draw.circle(self.screen, self.dragging_dino.color, 
                                 pygame.mouse.get_pos(), 30)
        
        elif self.game.state == GameState.BATTLE:
            if self.battle:
                self.renderer.draw_battle_view(self.game, self.battle)
        
        elif self.game.state == GameState.VICTORY:
            if self.battle:
                self.renderer.draw_battle_view(self.game, self.battle)
            self.renderer.draw_victory(self.game)
        
        elif self.game.state == GameState.DEFEAT:
            if self.battle:
                self.renderer.draw_battle_view(self.game, self.battle)
            self.renderer.draw_defeat(self.game)
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    app = DinoMergeApp()
    app.run()
