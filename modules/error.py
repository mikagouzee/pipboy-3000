# modules/error_module.py
import pygame
import traceback
import os
from core import Entity, EntityGroup
import config

ASSET_PIPBOY = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "images", "vault-error.png"))

class ErrorEntity(Entity):
	def __init__(self, message, size=(config.WIDTH, config.HEIGHT)):
		super(ErrorEntity, self).__init__(dimensions=size)
		self.message = message or "Unknown error"
		self._prepare_image()

	def _prepare_image(self):
		# Clear
		self.image.fill((0, 0, 0))
		w, h = self.image.get_size()

		# Load pipboy image (fallback to a simple circle)
		pip = None
		try:
			pip = pygame.image.load(ASSET_PIPBOY).convert_alpha()
		except Exception:
			pip = pygame.Surface((160, 160), pygame.SRCALPHA)
			pygame.draw.circle(pip, (80, 200, 80), (80, 80), 80)

		# Scale and blit pipboy on left
		pip_w = min(160, int(w * 0.35))
		pip_h = int(pip_w * pip.get_height() / max(1, pip.get_width()))
		pip = pygame.transform.smoothscale(pip, (pip_w, pip_h))
		pip_x = 20
		pip_y = (h - pip_h) // 2
		self.image.blit(pip, (pip_x, pip_y))

		# Draw text on right
		try:
			title_font = config.FONTS.get(22) or pygame.font.Font(None, 22)
			body_font = config.FONTS.get(16) or pygame.font.Font(None, 16)
		except Exception:
			title_font = pygame.font.Font(None, 22)
			body_font = pygame.font.Font(None, 16)

		# Title
		title = "Oops :"
		title_surf = title_font.render(title, True, (105, 251, 187))
		self.image.blit(title_surf, (pip_x + pip_w + 20, pip_y + 10))

		# Message (wrap)
		msg = str(self.message)
		max_width = w - (pip_x + pip_w + 40)
		y = pip_y + 40
		words = msg.split()
		line = ""
		for word in words:
			test = (line + " " + word).strip()
			ts = body_font.render(test, True, (180, 255, 200))
			if ts.get_width() > max_width and line:
				self.image.blit(body_font.render(line, True, (180, 255, 200)), (pip_x + pip_w + 20, y))
				y += ts.get_height() + 6
				line = word
			else:
				line = test
		if line:
			self.image.blit(body_font.render(line, True, (180, 255, 200)), (pip_x + pip_w + 20, y))
			y += body_font.get_height() + 6

		# Footer apology
		footer = "Apologies from VaultTec"
		footer_surf = body_font.render(footer, True, (105, 251, 187))
		self.image.blit(footer_surf, (pip_x + pip_w + 20, h - footer_surf.get_height() - 20))

	def render(self, interval=0, *args, **kwargs):
		# nothing dynamic for now; image already prepared
		pass

class Module(EntityGroup):
	"""
	Simple error module compatible with engine.register_module / set_active_module.
	Usage: module_manager.register_module("ERR", Module(engine, message="..."))
	"""
	label = "ERROR"

	def __init__(self, engine=None, message=None):
		super(Module, self).__init__()
		self.engine = engine
		self.message = message or "Unknown error"
		self.entity = ErrorEntity(self.message, size=(config.WIDTH, config.HEIGHT))
		self.add(self.entity)

		# minimal footer so UIManager can read footer.menu if needed
		try:
			import pypboy
			self.footer = pypboy.ui.Footer()
			self.footer.menu = []
			self.footer.selected = None
			self.footer.position = (0, config.HEIGHT - 53)
			self.add(self.footer)
		except Exception:
			self.footer = None

	def move(self, x, y):
		# keep API compatible
		for child in list(self):
			try:
				child.rect.move_ip(x, y)
			except Exception:
				pass

	def handle_action(self, action, value=0):
		# support pause/resume
		if action == "pause":
			self.paused = True
		elif action == "resume":
			self.paused = False

	def handle_event(self, event):
		# allow ESC to quit app
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			try:
				self.engine.running = False
			except Exception:
				pass

	def update(self, dt=0):
		pass

# helper to register and show error quickly
def show_error(engine, exc, label="ERROR"):
	"""
	Register and activate an error module on the engine.
	exc can be an Exception or a string.
	"""
	msg = exc if isinstance(exc, str) else "{}: {}".format(exc.__class__.__name__, str(exc))
	existing = engine.modules.get(label)
	if existing:
		try:
			existing.message = msg
			if hasattr(existing, "entity"):
				existing.entity.message = msg
				existing.entity._prepare_image()
		except Exception:
			pass
		engine.set_active_module(label)
		return existing

	# create instance and register
	mod = Module(engine, message=msg)
	engine.register_module(label, mod)
	engine.set_active_module(label)
	# also print traceback to console for debugging
	try:
		traceback.print_exc()
	except Exception:
		pass
	return mod
