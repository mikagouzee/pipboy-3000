from .list_screen import ListScreen

def create_item_screens(screen, manager):
	return {
		"items_aid": ListScreen(screen, manager, "AID", [
			"Stimpak",
			"RadAway",
			"Med-X",
			"Buffout"
		]),
		"items_ammo": ListScreen(screen, manager, "AMMO", [
			"10mm Rounds",
			"5.56mm Rounds",
			"Fusion Cells"
		]),
		"items_apparel": ListScreen(screen, manager, "APPAREL", [
			"Vault Suit",
			"Leather Armor",
			"Combat Armor"
		]),
		"items_misc": ListScreen(screen, manager, "MISC", [
			"Pre-War Money",
			"Gold Watch",
			"Dog Tags"
		]),
		"items_weapons": ListScreen(screen, manager, "WEAPONS", [
			"10mm Pistol",
			"Laser Rifle",
			"Baseball Bat"
		])
	}

