class ScreenManager:
	def __init__(self):
		self.screens = {}
		self.current = None

	def register(self, name, screen):
		self.screens[name] = screen
		if self.current is None:
			self.current = name

	def set(self, name):
		if name in self.screens:
			self.current = name

	def handle_event(self, event):
		if self.current:
			self.screens[self.current].handle_event(event)

	def update(self, dt):
		if self.current:
			self.screens[self.current].update(dt)

	def render(self):
		if self.current:
			self.screens[self.current].render()

