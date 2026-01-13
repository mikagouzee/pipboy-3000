class SubBar:
    def __init__(self, screen, get_items, get_selected):
        self.screen = screen
        self.get_items = get_items
        self.get_selected = get_selected
        self.font = load_font(20)

    def render(self):
        items = self.get_items()
        selected = self.get_selected()

        x = 20
        y = 60

        for item in items:
            text = glow_text(item, self.font) if item == selected else glow_text(item, self.font, dim=True)
            rect = text.get_rect(topleft=(x, y))
            self.screen.blit(text, rect)
            x += rect.width + 20

