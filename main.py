import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class Player:
    def __init__(self, player_class):
        self.player_class = player_class
        self.health = 100
        self.inventory = {"Health Potion": 2, "Damage Boost": 0}
        self.points = 0
        self.damage_boost_active = False
        self.damage_boost_moves_left = 0

    def reset_player(self):
        self.health = 100
        self.inventory = {"Health Potion": 2, "Damage Boost": 0}
        self.points = 0
        self.damage_boost_active = False
        self.damage_boost_moves_left = 0

    def display_stats(self, parent):
        stats = f"Class: {self.player_class}\nHealth: {max(0, self.health)}\nPoints: {self.points}\nInventory: {', '.join([f'{item}: {count}' for item, count in self.inventory.items()])}"
        messagebox.showinfo("Player Stats", stats, parent=parent)

class AdventureGameGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Quest for Aetheria")
        self.geometry("600x400")
        self.configure(bg="#2596be")
        self.player = Player("Adventurer")
        
        
        self.background_image = self.resize_image(Image.open("background_image.jpg"), (600, 400))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        #self.dragonlord_image = self.resize_image(Image.open("dragonlord.png"), (600, 400))
        self.dragonlord_photo = ImageTk.PhotoImage(file = "dragonlord.png")

        self.main_menu_frame = tk.Frame(self)
        self.adventure_frame = tk.Frame(self)
        self.shop_frame = tk.Frame(self)
        self.current_frame = None

        self.main_menu_frame = tk.Frame(self, bg="#2596be") 
        self.adventure_frame = tk.Frame(self, bg="#2596be") 
        self.shop_frame = tk.Frame(self, bg="#2596be") 
        self.current_frame = None

        self.create_main_menu()
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)

    def resize_image(self, image, new_size):
        return image.resize(new_size, Image.ANTIALIAS) if hasattr(Image, "ANTIALIAS") else image.resize(new_size)


    def create_main_menu(self):
        self.switch_frame(self.main_menu_frame)

        label = tk.Label(self.main_menu_frame, text="Welcome to the Quest for Aetheria!")
        label.pack(pady=10)

        button_start = tk.Button(self.main_menu_frame, text="Start Adventure", command=self.start_adventure)
        button_start.pack(pady=10)

        button_stats = tk.Button(self.main_menu_frame, text="View Stats⬆️", command=lambda: self.player.display_stats(self))
        button_stats.pack(pady=10)

        if self.player.points >= 150: #FIX FIX FIX fixed :)
            button_encounter_dragonlord = tk.Button(self.main_menu_frame, text="Encounter Dragonlord🐉", command=self.encounter_dragonlord)
            button_encounter_dragonlord.pack(pady=10)

    def start_adventure(self):
        self.canvas.destroy()
        self.switch_frame(self.adventure_frame)
        label = tk.Label(self.adventure_frame, text="You find yourself on a dirt road. Ahead, the path splits into two. Choose your path:")
        label.pack(pady=10)

        choices = [
            ("Encounter Goblins ( •̀ᴗ•́ )و ̑̑", self.encounter_goblins),
            ("Explore Cave", self.explore_cave),
            ("Visit Shop", self.visit_shop),
            ("View Stats⬆️", lambda: self.player.display_stats(self)),
            ("Use Health Potion❤️", self.use_health_potion),
            ("Use Damage Boost", self.use_damage_boost)
        ]

        for text, command in choices:
            button = tk.Button(self.adventure_frame, text=text, command=command)
            button.pack(pady=5)

    def switch_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack()

    def encounter_goblins(self):
        self.generic_encounter("goblins", 30, 40, 5, 10, 4, 8)

    def encounter_dragonlord(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.dragonlord_label = tk.Label(self, image=self.dragonlord_photo, bg="#2596be")
        self.dragonlord_label.pack()
        self.generic_encounter("Dragonlord", 200, 200, 5, 10, 10, 15)
        self.remove_dragonlord_image()

    def remove_dragonlord_image(self):
        if hasattr(self, 'dragonlord_label') and self.dragonlord_label is not None:
            self.dragonlord_label.destroy()

    def create_victory_screen(self):
        self.victory_frame = tk.Frame(self)
        self.switch_frame(self.victory_frame)

        label = tk.Label(self.victory_frame, text="Congratulations! You defeated the Dragonlord and saved the realm!♕")
        label.pack(pady=10)

        button_restart = tk.Button(self.victory_frame, text="Restart Adventure", command=self.create_option_select_menu)
        button_restart.pack(pady=5)

    def create_game_over_screen(self):
        
        self.game_over_frame = tk.Frame(self)
        self.switch_frame(self.game_over_frame)

        label = tk.Label(self.game_over_frame, text="Game Over! You were defeated. Better luck next time!☹")
        label.pack(pady=10)

        button_restart = tk.Button(self.game_over_frame, text="Restart Adventure", command=self.restart_adventure)
        button_restart.pack(pady=5)

    def restart_adventure(self):
        self.player.reset_player()
        self.create_option_select_menu()



    def generic_encounter(self, enemy, min_hp, max_hp, min_dmg, max_dmg, enemy_min_dmg, enemy_max_dmg):
        used_health_potion = False
        enemy_health = random.randint(min_hp, max_hp)
        result = messagebox.askyesno(
            "Encounter", f"You encounter {enemy} with {enemy_health} health. Do you wish to fight?", parent=self
        )
        if not result:
            messagebox.showinfo("Retreat", "You chose to avoid the encounter. (╯°□°)╯", parent=self)
            return

        while enemy_health > 0 and self.player.health > 0:
            if used_health_potion == False:
              attack_damage = random.randint(min_dmg, max_dmg)
              if self.player.damage_boost_active:
                attack_damage += 5
                self.apply_damage_boost_if_active()
              enemy_attack = random.randint(enemy_min_dmg, enemy_max_dmg)
              enemy_health -= attack_damage
              self.player.health -= enemy_attack
              if self.player.health <= 0 or enemy_health <= 0:
                  break

              continue_fight = messagebox.askyesno(
                  "Battle", f"You deal {attack_damage} damage⚔️.\nEnemy health❤️: {enemy_health} Your health❤️: {self.player.health}\nEnemy attacks! You receive {enemy_attack} damage. Continue fighting?\nYes: continue, No: use Health Potion",
                  parent=self
              )
              if not continue_fight:
                  self.use_health_potion()
                  used_health_potion = True
            else:
              continue_fight = messagebox.askyesno(
                "Battle", f"Enemy health❤️: {enemy_health} Your health❤️: {self.player.health}\nContinue fighting?\nYes: continue, No: use Health Potion",
                parent=self
              )
              if continue_fight:
                  used_health_potion = False
              if not continue_fight:
                  self.use_health_potion()

        if self.player.health <= 0:
            self.create_game_over_screen()
        elif enemy_health <= 0:
            if enemy == "Dragonlord":
                #self.dragonlord_label.destroy()
                self.create_victory_screen()
            else:
                messagebox.showinfo("Victory", f"You defeated the {enemy}. You gain 40 points.♕", parent=self)
                self.player.points += 40



    def explore_cave(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.explore_cave_frame = tk.Frame(self)
        self.switch_frame(self.explore_cave_frame)

        label = tk.Label(self.explore_cave_frame, text="You enter the dark cave and find a treasure chest. Do you want to open it?")
        label.pack(pady=10)

        button_open_chest = tk.Button(self.explore_cave_frame, text="Yes √", command=self.open_treasure_chest)
        button_open_chest.pack(pady=5)

        button_leave_cave = tk.Button(self.explore_cave_frame, text="No X", command=self.create_option_select_menu)
        button_leave_cave.pack(pady=5)

    def handle_chest_result(self, treasure):
        if treasure == "Gold Coins":
            messagebox.showinfo("Treasure", "You gain 10 points", parent=self)
        elif treasure == "Magic Scroll":
            messagebox.showinfo("Treasure", "You gain 20 points", parent=self)
        elif treasure == "Monster Trap":
            messagebox.showinfo("Trap", f"Oops! You lose 15 health. {self.player.health} health remaining", parent=self)
        elif treasure == "Friendly NPC":
            messagebox.showinfo("Treasure", "The friendly NPC gives you a Health Potion and some coins.\nYou gain 5 points", parent=self)
        elif treasure == "Assorted Gems":
            messagebox.showinfo("Treasure", "You gain 100 points", parent=self)

        #self.create_option_select_menu()


    def open_treasure_chest(self):
        treasure_options = ["Assorted Gems"] * 10
        treasure_options += ["Gold Coins"] * 20
        treasure_options += ["Magic Scroll"] * 10
        treasure_options += ["Friendly NPC"] * 15
        treasure_options += ["Monster Trap"] * 45
        treasure = random.choice(treasure_options)
        messagebox.showinfo("Treasure Chest", f"You found something in the chest!\n{treasure}", parent=self)
        if treasure == "Gold Coins":
            self.player.points += 10
        elif treasure == "Magic Scroll":
            self.player.points += 20
        elif treasure == "Monster Trap":
            self.player.health -= 15
            if self.player.health <= 0:
              self.create_game_over_screen()
              return
        elif treasure == "Friendly NPC":
            self.player.inventory["Health Potion"] += 1
            self.player.points += 5
        elif treasure == "Assorted Gems":
            self.player.points += 100

        self.handle_chest_result(treasure)
        self.create_option_select_menu()

    def visit_shop(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.shop_frame = tk.Frame(self)
        self.switch_frame(self.shop_frame)

        label = tk.Label(self.shop_frame, text="Welcome to the Shop!")
        label.pack(pady=10)

        button_buy_health_potion = tk.Button(self.shop_frame, text="Buy Health Potion (20 points)", command=self.buy_health_potion)
        button_buy_health_potion.pack(pady=5)

        button_buy_damage_boost = tk.Button(self.shop_frame, text="Buy Damage Boost (50 points)", command=self.buy_damage_boost)
        button_buy_damage_boost.pack(pady=5)

        button_return = tk.Button(self.shop_frame, text="Return to Main Menu", command=self.return_to_main_menu_from_shop)
        button_return.pack(pady=10)

    def return_to_main_menu_from_shop(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.create_option_select_menu()


    def create_option_select_menu(self):
        if self.current_frame:
            self.current_frame.destroy()
        #self.option_select_frame = tk.Frame(self, bg="#FFFFFF")
        self.option_select_frame = tk.Frame(self)
        #self.configure(bg="#be2596")
        # self.switch_frame(self.option_select_frame)

        #self.option_select_frame = tk.Frame(self, bg="#be2596")  # Replace with your desired hex color code
        self.switch_frame(self.option_select_frame)


        label = tk.Label(self.option_select_frame, text="Choose your path:")
        label.pack(pady=10)

        choices = [
            ("Encounter Goblins ( •̀ᴗ•́ )و ̑̑", self.encounter_goblins),
            ("Explore Cave", self.explore_cave),
            ("Visit Shop", self.visit_shop),
            ("View Stats⬆️", lambda: self.player.display_stats(self)),
            ("Use Health Potion❤️", self.use_health_potion),
            ("Use Damage Boost", self.use_damage_boost)
        ]

        for text, command in choices:
            button = tk.Button(self.option_select_frame, text=text, command=command)
            button.pack(pady=5)

        if self.player.points >= 150: 
            button_encounter_dragonlord = tk.Button(
                self.option_select_frame, text="Encounter Dragonlord", command=self.encounter_dragonlord
            )
            button_encounter_dragonlord.pack(pady=10)


    def buy_health_potion(self):
        if self.player.points >= 20:
            self.player.inventory["Health Potion"] += 1
            self.player.points -= 20
            messagebox.showinfo("Purchase", f"You bought a Health Potion.\nYou have {self.player.points} remaining points.", parent=self)
        else:
            messagebox.showinfo("Purchase", "Not enough points to buy a Health Potion.", parent=self)

    def buy_damage_boost(self):
        if self.player.points >= 50:
            self.player.inventory["Damage Boost"] += 1
            self.player.points -= 50
            messagebox.showinfo("Purchase", f"You bought a Damage Boost.\nYou have {self.player.points} remaining points.", parent=self)
        else:
            messagebox.showinfo("Purchase", "Not enough points to buy a Damage Boost.", parent=self)

    def use_health_potion(self):
        if self.player.health == 100:
          messagebox.showinfo("Heal", "You are already at full health.", parent=self)
        if self.player.inventory["Health Potion"] > 0:
            heal_amount = 25
            self.player.health = min(100, self.player.health + heal_amount)
            self.player.inventory["Health Potion"] -= 1
            messagebox.showinfo("Heal", f"You use a Health Potion and heal for {heal_amount} HP.\nYour health: {self.player.health}", parent=self)
        else:
            messagebox.showinfo("Heal", "You don't have any Health Potions left!", parent=self)

    def use_damage_boost(self):
      if self.player.damage_boost_active:
          refresh = messagebox.askyesno("Damage Boost", f"Currently active with {self.player.damage_boost_moves_left} moves left. Do you want to use another Damage Boost to refresh the effect?")
          if not refresh:
            return
      if self.player.inventory["Damage Boost"] > 0:
          self.player.damage_boost_active = True
          self.player.damage_boost_moves_left = 15
          self.player.inventory["Damage Boost"] -= 1
          messagebox.showinfo("Damage Boost", "Damage Boost activated! It will last for 15 moves.")
      else:
          messagebox.showinfo("Damage Boost", "You do not have any Damage Boosts available.")

    def apply_damage_boost_if_active(self):
      if self.player.damage_boost_active:
        self.player.damage_boost_moves_left -= 1
        if self.player.damage_boost_moves_left <= 0:
            self.player.damage_boost_active = False
            messagebox.showinfo("Damage Boost", "Your Damage Boost has run out.")

if __name__ == "__main__":
    app = AdventureGameGUI()
    app.mainloop()
