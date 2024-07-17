from tkinter import *
from pil import Image, ImageTk
import random

class Cells:
    def __init__(self, master, row, column, colorcombat):
        self.colorcombat = colorcombat
        self.row = row
        self.column = column
        self.count = 0
        self.clicked_by = None
        if self.colorcombat.rows == 3:
            width = 100
        elif self.colorcombat.rows == 4:
            width = 93
        elif self.colorcombat.rows == 5:
            width = 85
        elif self.colorcombat.rows == 6:
            width = 77
        elif self.colorcombat.rows == 7:
            width = 69
        elif self.colorcombat.rows == 8:
            width = 61
        elif self.colorcombat.rows == 9:
            width = 53
        elif self.colorcombat.rows == 10:
            width = 45

        p0_path = 'P0.png'
        self.p0 = self.resize_image(p0_path, width)
        p11_path = 'P11.png'
        self.p11 = self.resize_image(p11_path, width)
        p12_path = 'P12.png'
        self.p12 = self.resize_image(p12_path, width)
        p13_path = 'P13.png'
        self.p13 = self.resize_image(p13_path, width)
        p14_path = 'P14.png'
        self.p14 = self.resize_image(p14_path, width)
        p21_path = 'P21.png'
        self.p21 = self.resize_image(p21_path, width)
        p22_path = 'P22.png'
        self.p22 = self.resize_image(p22_path, width)
        p23_path = 'P23.png'
        self.p23 = self.resize_image(p23_path, width)
        p24_path = 'P24.png'
        self.p24 = self.resize_image(p24_path, width)

        self.button = Button (
            master = master, 
            image = self.p0,
            borderwidth = 0, 
            highlightthickness=0, 
            command= self.on_click,
        )
        self.button.grid(row = row, column = column, padx = 5, pady = 5)

        self.cell_type = self.get_cell_type(row, column)
    
    def resize_image(self, image_path, width):
        original_image = Image.open(image_path).convert("RGBA")
        aspect_ratio = original_image.width / original_image.height
        height = int(width / aspect_ratio)
        resized_image = original_image.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)

    def on_click(self):
        if (self.clicked_by is None) or (self.clicked_by == self.colorcombat.current_player):
            max_count = self.get_max_count()
            
            if self.count < max_count:
                self.clicked_by = self.colorcombat.current_player
                self.count += 1

                if self.colorcombat.current_player == 1:
                    player = 'p1'
                else:
                    player = 'p2'
                image_attr_name = f"{player}{self.count}"
                image = getattr(self, image_attr_name, None)
                self.button.configure(image = image)

                if (self.count == 2 and self.cell_type in ('corner_ul', 'corner_ur', 'corner_ll', 'corner_lr')) or \
                   (self.count == 3 and self.cell_type in ('edge_top', 'edge_bottom', 'edge_left', 'edge_right')) or \
                   self.count == 4:
                    self.explode()
                    self.button.configure(image = self.p0)
                
                self.check_chain_reactions()

                if self.colorcombat.check_game_over():
                    self.disable_buttons()
                    return

                self.switch_players()
            else:
                print(f"Cannot increment: max count reached for {self.cell_type}")

    def get_max_count(self):
        if self.cell_type in ('corner_ul', 'corner_ur', 'corner_ll', 'corner_lr'):
            return 2
        elif self.cell_type in ('edge_top', 'edge_bottom', 'edge_left', 'edge_right'):
            return 3
        else:
            return 4

    def check_chain_reactions(self):
        while True:
            recheck_board = False
            for i in range(self.colorcombat.rows):
                for j in range(self.colorcombat.columns): 
                    cell = self.colorcombat.cells[i][j]
                    if (cell.count == 2 and cell.cell_type in ('corner_ul', 'corner_ur', 'corner_ll', 'corner_lr')) or \
                       (cell.count == 3 and cell.cell_type in ('edge_top', 'edge_bottom', 'edge_left', 'edge_right')) or \
                       cell.count == 4:
                        cell.explode()
                        cell.button.configure(image = self.p0)
                        recheck_board = True
            if not recheck_board:
                break

    def disable_buttons(self):
        for row in self.colorcombat.cells:
            for cell in row:
                cell.button.config(state=DISABLED)

    def switch_players(self):
        if self.colorcombat.game_type == 1:
            self.colorcombat.current_player = 2 if self.colorcombat.current_player == 1 else 1
            self.colorcombat.player.config(text=f"Current Player: Player {self.colorcombat.current_player}")
        else:
            self.colorcombat.current_player = 2
            self.colorcombat.player.config(text="Current Player: Player 2")
            self.colorcombat.root.after(500, self.colorcombat.enemy_move)

    def get_cell_type(self, row, column):
        rows = self.colorcombat.rows
        columns = self.colorcombat.columns

        if row == 0 and column == 0:
            return 'corner_ul'
        elif row == 0 and column == columns - 1:
            return 'corner_ur'
        elif row == rows - 1 and column == 0:
            return 'corner_ll'
        elif row == rows - 1 and column == columns - 1:
            return 'corner_lr'
        elif row == 0:
            return 'edge_top'
        elif row == rows - 1:
            return 'edge_bottom'
        elif column == 0:
            return 'edge_left'
        elif column == columns - 1:
            return 'edge_right'
        else:
            return 'center'

    def explode(self):
        self.count = 0
        self.clicked_by = None

        if self.cell_type == 'corner_ul':
            self.explode_to_right()
            self.explode_to_bottom()
        elif self.cell_type == 'corner_ur':
            self.explode_to_left()
            self.explode_to_bottom()
        elif self.cell_type == 'corner_ll':
            self.explode_to_right()
            self.explode_to_top()
        elif self.cell_type == 'corner_lr':
            self.explode_to_left()
            self.explode_to_top()
        elif self.cell_type == 'edge_top':
            self.explode_to_left()
            self.explode_to_right()
            self.explode_to_bottom()
        elif self.cell_type == 'edge_bottom':
            self.explode_to_left()
            self.explode_to_right()
            self.explode_to_top()
        elif self.cell_type == 'edge_left':
            self.explode_to_right()
            self.explode_to_top()
            self.explode_to_bottom()
        elif self.cell_type == 'edge_right':
            self.explode_to_left()
            self.explode_to_top()
            self.explode_to_bottom()
        elif self.cell_type == 'center':
            self.explode_to_left()
            self.explode_to_right()
            self.explode_to_top()
            self.explode_to_bottom()

    def explode_to_left(self):
        self.explode_neighbors(self.row, self.column - 1)

    def explode_to_right(self):
        self.explode_neighbors(self.row, self.column + 1)

    def explode_to_top(self):
        self.explode_neighbors(self.row - 1, self.column)

    def explode_to_bottom(self):
        self.explode_neighbors(self.row + 1, self.column)
    
    def explode_neighbors(self, row, column):
        try:
            neighbor = self.colorcombat.cells[row][column]
            if neighbor.count < neighbor.get_max_count():
                neighbor.clicked_by = self.colorcombat.current_player
                neighbor.count += 1

                if self.colorcombat.current_player == 1:
                    player = 'p1'
                else:
                    player = 'p2'
                image_attr_name = f"{player}{neighbor.count}"
                image = getattr(self, image_attr_name, None)
                neighbor.button.configure(image = image)

        except IndexError:
            pass

class EnemyAI:
    def __init__(self, colorcombat):
        self.colorcombat = colorcombat
        self.transposition_table = {}

    def make_move(self):
        best_move = None
        best_score = float('-inf')
        for move in self.get_possible_moves():
            score = self.alpha_beta(move, 4, float('-inf'), float('inf'), True)  # Increased depth
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def alpha_beta(self, move, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal():
            return self.evaluate_board()

        move_key = self.hash_board(move)
        if move_key in self.transposition_table:
            return self.transposition_table[move_key]

        if maximizing_player:
            max_eval = float('-inf')
            for child in self.get_possible_moves():
                eval = self.alpha_beta(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[move_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for child in self.get_possible_moves():
                eval = self.alpha_beta(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[move_key] = min_eval
            return min_eval

    def get_possible_moves(self):
        moves = []
        for i in range(self.colorcombat.rows):
            for j in range(self.colorcombat.columns):
                cell = self.colorcombat.cells[i][j]
                if cell.clicked_by is None or cell.clicked_by == 2:
                    moves.append((i, j))

        # Prioritize moves based on potential impact
        moves.sort(key=lambda move: self.colorcombat.cells[move[0]][move[1]].count, reverse=True)
        
        return moves

    def evaluate_board(self):
        score = 0
        for i in range(self.colorcombat.rows):
            for j in range(self.colorcombat.columns):
                cell = self.colorcombat.cells[i][j]
                cell_type = cell.cell_type
                cell_value = 1  # Default value for center cells

                if cell_type in ('corner_ul', 'corner_ur', 'corner_ll', 'corner_lr'):
                    cell_value = 5
                elif cell_type in ('edge_top', 'edge_bottom', 'edge_left', 'edge_right'):
                    cell_value = 3

                if cell.clicked_by == 2:
                    score += cell.count * cell_value
                elif cell.clicked_by == 1:
                    score -= cell.count * cell_value

                if cell.clicked_by == 1 and cell.count >= 2:
                    score -= 10  # Penalize for potential explosions

                neighbor_score = sum(
                    1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 0 <= i + dx < self.colorcombat.rows and 0 <= j + dy < self.colorcombat.columns
                    and self.colorcombat.cells[i + dx][j + dy].clicked_by == 2
                )
                score += neighbor_score

                if cell.clicked_by == 2 and cell.count >= 3:
                    score += 15

                # Encourage control of corners and edges
                if cell_type in ('corner_ul', 'corner_ur', 'corner_ll', 'corner_lr') and cell.clicked_by == 2:
                    score += 20
                if cell_type in ('edge_top', 'edge_bottom', 'edge_left', 'edge_right') and cell.clicked_by == 2:
                    score += 10

                # Add randomness to the score
                score += random.uniform(0, 0.01)

        return score

    def is_terminal(self):
        player1_cells = player2_cells = 0
        for row in self.colorcombat.cells:
            for cell in row:
                if cell.clicked_by == 1:
                    player1_cells += 1
                elif cell.clicked_by == 2:
                    player2_cells += 1

        return player1_cells == 0 or player2_cells == 0

    def hash_board(self, move):
        hash_value = 0
        for i in range(self.colorcombat.rows):
            for j in range(self.colorcombat.columns):
                cell = self.colorcombat.cells[i][j]
                hash_value ^= hash((i, j, cell.clicked_by, cell.count))
        return hash_value
