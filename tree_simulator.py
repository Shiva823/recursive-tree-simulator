import pygame
import math
import random
import pygame_gui

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recursive Tree Growth Simulator")

# Colors
SKY_BLUE = (135, 206, 235)
BROWN = (101, 67, 33)
GREEN = (34, 139, 34)
# Leaf colors for different seasons
SPRING_LEAVES = [(144, 238, 144), (152, 251, 152), (124, 252, 0), (173, 255, 47)]
SUMMER_LEAVES = [(34, 139, 34), (0, 128, 0), (0, 100, 0), (46, 139, 87)]
AUTUMN_LEAVES = [(255, 140, 0), (255, 69, 0), (255, 99, 71), (178, 34, 34), (139, 69, 19)]

class FallingLeaf:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 6)
        self.speed_y = random.uniform(0.5, 1.5)
        self.speed_x = random.uniform(-0.3, 0.3)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
    
    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        self.rotation += self.rotation_speed
        
        # Add some wind effect (slight horizontal drift)
        self.speed_x += random.uniform(-0.1, 0.1)
        self.speed_x = max(-1, min(1, self.speed_x))  # Limit speed
    
    def draw(self, screen):
        # Draw leaf as a small circle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
    
    def is_off_screen(self, height):
        return self.y > height

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Season control
current_season = "spring"

# Growth animation
growth_depth = 0
max_depth = 10
growing = True
growth_speed = 0.08

# Falling leaves
falling_leaves = []

# GUI Manager for sliders
ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Tree parameters (adjustable)
branch_angle = math.pi / 6  # Default: 30 degrees
branch_length_ratio = 0.67
trunk_length = 120
recursion_depth = 10
leaf_colors = SPRING_LEAVES
show_leaves = True
bg_color = (135, 206, 235)

def draw_branch_animated(x, y, length, angle, current_depth, branch_thickness, leaf_colors, show_leaves, max_depth_to_draw, original_depth):
    """
    Draws tree with growth animation
    """
    if current_depth <= 0:
        return
    
    # Calculate what "level" we're at (1 = trunk, 2 = first branches, etc.)
    current_level = original_depth - current_depth + 1
    
    # Only draw if animation has reached this level
    if current_level > max_depth_to_draw:
        return
    
    # Calculate end point of the branch
    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)
    
    # Choose branch color
    if branch_thickness > 5:
        branch_color = (101, 67, 33)
    else:
        branch_color = (139, 90, 43)
    
    # Draw the branch
    pygame.draw.line(screen, branch_color, (x, y), (end_x, end_y), int(branch_thickness))
    
    # Draw leaves at the end of small branches
    if current_depth <= 3 and show_leaves:
        if leaf_colors:
            leaf_color = random.choice(leaf_colors)
            leaf_size = random.randint(4, 8)
            pygame.draw.circle(screen, leaf_color, (int(end_x), int(end_y)), leaf_size)
        
        # Store leaf positions for falling effect (only in autumn)
        if current_season == "autumn" and random.random() < 0.005:
            falling_leaves.append(FallingLeaf(end_x, end_y, random.choice(AUTUMN_LEAVES)))
    
    # Recursive calls (use adjustable parameters)
    new_length = length * branch_length_ratio
    new_thickness = branch_thickness * 0.7
    
    draw_branch_animated(end_x, end_y, new_length, angle - branch_angle, current_depth - 1, new_thickness,
                        leaf_colors, show_leaves, max_depth_to_draw, original_depth)
    draw_branch_animated(end_x, end_y, new_length, angle + branch_angle, current_depth - 1, new_thickness,
                        leaf_colors, show_leaves, max_depth_to_draw, original_depth)
    
def spawn_initial_leaves():
    """Spawn initial falling leaves for autumn"""
    falling_leaves.clear()
    # Pre-spawn some leaves at random positions
    for i in range(20):
        x = random.randint(WIDTH//2 - 200, WIDTH//2 + 200)
        y = random.randint(100, HEIGHT - 200)
        falling_leaves.append(FallingLeaf(x, y, random.choice(AUTUMN_LEAVES)))

# Create UI elements (smaller, cleaner sliders)
angle_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH - 230, 100), (200, 15)),
    start_value=30,
    value_range=(10, 60),
    manager=ui_manager
)
angle_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((WIDTH - 230, 75), (200, 25)),
    text='Angle: 30°',
    manager=ui_manager
)

depth_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH - 230, 150), (200, 15)),
    start_value=10,
    value_range=(5, 13),
    manager=ui_manager
)
depth_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((WIDTH - 230, 125), (200, 25)),
    text='Depth: 10',
    manager=ui_manager
)

length_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH - 230, 200), (200, 15)),
    start_value=67,
    value_range=(50, 80),
    manager=ui_manager
)
length_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((WIDTH - 230, 175), (200, 25)),
    text='Length: 67%',
    manager=ui_manager
)

trunk_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH - 230, 250), (200, 15)),
    start_value=120,
    value_range=(80, 200),
    manager=ui_manager
)
trunk_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((WIDTH - 230, 225), (200, 25)),
    text='Trunk: 120',
    manager=ui_manager
)

# Main game loop
running = True
while running:
    # Handle events
    time_delta = clock.tick(FPS) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_season = "spring"
                falling_leaves.clear()
            elif event.key == pygame.K_2:
                current_season = "summer"
                falling_leaves.clear()
            elif event.key == pygame.K_3:
                current_season = "autumn"
                spawn_initial_leaves()
            elif event.key == pygame.K_4:
                current_season = "winter"
                falling_leaves.clear()
            elif event.key == pygame.K_SPACE:
                growth_depth = 0
                growing = True
                if current_season == "autumn":
                    spawn_initial_leaves()
        
        # Handle slider events
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == angle_slider:
                branch_angle = math.radians(event.value)
                angle_label.set_text(f'Angle: {int(event.value)}°')
            elif event.ui_element == depth_slider:
                recursion_depth = int(event.value)
                max_depth = recursion_depth
                depth_label.set_text(f'Depth: {int(event.value)}')
            elif event.ui_element == length_slider:
                branch_length_ratio = event.value / 100
                length_label.set_text(f'Length: {int(event.value)}%')
            elif event.ui_element == trunk_slider:
                trunk_length = int(event.value)
                trunk_label.set_text(f'Trunk: {int(event.value)}')
        
        ui_manager.process_events(event)
    
    # Growth animation update
    if growing:
        growth_depth += growth_speed
        if growth_depth >= max_depth:
            growth_depth = max_depth
            growing = False
    
    # Select colors based on season
    if current_season == "spring":
        leaf_colors = SPRING_LEAVES
        bg_color = (135, 206, 235)
        show_leaves = True
    elif current_season == "summer":
        leaf_colors = SUMMER_LEAVES
        bg_color = (100, 149, 237)
        show_leaves = True
    elif current_season == "autumn":
        leaf_colors = AUTUMN_LEAVES
        bg_color = (255, 165, 0)
        show_leaves = True
    else:  # winter
        leaf_colors = []
        bg_color = (176, 196, 222)
        show_leaves = False
    
    # Clear screen with seasonal color
    screen.fill(bg_color)
    
    # Draw ground
    pygame.draw.rect(screen, (139, 69, 19), (0, HEIGHT - 100, WIDTH, 100))
    
    # Draw tree with growth animation
    tree_x = WIDTH // 2
    tree_y = HEIGHT - 100
    initial_angle = -math.pi / 2
    initial_thickness = 12
    
    draw_branch_animated(tree_x, tree_y, trunk_length, initial_angle, recursion_depth,
                        initial_thickness, leaf_colors, show_leaves, int(growth_depth), recursion_depth)
    
    # Update and draw falling leaves (autumn only)
    if current_season == "autumn":
        # Continuously spawn new leaves from tree area
        if random.random() < 0.1 and len(falling_leaves) < 50:
            x = random.randint(WIDTH//2 - 150, WIDTH//2 + 150)
            y = random.randint(HEIGHT//2 - 100, HEIGHT//2 + 100)
            falling_leaves.append(FallingLeaf(x, y, random.choice(AUTUMN_LEAVES)))
        
        for leaf in falling_leaves[:]:
            leaf.update()
            leaf.draw(screen)
            if leaf.is_off_screen(HEIGHT):
                falling_leaves.remove(leaf)
    
    # Display controls
    font = pygame.font.Font(None, 28)
    text1 = font.render(f"Season: {current_season.upper()} (1-4)", True, (255, 255, 255))
    text2 = font.render("SPACE: Restart Growth", True, (255, 255, 255))
    
    # Draw text with background for visibility
    pygame.draw.rect(screen, (0, 0, 0), (10, 10, 280, 60))
    screen.blit(text1, (20, 20))
    screen.blit(text2, (20, 45))
    
    # Update and draw UI
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    
    # Update display
    pygame.display.flip()
pygame.quit()