from dino_runner.components.power_ups.power_ups import PowerUp
from dino_runner.utils.constants import HEART_PLUS, HEART_TYPE

class Heart(PowerUp):
    def __init__(self):
        self.image = HEART_PLUS
        self.type = HEART_TYPE
        super().__init__(self.image, self.type)