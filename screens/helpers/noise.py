import pygame, random

def create_noise_surface(width, height, intensity=30):
    """
    Create a static noise overlay.
    - intensity: 0–255 brightness of noise pixels
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pixels = pygame.PixelArray(surface)

    for y in range(height):
        for x in range(width):
            # random brightness for each pixel
            brightness = random.randint(0, intensity)
            pixels[x, y] = (brightness, brightness, brightness, 40)

    del pixels
    return surface

