import pygame
import random
import time
import os
# Initialize Pygame
pygame.init()
# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Werewolf Chase")
# Clock display settings
font = pygame.font.Font(None, 36)  # Choose a font
# Colors
white = (255, 255, 255)
black = (0, 0, 0)
# Player
player_size = 70
player_x = 50
player_y = 50
player_speed = 10
player_health= 5
player_image = None

# Werewolf
werewolf_size = 50
werewolf_x = random.randint(100, screen_width - werewolf_size)
werewolf_y = random.randint(100, screen_height - werewolf_size)
werewolf_speed = 1
werewolf_health = 100  # Werewolf health
# House
house_x = 600
house_y = 300
house_width = 100
house_height = 100

door_x = 665 # Adjust as needed
door_y = 50
door_width = 55
door_height = 55

villager_size = 50
villager_x = 380  # Initial x-coordinate
villager_y = 100  # Initial y-coordinate
villager_speed = 2
villager_direction = 1  # 1 for moving right, -1 for moving left

# Movement boundaries for the villager
villager_min_x = 380
villager_max_x = 550
villager_min_y = 380
villager_max_y = 550

cave_x = 40
cave_y = 100
cave_width = 30
cave_height = 20
in_cave = False

cave_exit_area_x= 45
cave_exit_area_y= 250
cave_exit_area_height=20
cave_exit_area_width= 30

fors_x = 200 # Adjust as needed
fors_y = 125
fors_width = 70
fors_height = 85

gamze_x = 200
gamze_y = 5
gamze_width = 60
gamze_height = 70

health_bar_x = 100
health_bar_y = 10
health_bar_width = 25
health_bar_height = 20
heart_spacing = 25

item_size = 30
# Sword attack variables
sword_damage = 20  # Damage the sword deals
attacking = False  # Flag to indicate if the player is attacking
attack_cooldown = 500  # Cooldown in milliseconds between attacks
last_attack_time = 0   # Time of the last attack
attack_duration = 150 # **Increased duration of the 'attacking' state (longer attack window)**

fill_width = int(health_bar_width * (player_health / 5))

# Mining Processing Object
processing_station_x = 600
processing_station_y = 125
processing_station_width = 80
processing_station_height = 80
at_processing_station = False # Flag to indicate if player is at the station

# İşlem İstasyonu Görseli
processing_station_image = None # Görsel için değişken

# İşlem istasyonu görselini yükle ve boyutlandır
try:
    processing_station_image = pygame.image.load("craft.png") # Görsel dosyanızın adı
    processing_station_image = pygame.transform.scale(processing_station_image, (processing_station_width, processing_station_height))
except pygame.error as e:
    print(f"Hata: İşlem istasyonu görseli yüklenemedi: {e}")
    processing_station_image = None # Görsel yüklenemezse None olarak kalır

# Kılıç (Sword) objesi için görsel yükleme
try:
    sword_image = pygame.image.load("Emerald_Sword-Photoroom.png")  # Kılıç görseli dosya yolu
    sword_image = pygame.transform.scale(sword_image, (item_size, item_size)) # item_size kılıç boyutu için kullanılabilir
except pygame.error as e:
    print(f"Error loading sword image: {e}")
    sword_image = None # Görsel yüklenemezse None olarak ayarla

# Inventory icon (load the image)
try:
    inventory_icon_image = pygame.image.load("inventory_icon.png")  # Replace with your inventory icon image file
    # Scale the inventory icon to the desired size
    inventory_icon_image = pygame.transform.scale(inventory_icon_image, (40, 40)) # Example size, adjust as needed
except pygame.error as e:
    print(f"Error loading inventory icon image: {e}")
    inventory_icon_image = None # Handle missing image


# Oyuncunun kılıcı olup olmadığını takip eden bir bayrak
has_sword = False
# Werewolf initially hidden
werewolf_visible = False

# Background image
background_image = pygame.image.load("img.png") # Replace with your image
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


cave_exit_image = None # Mağara çıkışı görseli için değişken
cave_interior_background_image = None # Mağara içi görseli için yeni değişken

try:
    cave_interior_background_image = pygame.image.load("cave.jpg") # Mağara içi arkaplan görseli
    cave_interior_background_image = pygame.transform.scale(cave_interior_background_image, (screen_width, screen_height)) # Ekran boyutuna boyutlandırın
except pygame.error as e:
    print(f"Error loading cave interior background image: {e}")

# Kılıç yapımı için gereken madenler (örnek: 2 Altın Cevheri, 3 Demir Cevheri)
sword_recipe = {
    "Gold Ore": 2,
    "Iron Ore": 3,
}
# Clock and time variables
clock = pygame.time.Clock()
game_start_time = time.time()  # Record the game start time
fast_time_multiplier = 500   # Time passes 2 times faster
# Display the time (fast forward)
elapsed_time = (time.time() - game_start_time) * fast_time_multiplier
hours = int(elapsed_time // 3600) % 24  # Get hours (0-23)
minutes = int((elapsed_time % 3600) // 60)  # Get minutes (0-59)

# Maden nesneleri (liste olarak tutulur)
mine_objects = []
mine_object_size = 20
mine_image = None # Maden görseli için değişken

has_sword = False


# Item class
class Item:
    def __init__(self, name, description, damage=0):
        self.name = name
        self.description = description
        self.damage = damage # Damage value for weapons

# Bu görselleri proje klasörünüze eklemeniz gerekmektedir.
mine_images = {
    "Gold Ore": pygame.image.load("maden-Photoroom.png") if os.path.exists("maden-Photoroom.png") else None,
    "Iron Ore": pygame.image.load("maden-Photoroom.png") if os.path.exists("maden-Photoroom.png") else None,
    # İstediğiniz kadar maden türü ekleyebilirsiniz
}
for name, img in mine_images.items():
    if img:
        mine_images[name] = pygame.transform.scale(img, (mine_object_size, mine_object_size))

# Kılıç objesi (istasyonda oluşturulduğu varsayılıyor)
sword_item = Item("Kılıç", "Keskin bir kılıç.")
# Kılıç objesinin haritadaki başlangıç pozisyonu (istasyonda olduğu varsayıldı)
sword_object_rect = pygame.Rect(processing_station_x + processing_station_width // 2 - player_size // 2, processing_station_y + processing_station_height // 2 - player_size // 2, player_size, player_size)

# Mağara içinde rastgele maden nesneleri oluştur
def create_mine_objects(count=10):
  global mine_objects
  mine_objects = [] # Önceki madenleri temizle
  mine_types = list(mine_images.keys()) # Mevcut maden türleri
  if not mine_types:
    print("Warning: No mine images loaded, cannot create mine objects.")
    return
  if not cave_interior_background_image:
      print("Warning: Cave background image not loaded, cannot place mine objects.")
      return

  # Madenlerin oluşturulabileceği alanın sınırlarını belirle (mağara görselinin içinde)
  min_mx = cave_x + 10 # Mağara görselinin sol kenarından içeride
  max_mx = cave_x + cave_interior_background_image.get_width() - mine_object_size - 10 # Mağara görselinin genişliği kullanıldı
  min_my = cave_y + 10 # Mağara görselinin üst kenarından içeride
  max_my = cave_y + cave_interior_background_image.get_height() - mine_object_size - 10 # Mağara görselinin yüksekliği kullanıldı


  # Eğer geçerli bir aralık yoksa maden oluşturma
  if max_mx < min_mx or max_my < min_my:
      print(f"Warning: Cannot place mine object. Cave background image size or mine size is too restrictive.")
      return # Maden oluşturmayı durdur


  for _ in range(count):
    # Madenleri mağara ana görselinin sınırları içinde rastgele yerleştir
    mx = random.randint(min_mx, max_mx)
    my = random.randint(min_my, max_my)

    mine_type = random.choice(mine_types) # Rastgele maden türü seç
    # Maden nesnesini oluştururken konumu ve türünü sakla
    mine_objects.append({"rect": pygame.Rect(mx, my, mine_object_size, mine_object_size), "type": mine_type})

create_mine_objects() # Oyun başladığında madenleri oluştur
# Envanter
inventory = []
inventory_display = False # Envanter ekranının açık olup olmadığını kontrol etme

# Envanter görüntüleme fonksiyonu
def display_inventory():
    inventory_screen = pygame.Surface((screen_width, screen_height))
    inventory_screen.fill(white)

    font = pygame.font.Font(None, 36)
    text_y = 50

    # Envanter başlığı
    title_text = font.render("Envanter", True, black)
    title_rect = title_text.get_rect(center=(screen_width // 2, 30))
    inventory_screen.blit(title_text, title_rect)

    # Envanterdeki öğeleri say ve grupla
    item_counts = {}
    for item in inventory:
        item_counts[item.name] = item_counts.get(item.name, 0) + 1

    # Envanterdeki öğeleri listele
    if not item_counts:
        empty_text = font.render("Envanteriniz boş.", True, black)
        inventory_screen.blit(empty_text, (50, text_y))
    else:
        for item_name, count in item_counts.items():
            item_text = font.render(f"{item_name}: {count}", True, black)
            inventory_screen.blit(item_text, (50, text_y))
            text_y += 40

    # Kapatma talimatı
    close_text = font.render("Envanteri kapatmak için ESC tuşuna basın", True, black)
    close_rect = close_text.get_rect(center=(screen_width // 2, screen_height - 50))
    inventory_screen.blit(close_text, close_rect)

    # Envanter açıkken olay döngüsü
    waiting_for_close = True
    while waiting_for_close:
        # Envanter ikonunu çiz ve Rect objesini al (envanter açıkken de tıklanabilir olması için)
        inventory_icon_rect = draw_inventory_icon() # draw_inventory_icon fonksiyonunu burada çağırdık

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_i: # ESC veya 'i' tuşu ile kapat
                    waiting_for_close = False
            if event.type == pygame.MOUSEBUTTONDOWN: # Fare tıklamasını kontrol et
                if event.button == 1: # Sol tıklama
                     if inventory_icon_rect.collidepoint(event.pos):
                         waiting_for_close = False # Envanter ikonuna tıklanırsa envanteri kapat

        # Envanter ekranını güncelle (maden toplandığında envanter içeriği değişebilir)
        screen.blit(inventory_screen, (0, 0))
        # Envanter ikonunu tekrar çiz (mouse olaylarından sonra üstte kalması için)
        if inventory_icon_image:
            screen.blit(inventory_icon_image, (inventory_icon_rect.x, inventory_icon_rect.y))
        else:
             # Görsel yoksa varsayılan kareyi ve metni çiz
            pygame.draw.rect(screen, (150, 150, 150), inventory_icon_rect)
            font_icon = pygame.font.Font(None, 30)
            icon_text = font_icon.render("Env", True, black)
            icon_text_rect = icon_text.get_rect(center=inventory_icon_rect.center)
            screen.blit(icon_text, icon_text_rect)
        pygame.display.flip()
        clock.tick(60)
    # Envanter kapatıldığında inventory_display bayrağını False yap
    global inventory_display
    inventory_display = False


# Envanter ikonunu sağ üst köşede çizme fonksiyonu
def draw_inventory_icon():
    # Envanter ikonu boyutu ve konumu (sağ üst köşe)
    icon_size = 40
    icon_x = screen_width - icon_size - 10  # Sağ kenardan 10 piksel boşluk
    icon_y = 10 # Üst kenardan 10 piksel boşluk
    inventory_icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)

    # Envanter ikonunu görsel olarak çiz
    if inventory_icon_image:
        screen.blit(inventory_icon_image, (icon_x, icon_y))
    else:
        # Görsel yoksa varsayılan kareyi ve metni çiz
        pygame.draw.rect(screen, (150, 150, 150), inventory_icon_rect)
        font_icon = pygame.font.Font(None, 30)
        icon_text = font_icon.render("Env", True, black)
        icon_text_rect = icon_text.get_rect(center=inventory_icon_rect.center)
        screen.blit(icon_text, icon_text_rect)

    return inventory_icon_rect # Tıklama algılaması için Rect'i döndür

# Function to check if the player has the required items in inventory
def check_inventory_for_recipe(recipe):
    item_counts = {}
    for item in inventory:
        item_counts[item.name] = item_counts.get(item.name, 0) + 1

    for required_item, required_count in recipe.items():
        if item_counts.get(required_item, 0) < required_count:
            return False # Not enough of this item

    return True # Has all required items in sufficient quantities

# Function to remove items from inventory
def remove_items_from_inventory(recipe):
    for required_item, required_count in recipe.items():
        count_to_remove = required_count
        # Remove items from the end of the list to avoid indexing issues
        for i in range(len(inventory) - 1, -1, -1):
            if inventory[i].name == required_item and count_to_remove > 0:
                inventory.pop(i)
                count_to_remove -= 1
            if count_to_remove == 0:
                break
# Mağara ekranı fonksiyonu
def cave_screen():
    global player_x, player_y, in_cave, mine_objects, inventory, inventory_display

    in_cave = True
    player_x = player_x
    player_y = player_y

    # Mağara çıkışı için bir alan belirle (bu artık mağara içindeki bir kapı/geçit)
    # Bu çıkış alanı mağara duvarlarından birinde veya ortasında olabilir
    cave_exit_x = screen_width // 2 - 30 # X position relative to screen width
    cave_exit_y = screen_height - 50   # Y position relative to screen height
    cave_exit_width = 30             # **Independent width**
    cave_exit_height = 30            # **Independent height**
    cave_exit_area = pygame.Rect(cave_exit_x, cave_exit_y, cave_exit_width, cave_exit_height)

    # Envanter ikonu konumu
    inventory_icon_rect = pygame.Rect(750, 10, 40, 40) # Use a rect to handle clicks easily

    # Duvar kalınlığı
    wall_thickness =10

    while in_cave:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i: # 'i' tuşu ile envanteri aç/kapat
                    inventory_display = not inventory_display
                    if inventory_display:
                      display_inventory()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    if inventory_icon_rect.collidepoint(event.pos):
                        inventory_display = True
                        display_inventory()

        keys = pygame.key.get_pressed()
        # Oyuncu hareket sınırları mağara görseline göre ayarlanmalı
        # Bu örnekte ekran sınırlarını kullanıyoruz. Mağara görselinize göre duvar kontrolleri ekleyin.
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
            player_y += player_speed

        # Mağara çıkışı kontrolü
        if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(cave_exit_area):
            in_cave = False # Mağaradan çıkış

        # Maden toplama kontrolü
        collected_mines = []
        for mine_obj in mine_objects:
            if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(mine_obj["rect"]):
                inventory.append(Item(mine_obj["type"], f"Bir parça {mine_obj['type']}."))
                collected_mines.append(mine_obj)

        # Toplanan madenleri listeden çıkar
        for collected_mine in collected_mines:
            if collected_mine in mine_objects:
              mine_objects.remove(collected_mine)


        # Ekranı çiz
        if cave_interior_background_image:
            screen.blit(cave_interior_background_image, (0, 0)) # Mağara içi arkaplan görselini çiz
        else:
            screen.fill(cave_background_color) # Görsel yoksa varsayılan renk ile doldur

        # Mağara duvarlarını çiz (ekran boyutunda)
        wall_color = black # Duvar rengi
        pygame.draw.rect(screen, wall_color, (0, 0, screen_width, wall_thickness)) # Üst duvar
        pygame.draw.rect(screen, wall_color, (0, screen_height - wall_thickness, screen_width, wall_thickness)) # Alt duvar
        pygame.draw.rect(screen, wall_color, (0, 0, wall_thickness, screen_height)) # Sol duvar
        pygame.draw.rect(screen, wall_color, (screen_width - wall_thickness, 0, wall_thickness, screen_height)) # Sağ duvar


        # Maden nesnelerini çiz
        for mine_obj in mine_objects:
            mine_rect = mine_obj["rect"]
            mine_type = mine_obj["type"]
            mine_img = mine_images.get(mine_type)
            if mine_img:
                screen.blit(mine_img, mine_rect) # Görseli çiz
            else:
                pygame.draw.rect(screen, yellow, mine_rect) # Görsel yoksa sarı kare çiz


        # Oyuncuyu çiz
        player_image = pygame.image.load("prenses.gif")
        player_image = pygame.transform.scale(player_image, (player_size, player_size))
        screen.blit(player_image, (player_x, player_y))  # Scale to player size

        # Envanter ikonunu görsel olarak çiz
        if inventory_icon_image:
            screen.blit(inventory_icon_image, (inventory_icon_rect.x, inventory_icon_rect.y))
        else:
            # Görsel yoksa varsayılan kareyi ve metni çiz
            pygame.draw.rect(screen, (150, 150, 150), inventory_icon_rect)
            font_icon = pygame.font.Font(None, 30)
            icon_text = font_icon.render("Env", True, black)
            icon_text_rect = icon_text.get_rect(center=inventory_icon_rect.center)
            screen.blit(icon_text, icon_text_rect)


        pygame.display.flip()
        clock.tick(60)

    # **BURASI YENİ EKLENDİ:** Mağaradan çıkarken envanteri kapat
    inventory_display = False

    return player_x, player_y
def main_menu():
    menu_screen = pygame.Surface((screen_width, screen_height))

    # Load your background image (make sure it's wider than the screen)
    try:
        # Replace with your image file path for the moving background
        background_image = pygame.image.load("arkaplan.jpg")
        background_width = background_image.get_width()
        background_x = 0
    except pygame.error as e:
        print(f"Error loading moving background image: {e}")
        background_image = None
        menu_screen.fill(white)

    # Load button background images
    try:
        # Replace with your image file paths for the buttons
        new_game_button_image = pygame.image.load("button-Photoroom.png").convert_alpha()
        quit_button_image = pygame.image.load("button-Photoroom.png").convert_alpha()

        # Scale button images to match button sizes
        new_game_button_image = pygame.transform.scale(new_game_button_image, (200, 60))
        quit_button_image = pygame.transform.scale(quit_button_image, (200, 60))

    except pygame.error as e:
        print(f"Error loading button images: {e}")
        new_game_button_image = None
        quit_button_image = None
        # Fallback to drawing colored rectangles if images fail to load
        button_fallback_color = black


    font_title = pygame.font.Font(None, 100)
    font_button = pygame.font.Font(None, 50)

    title_text = font_title.render("Werewolf Chase", True, black)
    title_rect = title_text.get_rect(center=(screen_width // 2, 150))

    # Create button rectangles (positions and sizes)
    new_game_button_rect = pygame.Rect(screen_width // 2 - 100, 300, 200, 60)
    quit_button_rect = pygame.Rect(screen_width // 2 - 100, 400, 200, 60)

    new_game_text = font_button.render("Yeni Oyun", True, white)
    quit_text = font_button.render("Çıkış", True, white)

    new_game_text_rect = new_game_text.get_rect(center=new_game_button_rect.center)
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button_rect.collidepoint(event.pos):
                    in_menu = False  # Start a new game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        # Move the background
        if background_image:
            background_x -= 1 # Adjust the value to change the speed and direction
            if background_x < -background_width + screen_width:
                background_x = 0

            menu_screen.blit(background_image, (background_x, 0))
            menu_screen.blit(background_image, (background_x + background_width, 0))
        else:
            menu_screen.fill(white)

        # Draw menu elements on top of the background
        menu_screen.blit(title_text, title_rect)

        # Draw button images or fallback color rectangles
        if new_game_button_image:
            menu_screen.blit(new_game_button_image, new_game_button_rect)
        else:
            pygame.draw.rect(menu_screen, button_fallback_color, new_game_button_rect)

        if quit_button_image:
            menu_screen.blit(quit_button_image, quit_button_rect)
        else:
            pygame.draw.rect(menu_screen, button_fallback_color, quit_button_rect)


        # Draw the button text on top of the button backgrounds
        menu_screen.blit(new_game_text, new_game_text_rect)
        menu_screen.blit(quit_text, quit_text_rect)

        screen.blit(menu_screen, (0, 0))
        pygame.display.flip()
        clock.tick(60)

# Call the main menu function before the main game loop
main_menu()

def processing_screen():
    global inventory, werewolf_health # Access global variables
    processing_screen_active = True
    required_ores = {"Gold Ore": 2, "Iron Ore": 3} # Example recipe

    while processing_screen_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Exit processing screen
                    processing_screen_active = False
                if event.key == pygame.K_c: # Press 'c' to attempt crafting
                    craft_sword(required_ores)


        # Drawing the processing screen
        screen.fill(white) # White background for the processing screen
        font = pygame.font.Font(None, 36)

        # Display title
        title_text = font.render("Mining Processing Station", True, black)
        title_rect = title_text.get_rect(center=(screen_width // 2, 50))
        screen.blit(title_text, title_rect)

        # Display crafting recipe
        recipe_y = 150
        screen.blit(font.render("Crafting Recipe: Sword", True, black), (50, recipe_y))
        recipe_y += 40
        for ore, count in required_ores.items():
            screen.blit(font.render(f"- {count} x {ore}", True, black), (70, recipe_y))
            recipe_y += 30

        # Display instructions
        screen.blit(font.render("Press 'c' to Craft Sword", True, black), (50, recipe_y + 50))
        screen.blit(font.render("Press ESC to Exit", True, black), (50, recipe_y + 90))

        pygame.display.flip()
        clock.tick(60)

# Function to craft a sword
def craft_sword(recipe):
    global inventory
    can_craft = True
    temp_inventory = list(inventory) # Create a copy to check availability

    # Check if player has required items
    for ore, count in recipe.items():
        ore_count_in_inventory = sum(1 for item in temp_inventory if item.name == ore)
        if ore_count_in_inventory < count:
            can_craft = False
            print(f"Not enough {ore} to craft the sword.")
            break

    if can_craft:
        # Remove required items from inventory
        for ore, count in recipe.items():
            removed_count = 0
            i = 0
            while removed_count < count and i < len(temp_inventory):
                if temp_inventory[i].name == ore:
                    temp_inventory.pop(i)
                    removed_count += 1
                else:
                    i += 1
        inventory = temp_inventory # Update the actual inventory

        # Add the crafted sword to inventory
        inventory.append(Item("Sword", "A sharp sword for fighting.", damage=10)) # Add damage attribute
        print("Sword crafted successfully!")
    else:
        print("Cannot craft the sword. Missing materials.")

def new_screen(background_image_path, player_x_new, player_y_new):
    global player_x, player_y, inventory_display # inventory_display'i burada da kullanmak için global yapın
    try:
        new_background = pygame.image.load(background_image_path)
        new_background = pygame.transform.scale(new_background, (screen_width, screen_height))

        pygame.display.flip()

        villager_x = 380
        villager_y = 100
        villager_direction = 1

        # Event handling for the new screen
        in_new_screen = True
        while in_new_screen:
          # Envanter ikonunu çiz ve Rect objesini al
          inventory_icon_rect = draw_inventory_icon()  # Envanter ikonunu her zaman çiz
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  quit()
              if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press Escape to go back
                     in_new_screen = False
                if event.key == pygame.K_i:  # 'i' tuşu ile envanteri aç/kapat
                      inventory_display = not inventory_display
                      if inventory_display:
                          display_inventory()  # Envanter ekranını göster
                      else:
                          # Envanter kapatıldığında evin ekranını tekrar çizmek gerekebilir
                          pass  # Şu anki mantıkta display_inventory() dışındaki döngü otomatik çiziyor

              if event.type == pygame.MOUSEBUTTONDOWN:
                  if event.button == 1:  # Sol tıklama
                      if inventory_icon_rect.collidepoint(event.pos):
                          inventory_display = True
                          display_inventory()  # Envanter ekranını göster

          # Envanter açık değilse evin içindeki hareket ve çizimleri yap
          if not inventory_display:
              keys = pygame.key.get_pressed()
              if keys[pygame.K_LEFT] and player_x > 0:
                  player_x -= player_speed
              if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
                  player_x += player_speed
              if keys[pygame.K_UP] and player_y > 0:
                  player_y -= player_speed
              if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
                  player_y += player_speed
              screen.blit(new_background, (0, 0))

              player_image = pygame.image.load("prenses.gif")
              player_image = pygame.transform.scale(player_image, (player_size, player_size))
              screen.blit(player_image, (player_x, player_y))  # Scale to player size,

              villager_x += villager_speed * villager_direction
              if villager_x >= villager_max_x or villager_x <= villager_min_x:
                 villager_direction *= -1  # Reverse direction

              villager_image = pygame.image.load("büyücü.png")
              villager_image = pygame.transform.scale(villager_image, (villager_size, villager_size))
              screen.blit(villager_image, (villager_x, villager_y))

              door_image = pygame.image.load("kapı.jpg")
              door_image = pygame.transform.scale(door_image, (door_width, door_height))
              screen.blit(door_image, (door_x, door_y))

              # Envanter ikonunu çiz (Her zaman en üstte olması için en son çiziyoruz - diğer objelerin ve background'ın üstüne gelecek)
              draw_inventory_icon()

              if (player_x < door_x + door_width and
                  player_x + player_size > door_x and
                  player_y < door_y + door_height and
                  player_y + player_size > door_y):
                in_house = False
                return player_x, player_y  # Return to the main game loop

              pygame.display.flip()
              clock.tick(60)
          else:
              # Envanter açıksa sadece envanter ekranını çiz
              display_inventory()

        return player_x, player_y #return new coordinates

    except pygame.error as e:
        print(f"Error loading image: {e}")
        # Handle the error gracefully
        screen.fill(green)
        pygame.display.flip()
        pygame.time.delay(2000)
def new_screen_3(background_image_path, player_x_new, player_y_new):
    try:
        new_background = pygame.image.load(background_image_path)
        new_background = pygame.transform.scale(new_background, (screen_width, screen_height))
        screen.blit(new_background, (0, 0))

        font = pygame.font.Font(None, 36)
        text = font.render("You are in the Forest!", True, black)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

        # Player position in the new screen
        player_x = player_x_new
        player_y = player_y_new
        player_image = pygame.image.load("prenses.gif")
        player_image = pygame.transform.scale(player_image, (player_size, player_size))
        screen.blit(player_image, (player_x, player_y))  # Scale to player size

        pygame.display.flip()

        # Event handling for the new screen
        in_new_screen = True
        while in_new_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_ESCAPE:  # Press Escape to go back
                    in_new_screen = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
                player_y += player_speed

            screen.blit(new_background, (0, 0))
            player_image = pygame.image.load("prenses.gif")
            player_image = pygame.transform.scale(player_image, (player_size, player_size))
            screen.blit(player_image, (player_x, player_y))  # Scale to player size,

            fors_image = pygame.image.load("kapı.png")
            fors_image = pygame.transform.scale(fors_image, (fors_width, fors_height))
            screen.blit(fors_image, (fors_x, fors_y))

            if (player_x < fors_x + fors_width and
                    player_x + player_size > fors_x and
                    player_y < fors_y + fors_height and
                    player_y + player_size > fors_y):
                in_Forest = False
                return player_x, player_y  # Return to the main game loop

            pygame.display.flip()
            clock.tick(60)

        return player_x, player_y #return new coordinates
    except pygame.error as e:
        print(f"Error loading image: {e}")
        # Handle the error gracefully
        screen.fill(green)
        pygame.display.flip()
        pygame.time.delay(2000)

running = True
while running:
    inventory_icon_rect = draw_inventory_icon()
    current_time_ms = pygame.time.get_ticks() # Time in millisecond
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Sol tıklama
                if inventory_icon_rect.collidepoint(event.pos):
                    inventory_display = True
                    display_inventory()  # Envanter ekranını göster
        if event.type == pygame.KEYDOWN:

          if event.key == pygame.K_i and not in_cave and not at_processing_station: # Envanteri dışarıda ve istasyonda değilken aç/kapat
              inventory_display = not inventory_display
              if inventory_display:
                  display_inventory()
          if event.key == pygame.K_ESCAPE and inventory_display:
              inventory_display = False

          if event.key == pygame.K_SPACE and has_sword and werewolf_visible:  # Boşluk tuşu ve kılıç varsa ve kurtadam görünürse saldır
              # Saldırı bekleme süresi kontrolü
              if current_time_ms - last_attack_time > attack_cooldown:
                  # Oyuncu ve kurtadam yeterince yakın mı kontrol et (basit bir yakınlık kontrolü)
                  distance = ((player_x - werewolf_x) ** 2 + (player_y - werewolf_y) ** 2) ** 0.5
                  if distance < player_size + werewolf_size / 2:  # Yaklaşık olarak birbirlerine yakınlar
                      werewolf_health -= 20  # Kurtadamın canını azalt
                      last_attack_time = current_time_ms  # Son saldırı zamanını güncelle
                      print(f"Werewolf Health: {werewolf_health}")
                      if werewolf_health <= 0:
                          print("Werewolf defeated!")
                          werewolf_visible = False  # Kurtadamı görünmez yap

          # Envanter ikonuna tıklama algılamasını ana döngüye ekle
          if event.type == pygame.MOUSEBUTTONDOWN:
              if event.button == 1:  # Sol tıklama
                  # Envanter ikonunu çiz ve Rect objesini al
                  inventory_icon_rect = draw_inventory_icon()  # Burada tekrar çağırıyoruz ki tıklama algılaması güncel Rect'i kullansın
                  if inventory_icon_rect.collidepoint(event.pos):
                      inventory_display = True
                      display_inventory()



    if not inventory_display and not in_cave and not at_processing_station: # Envanter, mağara ve istasyon açık değilse ana oyun döngüsü çalışsın
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
            player_y += player_speed

    # Check if it's between 20:00 and 23:00
    werewolf_visible = (hours == 17 and minutes >= 0) or \
                       (hours == 18) or \
                       (hours == 19) or \
                       (hours == 20 and minutes < 60)


    # Werewolf movement (only if visible)
    if werewolf_visible:
        #  Werewolf will not chase the player
        # Instead, move randomly
        werewolf_x += random.randint(-werewolf_speed, werewolf_speed)
        werewolf_y += random.randint(-werewolf_speed, werewolf_speed)


        # Keep werewolf within screen bounds
        werewolf_x = max(0, min(werewolf_x, screen_width - werewolf_size))
        werewolf_y = max(0, min(werewolf_y, screen_height - werewolf_size))

    # Collision detection (only if werewolf is visible)
    if werewolf_visible:
        if werewolf_x < player_x:
            werewolf_x += werewolf_speed
        if werewolf_x > player_x:
            werewolf_x -= werewolf_speed
        if werewolf_y < player_y:
            werewolf_y += werewolf_speed
        if werewolf_y > player_y:
            werewolf_y -= werewolf_speed
    # Collision detection with werewolf
    if werewolf_visible and (player_x < werewolf_x + werewolf_size and
            player_x + player_size > werewolf_x and
            player_y < werewolf_y + werewolf_size and
            player_y + player_size > werewolf_y):
        player_health -= 1  # Decrease health by 1
        if player_health <= 0:
            print("Game Over!")
            running = False
        else:
            # Briefly make werewolf invisible or move it away
            # to prevent instant repeated collisions
            werewolf_visible = False
            werewolf_x = random.randint(100, screen_width - werewolf_size)
            werewolf_y = random.randint(100, screen_height - werewolf_size)
            pygame.time.delay(500)  # Short delay before werewolf reappears
            werewolf_visible = True

    # Collision detection with house
    if (player_x < house_x + house_width and
            player_x + player_size > house_x and
            player_y < house_y + house_height and
            player_y + player_size > house_y):
        print("You are in the house!")
        player_x, player_y = new_screen("img_1.png", player_x, player_y)
    # Collision detection with cave (enter cave)
    if (player_x < cave_x + cave_width and
            player_x + player_size > cave_x and
            player_y < cave_y + cave_height and
            player_y + player_size > cave_y and not in_cave and not inventory_display):
        cave_screen() # Switch to cave screen
    if (player_x < gamze_x + gamze_width and
            player_x + player_size > gamze_x and
            player_y < gamze_y + gamze_height and
            player_y + player_size > gamze_y):
        print("You are in the Forest!")
        player_x, player_y = new_screen_3("hhhh.png", player_x, player_y)

    # Collision detection with sword object on the ground (with material check)
    if not has_sword and pygame.Rect(player_x, player_y, player_size, player_size).colliderect(sword_object_rect):
        if check_inventory_for_recipe(sword_recipe):
            remove_items_from_inventory(sword_recipe)
            inventory.append(sword_item)
            has_sword = True
            sword_object_rect = pygame.Rect(0, 0, 0, 0)  # Kılıcı görünmez yap
            print("Kılıç alındı!")
        else:
            print("Kılıcı almak için yeterli madenin yok.")

    # Collision detection with processing station (enter processing screen)
    if (player_x < processing_station_x + processing_station_width and
            player_x + player_size > processing_station_x and
            player_y < processing_station_y + processing_station_height and
            player_y + player_size > processing_station_y and not in_cave and not inventory_display): # Check if not in cave or inventory
        at_processing_station = True
        processing_screen() # Switch to processing screen
        at_processing_station = False # Set flag back to False when exiting screen

    # Clear the screen
    screen.blit(background_image, (0, 0)) # Draw background

    gamze_image = pygame.image.load("kapı.png")
    gamze_image = pygame.transform.scale(gamze_image, (gamze_width, gamze_height))
    screen.blit(gamze_image, (gamze_x, gamze_y))

    health_bar_image = pygame.image.load("kalp.png")
    health_bar_image = pygame.transform.scale(health_bar_image, (health_bar_width, health_bar_height))
    screen.blit(health_bar_image, (health_bar_x, health_bar_y))

    if not in_cave and not inventory_display and not at_processing_station:
        # Draw player, werewolf, and house
        player_image = pygame.image.load("prenses.gif")
        player_image = pygame.transform.scale(player_image, (player_size, player_size))
        screen.blit(player_image, (player_x, player_y))  # Scale to player size
        if werewolf_visible:
            werewolf_image = pygame.image.load("kurt.png")
            werewolf_image = pygame.transform.scale(werewolf_image, (werewolf_size, werewolf_size))
            screen.blit(werewolf_image, (werewolf_x, werewolf_y))
        house_image = pygame.image.load("ev.png")
        house_image = pygame.transform.scale(house_image, (house_width, house_height))
        screen.blit(house_image, (house_x, house_y))
        # İşlem istasyonu görselini çiz
        if processing_station_image:
             screen.blit(processing_station_image, (processing_station_x, processing_station_y))
        else:
             # Görsel yüklenemediyse dikdörtgen çizmeye devam et
             pygame.draw.rect(screen, (100, 149, 237), (processing_station_x, processing_station_y, processing_station_width, processing_station_height))
    # Kılıç objesini çiz (Sadece henüz toplanmadıysa ve görsel yüklendiyse)
    if not has_sword and sword_object_rect.width > 0 and sword_image:  # Kılıç hala haritadaysa ve görseli varsa
        screen.blit(sword_image, sword_object_rect)
    elif not has_sword and sword_object_rect.width > 0:  # Görsel yoksa sarı bir kare çiz (örneğin)
        pygame.draw.rect(screen, yellow, sword_object_rect)
    # Oyuncunun üstünde kılıcı çiz (varsa)
    if has_sword and sword_image:
        # Oyuncunun pozisyonuna göre kılıcın pozisyonunu ayarla
        screen.blit(sword_image, (player_x + player_size / 2, player_y + player_size / 2))

    for i in range(player_health):
        screen.blit(health_bar_image, (health_bar_x + i * heart_spacing, health_bar_y))

    # Display the time (fast forward)
    elapsed_time = (time.time() - game_start_time) * fast_time_multiplier
    hours = int(elapsed_time // 3600) % 24  # Get hours (0-23)
    minutes = int((elapsed_time % 3600) // 60) # Get minutes (0-59)
    time_text = f"{hours:02d}:{minutes:02d}"
    font = pygame.font.Font(None, 36)
    time_surface = font.render(time_text, True, black)
    screen.blit(time_surface, (10, 10))


    # Display werewolf health (optional)
    if werewolf_visible:
        health_font = pygame.font.Font(None, 24)
        health_text = health_font.render(f"Health: {werewolf_health}", True, black)
        screen.blit(health_text, (werewolf_x, werewolf_y - 20))  # Display above werewolf

    # If inventory is open, display it
    if inventory_display:
        display_inventory()
    # Envanter ikonunu çiz (Her zaman en üstte olması için en son çiziyoruz - diğer objelerin ve background'ın üstüne gelecek)
    draw_inventory_icon()
    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()