
import pygame
import math
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Solar System - Science Exhibition")

clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("Arial", 30, bold=True)
font = pygame.font.SysFont("Arial", 20, bold=True)
small_font = pygame.font.SysFont("Arial", 15)

# Colors
BLACK = (5, 5, 25)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
PANEL = (20, 25, 55)
GREY = (80, 90, 120)

# Star background
random.seed(10)
stars = [
    (random.randint(0, WIDTH), random.randint(0, HEIGHT),
     random.randint(1, 2))
    for _ in range(180)
]

# Planet information
planet_data = [
    {
        "name": "Mercury", "orbit": 65, "radius": 5,
        "color": (180, 180, 180), "speed": 1.60,
        "fact": "Closest planet to the Sun.",
        "distance": "57.9 million km",
        "year": "88 Earth days"
    },
    {
        "name": "Venus", "orbit": 105, "radius": 9,
        "color": (240, 180, 90), "speed": 1.15,
        "fact": "The hottest planet in our solar system.",
        "distance": "108.2 million km",
        "year": "225 Earth days"
    },
    {
        "name": "Earth", "orbit": 145, "radius": 10,
        "color": (50, 140, 255), "speed": 0.90,
        "fact": "Our home planet. Known to support life.",
        "distance": "149.6 million km",
        "year": "365 days"
    },
    {
        "name": "Mars", "orbit": 185, "radius": 7,
        "color": (240, 80, 55), "speed": 0.72,
        "fact": "Known as the Red Planet.",
        "distance": "227.9 million km",
        "year": "687 Earth days"
    },
    {
        "name": "Jupiter", "orbit": 240, "radius": 17,
        "color": (215, 165, 120), "speed": 0.48,
        "fact": "The largest planet in our solar system.",
        "distance": "778.6 million km",
        "year": "11.86 Earth years"
    },
    {
        "name": "Saturn", "orbit": 295, "radius": 14,
        "color": (235, 210, 145), "speed": 0.36,
        "fact": "Famous for its spectacular ring system.",
        "distance": "1.43 billion km",
        "year": "29.45 Earth years"
    },
    {
        "name": "Uranus", "orbit": 345, "radius": 11,
        "color": (100, 220, 220), "speed": 0.25,
        "fact": "An ice giant that rotates on its side.",
        "distance": "2.87 billion km",
        "year": "84 Earth years"
    },
    {
        "name": "Neptune", "orbit": 390, "radius": 11,
        "color": (75, 100, 255), "speed": 0.19,
        "fact": "The farthest planet from the Sun.",
        "distance": "4.50 billion km",
        "year": "165 Earth years"
    }
]

# Initial planet positions
for planet in planet_data:
    planet["angle"] = random.uniform(0, math.tau)
    planet["position"] = (0, 0)

# Layout
SUN_X, SUN_Y = 470, 410
PANEL_X = 900

paused = False
speed_multiplier = 1.0
selected_planet = None
show_orbits = True
running = True


def draw_text(text, x, y, color=WHITE, font_obj=small_font):
    surface = font_obj.render(text, True, color)
    screen.blit(surface, (x, y))


while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                speed_multiplier = min(5.0, speed_multiplier + 0.25)
            elif event.key == pygame.K_DOWN:
                speed_multiplier = max(0.25, speed_multiplier - 0.25)
            elif event.key == pygame.K_o:
                show_orbits = not show_orbits
            elif event.key == pygame.K_r:
                selected_planet = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            selected_planet = None

            # Select a planet by clicking near it
            for planet in reversed(planet_data):
                px, py = planet["position"]
                hit_radius = max(planet["radius"] + 8, 14)

                if math.hypot(mouse_x - px, mouse_y - py) < hit_radius:
                    selected_planet = planet
                    break

    # Background
    screen.fill(BLACK)

    for sx, sy, size in stars:
        pygame.draw.circle(screen, WHITE, (sx, sy), size)

    # Title
    draw_text(
        "INTERACTIVE SOLAR SYSTEM",
        25, 20, YELLOW, title_font
    )

    draw_text(
        "Explore our Sun and eight planets",
        28, 60, WHITE, small_font
    )

    # Orbits
    if show_orbits:
        for planet in planet_data:
            pygame.draw.circle(
                screen, GREY,
                (SUN_X, SUN_Y),
                planet["orbit"], 1
            )

    # Sun glow
    for glow_radius in range(42, 25, -4):
        pygame.draw.circle(
            screen, (100, 65, 15),
            (SUN_X, SUN_Y), glow_radius
        )

    pygame.draw.circle(screen, (255, 130, 0), (SUN_X, SUN_Y), 25)
    pygame.draw.circle(screen, YELLOW, (SUN_X, SUN_Y), 19)
    draw_text("SUN", SUN_X - 17, SUN_Y + 32, YELLOW, font)

    # Move and draw planets
    for planet in planet_data:
        if not paused:
            planet["angle"] += (
                planet["speed"] * speed_multiplier * 0.01
            )

        orbit = planet["orbit"]
        angle = planet["angle"]

        px = int(SUN_X + orbit * math.cos(angle))
        py = int(SUN_Y + orbit * math.sin(angle))

        planet["position"] = (px, py)

        radius = planet["radius"]
        color = planet["color"]

        # Saturn's rings behind its planet
        if planet["name"] == "Saturn":
            pygame.draw.ellipse(
                screen, (190, 170, 120),
                (px - 23, py - 7, 46, 14), 2
            )

        pygame.draw.circle(screen, color, (px, py), radius)

        # Earth-like highlight
        pygame.draw.circle(
            screen,
            tuple(min(255, c + 35) for c in color),
            (px - max(1, radius // 3), py - max(1, radius // 3)),
            max(2, radius // 3)
        )

        # Planet name
        draw_text(
            planet["name"],
            px + radius + 5,
            py - 9,
            WHITE,
            small_font
        )

        # Highlight selected planet
        if selected_planet is planet:
            pygame.draw.circle(
                screen, YELLOW, (px, py), radius + 6, 2
            )

    # Information panel
    pygame.draw.rect(
        screen, PANEL,
        (PANEL_X, 105, 275, 450),
        border_radius=15
    )

    draw_text("PLANET EXPLORER", PANEL_X + 18, 125, YELLOW, font)

    if selected_planet:
        p = selected_planet
        draw_text(p["name"], PANEL_X + 18, 175, p["color"], title_font)
        draw_text("Quick fact:", PANEL_X + 18, 225, YELLOW, font)
        draw_text(p["fact"], PANEL_X + 18, 260, WHITE, small_font)
        draw_text("Average distance from Sun:", PANEL_X + 18, 325)
        draw_text(p["distance"], PANEL_X + 18, 350, YELLOW, font)
        draw_text("One orbit around the Sun:", PANEL_X + 18, 405)
        draw_text(p["year"], PANEL_X + 18, 430, YELLOW, font)
        draw_text("Press R to deselect", PANEL_X + 18, 500)
    else:
        draw_text("Click a planet", PANEL_X + 18, 185, YELLOW, font)
        draw_text("to discover facts!", PANEL_X + 18, 215, WHITE, font)
        draw_text("Mercury: closest planet", PANEL_X + 18, 285)
        draw_text("Venus: hottest planet", PANEL_X + 18, 320)
        draw_text("Earth: home of life", PANEL_X + 18, 355)
        draw_text("Jupiter: largest planet", PANEL_X + 18, 390)
        draw_text("Neptune: farthest planet", PANEL_X + 18, 425)

    # Controls panel
    pygame.draw.rect(
        screen, PANEL,
        (PANEL_X, 580, 275, 145),
        border_radius=15
    )

    draw_text("CONTROLS", PANEL_X + 18, 595, YELLOW, font)
    draw_text("SPACE - Pause / Resume", PANEL_X + 18, 628)
    draw_text("UP / DOWN - Speed", PANEL_X + 18, 653)
    draw_text("O - Toggle orbit paths", PANEL_X + 18, 678)
    draw_text("ESC - Exit", PANEL_X + 18, 703)

    # Status bar
    status = "PAUSED" if paused else "RUNNING"
    draw_text(
        f"Simulation: {status}",
        25, 740, YELLOW, font
    )
    draw_text(
        f"Speed: {speed_multiplier:.2f}x",
        250, 740, WHITE, font
    )
    draw_text(
        "Educational simulation - distances and sizes not to scale",
        450, 744, WHITE, small_font
    )

    pygame.display.flip()

pygame.quit()
