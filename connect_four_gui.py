import tkinter as tk
from player import Player
from rules import NormalRules
from checker import Checker

class ConnectFourWindow():
    def __init__(self):
        self._logic = NormalRules(6, 7, Player("Gracz 1", Checker.RED), Player("Gracz 2", Checker.YELLOW))
        
        # tworzenie okna aplikacji
        self._window = tk.Tk()
        self._window.title("Cztery w rzędzie")
        self._window.resizable(0, 0)
        self._window.geometry("600x700")

        # ramka zawierająca: informację kto ma wykonać ruch, przycisk reset oraz lista rozwijaną do wyboru reguł gry
        self._header = self.__create_header()
        # przyciski do planszy
        self._buttons_row = self.__create_buttons()
        # plansza
        self._board = self.__create_board()
    
    def __create_header(self):
        """Metoda odpowiedzialna za tworzenie pola kogo tura, przycisku reset oraz listy rozwijanej do wybotu trybów.
        Metoda zwraca ramkę, w której znajdują się wyżej wymienione rzeczy."""
        header = tk.Frame(self._window)
        header.place(x=0, y=0, height=120, width=600)

        self._lbl_whose_turn = tk.Label(text = "", master=header, foreground = "white", background = "black")
        self.change_whose_turn_lbl()
        self._lbl_whose_turn.place(in_= header, x=225, rely=0.25, width=150, height=50)

        self._btn_reset = tk.Button(master=header, bg="blue", text="RESET\nGRY", command=lambda: print("RESET"))
        self._btn_reset.place(in_= header, x=30, rely=0.25, width=100, height=50)
        
        default_mode = tk.StringVar(header)
        default_mode.set("Tryb 1")
        self._mode_list = tk.OptionMenu(header, default_mode, "Tryb 1", "Tryb 2", "Tryb 3")
        self._mode_list.place(in_= header, x=570, rely=0.25, anchor="ne", width=100, height=50)

        return header
    
    def __create_buttons(self):
        """Metoda odpowiedzialna za tworzenie przycisków, z których każdy odpowiedzialny jest za jedną kolumnę planszy.
        Metoda zwraca ramkę, w której zostały umieszczone przyciski"""
        buttons_row = tk.Frame(self._window)
        buttons_row.place(x=17, y=120, width=600, height=50)

        for i in range(7):
            przycisk = tk.Button(buttons_row, bg="red", text=str(i), command=lambda s=i: self.drop_coin(s))
            przycisk.place(in_= buttons_row, x=i*80+i, width=80, height=50)

        return buttons_row

    def __create_board(self):
        """Metoda tworząca planszę.
        Metoda zwraca planszę jako obiekt tk.Canvas"""
        board = tk.Canvas(self._window, bg="blue", width=565, height=485)
        board.place(x=15, y=190)

        for i in range(6):
            for j in range(7):
                self.draw_coin(x=41+j*80+j, y=40+i*80+i, r=35, canvas=board)

        return board

    def draw_coin(self, x, y, r, canvas, color="#f8f4f4"):
        """Metoda odpowiedzialna za tworzenie koła.
        Ta metoda nic nie zwraca"""
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, width=0)

    @property
    def header(self):
        return self._header
    
    @property
    def buttons_row(self):
        return self._buttons_row
    
    @property
    def board(self):
        return self._board

    def drop_coin(self, col):
        # print(f"Button {col} is clicked!")
        checker, x, y =  self._logic.dropCoin(col)
        color = "red" if checker == Checker.RED else "yellow" if checker == Checker.YELLOW else "#f8f4f4"
        self.draw_coin(x=41+y*80+y, y=40+x*80+x, r=35, canvas=self._board, color=color)
        if self._logic.checkWin():
            self.__congratulate_winner()

        self._logic.changePlayer()
        self.change_whose_turn_lbl()

    def __congratulate_winner(self):
        alert = tk.Toplevel(self._window)
        alert.geometry("700x250")
        alert.title("Mamy zwycięzcę")
        lbl_for_winner = tk.Label(alert, text= f"Wygrał {self._logic.whoWin().name}", font=('Roboto 34 bold'))
        lbl_for_winner.place(relx = 0.5, rely = 0.5, anchor="center")

    def change_whose_turn_lbl(self):
        self._lbl_whose_turn["text"] = "Tura gracza 1" if self._logic.whose_turn.checker == Checker.RED else "Tura gracza 2"

    def mainloop(self):
        tk.mainloop()