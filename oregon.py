import pygame
import random
import time

# ... (rest of the imports)

# Constants
GROWTH_MEAN = 30  # 30 seconds on average
GROWTH_STD_DEV = 2  

# Initialize pygame
pygame.init()


MONEY_COLOR = (255, 204, 73)
# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
DIRT = (181,101,30)

CROP_COLORS = {
    "carrot": (255, 105, 0),  # Orange for carrot
    "wheat": (223, 186, 105), # Light Brown for wheat
    "corn": (255, 228, 0),   # Yellow for corn
    "barley": (153, 101, 21) # Dark Brown for barley
}

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# World dimensions (big plot)
WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000

# Plot dimensions
PLOT_WIDTH = 50
PLOT_HEIGHT = 50
PLOT_MARGIN = 10

# Character properties
CHAR_WIDTH = 30
CHAR_HEIGHT = 40
CHAR_SPEED = 20
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Farming Simulator with Camera System')

#Box in top right
BACKGROUND_BOX_WIDTH = 140
BACKGROUND_BOX_HEIGHT = 150
BACKGROUND_BOX_COLOR = (240, 240, 240)  # Light gray

# Seed growth stages
SEED_STAGES = [
    pygame.Surface((PLOT_WIDTH, PLOT_HEIGHT)),
    pygame.Surface((PLOT_WIDTH, PLOT_HEIGHT)),
    pygame.Surface((PLOT_WIDTH, PLOT_HEIGHT))
]

# Draw seed stages
SEED_STAGES[0].fill(BROWN)
SEED_STAGES[1].fill(GREEN)
pygame.draw.circle(SEED_STAGES[1], BROWN, (PLOT_WIDTH // 2, PLOT_HEIGHT // 2), 10)
SEED_STAGES[2].fill(GREEN)



JohnDeer = [pygame.image.load('john_w.png').convert_alpha(), pygame.image.load('john_a.png').convert_alpha(), pygame.image.load('john_s.png').convert_alpha(),pygame.image.load('john_d.png').convert_alpha(), pygame.image.load('john_wa.png').convert_alpha(), pygame.image.load('john_wd.png').convert_alpha(),pygame.image.load('john_sa.png').convert_alpha(),pygame.image.load('john_sd.png').convert_alpha()]

CHARACTERS = [JohnDeer]

# Create a plot class
class Plot:
    def __init__(self, x, y, crop_type):
        self.x = x
        self.y = y
        self.crop_type = crop_type
        self.seed_stage = 2
        self.last_growth_time = time.time()  # Current time
        self.set_next_growth_time()
    
    def set_next_growth_time(self):
        # Set the next growth time based on a Gaussian distribution
        self.next_growth_time = self.last_growth_time + random.gauss(GROWTH_MEAN, GROWTH_STD_DEV)

    def plant_seed(self):
        if self.seed_stage == 0:
            self.seed_stage = 1

    def grow(self):
        if time.time() >= self.next_growth_time and self.seed_stage < 2:
            self.seed_stage = 2
            self.last_growth_time = time.time()
            self.set_next_growth_time()

    def draw(self, screen, camera_x, camera_y):
        color = BROWN if self.seed_stage == 0 else CROP_COLORS[self.crop_type]
        pygame.draw.rect(screen, color, (self.x - camera_x, self.y - camera_y, PLOT_WIDTH, PLOT_HEIGHT))

# Create a character class

money = 0

harvested_crops = {
    "carrot": 0,
    "wheat": 0,
    "corn": 0,
    "barley": 0
}



class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.character = 0
        self.image = CHARACTERS[self.character][0]

    def move(self, dx, dy):
        if dx != 0 and dy != 0:
            # Adjust the velocity for diagonal movement
            factor = 1 / (2**0.5)
            dx *= factor
            dy *= factor
        new_x = self.x + dx
        new_y = self.y + dy
        
        if 0 <= new_x <= WORLD_WIDTH - CHAR_WIDTH:
            self.x = new_x
        if 0 <= new_y <= WORLD_HEIGHT - CHAR_HEIGHT:
            self.y = new_y

    def draw(self, screen, camera_x, camera_y):
        character_image = pygame.image.load('Test2Clear.png').convert_alpha()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and keys[pygame.K_a]:
            self.image = CHARACTERS[self.character][4]
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            self.image = CHARACTERS[self.character][5]
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            self.image = CHARACTERS[self.character][6]
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            self.image = CHARACTERS[self.character][7]
        elif keys[pygame.K_w]:
            self.image = CHARACTERS[self.character][0]
        elif keys[pygame.K_a]:
            self.image = CHARACTERS[self.character][1]
        elif keys[pygame.K_s]:
            self.image = CHARACTERS[self.character][2]
        elif keys[pygame.K_d]:
            self.image = CHARACTERS[self.character][3]

        draw_x = self.x - camera_x - self.image.get_width() // 2
        draw_y = self.y - camera_y - self.image.get_height() // 2
        screen.blit(self.image, (draw_x, draw_y))

    def check_collision(self, plots):
        for plot in plots:
            if (plot.x <= self.x <= plot.x + PLOT_WIDTH or plot.x <= self.x + CHAR_WIDTH <= plot.x + PLOT_WIDTH) and \
               (plot.y <= self.y <= plot.y + PLOT_HEIGHT or plot.y <= self.y + CHAR_HEIGHT <= plot.y + PLOT_HEIGHT):
               if plot.seed_stage == 2:
                    harvested_crops[plot.crop_type] += 1
                    plot.seed_stage = 0
                

# Draw the harvested crop counts on the screen
def draw_harvested_counts(screen):
    font = pygame.font.SysFont(None, 24)
    offset_y = 10

    # Draw the background box
    pygame.draw.rect(screen, BACKGROUND_BOX_COLOR, (SCREEN_WIDTH - BACKGROUND_BOX_WIDTH, 0, BACKGROUND_BOX_WIDTH, BACKGROUND_BOX_HEIGHT))

    for crop, count in harvested_crops.items():
        text = f"{crop.capitalize()}: {count}"
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH - text_surface.get_width() - 10, offset_y))
        offset_y += 30

    # Display the money below the harvested crop counts with up to 5 significant figures
    formatted_money = "{:.5g}".format(money)  # Format the money value
    money_text = f"Money: ${formatted_money}"
    money_surface = font.render(money_text, True, MONEY_COLOR)
    
    # Adjust the x-coordinate to ensure the money text fits within the screen
    money_x = SCREEN_WIDTH - money_surface.get_width() - 10
    screen.blit(money_surface, (money_x, offset_y))



# Create the game screen

GRAVEL_COLOR = (200, 200, 200)  # Gray color for gravel
GRAVEL_WIDTH = 40  # Width of the gravel path

# ... (Plot and Character class definitions)

# Draw the gravel paths
def draw_gravel_paths(screen, camera_x, camera_y):
    # Horizontal path
    pygame.draw.rect(screen, GRAVEL_COLOR, (0 - camera_x, (WORLD_HEIGHT // 2) - (GRAVEL_WIDTH // 2) - camera_y, WORLD_WIDTH, GRAVEL_WIDTH))
    # Vertical path
    pygame.draw.rect(screen, GRAVEL_COLOR, ((WORLD_WIDTH // 2) - (GRAVEL_WIDTH // 2) - camera_x, 0 - camera_y, GRAVEL_WIDTH, WORLD_HEIGHT))

STORE_WIDTH = 300
STORE_HEIGHT = 400

# Store flags
store_open = False
left_store_area = True 
market_open = False
left_market_area = True

# ... (Plot and Character class definitions)

# Check if character is at the store position
def check_store_position(character):
    global store_open, left_store_area
    if left_store_area and character.x < CHAR_WIDTH and (WORLD_HEIGHT // 2 - STORE_HEIGHT // 2) < character.y < (WORLD_HEIGHT // 2 + STORE_HEIGHT // 2):
        store_open = True
        left_store_area = False 

# Draw the store menu
def draw_store(screen):
    pygame.draw.rect(screen, (150, 150, 150), (SCREEN_WIDTH // 2 - STORE_WIDTH // 2, SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2, STORE_WIDTH, STORE_HEIGHT))
    font = pygame.font.SysFont(None, 36)
    text = font.render("Store", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2 + 20))


def check_market_position(character):
    global market_open, left_market_area
    if left_market_area and character.x > WORLD_WIDTH - 2*CHAR_WIDTH and (WORLD_HEIGHT // 2 - STORE_HEIGHT // 2) < character.y < (WORLD_HEIGHT // 2 + STORE_HEIGHT // 2):
        market_open = True
        left_market_area = False

# Draw the market menu
def draw_market(screen):
    market_rect = pygame.Rect(SCREEN_WIDTH // 2 - STORE_WIDTH // 2, SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2, STORE_WIDTH, STORE_HEIGHT)
    pygame.draw.rect(screen, (150, 150, 150), market_rect)
    font = pygame.font.SysFont(None, 36)
    text = font.render("Market", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2 + 20))

    # Display selling options
    options = ["Sell Carrots", "Sell Wheat", "Sell Corn", "Sell Barley", "Sell All Crops"]
    offset_y = 80
    for option in options:
        text = font.render(option, True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2 + offset_y))
        offset_y += 40

# Building definitions
BUILDING_WIDTH = 100
BUILDING_HEIGHT = 100
BUILDING_COLOR = (150, 150, 150)

def draw_building(screen, x, y, label, camera_x, camera_y):
    """Draws a building with a label at the specified position."""
    # Building rectangle
    pygame.draw.rect(screen, BUILDING_COLOR, (x - camera_x, y - camera_y, BUILDING_WIDTH, BUILDING_HEIGHT))
    
    # Label for the building
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(label, True, (0, 0, 0))  # Black label
    screen.blit(text_surface, (x - camera_x + BUILDING_WIDTH // 2 - text_surface.get_width() // 2, y - camera_y + BUILDING_HEIGHT // 2 - text_surface.get_height() // 2))


# Adjust plot generation for the 2x2 grid with gravel paths
plots = []
sections = [
    {"start_x": 0, "end_x": WORLD_WIDTH // 2 - GRAVEL_WIDTH , "start_y": 0, "end_y": WORLD_HEIGHT // 2 - GRAVEL_WIDTH, "crop": "carrot"},
    {"start_x": WORLD_WIDTH // 2 + GRAVEL_WIDTH, "end_x": WORLD_WIDTH, "start_y": 0, "end_y": WORLD_HEIGHT // 2 - GRAVEL_WIDTH, "crop": "wheat"},
    {"start_x": 0, "end_x": WORLD_WIDTH // 2 - GRAVEL_WIDTH, "start_y": WORLD_HEIGHT // 2 + GRAVEL_WIDTH, "end_y": WORLD_HEIGHT, "crop": "corn"},
    {"start_x": WORLD_WIDTH // 2 + GRAVEL_WIDTH , "end_x": WORLD_WIDTH, "start_y": WORLD_HEIGHT // 2 + GRAVEL_WIDTH , "end_y": WORLD_HEIGHT, "crop": "barley"}
]

for section in sections:
    for x in range(section["start_x"], section["end_x"], PLOT_WIDTH + PLOT_MARGIN):
        for y in range(section["start_y"], section["end_y"], PLOT_HEIGHT + PLOT_MARGIN):
            plots.append(Plot(x, y, section["crop"]))


character = Character(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
# Define a margin for the dirt
DIRT_MARGIN = 10

# Load and scale the dirt texture
large_dirt_texture = pygame.image.load('dirt.png').convert_alpha()
scaled_dirt_texture = pygame.transform.scale(large_dirt_texture, (PLOT_WIDTH + DIRT_MARGIN * 2, PLOT_HEIGHT + DIRT_MARGIN * 2))


# Main game loop
running = True
while running:
    screen.fill(DIRT)
    #for x in range(0, SCREEN_WIDTH, dirt_texture.get_width()):
    #    for y in range(0, SCREEN_HEIGHT, dirt_texture.get_height()):
    #        screen.blit(dirt_texture, (x, y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Close store/market with ESC key
                store_open = False
                market_open = False
        if event.type == pygame.MOUSEBUTTONDOWN and market_open:
            x, y = pygame.mouse.get_pos()
            # Check which option was clicked and update money and crops accordingly
            option_height = 40
            for index, option in enumerate(["Sell Carrots", "Sell Wheat", "Sell Corn", "Sell Barley", "Sell All Crops"]):
                option_y = SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2 + 80 + index * option_height
                if SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100 and option_y < y < option_y + option_height:
                    if option == "Sell All Crops":
                        for crop_type in harvested_crops:
                            money += harvested_crops[crop_type]
                            harvested_crops[crop_type] = 0
                    else:
                        crop_type = option.split(" ")[1].lower()
                        money += harvested_crops[crop_type]
                        harvested_crops[crop_type] = 0



    keys = pygame.key.get_pressed()
    if not store_open and not market_open:
        dx, dy = 0, 0  # Initialize changes in x and y to 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dy -= CHAR_SPEED
        if keys[pygame.K_s]:
            dy += CHAR_SPEED
        if keys[pygame.K_a]:
            dx -= CHAR_SPEED
        if keys[pygame.K_d]:
            dx += CHAR_SPEED

        character.move(dx, dy)
        if not (character.x < CHAR_WIDTH and (WORLD_HEIGHT // 2 - STORE_HEIGHT // 2) < character.y < (WORLD_HEIGHT // 2 + STORE_HEIGHT // 2)):
            left_store_area = True
        if not (character.x > WORLD_WIDTH - 2*CHAR_WIDTH and (WORLD_HEIGHT // 2 - STORE_HEIGHT // 2) < character.y < (WORLD_HEIGHT // 2 + STORE_HEIGHT // 2)):
            left_market_area = True

        
    # Camera position (centered on the character)
    camera_x = character.x - SCREEN_WIDTH // 2
    camera_y = character.y - SCREEN_HEIGHT // 2

    # Clamp camera to world boundaries
    camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))


    check_store_position(character)
    check_market_position(character)

    draw_gravel_paths(screen, camera_x, camera_y)

    

    
    if store_open:
        draw_store(screen)
        pygame.display.flip()
        continue 

    if market_open:
        draw_market(screen)
        pygame.display.flip()
        continue

    for plot in plots:
        screen.blit(scaled_dirt_texture, (plot.x - camera_x - DIRT_MARGIN, plot.y - camera_y - DIRT_MARGIN))
        if (plot.x + PLOT_WIDTH + DIRT_MARGIN >= camera_x and plot.x - DIRT_MARGIN <= camera_x + SCREEN_WIDTH) and \
           (plot.y + PLOT_HEIGHT + DIRT_MARGIN >= camera_y and plot.y - DIRT_MARGIN <= camera_y + SCREEN_HEIGHT):
            plot.grow()
            plot.draw(screen, camera_x, camera_y)

        
    draw_building(screen, 0, WORLD_HEIGHT // 2 - BUILDING_HEIGHT // 2, "Store", camera_x, camera_y)
    draw_building(screen, WORLD_WIDTH - BUILDING_WIDTH, WORLD_HEIGHT // 2 - BUILDING_HEIGHT // 2, "Market", camera_x, camera_y)


    character.check_collision(plots)  # Plant seeds if character collides with a plot
    
    character.draw(screen, camera_x, camera_y)
    draw_harvested_counts(screen)
    

    pygame.display.flip()
    pygame.time.wait(50)

pygame.quit()
