import tkinter as tk
from tkinter import messagebox
from tkinter.constants import DISABLED
from exceptions import ColumnIsFullException, SetOfRulesNotDefinedException
from player import Player
from rules import NormalRules, FiveInARow
from checker import Checker

class ConnectFourWindow():
    def __init__(self, default=True, logic=None):
        if default:
            self._logic = NormalRules(6, 7, Player("Gracz 1", Checker.RED), Player("Gracz 2", Checker.YELLOW))
        elif not default and logic is not None:
            self._logic = logic
        else:
            raise SetOfRulesNotDefinedException("Nie podano zasad gry podczas inicjalizacji klasy ConnectFourWindow")
        # tworzenie okna aplikacji
        self._window = tk.Tk()
        self._screen_width = self._window.winfo_screenwidth()
        self._screen_height = self._window.winfo_screenheight()
        self._window.title("Cztery w rzędzie")
        self._window.resizable(0, 0)
        
        # ramka zawierająca: informację kto ma wykonać ruch, przycisk reset oraz lista rozwijaną do wyboru reguł gry
        self._header = self.__create_header()
        # przyciski do planszy
        self._buttons_row = self.__create_buttons()
        # plansza
        self._board = self.__create_board()
        
        self._window.update()
        width = self._board.winfo_width()
        height = self._board.winfo_height() + 230
        self._window.geometry("%dx%d+%d+%d" % (width, height, self._screen_width/2 - width/2, self._screen_height/2 - height/2))

        
        
    
    def __create_header(self):
        """Metoda odpowiedzialna za tworzenie pola kogo tura, przycisku reset oraz listy rozwijanej do wyboru trybów.
        Metoda zwraca ramkę, w której znajdują się wyżej wymienione rzeczy."""
        header = tk.Frame(self._window)
        header.place(x=0, y=0, height=180, width=600)

        self._btn_reset = tk.Button(master=header, bg="blue", text="RESET\nGRY", command=lambda: self.reset())
        self._btn_reset.place(in_= header, x=30, rely=0.25, width=100, height=50)

        self._lbl_whose_turn = tk.Label(text = "", master=header, foreground = "white", background = "black")
        self.change_whose_turn_lbl()
        self._lbl_whose_turn.place(in_= header, x=225, rely=0.25, width=150, height=50)
        
        default_mode = tk.StringVar(header)
        default_mode.set("Standard")
        self._mode_list = tk.OptionMenu(header, default_mode, "Standard", "Pięć w rzędzie", "PopOut", command=self.set_rules)
        self._mode_list.place(in_= header, x=570, rely=0.25, anchor="ne", width=100, height=50)

        return header
    
    def __create_buttons(self):
        """Metoda odpowiedzialna za tworzenie przycisków, z których każdy odpowiedzialny jest za jedną kolumnę planszy.
        Metoda zwraca ramkę, w której zostały umieszczone przyciski"""
        buttons_row = tk.Frame(self._window, borderwidth=0)
        buttons_row.place(x=0, y=180, width=4*(self._logic._n_cols+1)+80*self._logic._n_cols, height=50)

        for i in range(self._logic._n_cols):
            button = tk.Button(buttons_row, bg=self._logic.whose_turn.checker.name, border=1, text=str(i), command=lambda s=i: self.drop_checker(s), highlightthickness=1, relief='flat')
            button.place(in_= buttons_row, x=i*84, width=88, height=50)

        return buttons_row

    def __create_board(self):
        """Metoda tworząca planszę.
        Metoda zwraca planszę jako obiekt tk.Canvas"""
        space = 4
        board = tk.Canvas(self._window, bg="blue", width=space*(self._logic._n_cols+1)+80*self._logic._n_cols, height=space*(self._logic._n_rows+1)+80*self._logic._n_rows, highlightthickness=0)
        board.place(x=0, y=230)
        
        for i in range(self._logic._n_rows):
            for j in range(self._logic._n_cols):
                color = self._logic.board[-i-1][-j-1].name if self._logic.board[-i-1][-j-1] is not None else "#f8f4f4"
                self.print_coin(x=44+space*j+80*j, y=44+space*i+80*i, r=40, canvas=board, color=color)

        return board

    def set_rules(self, option):
        if option == "Standard":
            self.reset()
        elif option == "Pięć w rzędzie":
            if self._window is not None:
                self._window.destroy()
            self.__init__(False, FiveInARow(Player("Gracz 1", Checker.RED), Player("Gracz 2", Checker.YELLOW)))
        elif option == "PopOut":
            pass

    def print_coin(self, x, y, r, canvas, color="#f8f4f4"):
        """Metoda odpowiedzialna za tworzenie koła.
        Ta metoda nic nie zwraca"""
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, width=0)

    def drop_checker(self, col):
        try:
            checker, x, y =  self._logic.drop_checker(col)
        except ColumnIsFullException as e:
            self.__show_alert(e)
            return

        color = "red" if checker == Checker.RED else "yellow" if checker == Checker.YELLOW else "#f8f4f4"
        space = 4
        self.print_coin(x=44+space*y+80*y, y=44+space*x+80*x, r=40, canvas=self._board, color=color)
        if self._logic.check_win():
            self.change_buttons_property("state", DISABLED)
            self.print_end_game_info(False)
            return
        if self._logic.check_draw():
            self.change_buttons_property("state", DISABLED)
            self.print_end_game_info(True)

        self._logic.change_player()
        self.change_buttons_property("bg", self._logic.whose_turn.checker.name)
        self.change_whose_turn_lbl()

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
        messagebox.showinfo("Pełna kolumna", msg)

    def reset(self):
        if self._window is not None:
            self._window.destroy()
        self.__init__()
        

    def mainloop(self):
        tk.mainloop()