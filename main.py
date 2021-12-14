import tkinter as tk
from tkinter.constants import ANCHOR
from PIL import Image, ImageTk

def rysuj_monete(x, y, r, canvas):
        return canvas.create_oval(x - r, y - r, x + r, y + r, fill="#f8f4f4", width=0)

if __name__ == "__main__":

    # tworzenie okna aplikacji
    okno = tk.Tk()
    okno.title("Cztery w rzędzie")
    #okno.resizable(0, 0)
    okno.geometry("600x700")

    kogo_tura = "Tura gracza 1"
    
    img = Image.open("moneta.png")
    x = 80
    y = 80
    img = ImageTk.PhotoImage(img.resize((x, y)))

    # ramka zawierająca: informację kto ma wykonać ruch, przycisk reset oraz lista rozwijaną do wyboru reguł gry
    header = tk.Frame(okno)
    header.place(x=0, y=0, height=120, width=600)

    label_kogo_tura = tk.Label(text = kogo_tura, master=header, foreground = "white", background = "black")
    label_kogo_tura.place(in_= header, x=225, rely=0.25, width=150, height=50)

    przycisk_reset = tk.Button(master=header, bg="blue", text="RESET\nGRY", command=lambda: print("RESET"))
    przycisk_reset.place(in_= header, x=30, rely=0.25, width=100, height=50)
    
    domyslny_tryb = tk.StringVar(header)
    domyslny_tryb.set("Tryb 1")
    lista_trybow = tk.OptionMenu(header, domyslny_tryb, "Tryb 1", "Tryb 2", "Tryb 3")
    lista_trybow.place(in_= header, x=570, rely=0.25, anchor="ne", width=100, height=50)

    
    # przyciski do planszy
    rzad_przyciskow = tk.Frame(okno)
    rzad_przyciskow.place(x=17, y=120, width=600, height=50)

    for i in range(7):
        przycisk = tk.Button(rzad_przyciskow, bg="red", text=str(i), command=lambda: print("przycisk wrzucania monety"))
        przycisk.place(in_= rzad_przyciskow, x=i*80+i, width=80, height=50)

    # plansza 6 wierszy na 7 kolumn
    plansza = tk.Canvas(okno, bg="blue", width=565, height=485)
    plansza.place(x=15, y=190)
    
    # okno.update()
    # print(plansza.winfo_width(), plansza.winfo_height(), rzad_przyciskow.winfo_width(), header.winfo_width())

    for i in range(6):
        for j in range(7):
            rysuj_monete(x=41+j*80+j, y=40+i*80+i, r=35, canvas=plansza)
    
    
    # plansza = tk.Frame(okno)
    # plansza.place(x=17, y=190, width=700, height=550)
    
    # for i in range(6):
    #     for j in range(7):
    #         # moneta = tk.Label(plansza, image=img)
    #         moneta = tk.Label(plansza, highlightthickness=2, highlightbackground="#37d3ff")
    #         moneta.place(in_= plansza, x=j*80+j, y=i*80+i, width=80, height=80)

    
    okno.mainloop()
    