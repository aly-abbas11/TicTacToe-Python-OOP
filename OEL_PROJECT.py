from tkinter import *
import pygame

class TicTacToeGame:
    def __init__(self, root):
        pygame.mixer.init()

        pygame.mixer.music.load("assets/background_music.mp3")  
        self.win_sound = pygame.mixer.Sound("assets/win_sound.mp3")  
        self.draw_sound = pygame.mixer.Sound("assets/draw_sound.mp3")  
        self.click_sound = pygame.mixer.Sound("assets/click_sound.mp3")  

        self.root = root
        self.root.geometry("330x600")
        self.root.title("Tic Tac Toe")
        self.root.resizable(0, 0)

        self.board = {i: " " for i in range(1, 10)}
        self.turn = "x"
        self.game_end = False
        self.mode = None
        self.game_started = False
        self.buttons = []

        self.create_widgets()

    def create_widgets(self):
        frame1 = Frame(self.root)
        frame1.pack()
        self.title_label = Label(frame1, text="Tic Tac Toe", font=("Arial", 26), bg="orange", width=16)
        self.title_label.grid(row=0, column=0)

        self.option_frame = Frame(self.root, bg="grey")
        self.option_frame.pack()
        self.single_player_button = Button(self.option_frame, text="SinglePlayer", width=13, font=("Arial", 15),
                                           bg="lightgrey", command=self.change_mode_to_single_player)
        self.single_player_button.grid(row=0, column=0)
        self.multiplayer_button = Button(self.option_frame, text="Multiplayer", width=13, font=("Arial", 15),
                                         bg="lightgrey", command=self.change_mode_to_multiplayer)
        self.multiplayer_button.grid(row=0, column=1)

        frame2 = Frame(self.root, bg="yellow")
        frame2.pack()
        for i in range(3):
            for j in range(3):
                button = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30), bg="yellow")
                button.grid(row=i, column=j)
                button.bind("<Button-1>", self.play)
                self.buttons.append(button)

        restart_button = Button(frame2, text="Restart Game", width=19, font=("Arial", 20), bg="green",
                                 command=self.restart_game)
        restart_button.grid(row=4, column=0, columnspan=3)

        self.start_button = Button(self.root, text="Start Game", font=("Arial", 20), bg="blue", fg="white",
                                    command=self.start_game)
        self.start_button.pack(pady=10)

    def change_mode_to_single_player(self):
        if not self.game_started:
            self.mode = "singlePlayer"
            self.title_label.config(text="Mode: Single Player")

    def change_mode_to_multiplayer(self):
        if not self.game_started:
            self.mode = "multiPlayer"
            self.title_label.config(text="Mode: Multiplayer")

    def start_game(self):
        if not self.mode:
            self.title_label.config(text="Select a mode first")
            return
        self.game_started = True
        pygame.mixer.music.play(-1)
        self.title_label.config(text="Tic Tac Toe Started")
        self.start_button["state"] = "disabled"

    def restart_game(self):
        if not self.game_started:
            return
        self.game_end = False
        self.turn = "x"
        self.board = {i: " " for i in range(1, 10)}
        for button in self.buttons:
            button["text"] = " "
        self.title_label.config(text="Tic Tac Toe")
        self.start_button["state"] = "normal"
        self.game_started = False
        self.mode = None
        self.single_player_button["state"] = "normal"
        self.multiplayer_button["state"] = "normal"
        pygame.mixer.music.stop()

    def update_board(self):
        for key in self.board.keys():
            self.buttons[key - 1]["text"] = self.board[key]

    def check_for_win(self, player):
        return (self.board[1] == self.board[2] == self.board[3] == player or
                self.board[4] == self.board[5] == self.board[6] == player or
                self.board[7] == self.board[8] == self.board[9] == player or
                self.board[1] == self.board[4] == self.board[7] == player or
                self.board[2] == self.board[5] == self.board[8] == player or
                self.board[3] == self.board[6] == self.board[9] == player or
                self.board[1] == self.board[5] == self.board[9] == player or
                self.board[3] == self.board[5] == self.board[7] == player)

    def check_for_draw(self):
        return all(self.board[i] != " " for i in self.board.keys())

    def play_computer(self):
        for key in self.board.keys():
            if self.board[key] == " ":
                self.board[key] = "o"
                break

    def play(self, event):
        if self.game_end or not self.game_started:
            return
        button = event.widget
        clicked = int(button.grid_info()["row"] * 3 + button.grid_info()["column"] + 1)
        if self.board[clicked] == " ":
            self.click_sound.play()
            self.board[clicked] = self.turn
            self.update_board()

            if self.check_for_win(self.turn):
                pygame.mixer.music.stop()
                self.win_sound.play()
                self.title_label.config(text=f"{self.turn} wins the game")
                self.game_end = True
                return

            if self.check_for_draw():
                pygame.mixer.music.stop()
                self.draw_sound.play()
                self.title_label.config(text="Game Draw")
                self.game_end = True
                return

            self.turn = "o" if self.turn == "x" else "x"

            if self.mode == "singlePlayer" and self.turn == "o":
                self.play_computer()
                self.update_board()
                if self.check_for_win(self.turn):
                    pygame.mixer.music.stop()
                    self.win_sound.play()
                    self.title_label.config(text=f"{self.turn} wins the game")
                    self.game_end = True
                elif self.check_for_draw():
                    pygame.mixer.music.stop()
                    self.draw_sound.play()
                    self.title_label.config(text="Game Draw")
                self.turn = "x"


if __name__ == "__main__":
    root = Tk()
    game = TicTacToeGame(root)
    root.mainloop()