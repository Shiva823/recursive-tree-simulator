import pygame
import math
import random
import pygame_gui
import time
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌳 Advanced Recursive Tree Simulator")

# Colors
SKY_BLUE = (135, 206, 235)
BROWN = (101, 67, 33)
GREEN = (34, 139, 34)
NIGHT_SKY = (25, 25, 112)
SUNSET_SKY = (255, 99, 71)

# Leaf colors for different seasons
SPRING_LEAVES = [(144, 238, 144), (152, 251, 152), (124, 252, 0), (173, 255, 47), (186, 255, 201)]
SUMMER_LEAVES = [(34, 139, 34), (0, 128, 0), (0, 100, 0), (46, 139, 87), (60, 179, 113)]
AUTUMN_LEAVES = [(255, 140, 0), (255, 69, 0), (255, 99, 71), (178, 34, 34), (139, 69, 19), (205, 92, 0)]
SNOW_COLORS = [(255, 255, 255), (240, 248, 255), (230, 230, 250)]

# Flower colors for ground
FLOWER_COLORS = [(255, 182, 193), (255, 105, 180), (238, 130, 238), (255, 255, 0), (255, 165, 0)]

class FallingLeaf:
    def __init__(self, x, y, color, wind_strength=0):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(4, 8)
        self.speed_y = random.uniform(0.3, 0.8)  # Much slower falling
        self.speed_x = random.uniform(-0.1, 0.1)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-0.5, 0.5)  # Slow gentle rotation
        self.wind_strength = wind_strength
        self.wobble_offset = random.uniform(0, math.pi * 2)
        self.time = 0
    
    def update(self, wind_strength):
        self.time += 0.03  # Slower time progression
        self.y += self.speed_y
        # Gentle horizontal drift with subtle wind effect
        self.x += self.speed_x + wind_strength * 0.15 + math.sin(self.time + self.wobble_offset) * 0.15
        self.rotation += self.rotation_speed
        
        # Very subtle natural wobble
        self.speed_x += random.uniform(-0.01, 0.01)
        self.speed_x = max(-0.4, min(0.4, self.speed_x))
    
    def draw(self, screen):
        # Draw leaf as a rotated ellipse shape
        points = []
        for i in range(6):
            angle = self.rotation + i * 60
            rad = math.radians(angle)
            rx = self.size if i % 2 == 0 else self.size * 0.5
            ry = self.size * 0.6 if i % 2 == 0 else self.size * 0.3
            px = self.x + rx * math.cos(rad)
            py = self.y + ry * math.sin(rad)
            points.append((px, py))
        if len(points) >= 3:
            pygame.draw.polygon(screen, self.color, points)
    
    def is_off_screen(self, height, width):
        return self.y > height or self.x < -50 or self.x > width + 50

class Snowflake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.speed_y = random.uniform(0.5, 1.5)
        self.wobble = random.uniform(0, math.pi * 2)
        self.wobble_speed = random.uniform(0.02, 0.05)
    
    def update(self, wind_strength):
        self.y += self.speed_y
        self.wobble += self.wobble_speed
        self.x += math.sin(self.wobble) * 0.5 + wind_strength * 0.3
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size)
    
    def is_off_screen(self, height):
        return self.y > height

class Tree:
    def __init__(self, x, y, trunk_length=120, seed=None):
        self.x = x
        self.y = y
        self.trunk_length = trunk_length
        self.seed = seed if seed else random.randint(0, 10000)
        self.growth = 0
        self.growing = True
        self.branch_cache = []
        self.leaf_positions = []
        self.snow_positions = []
    
    def reset_growth(self):
        self.growth = 0
        self.growing = True
        self.branch_cache = []
        self.leaf_positions = []
        self.snow_positions = []

class Grass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = random.randint(8, 20)
        self.color = random.choice([(34, 139, 34), (50, 205, 50), (0, 128, 0), (60, 179, 113)])
        self.sway_offset = random.uniform(0, math.pi * 2)
        self.sway_speed = random.uniform(0.03, 0.08)

class Flower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(FLOWER_COLORS)
        self.size = random.randint(4, 8)
        self.petal_count = random.randint(5, 8)
        self.sway_offset = random.uniform(0, math.pi * 2)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Season control
current_season = "spring"
target_season = "spring"
season_transition = 0  # 0 to 1 for smooth transition

# Wind simulation
wind_strength = 0
wind_target = 0
wind_time = 0

# Growth animation
growth_speed = 0.05

# Falling particles
falling_leaves = []
snowflakes = []

# Multiple trees
trees = [Tree(WIDTH // 2, HEIGHT - 100, 120)]

# Ground vegetation
grass_blades = []
flowers = []

def generate_ground_vegetation():
    global grass_blades, flowers
    grass_blades = [Grass(random.randint(0, WIDTH), HEIGHT - 100 + random.randint(0, 10)) for _ in range(150)]
    flowers = [Flower(random.randint(0, WIDTH), HEIGHT - 95 + random.randint(0, 15)) for _ in range(30)]

generate_ground_vegetation()

# GUI Manager for sliders
ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Tree parameters (adjustable)
branch_angle = math.pi / 6  # Default: 30 degrees
branch_length_ratio = 0.67
trunk_length = 120
recursion_depth = 10
asymmetry = 0.15  # Branch randomness
leaf_colors = SPRING_LEAVES
show_leaves = True
bg_color = (135, 206, 235)
target_bg_color = (135, 206, 235)

def lerp_color(c1, c2, t):
    """Linearly interpolate between two colors"""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_leaf_shape(screen, x, y, size, color, rotation):
    """Draw a realistic leaf shape"""
    points = []
    # Create leaf shape with bezier-like curve
    for i in range(8):
        angle = rotation + i * 45
        rad = math.radians(angle)
        # Vary radius to create leaf shape
        if i in [0, 4]:
            r = size * 1.5
        elif i in [2, 6]:
            r = size * 0.4
        else:
            r = size * 0.8
        px = x + r * math.cos(rad)
        py = y + r * math.sin(rad)
        points.append((px, py))
    if len(points) >= 3:
        pygame.draw.polygon(screen, color, points)
        # Add vein
        darker = tuple(max(0, c - 30) for c in color)
        pygame.draw.line(screen, darker, (x - size, y), (x + size, y), 1)

def draw_branch_animated(surface, x, y, length, angle, current_depth, branch_thickness, 
                         leaf_colors, show_leaves, max_depth_to_draw, original_depth, 
                         wind_offset=0, tree_seed=0, collect_leaves=None, collect_snow=None):
    """
    Draws tree with growth animation, wind, and asymmetric branches
    """
    if current_depth <= 0:
        return
    
    # Calculate what "level" we're at (1 = trunk, 2 = first branches, etc.)
    current_level = original_depth - current_depth + 1
    
    # Only draw if animation has reached this level
    if current_level > max_depth_to_draw:
        return
    
    # Use seed for consistent randomness per tree
    random.seed(tree_seed + current_depth * 1000 + int(x * 100))
    
    # Add wind sway - very subtle effect on thinner branches
    wind_sway = wind_offset * (1 - branch_thickness / 15) * 0.015
    swayed_angle = angle + wind_sway
    
    # Add asymmetry for natural look
    asymmetry_offset = random.uniform(-asymmetry, asymmetry)
    
    # Calculate end point of the branch with sway
    end_x = x + length * math.cos(swayed_angle)
    end_y = y + length * math.sin(swayed_angle)
    
    # Choose branch color with slight variation
    base_brown = random.randint(90, 110)
    if branch_thickness > 5:
        branch_color = (base_brown, base_brown - 30, base_brown - 60)
    else:
        branch_color = (139, 90 + random.randint(-10, 10), 43)
    
    # Draw the branch with rounded ends for thicker branches
    thickness = max(1, int(branch_thickness))
    pygame.draw.line(surface, branch_color, (x, y), (end_x, end_y), thickness)
    
    # Add bark texture for thick branches
    if branch_thickness > 8:
        for _ in range(2):
            tx = x + random.uniform(0, end_x - x)
            ty = y + random.uniform(0, end_y - y)
            pygame.draw.circle(surface, (80, 50, 20), (int(tx), int(ty)), 2)
    
    # Draw leaves at the end of small branches
    if current_depth <= 3 and show_leaves:
        if leaf_colors:
            leaf_color = random.choice(leaf_colors)
            leaf_size = random.randint(5, 10)
            # Use seed-based rotation so leaves don't move constantly
            rotation = random.uniform(0, 360) + wind_offset * 0.5
            draw_leaf_shape(surface, end_x, end_y, leaf_size, leaf_color, rotation)
            
            # Collect leaf positions for falling effect
            if collect_leaves is not None and random.random() < 0.3:
                collect_leaves.append((end_x, end_y))
        
        # Store snow positions for winter
        if collect_snow is not None and current_season == "winter":
            if random.random() < 0.4:
                collect_snow.append((end_x, end_y - 3))
    
    # Draw snow accumulation on branches in winter
    if current_season == "winter" and branch_thickness > 3:
        snow_x = (x + end_x) / 2
        snow_y = min(y, end_y) - 2
        snow_size = int(branch_thickness * 0.8)
        pygame.draw.ellipse(surface, (255, 255, 255), 
                           (snow_x - snow_size, snow_y - snow_size//2, snow_size * 2, snow_size))
    
    # Reset random seed for consistent child branches
    random.seed(tree_seed + current_depth * 1000 + int(x * 100) + 1)
    
    # Recursive calls with asymmetric angles
    new_length = length * branch_length_ratio * random.uniform(0.95, 1.05)
    new_thickness = branch_thickness * random.uniform(0.65, 0.75)
    
    # Left branch (asymmetric)
    left_angle = swayed_angle - branch_angle * (1 + asymmetry_offset)
    draw_branch_animated(surface, end_x, end_y, new_length, left_angle, current_depth - 1, 
                        new_thickness, leaf_colors, show_leaves, max_depth_to_draw, 
                        original_depth, wind_offset, tree_seed + 1, collect_leaves, collect_snow)
    
    # Right branch (asymmetric)
    right_angle = swayed_angle + branch_angle * (1 - asymmetry_offset * 0.5)
    draw_branch_animated(surface, end_x, end_y, new_length * 0.95, right_angle, current_depth - 1, 
                        new_thickness, leaf_colors, show_leaves, max_depth_to_draw, 
                        original_depth, wind_offset, tree_seed + 2, collect_leaves, collect_snow)

def draw_grass(surface, grass, time_val, wind_strength):
    """Draw swaying grass blade"""
    sway = math.sin(time_val * grass.sway_speed * 0.3 + grass.sway_offset) * 1 + wind_strength * 0.5
    top_x = grass.x + sway
    top_y = grass.y - grass.height
    
    # Draw grass as a thin triangle
    points = [(grass.x - 1, grass.y), (grass.x + 1, grass.y), (top_x, top_y)]
    pygame.draw.polygon(surface, grass.color, points)

def draw_flower(surface, flower, time_val, wind_strength):
    """Draw a simple flower"""
    sway = math.sin(time_val * 0.02 + flower.sway_offset) * 0.5 + wind_strength * 0.3
    
    # Draw stem
    stem_top = (flower.x + sway, flower.y - 15)
    pygame.draw.line(surface, (34, 139, 34), (flower.x, flower.y), stem_top, 2)
    
    # Draw petals
    for i in range(flower.petal_count):
        angle = (i / flower.petal_count) * 360 + time_val * 0.1
        rad = math.radians(angle)
        px = stem_top[0] + flower.size * math.cos(rad)
        py = stem_top[1] + flower.size * math.sin(rad)
        pygame.draw.circle(surface, flower.color, (int(px), int(py)), 3)
    
    # Draw center
    pygame.draw.circle(surface, (255, 255, 0), (int(stem_top[0]), int(stem_top[1])), 3)

def spawn_initial_leaves():
    """Spawn initial falling leaves for autumn - from tree canopy"""
    falling_leaves.clear()
    for tree in trees:
        # Spawn fewer leaves initially, from tree canopy area
        canopy_height = tree.trunk_length * 2
        for _ in range(8):
            x = tree.x + random.randint(-80, 80)
            y = tree.y - canopy_height + random.randint(0, int(canopy_height * 0.5))
            falling_leaves.append(FallingLeaf(x, y, random.choice(AUTUMN_LEAVES), wind_strength))

def save_screenshot():
    """Save a screenshot of the current tree"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/tree_{timestamp}.png"
    os.makedirs("screenshots", exist_ok=True)
    pygame.image.save(screen, filename)
    return filename

# Create UI elements
panel_x = WIDTH - 240

# Title label
title_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((panel_x, 10), (220, 30)),
    text='🌳 Tree Controls',
    manager=ui_manager
)

angle_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((panel_x, 60), (200, 20)),
    start_value=30,
    value_range=(10, 60),
    manager=ui_manager
)
angle_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((panel_x, 40), (200, 20)),
    text='Branch Angle: 30°',
    manager=ui_manager
)

depth_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((panel_x, 110), (200, 20)),
    start_value=10,
    value_range=(5, 13),
    manager=ui_manager
)
depth_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((panel_x, 90), (200, 20)),
    text='Recursion Depth: 10',
    manager=ui_manager
)

length_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((panel_x, 160), (200, 20)),
    start_value=67,
    value_range=(50, 80),
    manager=ui_manager
)
length_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((panel_x, 140), (200, 20)),
    text='Branch Length: 67%',
    manager=ui_manager
)

trunk_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((panel_x, 210), (200, 20)),
    start_value=120,
    value_range=(80, 200),
    manager=ui_manager
)
trunk_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((panel_x, 190), (200, 20)),
    text='Trunk Length: 120',
    manager=ui_manager
)

# New sliders
speed_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((panel_x, 260), (200, 20)),
    start_value=50,
    value_range=(10, 100),
    manager=ui_manager
)
speed_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((panel_x, 240), (200, 20)),
    text='Growth Speed: 50%',
    manager=ui_manager
)

asymmetry_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((panel_x, 310), (200, 20)),
    start_value=15,
    value_range=(0, 40),
    manager=ui_manager
)
asymmetry_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((panel_x, 290), (200, 20)),
    text='Asymmetry: 15%',
    manager=ui_manager
)

wind_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((panel_x, 360), (200, 20)),
    start_value=0,
    value_range=(-50, 50),
    manager=ui_manager
)
wind_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((panel_x, 340), (200, 20)),
    text='Wind: 0',
    manager=ui_manager
)

# Notification text
notification_text = ""
notification_timer = 0

# Time for animation
game_time = 0

# Main game loop
running = True
while running:
    time_delta = clock.tick(FPS) / 1000.0
    game_time += time_delta
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_season = "spring"
                target_bg_color = (135, 206, 235)
                falling_leaves.clear()
                snowflakes.clear()
            elif event.key == pygame.K_2:
                current_season = "summer"
                target_bg_color = (100, 149, 237)
                falling_leaves.clear()
                snowflakes.clear()
            elif event.key == pygame.K_3:
                current_season = "autumn"
                target_bg_color = (255, 200, 150)
                spawn_initial_leaves()
                snowflakes.clear()
            elif event.key == pygame.K_4:
                current_season = "winter"
                target_bg_color = (200, 220, 240)
                falling_leaves.clear()
            elif event.key == pygame.K_SPACE:
                # Restart growth for all trees
                for tree in trees:
                    tree.reset_growth()
                if current_season == "autumn":
                    spawn_initial_leaves()
            elif event.key == pygame.K_c:
                # Clear all trees except the main one
                trees = [Tree(WIDTH // 2, HEIGHT - 100, trunk_length)]
                notification_text = "Trees cleared!"
                notification_timer = 2.0
            elif event.key == pygame.K_s:
                # Screenshot
                filename = save_screenshot()
                notification_text = f"Saved: {filename}"
                notification_timer = 3.0
            elif event.key == pygame.K_r:
                # Randomize tree seed
                for tree in trees:
                    tree.seed = random.randint(0, 10000)
                    tree.reset_growth()
                notification_text = "Randomized trees!"
                notification_timer = 2.0
        
        # Mouse click to plant new tree
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mx, my = event.pos
                # Only plant in the lower area (above ground, not on UI)
                if my > 200 and my < HEIGHT - 100 and mx < WIDTH - 250:
                    new_tree = Tree(mx, HEIGHT - 100, trunk_length * random.uniform(0.6, 1.0))
                    trees.append(new_tree)
                    notification_text = f"Planted tree! ({len(trees)} total)"
                    notification_timer = 2.0
        
        # Handle slider events
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == angle_slider:
                branch_angle = math.radians(event.value)
                angle_label.set_text(f'Branch Angle: {int(event.value)}°')
            elif event.ui_element == depth_slider:
                recursion_depth = int(event.value)
                depth_label.set_text(f'Recursion Depth: {int(event.value)}')
            elif event.ui_element == length_slider:
                branch_length_ratio = event.value / 100
                length_label.set_text(f'Branch Length: {int(event.value)}%')
            elif event.ui_element == trunk_slider:
                trunk_length = int(event.value)
                trunk_label.set_text(f'Trunk Length: {int(event.value)}')
                # Update main tree
                if trees:
                    trees[0].trunk_length = trunk_length
            elif event.ui_element == speed_slider:
                growth_speed = event.value / 1000
                speed_label.set_text(f'Growth Speed: {int(event.value)}%')
            elif event.ui_element == asymmetry_slider:
                asymmetry = event.value / 100
                asymmetry_label.set_text(f'Asymmetry: {int(event.value)}%')
            elif event.ui_element == wind_slider:
                wind_target = event.value / 10
                wind_label.set_text(f'Wind: {int(event.value)}')
        
        ui_manager.process_events(event)
    
    # Smooth wind transition
    wind_strength += (wind_target - wind_strength) * 0.02
    
    # Add very subtle natural wind variation (nearly still by default)
    wind_time += time_delta
    natural_wind = math.sin(wind_time * 0.2) * 0.02
    current_wind = wind_strength + natural_wind
    
    # Update tree growth
    for tree in trees:
        if tree.growing:
            tree.growth += growth_speed
            if tree.growth >= recursion_depth:
                tree.growth = recursion_depth
                tree.growing = False
    
    # Smooth background color transition
    bg_color = lerp_color(bg_color, target_bg_color, 0.02)
    
    # Select colors based on season
    if current_season == "spring":
        leaf_colors = SPRING_LEAVES
        show_leaves = True
    elif current_season == "summer":
        leaf_colors = SUMMER_LEAVES
        show_leaves = True
    elif current_season == "autumn":
        leaf_colors = AUTUMN_LEAVES
        show_leaves = True
    else:  # winter
        leaf_colors = []
        show_leaves = False
    
    # Clear screen with seasonal gradient
    screen.fill(bg_color)
    
    # Draw gradient sky
    for i in range(100):
        alpha = i / 100
        sky_color = lerp_color(bg_color, tuple(max(0, c - 30) for c in bg_color), alpha)
        pygame.draw.line(screen, sky_color, (0, i * 2), (WIDTH, i * 2))
    
    # Draw sun/moon
    if current_season == "winter":
        # Moon
        pygame.draw.circle(screen, (220, 220, 220), (100, 80), 30)
        pygame.draw.circle(screen, bg_color, (110, 75), 25)  # Crescent effect
    else:
        # Sun
        sun_color = (255, 220, 100) if current_season == "autumn" else (255, 255, 200)
        pygame.draw.circle(screen, sun_color, (100, 80), 35)
        # Sun rays
        for i in range(8):
            angle = i * 45 + game_time * 10
            rad = math.radians(angle)
            pygame.draw.line(screen, sun_color, 
                           (100 + 40 * math.cos(rad), 80 + 40 * math.sin(rad)),
                           (100 + 55 * math.cos(rad), 80 + 55 * math.sin(rad)), 2)
    
    # Draw clouds
    cloud_offset = game_time * 10 + wind_strength * 5
    for i in range(3):
        cx = (200 + i * 300 + cloud_offset) % (WIDTH + 200) - 100
        cy = 60 + i * 30
        cloud_color = (255, 255, 255) if current_season != "winter" else (200, 200, 210)
        pygame.draw.ellipse(screen, cloud_color, (cx, cy, 80, 30))
        pygame.draw.ellipse(screen, cloud_color, (cx + 20, cy - 15, 60, 35))
        pygame.draw.ellipse(screen, cloud_color, (cx + 50, cy, 70, 25))
    
    # Draw ground with gradient
    ground_color = (139, 69, 19) if current_season != "winter" else (200, 200, 210)
    pygame.draw.rect(screen, ground_color, (0, HEIGHT - 100, WIDTH, 100))
    
    # Snow on ground in winter
    if current_season == "winter":
        pygame.draw.ellipse(screen, (255, 255, 255), (0, HEIGHT - 110, WIDTH, 40))
    
    # Draw grass (not in winter)
    if current_season != "winter":
        for grass in grass_blades:
            draw_grass(screen, grass, game_time, current_wind)
    
    # Draw flowers (only in spring/summer)
    if current_season in ["spring", "summer"]:
        for flower in flowers:
            draw_flower(screen, flower, game_time, current_wind)
    
    # Draw all trees
    for tree in trees:
        initial_angle = -math.pi / 2
        initial_thickness = 12 * (tree.trunk_length / 120)
        
        draw_branch_animated(screen, tree.x, tree.y, tree.trunk_length, initial_angle, 
                            recursion_depth, initial_thickness, leaf_colors, show_leaves, 
                            int(tree.growth), recursion_depth, current_wind, tree.seed)
    
    # Update and draw falling leaves (autumn)
    if current_season == "autumn":
        # Spawn new leaves gently from tree canopy area
        if random.random() < 0.05 and len(falling_leaves) < 40:  # Slower spawn rate
            for tree in trees:
                if tree.growth > 5:
                    # Spawn from canopy area (top of tree)
                    canopy_height = tree.trunk_length * 2  # Approximate tree height
                    x = tree.x + random.randint(-80, 80)
                    y = tree.y - canopy_height + random.randint(0, int(canopy_height * 0.6))
                    falling_leaves.append(FallingLeaf(x, y, random.choice(AUTUMN_LEAVES), wind_strength))
        
        for leaf in falling_leaves[:]:
            leaf.update(current_wind)
            leaf.draw(screen)
            if leaf.is_off_screen(HEIGHT, WIDTH):
                falling_leaves.remove(leaf)
    
    # Update and draw snowflakes (winter)
    if current_season == "winter":
        # Spawn new snowflakes
        if random.random() < 0.3 and len(snowflakes) < 150:
            snowflakes.append(Snowflake(random.randint(0, WIDTH), -10))
        
        for flake in snowflakes[:]:
            flake.update(current_wind)
            flake.draw(screen)
            if flake.is_off_screen(HEIGHT):
                snowflakes.remove(flake)
    
    # Draw UI panel background
    pygame.draw.rect(screen, (0, 0, 0, 180), (WIDTH - 250, 0, 250, 400))
    pygame.draw.rect(screen, (50, 50, 50), (WIDTH - 250, 0, 250, 400), 2)
    
    # Display controls help
    font = pygame.font.Font(None, 24)
    help_texts = [
        f"Season: {current_season.upper()} (1-4)",
        "SPACE: Restart Growth",
        "Click: Plant Tree",
        "C: Clear Trees",
        "S: Screenshot",
        "R: Randomize"
    ]
    
    pygame.draw.rect(screen, (0, 0, 0, 200), (10, 10, 180, len(help_texts) * 22 + 10))
    for i, text in enumerate(help_texts):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (15, 15 + i * 22))
    
    # Show notification
    if notification_timer > 0:
        notification_timer -= time_delta
        notif_surface = font.render(notification_text, True, (255, 255, 100))
        notif_rect = notif_surface.get_rect(center=(WIDTH // 2, 50))
        pygame.draw.rect(screen, (0, 0, 0), notif_rect.inflate(20, 10))
        screen.blit(notif_surface, notif_rect)
    
    # Update and draw UI
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    
    # Update display
    pygame.display.flip()

pygame.quit()