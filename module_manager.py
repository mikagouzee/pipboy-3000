# module_manager.py
"""
Thin adapter around Engine module registration and switching.
Place this file in the project root next to main.py.
"""
class ModuleManager:
    def __init__(self, engine):
        self.engine = engine

    def register_module(self, label, module_instance):
        """Register a module instance (module_instance should be a BaseModule/SubModule style)."""
        self.engine.register_module(label, module_instance)

    def set_active(self, label):
        self.engine.set_active_module(label)

    def get_active_label(self):
        return self.engine.active.label if getattr(self.engine, "active", None) else None

    def get_modules(self):
        return list(self.engine.modules.keys())

    def get_active_module(self):
        return getattr(self.engine, "active", None)

    def update(self, dt):
        # delegate to engine single-step
        self.engine.run_once(dt)

    def handle_event(self, event):
        self.engine.handle_event(event)

