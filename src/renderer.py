import pygame
from src.constants import *
from src.grid import Grid
from src.dinosaur import Dinosaur
from src.game_state import DinoMergeGame, GameState
from src.battle import Battle
from src.shop import Shop


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.shop = Shop()
        self.selected_shop_level = None
    
    def draw_background(self):
        self.screen.fill(COLORS['background'])
    
    def draw_grid(self, grid: Grid, offset_x: int, offset_y: int, is_enemy: bool = False):
        for row in range(grid.height):
            for col in range(grid.width):
                x = offset_x + col * SLOT_SIZE
                y = offset_y + row * SLOT_SIZE
                
                if is_enemy:
                    if col < FRONT_LINE_COLS:
                        slot_color = COLORS['front_line']
                    else:
                        slot_color = COLORS['back_line']
                else:
                    if col >= GRID_WIDTH - FRONT_LINE_COLS:
                        slot_color = COLORS['front_line']
                    else:
                        slot_color = COLORS['back_line']
                
                pygame.draw.rect(self.screen, slot_color, 
                               (x, y, SLOT_SIZE, SLOT_SIZE), 2)
                
                dino = grid.get_dinosaur_at(row, col)
                if dino:
                    self.draw_dinosaur(dino, x + SLOT_SIZE // 2, y + SLOT_SIZE // 2, is_enemy)
    
    def draw_dinosaur(self, dino: Dinosaur, center_x: int, center_y: int, is_enemy: bool = False, scale: float = 1.0):
        size = int(30 * scale)
        
        color = dino.color
        if not dino.alive:
            color = (80, 80, 80)
        
        shape = dino.shape
        
        if shape == 'triangle_small':
            points = [
                (center_x, center_y - size),
                (center_x - size, center_y + size),
                (center_x + size, center_y + size),
            ]
        elif shape == 'triangle':
            points = [
                (center_x, center_y - size),
                (center_x - size - 5, center_y + size),
                (center_x + size + 5, center_y + size),
            ]
        elif shape == 'triangle_large':
            points = [
                (center_x, center_y - size - 10),
                (center_x - size - 10, center_y + size),
                (center_x + size + 10, center_y + size),
            ]
        elif shape == 'rectangle':
            rect = pygame.Rect(center_x - size, center_y - size // 2, size * 2, size)
            pygame.draw.rect(self.screen, color, rect)
            return
        elif shape == 'rectangle_large':
            rect = pygame.Rect(center_x - size - 5, center_y - size // 2 - 5, size * 2 + 10, size + 10)
            pygame.draw.rect(self.screen, color, rect)
            return
        elif shape == 'rectangle_long':
            rect = pygame.Rect(center_x - size - 10, center_y - size // 3, size * 2 + 20, size * 2 // 3)
            pygame.draw.rect(self.screen, color, rect)
            return
        elif shape == 'diamond':
            points = [
                (center_x, center_y - size),
                (center_x + size, center_y),
                (center_x, center_y + size),
                (center_x - size, center_y),
            ]
        else:
            points = [
                (center_x, center_y - size),
                (center_x - size, center_y + size),
                (center_x + size, center_y + size),
            ]
        
        pygame.draw.polygon(self.screen, color, points)
        
        if is_enemy:
            pygame.draw.polygon(self.screen, (255, 100, 100), points, 3)
        else:
            pygame.draw.polygon(self.screen, (100, 255, 100), points, 2)
        
        level_text = self.font_small.render(str(dino.level), True, (255, 255, 255))
        text_rect = level_text.get_rect(center=(center_x, center_y + size + 15))
        self.screen.blit(level_text, text_rect)
        
        if dino.alive:
            hp_percent = dino.current_hp / dino.max_hp
            hp_bar_width = int(size * 1.5)
            hp_bar_height = 4
            hp_bar_x = center_x - hp_bar_width // 2
            hp_bar_y = center_y - size - 10
            
            pygame.draw.rect(self.screen, (100, 0, 0), 
                           (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
            pygame.draw.rect(self.screen, (0, 200, 0), 
                           (hp_bar_x, hp_bar_y, int(hp_bar_width * hp_percent), hp_bar_height))
    
    def draw_ui_header(self, game: DinoMergeGame):
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, COLORS['ui_panel'], header_rect)
        
        level_text = self.font_medium.render(f"Level: {game.current_level}", True, COLORS['text'])
        self.screen.blit(level_text, (20, 25))
        
        tokens_text = self.font_medium.render(f"Tokens: {game.tokens}", True, COLORS['text'])
        tokens_rect = tokens_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(tokens_text, tokens_rect)
        
        self.draw_button(SCREEN_WIDTH - 160, 20, 140, 40, "BATTLE", 
                        game.grid.count_empty_slots() < 40, lambda: None)
    
    def draw_button(self, x: int, y: int, width: int, height: int, text: str, 
                   enabled: bool = True, callback=None) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        
        button_rect = pygame.Rect(x, y, width, height)
        is_hovered = button_rect.collidepoint(mouse_pos) and enabled
        
        if enabled:
            color = COLORS['button_hover'] if is_hovered else COLORS['button']
        else:
            color = COLORS['button_disabled']
        
        pygame.draw.rect(self.screen, color, button_rect, border_radius=5)
        pygame.draw.rect(self.screen, COLORS['text'], button_rect, 2, border_radius=5)
        
        text_surf = self.font_small.render(text, True, COLORS['text'])
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surf, text_rect)
        
        return is_hovered and enabled
    
    def draw_army_view(self, game: DinoMergeGame):
        self.draw_background()
        
        self.draw_ui_header(game)
        
        player_offset_x = 40
        enemy_offset_x = SCREEN_WIDTH // 2 + 20
        
        player_label = self.font_medium.render("Your Army", True, (100, 200, 100))
        self.screen.blit(player_label, (player_offset_x, 85))
        
        enemy_label = self.font_medium.render("Enemy (Next Battle)", True, (200, 100, 100))
        self.screen.blit(enemy_label, (enemy_offset_x, 85))
        
        if not game.enemy_grid.get_all_dinosaurs():
            game.generate_enemy_army(game.current_level)
        
        self.draw_grid(game.grid, player_offset_x, 120, is_enemy=False)
        self.draw_grid(game.enemy_grid, enemy_offset_x, 120, is_enemy=True)
        
        front_label_player = self.font_small.render("← Front", True, COLORS['text_dark'])
        front_label_enemy = self.font_small.render("Front →", True, COLORS['text_dark'])
        self.screen.blit(front_label_player, (player_offset_x + GRID_WIDTH * SLOT_SIZE - 60, 120 - 20))
        self.screen.blit(front_label_enemy, (enemy_offset_x + 5, 120 - 20))
        
        shop_x = 40
        shop_y = 120 + GRID_HEIGHT * SLOT_SIZE + 30
        shop_title = self.font_medium.render("Shop", True, COLORS['text'])
        self.screen.blit(shop_title, (shop_x, shop_y))
        
        shop_x += 10
        shop_y += 35
        
        for level in range(1, 11):
            price = self.shop.get_price(level)
            info = self.shop.get_dinosaur_info(level)
            can_buy = game.tokens >= price and game.grid.count_empty_slots() > 0
            
            btn_x = shop_x + ((level - 1) % 5) * 130
            btn_y = shop_y + ((level - 1) // 5) * 70
            
            btn_rect = pygame.Rect(btn_x, btn_y, 120, 60)
            is_hovered = btn_rect.collidepoint(pygame.mouse.get_pos()) and can_buy
            
            if can_buy:
                color = COLORS['button_hover'] if is_hovered else COLORS['button']
            else:
                color = COLORS['button_disabled']
            
            pygame.draw.rect(self.screen, color, btn_rect, border_radius=5)
            pygame.draw.rect(self.screen, COLORS['text'], btn_rect, 2, border_radius=5)
            
            name_text = self.font_small.render(f"Lv{level}", True, COLORS['text'])
            self.screen.blit(name_text, (btn_x + 5, btn_y + 5))
            
            price_text = self.font_small.render(f"{price}", True, COLORS['text'])
            self.screen.blit(price_text, (btn_x + 5, btn_y + 22))
            
            hp_text = self.font_small.render(f"HP:{info.get('hp', 0)}", True, COLORS['text_dark'])
            self.screen.blit(hp_text, (btn_x + 5, btn_y + 40))
    
    def draw_battle_view(self, game: DinoMergeGame, battle: Battle):
        self.draw_background()
        
        title_text = self.font_large.render(f"Battle - Level {game.current_level}", True, COLORS['text'])
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
        
        player_offset_x = 40
        enemy_offset_x = SCREEN_WIDTH // 2 + 20
        
        player_label = self.font_medium.render("Your Army", True, (100, 200, 100))
        self.screen.blit(player_label, (player_offset_x, 85))
        
        enemy_label = self.font_medium.render("Enemy Army", True, (200, 100, 100))
        self.screen.blit(enemy_label, (enemy_offset_x, 85))
        
        self.draw_grid(game.grid, player_offset_x, 120, is_enemy=False)
        self.draw_grid(game.enemy_grid, enemy_offset_x, 120, is_enemy=True)
        
        if battle.last_attack:
            attack_text = self.font_medium.render(
                f"{battle.last_attack['attacker'].name} attacks {battle.last_attack['target'].name} for {int(battle.last_attack['damage'])}!",
                True, COLORS['highlight']
            )
            self.screen.blit(attack_text, (SCREEN_WIDTH // 2 - attack_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        turn_text = self.font_small.render(f"Turn: {battle.turn_count}", True, COLORS['text_dark'])
        self.screen.blit(turn_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30))
    
    def draw_victory(self, game: DinoMergeGame):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        result_text = self.font_large.render("VICTORY!", True, COLORS['victory'])
        self.screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        reward = game.get_reward()
        reward_text = self.font_medium.render(f"Reward: {reward} tokens", True, COLORS['text'])
        self.screen.blit(reward_text, (SCREEN_WIDTH // 2 - reward_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        
        if game.current_level >= MAX_LEVEL:
            game_won_text = self.font_medium.render("You have beaten all levels!", True, COLORS['highlight'])
            self.screen.blit(game_won_text, (SCREEN_WIDTH // 2 - game_won_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        continue_text = self.font_small.render("Click to continue...", True, COLORS['text_dark'])
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    
    def draw_defeat(self, game: DinoMergeGame):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        result_text = self.font_large.render("DEFEAT", True, COLORS['defeat'])
        self.screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        hint_text = self.font_medium.render("Try reorganizing your army!", True, COLORS['text'])
        self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        
        continue_text = self.font_small.render("Click to try again...", True, COLORS['text_dark'])
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
