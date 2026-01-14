# game/core.py
import pygame


class Entity(pygame.sprite.DirtySprite):
    """
    Minimal Entity compatible with legacy code.
    Subclass and override render/update as needed.
    """
    def __init__(self, dimensions=(0, 0), layer=0, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.image = pygame.surface.Surface(dimensions).convert()
        self.rect = self.image.get_rect()
        self.groups = pygame.sprite.LayeredDirty()
        self.layer = layer
        self.dirty = 2
        self.blendmode = pygame.BLEND_RGBA_ADD

    def render(self, interval=0, *args, **kwargs):
        # override in subclasses
        pass

    def update(self, *args, **kwargs):
        # override in subclasses
        pass


class EntityGroup(pygame.sprite.LayeredDirty):
    """
    Group of Entities that supports legacy render/update/move semantics.
    Each child is expected to implement render(interval) and update().
    """
    def __init__(self, *args, **kwargs):
        super(EntityGroup, self).__init__(*args, **kwargs)

    def render(self, interval):
        # Call render on each child entity
        for entity in list(self):
            try:
                entity.render(interval)
            except Exception:
                # keep robust: don't break the whole render loop
                pass

    def update(self, *args, **kwargs):
        # Call update on each child entity
        for entity in list(self):
            try:
                entity.update(*args, **kwargs)
            except Exception:
                pass
        # mark group dirty so LayeredDirty will redraw
        try:
            super(EntityGroup, self).update()
        except Exception:
            pass

    def move(self, x, y):
        # Move each child's rect by (x, y)
        for child in list(self):
            try:
                child.rect.move_ip(x, y)
            except Exception:
                pass

    # convenience: clear background and redraw children (used by Engine.render)
    def clear(self, surface, background):
        try:
            surface.blit(background, (0, 0))
        except Exception:
            surface.fill((0, 0, 0))


