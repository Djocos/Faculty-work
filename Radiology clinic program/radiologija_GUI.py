from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from podaci import *
from pacijenti_GUI import PacijentiProzor
from snimanja_GUI import SnimanjaProzor


class GlProzor(Tk):

    def otvori_prozor_sa_snimanjima(self):
        snimanja_prozor = SnimanjaProzor(self, self.__podaci)
        self.wait_window(snimanja_prozor)

    def komanda_pacijenti_prozor(self):
        pacijent_prozor = PacijentiProzor(self, self.__podaci)
        self.wait_window(pacijent_prozor)

    def komanda_izlaz(self):
        x = messagebox.askokcancel("Radiologija", "Da li ste sigurni da želite da napustite aplikaciju?", icon='warning')
        if x:
            self.destroy()

    def komanda_o_aplikaciji(self):
        x = messagebox.showinfo("Radiologija", "Ova aplikacija je kreirana radi olakšavanja svakodnevnog rada sa "
                                               "pacijentima, uvid u njihova snimanja i još mnogo toga \nIzvršitelj "
                                               "projekta: Miroslav Đoćoš BI55/2019")

    def prikazi_sliku(self, roditelj):  # otvara i prikazuje sliku
        load = Image.open("NMK_logotip.png")
        render = ImageTk.PhotoImage(load)
        img = Label(roditelj, image=render)
        img.image = render
        img.place(x=20, y=20)

    def __init__(self, podaci):
        super().__init__()
        self.__podaci = podaci

        # Slika u glavnom prozoru

        self.prikazi_sliku(self)

        # Glavni meni u aplikaciji

        meni_bar = Menu(self)
        datoteka_meni = Menu(meni_bar, tearoff=0)
        datoteka_meni.add_command(label="Izlaz", command=self.komanda_izlaz)
        meni_bar.add_cascade(label="Datoteka", menu=datoteka_meni)

        pacijent_meni = Menu(meni_bar, tearoff=0)
        pacijent_meni.add_command(label="Pacijenti", command=self.komanda_pacijenti_prozor)
        meni_bar.add_cascade(label="Pacijenti", menu=pacijent_meni)

        snimanja_meni = Menu(meni_bar, tearoff=0)
        snimanja_meni.add_command(label="Snimanja", command=self.otvori_prozor_sa_snimanjima)
        meni_bar.add_cascade(label="Snimanja", menu=snimanja_meni)

        pomoc_meni = Menu(meni_bar, tearoff=0)
        pomoc_meni.add_command(label="O aplikaciji", command=self.komanda_o_aplikaciji)
        meni_bar.add_cascade(label="Pomoć", menu=pomoc_meni)

        self.config(menu=meni_bar)
        self.protocol("WM_DELETE_WINDOW", self.komanda_izlaz)

        self.update_idletasks()  # ucitavanje prozora pre njegovig stvaranja

        # podesavanje prozora
        self.minsize(350, 350)
        self.title("Radiologija")
        self.iconbitmap("NMK_logotip.ico")


def main():
    podaci = Podaci.prikupi_podatke()
    glavni_prozor = GlProzor(podaci)
    glavni_prozor.mainloop()


main()
