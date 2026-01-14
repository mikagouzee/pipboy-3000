# engine.py
import time
import pygame
import config

# Try to import GPIO if available
try:
    if getattr(config, "GPIO_AVAILABLE", False):
        import RPi.GPIO as GPIO
    else:
        GPIO = None
except Exception:
    GPIO = None

# Import EntityGroup from game/core primitives
from core import EntityGroup

class Engine(object):
    """
    Single authoritative Engine for the project.
    - Uses game.core.EntityGroup for root_children
    - Manages module registration and active module switching
    - Handles GPIO actions and keyboard action mapping
    - Exposes run_once(dt) for integration with external loops
    """
    EVENTS_UPDATE = pygame.USEREVENT + 1
    EVENTS_RENDER = pygame.USEREVENT + 2

    def __init__(self, title, width, height, *args, **kwargs):
        super(Engine, self).__init__(*args, **kwargs)
        # Window and screen
        self.window = pygame.display.set_mode((width, height))
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption(title)
        pygame.mouse.set_visible(True)

        # Scene groups
        self.root_children = EntityGroup()
        self.groups = []

        # Background
        self.background = pygame.surface.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))

        # Timing
        self.rescale = False
        self.last_render_time = 0.0

        # Module registry and active module
        self.modules = {}   # label -> module instance
        self.active = None

        # GPIO mapping
        self.gpio_actions = {}
        if getattr(config, "GPIO_AVAILABLE", False) and GPIO:
            self.init_gpio_controls()

        # Running flag for legacy run()
        self.running = False

    # --- basic group management (same semantics as legacy)
    def add(self, group):
        if group not in self.groups:
            self.groups.append(group)

    def remove(self, group):
        if group in self.groups:
            self.groups.remove(group)

    # --- render/update primitives (compatible with legacy)
    def render(self):
        if self.last_render_time == 0:
            self.last_render_time = time.time()
            return 0.0
        interval = time.time() - self.last_render_time
        self.last_render_time = time.time()

        # clear and render root children
        try:
            self.root_children.clear(self.screen, self.background)
            self.root_children.render(interval)
            self.root_children.draw(self.screen)
        except Exception:
            pass

        # render other groups
        for group in list(self.groups):
            try:
                group.render(interval)
                group.draw(self.screen)
            except Exception:
                pass

        pygame.display.flip()
        return interval

    def update(self):
        try:
            self.root_children.update()
        except Exception:
            pass
        for group in list(self.groups):
            try:
                group.update()
            except Exception:
                pass

    # --- GPIO helpers
    def init_gpio_controls(self):
        for pin in config.GPIO_ACTIONS.keys():
            try:
                GPIO.setup(pin, GPIO.IN)
                self.gpio_actions[pin] = config.GPIO_ACTIONS[pin]
            except Exception:
                pass

    def check_gpio_input(self):
        if not getattr(config, "GPIO_AVAILABLE", False) or not GPIO:
            return
        for pin in list(self.gpio_actions.keys()):
            try:
                if not GPIO.input(pin):
                    self.handle_action(self.gpio_actions[pin])
            except Exception:
                pass

    # --- module management (single place to register and switch)
    def register_module(self, label, module_instance):
        label = label.upper()
        self.modules[label] = module_instance
        # position modules like legacy code expects
        try:
            module_instance.move(4, 40)
        except Exception:
            pass
        # allow modules to reference engine if they expect pypboy/engine
        try:
            setattr(module_instance, "pypboy", self)
        except Exception:
            pass

    def set_active_module(self, label):
        if not label:
            return
        label = label.upper()
        if label not in self.modules:
            return
        # pause and remove previous active
        if hasattr(self, "active") and self.active:
            try:
                self.active.handle_action("pause")
                self.remove(self.active)
            except Exception:
                pass
        # set new active
        self.active = self.modules[label]
        self.active.parent = self
        try:
            self.active.handle_action("resume")
        except Exception:
            pass
        self.add(self.active)

    def handle_action(self, action):
        # module_ prefix switches modules
        if action.startswith("module_"):
            self.set_active_module(action[7:])
        else:
            if hasattr(self, "active") and self.active:
                self.active.handle_action(action)

    # --- event handling (keyboard, quit, song end, delegate to active)
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            else:
                if event.key in getattr(config, "ACTIONS", {}):
                    self.handle_action(config.ACTIONS[event.key])
        elif event.type == pygame.QUIT:
            self.running = False
        elif event.type == config.EVENTS.get('SONG_END', None):
            if hasattr(config, 'radio'):
                try:
                    config.radio.handle_event(event)
                except Exception:
                    pass
        else:
            if hasattr(self, "active") and self.active:
                self.active.handle_event(event)

    # --- single-step integration
    def run_once(self, dt):
        # update active module first
        if hasattr(self, "active") and self.active:
            try:
                self.active.update(dt)
            except Exception:
                pass
        # update engine groups
        self.update()
        # render engine and return interval
        interval = self.render()
        # check gpio
        self.check_gpio_input()
        return interval

    # --- legacy run loop kept for compatibility
    def run(self, fps=60):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            dt = clock.tick(fps) / 1000.0
            self.run_once(dt)
            pygame.time.wait(10)

