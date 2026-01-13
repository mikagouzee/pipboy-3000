class LeftList:
    def __init__(self, screen, get_items, get_selected):
        self.screen = screen
        self.get_items = get_items
        self.get_selected = get_selected
        self.font = load_font(20)

    def render(self):
        items = self.get_items()
        selected = self.get_selected()

        x = 20
        y = 100

        for item in items:
            text = glow_text(item, self.font) if item == selected else glow_text(item, self.font, dim=True)
            self.screen.blit(text, (x, y))
            y += 28

class RightPanel:
    def __init__(self, screen, get_selected_item):
        self.screen = screen
        self.get_selected_item = get_selected_item
        self.font = load_font(20)

    def render(self):
        w, h = self.screen.get_size()
        x = w // 2 + 10
        y = 100

        item = self.get_selected_item()
        if not item:
            return

        # Example: weapon stats
        for line in item.get_display_lines():
            text = glow_text(line, self.font)
            self.screen.blit(text, (x, y))
            y += 28

