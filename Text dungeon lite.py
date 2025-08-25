# Text Dungeon Lite — Python 3.11+
# Free version of Text Dungeon for demo/testing

import random
import os
import sys

# ---------- Player ----------
class Player:
    def __init__(self):
        self.hp = 20
        self.max_hp = 20
        self.gold = 10
        self.atk = (3, 7)
        self.inv = ["Healing Potion"]
        self.x = 0
        self.y = 0
    def is_alive(self):
        return self.hp > 0

player = Player()

# ---------- Board ----------
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

EMPTY = '.'
PLAYER_CHAR = 'P'
MONSTER = 'M'
CHEST = 'C'

board = []

# ---------- Events ----------
events = [
    "You found some gold.",
    "A goblin drops 2 gold.",
    "You opened a chest and found something.",
    "A rat squeaks at you.",
    "You feel like someone is watching...",
    "You tripped. -1 HP",
    "You found a potion. +2 HP"
]

# ---------- Utilities ----------
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def print_centered(text, width=50):
    lines = text.split('\n')
    for line in lines:
        print(line.center(width))

# ---------- Board Generation ----------
def generate_board():
    global player
    b = [[EMPTY for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    player.x, player.y = BOARD_WIDTH//2, BOARD_HEIGHT//2
    b[player.y][player.x] = PLAYER_CHAR
    for _ in range(10):
        x,y=random.randint(0,BOARD_WIDTH-1),random.randint(0,BOARD_HEIGHT-1)
        if b[y][x]==EMPTY: b[y][x]=MONSTER
    for _ in range(5):
        x,y=random.randint(0,BOARD_WIDTH-1),random.randint(0,BOARD_HEIGHT-1)
        if b[y][x]==EMPTY: b[y][x]=CHEST
    return b

def print_board():
    clear_screen()
    header = "=== TEXT DUNGEON LITE ==="
    print_centered(header)
    print()
    for row in board:
        print_centered(' '.join(row))
    print_centered(f"HP: {player.hp}/{player.max_hp}   Gold: {player.gold}")
    print_centered(f"Inventory: {player.inv}")

# ---------- Combat ----------
def combat():
    dmg = random.randint(*player.atk)
    player.hp -= random.randint(0,3)
    reward = random.randint(1,5)
    player.gold += reward
    print_centered(f"You fight a monster! You deal {dmg} damage and gain {reward} gold.")
    if player.hp <= 0:
        game_over()

# ---------- Chest ----------
def loot_chest():
    item = random.choice(["Gold", "Healing Potion", "Sword"])
    player.inv.append(item)
    gold = random.randint(1,5)
    player.gold += gold
    print_centered(f"Chest found: {item} and {gold} gold!")

# ---------- Game Flow ----------
def game_over():
    clear_screen()
    print_centered("=== YOU HAVE FAINTED ===")
    print_centered("[1] Restart  [2] Quit")
    choice = input("> ")
    if choice=="1":
        main()
    else:
        sys.exit()

def menu():
    clear_screen()
    print_centered("=== TEXT DUNGEON LITE ===")
    print_centered("[1] Start Game")
    print_centered("[2] Quit")
    choice = input("> ")
    if choice=="1":
        main()
    else:
        sys.exit()

def main():
    global board, player
    player.__init__()
    board = generate_board()
    while True:
        print_board()
        move = input("Move (W/A/S/D) or Q to quit > ").lower()
        if move=='q':
            menu()
        dx,dy = 0,0
        if move=='w': dy=-1
        elif move=='s': dy=1
        elif move=='a': dx=-1
        elif move=='d': dx=1
        new_x,new_y = player.x+dx,player.y+dy
        if 0<=new_x<BOARD_WIDTH and 0<=new_y<BOARD_HEIGHT:
            tile = board[new_y][new_x]
            if tile==MONSTER:
                combat()
            elif tile==CHEST:
                loot_chest()
            board[player.y][player.x]=EMPTY
            player.x, player.y = new_x,new_y
            board[player.y][player.x]=PLAYER_CHAR

if __name__=="__main__":
    menu()
