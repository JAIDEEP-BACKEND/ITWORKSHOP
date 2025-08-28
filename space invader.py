import tkinter as tk
import random

class SpaceInvaders:
    """
    A class to create a high-end retro Space Invaders game.
    The game features player movement, enemy logic, bullet firing, and collision detection.
    """
    def __init__(self, master):
        """Initializes the game window, canvas, and game objects."""
        self.master = master
        self.master.title("👾 Space Invaders")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        self.master.configure(bg='#0A1828')

        # --- Game Constants ---
        self.PLAYER_SIZE = 40
        self.ENEMY_SIZE = 30
        self.BULLET_SIZE = 10
        self.PLAYER_SPEED = 10
        self.BULLET_SPEED = -10
        self.ENEMY_SPEED = 1
        self.ENEMY_DROP_SPEED = 20
        self.LIVES = 3
        self.MAX_ENEMIES = 30

        # --- Game Variables ---
        self.score = 0
        self.lives = self.LIVES
        self.is_running = False
        self.player = None
        self.enemies = []
        self.bullets = []
        self.enemy_bullet_cooldown = 0
        self.enemy_direction = 1

        # --- UI Components ---
        self.score_label = tk.Label(master, text=f"Score: 0 | Lives: {self.lives}",
                                    font=("Arial", 20, "bold"), bg='#0A1828', fg='#FFFFFF')
        self.score_label.pack(pady=10)

        self.canvas = tk.Canvas(master, width=700, height=500, bg='#1A2D3E',
                                highlightthickness=0, bd=0, relief='flat')
        self.canvas.pack(pady=10)

        # Bind keyboard controls
        self.master.bind('<Left>', self.move_player)
        self.master.bind('<Right>', self.move_player)
        self.master.bind('<space>', self.fire_bullet)
        self.master.bind('<Return>', self.start_game)

        # Start message
        self.message = self.canvas.create_text(
            350, 250, text="Press ENTER to Start", font=("Arial", 24, "bold"), fill="#FFFFFF"
        )

    def start_game(self, event=None):
        """Initializes game state and starts the game loop."""
        if self.is_running:
            return

        self.is_running = True
        self.score = 0
        self.lives = self.LIVES
        self.score_label.config(text=f"Score: {self.score} | Lives: {self.lives}")
        self.canvas.delete(self.message)
        self.reset_game()
        self.game_loop()

    def reset_game(self):
        """Resets all game objects to their initial state."""
        self.canvas.delete("all")
        self.enemies.clear()
        self.bullets.clear()
        self.create_player()
        self.create_enemies()
        self.enemy_direction = 1
        self.master.bind('<Left>', self.move_player)
        self.master.bind('<Right>', self.move_player)
        self.master.bind('<space>', self.fire_bullet)
        self.master.bind('<Return>', self.start_game)


    def create_player(self):
        """Creates the player's ship."""
        x = 350
        y = 450
        self.player = self.canvas.create_rectangle(
            x - self.PLAYER_SIZE // 2, y,
            x + self.PLAYER_SIZE // 2, y + self.PLAYER_SIZE // 2,
            fill='#00FF00', tags="player"
        )

    def create_enemies(self):
        """Creates a grid of enemy invaders."""
        for row in range(5):
            for col in range(6):
                x = 100 + col * 70
                y = 50 + row * 40
                enemy = self.canvas.create_oval(
                    x, y, x + self.ENEMY_SIZE, y + self.ENEMY_SIZE,
                    fill='#FF00FF', tags="enemy"
                )
                self.enemies.append(enemy)

    def move_player(self, event):
        """Moves the player left or right based on key presses."""
        if not self.is_running:
            return

        dx = 0
        if event.keysym == 'Left':
            dx = -self.PLAYER_SPEED
        elif event.keysym == 'Right':
            dx = self.PLAYER_SPEED

        self.canvas.move(self.player, dx, 0)
        
        # Keep player within bounds
        player_coords = self.canvas.coords(self.player)
        if player_coords[0] < 0:
            self.canvas.coords(self.player, 0, player_coords[1], self.PLAYER_SIZE, player_coords[3])
        elif player_coords[2] > 700:
            self.canvas.coords(self.player, 700 - self.PLAYER_SIZE, player_coords[1], 700, player_coords[3])


    def fire_bullet(self, event):
        """Fires a bullet from the player's ship."""
        if not self.is_running:
            return

        player_coords = self.canvas.coords(self.player)
        x = (player_coords[0] + player_coords[2]) / 2
        y = player_coords[1]
        bullet = self.canvas.create_rectangle(
            x - self.BULLET_SIZE // 2, y - self.BULLET_SIZE,
            x + self.BULLET_SIZE // 2, y,
            fill='#00FFFF', tags="bullet"
        )
        self.bullets.append(bullet)

    def move_bullets(self):
        """Moves all player and enemy bullets."""
        # Player bullets
        for bullet in self.bullets:
            self.canvas.move(bullet, 0, self.BULLET_SPEED)

    def move_enemies(self):
        """Moves the enemies and handles side-to-side movement logic."""
        move_sideways = self.ENEMY_SPEED * self.enemy_direction
        move_down = 0
        
        # Check if enemies hit the side walls
        for enemy in self.enemies:
            coords = self.canvas.coords(enemy)
            if coords[0] <= 0 and self.enemy_direction == -1:
                self.enemy_direction = 1
                move_sideways = 0
                move_down = self.ENEMY_DROP_SPEED
                break
            if coords[2] >= 700 and self.enemy_direction == 1:
                self.enemy_direction = -1
                move_sideways = 0
                move_down = self.ENEMY_DROP_SPEED
                break
        
        for enemy in self.enemies:
            self.canvas.move(enemy, move_sideways, move_down)
        
    def check_collisions(self):
        """Checks for all collisions between bullets, enemies, and player."""
        # Player bullet hitting an enemy
        for bullet in self.bullets[:]:
            bullet_coords = self.canvas.coords(bullet)
            if not bullet_coords: # If bullet was already deleted
                self.bullets.remove(bullet)
                continue
                
            for enemy in self.enemies[:]:
                enemy_coords = self.canvas.coords(enemy)
                if not enemy_coords: # If enemy was already deleted
                    self.enemies.remove(enemy)
                    continue

                if self.canvas.coords(bullet) and self.canvas.coords(enemy) and \
                    self.check_collision_coords(bullet_coords, enemy_coords):
                    
                    self.canvas.delete(bullet)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.canvas.delete(enemy)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    
                    self.score += 10
                    self.score_label.config(text=f"Score: {self.score} | Lives: {self.lives}")
                    
        # Check for player-enemy collision
        if self.player:
            player_coords = self.canvas.coords(self.player)
            for enemy in self.enemies:
                if self.check_collision_coords(player_coords, self.canvas.coords(enemy)):
                    self.lives -= 1
                    self.score_label.config(text=f"Score: {self.score} | Lives: {self.lives}")
                    self.end_game()
                    break

    def check_collision_coords(self, coords1, coords2):
        """Helper function to check for intersection of two rectangles."""
        x1, y1, x2, y2 = coords1
        x3, y3, x4, y4 = coords2
        return x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3

    def end_game(self):
        """Stops the game and displays the game over message."""
        self.is_running = False
        self.canvas.delete("all")
        
        if self.lives <= 0:
            final_message = "Game Over!\nFinal Score: "
        elif not self.enemies:
            final_message = "You Win!\nFinal Score: "
            
        self.canvas.create_text(
            350, 250,
            text=f"{final_message}{self.score}",
            font=("Arial", 24, "bold"),
            fill='#FFD700',
            justify='center'
        )
        
        self.master.unbind('<Left>')
        self.master.unbind('<Right>')
        self.master.unbind('<space>')
        
        self.master.after(2000, lambda: self.show_restart_button())
    
    def show_restart_button(self):
        self.canvas.create_text(
            350, 300,
            text="Press ENTER to Play Again",
            font=("Arial", 16),
            fill='#FFFFFF',
            justify='center'
        )
        self.master.bind('<Return>', self.start_game)


    def game_loop(self):
        """The main game loop."""
        if not self.is_running:
            return

        self.move_bullets()
        self.move_enemies()
        self.check_collisions()

        if not self.enemies or self.lives <= 0:
            self.end_game()
            return

        self.master.after(20, self.game_loop)

def main():
    root = tk.Tk()
    game = SpaceInvaders(root)
    root.mainloop()

if __name__ == "__main__":
    main()
