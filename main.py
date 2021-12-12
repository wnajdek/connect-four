import tkinter as tk
from PIL import Image, ImageTk

if __name__ == "__main__":
    okno = tk.Tk()
    okno.title("Cztery w rzędzie")
    # okno.columnconfigure(0,weight=1, uniform='col')
    # okno.columnconfigure(1,weight=1, uniform='col')
    # okno.columnconfigure(2,weight=1, uniform='col')
    # okno.geometry("600x600")
    kogo_tura = "Tura gracza 1"
    
    img = Image.open("moneta.png")
    x = int(img.size[0]*0.05)
    y = int(img.size[1]*0.05)

    img = ImageTk.PhotoImage(img.resize((x, y)))

    ramka_gora = tk.Frame()
    # ramka_gora.columnconfigure(0,weight=2, uniform='col')
    label_kogo_tura = tk.Label(text = kogo_tura, master=okno, foreground = "white", background = "black")
    label_kogo_tura.grid(row=0, columnspan=3)

    przycisk_reset = tk.Button(master=okno, bg="blue", text="RESET\nGRY", command=lambda: print("RESET"))
    przycisk_reset.grid(row=0, column=3, columnspan=2)
    
    domyslny_tryb = tk.StringVar(okno)
    domyslny_tryb.set("Tryb 1")

    lista_trybow = tk.OptionMenu(okno, domyslny_tryb, "Tryb 1", "Tryb 2", "Tryb 3")
    lista_trybow.grid(row=0, column=5, columnspan=2)

    # rzad_przyciskow = tk.Frame()
    # rzad_przyciskow.grid(row=1)
    for i in range(7):
        kratka = tk.Frame(okno, borderwidth=0.1)
        kratka.grid(row=1, column=i)
        
        przycisk = tk.Button(kratka, bg="red", text=str(i), command=lambda: print("przycisk wrzucania monety"), padx=10, pady=10)
        przycisk.pack(side=tk.LEFT)

    # ramka_plansza = tk.Frame(bg="black")
    # ramka_plansza.grid(row=2)
    
    # plansza 6 wierszy na 7 kolumn
    for i in range(6):
        for j in range(7):
            kratka = tk.Frame(okno, borderwidth=0.1)
            kratka.grid(row=i+2, column=j)
            
            moneta = tk.Label(kratka, image=img)
            moneta.pack()

    okno.mainloop()
    