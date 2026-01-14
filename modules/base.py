# modules/base.py
class BaseModule(object):
    """
    Minimal module interface:
      - label: short string shown in topbar (e.g., "STAT", "INV")
      - submodules: dict name -> SubModule instance
      - active: currently active submodule instance
    Submodules must implement: render(surface), update(dt), handle_event(event), on_activate() optional.
    """
    label = "UNNAMED"

    def __init__(self, engine):
        self.engine = engine
        self.submodules = {}   # "WEAPONS" -> SubModule instance
        self.active = None

    def sublabels(self):
        """Return list of sublabels for the SubBar (order preserved if dict is ordered)."""
        return list(self.submodules.keys())

    def activate(self, sublabel=None):
        """Activate a submodule by name, or default to first if None."""
        if sublabel and sublabel in self.submodules:
            self.active = self.submodules[sublabel]
        elif not self.active and self.submodules:
            # default to first available
            self.active = next(iter(self.submodules.values()))
        if self.active and hasattr(self.active, "on_activate"):
            self.active.on_activate()

    def update(self, dt):
        if self.active:
            self.active.update(dt)

    def render(self, surface):
        if self.active:
            self.active.render(surface)

    def handle_event(self, event):
        if self.active:
            self.active.handle_event(event)

