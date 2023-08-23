from tkinter import *
from tkinter import messagebox
from podaci import *
from snimanja_GUI import SnimanjaProzor
import pydicom


class PacijentiProzor(Toplevel):
    def comanda_prikazi_snimanja(self):
        pacijent = self.__podaci.pacijenti[self.__pacijenti_listbox.curselection()[0]]
        snimanja_prozor = SnimanjaProzor(self, self.__podaci, pacijent.ime + " " + pacijent.prezime)
        self.wait_window(snimanja_prozor)

    def comanda_dodaj(self):
        dodavanje_prozor = DodavanjePacijentaProzor(self, self.__podaci)
        self.wait_window(dodavanje_prozor)

        if dodavanje_prozor.otkazan:
            return

        self.__podaci.sortiraj_pacijente()
        self.__podaci.sacuvaj(self.__podaci)
        self.popuni_listbox(self.__podaci.pacijenti)
        self.__pacijenti_listbox.selection_set(END)
        self.promena_selekcije_ulistboxu()

    def comanda_izmeni(self):
        x = self.__pacijenti_listbox.curselection()
        izmena_prozor = IzmenaPacijentaProzor(self, self.__podaci, self.__pacijenti_listbox.curselection()[0])
        self.wait_window(izmena_prozor)

        if izmena_prozor.otkazan:
            return

        self.__podaci.sortiraj_pacijente()
        self.__podaci.sacuvaj(self.__podaci)
        self.popuni_listbox(self.__podaci.pacijenti)
        self.__pacijenti_listbox.selection_set(x[0])
        self.promena_selekcije_ulistboxu()

    def comanda_obrisi(self):
        x = messagebox.askokcancel("Obrisati?", "Da li ste sigurni da želite da obrišete obeleženog pacijenta?\n"
                                                "Brisanjem pacijenta, obrisaćete i sva njegova snimanja.",
                                   icon="warning")
        if not x:
            return
        index = self.__pacijenti_listbox.curselection()[0]
        self.__podaci.obrisi_pacijenta(index)
        self.__podaci.sacuvaj(self.__podaci)
        self.popuni_listbox(self.__podaci.pacijenti)
        self.__pacijenti_listbox.selection_clear(0, END)
        self.promena_selekcije_ulistboxu()

    def popuni_labele(self, pacijent):
        self.__prezime_labela["text"] = pacijent.prezime
        self.__ime_labela["text"] = pacijent.ime
        self.__datum_rodjenja_labela["text"] = pacijent.datum_rodjenja.strftime('%d. %m. %Y.')
        self.__lbo_labela["text"] = pacijent.lbo

    def ocisti_labele(self):
        self.__prezime_labela["text"] = ""
        self.__ime_labela["text"] = ""
        self.__datum_rodjenja_labela["text"] = ""
        self.__lbo_labela["text"] = ""

    def popuni_listbox(self, *args):
        self.__pacijenti_listbox.delete(0, END)
        pretrazivanje = self.__pretraga.get()
        if pretrazivanje == '':
            for pacijent in self.__podaci.pacijenti:
                self.__pacijenti_listbox.insert(END, pacijent.ime + " " + pacijent.prezime)
        else:
            for pacijent in self.__podaci.pacijenti:
                if pretrazivanje.lower() in (pacijent.ime + " " + pacijent.prezime).lower():
                    self.__pacijenti_listbox.insert(END, pacijent.ime + " " + pacijent.prezime)

    def promena_selekcije_ulistboxu(self, event=None):
        if not self.__pacijenti_listbox.curselection():
            self.ocisti_labele()
            self.__snimanja_button.config(state=DISABLED)
            self.__izmeni_button.config(state=DISABLED)
            self.__obrisi_button.config(state=DISABLED)

            return
        index = self.__pacijenti_listbox.curselection()[0]
        pacijent = self.__podaci.pacijenti[index]
        self.popuni_labele(pacijent)
        self.__snimanja_button.config(state=ACTIVE)
        self.__izmeni_button.config(state=ACTIVE)
        self.__obrisi_button.config(state=ACTIVE)

    @property
    def listbox(self):
        return self.__pacijenti_listbox

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__podaci = podaci
        self.__pretraga = StringVar(master)
        self.__pretraga.set('')

        # ******************************************kreiranje GUI-a***************************************************

        # lista sa pacijentima

        self.__pacijenti_listbox = Listbox(self, activestyle="none")
        self.__pacijenti_listbox.grid(column=0, row=1)
        self.popuni_listbox()

        # Polje za pretragu

        pretraga_frame = Frame(self, borderwidth=2, relief=RIDGE)
        pretraga_frame.grid(row=0)
        Label(pretraga_frame, text="Pretraga:").grid(row=1)
        self.__pretraga_entry = Entry(pretraga_frame, textvariable=self.__pretraga).grid(row=1, column=1)
        self.__pretraga.trace('w', self.popuni_listbox)
        self.__pacijenti_listbox.bind("<<ListboxSelect>>", self.promena_selekcije_ulistboxu)

        # Podaci o pacijentu i button-i za opcije
        pacijent_frame = Frame(self, borderwidth=0, relief=RIDGE, padx=10, pady=10)
        pacijent_frame.grid(column=1, row=1)

        self.__prezime_labela = Label(pacijent_frame)
        self.__ime_labela = Label(pacijent_frame)
        self.__datum_rodjenja_labela = Label(pacijent_frame)
        self.__lbo_labela = Label(pacijent_frame)
        self.__snimanja_button = Button(pacijent_frame, width=16, text="Prikaži snimanja",
                                        command=self.comanda_prikazi_snimanja, state=DISABLED)

        red = 0
        Label(pacijent_frame, text="LBO:").grid(sticky=E, row=red)
        red += 1
        Label(pacijent_frame, text="Ime:").grid(sticky=E, row=red)
        red += 1
        Label(pacijent_frame, text="Prezime:").grid(sticky=E, row=red)
        red += 1
        Label(pacijent_frame, text="Datum rođenja:").grid(sticky=E, row=red)
        red += 1
        Label(pacijent_frame, text="Snimanja:").grid(sticky=E, row=red)

        # labele u koje kasnije upisujem vrednosti
        kolona = 1
        red = 0
        self.__lbo_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__ime_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__prezime_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__datum_rodjenja_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__snimanja_button.grid(sticky=W, row=red, column=kolona)
        red += 1
        Label(pacijent_frame).grid(sticky=W, row=red, column=kolona)
        red += 1
        Button(pacijent_frame, width=16, text="Dodaj pacijenta", command=self.comanda_dodaj).grid(sticky=W, row=red,
                                                                                                  column=kolona)
        red += 1
        self.__izmeni_button = Button(pacijent_frame, width=16, text="Izmeni podatke", command=self.comanda_izmeni,
                                      state=DISABLED)
        self.__izmeni_button.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__obrisi_button = Button(pacijent_frame, width=16, text="Obriši pacijenta", command=self.comanda_obrisi,
                                      state=DISABLED)
        self.__obrisi_button.grid(sticky=W, row=red, column=kolona)

        # podesavanje prozora
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.title("Pacijenti")
        self.iconbitmap("NMK_logotip.ico")
        self.transient(master)
        self.focus_force()
        self.grab_set()


class DodavanjePacijentaProzor(Toplevel):
    def lbo_validacija(self):
        try:
            x = int(self.__lbo.get())
        except ValueError:
            messagebox.showerror("Greška", "LBO mora da bude niz brojeva!", icon='warning')
            return None

        for pacijent in self.__podaci.pacijenti:
            if x == pacijent.lbo:
                messagebox.showerror("Greška", "LBO mora da bude jedinstven!", icon='warning')
                return None
            elif len(self.__lbo.get()) != 11:
                messagebox.showerror("Greška", "LBO mora da sadrži tačno 11 karaktera!", icon='warning')
                return None

        lbo = self.__lbo.get()
        return lbo

    def ime_validacija(self):
        ime = self.__ime.get()
        if len(ime) < 2:
            x = messagebox.showerror("Greška", "Ime mora da sadrži bar dva karaktera!", icon='warning')
            return None
        return ime.capitalize()

    def prezime_validacija(self):
        prezime = self.__prezime.get()
        if len(prezime) < 2:
            x = messagebox.showerror("Greška", "Prezime mora da sadrži bar dva karaktera", icon='warning')
            return None
        return prezime.capitalize()

    def datum_validacija(self):

        try:
            dan = self.__datum_dan.get()
            mesec = self.__datum_mesec.get()
            godina = self.__datum_godina.get()
        except TclError:
            messagebox.showerror("Greška", "Datum rođenja treba da se unese u obliku 1.1.2020, ne može se unositi text",
                                 icon='warning')
            return
        try:
            if datetime(godina, mesec, dan) > datetime.now():
                messagebox.showerror("Greška", "Datum rođenja može biti najkasnije današnji datum", icon='warning')
                return None
        except ValueError:
            messagebox.showerror("Greška", "Datum rođenja mora biti validan, postojeći datum", icon='warning')
            return None
        return datetime(godina, mesec, dan)

    def dodaj(self):
        lbo = self.lbo_validacija()
        if not lbo:
            return
        ime = self.ime_validacija()
        if not ime:
            return
        prezime = self.prezime_validacija()
        if not prezime:
            return
        datum = self.datum_validacija()
        if not datum:
            return
        novi_pacijent = Pacijent(lbo, ime, prezime, datum)

        self.__podaci.dodaj_pacijenta(novi_pacijent)
        self.sacuvaj_dodavanje()
        self.otkazan = False
        self.destroy()

    def sacuvaj_dodavanje(self):
        self.__podaci.sacuvaj(self.__podaci)

    def odustani(self):
        x = messagebox.askokcancel("Dodavanje pacijenta", "Da li ste sigurni da želite da odustanete od dodavanja,"
                                                          " svi podaci koje ste uneli biće izgubljeni", icon='warning')
        if x:
            self.destroy()

    @property
    def otkazan(self):
        return self.__otkazan

    @otkazan.setter
    def otkazan(self, otkazan):
        self.__otkazan = otkazan

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__podaci = podaci
        self.__otkazan = True

        self.__lbo = StringVar(master)
        self.__ime = StringVar(master)
        self.__prezime = StringVar(master)
        self.__datum_dan = IntVar(master)
        self.__datum_mesec = IntVar(master)
        self.__datum_godina = IntVar(master)

        # Kreiranje GUI-a
        red = 0
        Label(self, text="LBO:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Ime:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Prezime:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Datum rođenja:").grid(sticky=E, row=red)
        red += 1
        kolona = 1
        red = 0
        self.__lbo_entry = Entry(self, textvariable=self.__lbo)
        self.__lbo_entry.grid(sticky=E, row=red, column=kolona)
        red += 1
        self.__ime_entry = Entry(self, textvariable=self.__ime)
        self.__ime_entry.grid(sticky=E, row=red, column=kolona)
        red += 1
        self.__prezime_entry = Entry(self, textvariable=self.__prezime)
        self.__prezime_entry.grid(sticky=E, row=red, column=kolona)
        red += 1
        self.__datum_dan_spinbox = Spinbox(self, from_=1, to=31, textvariable=self.__datum_dan)
        self.__datum_dan_spinbox.grid(sticky=E, row=red, column=kolona)
        self.__datum_mesec_spinbox = Spinbox(self, from_=1, to=12, textvariable=self.__datum_mesec)
        self.__datum_mesec_spinbox.grid(sticky=E, row=red, column=kolona+1)
        self.__datum_godina_spinbox = Spinbox(self, from_=1900, to=datetime.today().year,
                                              textvariable=self.__datum_godina)
        self.__datum_godina_spinbox.grid(sticky=E, row=red, column=kolona+2)
        red += 1
        Label(self).grid(sticky=W, row=red, column=kolona)
        red += 1
        Button(self, width=16, text="Dodaj pacijenta", command=self.dodaj).grid(sticky=W, row=red, column=kolona)
        Button(self, width=16, text="Odustani", command=self.odustani).grid(sticky=E, row=red, column=kolona+1)

        self.protocol("WM_DELETE_WINDOW", self.odustani)
        # podesavanje prozora
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.title("Dodavanje pacijenta")
        self.iconbitmap("NMK_logotip.ico")
        self.transient(master)
        self.focus_force()
        self.grab_set()


class IzmenaPacijentaProzor(Toplevel):
    def ime_validacija(self):
        ime = self.__ime.get()
        if len(ime) < 2:
            x = messagebox.showerror("Greška", "Ime mora da sadrži bar dva karaktera", icon='warning')
            return None
        return ime.capitalize()

    def prezime_validacija(self):
        prezime = self.__prezime.get()
        if len(prezime) < 2:
            x = messagebox.showerror("Greška", "Prezime mora da sadrži bar dva karaktera", icon='warning')
            return None
        return prezime.capitalize()

    def datum_validacija(self):
        try:
            dan = self.__datum_dan.get()
            mesec = self.__datum_mesec.get()
            godina = self.__datum_godina.get()
        except TclError:
            messagebox.showerror("Greška", "Datum rođenja treba da se unese u obliku 1.1.2020, ne može se unositi text",
                                 icon='warning')
            return
        try:
            if datetime(godina, mesec, dan) > datetime.now():
                x = messagebox.showerror("Greška", "Datum rođenja može biti najkasnije današnji datum", icon='warning')
                return None
        except ValueError:
            x = messagebox.showerror("Greška", "Datum rođenja mora biti validan, postojeći datum", icon='warning')
            return None
        return datetime(godina, mesec, dan)

    def izmeni(self):

        lbo = self.__lbo.get()
        ime = self.ime_validacija()
        prezime = self.prezime_validacija()
        datum = self.datum_validacija()
        izmenjen_pacijent = Pacijent(lbo, ime, prezime, datum)

        self.__podaci.pacijenti[self.__index] = izmenjen_pacijent
        self.__podaci.izmena_pacijenta_u_snimanjima(izmenjen_pacijent)
        self.sacuvaj_izmene()
        self.__otkazan = False
        self.destroy()

    def sacuvaj_izmene(self):
        self.__podaci.sacuvaj(self.__podaci)

    def odustani(self):
        x = messagebox.askokcancel("Izmena pacijenta", "Da li ste sigurni da želite da odustanete od izmene, svi podaci"
                                                       " koje ste uneli biće izgubljeni", icon='warning')
        if x:
            self.destroy()

    @property
    def otkazan(self):
        return self.__otkazan

    def __init__(self, master, podaci, index):
        super().__init__(master)
        self.__podaci = podaci
        self.__index = index
        self.__pacijent = self.__podaci.pacijenti[index]

        self.__otkazan = True
        self.__lbo = StringVar(master)
        self.__lbo.set(self.__podaci.pacijenti[self.__index].lbo)
        self.__ime = StringVar(master)
        self.__ime.set(self.__podaci.pacijenti[self.__index].ime)
        self.__prezime = StringVar(master)
        self.__prezime.set(self.__podaci.pacijenti[self.__index].prezime)
        self.__datum_dan = IntVar(master)
        self.__datum_dan.set(self.__podaci.pacijenti[self.__index].datum_rodjenja.day)
        self.__datum_mesec = IntVar(master)
        self.__datum_mesec.set(self.__podaci.pacijenti[self.__index].datum_rodjenja.month)
        self.__datum_godina = IntVar(master)
        self.__datum_godina.set(self.__podaci.pacijenti[self.__index].datum_rodjenja.year)

        # *******************************************KREIRANJE GUI-a***************************************************

        red = 0
        Label(self, text="LBO:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Ime:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Prezime:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Datum rođenja:").grid(sticky=E, row=red)
        kolona = 1
        red = 0
        self.__lbo_entry = Entry(self, state=DISABLED, textvariable=self.__lbo)
        self.__lbo_entry.grid(sticky=E, row=red, column=kolona)
        red += 1
        self.__ime_entry = Entry(self, textvariable=self.__ime)
        self.__ime_entry.grid(sticky=E, row=red, column=kolona)
        red += 1
        self.__prezime_entry = Entry(self, textvariable=self.__prezime)
        self.__prezime_entry.grid(sticky=E, row=red, column=kolona)
        red += 1
        self.__datum_dan_spinbox = Spinbox(self, from_=1, to=31, textvariable=self.__datum_dan)
        self.__datum_dan_spinbox.grid(sticky=E, row=red, column=kolona)
        self.__datum_mesec_spinbox = Spinbox(self, from_=1, to=12, textvariable=self.__datum_mesec)
        self.__datum_mesec_spinbox.grid(sticky=E, row=red, column=kolona+1)
        self.__datum_godina_spinbox = Spinbox(self, from_=1900, to=datetime.today().year,
                                              textvariable=self.__datum_godina)
        self.__datum_godina_spinbox.grid(sticky=E, row=red, column=kolona+2)
        red += 1
        Label(self).grid(sticky=W, row=red, column=kolona)
        red += 1
        Button(self, width=16, text="Izmeni podatke", command=self.izmeni).grid(sticky=W, row=red, column=kolona)
        Button(self, width=16, text="Odustani", command=self.odustani).grid(sticky=E, row=red, column=kolona+1)

        self.protocol("WM_DELETE_WINDOW", self.odustani)
        # podesavanje prozora
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.title("Izmena podataka o pacijentu")
        self.iconbitmap("NMK_logotip.ico")
        self.transient(master)
        self.focus_force()
        self.grab_set()
