from tkinter import *
import tkinter as tk
from pil import Image, ImageTk
from cells import Cells, EnemyAI

class ColorCombat:
    def __init__(self, rows=5, columns=5):
        # Create the main window
        self.root = Tk()
        self.root.geometry("930x650")
        self.root.title("Color Combat")
        self.root.resizable(False, False)
        self.width = 930
        self.height = 650
        self.initialize_game()

    def initialize_game(self):
        # Set background image
        self.canvas = Canvas(self.root, width = self.width, height = self.height)
        self.canvas.pack(fill="both", expand=True)
        image_path = "Front.png"
        self.bg_image = Image.open(image_path)
        self.bg_image = self.bg_image.resize((self.width, self.height), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Play Button
        play_image_path = 'Play.png'
        self.play_image = self.resize_image(play_image_path, 350)
        self.play_button = tk.Button (
            self.root, 
            image = self.play_image, 
            borderwidth = 0, 
            highlightthickness=0, 
            highlightbackground="black", 
            activebackground="#ffffff",
            command = self.choose_opponent
        )
        self.play_button.place(x = self.width//2, y = 380, anchor = "center")

        # Mechanics Button
        mechanics_image_path = 'Mechanics.png'
        self.mechanics_image = self.resize_image(mechanics_image_path, 350)
        self.mechanics_button = tk.Button (
            self.root, 
            image = self.mechanics_image, 
            borderwidth = 0, 
            highlightthickness=0, 
            highlightbackground="black", 
            activebackground="#ffffff"
        )
        self.mechanics_button.place(x = self.width//2, y = 510, anchor = "center")

    def resize_image(self, image_path, width):
        original_image = Image.open(image_path).convert("RGBA")
        aspect_ratio = original_image.width / original_image.height
        height = int(width / aspect_ratio)
        resized_image = original_image.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)

    def choose_opponent(self):
        # Set background image
        image_path = "Opponent.png"
        self.bg_image = Image.open(image_path)
        self.bg_image = self.bg_image.resize((self.width, self.height), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.play_button.place_forget()
        self.mechanics_button.place_forget()

        # Human Player Button
        human_image_path = 'Human.png'
        self.human_image = self.resize_image(human_image_path, 350)
        self.human_button = tk.Button (
            self.root, 
            image = self.human_image, 
            borderwidth = 0, 
            highlightthickness=0, 
            highlightbackground="black", 
            activebackground="#ffffff",
            command = self.player_vs_player
        )
        self.human_button.place(x = self.width//2, y = 380, anchor = "center")

        # Enemy AI Button
        enemy_image_path = 'Enemy.png'
        self.enemy_image = self.resize_image(enemy_image_path, 350)
        self.enemy_button = tk.Button (
            self.root, 
            image = self.enemy_image, 
            borderwidth = 0, 
            highlightthickness=0, 
            highlightbackground="black", 
            activebackground="#ffffff",
            command = self.player_vs_ai
        )
        self.enemy_button.place(x = self.width//2, y = 510, anchor = "center")
    
    def player_vs_player(self):
        self.game_type = 1
        self.grid_size()
    
    def player_vs_ai(self):
        self.game_type = 2
        self.grid_size()
    
    def show_value(self, val):
        self.grid_size_label.config(text=f"Selected Value: {val}x{val}")
        self.rows = self.columns = int(val)

    def grid_size(self):
        self.rows = self.columns = 3
        # Set background image
        image_path = "Grid.png"
        self.bg_image = Image.open(image_path)
        self.bg_image = self.bg_image.resize((self.width, self.height), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.human_button.place_forget()
        self.enemy_button.place_forget()

        # Create a Scale widget
        self.grid_size_scale = tk.Scale (
            self.canvas, 
            from_ = 3, 
            to = 10, 
            orient = 'horizontal', 
            command = self.show_value, 
            fg = "white", 
            highlightcolor = "white", 
            activebackground = "white", 
            bg = "#0C0C0D",
            length = 500,
            sliderlength = 40,
            width = 30,
            font = ("Arcade Normal", 16),
            highlightthickness = 0
        )
        self.grid_size_scale.place(x = self.width//2, y = 330, anchor = "center")

        # Create a Label to display the selected value
        self.grid_size_label = tk.Label (
            self.canvas, 
            text = "Selected Value: 3x3", 
            fg = "white", 
            bg = "#0C0C0D",
            font = ("Arcade Normal", 16)
        )
        self.grid_size_label.place(x = self.width//2, y = 400, anchor = "center")

        # Start Button
        start_image_path = 'Start.png'
        self.start_image = self.resize_image(start_image_path, 350)
        self.start_button = tk.Button (
            self.root, 
            image = self.start_image, 
            borderwidth = 0, 
            highlightthickness=0, 
            highlightbackground="black", 
            activebackground="#ffffff",
            command = self.game_begin
        )
        self.start_button.place(x = self.width//2, y = 510, anchor = "center")

    def game_begin(self):
        # Set background image
        image_path = "Begin.png"
        self.bg_image = Image.open(image_path)
        self.bg_image = self.bg_image.resize((self.width, self.height), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.grid_size_scale.place_forget()
        self.grid_size_label.place_forget()
        self.start_button.place_forget()
        self.root.after(2000, self.game_board)
    
    def game_board(self):
        image_path = "Game Board.png"
        self.bg_image = Image.open(image_path)
        self.bg_image = self.bg_image.resize((self.width, self.height), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.current_player = 1
        self.cells = []
        self.player2_has_moved = False

        self.winner = Label(
            self.canvas, 
            text="", 
            fg="white", 
            bg="#393E46", 
            font=("Inter", 25, "bold")
        )
        self.winner.place(x=250, y=600)

        # Frame for the grid of buttons
        self.grid_frame = Frame(self.canvas, bg='#0C0C0D')
        self.window_id = self.canvas.create_window(self.width//2, self.height//2, window=self.grid_frame, anchor="center")
        
        for i in range(self.rows):
            row_cells = []
            for j in range(self.columns):
                cell = Cells(self.grid_frame, i, j, self)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        self.enemy_ai = EnemyAI(self)
    
    def enemy_move(self):
        best_move = self.enemy_ai.make_move()
        if best_move:
            i, j = best_move
            if self.current_player == 2:
                self.cells[i][j].on_click()

        self.current_player = 1

    def check_game_over(self):
        self.player1_cells = self.player2_cells = 0

        for row in self.cells:
            for cell in row:
                if cell.clicked_by == 1:
                    self.player1_cells += 1
                elif cell.clicked_by == 2:
                    self.player2_cells += 1
                    self.player2_has_moved = True

        if self.player2_has_moved:
            if self.player1_cells == 0:
                if self.game_type == 1:
                    self.gameover_path = "P2 Won.png"
                    self.gameover()
                    return True
                elif self.game_type == 2:
                    self.gameover_path = "AI Won.png"
                    self.gameover()
                    return True
            elif self.player2_cells == 0:
                self.gameover_path = "P1 Won.png"
                self.gameover()
                return True
    
        return False

    def gameover(self):
        self.canvas.delete(self.window_id)
        self.bg_image = Image.open(self.gameover_path)
        self.bg_image = self.bg_image.resize((self.width, self.height), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        for row_cells in self.cells:
            for cell in row_cells:
                cell.button.grid_forget()

        # Exit Button
        exit_image_path = 'Exit.png'
        self.exit_image = self.resize_image(exit_image_path, 350)
        self.exit_button = tk.Button (
            self.root, 
            image = self.exit_image, 
            borderwidth = 0, 
            highlightthickness=0, 
            highlightbackground="black", 
            activebackground="#ffffff",
            command=self.root.quit
        )
        self.exit_button.place(x = self.width//2, y = 450, anchor = "center")

# Show the Application Window
app = ColorCombat()
app.root.mainloop()
