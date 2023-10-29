import pygame
import random
import time
import sys

# ... (rest of the imports)

# Constants
GROWTH_MEAN = [120,90,60,30]  # 30 seconds on average
GROWTH_MEAN_IDX = 0
GROWTH_STD_DEV = GROWTH_MEAN[GROWTH_MEAN_IDX]/4

# Initialize pygame
pygame.init()


MONEY_COLOR = (255, 204, 73)
# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
DIRT = (131,101,57)

CROP_COLORS = {
    "Carrots": (255, 105, 0),  # Orange for carrot
    "Wheat": (223, 186, 105), # Light Brown for wheat
    "Corn": (255, 228, 0),   # Yellow for corn
    "Potatoes": (153, 101, 21) # Dark Brown for potato
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
CHAR_SPEED = [15,20,25,30]
CHAR_SPEED_IDX = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Farming Simulator 2023')

#Box in top right
BACKGROUND_BOX_WIDTH = 140
BACKGROUND_BOX_HEIGHT = 150
BACKGROUND_BOX_COLOR = (240, 240, 240)  # Light gray

#Crop banner dimensions
CROP_BANNER_WIDTH = 300
CROP_BANNER_HEIGHT = 100
CROP_BANNER_COLOR = (220, 20, 60) # Red

#Market banner dimensions
MARKET_BANNER_WIDTH = 250
MARKET_BANNER_HEIGHT = 75
MARKET_BANNER_COLOR = (50, 205, 50) # Green

# Building definitions
BUILDING_WIDTH = 100
BUILDING_HEIGHT = 100
BUILDING_COLOR = (150, 150, 150)

MAX_HOLD_SIZE = [50,100,200,400]
MAX_HOLD_SIZE_IDX  = 0

GRAVEL_COLOR = (200, 200, 200)  # Gray color for gravel
GRAVEL_WIDTH = 40  # Width of the gravel path
PATH_WIDTH = 50  # Adjust this value based on your desired path width

money = 20

sell_amount = {
    "Wheat": 1,
    "Potatoes": 4,
    "Carrots": 7,
    "Corn": 10,
}

# Draw the store menu
STORE_WIDTH = 500  # Adjust as needed
STORE_HEIGHT = 400  # Adjust as needed

# Store flags
store_open = False
left_store_area = True 
market_open = False
left_market_area = True
store_banner = False
latestUpgradePurchased = None
purchaseValidate = None

market_banner_on = False
latestCrop = None
latestSoldValue = None
latestSoldAmount = None

# Assuming you have these global variables defined at the top of your script:
upgrade_stages = [1, 1, 1, 1]  # Initial stages for the four upgrades
secret_option_cost = 10000  # Cost for the secret option

# Define a margin for the dirt
DIRT_MARGIN = 10

# Load and scale the dirt texture
large_dirt_texture = pygame.image.load('dirt.png').convert_alpha()
scaled_dirt_texture = pygame.transform.scale(large_dirt_texture, (PLOT_WIDTH + DIRT_MARGIN * 2, PLOT_HEIGHT + DIRT_MARGIN * 2))

tilled_dirt_template = pygame.image.load('tilled_dirt.png')
tilled_dirt_texture = pygame.transform.scale(tilled_dirt_template, (PLOT_WIDTH, PLOT_HEIGHT))

# Load the carrot texture
carrot_texture = pygame.image.load('carrot.png').convert_alpha()
carrot_texture = pygame.transform.scale(carrot_texture, (PLOT_WIDTH, PLOT_HEIGHT))

potatoe_texture = pygame.image.load('potatoes.png').convert_alpha()
potatoe_texture = pygame.transform.scale(potatoe_texture, (PLOT_WIDTH, PLOT_HEIGHT))

corn_texture = pygame.image.load('corn.png').convert_alpha()
corn_texture = pygame.transform.scale(corn_texture, (PLOT_WIDTH, PLOT_HEIGHT))

wheat_texture = pygame.image.load('wheat.png').convert_alpha()
wheat_texture = pygame.transform.scale(wheat_texture, (PLOT_WIDTH, PLOT_HEIGHT))

JohnDeerRed = [pygame.image.load('john_w.png').convert_alpha(), pygame.image.load('Truck Tiers/Red Truck/john_a.png').convert_alpha(), pygame.image.load('john_s.png').convert_alpha(),pygame.image.load('Truck Tiers/Red Truck/john_d.png').convert_alpha(), pygame.image.load('Truck Tiers/Red Truck/john_wa.png').convert_alpha(), pygame.image.load('Truck Tiers/Red Truck/john_wd.png').convert_alpha(),pygame.image.load('Truck Tiers/Red Truck/john_sa.png').convert_alpha(),pygame.image.load('Truck Tiers/Red Truck/john_sd.png').convert_alpha()]
JohnDeerBlue = [pygame.image.load('john_w.png').convert_alpha(), pygame.image.load('Truck Tiers/Blue Truck/john_a.png').convert_alpha(), pygame.image.load('john_s.png').convert_alpha(),pygame.image.load('Truck Tiers/Blue Truck/john_d.png').convert_alpha(), pygame.image.load('Truck Tiers/Blue Truck/john_wa.png').convert_alpha(), pygame.image.load('Truck Tiers/Blue Truck/john_wd.png').convert_alpha(),pygame.image.load('Truck Tiers/Blue Truck/john_sa.png').convert_alpha(),pygame.image.load('Truck Tiers/Blue Truck/john_sd.png').convert_alpha()]
JohnDeerPurple = [pygame.image.load('john_w.png').convert_alpha(), pygame.image.load('Truck Tiers/Purple Truck/john_a.png').convert_alpha(), pygame.image.load('john_s.png').convert_alpha(),pygame.image.load('Truck Tiers/Purple Truck/john_d.png').convert_alpha(), pygame.image.load('Truck Tiers/Purple Truck/john_wa.png').convert_alpha(), pygame.image.load('Truck Tiers/Purple Truck/john_wd.png').convert_alpha(),pygame.image.load('Truck Tiers/Purple Truck/john_sa.png').convert_alpha(),pygame.image.load('Truck Tiers/Purple Truck/john_sd.png').convert_alpha()]
JohnDeerYellow = [pygame.image.load('john_w.png').convert_alpha(), pygame.image.load('john_a.png').convert_alpha(), pygame.image.load('john_s.png').convert_alpha(),pygame.image.load('john_d.png').convert_alpha(), pygame.image.load('john_wa.png').convert_alpha(), pygame.image.load('john_wd.png').convert_alpha(),pygame.image.load('john_sa.png').convert_alpha(),pygame.image.load('john_sd.png').convert_alpha()]
CHARACTERS = [JohnDeerRed, JohnDeerBlue, JohnDeerPurple, JohnDeerYellow]

# ... (Plot and Character class definitions)
gravel_texture = pygame.image.load('gravel.png').convert_alpha()
original_width, original_height = gravel_texture.get_size()

# Compute the scaling factor
scaling_factor = PATH_WIDTH / original_width
new_height = int(original_height * scaling_factor)
scaled_gravel_texture = pygame.transform.scale(gravel_texture, (PATH_WIDTH, new_height))

building_image = pygame.image.load('Store.png')

# Create a plot class
class Plot:
    def __init__(self, x, y, crop_type):
        self.x = x
        self.y = y
        self.crop_type = crop_type
        self.seed_stage = 2
        self.last_growth_time = time.time()
        self.next_growth_time = time.time()
    
    def set_next_growth_time(self):
        # Set the next growth time based on a Gaussian distribution
        self.next_growth_time = time.time() + random.gauss(GROWTH_MEAN[GROWTH_MEAN_IDX], GROWTH_STD_DEV)

    def plant_seed(self):
        if self.seed_stage == 0:
            self.seed_stage = 1

    def grow(self):

        if time.time() >= self.next_growth_time and self.seed_stage < 2:
            self.seed_stage = 2
            self.last_growth_time = time.time()
            self.set_next_growth_time()

    def draw(self, screen, camera_x, camera_y):
        screen.blit(tilled_dirt_texture, (self.x - camera_x, self.y - camera_y))
        if self.crop_type == "Carrots" and self.seed_stage == 2:
            screen.blit(carrot_texture, (self.x - camera_x, self.y - camera_y))
        if self.crop_type == "Potatoes" and self.seed_stage == 2:
            screen.blit(potatoe_texture, (self.x - camera_x, self.y - camera_y))
        if self.crop_type == "Corn" and self.seed_stage == 2:
            screen.blit(corn_texture, (self.x - camera_x, self.y - camera_y))
        if self.crop_type == "Wheat" and self.seed_stage == 2:
            screen.blit(wheat_texture, (self.x - camera_x, self.y - camera_y))

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.character = 0
        self.image = CHARACTERS[self.character][0]
        self.money = money
        self.harvested_crops = {
            "Wheat": 0,
            "Potatoes": 0,
            "Carrots": 0,
            "Corn": 0
        }
        
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
        character_image = pygame.image.load('dirt.png').convert_alpha()
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

    def draw_crop_banner(self, crop, offset_x):
        pygame.draw.rect(screen, CROP_BANNER_COLOR, (250, 30, CROP_BANNER_WIDTH, CROP_BANNER_HEIGHT))
        font = pygame.font.SysFont(None, 23)
        offset_y = 70
        text = f"Upgrade your tractor to farm {crop.lower()}!"
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (offset_x, offset_y))

    def check_collision(self, plots):
        for plot in plots:
            if (plot.x <= self.x <= plot.x + PLOT_WIDTH or plot.x <= self.x + CHAR_WIDTH <= plot.x + PLOT_WIDTH) and \
               (plot.y <= self.y <= plot.y + PLOT_HEIGHT or plot.y <= self.y + CHAR_HEIGHT <= plot.y + PLOT_HEIGHT):
                if plot.crop_type == "Wheat":
                    if plot.seed_stage == 2 and self.harvested_crops["Wheat"] < MAX_HOLD_SIZE[MAX_HOLD_SIZE_IDX]:
                        self.harvested_crops[plot.crop_type] += 1
                        plot.seed_stage = 0
                        plot.set_next_growth_time()
                if plot.crop_type == "Potatoes":
                    if plot.seed_stage == 2 and self.character >= 1 and self.harvested_crops["Potatoes"] < MAX_HOLD_SIZE[MAX_HOLD_SIZE_IDX]:
                        self.harvested_crops[plot.crop_type] += 1
                        plot.seed_stage = 0
                        plot.set_next_growth_time()
                    elif self.character < 1: self.draw_crop_banner(plot.crop_type, 263)
                if plot.crop_type == "Carrots":
                    if plot.seed_stage == 2 and self.character >= 2 and self.harvested_crops["Carrots"] < MAX_HOLD_SIZE[MAX_HOLD_SIZE_IDX]:
                        self.harvested_crops[plot.crop_type] += 1
                        plot.seed_stage = 0
                        plot.set_next_growth_time()
                    elif self.character < 2: self.draw_crop_banner(plot.crop_type, 263)
                if plot.crop_type == "Corn":
                    if plot.seed_stage == 2 and self.character >= 3 and self.harvested_crops["Corn"] < MAX_HOLD_SIZE[MAX_HOLD_SIZE_IDX]:
                        self.harvested_crops[plot.crop_type] += 1
                        plot.seed_stage = 0
                        plot.set_next_growth_time()
                    elif self.character < 3: self.draw_crop_banner(plot.crop_type, 272)
                

# Draw the harvested crop counts on the screen
def draw_harvested_counts(screen,character):
    font = pygame.font.SysFont(None, 24)
    offset_y = 10

    # Draw the background box
    pygame.draw.rect(screen, BACKGROUND_BOX_COLOR, (SCREEN_WIDTH - BACKGROUND_BOX_WIDTH, 0, BACKGROUND_BOX_WIDTH, BACKGROUND_BOX_HEIGHT))

    for crop, count in character.harvested_crops.items():
        text = f"{crop.capitalize()}: {count}/{MAX_HOLD_SIZE[MAX_HOLD_SIZE_IDX]}"
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH - text_surface.get_width() - 10, offset_y))
        offset_y += 30

    # Display the money below the harvested crop counts with up to 5 significant figures
    formatted_money = "{:.5g}".format(character.money)  # Format the money value
    money_text = f"Money: ${formatted_money}"
    money_surface = font.render(money_text, True, MONEY_COLOR)
    
    # Adjust the x-coordinate to ensure the money text fits within the screen
    money_x = SCREEN_WIDTH - money_surface.get_width() - 10
    screen.blit(money_surface, (money_x, offset_y))



# Create the game screen

# ... (inside the main game loop)

# Horizontal path
# Draw the gravel paths
def draw_gravel_paths(screen, camera_x, camera_y):
    # Horizontal path
    pygame.draw.rect(screen, GRAVEL_COLOR, (0 - camera_x, (WORLD_HEIGHT // 2) - (GRAVEL_WIDTH // 2) - camera_y, WORLD_WIDTH, GRAVEL_WIDTH))
    # Vertical path
    pygame.draw.rect(screen, GRAVEL_COLOR, ((WORLD_WIDTH // 2) - (GRAVEL_WIDTH // 2) - camera_x, 0 - camera_y, GRAVEL_WIDTH, WORLD_HEIGHT))


# ... (Plot and Character class definitions)

# Check if character is at the store position
def check_store_position(character):
    global store_open, left_store_area
    if left_store_area and character.x < CHAR_WIDTH and (WORLD_HEIGHT // 2 - STORE_HEIGHT // 2) < character.y < (WORLD_HEIGHT // 2 + STORE_HEIGHT // 2):
        store_open = True
        left_store_area = False 

def draw_store(screen):
    store_rect = pygame.Rect(SCREEN_WIDTH // 2 - STORE_WIDTH // 2, SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2, STORE_WIDTH, STORE_HEIGHT)
    pygame.draw.rect(screen, (150, 150, 150), store_rect)
    font = pygame.font.SysFont(None, 36)

    # Title
    text = font.render("Store", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2 + 20))

    # Get mouse position and check for clicks
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]  # [0] is the left mouse button
    font = pygame.font.SysFont(None, 24)  # Choose an appropriate font size
    message = "Press 'Esc' to leave"
    text_surface = font.render(message, True, (255, 255, 255))  # White text
    position = (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT - 50)  # Adjust the y-coordinate as needed
    screen.blit(text_surface, position)
    # Display upgrades and their current stage
    upgrade_names = [upgrade for upgrade in store_options]
    stages = [store_options[upgrade]["stage"] + 1 for upgrade in store_options]
    upgrade_costs = [store_options[upgrade]["cost"][store_options[upgrade]["stage"]] for upgrade in store_options]
    costs = upgrade_costs + [secret_option_cost]
    offset_y = 80

    for idx, upgrade_name in enumerate(upgrade_names):
        if idx < 4:
            option_text = f"{upgrade_name} ({stages[idx]}/4) - Cost: ${costs[idx]}"
        else:
            option_text = f"{upgrade_name} - Cost: $10,000"

        text_width, text_height = font.size(option_text)
        text_x = store_rect.centerx - text_width // 2
        text_y = SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2 + offset_y
        text_rect = pygame.Rect(text_x, text_y, text_width, text_height)

        # Default color is black
        color = (0, 0, 0)

        # If mouse is hovering over the text, change color to white
        if text_rect.collidepoint(mouse_pos):
            color = (255, 255, 255)
            # If the text is clicked, change color to dark gray
            if mouse_clicked:
                color = (50, 50, 50)
        text = font.render(option_text, True, color)
        screen.blit(text, (text_x, text_y))
        offset_y += 40
    if store_banner:
        draw_store_banner(latestUpgradePurchased, purchaseValidate)
    draw_harvested_counts(screen,character)

def draw_store_banner(upgradePurchased, notValidPurchase):
    pygame.draw.rect(screen, MARKET_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
    font = pygame.font.SysFont(None, 23)
    offset_y = 47
    text = ""
    if(notValidPurchase == "not enough money"):
        text = f"Not enough money!"
        pygame.draw.rect(screen, CROP_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
    elif(notValidPurchase == "maxed out"):
        text = f"Upgrade already maxed out!!"
        pygame.draw.rect(screen, CROP_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
    else:
        if(latestUpgradePurchased == "increase_fertilizer"):
            text = f"Fertilizer upgrade purchased!"
            pygame.draw.rect(screen, MARKET_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
        elif(latestUpgradePurchased == "increase_tractor"):
            text = f"Tractor upgrade purchased!"
            pygame.draw.rect(screen, MARKET_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
        elif(latestUpgradePurchased == "increase_speed"):
            text = f"Speed upgrade purchased!"
            pygame.draw.rect(screen, MARKET_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
        elif(latestUpgradePurchased == "increase_inventory"):
            text = f"Inventory upgrade purchased!"
            pygame.draw.rect(screen, MARKET_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (SCREEN_WIDTH/2 - 100, offset_y))

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
    # Get mouse position and check for clicks
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]  # [0] is the left mouse button
    # Display selling options
    options = ["Sell Wheat ($1)", "Sell Potatoes ($4)", "Sell Carrots ($7)", "Sell Corn ($10)", "Sell All Crops"]
    font = pygame.font.SysFont(None, 24)  # Choose an appropriate font size
    message = "Press 'Esc' to leave"
    text_surface = font.render(message, True, (255, 255, 255))  # White text
    position = (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT - 50)  # Adjust the y-coordinate as needed
    screen.blit(text_surface, position)
    offset_y = 80
    for option in options:
        # Get the text width and height for the current option
        option_width, option_height = font.size(option)
        
        # Calculate the x-coordinate to center the text within market_rect
        text_x = market_rect.centerx - option_width // 2
        text_y = SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2 + offset_y

        # Calculate the position and size of the text to detect hover
        text_rect = pygame.Rect(text_x, text_y, option_width, option_height)
        # Default color is black
        color = (0, 0, 0)
        # If mouse is hovering over the text, change color to white
        if text_rect.collidepoint(mouse_pos):
            color = (255, 255, 255)
            # If the text is clicked, change color to dark gray
            if mouse_clicked:
                color = (50, 50, 50)
        text = font.render(option, True, color)
        screen.blit(text, (text_x, text_y))
        offset_y += 40
    if market_banner_on:
        draw_market_banner(latestCrop, latestSoldValue, latestSoldAmount)
    draw_harvested_counts(screen,character)

def draw_market_banner(crop, soldValue, soldAmount):
    pygame.draw.rect(screen, MARKET_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
    font = pygame.font.SysFont(None, 23)
    offset_y = 47
    text = ""
    if(crop == "all crops"):
        if soldValue == 0:
            text = f"No crops to sell!"
            pygame.draw.rect(screen, CROP_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))

        else:
            text = f"Sold all crops for {soldValue}!"
            pygame.draw.rect(screen, MARKET_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))

    else:
        if soldValue == 0:
            text = f"No {crop.lower()} to sell!"
            pygame.draw.rect(screen, CROP_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
        else:
            text = f"Sold {soldAmount} {crop.lower()} for {soldValue}!"
            pygame.draw.rect(screen, MARKET_BANNER_COLOR, (SCREEN_WIDTH/2 - MARKET_BANNER_WIDTH/2, 15, MARKET_BANNER_WIDTH, MARKET_BANNER_HEIGHT))
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (SCREEN_WIDTH/2 - 70, offset_y))

def draw_building(screen, x, y, label, camera_x, camera_y, flip):
    """Draws a building with a label at the specified position."""
    # Building rectangle
    if flip:
        newimage = pygame.transform.flip(building_image, True, False)
    else: newimage = building_image
    screen.blit(newimage, (x - camera_x, y - camera_y))
    # Label for the building
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(label, True, (255, 255, 255))  # Black label
    screen.blit(text_surface, (x - camera_x + BUILDING_WIDTH // 2 - text_surface.get_width() // 2, y - camera_y + BUILDING_HEIGHT // 2 - text_surface.get_height() // 2))

def run_secret_ending(screen):
    large_image = pygame.image.load("big_john.png")

    # Get screen dimensions
    screen_width, screen_height = screen.get_size()

    # Calculate position to center the image on the screen
    image_width, image_height = large_image.get_size()
    image_x = (screen_width - image_width) // 2
    image_y = (screen_height - image_height) // 2

    # Image rectangle for collision detection
    image_rect = pygame.Rect(image_x, image_y, image_width, image_height)

    # Prepare the "Thanks for playing" text
    font_large = pygame.font.SysFont(None, 36)  # Adjust font size as needed
    text_surface_large = font_large.render("Thanks for playing", True, (255, 255, 255))  # White text
    position_large = (SCREEN_WIDTH // 2 - text_surface_large.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface_large.get_height() // 2)
    

    # Render "not" with a smaller font size
    font_small = pygame.font.SysFont(None, 14)  # Adjust font size as needed
    text_surface_small = font_small.render("not", True, (255, 255, 255))  # White text
    position_small = (SCREEN_WIDTH // 2 - text_surface_large.get_width() // 2  , position_large[1] + text_surface_large.get_height() + 20)  # Positioned right below "Thanks for playing"
    

    # Render "sponsored by John Deere"
    text_surface_sponsor = font_large.render("sponsored by John Deere", True, (255, 255, 255))  # White text
    position_sponsor = (position_small[0] + text_surface_small.get_width() + 10 , position_small[1] - 10)  # Positioned to the right of "not"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for mouse click event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                x, y = pygame.mouse.get_pos()
                # If click is outside the image, close the game
                if not image_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

        # Draw the image centered on the screen
        screen.blit(large_image, (image_x, image_y))
        
        # Draw the text on top of the image
        screen.blit(text_surface_large, position_large)
        screen.blit(text_surface_small, position_small)
        screen.blit(text_surface_sponsor, position_sponsor)

        pygame.display.flip()


# Adjust plot generation for the 2x2 grid with gravel paths
plots = []
sections = [
    {"start_x": 0, "end_x": WORLD_WIDTH // 2 - GRAVEL_WIDTH , "start_y": 0, "end_y": WORLD_HEIGHT // 2 - GRAVEL_WIDTH, "crop": "Wheat"},
    {"start_x": WORLD_WIDTH // 2 + GRAVEL_WIDTH, "end_x": WORLD_WIDTH, "start_y": 0, "end_y": WORLD_HEIGHT // 2 - GRAVEL_WIDTH, "crop": "Potatoes"},
    {"start_x": 0, "end_x": WORLD_WIDTH // 2 - GRAVEL_WIDTH, "start_y": WORLD_HEIGHT // 2 + GRAVEL_WIDTH, "end_y": WORLD_HEIGHT, "crop": "Carrots"},
    {"start_x": WORLD_WIDTH // 2 + GRAVEL_WIDTH , "end_x": WORLD_WIDTH, "start_y": WORLD_HEIGHT // 2 + GRAVEL_WIDTH , "end_y": WORLD_HEIGHT, "crop": "Corn"}
]

for section in sections:
    for x in range(section["start_x"], section["end_x"], PLOT_WIDTH + PLOT_MARGIN):
        for y in range(section["start_y"], section["end_y"], PLOT_HEIGHT + PLOT_MARGIN):
            plots.append(Plot(x, y, section["crop"]))

character = Character(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

store_options = {
    "Upgrade Tractor": {
        "cost": [100,200,400,800],
        "stage": 0,
        "action": "increase_tractor"
    },
    "Upgrade Fertilizer": {
        "cost": [100,200,400,800],
        "stage": 0,
        "action": "increase_fertilizer"
    },
    "Upgrade Speed": {
        "cost": [100,200,400,800],
        "stage": 0,
        "action": "increase_speed"
    },
    "Upgrade Inventory": {
        "cost": [100,200,400,800],
        "stage": 0,
        "action": "increase_inventory"
    },
    "Secret?": {
        "cost": [10000],
        "stage": 0,
        "action": "secret_ending"
    }
    # You can add more options here in a similar manner
}

def get_option_rect(index):
    option_width = 200  # Or set this to the actual width of the option
    option_x = SCREEN_WIDTH // 2 - option_width // 2
    option_y = SCREEN_HEIGHT // 2 - STORE_HEIGHT // 2 + 80 + index * option_height
    return pygame.Rect(option_x, option_y, option_width, option_height)

# Main game loop
running = True
while running:
    screen.fill(DIRT)
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Close store/market with ESC key
                store_open = False
                market_open = False
                market_banner_on = False
                store_banner = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # Check which option was clicked and update money and crops accordingly
            option_height = 40
            if market_open:
                for index, option in enumerate(["Sell Wheat", "Sell Potatoes", "Sell Carrots", "Sell Corn", "Sell All Crops"]):
                    option_rect = get_option_rect(index)
                    
                    if option_rect.collidepoint(x, y):  # Use the collidepoint method to check if the mouse click was within the option's area
                        # Handle the click for this option
                        
                        if option == "Sell All Crops":
                            totalProfit = 0
                            for crop_type in character.harvested_crops:
                                totalProfit += character.harvested_crops[crop_type] * sell_amount[crop_type]
                                character.money += character.harvested_crops[crop_type] * sell_amount[crop_type]
                                character.harvested_crops[crop_type] = 0
                            latestSoldValue = totalProfit
                            latestCrop = "all crops"
                            latestSoldAmount = 0
                            market_banner_on = True
                        else:
                            crop_type = option.split(" ")[1]
                            cropProfit = character.harvested_crops[crop_type] * sell_amount[crop_type]
                            character.money += cropProfit
                            latestSoldValue = cropProfit
                            latestCrop = crop_type
                            latestSoldAmount = character.harvested_crops[crop_type]
                            market_banner_on = True
                            character.harvested_crops[crop_type] = 0
            if store_open:
                for index, (option_name, option_data) in enumerate(store_options.items()):
                    option_rect = get_option_rect(index)
                    if option_rect.collidepoint(x, y):
                        if character.money >= option_data["cost"][option_data["stage"]] and option_data["stage"] < 3:
                            if option_data["action"] == "increase_tractor":
                                character.character += 1
                                character.money -= option_data["cost"][option_data["stage"]]
                                option_data["stage"] += 1
                                latestUpgradePurchased = "increase_tractor"
                                purchaseValidate = "upgrade purchased"
                                store_banner = True
                            if option_data["action"] == "increase_fertilizer":
                                GROWTH_MEAN_IDX += 1
                                GROWTH_STD_DEV = GROWTH_MEAN[GROWTH_MEAN_IDX]/4
                                character.money -= option_data["cost"][option_data["stage"]]
                                option_data["stage"] += 1
                                latestUpgradePurchased = "increase_fertilizer"
                                purchaseValidate = "upgrade purchased"
                                store_banner = True
                            if option_data["action"] == "increase_speed":
                                CHAR_SPEED_IDX += 1
                                character.money -= option_data["cost"][option_data["stage"]]
                                option_data["stage"] += 1
                                latestUpgradePurchased = "increase_speed"
                                purchaseValidate = "upgrade purchased"
                                store_banner = True
                            if option_data["action"] == "increase_inventory":
                                MAX_HOLD_SIZE_IDX += 1
                                character.money -= option_data["cost"][option_data["stage"]]
                                option_data["stage"] += 1
                                latestUpgradePurchased = "increase_inventory"
                                purchaseValidate = "upgrade purchased"
                                store_banner = True
                            if option_data["action"] == "secret_ending":
                                run_secret_ending(screen)
                        elif character.money < option_data["cost"][option_data["stage"]]:
                            latestUpgradePurchased = None
                            purchaseValidate = "not enough money"
                            store_banner = True
                        elif option_data["stage"] == 3:
                            latestUpgradePurchased = None
                            purchaseValidate = "maxed out"
                            store_banner = True

    if store_open:
        draw_store(screen)
        pygame.display.flip()
        continue 

    if market_open:
        draw_market(screen)
        pygame.display.flip()
        continue


    keys = pygame.key.get_pressed()
    if not store_open and not market_open:
        dx, dy = 0, 0  # Initialize changes in x and y to 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dy -= CHAR_SPEED[CHAR_SPEED_IDX]
        if keys[pygame.K_s]:
            dy += CHAR_SPEED[CHAR_SPEED_IDX]
        if keys[pygame.K_a]:
            dx -= CHAR_SPEED[CHAR_SPEED_IDX]
        if keys[pygame.K_d]:
            dx += CHAR_SPEED[CHAR_SPEED_IDX]

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

    for x in range(0, WORLD_WIDTH, scaled_gravel_texture.get_width()):
        for y in range(WORLD_HEIGHT // 2 - PATH_WIDTH // 2 -2 , WORLD_HEIGHT // 2 -2, scaled_gravel_texture.get_height()):
            screen.blit(scaled_gravel_texture, (x - camera_x, y - camera_y))

    # Vertical path
    for y in range(0, WORLD_HEIGHT, scaled_gravel_texture.get_height()):
        for x in range(WORLD_WIDTH // 2 - PATH_WIDTH // 2 - 5 , WORLD_WIDTH // 2 + PATH_WIDTH // 2-5, scaled_gravel_texture.get_width()):
            screen.blit(scaled_gravel_texture, (x - camera_x, y - camera_y))
        
    for plot in plots:
        screen.blit(scaled_dirt_texture, (plot.x - camera_x - DIRT_MARGIN, plot.y - camera_y - DIRT_MARGIN))
        if (plot.x + PLOT_WIDTH + DIRT_MARGIN >= camera_x and plot.x - DIRT_MARGIN <= camera_x + SCREEN_WIDTH) and \
           (plot.y + PLOT_HEIGHT + DIRT_MARGIN >= camera_y and plot.y - DIRT_MARGIN <= camera_y + SCREEN_HEIGHT):
            plot.grow()
            plot.draw(screen, camera_x, camera_y)

        
    draw_building(screen, 0, WORLD_HEIGHT // 2 - BUILDING_HEIGHT // 2, "Store", camera_x, camera_y, False)
    draw_building(screen, WORLD_WIDTH - BUILDING_WIDTH, WORLD_HEIGHT // 2 - BUILDING_HEIGHT // 2, "Market", camera_x, camera_y, True)

    character.check_collision(plots)  # Plant seeds if character collides with a plot
    
    character.draw(screen, camera_x, camera_y)
    draw_harvested_counts(screen,character)

    pygame.display.flip()
    pygame.time.wait(50)

pygame.quit()
