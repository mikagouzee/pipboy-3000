# modules/items_module.py
from modules.base import BaseModule

# Example adapter: wrap your existing item screens or create small submodule classes.
# SimpleSub is a tiny adapter: it calls existing screen renderers. 
# Replace engine.screen_manager.render_named(...) with whatever method you use to render a named screen, 
# or adapt to call the screen instance directly.
#This lets you keep existing screen code while exposing a module/submodule API.

class SimpleSub(object):
    def __init__(self, engine, render_fn, update_fn=None, handle_fn=None, on_activate=None):
        self.engine = engine
        self._render = render_fn
        self._update = update_fn or (lambda dt: None)
        self._handle = handle_fn or (lambda e: None)
        self.on_activate = on_activate or (lambda: None)

    def render(self, surface):
        self._render(surface)

    def update(self, dt):
        self._update(dt)

    def handle_event(self, event):
        self._handle(event)

class ItemsModule(BaseModule):
    label = "INV"

    def __init__(self, engine):
        super().__init__(engine)
        # Create submodules by wrapping existing screen renderers or functions.
        # Replace the lambdas below with calls to your existing screen objects.
        self.submodules = {
            "WEAPONS": SimpleSub(engine,
                                 render_fn=lambda s: engine.screen_manager.render_named("inv_weapons", s),
                                 update_fn=lambda dt: None,
                                 handle_fn=lambda e: None),
            "APPAREL": SimpleSub(engine,
                                 render_fn=lambda s: engine.screen_manager.render_named("inv_apparel", s)),
            "AID": SimpleSub(engine,
                             render_fn=lambda s: engine.screen_manager.render_named("inv_aid", s)),
        }
        self.activate(None)

