import tkinter as tk
from tkinter import messagebox
from tkinter.constants import DISABLED
from PIL import ImageTk,Image
from logic.exceptions import CheckerCannotBeRemovedException, ColumnIsFullException, SetOfRulesNotDefinedException
from logic.rules_impl.normal_rules import NormalRules
from logic.rules_impl.five_in_a_row import FiveInARow
from logic.rules_impl.pop_out import PopOut
from logic.objects.checker import Checker
from logic.objects.player import Player

class ConnectFourWindow():
    """Klasa dodająca interfejs graficzny.
    
    Atrybuty:
        _logic (GameRules): obiekt z zasadami gry
        _window (tk.Tk): okno główne aplikacji
        _screen_width (int): szerokość ekranu
        _screen_height (int): wysokość ekranu
        _board (tk.Canvas): plansza do gry
        _checkers_map (list): przechowuje id monet na planszy _board
        _header (tk.Frame): ramka na górze aplikacji zawierająca przycisk reset, informację kogo tura i listę rozwijaną
        _buttons_row (tk.Frame): ramka z przyciskami do wrzucania monet
        _lbl_mode_rules (tk.Label): po najechaniu na ten widget wyświetlane są zasady gry
        _btn_reset (tk.Button): przycisk resetujący grę
        _lbl_whose_turn (tk.Label): pokazuje informację kogo tura
        _current_mode (tk.StringVar): przechowuje nazwę aktywnego trybu
        _mode_list (tk.OptionMenu): przechowuje listę trybów
        _arrow_image (PIL.ImageTk.PhotoImage): obraz strzałki do listy rozwijanej
        _buttons_row_image (PIL.ImageTk.PhotoImage): obraz koła przed najechaniem kursorem
        _buttons_row_image_HOVER (PIL.ImageTk.PhotoImage): obraz koła po najechaniu kursorem
        _mode_rules_popup (tk.Label): przechowuje zasady gry jako tk.Label
        _pop_out_buttons_row (tk.Frame): rząd przycisków do wyjmowania monet (tryb PopOut)
        _pop_out_image_red (PIL.ImageTk.PhotoImage): czerowny znak 'X' dla przycisków wyjmowania
        _pop_out_image_yellow (PIL.ImageTk.PhotoImage): żółty znak 'X' dla przycisków wyjmowania
        _checker_dropped (tk.BooleanVar): czy moneta już spadła (informacja potrzebna do opóźnienia wyświetlenia komunikatu o wygranej)

    Metody: 
        set_current_mode(): Ustaw aktywny tryb dla listy rozwijanej.
        display_rules(event): Wyświetl zasady gry.
        hide_rules(event): Schowaj zasady gry.
        resize_image(source, width, height): Zmień rozmiar obrazu.
        on_buttons_row_enter(event): Zmień obraz po najechaniu na przycisk.
        on_buttons_row_leave(event): Zmień obraz po zjechaniu z przycisku.
        move_checker(curr_checker, curr_y, end_y, speed=16): Przesuń monetę w dół z pozycji curr_y do end_y.
        print_checker(x, y, r, canvas, color="#f8f4f4"): Rysuj monetę.
        drop_checker(col): Upuść monetę po naciśnięciu przycisku.
        remove_checker(col): Wyjmij monetę.
        print_end_game_info(draw: bool): Wyświetl informacje końcowe.
        change_whose_turn_lbl(): Zmień informację kogo jest tura.
        disable_buttons(button_numbers: list = None): Wyłącz możliwość wciskania przycisków do wrzucania monet.
        change_buttons_property(property, value, button_numbers: list = None, pop_out=False): Zmień jedną cechę przycisków do wrzucania lub usuwania monet.
        unbind_buttons_event(event_type, button_numbers: list = None): Usuń obsługę zdarzenia przez przyciski do wrzucania monet.
        show_alert(title, msg): Wyświetl komunikat.
        reset(option): Resetuj grę w danym trybie.
        mainloop(): Uruchom pętlę zdarzeń.
    """
    
    def __init__(self, default=True, logic=None):
        """Inicjalizuj obiekt klasy ConnectFourWindow.
        
        Tworzone jest główne okno i wywoływana jest metoda __initialize_game, która ustala
        odpowiedni rozmiar planszy i dodaje wszystkie widgety wymagane w grze.

        Parametry:
            default (bool): czy gra ma zostać uruchomiona w trybie Normalnym
            logic (GameRules): obiekt z zasadami gry
        """
        
        # tworzenie okna aplikacji
        self._window = tk.Tk()
        self._window.title("Cztery w rzędzie")
        self._window.resizable(0, 0)

        self.__initialize_game(default, logic)
        
        
    def __initialize_game(self, default=True, logic=None):
        """Utwórz obiekty na podstawie trybu.

        Na początku ustalany jest tryb w jakim rozpocznie się gra.
        Tworzone jest okno gry i umieszczane w nim są wszystkie obiekty konieczne do rozpoczęcia rozgrywki.
        Jeżeli zmienna default jest True to gra uruchomi się ze standardowymi regułami (niezależnie od tego czy podany zostanie parametr logic).
        Aby przekazać obiekt z innymi zasadami, parametr default musi zostać ustawiony na False.

        Parametry:
            default (bool): czy gra ma zostać uruchomiona w trybie Normalnym
            logic (GameRules): obiekt z zasadami gry

        Zwraca:
            None
        """
        if default:
            self._logic = NormalRules(6, 7, Player("Gracz 1", Checker.RED), Player("Gracz 2", Checker.YELLOW))
        elif not default and logic is not None:
            self._logic = logic
        else:
            raise SetOfRulesNotDefinedException("Nie podano zasad gry podczas inicjalizacji klasy ConnectFourWindow")

        self._screen_width = self._window.winfo_screenwidth()
        self._screen_height = self._window.winfo_screenheight()

        # plansza
        self._board = self.__create_board()
        self._window.update()
        # ramka zawierająca: informację kto ma wykonać ruch, przycisk reset oraz lista rozwijaną do wyboru reguł gry
        self._header = self.__create_header()
        # przyciski do planszy
        self._buttons_row = self.__create_buttons()

        # modyfikacja wielkości okna na podstawie wielkości planszy do gry
        width = self._board.winfo_width()
        height = self._board.winfo_height() + 230
        self._window.geometry("%dx%d+%d+%d" % (width, height, self._screen_width/2 - width/2, self._screen_height/2 - height/2))

        # pole, które po najechaniu wyświetla zasady
        self._lbl_mode_rules = tk.Label(self._window, text="Zasady",
                                        bg="black",
                                        fg="white",
                                        font="Roboto 12 bold",
                                        cursor="question_arrow")
        self._lbl_mode_rules.place(x=0, y=0, width=70, height=40)
        self._lbl_mode_rules.bind("<Enter>", self.display_rules)
        self._lbl_mode_rules.bind("<Leave>", self.hide_rules)
        
        if self._current_mode.get() == "PopOut":
            self.__create_pop_out_buttons()

        # blokuję dwa skrajne przyciski dla trybu Pięć w rzędzie
        if self._current_mode.get() == "Pięć w rzędzie":
            self.disable_buttons([0, 8])
            self.change_buttons_property("text", "", [0, 8])
        
        self._checker_dropped = tk.BooleanVar()

    def __create_header(self):
        """Utwórz panel górny gry.
        
        Metoda odpowiedzialna za tworzenie pola kogo tura (_lbl_whose_turn), przycisku reset (_btn_reset) oraz listy rozwijanej do wyboru trybów (_mode_list).
        
        Zwraca:
            tk.Frame: zwraca ramkę, w której znajdują się wyżej wymienione rzeczy.
        """

        header = tk.Frame(self._window, bg="black")
        header.place(x=0, y=0, height=180, width=self._board.winfo_width())

        # przycisk reset
        self._btn_reset = tk.Button(master=header, 
                                    bg="blue", text="RESET\nGRY", 
                                    command=lambda: self.reset(self._current_mode.get()), 
                                    font=('Roboto 10 bold'),
                                    activebackground="blue",
                                    cursor="hand2")
        self._btn_reset.place(in_= header, x=80, rely=0.5, anchor="center", width=100, height=50)

        # pole kogo tura
        self._lbl_whose_turn = tk.Label(text = "",
                                        master=header,
                                        foreground = "white",
                                        background = "black",
                                        font=('Roboto 16 bold'))
        self.change_whose_turn_lbl()
        self._lbl_whose_turn.place(in_= header, relx=0.5, rely=0.5, anchor="center", width=150, height=150)
        
        # lista rozwijana
        self._current_mode = tk.StringVar(header)
        self._mode_list = tk.OptionMenu(header, self._current_mode, "Standard", "Pięć w rzędzie", "PopOut", command=self.reset)
        self._arrow_image = ImageTk.PhotoImage(Image.open("gui/img/arrow.png"))
        self._mode_list.configure(font=('Roboto 10 bold'),
                                  bg="brown",
                                  fg="white",
                                  activebackground="brown",
                                  highlightbackground="black",
                                  indicatoron=0,
                                  compound=tk.RIGHT,
                                  image=self._arrow_image,
                                  cursor="hand1")
        self.set_current_mode()
        self._mode_list.place(in_= header, x=self._board.winfo_width(), y=5, anchor="ne", width=150, height=50)
        # ustawiam style dla opcji na liście rozwijanej
        self._mode_list['menu'].configure(font=('Roboto 10 bold'),
                                          bg="brown",
                                          fg="white",
                                          activebackground="#7d1f1f")

        return header
    
    def __create_pop_out_buttons(self):
        """Utwórz rząd przycisków dla trybu PopOut (przyciski z 'X').
        
        Metoda odpowiedzialna za tworzenie przycisków i umieszczanie ich na planszy. Każdy przycisk odpowiedzialny jest za jedną kolumnę planszy.
        Po naciśnięciu przycisku moneta jest wyjmowana z danej kolumny (tryb PopOut).

        Zwraca:
            None
        """
        self._pop_out_buttons_row = tk.Frame(self._window, borderwidth=0, bg="black")
        self._pop_out_buttons_row.place(x=0, y=130, width=80*self._logic._n_cols, height=50)
        
        self._pop_out_image_yellow = ImageTk.PhotoImage(Image.open("gui/img/x-mark-yellow.png"))
        self._pop_out_image_red = ImageTk.PhotoImage(Image.open("gui/img/x-mark-red.png"))
        
        whose_turn_color = self._logic.whose_turn.checker.name.lower()

        for i in range(self._logic._n_cols):
            button = tk.Button(self._pop_out_buttons_row,
                            bg= "black",
                            image = self._pop_out_image_red if whose_turn_color == "red" else self._pop_out_image_yellow,
                            border=1,
                            text=str(i),
                            command=lambda s=i: self.remove_checker(s),
                            highlightthickness=1,
                            activeforeground="red",
                            activebackground="black",
                            relief='flat',
                            cursor="X_cursor")
            button.place(in_= self._pop_out_buttons_row, x=i*80, width=80, height=50)   
            

    def __create_buttons(self):
        """Utwórz rząd przycisków.
        
        Metoda odpowiedzialna za tworzenie przycisków i umieszczanie ich na planszy. Każdy przycisk odpowiedzialny jest za jedną kolumnę planszy.
        Po naciśnięciu przycisku moneta jest umieszczana w danej kolumnie (o ile kolumna nie jest pełna).

        Zwraca:
            tk.Frame: zwraca ramkę, w której znajdują się przyciski.
        """
        
        buttons_row = tk.Frame(self._window, borderwidth=0, bg="black")
        buttons_row.place(x=0, y=180, width=80*self._logic._n_cols, height=50)

        # obraz z dopiskiem HOVER pojawia się w momencie najechania na przycisk, po zjechaniu powraca obraz bez HOVER
        self._buttons_row_image = self.resize_image("gui/img/circle_black.png", 30, 30)
        self._buttons_row_image_HOVER = self.resize_image("gui/img/circle.png", 30, 30)
        for i in range(self._logic._n_cols):
            button = tk.Button(buttons_row,
                               bg=self._logic.whose_turn.checker.name,
                               image = self._buttons_row_image,
                               border=1,
                               text=str(i),
                               command=lambda s=i: self.drop_checker(s),
                               highlightthickness=1,
                               relief='flat',
                               cursor="sb_down_arrow")
            button.place(in_= buttons_row, x=i*80, width=80, height=50)
            button.bind('<Enter>',  self.on_buttons_row_enter)
            button.bind('<Leave>',  self.on_buttons_row_leave)
        
        return buttons_row

    def __create_board(self):
        """Utwórz planszę do gry.
        
        Metoda odpowiedzialna za tworzenie planszy i wypełnianie jej monetami (przed rozpoczęciem rozgrywki), jeżeli wymaga tego tryb (np. "Pięć w rzędzie"). 
        Tworzona jest tutaj również zmienna self._checkers_map, która przechowuje id monet na planszy self._board.

        Zwraca:
            tk.Canvas: zwraca planszę, jako obiekt tk.Canvas.
        """

        board = tk.Canvas(self._window,
                          width=80*self._logic._n_cols,
                          height=80*self._logic._n_rows,
                          highlightthickness=0)
        board.place(x=0, y=230)
        
        # obraz pola na monetę
        self.img_box = self.resize_image("gui/img/checker2.png", 81, 81)

        self._checkers_map = [[None for _ in range(self._logic._n_cols)] for _ in range(self._logic._n_rows)]
        for i in range(self._logic._n_rows):
            for j in range(self._logic._n_cols):
                color = self._logic.board[-i-1][-j-1].name if self._logic.board[-i-1][-j-1] is not None else "#f8f4f4"
                board.create_image(40+80*j, 40+80*i, image=self.img_box)
                if color.lower() in ("red", "yellow"):
                    self._checkers_map[-i-1][-j-1] = self.print_checker(x=40+80*j, y=40+80*i, r=38, canvas=board, color=color)

        return board

    def set_current_mode(self):
        """Ustaw aktywny tryb dla listy rozwijanej.
        
        Metoda zmienia widoczną nazwę trybu na liście rozwijanej na aktywny tryb gry.
        
        Zwraca:
            None
        """
        
        if isinstance(self._logic, FiveInARow):
            self._current_mode.set("Pięć w rzędzie")
        elif isinstance(self._logic, PopOut):
            self._current_mode.set("PopOut")
        elif isinstance(self._logic, NormalRules):
            self._current_mode.set("Standard")

    def display_rules(self, event):
        """Wyświetl zasady gry.
        
        Metoda wyświetla zasady gry dla aktualnie wybranego trybu. Zasady wyświetlane są w miejscu, w którym znajduje się plansza.
        Tekstowy opis zasad gry, który jest wyświetlany w programie, znajduje się w pliku rules_txt.py.

        Parametry:
            event (tkinter.Event): obiekt opisujący zdarzenie, które spowodowało wywołanie funkcji.

        Zwraca:
            None
        """
        
        board_width = self._board.winfo_width()
        
        self._mode_rules_popup = tk.Label(self._board, bg="white", relief="solid", borderwidth=6)
        self._mode_rules_popup.place(width=self._board.winfo_width(), height=self._board.winfo_height())

        header_txt = tk.Label(self._mode_rules_popup, text=self._logic.rules_txt_header, bg="white", font=('Roboto 34 bold'))
        header_txt.place(relx=0.5, y=50, anchor="center", width=board_width-50, height=100)

        info_txt = tk.Label(self._mode_rules_popup,
                            text=self._logic.rules_txt_info,
                            bg="white",
                            wraplength=board_width-100,
                            font=('Roboto 10 bold'),
                            justify="left")
        info_txt.place(relx=0.5, rely=0.5, anchor="center", width=board_width-20, height=300)
        

    def hide_rules(self, event):
        """Schowaj zasady gry.

        Metoda odpowiada za chowanie opisu zasad gry, gdy kursor myszy opuści określone miejsce w oknie gry.

        Parametry:
            event (tkinter.Event): obiekt opisujący zdarzenie, które spowodowało wywołanie funkcji.

        Zwraca:
            None
        """

        self._mode_rules_popup.place_forget()

    def resize_image(self, source, width, height):
        """Zmień rozmiar obrazu.
        
        Metoda zmienia długość i szerokość obrazu według według podanych parametrów.

        Parametry:
            source (str): ścieżka do obrazu.
            width (int): docelowa szerokość obrazu w pikselach.
            height (int): docelowa długość obrazu w pikselach.

        Zwraca:
            PIL.ImageTk.PhotoImage: obiekt zdjęcia o rządanych wymiarach.
        """

        full_size_circle_img = Image.open(source)
        full_size_circle_img_RGBA = full_size_circle_img.convert("RGBA")
        resized_circle = full_size_circle_img_RGBA.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_circle)

    def on_buttons_row_enter(self, event):
        """Zmień obraz po najechaniu na przycisk.
        
        Metoda działa dla przycisków odpowiedzialnych za umieszczanie monet w odpowiednich kolumnach.
        Parametr event pozwala określić dla którego przycisku ma zostać zmieniony obraz w jego wnętrzu.

        Parametry:
            event (tkinter.Event): obiekt opisujący zdarzenie, które spowodowało wywołanie funkcji.

        Zwraca:
            None
        """

        event.widget["image"] = self._buttons_row_image_HOVER

    def on_buttons_row_leave(self, event):
        """Zmień obraz po zjechaniu z przycisku.
        
        Metoda działa dla przycisków odpowiedzialnych za umieszczanie monet w odpowiednich kolumnach.
        Parametr event pozwala określić dla którego przycisku ma zostać zmieniony obraz w jego wnętrzu.

        Parametry:
            event (tkinter.Event): obiekt opisujący zdarzenie, które spowodowało wywołanie funkcji.

        Zwraca:
            None
        """
        
        event.widget["image"] = self._buttons_row_image

    def move_checker(self, curr_checker, curr_y, end_y, speed=16):
        """Przesuń monetę.

        Metoda wykorzystywana przy wrzucaniu i usuwaniu monet z planszy.
        Przesuwa monetę (curr_checker) od podanego curr_y do pozycji end_y.
        W momencie osiągnięcia oczekiwanej pozycji zmienna self._checker_dropped jest ustawiana na True.
        Ta zmienna ma za zadanie opóźnić wyświetlenie komunikatu o wygranej w self.drop_checker() do czasu aż moneta się nie zatrzyma.
        Parametry:
            curr_checker (int): id obiektu na canvas
            curr_y (int): pozycja aktualna obiektu
            end_y (int): pozycja do której przesuwana będzie moneta
            speed (int): prędkość, im mniejsza tym szybciej spada obiekt

        Zwraca:
            None
        """
        i = 0
        if curr_y < end_y:
            if curr_y % 40 == 0:
                i = 1
            self._board.move(curr_checker, 0, 10)
            self._board.after(speed - i, self.move_checker, curr_checker, curr_y+10, end_y, speed - i)
        else:
            self._checker_dropped.set(True)
    
    
    def print_checker(self, x, y, r, canvas, color="#f8f4f4"):
        """Rysuj monetę.
        
        Metoda rysuje monetę na planszy w podanym miejscu i o podanym kolorze.

        Parametry:
            x (int): określa położenie środka koła w poziomie.
            y (int): określa położenie środka koła w pionie.
            r (int): promień koła
            canvas (tk.Canvas): plasza, na której zostanie narysowana moneta.
            color (str): kolor monety

        Zwraca:
            int: id narysowanego właśnie obiektu dla danego canvas
        """
        
        curr_checker = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, width=0)
        canvas.tag_lower(curr_checker) # moneta będzie wyświetlana pod planszą

        return curr_checker
    
    def drop_checker(self, col):
        """Upuść monetę.
        
        Metoda bazuje na klasie opisującej reguły gry. Wykorzystuje metody zawarte w tej klasie.
        Po kliknięciu jednego z przycisków sprawdzane są warunki konieczne do umieszczenia monety w danej kolumnie.
        Jeżeli nie zostanie napotkany błąd wynikający z próby umieszczenia monety w zapełnionej kolumnie to do kolumny zostaje wrzucona moneta.
        Następnie sprawdzana jest potencjalna wygrana lub remis. Jeżeli nie ma wygranej ani remisu to drugi gracz dostaje możliwość wykonania ruchu.
        Parametry:
            col (int): indeks kolumny, do której ma zostać wrzucona moneta (0 to pierwsza kolumna od lewej).
        Zwraca:
            None
        """

        try:
            checker, x, y, win, draw =  self._logic.drop_checker(col)
        except ColumnIsFullException as e:
            self.show_alert("Pełna kolumna", e)
            return

        # dodawanie monety na planszę
        # najpierw rysuję monetę za pomocą self.print_checker() i zapisuję id stworzonego obiektu do curr_checker
        # aktualizuję macierz self._checkers_map, która przechowuje aktualny stan planszy (id obiektów na odpowiednich pozycjach)
        # na końcu wywoływana jest metoda self.move_checker, która przesuwa monetę na ekranie
        final_x = 40+80*y
        end_y = 40+80*x
        curr_checker = self.print_checker(x=final_x, y=0, r=38, canvas=self._board, color=checker.name)
        self._checkers_map[x][y] = curr_checker
        self._checker_dropped.set(False)
        self.move_checker(curr_checker, 0, end_y)

        if win:
            self.disable_buttons()
            self.change_buttons_property("text", "🏆")
            self._window.wait_variable(self._checker_dropped)  # oczekiwanie aż zwycięska moneta się zatrzyma
            self.print_end_game_info(draw=False)
            if self._current_mode.get() == "PopOut":
                self.change_buttons_property("state", DISABLED, pop_out=True)
        if draw:
            self.disable_buttons()
            self.print_end_game_info(draw=True)
            self.change_buttons_property("bg", "black")
            self.change_buttons_property("text", "🤝")

        self.change_buttons_property("bg", self._logic.whose_turn.checker.name)
        self.change_buttons_property("activebackground", self._logic.whose_turn.checker.name)
        # ustawianie przycisków z 'X' na kolor danego gracza
        if self._current_mode.get() == "PopOut":
            curr_pop_out_image = self._pop_out_image_red if self._logic.whose_turn.checker == Checker.RED else self._pop_out_image_yellow
            self.change_buttons_property("image", curr_pop_out_image, pop_out=True)
        self.change_whose_turn_lbl()

    def remove_checker(self, col):
        """Usuń monetę z planszy.
        
        Metoda bazuje na klasie opisującej reguły gry. Wykorzystuje metody zawarte w tej klasie.
        Po kliknięciu jednego z przycisków odpowiedzialnych za usuwanie dolnej monety z danej kolumny, 
        sprawdzana jest możliwość wyjęcia monety. Jeżeli w kolumnie nie ma monet lub moneta, którą chcemy usunąć, 
        jest przeciwnika to pojawi się komunikat o błędzie (CheckerCannotBeRemovedException).
        W zmienej win przechowywana jest informacja czy ktoś wygrał.
        Jeżeli nie ma wygranej zmieniane są obrazy przycisków i kolor przycisków na kolor gracza, który będzie wykonywał ruch.

        Parametry:
            col (int): indeks kolumny, z której moneta ma zostać wyjęta.

        Zwraca:
            None
        """
        try:
            win = self._logic.remove_checker(col)
        except CheckerCannotBeRemovedException as e:
            self.show_alert("Nie można wyjąć monety", e)
            return

        # proces przesuwania monet w dół:
        # w self._checkers_map przechowuję id monet na planszy
        # najpierw usuwam monetę na dole z pomocą self._board.delete (Canvas, moneta zniknie z ekranu), następnie dla wyższych wierszy zastępuje akualne id w self._checkers_map wartościami id z wiersza o 1 wyżej
        # dla wiersza, który nie ma nad sobą żadnej monety ustawiana jest wartość None w self._checkers_map
        self._board.delete(self._checkers_map[self._logic._n_rows-1][col])
        self._checkers_map[self._logic._n_rows-1][col] = self._checkers_map[self._logic._n_rows-2][col]
        for x in range(self._logic._n_rows-2, -1, -1):
            # jeśli jest moneta w danym rzędzie i danej kolumnie to jest przesuwana o 1 w dół
            if self._checkers_map[x][col] is not None:
                x0, y0, x1, y1 = self._board.coords(self._checkers_map[x][col])
                self.move_checker(self._checkers_map[x][col], (y1-y0)//2, (y1-y0)//2 + 80)
                if x != 0:
                    self._checkers_map[x][col] = self._checkers_map[x-1][col]
                else:
                    self._checkers_map[x][col] = None
        
        if win:
            self.disable_buttons()
            self.print_end_game_info(False)
            self.change_buttons_property("text", "🏆")
            if self._current_mode.get() == "PopOut":
                self.change_buttons_property("state", DISABLED, pop_out=True)
        
        self.change_buttons_property("bg", self._logic.whose_turn.checker.name)
        self.change_whose_turn_lbl()
        
        curr_pop_out_image = self._pop_out_image_red if self._logic.whose_turn.checker == Checker.RED else self._pop_out_image_yellow
        self.change_buttons_property("image", curr_pop_out_image, pop_out=True)

    def print_end_game_info(self, draw: bool):
        """Wyświetl informację końcową.
        
        W zależności od tego czy gra zakończyła się remisem czy wygraną zostaje wyświetlony odpowiedni komunikat w nowym oknie.

        Parametry:
            draw (bool): zmienna informująca czy w grze doszło do remisu.

        Zwraca:
            None
        """

        alert = tk.Toplevel(self._window)
        alert.geometry("%dx250+%d+%d" % (self._window.winfo_width(), self._window.winfo_x(), self._window.winfo_y()))
        if draw:
            alert.title("Remis")
            lbl_header_text = tk.Label(alert, text= f"REMIS", font=('Roboto 34 bold'))
            btn_background = "white"
        else:
            alert.title("Mamy zwycięzcę")
            lbl_header_text = tk.Label(alert, text= f"Wygrał {self._logic.who_win().name}", font=('Roboto 34 bold')) 
            btn_background = self._logic.who_win().checker.name
        lbl_header_text.place(relx = 0.5, rely = 0.25, anchor="center")

        txt_info = "W celu rozegrania kolejnej partii naciśnij przycisk reset.\nJeżeli chcesz zagrać w innym trybie wybierz tryb z listy rozwijanej."
        lbl_info = tk.Label(alert, text=txt_info, font=('Roboto 12 bold'))
        lbl_info.place(relx = 0.5, rely = 0.5, anchor="center")
        btn_ok = tk.Button(alert,
                           text="ok",
                           font=('Roboto 12 bold'),
                           bg=btn_background,
                           activebackground=btn_background,
                           command=lambda: alert.destroy())
        if draw:
            btn_ok["bg"] = "black"
            btn_ok["activebackground"] = "black"
            btn_ok["fg"] = "white"
        btn_ok.place(relx = 0.5, rely = 0.75, width=70, height=50, anchor="center")

    def change_whose_turn_lbl(self):
        """Zmień informację kogo jest tura.
        
        Metoda zmienia tekst informujący kto teraz wykonuje ruch.

        Zwraca:
            None
        """

        self._lbl_whose_turn["text"] = "Tura gracza 1" if self._logic.whose_turn.checker == Checker.RED else "Tura gracza 2"

    def disable_buttons(self, button_numbers: list = None):
        """Wyłącz przyciski.
        
        Metoda wyłącza działanie przycisków odpowiedzialnych za umieszczanie monet na planszy. Stan przycisku zostaje ustawiony na DISABLED.
        Wyłączane zostają również zdarzenia wykrywane przy najechaniu i zjechaniu kursorem z przycisku.

        Parametry:
            button_numbers (list): podawane są dokładne numery przycisków (wartości int), dla których ma zajść zmiana. Przy podaniu None wykona się na wszystkich przyciskach w rzędzie.
        Zwraca:
            None
        """

        self.change_buttons_property("state", DISABLED, button_numbers)
        self.unbind_buttons_event("<Enter>", button_numbers)
        self.unbind_buttons_event("<Leave>", button_numbers)
        self.change_buttons_property("image", "", button_numbers)
        self.change_buttons_property("cursor", "", button_numbers)
        self.change_buttons_property("disabledforeground", "black", button_numbers)
        self.change_buttons_property("font", ('Roboto 18 bold'), button_numbers)

    def change_buttons_property(self, property, value, button_numbers: list = None, pop_out=False):
        """Zmień jedną cechę przycisków.
        
        Metoda zmienia jedną cechę (np. image, bg) dla wszystkich przycisków odpowiedzialnych za umieszczanie monet na planszy
        lub gdy pop_out=True to zmiana będzie wykonywana na przyciskach wyjmowania monet w trybie PopOut.
        W wypadku podania argumentu button_numbers robione jest to dla konkretnych przycisków a nie dla wszystkich.

        Parametry:
            property (str): nazwa parametru do modyfikacji.
            value (?): wartość jaka ma być przypisana do danego parametru. Typ wartości jest zależny od tego jaki parametr jest ustawiany.
            button_numbers (list): podawane są dokładne numery przycisków (wartości int), dla których ma zajść zmiana. Przy podaniu None wykona się na wszystkich przyciskach w rzędzie.
            pop_out (bool): czy dla przycisków wyjmowania monet
        Zwraca:
            None
        """

        if not pop_out:
            buttons_row_children = self._buttons_row.winfo_children()
        else:
            buttons_row_children = self._pop_out_buttons_row.winfo_children()

        if button_numbers is None:
            for i in range(len(buttons_row_children)):
                buttons_row_children[i][property] = value
        else:
            for i in button_numbers:
                buttons_row_children[i][property] = value

    def unbind_buttons_event(self, event_type, button_numbers: list = None):
        """Usuwanie obsługi zdarzenia przez przyciski.
        
        Metoda usuwająca obsługę zdarzenia dla wszystkich przycisków odpowiedzialnych za umieszczanie monet na planszy.
        W wypadku podania argumentu button_numbers usuwane jest zdarzenie dla konkretnych przycisków.

        Parametry:
            event_type (str): nazwa zdarzenia, które nie będzie już obsługiwane.
            button_numbers (list): podawane są dokładne numery przycisków (wartości int), dla których ma zajść zmiana. Przy podaniu None wykona się na wszystkich przyciskach w rzędzie.
        Zwraca:
            None
        """
        buttons_row_children = self._buttons_row.winfo_children()
        if button_numbers is None:
            for i in range(len(buttons_row_children)):
                buttons_row_children[i].bind(event_type, "")
        else:
            for i in button_numbers:
                buttons_row_children[i].bind(event_type, "")

    def show_alert(self, title, msg):
        """Wyświetl informację o niepoprawnej akcji użytkownika.
        
        Na ekranie zostaje wyświetlone okno, w którym zostaje wyświetlony dany komunikat.

        Parametry:
            title (str): tytuł komunikatu.
            msg (str): wiadomość do wyświetlenia dla użytkownika

        Zwraca:
            None
        """
        messagebox.showinfo(title, msg)

    def reset(self, option):
        """Resetuj grę.
        
        Resetuje grę w danym trybie lub uruchamia grę w innym.

        Parametry:
            option (str): tryb gry

        Zwraca:
            None
        """

        if option == "Standard":
            self.__initialize_game()
        elif option == "Pięć w rzędzie":
            self.__initialize_game(False, FiveInARow(Player("Gracz 1", Checker.RED), Player("Gracz 2", Checker.YELLOW)))
        elif option == "PopOut":
            self.__initialize_game(False, PopOut(6, 7, Player("Gracz 1", Checker.RED), Player("Gracz 2", Checker.YELLOW)))
        

    def mainloop(self):
        """Uruchom pętlę zdarzeń.
        
        Uruchamia pętlę zdarzeń dla tego okna. 

        Zwraca:
            None
        """
        tk.mainloop()