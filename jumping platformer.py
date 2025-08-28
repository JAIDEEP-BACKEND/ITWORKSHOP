import tkinter as tk
import time

class PlatformerGame:
    """
    A simple jumping platformer game that simulates gravity and collisions.
    The game features player movement, platforms, enemies, and a goal.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Jumping Platformer")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        self.master.configure(bg='#1A2D3E')

        # --- Game Constants ---
        self.PLAYER_SIZE = 20
        self.GRAVITY = 1
        self.JUMP_STRENGTH = -20
        self.PLAYER_SPEED = 8
        self.PLATFORM_COLOR = '#00FF00'
        self.PLAYER_COLOR = '#FFD700'
        self.GOAL_COLOR = '#FF0000'
        self.ENEMY_COLOR = '#FF5733'
        self.ENEMY_SIZE = 20

        # --- Game Variables ---
        self.player_vel_y = 0
        self.on_ground = False
        self.is_running = False
        self.start_time = 0
        self.keys_pressed = {}

        # --- UI Components ---
        self.control_frame = tk.Frame(master, bg='#1A2D3E')
        self.control_frame.pack(pady=10)

        self.timer_label = tk.Label(self.control_frame, text="Time: 0.00s",
                                   font=("Arial", 20, "bold"), bg='#1A2D3E', fg='#FFFFFF')
        self.timer_label.pack()

        self.canvas = tk.Canvas(master, width=700, height=500, bg='#4B3F72',
                                highlightthickness=0, bd=0)
        self.canvas.pack(pady=10)

        # Create game elements
        self.player = self.canvas.create_oval(
            50, 450, 50 + self.PLAYER_SIZE, 450 + self.PLAYER_SIZE,
            fill=self.PLAYER_COLOR, tags="player"
        )
        self.platforms = self.create_platforms()
        self.enemies = self.create_enemies()
        self.goal = self.create_goal()

        # Start message
        self.message = self.canvas.create_text(
            350, 250, text="Press ENTER to Start", font=("Arial", 24, "bold"), fill="#FFFFFF"
        )
        self.master.bind('<Return>', self.start_game)
        self.master.bind('<KeyPress>', self.on_key_press)
        self.master.bind('<KeyRelease>', self.on_key_release)

    def on_key_press(self, event):
        """Records which keys are currently being pressed."""
        self.keys_pressed[event.keysym] = True

    def on_key_release(self, event):
        """Removes keys from the pressed list when released."""
        self.keys_pressed[event.keysym] = False

    def create_platforms(self):
        """Creates the platforms for the level."""
        platforms = []
        platforms.append(self.canvas.create_rectangle(0, 480, 700, 500, fill=self.PLATFORM_COLOR)) # ground
        platforms.append(self.canvas.create_rectangle(150, 400, 250, 420, fill=self.PLATFORM_COLOR))
        platforms.append(self.canvas.create_rectangle(200, 300, 300, 320, fill=self.PLATFORM_COLOR))
        platforms.append(self.canvas.create_rectangle(350, 250, 450, 270, fill=self.PLATFORM_COLOR))
        platforms.append(self.canvas.create_rectangle(500, 200, 600, 220, fill=self.PLATFORM_COLOR))
        platforms.append(self.canvas.create_rectangle(650, 100, 700, 120, fill=self.PLATFORM_COLOR))
        return platforms

    def create_enemies(self):
        """Creates enemies at specific locations."""
        enemies = []
        enemies.append(self.canvas.create_rectangle(
            220, 280, 220 + self.ENEMY_SIZE, 280 + self.ENEMY_SIZE,
            fill=self.ENEMY_COLOR, tags="enemy"
        ))
        enemies.append(self.canvas.create_rectangle(
            550, 180, 550 + self.ENEMY_SIZE, 180 + self.ENEMY_SIZE,
            fill=self.ENEMY_COLOR, tags="enemy"
        ))
        return enemies

    def create_goal(self):
        """Creates the finish line for the level."""
        return self.canvas.create_rectangle(660, 50, 690, 100, fill=self.GOAL_COLOR)

    def start_game(self, event=None):
        """Starts the game loop and resets state."""
        if self.is_running:
            return
        self.is_running = True
        self.start_time = time.time()
        self.canvas.delete(self.message)
        self.game_loop()

    def game_loop(self):
        """The main game loop that updates player position and checks collisions."""
        if not self.is_running:
            return

        self.handle_input()
        self.apply_gravity()
        self.check_collisions()
        self.update_timer()

        if self.check_win():
            self.end_game("You Win!")
        elif self.check_death():
            self.end_game("Game Over!")

        self.master.after(20, self.game_loop)

    def handle_input(self):
        """Handles player movement based on pressed keys."""
        dx = 0
        if self.keys_pressed.get('Left'):
            dx -= self.PLAYER_SPEED
        if self.keys_pressed.get('Right'):
            dx += self.PLAYER_SPEED
        
        self.canvas.move(self.player, dx, 0)
        self.check_bounds()
        
        if self.keys_pressed.get('Up') and self.on_ground:
            self.jump()

    def apply_gravity(self):
        """Applies gravity to the player if they are not on the ground."""
        if not self.on_ground:
            self.player_vel_y += self.GRAVITY
            self.canvas.move(self.player, 0, self.player_vel_y)

    def jump(self):
        """Makes the player jump if they are on the ground."""
        self.player_vel_y = self.JUMP_STRENGTH
        self.on_ground = False
            
    def check_bounds(self):
        """Ensures the player stays within the canvas boundaries."""
        coords = self.canvas.coords(self.player)
        if coords[0] < 0:
            self.canvas.coords(self.player, 0, coords[1], self.PLAYER_SIZE, coords[3])
        elif coords[2] > 700:
            self.canvas.coords(self.player, 700 - self.PLAYER_SIZE, coords[1], 700, coords[3])

    def check_collisions(self):
        """Checks for collisions with platforms and updates the player's vertical velocity."""
        player_coords = self.canvas.coords(self.player)
        
        # Reset on_ground status
        self.on_ground = False
        
        # Check for collisions with each platform
        for platform in self.platforms:
            platform_coords = self.canvas.coords(platform)
            if self.is_colliding(player_coords, platform_coords) and self.player_vel_y >= 0:
                self.canvas.coords(self.player, player_coords[0], platform_coords[1] - self.PLAYER_SIZE,
                                   player_coords[2], platform_coords[1])
                self.player_vel_y = 0
                self.on_ground = True

    def is_colliding(self, coords1, coords2):
        """Helper function to check for intersection of two rectangles."""
        x1, y1, x2, y2 = coords1
        x3, y3, x4, y4 = coords2
        return x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3

    def check_win(self):
        """Checks if the player has reached the goal."""
        player_coords = self.canvas.coords(self.player)
        goal_coords = self.canvas.coords(self.goal)
        return self.is_colliding(player_coords, goal_coords)

    def check_death(self):
        """Checks if the player has collided with an enemy."""
        player_coords = self.canvas.coords(self.player)
        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy)
            if self.is_colliding(player_coords, enemy_coords):
                return True
        return False

    def update_timer(self):
        """Updates the timer display."""
        elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=f"Time: {elapsed_time:.2f}s")
        
    def end_game(self, message):
        """Stops the game and displays the final message."""
        self.is_running = False
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_reqwidth() // 2, self.canvas.winfo_reqheight() // 2,
            text=message, font=("Arial", 28, "bold"), fill='#FFD700', justify='center'
        )
        self.master.unbind('<Return>')
        self.master.unbind('<Left>')
        self.master.unbind('<Right>')
        self.master.unbind('<Up>')
        self.master.unbind('<KeyPress>')
        self.master.unbind('<KeyRelease>')

def main():
    root = tk.Tk()
    game = PlatformerGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
