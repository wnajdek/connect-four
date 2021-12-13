import tkinter as tk
from PIL import Image, ImageTk

if __name__ == "__main__":
    okno = tk.Tk()
    okno.title("Cztery w rzędzie")
    okno.resizable(0, 0)
    okno.geometry("700x700")

    kogo_tura = "Tura gracza 1"
    
    img = Image.open("moneta.png")
    # x = int(img.size[0]*0.05)
    # y = int(img.size[1]*0.05)
    x = 90
    y = 90
    img = ImageTk.PhotoImage(img.resize((x, y)))

    header = tk.Frame(okno, bg="blue", background="yellow")
    header.pack()

    # header.columnconfigure(0, weight=2)
    # header.columnconfigure(1, weight=1)
    # header.columnconfigure(2, weight=2)
    # header.rowconfigure(0, weight=1)

    pixel = tk.PhotoImage(width=1, height=1)
    label_kogo_tura = tk.Label(text = kogo_tura, master=header, image=pixel, foreground = "white", background = "black", width=200, height=100)
    label_kogo_tura.grid(row=0, column=0)

    przycisk_reset = tk.Button(master=header, bg="blue", image=pixel, text="RESET\nGRY", command=lambda: print("RESET"))
    przycisk_reset.grid(row=0, column=1)
    
    domyslny_tryb = tk.StringVar(header)
    domyslny_tryb.set("Tryb 1")

    lista_trybow = tk.OptionMenu(header, domyslny_tryb, "Tryb 1", "Tryb 2", "Tryb 3")
    lista_trybow.grid(row=0, column=2)

    rzad_przyciskow = tk.Frame(okno, borderwidth=1)
    rzad_przyciskow.pack()

    

    # plansza 6 wierszy na 7 kolumn
    plansza = tk.Frame(okno, borderwidth=1)
    plansza.pack()
    for i in range(6):
        for j in range(7):
            moneta = tk.Label(plansza, image=img)
            moneta.grid(row=i, column=j)
            


    # przyciski do planszy
    for i in range(7):
        przycisk = tk.Button(rzad_przyciskow, bg="red", text=str(i), command=lambda: print("przycisk wrzucania monety"))
        przycisk.grid(row=0, column=i)

    okno.mainloop()
    