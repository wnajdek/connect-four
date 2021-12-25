import tkinter as tk
from tkinter import messagebox
from tkinter.constants import DISABLED
from exceptions import ColumnIsFullException
from player import Player
from rules import NormalRules
from checker import Checker

class ConnectFourWindow():
    def __init__(self):
        self._logic = NormalRules(6, 7, Player("Gracz 1", Checker.RED), Player("Gracz 2", Checker.YELLOW))
        
        # tworzenie okna aplikacji
        self._window = tk.Tk()
        self._screen_width = self._window.winfo_screenwidth()
        self._screen_height = self._window.winfo_screenheight()
        self._window.title("Cztery w rzędzie")
        self._window.resizable(0, 0)
        self._window.geometry("600x700+%d+%d" % (self._screen_width/2 - 600/2, self._screen_height/2 - 700/2))
        self._window.option_add('*Dialog.msg.font', 'Helvetica 32')
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
        header.place(x=0, y=0, height=180, width=600)

        self._lbl_whose_turn = tk.Label(text = "", master=header, foreground = "white", background = "black")
        self.change_whose_turn_lbl()
        self._lbl_whose_turn.place(in_= header, x=225, rely=0.25, width=150, height=50)

        self._btn_reset = tk.Button(master=header, bg="blue", text="RESET\nGRY", command=lambda: self.reset())
        self._btn_reset.place(in_= header, x=30, rely=0.25, width=100, height=50)
        
        default_mode = tk.StringVar(header)
        default_mode.set("Tryb 1")
        self._mode_list = tk.OptionMenu(header, default_mode, "Tryb 1", "Tryb 2", "Tryb 3")
        self._mode_list.place(in_= header, x=570, rely=0.25, anchor="ne", width=100, height=50)

        return header
    
    def __create_buttons(self):
        """Metoda odpowiedzialna za tworzenie przycisków, z których każdy odpowiedzialny jest za jedną kolumnę planszy.
        Metoda zwraca ramkę, w której zostały umieszczone przyciski"""
        buttons_row = tk.Frame(self._window, borderwidth=0)
        buttons_row.place(x=17, y=170, width=600, height=50)

        for i in range(7):
            button = tk.Button(buttons_row, bg=self._logic.whose_turn.checker.name, text=str(i), command=lambda s=i: self.drop_coin(s), highlightthickness=1, relief='flat')
            button.place(in_= buttons_row, x=i*80+i, width=80, height=50)

        return buttons_row

    def __create_board(self):
        """Metoda tworząca planszę.
        Metoda zwraca planszę jako obiekt tk.Canvas"""
        board = tk.Canvas(self._window, bg="blue", width=566, height=485)
        board.place(x=15, y=190)

        for i in range(6):
            for j in range(7):
                self.draw_coin(x=41+j*80+j, y=40+i*80+i, r=35, canvas=board)

        return board

    def draw_coin(self, x, y, r, canvas, color="#f8f4f4"):
        """Metoda odpowiedzialna za tworzenie koła.
        Ta metoda nic nie zwraca"""
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, width=0)

    # @property
    # def header(self):
    #     return self._header
    
    # @property
    # def buttons_row(self):
    #     return self._buttons_row
    
    # @property
    # def board(self):
    #     return self._board

    def drop_coin(self, col):
        try:
            checker, x, y =  self._logic.dropCoin(col)
        except ColumnIsFullException as e:
            self.__show_alert(e)
            return

        color = "red" if checker == Checker.RED else "yellow" if checker == Checker.YELLOW else "#f8f4f4"
        self.draw_coin(x=41+y*80+y, y=40+x*80+x, r=35, canvas=self._board, color=color)
        if self._logic.checkWin():
            self.change_buttons_property("state", DISABLED)
            self.print_end_game_info(False)
            return
        if self._logic.check_draw():
            self.change_buttons_property("state", DISABLED)
            self.print_end_game_info(True)

        self._logic.changePlayer()
        self.change_buttons_property("bg", self._logic.whose_turn.checker.name)
        self.change_whose_turn_lbl()

    def __congratulate_winner(self):
        alert = tk.Toplevel(self._window)
        alert.geometry("600x250+%d+%d" % (self._screen_width/2 - 600/2, self._screen_height/2 - 700/2))
        alert.title("Mamy zwycięzcę")
        lbl_for_winner = tk.Label(alert, text= f"Wygrał {self._logic.who_win().name}", font=('Roboto 34 bold'))
        lbl_for_winner.place(relx = 0.5, rely = 0.25, anchor="center")
        txt_info = "W celu rozegrania kolejnej partii naciśnij przycisk reset.\nJeżeli chcesz zagrać w innym trybie wybierz tryb z listy rozwijanej."
        lbl_info= tk.Label(alert, text=txt_info, font=('Roboto 12 bold'))
        lbl_info.place(relx = 0.5, rely = 0.5, anchor="center")
        btn_ok = tk.Button(alert, text="ok", font=('Roboto 12 bold'), bg=self._logic.whose_turn.checker.name, command=lambda: alert.destroy())
        btn_ok.place(relx = 0.5, rely = 0.75, width=70, height=50, anchor="center")
        # messagebox.showinfo("Mamy zwycięzcę", f"Wygrał {self._logic.whoWin().name}\n{txt_info}")

    def print_end_game_info(self, draw: bool):
        alert = tk.Toplevel(self._window)
        alert.geometry("600x250+%d+%d" % (self._screen_width/2 - 600/2, self._screen_height/2 - 700/2))
        if draw:
            alert.title("Remis")
            lbl_header_text = tk.Label(alert, text= f"REMIS", font=('Roboto 34 bold'))
        else:
            alert.title("Mamy zwycięzcę")
            lbl_header_text = tk.Label(alert, text= f"Wygrał {self._logic.who_win().name}", font=('Roboto 34 bold'))  
        lbl_header_text.place(relx = 0.5, rely = 0.25, anchor="center")

        txt_info = "W celu rozegrania kolejnej partii naciśnij przycisk reset.\nJeżeli chcesz zagrać w innym trybie wybierz tryb z listy rozwijanej."
        lbl_info = tk.Label(alert, text=txt_info, font=('Roboto 12 bold'))
        lbl_info.place(relx = 0.5, rely = 0.5, anchor="center")
        btn_ok = tk.Button(alert, text="ok", font=('Roboto 12 bold'), bg=self._logic.whose_turn.checker.name, command=lambda: alert.destroy())
        if draw:
            btn_ok["bg"] = "black"
            btn_ok["fg"] = "white"
        btn_ok.place(relx = 0.5, rely = 0.75, width=70, height=50, anchor="center")

    def change_whose_turn_lbl(self):
        self._lbl_whose_turn["text"] = "Tura gracza 1" if self._logic.whose_turn.checker == Checker.RED else "Tura gracza 2"

    def change_buttons_property(self, property, value):
        buttons_row_children = self._buttons_row.winfo_children()
        for i in range(len(buttons_row_children)):
            buttons_row_children[i][property] = value

    def __show_alert(self, msg):
        # alert = tk.Toplevel(self._window)
        # alert.geometry("450x150+%d+%d" % (self._screen_width/2 - 600/2 + 75, self._screen_height/2 - 700/2 + 100))
        # alert.title("")
        # lbl_alert = tk.Label(alert, text= msg, font=('Roboto 14 bold'))
        # lbl_alert.place(relx = 0.5, rely = 0.5, anchor="center")
        messagebox.showinfo("Pełna kolumna", msg)

    def reset(self):
        if self._window is not None:
            self._window.destroy()
        self.__init__()
        

    def mainloop(self):
        tk.mainloop()