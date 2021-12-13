import tkinter as tk
from tkinter.constants import ANCHOR
from PIL import Image, ImageTk

if __name__ == "__main__":
    okno = tk.Tk()
    okno.title("Cztery w rzędzie")
    okno.resizable(0, 0)
    okno.geometry("600x700")

    kogo_tura = "Tura gracza 1"
    
    img = Image.open("moneta.png")
    # x = int(img.size[0]*0.05)
    # y = int(img.size[1]*0.05)
    x = 80
    y = 80
    img = ImageTk.PhotoImage(img.resize((x, y)))

    header = tk.Frame(okno)
    header.place(x=0, y=0, height=120, width=700)

    pixel = tk.PhotoImage(width=1, height=1)
    label_kogo_tura = tk.Label(text = kogo_tura, master=header, foreground = "white", background = "black")
    label_kogo_tura.place(in_= header, x=225, rely=0.25, width=150, height=50)

    przycisk_reset = tk.Button(master=header, bg="blue", text="RESET\nGRY", command=lambda: print("RESET"))
    przycisk_reset.place(in_= header, x=30, rely=0.25, width=100, height=50)
    
    domyslny_tryb = tk.StringVar(header)
    domyslny_tryb.set("Tryb 1")

    lista_trybow = tk.OptionMenu(header, domyslny_tryb, "Tryb 1", "Tryb 2", "Tryb 3")
    lista_trybow.place(in_= header, x=570, rely=0.25, anchor="ne", width=100, height=50)

    rzad_przyciskow = tk.Frame(okno)
    rzad_przyciskow.place(x=17, y=120, width=700, height=50)

    # przyciski do planszy
    for i in range(7):
        przycisk = tk.Button(rzad_przyciskow, bg="red", text=str(i), command=lambda: print("przycisk wrzucania monety"))
        przycisk.place(in_= rzad_przyciskow, x=i*80+i, width=80, height=50)

    # plansza 6 wierszy na 7 kolumn
    plansza = tk.Frame(okno)
    plansza.place(x=17, y=190, width=700, height=550)
    for i in range(6):
        for j in range(7):
            # moneta = tk.Label(plansza, image=img)
            moneta = tk.Label(plansza, highlightthickness=2, highlightbackground="#37d3ff")
            moneta.place(in_= plansza, x=j*80+j, y=i*80+i, width=80, height=80)

    

    okno.mainloop()
    