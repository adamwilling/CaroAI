# Author: aqeelanwar
# Created: 12 March,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
import numpy as np

from CaroProblem import *


class Window():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):

        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.geometry()
        self.window.title("Caro Game")

        self.size = tk.IntVar()
        self.size.set(30)

        self.size_of_board = 1080
        self.symbol_size = 15
        self.symbol_thickness = 5
        self.symbol_X_color = '#EE4035'
        self.symbol_O_color = '#0492CF'

        self.caro = CaroProblem(
            self.size.get(), self.size.get(), 5)
        self.state = GameState(
            to_move='X',
            utility=1,
            board={},
            moves=[(x, y) for x in range(0, self.size.get())
                   for y in range(0, self.size.get())]
        )

        self.canvas = Canvas(
            self.window, width=self.size_of_board, height=self.size_of_board)
        self.canvas.pack()
        self.canvas.bind(
            "<Button-1>", self.click)

        self.mode = 2  # 1: Chơi với máy, 2: 2 người chơi. Mặc định khi mới chạy chương trình là 2 người chơi

        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

        self.main_image = tk.PhotoImage(file="./caro.png")
        self.image_label = tk.Label(
            self.window, image=self.main_image).place(x=60, y=40)

        # Thay đổi kích thước bảng
        self.size_label = tk.Label(
            self.window, text="Size:", font=("Times new roman bold", 20))
        self.size_label.place(x=60, y=600)
        self.size_entered = tk.Entry(
            self.window, width=5, textvariable=self.size, justify = CENTER, font=("Times new roman", 20))
        self.size_entered.place(x=130, y=600)
        self.btn_change_size = tk.Button(self.window, text="Change", width=12, font=(
            "Times new roman", 15), bd=1, command=self.new_game).place(x=228, y=600)

        # Button chuyển chế độ chơi sang người với máy
        self.btn_single_player = tk.Button(self.window, text="Single player", width=20, font=(
            "Times new roman", 20), bd=1, command=lambda: self.change_mode(1)).place(x=60, y=700)

        # Button quit game
        self.btn_multi_player = tk.Button(self.window, text="Multi player", width=20, font=(
            "Times new roman", 20), bd=1, command=lambda: self.change_mode(2)).place(x=60, y=800)

        # Button new game
        self.btn_new_game = tk.Button(self.window, text="New game", width=20, font=(
            "Times new roman", 20), bd=1, command=self.new_game).place(x=60, y=900)

        # Button quit game
        self.btn_quit_game = tk.Button(self.window, text="Quit game", width=20, font=(
            "Times new roman", 20), bd=1, command=lambda: self.window.destroy()).place(x=60, y=1000)

        self.initialize_board()

    def mainloop(self):
        self.window.mainloop()

    def change_mode(self, new_mode):
        if self.mode != new_mode and new_mode == 1:
            self.mode = 1
            self.new_game()
        elif self.mode != new_mode and new_mode == 2:
            self.mode = 2
            self.new_game()

    def initialize_board(self):
        for i in range(self.size.get() - 1):
            self.canvas.create_line((i + 1) * self.size_of_board / self.size.get(),
                                    0, (i + 1) * self.size_of_board / self.size.get(), self.size_of_board)
        for i in range(self.size.get() - 1):
            self.canvas.create_line(0, (i + 1) * self.size_of_board / self.size.get(),
                                    self.size_of_board, (i + 1) * self.size_of_board / self.size.get())

    def new_game(self):
        self.symbol_size = 300 / self.size.get()
        self.canvas.delete("all")
        self.state = GameState(
            to_move='X',
            utility=1,
            board={},
            moves=[(x, y) for x in range(0, self.size.get())
                   for y in range(0, self.size.get())]
        )
        self.initialize_board()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        # logical_position: vị trí logic trên bàn cờ
        # grid_position: vị trí tọa đồ trên GUI
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                                grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size, width=self.symbol_thickness,
                                outline=self.symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                                grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size, width=self.symbol_thickness,
                                fill=self.symbol_X_color)
        self.canvas.create_line(grid_position[0] - self.symbol_size, grid_position[1] + self.symbol_size,
                                grid_position[0] + self.symbol_size, grid_position[1] - self.symbol_size, width=self.symbol_thickness,
                                fill=self.symbol_X_color)

    def display_gameover(self):
        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = self.symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = self.symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(
            self.size_of_board / 2, self.size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(self.size_of_board / 2, 5 * self.size_of_board / 8, font="cmr 40 bold", fill="blue",
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(self.size_of_board / 2, 3 * self.size_of_board / 4, font="cmr 30 bold", fill="blue",
                                text=score_text)
        self.reset_board = True

        score_text = 'Play again \n'
        self.canvas.create_text(self.size_of_board / 2, 15 * self.size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (self.size_of_board / self.size.get()) * logical_position + self.size_of_board / (self.size.get() * 2)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return tuple(np.array(grid_position // (self.size_of_board / self.size.get()), dtype=int))

    def is_grid_occupied(self, logical_position):
        return logical_position not in self.state.moves

    def is_winner(self, player, move):
        return self.caro.compute_utility(self.state.board, move, player) == 1 or self.caro.compute_utility(self.state.board, move, player) == -1

    def is_tie(self):
        return self.state.utility != 0 and len(self.state.moves) == 0

    def is_gameover(self, move):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X', move)
        if not self.X_wins:
            self.O_wins = self.is_winner('O', move)

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        if self.mode == 1:      # Xử lý chế độ 1 người chơi (chơi với máy)
            if not self.reset_board:
                if self.state.to_move == "X":
                    if not self.is_grid_occupied(logical_position):
                        self.state = self.caro.result(
                            self.state, logical_position)
                        self.draw_X(logical_position)
                else:
                    if not self.is_grid_occupied(logical_position):
                        self.state = self.caro.result(
                            self.state, logical_position)
                        self.draw_O(logical_position)
                        # Check if game is concluded
                if self.is_gameover(logical_position):
                    self.display_gameover()
                else:
                    ai_move = ai_player(self.caro, self.state)
                    if self.state.to_move == "X":
                        if not self.is_grid_occupied(ai_move):
                            self.state = self.caro.result(
                                self.state, tuple(ai_move))
                            self.draw_X(ai_move)
                    else:
                        if not self.is_grid_occupied(logical_position):
                            self.state = self.caro.result(
                                self.state, tuple(ai_move))
                            self.draw_O(ai_move)
                    if self.is_gameover(ai_move):
                        self.display_gameover()
            else:  # Play Again
                self.new_game()
                self.reset_board = False

        elif self.mode == 2:    # Xử lý chế độ 2 người chơi
            if not self.reset_board:
                if self.state.to_move == "X":
                    if not self.is_grid_occupied(logical_position):
                        self.state = self.caro.result(
                            self.state, logical_position)
                        self.draw_X(logical_position)
                else:
                    if not self.is_grid_occupied(logical_position):
                        self.state = self.caro.result(
                            self.state, logical_position)
                        self.draw_O(logical_position)
                if self.is_gameover(logical_position):
                    self.display_gameover()
            else:  # Game mới
                self.new_game()
                self.reset_board = False


game_instance = Window()
game_instance.mainloop()
