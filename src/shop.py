from src.constants import PRICES, DINOSAURS


class Shop:
    def __init__(self):
        self.prices = PRICES.copy()
    
    def get_price(self, level: int) -> int:
        return self.prices.get(level, 0)
    
    def get_dinosaur_info(self, level: int) -> dict:
        return DINOSAURS.get(level, {})
    
    def can_afford(self, tokens: int, level: int) -> bool:
        return tokens >= self.get_price(level)
