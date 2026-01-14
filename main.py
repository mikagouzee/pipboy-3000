# main.py
import sys
import pygame
import time

import importlib
import pkgutil
import modules as modules_pkg


from engine import Engine
from module_manager import ModuleManager
from screens.helpers.ui_manager import UIManager
from modules.error import show_error

# Try to import legacy modules (these should exist in your repo)
#try:
#	from pypboy.modules import data as data_mod
#	from pypboy.modules import items as items_mod
#	from pypboy.modules import stats as stats_mod
#except Exception:
#	data_mod = items_mod = stats_mod = None

# Set this to your TFT resolution (override config if needed)
import config
SCREEN_WIDTH = getattr(config, "WIDTH", 480)
SCREEN_HEIGHT = getattr(config, "HEIGHT", 320)

def main():
	pygame.init()
	pygame.font.init()

	# Create engine (this sets up screen and root children)
	engine = Engine("Pip-Boy", SCREEN_WIDTH, SCREEN_HEIGHT)

	# Module manager wraps engine modules
	module_manager = ModuleManager(engine)

	registered = []
	for finder, name, ispkg in pkgutil.iter_modules(modules_pkg.__path__):
		try:
			mod = importlib.import_module(f"modules.{name}")
			if (hasattr(mod, "Module")):
				try:
					instance = mod.Module(engine)
				except TypeError:
					instance = mod.Module()
					try:
						instance.pypboy = engine
					except Exception: pass
				module_manager.register_module(name.upper(), instance)
				registered.append(name.upper())
		except Exception as e:
			print("module import failed:", name, e)

	print("Registered Modules :", registered)
	if not engine.active and registered:
		module_manager.set_active(registered[0])
	# UIManager needs a way to get/set sub selection; we store it on engine for simplicity
	engine.current_sub = None

	def get_sub_selected():
		return getattr(engine, "current_sub", None)

	def set_sub_selected(v):
		engine.current_sub = v

	ui = UIManager(engine.screen, module_manager, get_sub_selected, set_sub_selected)

	clock = pygame.time.Clock()
	running = True
	engine.running = True

	while running and engine.running:
		dt = clock.tick(60) / 1000.0
		try:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					engine.running = False
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					running = False
					engine.running = False

				# route events: engine handles module events; UI handles topbar/subbar taps
				engine.handle_event(event)
				ui.handle_event(event)

			# update active module and engine groups
			engine.update()
			ui.render(dt)
			engine.render()
			# flip already done by engine.render(); ensure display updated
			# pygame.display.flip()  # engine.render already flips
		except Exception as e:
			if getattr(engine, "active", None) and getattr(engine.active, "label", "") == "ERR":
				import traceback; traceback.print_exc()
				pygame.time.wait(200)
			else:
				show_error(engine, e, label="ERR")
				pygame.time.wait(200)
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()
