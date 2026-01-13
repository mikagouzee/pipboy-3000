import sys
import pygame
import math

from screen_manager import ScreenManager
from screens.main_menu import MainMenu
from screens.stats import StatsScreen
from screens.items_menu import ItemsMenu
from screens.items_lists import create_item_screens

from screens.data_menu import DataMenu
from screens.data_map import MapScreen
from screens.data_misc import MiscScreen
from screens.data_quests import QuestsScreen
from screens.data_radio import RadioScreen

from screens.helpers.crt import create_scanlines
from screens.helpers.noise import  create_noise_surface
from screens.helpers.touch import TouchArea

from screens.helpers.ui_manager import UIManager

# Set this to your TFT resolution
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

def main():
	pygame.init()
	pygame.font.init()

	# Fullscreen on Pi: use FULLSCREEN flag; we’ll refine for TFT later
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
	pygame.display.set_caption("Pip-Boy")

	clock = pygame.time.Clock()
	running = True

	manager = ScreenManager()
	manager.register("menu", MainMenu(screen, manager))
	manager.register("stats", StatsScreen(screen, manager))
	manager.register("items", ItemsMenu(screen, manager))

	item_screens = create_item_screens(screen, manager)
	for name, scr in item_screens.items():
		manager.register(name, scr)

	manager.register("data", DataMenu(screen, manager))
	manager.register("data_map", MapScreen(screen, manager))
	manager.register("data_misc", MiscScreen(screen, manager))
	manager.register("data_quests", QuestsScreen(screen, manager))
	manager.register("data_radio", RadioScreen(screen, manager))

	manager.set("menu")

	manager.current_main = "MENU"
	manager.current_sub = None


	def get_main_selected():
		return getattr(manager, "current_main", "MENU").upper()

	def get_sub_selected():
		return getattr(manager, "current_sub", None)

	def set_sub_selected(v):
		manager.current_sub = v


	ui = UIManager(screen, get_main_selected, get_sub_selected, set_sub_selected)



	while running:
		dt = clock.tick(60) / 1000.0  # seconds

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					running = False

			manager.handle_event(event)
			ui.handle_event(event)

		manager.update(dt)
		manager.render()

		if hasattr(manager.current, "buttons"):
			for btn in manager.current.buttons:
				btn.update(dt)
				btn.draw_pulse(screen)

		if hasattr(manager.current, "back_button"):
			manager.current.back_button.update(dt)
			manager.current.back_button.draw_pulse(screen)

		ui.render(dt)
		pygame.display.flip()

	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()

