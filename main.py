import pygame
import math
import random
import json
import os
import sys

pygame.init()

# ============================================================
# OMEGA MULTIVERSE V8 - STORY EDITION
# ============================================================

WIDTH, HEIGHT = 1280, 800
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OMEGA MULTIVERSE V8 - STORY EDITION")
clock = pygame.time.Clock()

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "omega_save.json")

# ============================================================
# COLORS
# ============================================================

BLACK = (4, 6, 9)
BG = (8, 13, 19)
PANEL = (13, 21, 29)
PANEL2 = (22, 32, 41)
PANEL3 = (30, 42, 52)
WHITE = (235, 245, 250)
GRAY = (125, 140, 150)
DARK = (30, 36, 42)
GREEN = (50, 255, 150)
CYAN = (40, 220, 255)
BLUE = (70, 120, 255)
PURPLE = (180, 70, 255)
ORANGE = (255, 145, 45)
RED = (255, 65, 75)
YELLOW = (255, 225, 70)
PINK = (255, 80, 180)
ICE = (130, 230, 255)
TOXIC = (120, 255, 70)

# ============================================================
# FONTS
# ============================================================

FONT_HUGE = pygame.font.SysFont("arial", 50, bold=True)
FONT_BIG = pygame.font.SysFont("arial", 38, bold=True)
FONT_MED = pygame.font.SysFont("arial", 25, bold=True)
FONT = pygame.font.SysFont("arial", 18)
FONT_SMALL = pygame.font.SysFont("arial", 14)

# ============================================================
# WORLD DEFINITIONS
# ============================================================

WORLD_DEFS = [
    {
        "name": "EARTH C-137", "subtitle": "STABLE DIMENSION", "color": GREEN,
        "enemies": ["STALKER", "HUNTER"], "reward": 35, "danger": 1.0,
    },
    {
        "name": "ALIEN WORLD", "subtitle": "UNSTABLE BIO-ZONE", "color": PURPLE,
        "enemies": ["SPITTER", "HUNTER"], "reward": 55, "danger": 1.2,
    },
    {
        "name": "TOXIC SWAMP", "subtitle": "CORRUPTED BIOSPHERE", "color": TOXIC,
        "enemies": ["SPITTER", "SWARM", "TANK"], "reward": 75, "danger": 1.45,
    },
    {
        "name": "NEON CITY", "subtitle": "CYBER DIMENSION", "color": PINK,
        "enemies": ["HUNTER", "SWARM", "PHANTOM"], "reward": 100, "danger": 1.7,
    },
    {
        "name": "VOID DIMENSION", "subtitle": "REALITY COLLAPSE", "color": PURPLE,
        "enemies": ["PHANTOM", "VOID"], "reward": 135, "danger": 2.0,
    },
    {
        "name": "FROZEN CORE", "subtitle": "CRYOGENIC WORLD", "color": ICE,
        "enemies": ["TANK", "PHANTOM", "FROST"], "reward": 170, "danger": 2.3,
    },
    {
        "name": "OMEGA DIMENSION", "subtitle": "FORBIDDEN REALITY", "color": ORANGE,
        "enemies": ["OMEGA"], "reward": 300, "danger": 3.0,
    },
    {
        "name": "404 DIMENSION", "subtitle": "DELETED REALITY", "color": CYAN,
        "enemies": ["GLITCH", "PHANTOM"], "reward": 250, "danger": 2.7,
        "secret": True, "unlock": "kills", "unlock_value": 15,
    },
    {
        "name": "BACKROOMS", "subtitle": "DO NOT LOOK BEHIND YOU", "color": YELLOW,
        "enemies": ["HUNTER", "GLITCH"], "reward": 300, "danger": 3.1,
        "secret": True, "unlock": "dimensions", "unlock_value": 5,
    },
    {
        "name": "CORRUPTED OMEGA", "subtitle": "SAVE DATA COLLAPSE", "color": RED,
        "enemies": ["VOID", "OMEGA", "GLITCH"], "reward": 450, "danger": 3.8,
        "secret": True, "unlock": "bosses", "unlock_value": 1,
    },
    {
        "name": "RICK'S GARAGE", "subtitle": "UNKNOWN ORIGIN", "color": YELLOW,
        "enemies": ["GLITCH", "HUNTER"], "reward": 600, "danger": 2.2,
        "secret": True, "unlock": "artifacts", "unlock_value": 3,
    },
]

BOSS_DEFS = {
    3: ("NEON OVERLORD", PINK, 1800, 24),
    4: ("VOID KING", PURPLE, 2200, 28),
    5: ("FROST COLOSSUS", ICE, 2600, 31),
    6: ("OMEGA TITAN", ORANGE, 3400, 35),
    9: ("CORRUPTED OMEGA", RED, 4200, 42),
}

# ============================================================
# WEAPONS
# ============================================================

WEAPONS = {
    "BLASTER": {"damage": 16, "speed": 12, "cooldown": 0.20, "price": 0, "color": CYAN},
    "PLASMA": {"damage": 30, "speed": 14, "cooldown": 0.32, "price": 120, "color": GREEN},
    "VOID": {"damage": 47, "speed": 16, "cooldown": 0.48, "price": 250, "color": PURPLE},
    "OMEGA": {"damage": 75, "speed": 18, "cooldown": 0.70, "price": 500, "color": ORANGE},
}

GUN_MODES = [
    "BLASTER",
    "GRAVITY",
    "SHOCKWAVE",
    "TIME SHOT",
    "BLACK HOLE",
]

# ============================================================
# CHARACTER SYSTEM
# ============================================================

CHARACTERS = {
    "EVIL MORTY": {
        "color": GREEN, "secondary": YELLOW,
        "passive": "CONTROL LINK",
        "z": "PORTAL SNARE", "x": "MIND SPIKE",
        "ultimate": "EVIL PROTOCOL",
        "description": "Pułapki portalowe, hackowanie wrogów i kontrola pola walki.",
        "role": "CONTROL",
    },
    "RICK PRIME": {
        "color": PINK, "secondary": PURPLE,
        "passive": "PRIME REACTOR",
        "z": "OMEGA BOMB", "x": "PRIME RIFT",
        "ultimate": "PRIME COLLAPSE",
        "description": "Eksplozywny burst, szczeliny wymiarowe i ogromne eksplozje.",
        "role": "BURST",
    },
    "RICK": {
        "color": CYAN, "secondary": BLUE,
        "passive": "GADGET MASTER",
        "z": "FREEZE RAY", "x": "DRONE SWARM",
        "ultimate": "DIMENSION CANNON",
        "description": "Technologia, automatyczne drony i precyzyjna broń wymiarowa.",
        "role": "TECH",
    },
    "SUMMER": {
        "color": PINK, "secondary": YELLOW,
        "passive": "CHAOS RUNNER",
        "z": "PHASE DASH", "x": "HOLO DECOY",
        "ultimate": "CHAOS BARRAGE",
        "description": "Mobilność, wabik holograficzny i bardzo szybki styl gry.",
        "role": "MOBILITY",
    },
    "MORTY": {
        "color": YELLOW, "secondary": GREEN,
        "passive": "LUCKY ANOMALY",
        "z": "PROBABILITY SHOT", "x": "ANOMALY BOX",
        "ultimate": "UNSTABLE DIMENSION",
        "description": "Losowe anomalie, nieprzewidywalne efekty i chaos wymiarowy.",
        "role": "CHAOS",
    },
}

CHARACTER_NAMES = list(CHARACTERS.keys())
CHARACTER_PRICES = {
    "EVIL MORTY": 500,
    "MORTY": 800,
    "SUMMER": 1400,
    "RICK": 2200,
    "RICK PRIME": 5000,
}

def character_profile():
    return CHARACTERS.get(current_character) if current_character else None


def character_color():
    profile = character_profile()
    return profile["color"] if profile else GRAY


def character_display_name():
    return current_character if current_character else "ROOKIE // NO CHARACTER"


# ============================================================
# ENEMY STATS
# ============================================================

ENEMY_STATS = {
    "STALKER": (120, 1.5, 8, 25),
    "HUNTER": (90, 2.3, 7, 23),
    "SPITTER": (180, 1.0, 11, 27),
    "SWARM": (55, 3.2, 5, 17),
    "TANK": (360, 0.65, 18, 34),
    "PHANTOM": (210, 1.7, 14, 28),
    "VOID": (290, 1.35, 16, 30),
    "FROST": (330, 0.9, 17, 30),
    "OMEGA": (900, 0.85, 24, 55),
    "GLITCH": (240, 2.0, 15, 27),
}

# ============================================================
# STATE
# ============================================================

player_x = 640.0
player_y = 420.0
player_speed = 4.5
player_hp = 100
player_max_hp = 100
player_stamina = 100
player_max_stamina = 100
player_energy = 100
player_max_energy = 100
coins = 200
potions = 3
player_level = 1
player_xp = 0
player_xp_needed = 100
skill_points = 0
kills = 0
bosses_defeated = 0
dimensions_visited = set()
portal_shards = 0
omega_cores = 0
artifacts = 0

owned_weapons = ["BLASTER"]
current_weapon = "BLASTER"
weapon_levels = {name: 1 for name in WEAPONS}
last_shot = 0.0
gun_mode_index = 0

current_character = None
owned_characters = []
character_cooldowns = {"Z": 0.0, "X": 0.0, "V": 0.0}
character_timers = {
    "phase": 0.0,
    "lucky": 0.0,
    "prime_invuln": 0.0,
    "evil_protocol": 0.0,
}
turrets = []
ability_fx = []

skills = {
    "VITALITY": 0,
    "ENERGY": 0,
    "DASH": 0,
    "WEAPON": 0,
    "PORTAL": 0,
    "LOOT": 0,
}

current_world = 0
selected_world = 0
mode = "HUB"

portal_active = False
portal_x = 640
portal_y = 300
portal_energy = 100
portal_max_energy = 100
portal_color = GREEN
portal_color_name = "GREEN"
PORTAL_COLORS = {
    "GREEN": GREEN, "CYAN": CYAN, "PURPLE": PURPLE,
    "ORANGE": ORANGE, "PINK": PINK, "ICE": ICE, "YELLOW": YELLOW,
}

# UI overlays
open_menu = None  # inventory / skills / quests / stats / armory / lab / dimensions / npc

# gameplay
bullets = []
enemy_projectiles = []
enemies = []
pickups = []
particles = []
boss = None

enemy_spawn_timer = 0.0
world_kills = 0
world_time = 0.0
last_save = 0.0
save_flash = 0.0
screen_shake = 0.0
damage_flash = 0.0

dash_cooldown = 0.0
time_glitch_timer = 0.0
black_hole_timer = 0.0
random_event_timer = 18.0
random_event_text = ""
random_event_color = CYAN
random_event_display = 0.0

# Chill / lounge / minigames
chill_game = None
chill_game_time = 0.0
chill_score = 0
chill_round = 0
chill_target = {"x": 0, "y": 0, "r": 24}
chill_sequence = []
chill_sequence_index = 0
chill_message = ""
chill_message_timer = 0.0
chill_total_time = 0.0
chill_completed = 0
chill_best = {"TARGETS": 0, "HACK": 0, "HOLO": 0}
chill_lounge_coins_timer = 0.0
chill_holo_phase = 0.0


# ============================================================
# STORY / CUTSCENES / FINALE
# ============================================================

story_chapter = 0
story_intro_seen = False
story_boss_dialogue_seen = False
story_artifact_dialogue_seen = False
story_final_warning_seen = False
story_dialogue_active = False
story_dialogue_index = 0
story_dialogue_speaker = "NEXUS"
story_dialogue_color = GREEN
story_dialogue_lines = []
story_dialogue_title = "TRANSMISSION"
ending_choice_active = False
ending_complete = False
ending_title = ""
ending_body = []


def start_dialogue(lines, speaker="NEXUS", color=GREEN, title="TRANSMISSION"):
    global story_dialogue_active, story_dialogue_index
    global story_dialogue_speaker, story_dialogue_color
    global story_dialogue_lines, story_dialogue_title
    story_dialogue_active = True
    story_dialogue_index = 0
    story_dialogue_speaker = speaker
    story_dialogue_color = color
    story_dialogue_lines = list(lines)
    story_dialogue_title = title


def advance_dialogue():
    global story_dialogue_active, story_dialogue_index
    if not story_dialogue_active:
        return
    story_dialogue_index += 1
    if story_dialogue_index >= len(story_dialogue_lines):
        story_dialogue_active = False
        story_dialogue_index = 0


def story_objective():
    if story_chapter <= 1:
        return "PROLOGUE: Find the first Omega Core."
    if story_chapter == 2:
        return f"CHAPTER I: Recover 3 artifacts.  [{artifacts}/3]"
    if story_chapter == 3:
        return "CHAPTER II: Enter CORRUPTED OMEGA."
    if story_chapter == 4:
        return "CHAPTER III: Defeat the CORRUPTED OMEGA."
    if story_chapter >= 5 and not ending_complete:
        return "FINALE: The Omega Core is yours. Choose its fate."
    return "EPILOGUE: The multiverse is stable... for now."


def start_story_intro():
    global story_chapter, story_intro_seen
    story_intro_seen = True
    story_chapter = max(story_chapter, 1)
    start_dialogue([
        "Wake up. The garage is running on emergency power.",
        "Seven realities were mapped. Eleven were found.",
        "Someone has been opening portals from the other side.",
        "Every broken portal leaves behind an OMEGA CORE.",
        "Collect them. Find out who is rewriting the multiverse.",
        "And whatever you do... do not trust the corrupted signal."
    ], speaker="NEXUS", color=GREEN, title="CHAPTER 0 // THE SIGNAL")


def update_story_state():
    global story_chapter, story_boss_dialogue_seen
    global story_artifact_dialogue_seen, story_final_warning_seen
    global ending_choice_active

    if story_chapter == 1 and bosses_defeated >= 1 and not story_boss_dialogue_seen:
        story_boss_dialogue_seen = True
        story_chapter = 2
        start_dialogue([
            "One boss is down.",
            "Its core contained a fragment of the same signal.",
            "The signal is being distributed through artifacts.",
            "Find three of them. Then we can trace the source."
        ], speaker="NEXUS", color=CYAN, title="CHAPTER I // TRACE THE SIGNAL")

    if story_chapter == 2 and artifacts >= 3 and not story_artifact_dialogue_seen:
        story_artifact_dialogue_seen = True
        story_chapter = 3
        start_dialogue([
            "Three artifacts. Signal triangulated.",
            "The source is not random space.",
            "It is a damaged mirror of the Omega Dimension.",
            "Coordinates locked: CORRUPTED OMEGA.",
            "The portal is going to hate this."
        ], speaker="NEXUS", color=PURPLE, title="CHAPTER II // THE MIRROR")

    if story_chapter == 3 and current_world == 9 and not story_final_warning_seen:
        story_final_warning_seen = True
        story_chapter = 4
        start_dialogue([
            "Signal confirmed.",
            "This dimension is being held together by one unstable core.",
            "Whatever is inside has copied every boss pattern we have seen.",
            "There is no backup route.",
            "Defeat it. Then decide what happens to reality."
        ], speaker="NEXUS", color=RED, title="CHAPTER III // ZERO HOUR")


def begin_finale():
    global story_chapter, ending_choice_active
    story_chapter = 5
    ending_choice_active = True
    start_dialogue([
        "The Corrupted Omega is down.",
        "The core is rewriting the laws of every connected dimension.",
        "There are two stable commands left.",
        "SEAL the core and preserve the multiverse.",
        "or REWRITE reality and build something completely new."
    ], speaker="OMEGA CORE", color=ORANGE, title="FINAL DECISION")


def choose_ending(choice):
    global ending_choice_active, ending_complete, ending_title, ending_body
    global mode, open_menu, current_world, boss
    global enemies, enemy_projectiles, bullets, pickups

    if story_dialogue_active:
        return

    if choice == 1:
        ending_title = "THE STABILIZED ENDING"
        ending_body = [
            "You sealed the Omega Core.",
            "The dimensions remain separate and stable.",
            "The portal network goes quiet.",
            "Nexus records one final line:",
            "'You saved a broken universe instead of replacing it.'"
        ]
    else:
        if artifacts >= 5:
            ending_title = "TRUE ENDING // OMEGA REWRITE"
            ending_body = [
                "You used the artifacts to rewrite the core safely.",
                "The old portal network disappears.",
                "A new multiverse is generated from the recovered fragments.",
                "Nexus smiles for the first time.",
                "Secret route discovered: REALITY ZERO."
            ]
        else:
            ending_title = "THE REWRITTEN ENDING"
            ending_body = [
                "You rewrote the Omega Core.",
                "The multiverse survives, but some worlds are different.",
                "New portal coordinates appear in the garage.",
                "Something new is waiting beyond them."
            ]

    ending_choice_active = False
    ending_complete = True
    story_chapter = 6
    mode = "HUB"
    open_menu = None
    current_world = 0
    boss = None
    enemies.clear()
    enemy_projectiles.clear()
    bullets.clear()
    pickups.clear()
    player_hp = player_max_hp
    player_energy = player_max_energy
    portal_energy = portal_max_energy
    save_game()


def draw_story_objective():
    rect = pygame.Rect(WIDTH - 365, 105, 335, 74)
    pygame.draw.rect(screen, (7, 12, 17), rect, border_radius=10)
    pygame.draw.rect(screen, YELLOW, rect, 2, border_radius=10)
    text("CURRENT OBJECTIVE", rect.x + 15, rect.y + 10, FONT_SMALL, YELLOW)
    text(story_objective(), rect.x + 15, rect.y + 38, FONT_SMALL, WHITE)


def draw_dialogue_overlay():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))
    box = pygame.Rect(110, HEIGHT - 245, WIDTH - 220, 190)
    pygame.draw.rect(screen, (7, 12, 17), box, border_radius=16)
    pygame.draw.rect(screen, story_dialogue_color, box, 3, border_radius=16)
    text(story_dialogue_title, box.x + 25, box.y + 18, FONT_SMALL, story_dialogue_color)
    text(story_dialogue_speaker, box.x + 25, box.y + 47, FONT_MED, WHITE)
    if story_dialogue_lines:
        line = story_dialogue_lines[story_dialogue_index]
        text(line, box.x + 25, box.y + 92, FONT_MED, WHITE)
    text("SPACE / ENTER / LMB = CONTINUE", box.right - 260, box.bottom - 28, FONT_SMALL, GRAY)


def draw_ending_overlay():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((2, 4, 7, 220))
    screen.blit(overlay, (0, 0))
    if not ending_complete:
        box = pygame.Rect(200, 115, 880, 570)
        pygame.draw.rect(screen, (8, 12, 18), box, border_radius=18)
        pygame.draw.rect(screen, ORANGE, box, 3, border_radius=18)
        text("OMEGA CORE // FINAL DECISION", box.centerx, box.y + 45, FONT_BIG, ORANGE, center=True)
        text("1  SEAL THE CORE", box.centerx, box.y + 190, FONT_HUGE, GREEN, center=True)
        text("2  REWRITE REALITY", box.centerx, box.y + 300, FONT_HUGE, PURPLE, center=True)
        text("Make your choice. There is no combat after this point.", box.centerx, box.y + 425, FONT, WHITE, center=True)
        text("Press 1 or 2", box.centerx, box.y + 475, FONT_MED, YELLOW, center=True)
    else:
        box = pygame.Rect(180, 100, 920, 600)
        pygame.draw.rect(screen, (8, 12, 18), box, border_radius=18)
        pygame.draw.rect(screen, GREEN if "STABILIZED" in ending_title else PURPLE, box, 3, border_radius=18)
        text(ending_title, box.centerx, box.y + 50, FONT_BIG, WHITE, center=True)
        y = box.y + 150
        for line in ending_body:
            text(line, box.centerx, y, FONT_MED if y < box.y + 330 else FONT, GRAY if y < box.y + 330 else WHITE, center=True)
            y += 55
        text("ENTER = RETURN TO THE GARAGE", box.centerx, box.bottom - 45, FONT_SMALL, YELLOW, center=True)


# ============================================================
# QUESTS
# ============================================================

quests = [
    {"id": "kill", "name": "ALIEN CLEANUP", "desc": "Pokonaj 10 przeciwników.", "target": 10, "progress": 0, "reward": 180, "done": False, "claimed": False},
    {"id": "visit", "name": "DIMENSIONAL TOURIST", "desc": "Odwiedz 5 różnych wymiarów.", "target": 5, "progress": 0, "reward": 250, "done": False, "claimed": False},
    {"id": "core", "name": "CORE HUNTER", "desc": "Zdobądź 2 Omega Core.", "target": 2, "progress": 0, "reward": 400, "done": False, "claimed": False},
    {"id": "chill", "name": "CHILL PROTOCOL", "desc": "Ukończ 3 minigry w Chill Room.", "target": 3, "progress": 0, "reward": 220, "done": False, "claimed": False},
    {"id": "lounge", "name": "ZEN SHIFT", "desc": "Spędź 20 sekund w Lounge.", "target": 20, "progress": 0, "reward": 160, "done": False, "claimed": False},
]

# ============================================================
# NPC / HUB ZONES
# ============================================================

HUB_ZONES = [
    {"name": "ARMORY", "rect": pygame.Rect(90, 170, 230, 150), "color": CYAN, "menu": "armory"},
    {"name": "PORTAL LAB", "rect": pygame.Rect(960, 170, 230, 150), "color": PURPLE, "menu": "lab"},
    {"name": "QUEST BOARD", "rect": pygame.Rect(90, 500, 230, 150), "color": YELLOW, "menu": "quests"},
    {"name": "NEXUS NPC", "rect": pygame.Rect(960, 500, 230, 150), "color": GREEN, "menu": "npc"},
]

# ============================================================
# UTILITIES
# ============================================================


def clamp(value, low, high):
    return max(low, min(high, value))


def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def text(text_value, x, y, font=FONT, color=WHITE, center=False):
    surf = font.render(str(text_value), True, color)
    if center:
        rect = surf.get_rect(center=(x, y))
        screen.blit(surf, rect)
    else:
        screen.blit(surf, (x, y))


def add_particles(x, y, color, amount=10, speed=3):
    for _ in range(amount):
        angle = random.uniform(0, math.pi * 2)
        vel = random.uniform(0.4, speed)
        particles.append({
            "x": x, "y": y,
            "vx": math.cos(angle) * vel,
            "vy": math.sin(angle) * vel,
            "life": random.uniform(0.25, 0.9),
            "max_life": 0.9,
            "color": color,
            "size": random.randint(2, 5),
        })


def is_world_unlocked(index):
    if index < 7:
        return True
    world = WORLD_DEFS[index]
    unlock = world.get("unlock")
    value = world.get("unlock_value", 0)
    if unlock == "kills":
        return kills >= value
    if unlock == "dimensions":
        return len(dimensions_visited) >= value
    if unlock == "bosses":
        return bosses_defeated >= value
    if unlock == "artifacts":
        return artifacts >= value
    return False


def world_name(index=None):
    idx = current_world if index is None else index
    return WORLD_DEFS[idx]["name"]


def active_world():
    return WORLD_DEFS[current_world]


def current_gun_mode():
    return GUN_MODES[gun_mode_index]

# ============================================================
# SAVE SYSTEM
# ============================================================


def save_game():
    data = {
        "player_x": player_x,
        "player_y": player_y,
        "hp": player_hp,
        "max_hp": player_max_hp,
        "stamina": player_stamina,
        "max_stamina": player_max_stamina,
        "energy": player_energy,
        "max_energy": player_max_energy,
        "coins": coins,
        "potions": potions,
        "level": player_level,
        "xp": player_xp,
        "xp_needed": player_xp_needed,
        "skill_points": skill_points,
        "kills": kills,
        "bosses": bosses_defeated,
        "dimensions_visited": list(dimensions_visited),
        "portal_shards": portal_shards,
        "omega_cores": omega_cores,
        "artifacts": artifacts,
        "owned_weapons": owned_weapons,
        "current_weapon": current_weapon,
        "weapon_levels": weapon_levels,
        "skills": skills,
        "current_character": current_character,
        "owned_characters": owned_characters,
        "world": current_world,
        "portal_color_name": portal_color_name,
        "quests": quests,
        "story_chapter": story_chapter,
        "story_intro_seen": story_intro_seen,
        "story_boss_dialogue_seen": story_boss_dialogue_seen,
        "story_artifact_dialogue_seen": story_artifact_dialogue_seen,
        "story_final_warning_seen": story_final_warning_seen,
        "ending_complete": ending_complete,
        "ending_title": ending_title,
        "chill_best": chill_best,
        "chill_completed": chill_completed,
        "chill_total_time": chill_total_time,
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except OSError:
        return False


def load_game():
    global player_x, player_y, player_hp, player_max_hp
    global player_stamina, player_max_stamina, player_energy, player_max_energy
    global coins, potions, player_level, player_xp, player_xp_needed, skill_points
    global kills, bosses_defeated, dimensions_visited, portal_shards, omega_cores, artifacts
    global owned_weapons, current_weapon, weapon_levels, skills
    global current_character, owned_characters
    global current_world, selected_world, portal_color_name, portal_color, quests
    global story_chapter, story_intro_seen, story_boss_dialogue_seen
    global story_artifact_dialogue_seen, story_final_warning_seen, ending_complete, ending_title
    global chill_best, chill_completed, chill_total_time

    if not os.path.exists(SAVE_FILE):
        dimensions_visited = {0}
        return
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        dimensions_visited = {0}
        return

    player_x = float(data.get("player_x", 640))
    player_y = float(data.get("player_y", 420))
    player_hp = int(data.get("hp", 100))
    player_max_hp = int(data.get("max_hp", 100))
    player_stamina = float(data.get("stamina", 100))
    player_max_stamina = int(data.get("max_stamina", 100))
    player_energy = float(data.get("energy", 100))
    player_max_energy = int(data.get("max_energy", 100))
    coins = int(data.get("coins", 200))
    potions = int(data.get("potions", 3))
    player_level = int(data.get("level", 1))
    player_xp = int(data.get("xp", 0))
    player_xp_needed = int(data.get("xp_needed", 100))
    skill_points = int(data.get("skill_points", 0))
    kills = int(data.get("kills", 0))
    bosses_defeated = int(data.get("bosses", 0))
    dimensions_visited = set(data.get("dimensions_visited", [0]))
    portal_shards = int(data.get("portal_shards", 0))
    omega_cores = int(data.get("omega_cores", 0))
    artifacts = int(data.get("artifacts", 0))
    owned_weapons = data.get("owned_weapons", ["BLASTER"])
    current_weapon = data.get("current_weapon", "BLASTER")
    weapon_levels = {**{name: 1 for name in WEAPONS}, **data.get("weapon_levels", {})}
    skills = {**skills, **data.get("skills", {})}
    saved_owned = data.get("owned_characters", [])
    if isinstance(saved_owned, list):
        owned_characters = [name for name in saved_owned if name in CHARACTERS]
    else:
        owned_characters = []

    saved_character = data.get("current_character", None)
    if saved_character in CHARACTERS:
        current_character = saved_character
        if current_character not in owned_characters:
            owned_characters.append(current_character)
    else:
        current_character = None

    current_world = int(data.get("world", 0))
    current_world = clamp(current_world, 0, len(WORLD_DEFS) - 1)
    selected_world = current_world
    portal_color_name = data.get("portal_color_name", "GREEN")
    portal_color = PORTAL_COLORS.get(portal_color_name, GREEN)
    story_chapter = int(data.get("story_chapter", 0))
    story_intro_seen = bool(data.get("story_intro_seen", False))
    story_boss_dialogue_seen = bool(data.get("story_boss_dialogue_seen", False))
    story_artifact_dialogue_seen = bool(data.get("story_artifact_dialogue_seen", False))
    story_final_warning_seen = bool(data.get("story_final_warning_seen", False))
    ending_complete = bool(data.get("ending_complete", False))
    ending_title = data.get("ending_title", "")
    saved_chill_best = data.get("chill_best", {})
    if isinstance(saved_chill_best, dict):
        for key in ("TARGETS", "HACK", "HOLO"):
            chill_best[key] = int(saved_chill_best.get(key, chill_best.get(key, 0)))
    chill_completed = int(data.get("chill_completed", 0))
    chill_total_time = float(data.get("chill_total_time", 0.0))
    saved_quests = data.get("quests")
    if isinstance(saved_quests, list):
        saved_by_id = {q.get("id"): q for q in saved_quests if isinstance(q, dict)}
        for q in quests:
            old = saved_by_id.get(q["id"])
            if old:
                q["progress"] = float(old.get("progress", q["progress"]))
                q["done"] = bool(old.get("done", False))
                q["claimed"] = bool(old.get("claimed", False))
    dimensions_visited.add(0)
    for q in quests:
        if q["id"] == "kill":
            q["progress"] = min(q["target"], kills)
        elif q["id"] == "visit":
            q["progress"] = min(q["target"], len(dimensions_visited))
        elif q["id"] == "core":
            q["progress"] = min(q["target"], omega_cores)
        elif q["id"] == "chill":
            q["progress"] = min(q["target"], chill_completed)
        if q["progress"] >= q["target"]:
            q["done"] = True


def autosave(dt):
    global last_save, save_flash
    last_save += dt
    if last_save >= 15:
        if save_game():
            save_flash = 1.2
        last_save = 0.0

# ============================================================
# PLAYER / LEVEL
# ============================================================


def add_xp(amount):
    global player_xp, player_level, player_xp_needed, skill_points
    global player_max_hp, player_hp, player_max_energy, player_energy
    player_xp += amount
    while player_xp >= player_xp_needed:
        player_xp -= player_xp_needed
        player_level += 1
        skill_points += 2
        player_xp_needed = int(player_xp_needed * 1.22)
        player_max_hp += 10
        player_hp = player_max_hp
        player_max_energy += 8
        player_energy = player_max_energy
        add_particles(player_x, player_y, YELLOW, 50, 6)


def reset_player():
    global player_x, player_y, player_hp, player_stamina, player_energy, portal_energy
    player_x, player_y = 640, 420
    player_hp = player_max_hp
    player_stamina = player_max_stamina
    player_energy = player_max_energy
    portal_energy = portal_max_energy
    bullets.clear()
    enemy_projectiles.clear()
    add_particles(player_x, player_y, CYAN, 40, 6)

# ============================================================
# QUEST SYSTEM
# ============================================================


def update_quest_progress(event_type, amount=1):
    for q in quests:
        if q["done"]:
            continue
        if q["id"] == event_type:
            q["progress"] = min(q["target"], q["progress"] + amount)
            if q["progress"] >= q["target"]:
                q["done"] = True


def claim_quest(index):
    global coins, portal_shards, potions
    if index < 0 or index >= len(quests):
        return
    q = quests[index]
    if q["done"] and not q["claimed"]:
        coins += q["reward"]
        if q["id"] == "core":
            portal_shards += 2
        elif q["id"] == "kill":
            potions += 1
        elif q["id"] == "visit":
            portal_shards += 3
        q["claimed"] = True
        save_game()

# ============================================================
# PORTAL
# ============================================================


def activate_portal():
    global portal_active, portal_energy
    cost = max(15, 20 - skills["PORTAL"] * 2)
    if portal_active:
        portal_active = False
        global open_menu
        open_menu = None
        return
    if portal_energy >= cost:
        portal_energy -= cost
        portal_active = True
        add_particles(portal_x, portal_y, portal_color, 60, 7)


def travel_to(index):
    global current_world, selected_world, open_menu, portal_energy, mode
    global player_x, player_y, enemies, enemy_projectiles, bullets, boss, world_kills, world_time
    if not is_world_unlocked(index):
        return
    if portal_energy < 15 and index != current_world:
        return
    selected_world = index
    current_world = index
    dimensions_visited.add(index)
    update_quest_progress("visit")
    if index != 0:
        portal_energy = max(0, portal_energy - 15 + skills["PORTAL"] * 2)
    mode = "WORLD"
    open_menu = None
    player_x, player_y = 500, 420
    enemies.clear()
    enemy_projectiles.clear()
    bullets.clear()
    pickups.clear()
    boss = None
    world_kills = 0
    world_time = 0.0
    add_particles(player_x, player_y, active_world()["color"], 90, 9)
    save_game()


def return_to_hub():
    global mode, open_menu, enemies, enemy_projectiles, bullets, boss
    mode = "HUB"
    open_menu = None
    enemies.clear()
    enemy_projectiles.clear()
    bullets.clear()
    boss = None
    save_game()

# ============================================================
# PORTAL GUN MODES
# ============================================================


def shoot():
    global last_shot, player_energy
    now = pygame.time.get_ticks() / 1000
    weapon = WEAPONS[current_weapon]
    if now - last_shot < weapon["cooldown"]:
        return
    energy_cost = {"BLASTER": 2, "GRAVITY": 7, "SHOCKWAVE": 9, "TIME SHOT": 6, "BLACK HOLE": 16}[current_gun_mode()]
    if player_energy < energy_cost:
        return
    last_shot = now
    player_energy -= max(1, energy_cost - skills["ENERGY"])
    mx, my = pygame.mouse.get_pos()
    angle = math.atan2(my - player_y, mx - player_x)
    speed_bonus = 1.10 if current_character == "RICK" else 1.0
    level_bonus = (weapon_levels[current_weapon] - 1) * (4 + skills["WEAPON"])
    damage = weapon["damage"] + level_bonus
    if current_character == "RICK PRIME":
        damage = int(damage * 1.25)
    elif current_character == "EVIL MORTY":
        damage = int(damage * 1.12)
    elif current_character == "RICK":
        damage += 5
    elif current_character == "SUMMER":
        damage = int(damage * 1.05)
    elif current_character == "MORTY" and character_timers["lucky"] > 0:
        damage = int(damage * 3.5)
        character_timers["lucky"] = 0.0
    mode_name = current_gun_mode()
    if mode_name == "SHOCKWAVE":
        create_shockwave(mx, my, damage)
        return
    bullet = {
        "x": player_x,
        "y": player_y,
        "vx": math.cos(angle) * weapon["speed"] * speed_bonus,
        "vy": math.sin(angle) * weapon["speed"] * speed_bonus,
        "damage": damage,
        "color": (PINK if current_character in ("RICK PRIME", "SUMMER") else GREEN if current_character == "EVIL MORTY" else YELLOW if current_character == "MORTY" else weapon["color"]),
        "mode": mode_name,
        "life": 1.7,
    }
    bullets.append(bullet)
    add_particles(player_x + math.cos(angle) * 28, player_y + math.sin(angle) * 28, weapon["color"], 6, 2)


def create_shockwave(tx, ty, damage):
    radius = 125 + skills["WEAPON"] * 10
    add_particles(tx, ty, CYAN, 60, 6)
    for enemy in enemies:
        d = dist(tx, ty, enemy["x"], enemy["y"])
        if d <= radius:
            enemy["hp"] -= int(damage * 0.9)
            if d > 0:
                push = max(0, (radius - d) / radius)
                enemy["x"] += (enemy["x"] - tx) / d * 100 * push
                enemy["y"] += (enemy["y"] - ty) / d * 100 * push
    if boss is not None and dist(tx, ty, boss["x"], boss["y"]) <= radius:
        boss["hp"] -= int(damage * 0.7)


def cycle_gun_mode():
    global gun_mode_index
    gun_mode_index = (gun_mode_index + 1) % len(GUN_MODES)
    add_particles(player_x, player_y, CYAN, 12, 2)


def damage_area(tx, ty, radius, damage, color, slow=0.0):
    for enemy in enemies:
        d = dist(tx, ty, enemy["x"], enemy["y"])
        if d <= radius:
            enemy["hp"] -= int(damage * (1.0 - min(0.35, d / max(1, radius) * 0.35)))
            if slow > 0:
                enemy["slow"] = max(enemy.get("slow", 0.0), slow)
            add_particles(enemy["x"], enemy["y"], color, 8, 3)
    if boss is not None and dist(tx, ty, boss["x"], boss["y"]) <= radius:
        boss["hp"] -= int(damage * 0.75)
        if slow > 0:
            boss["slow"] = max(boss.get("slow", 0.0), slow)
        add_particles(boss["x"], boss["y"], color, 15, 4)


def use_character_ability(slot):
    global character_cooldowns, character_timers
    global player_x, player_y, player_hp, player_energy, coins
    global time_glitch_timer, screen_shake, chill_message, chill_message_timer

    if character_cooldowns.get(slot, 0.0) > 0:
        return
    if mode != "WORLD" or open_menu is not None or story_dialogue_active or ending_choice_active or ending_complete:
        return

    mx, my = pygame.mouse.get_pos()
    name = current_character
    if name is None:
        return

    # EVIL MORTY = CONTROL / TRAPS
    if name == "EVIL MORTY":
        if slot == "Z":
            ability_fx.append({"type": "morty_trap", "x": mx, "y": my, "life": 6.0, "max_life": 6.0})
            character_cooldowns["Z"] = 5.0
            add_particles(mx, my, GREEN, 60, 5)
        elif slot == "X":
            victims = 0
            for enemy in enemies:
                if dist(enemy["x"], enemy["y"], mx, my) < 180:
                    enemy["slow"] = max(enemy.get("slow", 0.0), 4.5)
                    enemy["mind_control"] = max(enemy.get("mind_control", 0.0), 4.5)
                    enemy["hp"] -= 70 + player_level * 6
                    victims += 1
            if boss is not None and dist(boss["x"], boss["y"], mx, my) < 210:
                boss["slow"] = max(boss.get("slow", 0.0), 3.5)
                boss["hp"] -= 120 + player_level * 10
            character_cooldowns["X"] = 8.0
            ability_fx.append({"type": "mind_spike", "x": mx, "y": my, "life": 0.6, "max_life": 0.6})
            add_particles(mx, my, GREEN, 90 + victims * 15, 7)
        else:
            character_timers["evil_protocol"] = 6.0
            time_glitch_timer = 6.0
            character_cooldowns["V"] = 26.0
            ability_fx.append({"type": "evil_protocol", "x": player_x, "y": player_y, "life": 6.0, "max_life": 6.0})
            for enemy in enemies:
                enemy["slow"] = max(enemy.get("slow", 0.0), 6.0)
                enemy["hp"] -= 95 + player_level * 8
            if boss is not None:
                boss["slow"] = max(boss.get("slow", 0.0), 5.0)
                boss["hp"] -= 420 + player_level * 22
            add_particles(player_x, player_y, GREEN, 180, 10)

    # RICK PRIME = PURE BURST / RIFTS
    elif name == "RICK PRIME":
        if slot == "Z":
            ability_fx.append({"type": "prime_bomb", "x": mx, "y": my, "life": 1.0, "max_life": 1.0})
            character_cooldowns["Z"] = 6.0
            damage_area(mx, my, 190, 175 + player_level * 14, PINK)
            screen_shake = 13
            add_particles(mx, my, PINK, 150, 11)
        elif slot == "X":
            # A rift that launches a concentrated fan of PRIME bolts.
            angle = math.atan2(my - player_y, mx - player_x)
            for spread in (-0.28, -0.14, 0, 0.14, 0.28):
                a = angle + spread
                bullets.append({
                    "x": player_x, "y": player_y,
                    "vx": math.cos(a) * 17, "vy": math.sin(a) * 17,
                    "damage": 115 + player_level * 9,
                    "color": PINK, "mode": "PRIME_RIFT", "life": 1.8,
                })
            character_cooldowns["X"] = 4.5
            ability_fx.append({"type": "prime_rift", "x": player_x, "y": player_y, "life": 0.8, "max_life": 0.8, "angle": angle})
            add_particles(player_x, player_y, PURPLE, 75, 7)
        else:
            character_cooldowns["V"] = 30.0
            character_timers["prime_invuln"] = 3.5
            ability_fx.append({"type": "prime_collapse", "x": player_x, "y": player_y, "life": 3.0, "max_life": 3.0})
            damage_area(player_x, player_y, 390, 420 + player_level * 22, PINK)
            if boss is not None:
                boss["hp"] -= 750 + player_level * 45
            screen_shake = 26
            add_particles(player_x, player_y, PINK, 260, 14)

    # RICK = TECH / DRONES / LASER
    elif name == "RICK":
        if slot == "Z":
            angle = math.atan2(my - player_y, mx - player_x)
            ability_fx.append({"type": "freeze_ray", "x": player_x, "y": player_y, "life": 0.45, "max_life": 0.45, "angle": angle})
            for enemy in enemies:
                if dist(enemy["x"], enemy["y"], player_x, player_y) < 520:
                    enemy["slow"] = max(enemy.get("slow", 0.0), 7.0)
                    enemy["hp"] -= 80 + player_level * 6
            if boss is not None and dist(boss["x"], boss["y"], player_x, player_y) < 600:
                boss["slow"] = max(boss.get("slow", 0.0), 6.0)
                boss["hp"] -= 150 + player_level * 12
            character_cooldowns["Z"] = 6.5
            add_particles(player_x, player_y, ICE, 110, 8)
        elif slot == "X":
            for i in range(3):
                a = math.tau * i / 3.0
                turrets.append({
                    "x": player_x + math.cos(a) * 35,
                    "y": player_y + math.sin(a) * 35,
                    "life": 14.0,
                    "cooldown": i * 0.18,
                    "color": CYAN,
                    "damage": 32 + player_level * 3,
                })
            character_cooldowns["X"] = 12.0
            ability_fx.append({"type": "drone_swarm", "x": player_x, "y": player_y, "life": 1.2, "max_life": 1.2})
            add_particles(player_x, player_y, CYAN, 95, 6)
        else:
            character_cooldowns["V"] = 27.0
            angle = math.atan2(my - player_y, mx - player_x)
            ability_fx.append({"type": "dimension_cannon", "x": player_x, "y": player_y, "life": 0.75, "max_life": 0.75, "angle": angle})
            # Cannon hits in a line.
            for enemy in enemies:
                ex = enemy["x"] - player_x
                ey = enemy["y"] - player_y
                proj = ex * math.cos(angle) + ey * math.sin(angle)
                perp = abs(-ex * math.sin(angle) + ey * math.cos(angle))
                if 0 < proj < 900 and perp < 55:
                    enemy["hp"] -= 300 + player_level * 18
            if boss is not None:
                ex = boss["x"] - player_x
                ey = boss["y"] - player_y
                proj = ex * math.cos(angle) + ey * math.sin(angle)
                perp = abs(-ex * math.sin(angle) + ey * math.cos(angle))
                if 0 < proj < 1000 and perp < 70:
                    boss["hp"] -= 850 + player_level * 35
            screen_shake = 16
            add_particles(player_x, player_y, CYAN, 220, 13)

    # SUMMER = MOBILITY / DECOYS
    elif name == "SUMMER":
        if slot == "Z":
            old_x, old_y = player_x, player_y
            angle = math.atan2(my - player_y, mx - player_x)
            player_x = clamp(player_x + math.cos(angle) * 240, 45, WIDTH - 45)
            player_y = clamp(player_y + math.sin(angle) * 240, 120, HEIGHT - 80)
            ability_fx.append({"type": "phase_dash", "x": old_x, "y": old_y, "x2": player_x, "y2": player_y, "life": 0.55, "max_life": 0.55})
            damage_area(player_x, player_y, 110, 90 + player_level * 7, PINK)
            character_timers["phase"] = 0.9
            character_cooldowns["Z"] = 3.2
            add_particles(player_x, player_y, PINK, 90, 8)
        elif slot == "X":
            ability_fx.append({"type": "holo_decoy", "x": mx, "y": my, "life": 7.0, "max_life": 7.0, "phase": 0.0})
            character_timers["phase"] = 4.0
            character_cooldowns["X"] = 11.0
            add_particles(mx, my, CYAN, 100, 7)
        else:
            character_cooldowns["V"] = 21.0
            ability_fx.append({"type": "chaos_barrage", "x": player_x, "y": player_y, "life": 1.2, "max_life": 1.2})
            for i in range(30):
                a = math.tau * i / 30.0 + random.uniform(-0.05, 0.05)
                color = [PINK, YELLOW, CYAN, WHITE][i % 4]
                bullets.append({
                    "x": player_x, "y": player_y,
                    "vx": math.cos(a) * random.uniform(11, 18),
                    "vy": math.sin(a) * random.uniform(11, 18),
                    "damage": 62 + player_level * 4,
                    "color": color, "mode": "CHAOS", "life": 1.55,
                })
            add_particles(player_x, player_y, PINK, 190, 12)

    # MORTY = PURE CHAOS / RANDOM OUTCOMES
    else:
        if slot == "Z":
            angle = math.atan2(my - player_y, mx - player_x)
            for spread in (-0.18, 0, 0.18):
                a = angle + spread
                bullets.append({
                    "x": player_x, "y": player_y,
                    "vx": math.cos(a) * 15, "vy": math.sin(a) * 15,
                    "damage": random.randint(55, 150) + player_level * 5,
                    "color": random.choice([YELLOW, GREEN, CYAN]),
                    "mode": "LUCKY", "life": 1.6,
                })
            character_cooldowns["Z"] = 5.0
            add_particles(player_x, player_y, YELLOW, 65, 6)
        elif slot == "X":
            roll = random.randint(1, 6)
            character_cooldowns["X"] = 8.0
            if roll == 1:
                player_hp = min(player_max_hp, player_hp + 80)
                chill_message = "ANOMALY: PERFECT HEAL"
                chill_message_timer = 1.5
                add_particles(player_x, player_y, GREEN, 120, 8)
            elif roll == 2:
                coins += 350
                add_particles(player_x, player_y, YELLOW, 150, 10)
            elif roll == 3:
                for enemy in enemies:
                    if enemy["hp"] < 230:
                        enemy["hp"] = 0
                add_particles(player_x, player_y, RED, 100, 8)
            elif roll == 4:
                time_glitch_timer = 5.5
                add_particles(player_x, player_y, CYAN, 140, 9)
            elif roll == 5:
                for enemy in enemies:
                    enemy["x"] += random.randint(-160, 160)
                    enemy["y"] += random.randint(-120, 120)
                add_particles(player_x, player_y, PURPLE, 120, 9)
            else:
                portal_energy = min(portal_max_energy, portal_energy + 60)
                player_energy = min(player_max_energy, player_energy + 80)
                add_particles(player_x, player_y, ORANGE, 120, 8)
            ability_fx.append({"type": "anomaly_box", "x": mx, "y": my, "life": 1.0, "max_life": 1.0})
        else:
            character_cooldowns["V"] = 29.0
            time_glitch_timer = 7.0
            ability_fx.append({"type": "unstable_dimension", "x": player_x, "y": player_y, "life": 5.0, "max_life": 5.0})
            for enemy in enemies:
                enemy["hp"] -= random.randint(140, 300) + player_level * 5
                enemy["slow"] = max(enemy.get("slow", 0.0), 5.5)
                enemy["x"] = clamp(player_x + random.randint(-330, 330), 50, WIDTH - 50)
                enemy["y"] = clamp(player_y + random.randint(-230, 230), 120, HEIGHT - 90)
            if boss is not None:
                boss["hp"] -= 1000 + player_level * 35
                boss["slow"] = max(boss.get("slow", 0.0), 4.5)
            player_hp = min(player_max_hp, player_hp + 55)
            screen_shake = 22
            add_particles(player_x, player_y, YELLOW, 300, 15)


def switch_character(name):
    global current_character, character_cooldowns, coins, owned_characters
    if name not in CHARACTERS:
        return
    if name not in owned_characters:
        price = CHARACTER_PRICES[name]
        if coins < price:
            return
        coins -= price
        owned_characters.append(name)
    current_character = name
    character_cooldowns = {"Z": 0.0, "X": 0.0, "V": 0.0}
    add_particles(player_x, player_y, CHARACTERS[name]["color"], 100, 8)
    save_game()


def unequip_character():
    global current_character, character_cooldowns
    current_character = None
    character_cooldowns = {"Z": 0.0, "X": 0.0, "V": 0.0}
    add_particles(player_x, player_y, WHITE, 35, 3)
    save_game()


def update_character_system(dt):
    # Resolve ability damage / timed effects.
    for enemy in enemies[:]:
        if enemy.get("mind_control", 0.0) > 0:
            enemy["mind_control"] = max(0.0, enemy["mind_control"] - dt)
        if enemy.get("slow", 0.0) > 0:
            enemy["slow"] = max(0.0, enemy["slow"] - dt)
        if enemy.get("hp", 1) <= 0:
            kill_enemy(enemy)
            if enemy in enemies:
                enemies.remove(enemy)

    if boss is not None:
        if boss.get("mind_control", 0.0) > 0:
            boss["mind_control"] = max(0.0, boss["mind_control"] - dt)
        if boss.get("slow", 0.0) > 0:
            boss["slow"] = max(0.0, boss["slow"] - dt)
        if boss.get("hp", 1) <= 0:
            kill_enemy(boss, True)

    for key in character_cooldowns:
        character_cooldowns[key] = max(0.0, character_cooldowns[key] - dt)
    for key in character_timers:
        character_timers[key] = max(0.0, character_timers[key] - dt)

    # Turrets / Rick's drone swarm.
    for turret in turrets[:]:
        turret["life"] -= dt
        turret["cooldown"] -= dt
        if turret["life"] <= 0:
            turrets.remove(turret)
            continue
        if turret["cooldown"] <= 0:
            nearest = None
            nearest_d = 99999
            for enemy in enemies:
                d = dist(turret["x"], turret["y"], enemy["x"], enemy["y"])
                if d < nearest_d:
                    nearest, nearest_d = enemy, d
            if boss is not None:
                bd = dist(turret["x"], turret["y"], boss["x"], boss["y"])
                if bd < nearest_d:
                    nearest, nearest_d = boss, bd
            if nearest is not None:
                a = math.atan2(nearest["y"] - turret["y"], nearest["x"] - turret["x"])
                bullets.append({
                    "x": turret["x"], "y": turret["y"],
                    "vx": math.cos(a) * 13, "vy": math.sin(a) * 13,
                    "damage": turret.get("damage", 32),
                    "color": turret.get("color", CYAN),
                    "mode": "DRONE", "life": 1.3,
                })
                turret["cooldown"] = 0.38


def draw_character_fx():
    for fx in ability_fx[:]:
        fx["life"] -= clock.get_time() / 1000.0
        if fx["life"] <= 0:
            ability_fx.remove(fx)
            continue
        x, y = int(fx["x"]), int(fx["y"])
        ratio = clamp(fx["life"] / max(0.01, fx.get("max_life", 1.0)), 0, 1)

        if fx["type"] == "morty_trap":
            r = int(48 + math.sin(game_time * 8) * 9)
            pygame.draw.circle(screen, GREEN, (x, y), r, 3)
            pygame.draw.circle(screen, YELLOW, (x, y), max(6, r // 2), 2)
            for i in range(6):
                a = game_time * 1.7 + i * math.tau / 6
                px, py = x + math.cos(a) * r, y + math.sin(a) * r
                pygame.draw.line(screen, GREEN, (x, y), (int(px), int(py)), 1)

        elif fx["type"] == "mind_spike":
            r = int(190 * (1 - ratio))
            pygame.draw.circle(screen, GREEN, (x, y), max(8, r), 4)
            for i in range(10):
                a = i * math.tau / 10 + game_time * 2
                pygame.draw.line(screen, YELLOW, (x, y), (x + int(math.cos(a) * r), y + int(math.sin(a) * r)), 2)

        elif fx["type"] == "evil_protocol":
            r1 = int(70 + (1 - ratio) * 270)
            r2 = int(40 + (1 - ratio) * 190)
            pygame.draw.circle(screen, GREEN, (x, y), r1, 4)
            pygame.draw.circle(screen, YELLOW, (x, y), r2, 2)
            for i in range(14):
                a = game_time * 1.7 + i * math.tau / 14
                pygame.draw.circle(screen, GREEN, (x + int(math.cos(a) * r1), y + int(math.sin(a) * r1)), 4)

        elif fx["type"] == "prime_bomb":
            r = int(185 * (1 - ratio))
            pygame.draw.circle(screen, PINK, (x, y), max(8, r), 6)
            pygame.draw.circle(screen, PURPLE, (x, y), max(4, r // 2), 3)
            for i in range(18):
                a = game_time * 2 + i * math.tau / 18
                pygame.draw.line(screen, PINK, (x, y), (x + int(math.cos(a) * r), y + int(math.sin(a) * r)), 2)

        elif fx["type"] == "prime_rift":
            angle = fx.get("angle", 0.0)
            length = int(340 * (1 - ratio))
            for off in (-15, 0, 15):
                a = angle + math.radians(off)
                pygame.draw.line(screen, PURPLE, (x, y), (x + int(math.cos(a) * length), y + int(math.sin(a) * length)), 4)
            pygame.draw.circle(screen, PINK, (x, y), int(30 + ratio * 25), 3)

        elif fx["type"] == "prime_collapse":
            r = int(390 * (1 - ratio))
            pygame.draw.circle(screen, PINK, (x, y), max(12, r), 7)
            pygame.draw.circle(screen, PURPLE, (x, y), max(6, r // 2), 3)
            pygame.draw.circle(screen, WHITE, (x, y), max(3, r // 7))

        elif fx["type"] == "freeze_ray":
            angle = fx.get("angle", 0.0)
            length = 540
            width = 34
            end_x = x + int(math.cos(angle) * length)
            end_y = y + int(math.sin(angle) * length)
            pygame.draw.line(screen, ICE, (x, y), (end_x, end_y), width)
            pygame.draw.line(screen, WHITE, (x, y), (end_x, end_y), 5)

        elif fx["type"] == "drone_swarm":
            for i in range(3):
                a = game_time * 2 + i * math.tau / 3
                px = x + int(math.cos(a) * 48)
                py = y + int(math.sin(a) * 48)
                pygame.draw.circle(screen, CYAN, (px, py), 10, 2)
                pygame.draw.line(screen, WHITE, (px - 9, py), (px + 9, py), 2)

        elif fx["type"] == "dimension_cannon":
            angle = fx.get("angle", 0.0)
            length = 980
            end_x = x + int(math.cos(angle) * length)
            end_y = y + int(math.sin(angle) * length)
            pygame.draw.line(screen, CYAN, (x, y), (end_x, end_y), 18)
            pygame.draw.line(screen, WHITE, (x, y), (end_x, end_y), 5)

        elif fx["type"] == "phase_dash":
            x2, y2 = int(fx.get("x2", x)), int(fx.get("y2", y))
            for i in range(6):
                t = i / 6
                px = int(x + (x2 - x) * t)
                py = int(y + (y2 - y) * t)
                pygame.draw.circle(screen, PINK, (px, py), max(3, 12 - i), 2)

        elif fx["type"] == "holo_decoy":
            r = int(26 + math.sin(game_time * 8) * 8)
            pygame.draw.circle(screen, CYAN, (x, y), r, 3)
            pygame.draw.circle(screen, PINK, (x, y), r + 10, 1)
            pygame.draw.line(screen, WHITE, (x - r, y), (x + r, y), 2)
            pygame.draw.line(screen, WHITE, (x, y - r), (x, y + r), 2)

        elif fx["type"] == "chaos_barrage":
            r = int(30 + (1 - ratio) * 110)
            pygame.draw.circle(screen, PINK, (x, y), r, 3)
            pygame.draw.circle(screen, YELLOW, (x, y), max(5, r // 3), 2)

        elif fx["type"] == "anomaly_box":
            size = int(28 + (1 - ratio) * 70)
            rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
            pygame.draw.rect(screen, YELLOW, rect, 3, border_radius=8)
            pygame.draw.line(screen, GREEN, (x - size, y - size), (x + size, y + size), 2)
            pygame.draw.line(screen, CYAN, (x + size, y - size), (x - size, y + size), 2)

        elif fx["type"] == "unstable_dimension":
            r = int(65 + (1 - ratio) * 280)
            for i, c in enumerate((YELLOW, GREEN, CYAN, PURPLE)):
                pygame.draw.ellipse(screen, c, (x - r + i * 6, y - r // 2, 2 * r - i * 12, r), 2)


def draw_turrets():
    for turret in turrets:
        x, y = int(turret["x"]), int(turret["y"])
        c = turret.get("color", CYAN)
        pygame.draw.circle(screen, (35, 45, 60), (x, y), 15)
        pygame.draw.circle(screen, c, (x, y), 8)
        pygame.draw.circle(screen, WHITE, (x, y), 3)
        pygame.draw.line(screen, c, (x - 14, y), (x + 14, y), 3)
# ============================================================
# ENEMIES
# ============================================================


def make_enemy(enemy_type, x, y):
    hp, speed, damage, radius = ENEMY_STATS.get(enemy_type, (120, 1.5, 8, 25))
    danger = active_world()["danger"]
    return {
        "x": x, "y": y, "type": enemy_type,
        "hp": int(hp * danger), "max_hp": int(hp * danger),
        "speed": speed, "damage": int(damage * danger), "radius": radius,
        "attack_timer": random.uniform(0.5, 1.6),
        "phase": random.random() * 10,
        "slow": 0.0, "blackhole": 0.0,
    }


def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x, y = random.randint(80, WIDTH - 80), 120
    elif side == "bottom":
        x, y = random.randint(80, WIDTH - 80), HEIGHT - 110
    elif side == "left":
        x, y = 75, random.randint(140, HEIGHT - 110)
    else:
        x, y = WIDTH - 75, random.randint(140, HEIGHT - 110)
    choices = active_world()["enemies"]
    enemies.append(make_enemy(random.choice(choices), x, y))


def spawn_boss():
    global boss
    if current_world not in BOSS_DEFS or boss is not None:
        return
    name, color, hp, damage = BOSS_DEFS[current_world]
    boss = make_enemy("OMEGA", WIDTH - 170, HEIGHT // 2)
    boss["name"] = name
    boss["color"] = color
    boss["hp"] = hp + player_level * 130
    boss["max_hp"] = boss["hp"]
    boss["damage"] = damage + player_level * 2
    boss["radius"] = 65
    boss["speed"] = 0.8
    boss["attack_timer"] = 1.0
    boss["boss"] = True


def shoot_enemy_projectile(enemy, spread=0.0):
    angle = math.atan2(player_y - enemy["y"], player_x - enemy["x"]) + spread
    speed = 5.4 if not enemy.get("boss") else 6.2
    enemy_projectiles.append({
        "x": enemy["x"], "y": enemy["y"],
        "vx": math.cos(angle) * speed, "vy": math.sin(angle) * speed,
        "damage": enemy["damage"],
    })


def enemy_ai(enemy, dt):
    global player_hp, damage_flash, screen_shake
    dx = player_x - enemy["x"]
    dy = player_y - enemy["y"]
    d = math.hypot(dx, dy)
    nx, ny = (dx / d, dy / d) if d else (0, 0)
    slow_factor = 0.45 if enemy["slow"] > 0 else 1.0
    black_factor = 0.35 if enemy["blackhole"] > 0 else 1.0
    enemy["slow"] = max(0, enemy["slow"] - dt)
    enemy["blackhole"] = max(0, enemy["blackhole"] - dt)
    enemy["attack_timer"] -= dt
    speed = enemy["speed"] * slow_factor * black_factor
    t = enemy["type"]

    # Evil Morty's Mind Spike turns an enemy against the flow of combat:
    # it becomes harmless toward the player and wanders in a disrupted state.
    if enemy.get("mind_control", 0) > 0:
        enemy["no_contact_damage"] = True
        drift = math.sin(game_time * 5 + enemy["phase"])
        enemy["x"] += (-ny) * drift * 20 * dt
        enemy["y"] += nx * drift * 20 * dt
        if enemy["attack_timer"] <= 0:
            enemy["attack_timer"] = 0.35
        return
    else:
        enemy["no_contact_damage"] = False

    if enemy.get("boss"):
        if d > 180:
            enemy["x"] += nx * speed * 60 * dt
            enemy["y"] += ny * speed * 60 * dt
        if enemy["attack_timer"] <= 0:
            for spread in (-0.45, -0.23, 0, 0.23, 0.45):
                shoot_enemy_projectile(enemy, spread)
            enemy["attack_timer"] = 1.15
        if d < 175 and enemy["attack_timer"] <= 0:
            player_hp -= 0 if enemy.get("no_contact_damage", False) else enemy["damage"]
            damage_flash = 0.2
            screen_shake = 12
        return

    if t == "STALKER":
        if d > 55:
            enemy["x"] += nx * speed * 60 * dt
            enemy["y"] += ny * speed * 60 * dt
        elif enemy["attack_timer"] <= 0:
            player_hp -= 0 if enemy.get("no_contact_damage", False) else enemy["damage"]
            enemy["attack_timer"] = 0.75
            damage_flash = 0.12
            screen_shake = 5
    elif t == "HUNTER":
        ang = math.atan2(dy, dx) + math.sin(game_time * 2 + enemy["phase"]) * 0.75
        enemy["x"] += math.cos(ang) * speed * 60 * dt
        enemy["y"] += math.sin(ang) * speed * 60 * dt
        if enemy["attack_timer"] <= 0:
            shoot_enemy_projectile(enemy)
            enemy["attack_timer"] = 1.2
    elif t == "SPITTER":
        if d > 310:
            enemy["x"] += nx * speed * 60 * dt
            enemy["y"] += ny * speed * 60 * dt
        elif d < 210:
            enemy["x"] -= nx * speed * 60 * dt
            enemy["y"] -= ny * speed * 60 * dt
        if enemy["attack_timer"] <= 0 and d < 700:
            shoot_enemy_projectile(enemy)
            enemy["attack_timer"] = 1.5
    elif t == "SWARM":
        enemy["x"] += nx * speed * 60 * dt + math.cos(game_time * 7 + enemy["phase"]) * 0.8
        enemy["y"] += ny * speed * 60 * dt + math.sin(game_time * 8 + enemy["phase"]) * 0.8
        if d < 42 and enemy["attack_timer"] <= 0:
            player_hp -= 0 if enemy.get("no_contact_damage", False) else enemy["damage"]
            enemy["attack_timer"] = 0.5
            damage_flash = 0.1
    elif t == "TANK":
        if d > 80:
            enemy["x"] += nx * speed * 60 * dt
            enemy["y"] += ny * speed * 60 * dt
        if enemy["attack_timer"] <= 0:
            shoot_enemy_projectile(enemy, 0.12)
            enemy["attack_timer"] = 1.9
    elif t == "PHANTOM":
        wave = math.sin(game_time * 3 + enemy["phase"])
        enemy["x"] += nx * speed * 55 * dt + (-ny) * wave * 18 * dt
        enemy["y"] += ny * speed * 55 * dt + nx * wave * 18 * dt
        if enemy["attack_timer"] <= 0:
            shoot_enemy_projectile(enemy, 0.22)
            enemy["attack_timer"] = 1.45
    elif t == "VOID":
        if d > 160:
            enemy["x"] += nx * speed * 60 * dt
            enemy["y"] += ny * speed * 60 * dt
        if enemy["attack_timer"] <= 0:
            for spread in (-0.25, 0, 0.25):
                shoot_enemy_projectile(enemy, spread)
            enemy["attack_timer"] = 1.7
    elif t == "FROST":
        if d > 100:
            enemy["x"] += nx * speed * 60 * dt
            enemy["y"] += ny * speed * 60 * dt
        if enemy["attack_timer"] <= 0:
            shoot_enemy_projectile(enemy)
            enemy["attack_timer"] = 1.6
    elif t == "GLITCH":
        if random.random() < 0.025:
            enemy["x"] = random.randint(100, WIDTH - 100)
            enemy["y"] = random.randint(130, HEIGHT - 130)
            add_particles(enemy["x"], enemy["y"], CYAN, 15, 4)
        if d > 120:
            enemy["x"] += nx * speed * 60 * dt
            enemy["y"] += ny * speed * 60 * dt
        if enemy["attack_timer"] <= 0:
            shoot_enemy_projectile(enemy, random.choice([-0.3, 0, 0.3]))
            enemy["attack_timer"] = 1.35


def update_enemies(dt):
    for enemy in enemies[:]:
        enemy_ai(enemy, dt)
    if boss is not None:
        enemy_ai(boss, dt)


def update_enemy_projectiles(dt):
    global player_hp, damage_flash, screen_shake
    for p in enemy_projectiles[:]:
        p["x"] += p["vx"] * 60 * dt
        p["y"] += p["vy"] * 60 * dt
        if p["x"] < -80 or p["x"] > WIDTH + 80 or p["y"] < -80 or p["y"] > HEIGHT + 80:
            enemy_projectiles.remove(p)
            continue
        if dist(p["x"], p["y"], player_x, player_y) < 20:
            if character_timers["phase"] <= 0 and character_timers["prime_invuln"] <= 0:
                player_hp -= p["damage"]
                damage_flash = 0.15
                screen_shake = 7
                add_particles(player_x, player_y, RED, 8, 3)
            else:
                add_particles(player_x, player_y, character_color(), 8, 3)
            if p in enemy_projectiles:
                enemy_projectiles.remove(p)

# ============================================================
# BULLET UPDATE / DEATHS / LOOT
# ============================================================


def kill_enemy(enemy, boss_kill=False):
    global coins, kills, bosses_defeated, omega_cores, portal_shards, world_kills, boss, artifacts
    reward = active_world()["reward"]
    if boss_kill:
        bosses_defeated += 1
        coins += reward * 8
        omega_cores += 1
        portal_shards += 5
        artifacts += 1
        update_quest_progress("core")
        add_xp(500 + current_world * 100)
        add_particles(enemy["x"], enemy["y"], enemy.get("color", ORANGE), 180, 11)
        pickups.append({"x": enemy["x"], "y": enemy["y"], "type": "OMEGA_CORE", "value": reward * 6})
        boss = None
        if current_world == 9:
            begin_finale()
        else:
            update_story_state()
        return
    kills += 1
    world_kills += 1
    update_quest_progress("kill")
    add_xp(18 + current_world * 6)
    coins += reward
    add_particles(enemy["x"], enemy["y"], active_world()["color"], 35, 6)
    loot_bonus = 1.0 + skills["LOOT"] * 0.15
    if random.random() < min(0.95, 0.55 * loot_bonus):
        pickups.append({"x": enemy["x"], "y": enemy["y"], "type": "CREDIT", "value": random.randint(10, max(12, reward))})
    if random.random() < min(0.35, 0.08 * loot_bonus):
        pickups.append({"x": enemy["x"], "y": enemy["y"], "type": "HEAL", "value": 25})
    if random.random() < min(0.35, 0.10 * loot_bonus):
        pickups.append({"x": enemy["x"], "y": enemy["y"], "type": "ENERGY", "value": 30})
    if current_world >= 7 and random.random() < 0.12:
        pickups.append({"x": enemy["x"], "y": enemy["y"], "type": "ARTIFACT", "value": 1})


def update_bullets(dt):
    for bullet in bullets[:]:
        bullet["x"] += bullet["vx"] * 60 * dt
        bullet["y"] += bullet["vy"] * 60 * dt
        bullet["life"] -= dt
        if bullet["life"] <= 0:
            bullets.remove(bullet)
            continue
        mode_name = bullet["mode"]
        hit = False
        for enemy in enemies[:]:
            if dist(bullet["x"], bullet["y"], enemy["x"], enemy["y"]) <= enemy["radius"] + 8:
                enemy["hp"] -= bullet["damage"]
                if mode_name == "GRAVITY":
                    enemy["blackhole"] = max(enemy["blackhole"], 1.2)
                elif mode_name == "TIME SHOT":
                    enemy["slow"] = max(enemy["slow"], 2.6)
                elif mode_name == "BLACK HOLE":
                    enemy["blackhole"] = max(enemy["blackhole"], 3.0)
                    enemy["x"] += (player_x - enemy["x"]) * 0.08
                    enemy["y"] += (player_y - enemy["y"]) * 0.08
                add_particles(bullet["x"], bullet["y"], bullet["color"], 10, 3)
                hit = True
                if enemy["hp"] <= 0:
                    kill_enemy(enemy)
                    enemies.remove(enemy)
                break
        if boss is not None and not hit and dist(bullet["x"], bullet["y"], boss["x"], boss["y"]) <= boss["radius"] + 8:
            boss["hp"] -= bullet["damage"]
            if mode_name == "TIME SHOT":
                boss["slow"] = max(boss["slow"], 2.0)
            elif mode_name == "BLACK HOLE":
                boss["blackhole"] = max(boss["blackhole"], 2.0)
            add_particles(bullet["x"], bullet["y"], ORANGE, 12, 4)
            hit = True
            if boss["hp"] <= 0:
                kill_enemy(boss, True)
        if hit and bullet in bullets:
            bullets.remove(bullet)

# ============================================================
# PICKUPS / PARTICLES
# ============================================================


def update_pickups():
    global coins, player_hp, player_energy, omega_cores, artifacts
    for item in pickups[:]:
        if dist(item["x"], item["y"], player_x, player_y) < 36:
            kind = item["type"]
            if kind == "CREDIT":
                coins += item["value"]
            elif kind == "HEAL":
                player_hp = min(player_max_hp, player_hp + item["value"])
            elif kind == "ENERGY":
                player_energy = min(player_max_energy, player_energy + item["value"])
            elif kind == "OMEGA_CORE":
                omega_cores += 1
                update_quest_progress("core")
                add_xp(150)
            elif kind == "ARTIFACT":
                artifacts += 1
                add_xp(80)
                update_story_state()
            add_particles(item["x"], item["y"], YELLOW, 18, 3)
            pickups.remove(item)


def update_particles(dt):
    for p in particles[:]:
        p["x"] += p["vx"] * 60 * dt
        p["y"] += p["vy"] * 60 * dt
        p["vx"] *= 0.96
        p["vy"] *= 0.96
        p["life"] -= dt
        if p["life"] <= 0:
            particles.remove(p)

# ============================================================
# RANDOM EVENTS
# ============================================================


def trigger_random_event():
    global random_event_timer, random_event_text, random_event_color, random_event_display
    global coins, player_energy, portal_energy
    event = random.choice(["SWARM", "STORM", "GLITCH", "STASH"])
    if event == "SWARM":
        for _ in range(5 + current_world // 2):
            spawn_enemy()
        random_event_text = "ALIEN SWARM INBOUND"
        random_event_color = RED
    elif event == "STORM":
        portal_energy = portal_max_energy
        player_energy = player_max_energy
        add_particles(player_x, player_y, CYAN, 80, 8)
        random_event_text = "PORTAL STORM - ENERGY REFILLED"
        random_event_color = CYAN
    elif event == "GLITCH":
        for enemy in enemies:
            enemy["slow"] = 3.5
        random_event_text = "TIME GLITCH - ENEMIES SLOWED"
        random_event_color = YELLOW
    else:
        coins += 120 + current_world * 30
        portal_shards += 1
        add_particles(player_x, player_y, YELLOW, 70, 8)
        random_event_text = "DIMENSIONAL STASH DISCOVERED"
        random_event_color = YELLOW
    random_event_display = 4.0
    random_event_timer = random.uniform(18, 30)

# ============================================================
# DASH / SKILLS
# ============================================================


def perform_dash():
    global player_x, player_y, dash_cooldown, player_stamina
    cooldown = max(0.25, 0.85 - skills["DASH"] * 0.11)
    cost = max(10, 25 - skills["DASH"] * 2)
    if dash_cooldown > 0 or player_stamina < cost:
        return
    keys = pygame.key.get_pressed()
    dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    dy = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    if dx == 0 and dy == 0:
        mx, my = pygame.mouse.get_pos()
        ang = math.atan2(my - player_y, mx - player_x)
        dx, dy = math.cos(ang), math.sin(ang)
    else:
        length = math.hypot(dx, dy)
        dx, dy = dx / length, dy / length
    old_x, old_y = player_x, player_y
    distance_dash = 140 + skills["DASH"] * 12
    player_x = clamp(player_x + dx * distance_dash, 45, WIDTH - 45)
    player_y = clamp(player_y + dy * distance_dash, 120, HEIGHT - 80)
    player_stamina -= cost
    dash_cooldown = cooldown
    for i in range(18):
        t = i / 18
        add_particles(old_x + (player_x - old_x) * t, old_y + (player_y - old_y) * t, CYAN, 2, 1.5)


def upgrade_skill(name):
    global skill_points, player_max_hp, player_hp, player_max_energy, player_energy
    if skill_points <= 0 or skills[name] >= 5:
        return
    skill_points -= 1
    skills[name] += 1
    if name == "VITALITY":
        player_max_hp += 12
        player_hp += 12
    elif name == "ENERGY":
        player_max_energy += 10
        player_energy += 10
    add_particles(player_x, player_y, YELLOW, 18, 3)
    save_game()

# ============================================================
# MENUS - COMMON
# ============================================================


def draw_menu_box(rect, title, color):
    pygame.draw.rect(screen, (6, 11, 16), rect, border_radius=14)
    pygame.draw.rect(screen, color, rect, 2, border_radius=14)
    text(title, rect.centerx, rect.y + 28, FONT_BIG, color, center=True)


def draw_inventory():
    rect = pygame.Rect(260, 90, 760, 620)
    draw_menu_box(rect, "INVENTORY", CYAN)
    items = [
        ("POTIONS", potions, GREEN),
        ("OMEGA CORES", omega_cores, ORANGE),
        ("PORTAL SHARDS", portal_shards, PURPLE),
        ("ARTIFACTS", artifacts, YELLOW),
        ("CREDITS", coins, WHITE),
    ]
    y = 150
    for name, value, color in items:
        pygame.draw.rect(screen, PANEL2, (330, y, 620, 65), border_radius=8)
        pygame.draw.rect(screen, color, (330, y, 620, 65), 2, border_radius=8)
        text(name, 350, y + 12, FONT_MED, color)
        text(value, 870, y + 15, FONT_MED, WHITE)
        y += 82
    text("I / ESC = CLOSE", rect.centerx, 675, FONT_SMALL, GRAY, center=True)


def draw_skills():
    rect = pygame.Rect(220, 70, 840, 680)
    draw_menu_box(rect, "SKILL TREE", YELLOW)
    text(f"SKILL POINTS: {skill_points}", rect.centerx, 125, FONT_MED, WHITE, center=True)
    names = [
        ("VITALITY", "+HP", GREEN),
        ("ENERGY", "+ENERGY", CYAN),
        ("DASH", "FASTER DASH", BLUE),
        ("WEAPON", "+DAMAGE", ORANGE),
        ("PORTAL", "CHEAPER PORTALS", PURPLE),
        ("LOOT", "+LOOT", YELLOW),
    ]
    cols = 3
    for i, (name, desc, color) in enumerate(names):
        col = i % cols
        row = i // cols
        x = 280 + col * 245
        y = 190 + row * 200
        card = pygame.Rect(x, y, 210, 150)
        pygame.draw.rect(screen, PANEL2, card, border_radius=10)
        pygame.draw.rect(screen, color, card, 2, border_radius=10)
        text(name, card.centerx, y + 28, FONT_MED, color, center=True)
        text(desc, card.centerx, y + 62, FONT, WHITE, center=True)
        text(f"LEVEL {skills[name]} / 5", card.centerx, y + 92, FONT_SMALL, GRAY, center=True)
        text("CLICK TO UPGRADE", card.centerx, y + 122, FONT_SMALL, YELLOW, center=True)
    text("K / ESC = CLOSE", rect.centerx, 718, FONT_SMALL, GRAY, center=True)


def draw_quests():
    rect = pygame.Rect(170, 70, 940, 690)
    draw_menu_box(rect, "QUEST BOARD", YELLOW)
    row_h = 108
    gap = 12
    start_y = 145
    for i, q in enumerate(quests):
        y = start_y + i * (row_h + gap)
        card = pygame.Rect(220, y, 840, row_h)
        color = GREEN if q["done"] else YELLOW
        pygame.draw.rect(screen, PANEL2, card, border_radius=10)
        pygame.draw.rect(screen, color, card, 2, border_radius=10)
        progress = q["progress"]
        display_progress = int(progress) if float(progress).is_integer() else round(progress, 1)
        text(q["name"], 240, y + 10, FONT_MED, color)
        text(q["desc"], 240, y + 45, FONT_SMALL, WHITE)
        text(f"{display_progress} / {q['target']}", 240, y + 78, FONT_SMALL, GRAY)
        bar = pygame.Rect(380, y + 79, 330, 9)
        pygame.draw.rect(screen, (25, 25, 30), bar, border_radius=4)
        pygame.draw.rect(screen, color, (bar.x, bar.y, int(bar.w * clamp(progress / max(1, q['target']), 0, 1)), bar.h), border_radius=4)
        if q["claimed"]:
            text("CLAIMED", 955, y + 48, FONT_SMALL, GREEN, center=True)
        elif q["done"]:
            text("CLICK TO CLAIM", 945, y + 48, FONT_SMALL, YELLOW, center=True)
        else:
            text(f"REWARD {q['reward']} C", 940, y + 48, FONT_SMALL, WHITE, center=True)
    text("Q / ESC = CLOSE", rect.centerx, 735, FONT_SMALL, GRAY, center=True)


def draw_stats():
    rect = pygame.Rect(250, 85, 780, 630)
    draw_menu_box(rect, "STATISTICS", CYAN)
    stats = [
        ("LEVEL", player_level),
        ("KILLS", kills),
        ("BOSSES DEFEATED", bosses_defeated),
        ("DIMENSIONS VISITED", len(dimensions_visited)),
        ("CREDITS", coins),
        ("OMEGA CORES", omega_cores),
        ("PORTAL SHARDS", portal_shards),
        ("ARTIFACTS", artifacts),
    ]
    for i, (name, value) in enumerate(stats):
        col = i % 2
        row = i // 2
        x = 310 + col * 330
        y = 170 + row * 100
        pygame.draw.rect(screen, PANEL2, (x, y, 290, 72), border_radius=8)
        text(name, x + 20, y + 13, FONT_SMALL, GRAY)
        text(value, x + 20, y + 38, FONT_MED, WHITE)
    text("L / ESC = CLOSE", rect.centerx, 680, FONT_SMALL, GRAY, center=True)


def draw_armory():
    rect = pygame.Rect(180, 70, 920, 690)
    draw_menu_box(rect, "OMEGA ARMORY", CYAN)
    text(f"CREDITS: {coins}", rect.centerx, 122, FONT_MED, YELLOW, center=True)
    y = 165
    for name, data in WEAPONS.items():
        card = pygame.Rect(245, y, 790, 92)
        selected = name == current_weapon
        pygame.draw.rect(screen, (30, 48, 55) if selected else PANEL2, card, border_radius=9)
        pygame.draw.rect(screen, data["color"], card, 2, border_radius=9)
        level = weapon_levels[name]
        damage = data["damage"] + (level - 1) * 8
        text(name, 270, y + 12, FONT_MED, data["color"])
        text(f"LVL {level}   DAMAGE {damage}", 270, y + 50, FONT_SMALL, WHITE)
        if name not in owned_weapons:
            text(f"BUY {data['price']} C", 905, y + 30, FONT_SMALL, YELLOW, center=True)
        else:
            text("EQUIP", 805, y + 25, FONT_SMALL, GREEN if selected else GRAY, center=True)
            upgrade_cost = 150 * level
            text(f"UPGRADE {upgrade_cost} C", 940, y + 52, FONT_SMALL, YELLOW, center=True)
        y += 105
    text("B / ESC = CLOSE", rect.centerx, 725, FONT_SMALL, GRAY, center=True)


def draw_portal_lab():
    rect = pygame.Rect(190, 110, 900, 610)
    draw_menu_box(rect, "PORTAL LAB", portal_color)
    text(f"ACTIVE COLOR: {portal_color_name}", rect.centerx, 170, FONT_MED, portal_color, center=True)
    names = list(PORTAL_COLORS.keys())
    for i, name in enumerate(names):
        col = i % 4
        row = i // 4
        x = 300 + col * 165
        y = 240 + row * 120
        card = pygame.Rect(x, y, 135, 90)
        color = PORTAL_COLORS[name]
        pygame.draw.rect(screen, PANEL2, card, border_radius=9)
        pygame.draw.rect(screen, color, card, 3, border_radius=9)
        pygame.draw.circle(screen, color, card.center, 20)
        text(name, card.centerx, y + 68, FONT_SMALL, WHITE, center=True)
    text("CURRENT GUN MODE", rect.centerx, 500, FONT, WHITE, center=True)
    text(current_gun_mode(), rect.centerx, 540, FONT_BIG, CYAN, center=True)
    text("R = CHANGE MODE", rect.centerx, 585, FONT_SMALL, GRAY, center=True)
    text("TAB / ESC = CLOSE", rect.centerx, 660, FONT_SMALL, GRAY, center=True)


def draw_character_menu():
    frame_color = character_color() if current_character else CYAN
    pygame.draw.rect(screen, (5, 9, 14), (150, 50, 980, 710), border_radius=18)
    pygame.draw.rect(screen, frame_color, (150, 50, 980, 710), 2, border_radius=18)
    text("CHARACTER SELECT", WIDTH // 2, 85, FONT_HUGE, WHITE, center=True)
    text("Kazdy bohater ma osobne moce. Nowy gracz zaczyna bez postaci.", WIDTH // 2, 130, FONT, GRAY, center=True)

    # Rookie / no character
    rookie_rect = pygame.Rect(200, 165, 880, 68)
    pygame.draw.rect(screen, PANEL2 if current_character else (32, 44, 50), rookie_rect, border_radius=10)
    pygame.draw.rect(screen, CYAN if current_character is None else DARK, rookie_rect, 2, border_radius=10)
    text("ROOKIE // NO CHARACTER", rookie_rect.x + 18, rookie_rect.y + 10, FONT_MED, WHITE)
    text("Brak pasywki i brak Z/X/V. Tylko podstawowy Portal Gun.", rookie_rect.x + 18, rookie_rect.y + 40, FONT_SMALL, GRAY)
    text("EQUIPPED" if current_character is None else "CLICK TO UNEQUIP", rookie_rect.right - 155, rookie_rect.y + 23, FONT_SMALL, CYAN)

    for i, name in enumerate(CHARACTER_NAMES):
        col = i % 2
        row = i // 2
        x, y = 200 + col * 440, 250 + row * 125
        rect = pygame.Rect(x, y, 410, 108)
        color = CHARACTERS[name]["color"]
        owned = name in owned_characters
        selected = name == current_character
        pygame.draw.rect(screen, (30, 46, 54) if selected else PANEL2, rect, border_radius=12)
        pygame.draw.rect(screen, color, rect, 3 if selected else 2, border_radius=12)
        text(name, x + 16, y + 10, FONT_MED, color)
        text("ROLE: " + CHARACTERS[name]["role"] + "   PASSIVE: " + CHARACTERS[name]["passive"], x + 16, y + 43, FONT_SMALL, WHITE)
        text("Z " + CHARACTERS[name]["z"] + "   X " + CHARACTERS[name]["x"], x + 16, y + 63, FONT_SMALL, GRAY)
        text("V " + CHARACTERS[name]["ultimate"], x + 16, y + 82, FONT_SMALL, YELLOW)
        if owned:
            status = "EQUIPPED" if selected else "OWNED // CLICK"
            status_color = color if selected else GREEN
        else:
            status = f"BUY {CHARACTER_PRICES[name]} C"
            status_color = YELLOW
        text(status, x + 275, y + 18, FONT_SMALL, status_color)

    profile = character_profile()
    if profile:
        text(profile["description"], WIDTH // 2, 705, FONT, WHITE, center=True)
    else:
        text("Z/X/V pozostają wyłączone dopóki nie odblokujesz postaci.", WIDTH // 2, 705, FONT, CYAN, center=True)
    text("C / ESC = CLOSE", WIDTH // 2, 738, FONT_SMALL, GRAY, center=True)


def handle_character_click(mx, my):
    global current_character

    rookie_rect = pygame.Rect(200, 165, 880, 68)
    if rookie_rect.collidepoint(mx, my):
        unequip_character()
        return

    for i, name in enumerate(CHARACTER_NAMES):
        col = i % 2
        row = i // 2
        rect = pygame.Rect(200 + col * 440, 250 + row * 125, 410, 108)
        if rect.collidepoint(mx, my):
            switch_character(name)
            return

def draw_dimension_menu():
    rect = pygame.Rect(135, 50, 1010, 715)
    draw_menu_box(rect, "MULTIVERSE MAP", portal_color)
    text(f"PORTAL SHARDS: {portal_shards}", rect.centerx, 98, FONT, YELLOW, center=True)
    for i, world in enumerate(WORLD_DEFS):
        col = i % 3
        row = i // 3
        x = 175 + col * 325
        y = 135 + row * 112
        card = pygame.Rect(x, y, 290, 92)
        unlocked = is_world_unlocked(i)
        color = world["color"] if unlocked else DARK
        pygame.draw.rect(screen, PANEL2, card, border_radius=10)
        pygame.draw.rect(screen, color, card, 2, border_radius=10)
        label = world["name"] if unlocked else "LOCKED DIMENSION"
        text(f"{i + 1}. {label}", x + 12, y + 10, FONT_MED, color if unlocked else GRAY)
        if unlocked:
            text(world["subtitle"], x + 12, y + 44, FONT_SMALL, WHITE)
            if i == current_world:
                text("CURRENT", x + 220, y + 14, FONT_SMALL, GREEN)
            else:
                text("CLICK", x + 235, y + 55, FONT_SMALL, GRAY)
        else:
            unlock = world.get("unlock")
            req = world.get("unlock_value")
            if unlock == "kills":
                detail = f"Need {req} kills"
            elif unlock == "dimensions":
                detail = f"Visit {req} dimensions"
            elif unlock == "bosses":
                detail = f"Defeat {req} boss"
            else:
                detail = f"Find {req} artifacts"
            text(detail, x + 12, y + 47, FONT_SMALL, GRAY)
    text("M / ESC = CLOSE   1-9 / 0 = QUICK SELECT", rect.centerx, 732, FONT_SMALL, GRAY, center=True)

def draw_npc():
    rect = pygame.Rect(290, 130, 700, 500)
    draw_menu_box(rect, "NEXUS // MULTIVERSE FIXER", GREEN)
    lines = [
        "NEXUS: 'System stable... mostly.'",
        "",
        "I keep track of dimensional anomalies,",
        "lost cores and suspicious portal activity.",
        "",
        "TIP:",
        "• Explore dangerous dimensions for artifacts.",
        "• Defeat bosses to unlock corrupted realities.",
        "• Upgrade the Portal Gun in ARMORY.",
        "• Use the Skill Tree after leveling up.",
        "",
        f"CURRENT LEVEL: {player_level}",
        f"CURRENT WORLD: {world_name()}",
        "",
        f"STORY: {story_objective()}",
        "Press F near Nexus to receive story transmissions.",
    ]
    y = 205
    for line in lines:
        text(line, 345, y, FONT if not line.startswith("TIP") else FONT_MED, WHITE if not line.startswith("TIP") else YELLOW)
        y += 28
    text("N / ESC = CLOSE", rect.centerx, 590, FONT_SMALL, GRAY, center=True)

# ============================================================
# DRAWING - PLAYER, ENEMIES, GUN, PORTAL
# ============================================================


def draw_portal_gun(x, y, angle):
    surf = pygame.Surface((170, 100), pygame.SRCALPHA)
    pygame.draw.rect(surf, WHITE, (25, 31, 82, 30), border_radius=8)
    pygame.draw.rect(surf, CYAN, (30, 54, 72, 8), border_radius=4)
    pygame.draw.polygon(surf, (34, 44, 50), [(58, 58), (84, 58), (74, 89), (49, 89)])
    pygame.draw.rect(surf, (25, 35, 40), (46, 10, 44, 25), border_radius=8)
    pygame.draw.rect(surf, GREEN, (52, 14, 31, 17), border_radius=6)
    pygame.draw.line(surf, WHITE, (58, 16), (58, 27), 2)
    pygame.draw.circle(surf, RED, (99, 36), 5)
    pygame.draw.rect(surf, (25, 30, 34), (105, 34, 36, 20), border_radius=5)
    pygame.draw.rect(surf, portal_color, (133, 37, 18, 14), border_radius=4)
    rotated = pygame.transform.rotate(surf, -math.degrees(angle))
    screen.blit(rotated, rotated.get_rect(center=(x, y)))


def draw_player():
    bob = math.sin(game_time * 8) * 2
    x, y = player_x, player_y + bob
    profile = character_profile()
    c = profile["color"] if profile else GRAY
    secondary = profile["secondary"] if profile else WHITE

    pygame.draw.ellipse(screen, (3, 5, 7), (x - 31, y + 30, 62, 16))
    pygame.draw.rect(screen, (48, 58, 68), (x - 17, y + 8, 13, 28), border_radius=5)
    pygame.draw.rect(screen, (48, 58, 68), (x + 4, y + 8, 13, 28), border_radius=5)
    pygame.draw.rect(screen, (18, 22, 27), (x - 20, y + 30, 19, 9), border_radius=3)
    pygame.draw.rect(screen, (18, 22, 27), (x + 2, y + 30, 19, 9), border_radius=3)

    if current_character == "RICK":
        body_color = (70, 110, 190)
    elif current_character == "RICK PRIME":
        body_color = (55, 35, 65)
    elif current_character == "EVIL MORTY":
        body_color = (52, 105, 68)
    elif current_character == "SUMMER":
        body_color = (180, 75, 120)
    elif current_character == "MORTY":
        body_color = (190, 165, 65)
    else:
        body_color = (90, 100, 108)

    pygame.draw.rect(screen, body_color, (x - 23, y - 6, 46, 41), border_radius=11)
    pygame.draw.rect(screen, (38, 53, 60), (x - 18, y - 2, 36, 29), border_radius=7)
    pygame.draw.rect(screen, c, (x - 5, y + 2, 10, 21), border_radius=4)
    pygame.draw.rect(screen, (28, 36, 42), (x - 32, y - 1, 10, 30), border_radius=4)
    pygame.draw.rect(screen, secondary, (x - 31, y + 5, 5, 13), border_radius=2)

    pygame.draw.rect(screen, (182, 151, 125), (x - 7, y - 14, 14, 11))
    pygame.draw.circle(screen, (207, 178, 148), (int(x), int(y - 25)), 19)

    if current_character in ("RICK", "RICK PRIME"):
        pygame.draw.arc(screen, (180, 185, 195), (x - 21, y - 47, 42, 28), math.pi, math.tau, 7)
        for sx in (-14, -6, 5, 14):
            pygame.draw.polygon(screen, (180, 185, 195), [(x + sx - 4, y - 38), (x + sx, y - 53), (x + sx + 5, y - 38)])
    elif current_character == "SUMMER":
        pygame.draw.arc(screen, (150, 80, 95), (x - 19, y - 44, 38, 26), math.pi, math.tau, 6)
        pygame.draw.circle(screen, (150, 80, 95), (int(x + 20), int(y - 28)), 8)
    elif current_character == "MORTY":
        pygame.draw.arc(screen, (65, 45, 35), (x - 19, y - 44, 38, 26), math.pi, math.tau, 7)
    else:
        pygame.draw.arc(screen, GRAY, (x - 19, y - 44, 38, 26), math.pi, math.tau, 6)

    pygame.draw.circle(screen, c, (int(x + 7), int(y - 27)), 3)
    pygame.draw.circle(screen, c, (int(x - 10), int(y + 8)), 3)

    mx, my = pygame.mouse.get_pos()
    angle = math.atan2(my - y, mx - x)
    arm_x = x + math.cos(angle) * 26
    arm_y = y + math.sin(angle) * 26
    pygame.draw.line(screen, (190, 160, 135), (x, y + 2), (arm_x, arm_y), 9)
    draw_portal_gun(arm_x, arm_y, angle)

    if character_timers["phase"] > 0 or character_timers["prime_invuln"] > 0:
        pygame.draw.circle(screen, c, (int(x), int(y - 5)), 42, 3)

    if current_character:
        text(current_character, x, y - 66, FONT_SMALL, c, center=True)
    else:
        text("ROOKIE", x, y - 66, FONT_SMALL, GRAY, center=True)


def draw_portal():
    if not portal_active:
        return
    pulse = math.sin(game_time * 5) * 5
    cx, cy = int(portal_x), int(portal_y)
    for radius in range(90, 28, -8):
        alpha = max(3, int(28 * (1 - radius / 95)))
        glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*portal_color, alpha), (radius, radius), radius)
        screen.blit(glow, (cx - radius, cy - radius))
    pygame.draw.ellipse(screen, portal_color, (cx - 54 - pulse / 2, cy - 78, 108 + pulse, 156), 7)
    pygame.draw.ellipse(screen, WHITE, (cx - 44, cy - 66, 88, 132), 2)
    pygame.draw.ellipse(screen, portal_color, (cx - 33, cy - 55, 66, 110), 3)
    pygame.draw.ellipse(screen, (10, 20, 25), (cx - 28, cy - 51, 56, 102))
    for i in range(10):
        a = game_time * 1.3 + i * 0.65
        px = cx + math.cos(a) * 60
        py = cy + math.sin(a) * 80
        pygame.draw.circle(screen, portal_color, (int(px), int(py)), 3)


def draw_enemy(enemy):
    x, y = int(enemy["x"]), int(enemy["y"])
    t = enemy["type"]
    r = int(enemy.get("radius", 25))
    phase = enemy.get("phase", 0.0)
    bob = math.sin(game_time * 4 + phase)
    pulse = (math.sin(game_time * 5 + phase) + 1) * 0.5

    # --------------------------------------------------------
    # STATUS AURA / HIT EFFECTS
    # --------------------------------------------------------
    if enemy.get("mind_control", 0) > 0:
        pygame.draw.circle(screen, GREEN, (x, y), r + 9 + int(pulse * 3), 2)
        for i in range(3):
            a = game_time * 2.0 + i * 2.1
            sx = x + math.cos(a) * (r + 7)
            sy = y + math.sin(a) * (r + 7)
            pygame.draw.circle(screen, GREEN, (int(sx), int(sy)), 3)

    if enemy.get("slow", 0) > 0:
        pygame.draw.circle(screen, ICE, (x, y), r + 5, 2)

    if enemy.get("blackhole", 0) > 0:
        pygame.draw.ellipse(screen, PURPLE, (x - r - 8, y - r // 2, (r + 8) * 2, r), 2)

    # --------------------------------------------------------
    # STALKER - low, armored hunter
    # --------------------------------------------------------
    if t == "STALKER":
        body = (74, 88, 98)
        dark = (25, 31, 36)
        eye = RED

        # legs
        for side in (-1, 1):
            pygame.draw.line(screen, dark, (x + side * 12, y + 12), (x + side * 25, y + 31), 6)
            pygame.draw.line(screen, dark, (x + side * 18, y + 18), (x + side * 34, y + 10), 5)

        # silhouette + armor plates
        pygame.draw.polygon(screen, dark, [(x - 28, y + 4), (x - 16, y - 25), (x, y - 33), (x + 19, y - 24), (x + 29, y + 6), (x + 15, y + 25), (x - 15, y + 25)])
        pygame.draw.circle(screen, body, (x, y - 2), 24)
        pygame.draw.polygon(screen, (96, 110, 120), [(x - 18, y - 8), (x - 5, y - 21), (x + 7, y - 20), (x + 18, y - 7), (x + 11, y + 10), (x - 11, y + 10)])

        # face slit + eyes
        pygame.draw.rect(screen, (18, 24, 28), (x - 17, y - 7, 34, 13), border_radius=5)
        pygame.draw.circle(screen, eye, (x - 8, y - 1), 4)
        pygame.draw.circle(screen, eye, (x + 8, y - 1), 4)
        pygame.draw.line(screen, (180, 40, 45), (x - 7, y + 7), (x + 7, y + 7), 3)

        # shoulder lights
        pygame.draw.circle(screen, CYAN, (x - 21, y + 3), 3)
        pygame.draw.circle(screen, CYAN, (x + 21, y + 3), 3)

    # --------------------------------------------------------
    # HUNTER - fast floating alien drone
    # --------------------------------------------------------
    elif t == "HUNTER":
        c = BLUE
        dark = (20, 28, 50)
        wing = (90, 160, 255)
        float_y = int(y + bob * 3)

        # energy wings
        pygame.draw.polygon(screen, dark, [(x - 13, float_y - 3), (x - 43, float_y - 20), (x - 32, float_y + 8), (x - 12, float_y + 11)])
        pygame.draw.polygon(screen, dark, [(x + 13, float_y - 3), (x + 43, float_y - 20), (x + 32, float_y + 8), (x + 12, float_y + 11)])
        pygame.draw.line(screen, wing, (x - 17, float_y - 5), (x - 39, float_y - 18), 3)
        pygame.draw.line(screen, wing, (x + 17, float_y - 5), (x + 39, float_y - 18), 3)

        # body
        pygame.draw.polygon(screen, dark, [(x, float_y - 31), (x + 25, float_y - 3), (x + 13, float_y + 27), (x - 13, float_y + 27), (x - 25, float_y - 3)])
        pygame.draw.polygon(screen, c, [(x, float_y - 24), (x + 17, float_y - 2), (x + 8, float_y + 18), (x - 8, float_y + 18), (x - 17, float_y - 2)])
        pygame.draw.circle(screen, WHITE, (x, float_y - 1), 7)
        pygame.draw.circle(screen, c, (x, float_y - 1), 3)
        pygame.draw.line(screen, WHITE, (x - 8, float_y + 13), (x + 8, float_y + 13), 2)

    # --------------------------------------------------------
    # SPITTER - bio creature with acid sac
    # --------------------------------------------------------
    elif t == "SPITTER":
        shell = (58, 126, 76)
        dark = (27, 63, 41)
        acid = TOXIC

        bob_y = int(y + bob * 2)

        # rear legs / tendrils
        for side in (-1, 1):
            for off in (0, 9):
                pygame.draw.line(screen, dark, (x + side * (18 + off // 2), bob_y + 10), (x + side * (31 + off), bob_y + 23), 4)

        # outer shell
        pygame.draw.ellipse(screen, dark, (x - 34, bob_y - 27, 68, 54))
        pygame.draw.ellipse(screen, shell, (x - 29, bob_y - 23, 58, 46))

        # acid sacs
        pygame.draw.circle(screen, acid, (x - 15, bob_y + 5), 9)
        pygame.draw.circle(screen, acid, (x + 15, bob_y + 5), 9)
        pygame.draw.circle(screen, WHITE, (x - 17, bob_y + 2), 2)
        pygame.draw.circle(screen, WHITE, (x + 13, bob_y + 2), 2)

        # face
        pygame.draw.ellipse(screen, (15, 35, 22), (x - 18, bob_y - 15, 36, 23))
        pygame.draw.circle(screen, GREEN, (x - 8, bob_y - 6), 4)
        pygame.draw.circle(screen, GREEN, (x + 8, bob_y - 6), 4)
        pygame.draw.line(screen, acid, (x - 11, bob_y + 2), (x + 11, bob_y + 2), 4)
        pygame.draw.circle(screen, acid, (x, bob_y + 2), 2)

    # --------------------------------------------------------
    # SWARM - small alien insect
    # --------------------------------------------------------
    elif t == "SWARM":
        yy = int(y + bob * 4)
        wing = (255, 240, 120)

        pygame.draw.ellipse(screen, (65, 55, 25), (x - 10, yy - 13, 20, 28))
        pygame.draw.ellipse(screen, wing, (x - 20, yy - 15, 19, 12), 2)
        pygame.draw.ellipse(screen, wing, (x + 1, yy - 15, 19, 12), 2)

        for side in (-1, 1):
            pygame.draw.line(screen, (120, 90, 25), (x + side * 5, yy + 8), (x + side * 15, yy + 19), 3)
            pygame.draw.line(screen, (120, 90, 25), (x + side * 6, yy + 2), (x + side * 18, yy - 5), 3)

        pygame.draw.circle(screen, YELLOW, (x, yy - 4), 9)
        pygame.draw.circle(screen, RED, (x - 3, yy - 5), 2)
        pygame.draw.circle(screen, RED, (x + 3, yy - 5), 2)

    # --------------------------------------------------------
    # TANK - heavy six-legged alien
    # --------------------------------------------------------
    elif t == "TANK":
        armor = (82, 98, 110)
        dark = (34, 43, 50)
        glow = ORANGE

        # heavy legs
        for side in (-1, 1):
            pygame.draw.line(screen, dark, (x + side * 14, y + 10), (x + side * 36, y + 22), 8)
            pygame.draw.line(screen, dark, (x + side * 18, y - 2), (x + side * 42, y - 8), 7)
            pygame.draw.line(screen, dark, (x + side * 13, y + 16), (x + side * 25, y + 31), 6)

        # armor body
        pygame.draw.circle(screen, dark, (x, y), 38)
        pygame.draw.polygon(screen, armor, [(x - 28, y - 12), (x - 15, y - 29), (x + 15, y - 29), (x + 29, y - 12), (x + 24, y + 18), (x, y + 30), (x - 24, y + 18)])

        # cannon core
        pygame.draw.rect(screen, (42, 48, 54), (x - 14, y - 8, 28, 17), border_radius=4)
        pygame.draw.circle(screen, glow, (x, y), 8)
        pygame.draw.circle(screen, WHITE, (x, y), 3)

        # armor lights
        for sx in (-20, 20):
            pygame.draw.circle(screen, RED, (x + sx, y - 4), 3)

        # top plates
        pygame.draw.line(screen, WHITE, (x - 16, y - 23), (x + 16, y - 23), 2)

    # --------------------------------------------------------
    # PHANTOM - ghost with masked face and trailing energy
    # --------------------------------------------------------
    elif t == "PHANTOM":
        yy = int(y + bob * 3)
        c = PURPLE
        ghost = (82, 56, 108)
        dark = (31, 20, 45)

        # spectral tail
        pygame.draw.polygon(screen, dark, [(x - 26, yy + 6), (x - 16, yy + 29), (x - 5, yy + 18), (x, yy + 34), (x + 8, yy + 17), (x + 20, yy + 30), (x + 28, yy + 5)])
        pygame.draw.circle(screen, ghost, (x, yy - 5), 29)
        pygame.draw.circle(screen, c, (x, yy - 8), 22)

        # mask
        pygame.draw.polygon(screen, dark, [(x - 16, yy - 12), (x, yy - 22), (x + 16, yy - 12), (x + 12, yy + 8), (x, yy + 14), (x - 12, yy + 8)])
        pygame.draw.circle(screen, WHITE, (x - 7, yy - 3), 4)
        pygame.draw.circle(screen, WHITE, (x + 7, yy - 3), 4)
        pygame.draw.line(screen, c, (x - 8, yy + 8), (x + 8, yy + 8), 3)

        # orbiting shards
        for i in range(4):
            a = game_time * 1.5 + i * math.tau / 4
            sx = x + math.cos(a) * 38
            sy = yy + math.sin(a) * 32
            pygame.draw.polygon(screen, c, [(int(sx), int(sy - 4)), (int(sx + 4), int(sy)), (int(sx), int(sy + 4)), (int(sx - 4), int(sy))])

    # --------------------------------------------------------
    # VOID - miniature singularity
    # --------------------------------------------------------
    elif t == "VOID":
        spin = game_time * 1.8 + phase
        core = (8, 7, 14)

        # rotating accretion ring
        for i in range(3):
            a = spin + i * math.pi / 3
            rx = x + math.cos(a) * 28
            ry = y + math.sin(a) * 16
            pygame.draw.ellipse(screen, PURPLE, (int(rx - 26), int(ry - 8), 52, 16), 2)

        pygame.draw.circle(screen, (34, 18, 52), (x, y), 31 + int(pulse * 4))
        pygame.draw.circle(screen, PURPLE, (x, y), 24)
        pygame.draw.circle(screen, core, (x, y), 14)
        pygame.draw.circle(screen, WHITE, (x, y), 3)

        # gravitational sparks
        for i in range(6):
            a = -spin * 1.4 + i
            sx = x + math.cos(a) * (38 + i * 2)
            sy = y + math.sin(a) * (38 + i * 2)
            pygame.draw.circle(screen, PURPLE, (int(sx), int(sy)), 2)

    # --------------------------------------------------------
    # FROST - crystalline alien
    # --------------------------------------------------------
    elif t == "FROST":
        yy = int(y + bob * 1.5)
        dark = (44, 105, 125)

        # crystal limbs
        for sx in (-1, 1):
            pygame.draw.polygon(screen, dark, [(x + sx * 18, yy + 8), (x + sx * 34, yy + 24), (x + sx * 26, yy + 28), (x + sx * 10, yy + 14)])

        # body crystals
        pygame.draw.polygon(screen, dark, [(x, yy - 36), (x + 28, yy - 8), (x + 19, yy + 26), (x, yy + 34), (x - 19, yy + 26), (x - 28, yy - 8)])
        pygame.draw.polygon(screen, ICE, [(x, yy - 28), (x + 19, yy - 7), (x + 13, yy + 19), (x, yy + 26), (x - 13, yy + 19), (x - 19, yy - 7)])

        # face crystal
        pygame.draw.polygon(screen, WHITE, [(x, yy - 16), (x + 10, yy - 1), (x, yy + 10), (x - 10, yy - 1)])
        pygame.draw.circle(screen, BLUE, (x - 4, yy - 2), 3)
        pygame.draw.circle(screen, BLUE, (x + 4, yy - 2), 3)

        # ice sparks
        for i in range(4):
            a = -game_time * 1.3 + i * math.tau / 4
            sx = x + math.cos(a) * 42
            sy = yy + math.sin(a) * 38
            pygame.draw.line(screen, ICE, (int(sx), int(sy - 4)), (int(sx), int(sy + 4)), 2)

    # --------------------------------------------------------
    # GLITCH - broken digital creature
    # --------------------------------------------------------
    elif t == "GLITCH":
        shift = int(math.sin(game_time * 30 + phase) * 5)
        c1 = CYAN if int(game_time * 10 + phase) % 2 else RED
        c2 = PINK if int(game_time * 7 + phase) % 2 else BLUE

        # ghosted fragments
        pygame.draw.rect(screen, c1, (x - 29 + shift, y - 18, 17, 38), 2)
        pygame.draw.rect(screen, c2, (x + 12 - shift, y - 27, 18, 21), 2)
        pygame.draw.polygon(screen, (32, 35, 50), [(x - 22, y - 25), (x + 25, y - 18), (x + 18, y + 25), (x - 27, y + 17)])

        # core
        pygame.draw.rect(screen, WHITE, (x - 9, y - 9, 18, 18))
        pygame.draw.rect(screen, c1, (x - 5, y - 5, 10, 10))

        # scanline cuts
        for i in (-16, -4, 8, 20):
            pygame.draw.line(screen, c2, (x - 27, y + i), (x + 27, y + i), 2)

    # --------------------------------------------------------
    # OMEGA - boss with reactor core and orbiting nodes
    # --------------------------------------------------------
    elif t == "OMEGA":
        color = enemy.get("color", ORANGE)
        boss_phase = game_time * (1.4 if enemy.get("boss") else 1.0)
        outer = 54 if enemy.get("boss") else 43
        core_r = 34 if enemy.get("boss") else 29

        # energy halo
        pygame.draw.circle(screen, (55, 25, 20), (x, y), outer + int(pulse * 5))
        pygame.draw.circle(screen, (45, 18, 15), (x, y), outer - 7)

        # segmented armor
        pygame.draw.polygon(screen, color, [(x, y - core_r - 9), (x + core_r, y - 8), (x + 21, y + 28), (x, y + core_r + 9), (x - 21, y + 28), (x - core_r, y - 8)])
        pygame.draw.circle(screen, (255, 183, 55), (x, y), core_r - 5)
        pygame.draw.circle(screen, (255, 235, 150), (x, y), 13 if enemy.get("boss") else 11)
        pygame.draw.circle(screen, WHITE, (x, y), 5)

        # reactor seams
        for a in (0, math.pi / 2, math.pi, math.pi * 1.5):
            sx = x + math.cos(a) * (core_r + 1)
            sy = y + math.sin(a) * (core_r + 1)
            ex = x + math.cos(a) * (core_r + 16)
            ey = y + math.sin(a) * (core_r + 16)
            pygame.draw.line(screen, color, (int(sx), int(sy)), (int(ex), int(ey)), 4)

        # orbiting power nodes
        count = 6 if enemy.get("boss") else 4
        orbit = outer + 13
        for i in range(count):
            a = boss_phase * (1 if i % 2 == 0 else -1) + i * math.tau / count
            sx = x + math.cos(a) * orbit
            sy = y + math.sin(a) * orbit * 0.72
            pygame.draw.circle(screen, (18, 20, 24), (int(sx), int(sy)), 7)
            pygame.draw.circle(screen, color, (int(sx), int(sy)), 4)

        if enemy.get("boss"):
            pygame.draw.ellipse(screen, color, (x - 80, y - 40, 160, 80), 3)
            pygame.draw.ellipse(screen, WHITE, (x - 63, y - 30, 126, 60), 1)

    # final emergency fallback
    else:
        pygame.draw.circle(screen, WHITE, (x, y), r)

    # --------------------------------------------------------
    # HP BAR + BOSS LABEL
    # --------------------------------------------------------
    hp_ratio = clamp(enemy["hp"] / max(1, enemy["max_hp"]), 0, 1)
    bw = 64 if not enemy.get("boss") else 130
    bar_y = y - r - 17
    pygame.draw.rect(screen, (20, 23, 27), (x - bw // 2, bar_y, bw, 6), border_radius=3)
    pygame.draw.rect(screen, RED, (x - bw // 2, bar_y, int(bw * hp_ratio), 6), border_radius=3)

    if enemy.get("boss"):
        text(enemy.get("name", "BOSS"), x, y - 112, FONT_MED, enemy.get("color", ORANGE), center=True)

def draw_bullets():
    for b in bullets:
        radius = 6 if b["mode"] != "BLACK HOLE" else 9
        pygame.draw.circle(screen, b["color"], (int(b["x"]), int(b["y"])), radius)
        pygame.draw.circle(screen, WHITE, (int(b["x"]), int(b["y"])), 2)


def draw_enemy_projectiles():
    for p in enemy_projectiles:
        pygame.draw.circle(screen, RED, (int(p["x"]), int(p["y"])), 7)
        pygame.draw.circle(screen, WHITE, (int(p["x"]), int(p["y"])), 2)


def draw_pickups():
    for item in pickups:
        x = int(item["x"])
        y = int(item["y"] + math.sin(game_time * 5) * 5)
        color = {"CREDIT": YELLOW, "HEAL": GREEN, "ENERGY": CYAN, "OMEGA_CORE": ORANGE, "ARTIFACT": PINK}.get(item["type"], WHITE)
        pygame.draw.circle(screen, color, (x, y), 9)
        pygame.draw.circle(screen, WHITE, (x, y), 3)


def draw_particles():
    for p in particles:
        ratio = p["life"] / p["max_life"]
        size = max(1, int(p["size"] * ratio))
        pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), size)

# ============================================================
# BACKGROUNDS / HUB
# ============================================================


def draw_world_background():
    world = active_world()
    screen.fill(BG)
    grid = tuple(max(4, c // 9) for c in world["color"])
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, grid, (x, 95), (x, HEIGHT), 1)
    for y in range(105, HEIGHT, 40):
        pygame.draw.line(screen, grid, (0, y), (WIDTH, y), 1)
    if current_world == 2:
        for i in range(25):
            x = (i * 93) % WIDTH
            y = (i * 57 + int(game_time * 35)) % HEIGHT
            pygame.draw.circle(screen, TOXIC, (x, y), 2)
    elif current_world == 3:
        for i in range(12):
            x = i * 120 + 30
            pygame.draw.rect(screen, (30, 30, 45), (x, 130, 75, 145))
            pygame.draw.rect(screen, PINK, (x + 12, 148, 12, 25))
            pygame.draw.rect(screen, CYAN, (x + 40, 194, 12, 40))
    elif current_world == 4:
        for i in range(35):
            a = game_time * 0.4 + i
            x = WIDTH / 2 + math.cos(a) * (150 + i * 5)
            y = HEIGHT / 2 + math.sin(a) * (110 + i * 4)
            pygame.draw.circle(screen, PURPLE, (int(x), int(y)), 2)
    elif current_world == 5:
        for i in range(14):
            x = i * 95
            pygame.draw.line(screen, ICE, (x, 120), (x + 80, 200), 2)
    elif current_world in (6, 9):
        pygame.draw.circle(screen, world["color"], (WIDTH // 2, HEIGHT // 2), 240, 2)
        pygame.draw.circle(screen, world["color"], (WIDTH // 2, HEIGHT // 2), 175, 1)
    elif current_world == 7:
        for i in range(30):
            x = random.Random(i).randint(50, WIDTH - 50)
            y = random.Random(i + 50).randint(100, HEIGHT - 50)
            if i % 2 == 0:
                pygame.draw.rect(screen, CYAN, (x, y, 16, 5))
            else:
                pygame.draw.rect(screen, RED, (x, y, 5, 16))
    elif current_world == 8:
        # simple liminal walls
        for x in range(120, WIDTH, 190):
            pygame.draw.line(screen, (70, 63, 45), (x, 100), (x, HEIGHT), 5)
        for y in range(160, HEIGHT, 130):
            pygame.draw.line(screen, (70, 63, 45), (50, y), (WIDTH - 50, y), 3)
    for i in range(35):
        x = (i * 97 + int(game_time * 10)) % WIDTH
        y = (i * 53) % HEIGHT
        pygame.draw.circle(screen, world["color"], (x, y), 1)


def draw_hub_background():
    screen.fill((7, 12, 17))
    # garage floor
    for x in range(0, WIDTH, 50):
        pygame.draw.line(screen, (15, 24, 31), (x, 100), (x, HEIGHT), 1)
    for y in range(100, HEIGHT, 50):
        pygame.draw.line(screen, (15, 24, 31), (0, y), (WIDTH, y), 1)
    # ceiling lights
    for x in range(100, WIDTH, 190):
        pygame.draw.rect(screen, (20, 36, 43), (x, 105, 90, 8), border_radius=4)
        pygame.draw.line(screen, CYAN, (x + 10, 109), (x + 80, 109), 2)
    # central platform
    pygame.draw.ellipse(screen, (9, 18, 23), (470, 255, 340, 250))
    pygame.draw.ellipse(screen, CYAN, (470, 255, 340, 250), 4)
    pygame.draw.ellipse(screen, PURPLE, (495, 275, 290, 210), 2)
    pygame.draw.circle(screen, (15, 25, 32), (640, 385), 75)
    # title screen
    text("OMEGA GARAGE", WIDTH // 2, 120, FONT_HUGE, WHITE, center=True)
    text("MULTIVERSE COMMAND HUB", WIDTH // 2, 165, FONT, CYAN, center=True)
    # zones
    for zone in HUB_ZONES:
        pygame.draw.rect(screen, (12, 20, 27), zone["rect"], border_radius=12)
        pygame.draw.rect(screen, zone["color"], zone["rect"], 2, border_radius=12)
        text(zone["name"], zone["rect"].centerx, zone["rect"].centery, FONT_MED, zone["color"], center=True)
    # NPC marker
    pygame.draw.circle(screen, GREEN, (1030, 575), 22)
    pygame.draw.circle(screen, WHITE, (1030, 570), 4)
    # portal console
    pygame.draw.rect(screen, PANEL2, (560, 260, 160, 42), border_radius=8)
    pygame.draw.rect(screen, portal_color, (560, 260, 160, 42), 2, border_radius=8)
    text("PORTAL CORE", 640, 281, FONT_SMALL, portal_color, center=True)

# ============================================================
# HUD
# ============================================================


def draw_world_hud():
    world = active_world()
    pygame.draw.rect(screen, (6, 10, 14), (15, 15, WIDTH - 30, 72), border_radius=10)
    pygame.draw.rect(screen, world["color"], (15, 15, WIDTH - 30, 72), 2, border_radius=10)
    text("OMEGA MULTIVERSE", 30, 25, FONT_MED, world["color"])
    text(world["name"], 30, 56, FONT_SMALL, WHITE)
    text(f"LVL {player_level}", 270, 32, FONT, YELLOW)
    text(f"XP {player_xp}/{player_xp_needed}", 270, 58, FONT_SMALL, GRAY)
    text(f"WEAPON {current_weapon}", 430, 32, FONT, WEAPONS[current_weapon]["color"])
    text(f"MODE {current_gun_mode()}", 430, 58, FONT_SMALL, CYAN)
    text(f"CREDITS {coins}", 670, 32, FONT, YELLOW)
    text(f"KILLS {kills}", 840, 32, FONT, RED)
    text(f"CORES {omega_cores}", 940, 32, FONT, ORANGE)
    # bars
    pygame.draw.rect(screen, (25, 25, 30), (30, HEIGHT - 82, 250, 18), border_radius=5)
    pygame.draw.rect(screen, RED, (30, HEIGHT - 82, int(250 * clamp(player_hp / player_max_hp, 0, 1)), 18), border_radius=5)
    text(f"HP {max(0, int(player_hp))}/{player_max_hp}", 35, HEIGHT - 110, FONT_SMALL)
    pygame.draw.rect(screen, (25, 25, 30), (30, HEIGHT - 48, 250, 10), border_radius=5)
    pygame.draw.rect(screen, YELLOW, (30, HEIGHT - 48, int(250 * clamp(player_stamina / player_max_stamina, 0, 1)), 10), border_radius=5)
    pygame.draw.rect(screen, (25, 25, 30), (990, HEIGHT - 48, 240, 10), border_radius=5)
    pygame.draw.rect(screen, CYAN, (990, HEIGHT - 48, int(240 * clamp(player_energy / player_max_energy, 0, 1)), 10), border_radius=5)
    text(f"ENERGY {int(player_energy)}", 990, HEIGHT - 74, FONT_SMALL, CYAN)
    pygame.draw.rect(screen, (25, 25, 30), (990, HEIGHT - 82, 240, 10), border_radius=5)
    pygame.draw.rect(screen, portal_color, (990, HEIGHT - 82, int(240 * clamp(portal_energy / portal_max_energy, 0, 1)), 10), border_radius=5)
    text(f"PORTAL {int(portal_energy)}", 990, HEIGHT - 108, FONT_SMALL, portal_color)
    text(f"CHARACTER {character_display_name()}", WIDTH - 300, 55, FONT_SMALL, character_color())
    text("Z/X/V POWERS" if current_character else "NO CHARACTER / NO POWERS", 30, HEIGHT - 23, FONT_SMALL, character_color())
    controls = "WASD MOVE   LMB FIRE   R MODE   C CHARACTERS   SPACE DASH   SHIFT+P PORTAL   E MAP   I INVENTORY   K SKILLS   Q QUESTS   L STATS   B ARMORY   TAB LAB"
    text(controls, 165, HEIGHT - 23, FONT_SMALL, GRAY)
    if boss is not None:
        pygame.draw.rect(screen, (25, 10, 10), (350, 102, 580, 16), border_radius=7)
        pygame.draw.rect(screen, ORANGE, (350, 102, int(580 * clamp(boss["hp"] / boss["max_hp"], 0, 1)), 16), border_radius=7)
        text(boss.get("name", "BOSS"), 640, 128, FONT_MED, boss.get("color", ORANGE), center=True)
    draw_story_objective()


def draw_hub_hud():
    text(f"LEVEL {player_level}   CREDITS {coins}   CORES {omega_cores}   SHARDS {portal_shards}", 35, 25, FONT, WHITE)
    text(f"CHARACTER: {character_display_name()}", WIDTH - 320, 25, FONT_SMALL, character_color())
    draw_story_objective()
    text("WASD MOVE    E = PORTAL    C = CHARACTERS    Z/X/V = POWERS    I = INVENTORY    K = SKILLS", 35, HEIGHT - 42, FONT_SMALL, GRAY)
    text("Q = QUESTS    L = STATS    B = ARMORY    TAB = PORTAL LAB    N = NEXUS NPC    T = CHILL ROOM", 35, HEIGHT - 22, FONT_SMALL, GRAY)
    if portal_active:
        text("PORTAL CORE ONLINE - PRESS E", 640, 520, FONT_MED, portal_color, center=True)

# ============================================================
# CHILL ROOM / MINIGAMES
# ============================================================


def chill_set_message(message, seconds=2.0):
    global chill_message, chill_message_timer
    chill_message = message
    chill_message_timer = seconds


def chill_random_target():
    chill_target["x"] = random.randint(270, WIDTH - 270)
    chill_target["y"] = random.randint(250, HEIGHT - 150)
    chill_target["r"] = random.randint(18, 30)


def start_chill_game(game_name):
    global chill_game, chill_game_time, chill_score, chill_round
    global chill_sequence, chill_sequence_index, chill_holo_phase

    chill_game = game_name
    chill_game_time = 20.0
    chill_score = 0
    chill_round = 0
    chill_sequence_index = 0
    chill_sequence = []
    chill_holo_phase = 0.0

    if game_name == "TARGETS":
        chill_random_target()
        chill_set_message("TRAF 10 TARGETÓW", 2.0)
    elif game_name == "HACK":
        keys = ["W", "A", "S", "D"]
        chill_sequence = [random.choice(keys) for _ in range(6)]
        chill_set_message("SEKWENCJA PORTALU GOTOWA", 2.0)
    elif game_name == "HOLO":
        chill_random_target()
        chill_set_message("ŁAP HOLOGRAMY!", 2.0)


def finish_chill_game(success=True):
    global chill_game, chill_completed, coins, player_xp, chill_best

    if success:
        chill_completed += 1
        update_quest_progress("chill", 1)
        reward = 45 + chill_score * 5
        coins += reward
        add_xp(20 + chill_score * 3)
        chill_set_message(f"MINIGRA UKOŃCZONA  +{reward} C", 3.0)
        if chill_game in chill_best:
            chill_best[chill_game] = max(chill_best[chill_game], chill_score)
        add_particles(player_x, player_y, CYAN, 80, 6)
    else:
        chill_set_message("MINIGRA NIEUDANA — SPRÓBUJ JESZCZE RAZ", 2.2)
        add_particles(player_x, player_y, RED, 35, 4)
    chill_game = None
    save_game()


def leave_chill_room():
    global open_menu, chill_game
    chill_game = None
    open_menu = None
    save_game()


def handle_chill_key(key):
    global chill_sequence_index, chill_score, chill_game_time, chill_holo_phase, chill_game

    if chill_game is None:
        if key == pygame.K_1:
            start_chill_game("TARGETS")
        elif key == pygame.K_2:
            start_chill_game("HACK")
        elif key == pygame.K_3:
            start_chill_game("HOLO")
        elif key in (pygame.K_ESCAPE, pygame.K_t):
            leave_chill_room()
        return

    if key == pygame.K_ESCAPE:
        chill_game = None
        chill_set_message("WRÓCIŁEŚ DO LOUNGE", 1.5)
        return

    if chill_game == "HACK":
        names = {
            pygame.K_w: "W", pygame.K_a: "A",
            pygame.K_s: "S", pygame.K_d: "D",
        }
        pressed = names.get(key)
        if pressed is None:
            return
        if chill_sequence_index < len(chill_sequence) and pressed == chill_sequence[chill_sequence_index]:
            chill_sequence_index += 1
            chill_score = chill_sequence_index
            if chill_sequence_index >= len(chill_sequence):
                finish_chill_game(True)
        else:
            chill_sequence_index = 0
            chill_score = 0
            chill_game_time = max(0.0, chill_game_time - 2.0)
            chill_set_message("BŁĄD SEKWENCJI! RESET", 1.1)


def handle_chill_click(mx, my):
    global chill_score, chill_round

    if chill_game is None:
        buttons = [
            (pygame.Rect(205, 265, 260, 100), "TARGETS"),
            (pygame.Rect(510, 265, 260, 100), "HACK"),
            (pygame.Rect(815, 265, 260, 100), "HOLO"),
        ]
        for rect, game_name in buttons:
            if rect.collidepoint(mx, my):
                start_chill_game(game_name)
                return
        lounge_rect = pygame.Rect(360, 500, 560, 90)
        if lounge_rect.collidepoint(mx, my):
            chill_set_message("SIEDZISZ NA KANAPIE. SPOKOJNIE.", 2.0)
        return

    if chill_game in ("TARGETS", "HOLO"):
        x, y = chill_target["x"], chill_target["y"]
        r = chill_target["r"] + (5 if chill_game == "HOLO" else 0)
        if dist(mx, my, x, y) <= r:
            chill_score += 1
            chill_round += 1
            if chill_game == "TARGETS" and chill_score >= 10:
                finish_chill_game(True)
                return
            if chill_game == "HOLO" and chill_score >= 12:
                finish_chill_game(True)
                return
            chill_random_target()
            add_particles(x, y, CYAN if chill_game == "HOLO" else GREEN, 22, 4)


def update_chill(dt):
    global chill_game_time, chill_message_timer, chill_total_time, chill_lounge_coins_timer, chill_holo_phase

    if open_menu != "chill":
        return

    if chill_message_timer > 0:
        chill_message_timer -= dt

    if chill_game is None:
        chill_total_time += dt
        chill_lounge_coins_timer += dt
        update_quest_progress("lounge", dt)
        # Small reward for actually chilling in the lounge.
        if chill_lounge_coins_timer >= 6.0:
            chill_lounge_coins_timer = 0.0
            global coins
            coins += 5
            add_particles(640, 545, YELLOW, 12, 2)
        return

    chill_game_time -= dt
    chill_holo_phase += dt * 4.0

    if chill_game == "HOLO":
        # The hologram drifts around while you try to catch it.
        chill_target["x"] = int(chill_target["x"] + math.cos(chill_holo_phase * 1.7) * 0.55)
        chill_target["y"] = int(chill_target["y"] + math.sin(chill_holo_phase * 1.3) * 0.45)
        chill_target["x"] = int(clamp(chill_target["x"], 260, WIDTH - 260))
        chill_target["y"] = int(clamp(chill_target["y"], 240, HEIGHT - 170))

    if chill_game_time <= 0:
        finish_chill_game(False)


def draw_chill_room():
    screen.fill((7, 11, 18))

    # Chill-room neon walls
    pygame.draw.rect(screen, (12, 20, 28), (70, 90, WIDTH - 140, HEIGHT - 150), border_radius=24)
    pygame.draw.rect(screen, CYAN, (70, 90, WIDTH - 140, HEIGHT - 150), 2, border_radius=24)

    # ambient stars / LEDs
    for i in range(25):
        a = game_time * 0.2 + i
        x = 110 + int((i * 71) % (WIDTH - 220))
        y = 125 + int((math.sin(a) * 0.5 + 0.5) * 80)
        pygame.draw.circle(screen, (40, 90, 105), (x, y), 2)

    text("OMEGA CHILL ROOM", WIDTH // 2, 125, FONT_HUGE, CYAN, center=True)
    text("Nie każda chwila musi kończyć się walką.", WIDTH // 2, 175, FONT, GRAY, center=True)

    if chill_game is None:
        # Couch
        pygame.draw.rect(screen, (55, 40, 60), (405, 485, 470, 115), border_radius=25)
        pygame.draw.rect(screen, (80, 55, 90), (385, 455, 510, 70), border_radius=22)
        pygame.draw.circle(screen, PINK, (490, 485), 22)
        pygame.draw.circle(screen, PURPLE, (790, 485), 22)

        # tiny aquarium / hologram
        pygame.draw.rect(screen, (10, 25, 35), (105, 420, 180, 140), border_radius=12)
        pygame.draw.rect(screen, CYAN, (105, 420, 180, 140), 2, border_radius=12)
        for i in range(5):
            fx = 125 + ((i * 33 + int(game_time * (12 + i))) % 135)
            fy = 455 + int(math.sin(game_time * (1.5 + i * 0.2) + i) * 25)
            pygame.draw.circle(screen, CYAN if i % 2 else GREEN, (fx, fy), 4)

        buttons = [
            (pygame.Rect(205, 265, 260, 100), "1  TARGET RANGE", GREEN),
            (pygame.Rect(510, 265, 260, 100), "2  PORTAL HACK", PURPLE),
            (pygame.Rect(815, 265, 260, 100), "3  HOLO CATCH", PINK),
        ]
        for rect, label, color in buttons:
            pygame.draw.rect(screen, PANEL2, rect, border_radius=14)
            pygame.draw.rect(screen, color, rect, 3, border_radius=14)
            text(label, rect.centerx, rect.centery - 8, FONT_MED, color, center=True)
            text("MINIGRA", rect.centerx, rect.centery + 25, FONT_SMALL, GRAY, center=True)

        lounge_rect = pygame.Rect(360, 500, 560, 90)
        pygame.draw.rect(screen, (30, 37, 48), lounge_rect, border_radius=18)
        pygame.draw.rect(screen, YELLOW, lounge_rect, 2, border_radius=18)
        text("SIT / CHILL / LISTEN TO THE PORTAL HUM", lounge_rect.centerx, lounge_rect.centery, FONT, YELLOW, center=True)
        text(f"CHILL TIME: {int(chill_total_time)}s   COMPLETED: {chill_completed}", WIDTH // 2, 655, FONT_SMALL, WHITE, center=True)
        text("T / ESC = CLOSE", WIDTH // 2, 700, FONT_SMALL, GRAY, center=True)

    else:
        title = {"TARGETS": "TARGET RANGE", "HACK": "PORTAL HACK", "HOLO": "HOLO CATCH"}[chill_game]
        color = {"TARGETS": GREEN, "HACK": PURPLE, "HOLO": PINK}[chill_game]
        text(title, WIDTH // 2, 235, FONT_BIG, color, center=True)
        text(f"TIME {chill_game_time:04.1f}s", WIDTH // 2, 275, FONT_MED, YELLOW, center=True)
        text(f"SCORE {chill_score}", WIDTH // 2, 310, FONT, WHITE, center=True)

        if chill_game == "TARGETS":
            x, y, r = chill_target["x"], chill_target["y"], chill_target["r"]
            for ring in (r + 12, r, max(4, r // 2)):
                pygame.draw.circle(screen, GREEN, (x, y), ring, 3)
            pygame.draw.circle(screen, WHITE, (x, y), 4)
            text("KLIKNIJ WSZYSTKIE CELE", WIDTH // 2, 700, FONT, GREEN, center=True)

        elif chill_game == "HOLO":
            x, y, r = chill_target["x"], chill_target["y"], chill_target["r"] + 5
            pulse = int(math.sin(game_time * 8) * 6)
            pygame.draw.circle(screen, PINK, (x, y), r + pulse, 3)
            pygame.draw.circle(screen, CYAN, (x, y), r + 16 + pulse, 2)
            pygame.draw.line(screen, WHITE, (x - r, y), (x + r, y), 2)
            pygame.draw.line(screen, WHITE, (x, y - r), (x, y + r), 2)
            text("ZŁAP 12 RUCHOMYCH HOLOGRAMÓW", WIDTH // 2, 700, FONT, PINK, center=True)

        else:
            seq = " ".join(chill_sequence)
            progress = chill_sequence_index
            text("SEQUENCE:", WIDTH // 2, 355, FONT, WHITE, center=True)
            text(seq, WIDTH // 2, 395, FONT_BIG, PURPLE, center=True)
            text(f"POSTĘP: {progress}/{len(chill_sequence)}", WIDTH // 2, 445, FONT_MED, CYAN, center=True)
            if progress < len(chill_sequence):
                text(f"NASTĘPNY KLAWISZ: {chill_sequence[progress]}", WIDTH // 2, 505, FONT_BIG, YELLOW, center=True)
            text("WCISKAJ W / A / S / D", WIDTH // 2, 700, FONT, PURPLE, center=True)

    if chill_message_timer > 0:
        text(chill_message, WIDTH // 2, 735, FONT_MED, YELLOW, center=True)

    # best scores
    text(f"BEST  TARGETS {chill_best['TARGETS']}   HACK {chill_best['HACK']}   HOLO {chill_best['HOLO']}", WIDTH // 2, 765, FONT_SMALL, GRAY, center=True)

# ============================================================
# HUB INTERACTIONS
# ============================================================


def nearest_hub_menu():
    center = pygame.Vector2(player_x, player_y)
    best = None
    best_d = 99999
    for zone in HUB_ZONES:
        d = center.distance_to(zone["rect"].center)
        if d < best_d:
            best_d = d
            best = zone
    if best_d < 200:
        return best
    return None

# ============================================================
# INPUT HANDLERS
# ============================================================


def handle_armory_click(mx, my):
    global coins, current_weapon
    y = 165
    for name, data in WEAPONS.items():
        card = pygame.Rect(245, y, 790, 92)
        if card.collidepoint(mx, my):
            if name not in owned_weapons:
                if coins >= data["price"]:
                    coins -= data["price"]
                    owned_weapons.append(name)
                    current_weapon = name
                    save_game()
            else:
                current_weapon = name
                # upgrade click is handled by right side sub-area
                if mx >= 900:
                    cost = 150 * weapon_levels[name]
                    if coins >= cost:
                        coins -= cost
                        weapon_levels[name] += 1
                        save_game()
                else:
                    save_game()
            return
        y += 105


def handle_skill_click(mx, my):
    names = ["VITALITY", "ENERGY", "DASH", "WEAPON", "PORTAL", "LOOT"]
    for i, name in enumerate(names):
        col = i % 3
        row = i // 3
        card = pygame.Rect(280 + col * 245, 190 + row * 200, 210, 150)
        if card.collidepoint(mx, my):
            upgrade_skill(name)
            return


def handle_quest_click(mx, my):
    row_h = 108
    gap = 12
    start_y = 145
    for i in range(len(quests)):
        y = start_y + i * (row_h + gap)
        card = pygame.Rect(220, y, 840, row_h)
        if card.collidepoint(mx, my):
            claim_quest(i)
            return


def handle_lab_click(mx, my):
    global portal_color_name, portal_color
    names = list(PORTAL_COLORS.keys())
    for i, name in enumerate(names):
        col = i % 4
        row = i // 4
        rect = pygame.Rect(300 + col * 165, 240 + row * 120, 135, 90)
        if rect.collidepoint(mx, my):
            portal_color_name = name
            portal_color = PORTAL_COLORS[name]
            save_game()
            return


def handle_dimension_click(mx, my):
    for i, world in enumerate(WORLD_DEFS):
        col = i % 3
        row = i // 3
        rect = pygame.Rect(175 + col * 325, 135 + row * 112, 290, 92)
        if rect.collidepoint(mx, my) and is_world_unlocked(i):
            travel_to(i)
            return

# ============================================================
# MAIN LOOP
# ============================================================

load_game()
game_time = 0.0
if not story_intro_seen and not ending_complete:
    start_story_intro()
running = True

while running:
    dt = clock.tick(FPS) / 1000.0
    game_time += dt
    time_scale = 0.35 if time_glitch_timer > 0 else 1.0
    world_dt = dt * time_scale

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False

        if event.type == pygame.KEYDOWN:
            key = event.key

            # Story dialogue has priority over every other control.
            if story_dialogue_active:
                if key in (pygame.K_SPACE, pygame.K_RETURN):
                    advance_dialogue()
                continue

            # Final decision / ending screen.
            if ending_choice_active:
                if key == pygame.K_1:
                    choose_ending(1)
                elif key == pygame.K_2:
                    choose_ending(2)
                continue

            if ending_complete:
                if key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    ending_complete = False
                    save_game()
                continue

            if open_menu == "chill" and mode == "HUB":
                handle_chill_key(key)
                continue

            if key == pygame.K_f and mode == "HUB" and open_menu is None:
                zone = nearest_hub_menu()
                if zone and zone["name"] == "NEXUS NPC":
                    if story_chapter <= 1:
                        start_dialogue([
                            "The portal core is listening.",
                            "Every boss carries a piece of the corrupted signal.",
                            "Bring me a core and I can decode the next location."
                        ], speaker="NEXUS", color=GREEN, title="NEXUS // FIELD REPORT")
                    else:
                        start_dialogue([
                            f"Current objective: {story_objective()}",
                            f"Bosses defeated: {bosses_defeated}",
                            f"Artifacts recovered: {artifacts}",
                            "The final coordinate is waiting for you."
                        ], speaker="NEXUS", color=GREEN, title="NEXUS // CURRENT STATUS")
                continue

            if key == pygame.K_t and mode == "HUB" and open_menu is None:
                open_menu = "chill"
                chill_game = None
                chill_set_message("WITAJ W OMEGA CHILL ROOM", 2.0)

            elif key == pygame.K_ESCAPE:
                open_menu = None

            elif key == pygame.K_i:
                open_menu = None if open_menu == "inventory" else "inventory"

            elif key == pygame.K_k:
                open_menu = None if open_menu == "skills" else "skills"

            elif key == pygame.K_q:
                open_menu = None if open_menu == "quests" else "quests"

            elif key == pygame.K_l:
                open_menu = None if open_menu == "stats" else "stats"

            elif key == pygame.K_b:
                open_menu = None if open_menu == "armory" else "armory"

            elif key == pygame.K_TAB:
                open_menu = None if open_menu == "lab" else "lab"

            elif key == pygame.K_n:
                open_menu = None if open_menu == "npc" else "npc"

            elif key == pygame.K_c:
                open_menu = None if open_menu == "characters" else "characters"

            elif key in (pygame.K_z, pygame.K_x, pygame.K_v) and open_menu is None:
                slot = {pygame.K_z: "Z", pygame.K_x: "X", pygame.K_v: "V"}[key]
                use_character_ability(slot)

            elif key == pygame.K_r and open_menu is None:
                cycle_gun_mode()

            elif key == pygame.K_SPACE and open_menu is None and mode == "WORLD":
                perform_dash()

            elif key == pygame.K_h and open_menu is None and mode == "WORLD":
                if potions > 0 and player_hp < player_max_hp:
                    potions -= 1
                    player_hp = min(player_max_hp, player_hp + 35)
                    add_particles(player_x, player_y, GREEN, 20, 3)

            elif key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_SHIFT and mode == "WORLD" and open_menu is None:
                activate_portal()

            elif key == pygame.K_e and open_menu is None:
                if mode == "HUB":
                    # activate only near center portal
                    if dist(player_x, player_y, portal_x, portal_y) < 190:
                        if not portal_active:
                            activate_portal()
                        else:
                            open_menu = "dimensions"
                else:
                    if portal_active:
                        open_menu = "dimensions"

            elif key == pygame.K_m:
                if open_menu == "dimensions":
                    open_menu = None
                else:
                    open_menu = "dimensions"

            elif open_menu == "dimensions":
                mapping = {
                    pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3,
                    pygame.K_5: 4, pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7,
                    pygame.K_9: 8, pygame.K_0: 9,
                }
                if key in mapping and is_world_unlocked(mapping[key]):
                    travel_to(mapping[key])

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if story_dialogue_active:
                advance_dialogue()
                continue
            if ending_choice_active:
                if my < HEIGHT // 2:
                    choose_ending(1)
                else:
                    choose_ending(2)
                continue
            if ending_complete:
                ending_complete = False
                save_game()
                continue
            if open_menu == "armory":
                handle_armory_click(mx, my)
            elif open_menu == "skills":
                handle_skill_click(mx, my)
            elif open_menu == "quests":
                handle_quest_click(mx, my)
            elif open_menu == "lab":
                handle_lab_click(mx, my)
            elif open_menu == "dimensions":
                handle_dimension_click(mx, my)
            elif open_menu == "characters":
                handle_character_click(mx, my)
            elif open_menu == "chill":
                handle_chill_click(mx, my)
            elif open_menu is None and mode == "WORLD":
                shoot()

    # --------------------------------------------------------
    # MOVEMENT
    # --------------------------------------------------------
    if open_menu is None and not story_dialogue_active and not ending_choice_active and not ending_complete:
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        dy = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if dx or dy:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length
            player_x += dx * player_speed * 60 * dt
            player_y += dy * player_speed * 60 * dt
            player_stamina -= 8 * dt
        else:
            player_stamina += 22 * dt

        if mode == "HUB":
            player_x = clamp(player_x, 35, WIDTH - 35)
            player_y = clamp(player_y, 130, HEIGHT - 70)
        else:
            player_x = clamp(player_x, 45, WIDTH - 45)
            player_y = clamp(player_y, 110, HEIGHT - 80)

    player_stamina = clamp(player_stamina, 0, player_max_stamina)
    player_energy = min(player_max_energy, player_energy + (11 + skills["ENERGY"] * 2) * dt)
    portal_energy = min(portal_max_energy, portal_energy + (4 + skills["PORTAL"]) * dt)

    if dash_cooldown > 0:
        dash_cooldown -= dt
    if time_glitch_timer > 0:
        time_glitch_timer -= dt
    if damage_flash > 0:
        damage_flash -= dt
    if screen_shake > 0:
        screen_shake -= 18 * dt
    if save_flash > 0:
        save_flash -= dt
    if random_event_display > 0:
        random_event_display -= dt

    # --------------------------------------------------------
    # HOLD LMB SHOOT
    # --------------------------------------------------------
    if mode == "WORLD" and open_menu is None and not story_dialogue_active and not ending_choice_active and not ending_complete and pygame.mouse.get_pressed()[0]:
        shoot()

    # --------------------------------------------------------
    # WORLD UPDATE
    # --------------------------------------------------------
    if mode == "WORLD" and open_menu is None and not story_dialogue_active and not ending_choice_active and not ending_complete:
        world_time += world_dt
        random_event_timer -= world_dt
        enemy_spawn_timer -= world_dt

        if random_event_timer <= 0:
            trigger_random_event()

        max_enemies = 5 + min(8, current_world)
        if current_world == 6 or current_world == 9:
            max_enemies = 7

        if enemy_spawn_timer <= 0 and len(enemies) < max_enemies and boss is None:
            spawn_enemy()
            enemy_spawn_timer = max(0.55, 1.8 - current_world * 0.12)

        # Boss trigger after 8 kills in hard worlds
        if current_world in BOSS_DEFS and boss is None and world_kills >= 8:
            spawn_boss()

        update_enemies(world_dt)
        update_enemy_projectiles(world_dt)
        update_bullets(world_dt)
        update_pickups()

        if player_hp <= 0:
            reset_player()

    update_story_state()
    update_character_system(dt)
    update_chill(dt)
    update_particles(dt)
    autosave(dt)

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------
    if mode == "HUB":
        draw_hub_background()
        # Portal in hub
        portal_active_temp = portal_active
        # draw player and portal always
        draw_portal()
        draw_character_fx()
        draw_particles()
        draw_player()
        draw_hub_hud()
        if open_menu == "inventory":
            draw_inventory()
        elif open_menu == "skills":
            draw_skills()
        elif open_menu == "quests":
            draw_quests()
        elif open_menu == "stats":
            draw_stats()
        elif open_menu == "armory":
            draw_armory()
        elif open_menu == "lab":
            draw_portal_lab()
        elif open_menu == "dimensions":
            draw_dimension_menu()
        elif open_menu == "npc":
            draw_npc()
        elif open_menu == "characters":
            draw_character_menu()
        elif open_menu == "chill":
            draw_chill_room()
    else:
        draw_world_background()
        draw_portal()
        draw_pickups()
        draw_enemy_projectiles()
        draw_bullets()
        for enemy in enemies:
            draw_enemy(enemy)
        if boss is not None:
            draw_enemy(boss)
        draw_turrets()
        draw_character_fx()
        draw_particles()
        draw_player()
        draw_world_hud()
        if open_menu == "inventory":
            draw_inventory()
        elif open_menu == "skills":
            draw_skills()
        elif open_menu == "quests":
            draw_quests()
        elif open_menu == "stats":
            draw_stats()
        elif open_menu == "armory":
            draw_armory()
        elif open_menu == "lab":
            draw_portal_lab()
        elif open_menu == "dimensions":
            draw_dimension_menu()
        elif open_menu == "npc":
            draw_npc()
        elif open_menu == "characters":
            draw_character_menu()

    if random_event_display > 0:
        text(random_event_text, WIDTH // 2, 130, FONT_MED, random_event_color, center=True)

    if save_flash > 0:
        text("GAME SAVED", WIDTH - 95, 25, FONT_SMALL, GREEN, center=True)

    if damage_flash > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 30, 40, 42))
        screen.blit(overlay, (0, 0))

    if story_dialogue_active:
        draw_dialogue_overlay()
    if ending_choice_active or ending_complete:
        draw_ending_overlay()

    pygame.display.flip()

pygame.quit()
sys.exit()
