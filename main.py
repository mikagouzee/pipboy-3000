# main.py
import sys
import pygame
import time

from engine import Engine
from module_manager import ModuleManager
from screens.helpers.ui_manager import UIManager

# Try to import legacy modules (these should exist in your repo)
try:
    from pypboy.modules import data as data_mod
    from pypboy.modules import items as items_mod
    from pypboy.modules import stats as stats_mod
except Exception:
    data_mod = items_mod = stats_mod = None

# Set this to your TFT resolution (override config if needed)
import config
SCREEN_WIDTH = getattr(config, "WIDTH", 480)
SCREEN_HEIGHT = getattr(config, "HEIGHT", 320)

def main():
    pygame.init()
    pygame.font.init()

    # Create engine (this sets up screen and root children)
    engine = Engine("Pip-Boy", SCREEN_WIDTH, SCREEN_HEIGHT)

    # If pypboy UI helpers exist, add header/scanlines like legacy init_children
    try:
        import pypboy
        # header and scanlines are added by legacy pypboy init; if not present, skip
        engine.root_children.add(pypboy.ui.Header())
        engine.root_children.add(pypboy.ui.Scanlines(SCREEN_WIDTH, SCREEN_HEIGHT, 3, 1, [(0,13,3,50)]))
    except Exception:
        pass

    # Module manager wraps engine modules
    module_manager = ModuleManager(engine)

    # Register legacy modules if available (they expect engine/pypboy instance as parent)
    # These Module classes typically accept the engine/pypboy instance in their constructor.
    if stats_mod:
        try:
            module_manager.register_module("STAT", stats_mod.Module(engine))
        except Exception:
            pass
    if items_mod:
        try:
            module_manager.register_module("INV", items_mod.Module(engine))
        except Exception:
            pass
    if data_mod:
        try:
            module_manager.register_module("DATA", data_mod.Module(engine))
        except Exception:
            pass

    # Set a sensible default active module
    module_manager.set_active("STAT" if "STAT" in engine.modules else next(iter(engine.modules.keys()), None))

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
        # engine.run_once will call active.update and engine.update/render
        engine.run_once(dt)

        # draw pulses for any TouchAreas that rely on screen-level pulses (if used)
        # (TouchArea.draw_pulse overlays full-screen tint; we call it from screens if needed)

        # render UI chrome on top of engine content
        ui.render(dt)

        # flip already done by engine.render(); ensure display updated
        # pygame.display.flip()  # engine.render already flips

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

