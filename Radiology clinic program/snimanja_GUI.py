from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from podaci import *
from PIL import Image, ImageTk
import pydicom_PIL


class SnimanjaProzor(Toplevel):  # prozor gde se prikazuju sva snimanja

    def comanda_dodaj(self):
        dodavanje_prozor = DodavanjeSnimanjaProzor(self, self.__podaci)
        self.wait_window(dodavanje_prozor)

        if dodavanje_prozor.otkazan:
            return

        self.__podaci.sortiraj_snimanja()
        self.__podaci.sacuvaj(self.__podaci)
        self.popuni_listbox(self.__podaci.snimanja)
        self.__snimanja_listbox.selection_set(END)
        self.promena_selekcije_ulistboxu()

    def comanda_izmeni(self):
        index = self.__snimanja_listbox.curselection()[0]
        izmene_prozor = IzmenaSnimanjaProzor(self, self.__podaci, index)
        self.wait_window(izmene_prozor)

        if izmene_prozor.otkazan:
            return

        self.__podaci.sortiraj_snimanja()
        self.__podaci.sacuvaj(self.__podaci)
        self.popuni_listbox(self.__podaci.snimanja)
        self.__snimanja_listbox.selection_set(index)
        self.promena_selekcije_ulistboxu()

    def comanda_obrisi(self):
        x = messagebox.askokcancel("Obrisati?", "Da li ste sigurni da želite da obrišete obeleženo snimanje?\n"
                                                "Brisanjem snimanja, obrisaćete sve podatke vezane za to snimanje!",
                                   icon="warning")
        if not x:
            return
        index = self.__snimanja_listbox.curselection()[0]
        self.__podaci.obrisi_snimanje(index)
        self.__podaci.sacuvaj(self.__podaci)
        self.popuni_listbox(self.__podaci.snimanja)
        self.__snimanja_listbox.selection_clear(0, END)
        self.promena_selekcije_ulistboxu()

    def popuni_labele(self, snimanje):
        self.__pacijent_labela["text"] = snimanje.pacijent.ime + " " + snimanje.pacijent.prezime
        self.__datum_labela["text"] = snimanje.datum_i_vreme.strftime('%d.%m.%Y | %H:%M')
        self.__tip_labela["text"] = snimanje.tip
        self.__lekar_labela["text"] = snimanje.lekar
        self.__putanja.set(snimanje.snimak)

    def ocisti_labele(self):
        self.__pacijent_labela["text"] = ""
        self.__datum_labela["text"] = ""
        self.__tip_labela["text"] = ""
        self.__lekar_labela["text"] = ""

    def popuni_listbox(self,  *args):
        self.__snimanja_listbox.delete(0, END)
        for snimanje in self.lista_snimanja_sa_filterima():
            self.__snimanja_listbox.insert(END, snimanje.datum_i_vreme.strftime('%d.%m.%Y | %H:%M'))

    def promena_selekcije_ulistboxu(self, event=None):
        if not self.__snimanja_listbox.curselection():
            self.ocisti_labele()
            return
        index = self.__snimanja_listbox.curselection()[0]
        snimanje = self.lista_snimanja_sa_filterima()[index]
        self.popuni_labele(snimanje)
        self.__izmeni_button.config(state=ACTIVE)
        self.__obrisi_button.config(state=ACTIVE)
        if self.__putanja.get() != "None":
            self.__otvori_button.config(state=ACTIVE)
        else:
            self.__otvori_button.config(state=DISABLED)

    def napravi_listu_pacijenata(self):
        pacijenti_za_combo = []
        pacijenti = self.__podaci.pacijenti
        for pacijent in pacijenti:
            pacijenti_za_combo.append(pacijent.ime + " " + pacijent.prezime)
        pacijenti_za_combo.append("Svi pacijenti")
        return pacijenti_za_combo

    def vrati_tip(self, snimanje_tip):
        if snimanje_tip == "Magnetic Resonance (MR)":
            return "MR"
        elif snimanje_tip == "Computerised Thomography (CT)":
            return "CT"
        elif snimanje_tip == "X-Ray (RX)":
            return "RX"
        elif snimanje_tip == "Ultra Sound (US)":
            return "US"

    def otvori_snimak(self):  # dataset namerno nije cuvan jer pojedini dicom-i ne dozvoljavaju trajnu izmenu podataka,
        # pa da bi se izbegao error
        snimanje = self.lista_snimanja_sa_filterima()[self.__snimanja_listbox.curselection()[0]]
        dataset = self.__podaci.preuzmi_dataset(self.__putanja.get())
        dataset.PatientName = snimanje.pacijent.ime + ' ' + snimanje.pacijent.prezime
        dataset.PatientID = snimanje.pacijent.lbo
        dataset.PatientBirthDate = snimanje.pacijent.datum_rodjenja.strftime('%d.%m.%Y')
        dataset.StudyDate = snimanje.datum_i_vreme.strftime('%d.%m.%Y')
        dataset.Modality = self.vrati_tip(snimanje.tip)
        dataset.ReferringPhysicianName = snimanje.lekar

        snimak_prozor = SnimakProzor(self, self.__podaci, self.__putanja.get(), dataset)
        print(dataset)
        self.wait_window(snimak_prozor)

    def lista_snimanja_sa_filterima(self):
        snimanja_za_prikaz = []
        konacna_snimanja_za_prikaz = []
        if self.__trazeni_pacijent.get() == "Svi pacijenti":
            for snimanje in self.__podaci.snimanja:
                snimanja_za_prikaz.append(snimanje)
        else:
            for snimanje in self.__podaci.snimanja:
                if snimanje.pacijent.ime + " " + snimanje.pacijent.prezime == self.__trazeni_pacijent.get():
                    snimanja_za_prikaz.append(snimanje)

        if self.__trazeni_tip.get() == "Svi tipovi":
            konacna_snimanja_za_prikaz = snimanja_za_prikaz
        else:
            for snimanje in snimanja_za_prikaz:
                if snimanje.tip == self.__trazeni_tip.get():
                    konacna_snimanja_za_prikaz.append(snimanje)
        return konacna_snimanja_za_prikaz

    def lista_u_slucaju_odr_pac(self):
        snimanja = []
        if self.__pacijent == "Svi pacijenti":
            return self.__podaci.snimanja
        for snimanje in self.__podaci.snimanja:
            if snimanje.pacijent.ime + " " + snimanje.pacijent.prezime == self.__pacijent:
                snimanja.append(snimanje)
        return snimanja

    @property
    def putanja(self):
        return self.__putanja.get()

    def __init__(self, master, podaci, pacijent="Svi pacijenti"):
        super().__init__(master)
        self.__podaci = podaci
        self.__pacijent = pacijent
        self.__putanja = StringVar(master)
        self.__trazeni_pacijent = StringVar(master)
        self.__trazeni_tip = StringVar(master)

        # kreiranje GUI-a
        # ***************************************************************************************************
        # comboboxovi za pretragu snimanja
        combobox_frame = Frame(self, borderwidth=0, relief=RIDGE)
        combobox_frame.grid(row=0, column=0)

        Label(combobox_frame, text="Pacijent:").pack(side=LEFT)
        self.pacijent_combo = ttk.Combobox(combobox_frame, textvariable=self.__trazeni_pacijent)
        self.pacijent_combo.pack(side=LEFT)
        self.pacijent_combo.config(values=self.napravi_listu_pacijenata())
        self.pacijent_combo.set(self.__pacijent)
        self.pacijent_combo.bind("<<ComboboxSelected>>", self.popuni_listbox)

        Label(combobox_frame, text="Tip snimanja:").pack(side=LEFT)
        self.tip_snimanja_combo = ttk.Combobox(combobox_frame, textvariable=self.__trazeni_tip)
        self.tip_snimanja_combo.pack(side=LEFT)
        lista_tipova = ["Magnetic Resonance (MR)", "Computerised Thomography (CT)", "X-Ray (RX)", "Ultra Sound (US)",
                        "Svi tipovi"]
        self.tip_snimanja_combo.config(values=lista_tipova)
        self.tip_snimanja_combo.set(lista_tipova[-1])
        self.tip_snimanja_combo.bind("<<ComboboxSelected>>", self.popuni_listbox)

        # ostale stvari u prozoru
        self.__okupljac = Frame(self, relief=RIDGE)
        self.__okupljac.grid(row=1, column=0)

        # listbox sa svim snimanjima
        self.__snimanja_listbox = Listbox(self.__okupljac, activestyle="none")
        self.__snimanja_listbox.pack(side=LEFT)
        for snimanje in self.lista_u_slucaju_odr_pac():
            self.__snimanja_listbox.insert(END, snimanje.datum_i_vreme.strftime('%d.%m.%Y | %H:%M'))
        self.__snimanja_listbox.bind("<<ListboxSelect>>", self.promena_selekcije_ulistboxu)

        # frame sa podacima o samom snimanju
        snimanja_frame = Frame(self.__okupljac, borderwidth=2, relief=RIDGE, padx=10, pady=10)
        snimanja_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.__pacijent_labela = Label(snimanja_frame)
        self.__datum_labela = Label(snimanja_frame)
        self.__tip_labela = Label(snimanja_frame)
        self.__lekar_labela = Label(snimanja_frame)

        red = 0
        Label(snimanja_frame, text="Pacijent:").grid(sticky=E, row=red)
        red += 1
        Label(snimanja_frame, text="Datum:").grid(sticky=E, row=red)
        red += 1
        Label(snimanja_frame, text="Tip snimanja:").grid(sticky=E, row=red)
        red += 1
        Label(snimanja_frame, text="Lekar:").grid(sticky=E, row=red)
        # labele u koje kasnije upisujem vrednosti
        kolona = 1
        red = 0
        self.__pacijent_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__datum_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__tip_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__lekar_labela.grid(sticky=W, row=red, column=kolona)
        red += 1

        # frame gde se nalazi entry sa putanjom i button gde se otvara snimak

        self.__snimak_frame = Frame(snimanja_frame)
        self.__snimak_frame.grid(sticky=E, row=red, column=kolona)
        self.__putanja_entry = Entry(self.__snimak_frame, state=DISABLED, textvariable=self.__putanja)

        self.__putanja_entry.grid(sticky=W, row=red, column=0)

        self.__otvori_button = Button(self.__snimak_frame, width=7, text="Otvori", command=self.otvori_snimak,
                                      state=DISABLED)
        self.__otvori_button.grid(sticky=W, row=red, column=2)
        red += 1
        Label(snimanja_frame).grid(sticky=W, row=red, column=kolona)
        red += 1
        Button(snimanja_frame, width=16, text="Dodaj snimanje", command=self.comanda_dodaj).grid(sticky=W, row=red,
                                                                                                 column=kolona)
        red += 1
        self.__izmeni_button = Button(snimanja_frame, width=16, text="Izmeni podatke", command=self.comanda_izmeni,
                                      state=DISABLED)
        self.__izmeni_button.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__obrisi_button = Button(snimanja_frame, width=16, text="Obriši snimanje", command=self.comanda_obrisi,
                                      state=DISABLED)
        self.__obrisi_button.grid(sticky=W, row=red, column=kolona)

        # podesavanje prozora
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.title("Snimanja")
        self.iconbitmap("NMK_logotip.ico")
        self.transient(master)
        self.focus_force()
        self.grab_set()


class DodavanjeSnimanjaProzor(Toplevel):
    def pacijent_validacija(self):
        prosledjen_pacijent = self.__pacijent.get()
        pacijent = self.__podaci.pronadji_pacijenta_po_imenu(prosledjen_pacijent)
        if not pacijent:
            return None
        return pacijent

    def lekar_validacija(self):
        lekar = self.__lekar.get()
        if len(lekar) < 2:
            messagebox.showerror("Greška", "Ime lekara mora da sadrži bar dva karaktera!", icon='warning')
            return None
        return "Dr" + " " + lekar.title()

    def tip_validacija(self):
        lista_tipova = ["Magnetic Resonance (MR)", "Computerised Thomography (CT)", "X-Ray (RX)", "Ultra Sound (US)"]
        tip = self.__tip.get()
        if tip not in lista_tipova:
            messagebox.showerror("Greška", "Tip snimanja koji ste uneli ne postoji, odaberite jedan od pondjenih",
                                 icon='warning')
            return None
        return tip

    def datum_validacija(self):
        try:
            dan = self.__datum_dan.get()
            mesec = self.__datum_mesec.get()
            godina = self.__datum_godina.get()
            sati = self.__sati.get()
            minuti = self.__minuti.get()
        except TclError:
            messagebox.showerror("Greška", "Datum rođenja treba da se unese u obliku 1.1.2020, ne može se unositi text",
                                 icon='warning')
            return None

        if datetime(godina, mesec, dan, sati, minuti) > datetime.now():
            x = messagebox.showerror("Greška", "Datum snimanja može biti najkasnije današnji datum", icon='warning')
            return None
        elif datetime(godina, mesec, dan, sati, minuti) < self.pacijent_validacija().datum_rodjenja:
            x = messagebox.showerror("Greška", "Datum snimanja može biti najkasnije današnji datum", icon='warning')
            return None

        return datetime(godina, mesec, dan, sati, minuti)

    def snimak_validacija(self):
        snimak = self.__snimak_putanja.get()
        return snimak

    def dodaj(self):
        pacijent = self.pacijent_validacija()
        if not pacijent:
            return
        lekar = self.lekar_validacija()
        if not lekar:
            return
        tip = self.tip_validacija()
        if not tip:
            return
        datum = self.datum_validacija()
        if not datum:
            return
        snimak = self.snimak_validacija()
        novo_snimanje = Snimanje(pacijent, datum, tip, lekar, snimak=snimak)
        self.__podaci.dodaj_snimanje(novo_snimanje)
        pacijent.snimanja.append(novo_snimanje)
        self.sacuvaj_dodavanje()
        self.otkazan = False
        self.destroy()

    def napravi_listu_pacijenata(self):
        pacijenti_za_combo = []
        pacijenti = self.__podaci.pacijenti
        for pacijent in pacijenti:
            pacijenti_za_combo.append(pacijent.ime + " " + pacijent.prezime)
        return pacijenti_za_combo

    def sacuvaj_dodavanje(self):
        self.__podaci.sacuvaj(self.__podaci)

    def odustani(self):
        x = messagebox.askokcancel("Dodavanje snimanja", "Da li ste sigurni da želite da odustanete od dodavanja,"
                                                         " svi podaci koje ste uneli biće izgubljeni", icon='warning')
        if x:
            self.destroy()

    def otvori_dicom(self):
        putanja = self.__podaci.otvori_dicom()
        self.__snimak_putanja.set(putanja)

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
        self.__putanja = StringVar(master)

        self.__pacijent = StringVar(master)
        self.__datum_dan = IntVar(master)
        self.__datum_mesec = IntVar(master)
        self.__datum_godina = IntVar(master)
        self.__sati = IntVar(master)
        self.__minuti = IntVar(master)
        self.__lekar = StringVar(master)
        self.__snimak_putanja = StringVar(master)
        self.__tip = StringVar(master)
        self.__datum_godina.set(2019)

        # Kreiranje GUI-a
        red = 0
        Label(self, text="Pacijent:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Datum snimanja:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Sati i minuti:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Tip snimanja:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Ime i prezime lekara:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Snimak:").grid(sticky=E, row=red)
        kolona = 1
        red = 0
        self.__pacijent_combobox = ttk.Combobox(self, textvariable=self.__pacijent)
        self.__pacijent_combobox.grid(sticky=E, row=red, column=kolona)
        self.__pacijent_combobox.config(values=self.napravi_listu_pacijenata())
        self.__pacijent_combobox.set(self.napravi_listu_pacijenata()[0])
        red += 1
        self.__datum_dan_spinbox = Spinbox(self, from_=1, to=31, textvariable=self.__datum_dan)
        self.__datum_dan_spinbox.grid(sticky=E, row=red, column=kolona)
        self.__datum_mesec_spinbox = Spinbox(self, from_=1, to=12, textvariable=self.__datum_mesec)
        self.__datum_mesec_spinbox.grid(sticky=E, row=red, column=kolona+1)
        self.__datum_godina_spinbox = Spinbox(self, from_=1900, to=datetime.today().year,
                                              textvariable=self.__datum_godina)
        self.__datum_godina_spinbox.grid(sticky=E, row=red, column=kolona+2)
        red += 1
        self.__datum_sat_spinbox = Spinbox(self, from_=0, to=23, textvariable=self.__sati)
        self.__datum_sat_spinbox.grid(sticky=E, row=red, column=kolona)

        self.__datum_minut_spinbox = Spinbox(self, from_=0, to=59, textvariable=self.__minuti)
        self.__datum_minut_spinbox.grid(sticky=E, row=red, column=kolona+1)
        red += 1
        __lista_tipova = ["Magnetic Resonance (MR)", "Computerised Thomography (CT)", "X-Ray (RX)", "Ultra Sound (US)"]
        self.__tip_combobox = ttk.Combobox(self, textvariable=self.__tip)
        self.__tip_combobox.grid(sticky=E, row=red, column=kolona)
        self.__tip_combobox.config(values=__lista_tipova)
        self.__tip_combobox.set(__lista_tipova[0])
        red += 1
        self.__lekar_entry = Entry(self, textvariable=self.__lekar)
        self.__lekar_entry.grid(sticky=E, row=red, column=kolona)
        red += 1

        self.__snimak_frame = Frame(self)
        self.__snimak_frame.grid(sticky=E, row=red, column=kolona)
        self.__putanja_entry = Entry(self.__snimak_frame, state=DISABLED, textvariable=self.__snimak_putanja)
        self.__putanja_entry.grid(sticky=W, row=red, column=0)
        Button(self.__snimak_frame, width=4, text="...", command=self.otvori_dicom).grid(sticky=W, row=red, column=1)
        red += 1
        Label(self).grid(sticky=W, row=red, column=kolona)
        red += 1
        Button(self, width=16, text="Dodaj snimanmje", command=self.dodaj).grid(sticky=W, row=red, column=kolona)
        Button(self, width=16, text="Odustani", command=self.odustani).grid(sticky=E, row=red, column=kolona+1)

        self.protocol("WM_DELETE_WINDOW", self.odustani)
        # podesavanje prozora
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.title("Dodavanje snimanja")
        self.iconbitmap("NMK_logotip.ico")
        self.transient(master)
        self.focus_force()
        self.grab_set()


class IzmenaSnimanjaProzor(Toplevel):

    def pacijent_validacija(self):
        pacijent = self.__pacijent.get()
        return pacijent

    def lekar_validacija(self):
        lekar = self.__lekar.get()
        if len(lekar) < 2:
            messagebox.showerror("Greška", "Ime lekara mora da sadrži bar dva karaktera!", icon='warning')
            return None
        return lekar.title()

    def tip_validacija(self):
        lista_tipova = ["Magnetic Resonance (MR)", "Computerised Thomography (CT)", "X-Ray (RX)", "Ultra Sound (US)"]
        tip = self.__tip.get()
        if tip not in lista_tipova:
            messagebox.showerror("Greška", "Tip snimanja koji ste uneli ne postoji, odaberite jedan od pondjenih",
                                 icon='warning')
            return None
        return tip

    def datum_validacija(self):
        try:
            dan = self.__datum_dan.get()
            mesec = self.__datum_mesec.get()
            godina = self.__datum_godina.get()
            sati = self.__sati.get()
            minuti = self.__minuti.get()
        except TclError:
            messagebox.showerror("Greška", "Datum rođenja treba da se unese u obliku 1.1.2020, ne može se unositi text",
                                 icon='warning')
            return None

        if datetime(godina, mesec, dan, sati, minuti) > datetime.now():
            messagebox.showerror("Greška", "Datum snimanja može biti najkasnije današnji datum", icon='warning')
            return None
        elif datetime(godina, mesec, dan, sati, minuti) < self.__podaci.pronadji_pacijenta_po_imenu(
                self.pacijent_validacija()).datum_rodjenja:
            messagebox.showerror("Greška", "Datum snimanja može biti najkasnije današnji datum", icon='warning')
            return None

        return datetime(godina, mesec, dan, sati, minuti)

    def snimak_validacija(self):
        snimak = self.__snimak_putanja.get()
        return snimak

    def izmeni(self):
        pacijent = self.__snimanje.pacijent
        if not pacijent:
            return

        lekar = self.lekar_validacija()
        if not lekar:
            return
        tip = self.tip_validacija()
        if not tip:
            return
        datum = self.datum_validacija()
        if not datum:
            return
        snimak = self.snimak_validacija()
        izmenjeno_snimanje = Snimanje(pacijent, datum, tip, lekar, snimak=snimak)

        pacijent.snimanja[self.__index_snimanja_pacijenta] = izmenjeno_snimanje
        self.__podaci.snimanja[self.__index] = izmenjeno_snimanje

        self.sacuvaj_dodavanje()
        self.otkazan = False
        self.destroy()

    def napravi_listu_pacijenata(self):
        pacijenti_za_combo = []
        pacijenti = self.__podaci.pacijenti
        for pacijent in pacijenti:
            pacijenti_za_combo.append(pacijent.ime + " " + pacijent.prezime)
        return pacijenti_za_combo

    def sacuvaj_dodavanje(self):
        self.__podaci.sacuvaj(self.__podaci)

    def odustani(self):
        x = messagebox.askokcancel("Dodavanje pacijenta", "Da li ste sigurni da želite da odustanete od dodavanja,"
                                                          " svi podaci koje ste uneli biće izgubljeni", icon='warning')
        if x:
            self.destroy()

    def otvori_dicom(self):
        putanja = self.__podaci.otvori_dicom()
        self.__snimak_putanja.set(putanja)

    @property
    def otkazan(self):
        return self.__otkazan

    @otkazan.setter
    def otkazan(self, otkazan):
        self.__otkazan = otkazan

    def __init__(self, master, podaci, index):
        super().__init__(master)
        self.__podaci = podaci
        self.__otkazan = True
        self.__putanja = StringVar(master)
        self.__index = index
        self.__snimanje = self.__podaci.snimanja[self.__index]
        self.__pacijent = self.__snimanje.pacijent
        self.__index_snimanja_pacijenta = self.__podaci.pronadji_snimanje_pacijenta(self.__pacijent,
                                                                                    self.__snimanje.datum_i_vreme)

        self.__pacijent = StringVar(master)
        self.__datum_dan = IntVar(master)
        self.__datum_mesec = IntVar(master)
        self.__datum_godina = IntVar(master)
        self.__sati = IntVar(master)
        self.__minuti = IntVar(master)
        self.__lekar = StringVar(master)
        self.__snimak_putanja = StringVar(master)
        self.__tip = StringVar(master)
        self.__datum_godina.set(2019)

        # Kreiranje GUI-a
        red = 0
        Label(self, text="Pacijent:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Datum snimanja:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Sati i minuti:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Tip snimanja:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Ime i prezime lekara:").grid(sticky=E, row=red)
        red += 1
        Label(self, text="Snimak:").grid(sticky=E, row=red)
        kolona = 1
        red = 0
        self.__pacijent_combobox = ttk.Combobox(self, state=DISABLED, textvariable=self.__pacijent)
        self.__pacijent_combobox.grid(sticky=E, row=red, column=kolona)
        self.__pacijent_combobox.config(values=self.napravi_listu_pacijenata())
        self.__pacijent_combobox.set(self.__snimanje.pacijent.ime + " " + self.__snimanje.pacijent.prezime)
        red += 1
        self.__datum_dan_spinbox = Spinbox(self, from_=1, to=31, textvariable=self.__datum_dan)
        self.__datum_dan_spinbox.grid(sticky=E, row=red, column=kolona)
        self.__datum_dan.set(self.__snimanje.datum_i_vreme.day)
        self.__datum_mesec_spinbox = Spinbox(self, from_=1, to=12, textvariable=self.__datum_mesec)
        self.__datum_mesec_spinbox.grid(sticky=E, row=red, column=kolona+1)
        self.__datum_mesec.set(self.__snimanje.datum_i_vreme.month)
        self.__datum_godina_spinbox = Spinbox(self, from_=1900, to=datetime.today().year,
                                              textvariable=self.__datum_godina)
        self.__datum_godina_spinbox.grid(sticky=E, row=red, column=kolona+2)
        self.__datum_godina.set(self.__snimanje.datum_i_vreme.year)
        red += 1
        self.__datum_sat_spinbox = Spinbox(self, from_=0, to=23, textvariable=self.__sati)
        self.__datum_sat_spinbox.grid(sticky=E, row=red, column=kolona)
        self.__sati.set(self.__snimanje.datum_i_vreme.hour)

        self.__datum_minut_spinbox = Spinbox(self, from_=0, to=59, textvariable=self.__minuti)
        self.__datum_minut_spinbox.grid(sticky=E, row=red, column=kolona+1)
        self.__minuti.set(self.__snimanje.datum_i_vreme.minute)
        red += 1
        __lista_tipova = ["Magnetic Resonance (MR)", "Computerised Thomography (CT)", "X-Ray (RX)", "Ultra Sound (US)"]
        self.__tip_combobox = ttk.Combobox(self, textvariable=self.__tip)
        self.__tip_combobox.grid(sticky=E, row=red, column=kolona)
        self.__tip_combobox.config(values=__lista_tipova)
        self.__tip_combobox.set(self.__snimanje.tip)
        red += 1
        self.__lekar_entry = Entry(self, textvariable=self.__lekar)
        self.__lekar_entry.grid(sticky=E, row=red, column=kolona)
        self.__lekar.set(self.__snimanje.lekar)
        red += 1

        self.__snimak_frame = Frame(self)
        self.__snimak_frame.grid(sticky=E, row=red, column=kolona)
        self.__putanja_entry = Entry(self.__snimak_frame, state=DISABLED, textvariable=self.__snimak_putanja)
        self.__putanja_entry.grid(sticky=W, row=red, column=0)
        self.__snimak_putanja.set(self.__snimanje.snimak)
        Button(self.__snimak_frame, width=4, text="...", command=self.otvori_dicom).grid(sticky=W, row=red, column=1)
        red += 1
        Label(self).grid(sticky=W, row=red, column=kolona)
        red += 1
        Button(self, width=16, text="Izmeni snimanmje", command=self.izmeni).grid(sticky=W, row=red, column=kolona)
        Button(self, width=16, text="Odustani", command=self.odustani).grid(sticky=E, row=red, column=kolona+1)

        self.protocol("WM_DELETE_WINDOW", self.odustani)
        # podesavanje prozora
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.title("Izmena snimanja")
        self.iconbitmap("NMK_logotip.ico")
        self.transient(master)
        self.focus_force()
        self.grab_set()


class SnimakProzor(Toplevel):
    @property
    def dataset(self):
        return self.__dataset

    def __init__(self, master, podaci, putanja, dataset):
        super().__init__(master)
        self.__podaci = podaci
        self.__putanja = putanja
        self.__dataset = dataset

        # Prikazivanje podataka o snimanju iz dataseta
        self.__podaci_frame = Frame(self, relief=RIDGE, padx=10, pady=10)
        self.__podaci_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.__lbo_labela = Label(self.__podaci_frame)
        self.__ime_i_prezime_labela = Label(self.__podaci_frame)
        self.__datum_rodj_labela = Label(self.__podaci_frame)
        self.__datum_pregleda_labela = Label(self.__podaci_frame)
        self.__tip_pregleda_labela = Label(self.__podaci_frame)
        self.__lekar_labela = Label(self.__podaci_frame)

        red = 0
        Label(self.__podaci_frame, text="LBO pacijenta:").grid(sticky=E, row=red)
        red += 1
        Label(self.__podaci_frame, text="Ime i prezime pacijenta:").grid(sticky=E, row=red)
        red += 1
        Label(self.__podaci_frame, text="Datum rođenja pacijenta:").grid(sticky=E, row=red)
        red += 1
        Label(self.__podaci_frame, text="Datum pregleda:").grid(sticky=E, row=red)
        red += 1
        Label(self.__podaci_frame, text="Tip pregleda:").grid(sticky=E, row=red)
        red += 1
        Label(self.__podaci_frame, text="Lekar:").grid(sticky=E, row=red)

        # labele u koje kasnije upisujem vrednosti
        kolona = 1
        red = 0
        self.__lbo_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__ime_i_prezime_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__datum_rodj_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__datum_pregleda_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__tip_pregleda_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        self.__lekar_labela.grid(sticky=W, row=red, column=kolona)
        red += 1
        try:
            self.__lbo_labela.config(text=self.__dataset.PatientID)
        except AttributeError:
            self.__lbo_labela.config(text="Nema podatka")
        try:
            self.__ime_i_prezime_labela.config(text=self.__dataset.PatientName)
        except AttributeError:
            self.__ime_i_prezime_labela.config(text="Nema podatka")
        try:
            self.__datum_rodj_labela.config(text=self.__dataset.PatientBirthDate)
        except AttributeError:
            self.__datum_rodj_labela.config(text="Nema podatka")
        try:
            self.__datum_pregleda_labela.config(text=self.__dataset.StudyDate)
        except AttributeError:
            self.__datum_pregleda_labela.config(text="Nema podatka")
        try:
            self.__tip_pregleda_labela.config(text=self.__dataset.Modality)
        except AttributeError:
            self.__tip_pregleda_labela.config(text="Nema podatka")
        try:
            self.__lekar_labela.config(text=self.__dataset.ReferringPhysicianName)
        except AttributeError:
            self.__lekar_labela.config(text="Nema podatka")

        # Prikazivanje slike
        self.__pocetna_slika = ImageTk.PhotoImage(Image.open('DICOM-logo.png'))
        self.__dicom_slika = ImageTk.PhotoImage(pydicom_PIL.get_PIL_image(self.__dataset))
        self.__slika_labela = Label(self)
        self.__slika_labela.pack(side=LEFT, fill=BOTH, expand=1)
        try:
            self.__slika_labela["image"] = self.__dicom_slika
            self.__slika_labela.image = self.__dicom_slika
        except TclError or RuntimeError:
            self.__slika_labela["image"] = self.__pocetna_slika
            self.__slika_labela.image = self.__pocetna_slika
            messagebox.showerror("Greška pri učitvanju", "Slika ne može biti učitana", icon='warning')

        # podesavanje prozora
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.title("Prikaz snimka")
        self.iconbitmap("NMK_logotip.ico")
        self.transient(master)
        self.focus_force()
        self.grab_set()
