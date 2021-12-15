import tkinter as tk

class ConnectFourWindow():
    def __init__(self):
        # tworzenie okna aplikacji
        self.window = tk.Tk()
        self.window.title("Cztery w rzędzie")
        self.window.resizable(0, 0)
        self.window.geometry("600x700")

        # ramka zawierająca: informację kto ma wykonać ruch, przycisk reset oraz lista rozwijaną do wyboru reguł gry
        self.header = self.__create_header()
        # przyciski do planszy
        self.buttons_row = self.__create_buttons()
        # plansza
        self.board = self.__create_board()
        
    
    def __create_header(self):
        """Metoda odpowiedzialna za tworzenie pola kogo tura, przycisku reset oraz listy rozwijanej do wybotu trybów.
        Metoda zwraca ramkę, w której znajdują się wyżej wymienione rzeczy."""
        header = tk.Frame(self.window)
        header.place(x=0, y=0, height=120, width=600)

        self.lbl_whose_turn = tk.Label(text = "Tura gracza 1", master=header, foreground = "white", background = "black")
        self.lbl_whose_turn.place(in_= header, x=225, rely=0.25, width=150, height=50)

        self.btn_reset = tk.Button(master=header, bg="blue", text="RESET\nGRY", command=lambda: print("RESET"))
        self.btn_reset.place(in_= header, x=30, rely=0.25, width=100, height=50)
        
        default_mode = tk.StringVar(header)
        default_mode.set("Tryb 1")
        self.mode_list = tk.OptionMenu(header, default_mode, "Tryb 1", "Tryb 2", "Tryb 3")
        self.mode_list.place(in_= header, x=570, rely=0.25, anchor="ne", width=100, height=50)

        return header
    
    def __create_buttons(self):
        """Metoda odpowiedzialna za tworzenie przycisków, z których każdy odpowiedzialny jest za jedną kolumnę planszy.
        Metoda zwraca ramkę, w której zostały umieszczone przyciski"""
        buttons_row = tk.Frame(self.window)
        buttons_row.place(x=17, y=120, width=600, height=50)

        for i in range(7):
            przycisk = tk.Button(buttons_row, bg="red", text=str(i), command=lambda: print("przycisk wrzucania monety"))
            przycisk.place(in_= buttons_row, x=i*80+i, width=80, height=50)

        return buttons_row

    def __create_board(self):
        """Metoda tworząca planszę.
        Metoda zwraca planszę jako obiekt tk.Canvas"""
        # plansza 6 wierszy na 7 kolumn
        board = tk.Canvas(self.window, bg="blue", width=565, height=485)
        board.place(x=15, y=190)
        board.tk.call('tk', 'scaling', 2.0)
        # okno.update()
        # print(plansza.winfo_width(), plansza.winfo_height(), rzad_przyciskow.winfo_width(), header.winfo_width())

        for i in range(6):
            for j in range(7):
                self.draw_coin(x=41+j*80+j, y=40+i*80+i, r=35, canvas=board)

        return board

    def draw_coin(self, x, y, r, canvas, color="#f8f4f4"):
        return canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, width=0)

    def mainloop(self):
        tk.mainloop()