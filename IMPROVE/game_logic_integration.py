import pygame
from fishing_challenge import FishingSkillChallenge
from map_explore import MapExplorer
from fishing_system import FishingSystem  # Untuk hook utama (jika tetap digunakan)
from inventory import Inventory
from fish import Fish
from game_map import GameMap
from ui import UI
from config import Config

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "explore"
        self.wallet = 0

        self.inventory = Inventory()
        self.map = GameMap("Coast")
        self.ui = UI(self)
        self.map_explorer = MapExplorer()
        self.fishing_minigame = None
        self.active_location = None

        self.sound_success = pygame.mixer.Sound("assets/sounds/catch.wav")
        self.sound_fail = pygame.mixer.Sound("assets/sounds/fail.wav")

    def set_state(self, state):
        self.state = state

    def handle_event(self, event):
        if self.state == "explore":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                location = self.map_explorer.get_selected_location()
                if location:
                    self.active_location = location
                    self.fishing_minigame = FishingSkillChallenge()
                    self.fishing_minigame.start()
                    self.set_state("minigame")

        elif self.state == "minigame":
            self.fishing_minigame.update_events(event)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if self.state == "explore":
            self.map_explorer.update(dt, keys)

        elif self.state == "minigame":
            self.fishing_minigame.update()
            if self.fishing_minigame.is_done():
                result = self.fishing_minigame.result
                if result == "caught":
                    fish_data = GameMap(self.active_location).get_random_fish()
                    new_fish = Fish(fish_data, (100, 100))
                    self.inventory.add(new_fish)
                    self.wallet += new_fish.value
                    self.sound_success.play()
                else:
                    self.sound_fail.play()
                self.set_state("explore")

    def render(self):
        if self.state == "explore":
            self.map_explorer.render(self.screen)
            self.ui.render(self.screen)

        elif self.state == "minigame":
            self.screen.fill((0, 0, 30))
            self.fishing_minigame.render(self.screen)
            self.ui.render(self.screen)

        pygame.display.flip()
