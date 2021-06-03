from random import choice
from pyb import SPI, Pin, UART, delay, Timer
from lis3dsh import LIS3DSH

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 50
SPACESHIP_Y = SCREEN_HEIGHT - 2

uart = UART(2, 115200)
CS = Pin("PE3", Pin.OUT_PP)
SPI_1 = SPI(
    1,  # PA5, PA6, PA7
    SPI.MASTER,
    baudrate=50000,
    polarity=0,
    phase=0,
    firstbit=SPI.MSB,
    crc=None,
)
accel = LIS3DSH(SPI_1, CS)
push_button = Pin("PA0", Pin.IN, Pin.PULL_DOWN)

clock_time = 0  # in tenth of seconds


def clock(timer):
    global clock_time
    clock_time += 1


t = Timer(4, freq=10)
t.callback(clock)


def clear_screen():
    uart.write("\x1b[2J\x1b[?25l")


def move(x, y):
    uart.write("\x1b[{};{}H".format(y, x))


def borders():
    move(1, 1)
    uart.write("█" * SCREEN_WIDTH)
    move(1, SCREEN_HEIGHT)
    uart.write("█" * SCREEN_WIDTH)
    for y in range(1, SCREEN_HEIGHT):
        move(1, y)
        uart.write("█")
        move(SCREEN_WIDTH, y)
        uart.write("█")


def push_button_pressed():
    state = push_button.value()
    active = 0
    while active < 50:
        if push_button.value() == state:
            active += 1
        else:
            return 0  # unstable, consider not pressed
        delay(1)
    return state


logo = r"""  /$$$$$$                                                /$$$$$$                                     /$$                              
 /$$__  $$                                              |_  $$_/                                    | $$                              
| $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$         | $$   /$$$$$$$  /$$    /$$ /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$$
|  $$$$$$  /$$__  $$ |____  $$ /$$_____/ /$$__  $$        | $$  | $$__  $$|  $$  /$$/|____  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$_____/
 \____  $$| $$  \ $$  /$$$$$$$| $$      | $$$$$$$$        | $$  | $$  \ $$ \  $$/$$/  /$$$$$$$| $$  | $$| $$$$$$$$| $$  \__/|  $$$$$$ 
 /$$  \ $$| $$  | $$ /$$__  $$| $$      | $$_____/        | $$  | $$  | $$  \  $$$/  /$$__  $$| $$  | $$| $$_____/| $$       \____  $$
|  $$$$$$/| $$$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$       /$$$$$$| $$  | $$   \  $/  |  $$$$$$$|  $$$$$$$|  $$$$$$$| $$       /$$$$$$$/
 \______/ | $$____/  \_______/ \_______/ \_______/      |______/|__/  |__/    \_/    \_______/ \_______/ \_______/|__/      |_______/ 
          | $$                                                                                                                        
          | $$                                                                                                                        
          |__/                                                                                                                        """

looser = r"""          _____                    _____                    _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\    \                /::\    \                /::\____\        
       /::::\    \              /::::\    \              /::::\    \              /::::\    \              /:::/    /        
      /::::::\    \            /::::::\    \            /::::::\    \            /::::::\    \            /:::/    /         
     /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/    /          
    /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/  \:::\    \        /:::/    /           
   /::::\   \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /:::/    \:::\    \      /:::/    /            
  /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /:::/    / \:::\    \    /:::/    /      _____  
 /:::/\:::\   \:::\____\  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\  /:::/    /   \:::\ ___\  /:::/____/      /\    \ 
/:::/  \:::\   \:::|    |/:::/__\:::\   \:::\____\/:::/  \:::\   \:::|    |/:::/____/     \:::|    ||:::|    /      /::\____\
\::/    \:::\  /:::|____|\:::\   \:::\   \::/    /\::/   |::::\  /:::|____|\:::\    \     /:::|____||:::|____\     /:::/    /
 \/_____/\:::\/:::/    /  \:::\   \:::\   \/____/  \/____|:::::\/:::/    /  \:::\    \   /:::/    /  \:::\    \   /:::/    / 
          \::::::/    /    \:::\   \:::\    \            |:::::::::/    /    \:::\    \ /:::/    /    \:::\    \ /:::/    /  
           \::::/    /      \:::\   \:::\____\           |::|\::::/    /      \:::\    /:::/    /      \:::\    /:::/    /   
            \::/____/        \:::\   \::/    /           |::| \::/____/        \:::\  /:::/    /        \:::\__/:::/    /    
             ~~               \:::\   \/____/            |::|  ~|               \:::\/:::/    /          \::::::::/    /     
                               \:::\    \                |::|   |                \::::::/    /            \::::::/    /      
                                \:::\____\               \::|   |                 \::::/    /              \::::/    /       
                                 \::/    /                \:|   |                  \::/____/                \::/____/        
                                  \/____/                  \|___|                   ~~                       ~~              
                                                                                                                             """

victory = r"""         _________ _______ _________ _______ _________ _______  _______ 
|\     /|\__   __/(  ____ \\__   __/(  ___  )\__   __/(  ____ )(  ____ \
| )   ( |   ) (   | (    \/   ) (   | (   ) |   ) (   | (    )|| (    \/
| |   | |   | |   | |         | |   | |   | |   | |   | (____)|| (__    
( (   ) )   | |   | |         | |   | |   | |   | |   |     __)|  __)   
 \ \_/ /    | |   | |         | |   | |   | |   | |   | (\ (   | (      
  \   /  ___) (___| (____/\   | |   | (___) |___) (___| ) \ \__| (____/\
   \_/   \_______/(_______/   )_(   (_______)\_______/|/   \__/(_______/
                                                                        """


def print_logo(logo_str):
    text = logo_str.splitlines()
    height = len(text)
    width = len(text[0])
    x_offset = (SCREEN_WIDTH - width) // 2
    y_offset = (SCREEN_HEIGHT - height) // 2
    for index, line in enumerate(text):
        move(x_offset, y_offset + index)
        uart.write(line)


class Spaceship:
    def __init__(self, x, y, skin):
        self.skin = skin
        self.x = x
        self.y = y
        self.last_shoot_time = 0
        self.missile_dir = -1 if y == SPACESHIP_Y else 1
        self.missile_skin = "💈" if y == SPACESHIP_Y else "⚡"

    @property
    def skin(self):
        return self._skin

    @skin.setter
    def skin(self, value):
        self._skin = value
        self._skin_length = len(value)

    @property
    def skin_length(self):
        return self._skin_length

    def print(self):
        move(self.x, self.y)
        uart.write(self.skin)

    def erase(self):
        move(self.x, self.y)
        uart.write(self.skin_length * " ")

    def move_left(self, delta):
        if self.x > 1 + delta:
            self.x -= delta
            move(self.x, self.y)
            uart.write(self.skin)
            uart.write(" " * delta)

    def move_right(self, delta):
        if self.x < SCREEN_WIDTH + 1 - self.skin_length - delta:
            move(self.x, self.y)
            uart.write(" " * delta)
            uart.write(self.skin)
            self.x += delta

    def shoot(self):
        if clock_time - self.last_shoot_time > 5:
            missiles.append(
                Missile(
                    self.missile_skin,
                    self.x + self.skin_length // 2,
                    self.y + self.missile_dir,
                    self.missile_dir,
                )
            )
            self.last_shoot_time = clock_time


class Missile:
    def __init__(self, skin, x, y, dir_y):
        self.skin = skin[0]
        self.x = x
        self.y = y
        self.dir_y = dir_y
        self._destroyed = False

    def move(self):
        move(self.x, self.y)
        uart.write(" ")
        self.y += self.dir_y
        self._collide()
        if not self.destroyed:
            move(self.x, self.y)
            uart.write(self.skin)

    def _collide(self):
        if self.dir_y < 0:
            for enemy in enemies[:]:
                if (
                    self.y == enemy.y
                    and enemy.x <= self.x < enemy.x + enemy.skin_length
                ):
                    self._destroyed = True
                    enemy.erase()
                    enemies.remove(enemy)
                    return
        else:
            if (
                self.y == spaceship.y
                and spaceship.x <= self.x < spaceship.x + spaceship.skin_length
            ):
                clear_screen()
                print_logo(looser)
                while True:
                    pass

    @property
    def destroyed(self):
        return not (1 < self.y < SCREEN_HEIGHT - 1) or self._destroyed


# screen setup
clear_screen()
move(SCREEN_WIDTH // 2 - 8, SCREEN_HEIGHT // 2)
print_logo(logo)
borders()

# spaceship creation
spaceship = Spaceship(x=(SCREEN_WIDTH - 5) // 2, y=SPACESHIP_Y, skin="┣━☗━┫")
spaceship.print()

# missiles creation
missiles = []

# enemies creation
enemies = []
for x in range(10):
    for y in range(4):
        enemies.append(Spaceship(x=10 + x * 18, y=3 + 2 * y, skin="╠══V══╣"))
        enemies[-1].print()
enemies_dir = -1
enemies_moves_left = 0

while True:
    # spaceship management
    accel_x = accel.x
    if accel_x > 900:
        spaceship.move_right(3)
    elif accel_x < -900:
        spaceship.move_left(3)
    elif accel_x > 600:
        spaceship.move_right(2)
    elif accel_x < -600:
        spaceship.move_left(2)
    elif accel_x > 300:
        spaceship.move_right(1)
    elif accel_x < -300:
        spaceship.move_left(1)

    if push_button_pressed():
        spaceship.shoot()

    # missiles management
    for missile in missiles[:]:
        missile.move()
        if missile.destroyed:
            missiles.remove(missile)

    # enemies management
    if not clock_time % 10:
        if enemies_moves_left:
            enemies_moves_left -= 1
            for enemy in enemies:
                if enemies_dir > 0:
                    enemy.move_right(1)
                else:
                    enemy.move_left(1)
        else:
            enemies_moves_left = 10
            enemies_dir = -enemies_dir
    if enemies:
        if not clock_time % 5:
            choice(enemies).shoot()
    else:
        clear_screen()
        print_logo(victory)
        while True:
            pass
