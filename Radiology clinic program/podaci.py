from pacijent import *
from datetime import datetime
import pickle
from tkinter import filedialog
import pydicom


class Podaci:
    @property
    def snimanja(self):
        return self.__snimanja

    @property
    def pacijenti(self):
        return self.__pacijenti

    def __init__(self):
        self.__snimanja = []
        self.__pacijenti = []

    __naziv_datoteke = "pacijent_i_snimanja_podaci.xml"

    @classmethod
    def sacuvaj(cls, podaci):
        datoteka = open(cls.__naziv_datoteke, "wb")
        pickle.dump(podaci, datoteka)
        datoteka.close()

    @classmethod
    def kreiraj_pocetne(cls):
        podaci = Podaci()

        pacijent1 = Pacijent("00000000001", "Stefan", "Rakic", datetime(1995, 8, 15))
        pacijent2 = Pacijent("00000000002", "Andrej", "Neskovic", datetime(1999, 4, 23))
        snimanje1 = Snimanje(pacijent1, datetime(2015, 12, 11), "Computerised Thomography (CT)",
                             "Dr Dobrica Pavlovic")
        pacijent1.snimanja.append(snimanje1)
        pacijenti = podaci.pacijenti
        pacijenti.append(pacijent1)
        pacijenti.append(pacijent2)
        snimanja = podaci.snimanja
        snimanja.append(snimanje1)
        return podaci

    def otvori_dicom(self):
        staza_do_snimanja = filedialog.askopenfilename(title="Otvaranje", filetypes=[("All files", "*.*"),
                                                                                     ("DICOM files", "*.dcm")])
        if staza_do_snimanja == "":
            return
        return staza_do_snimanja

    def preuzmi_dataset(self, staza):
        dataset = pydicom.dcmread(staza, force=True)
        return dataset

    def dodaj_pacijenta(self, pacijent):
        self.__pacijenti.append(pacijent)

    def dodaj_snimanje(self, snimanje):
        self.__snimanja.append(snimanje)

    @classmethod
    def prikupi_podatke(cls):
        try:
            datoteka = open(cls.__naziv_datoteke, "rb")
            podaci = pickle.load(datoteka)
            datoteka.close()
            return podaci
        except FileNotFoundError:

            return cls.kreiraj_pocetne()

    def obrisi_pacijenta(self, index_pacijenta):
        pacijent = self.__pacijenti[index_pacijenta]
        snimanja_za_brisanje = []
        for snimanje in self.__snimanja:
            if snimanje.pacijent == pacijent:
                snimanja_za_brisanje.append(snimanje)
        for snimanje1 in snimanja_za_brisanje:
            for snimanje2 in self.snimanja:
                if snimanje1 == snimanje2:
                    self.__snimanja.remove(snimanje2)
        self.__pacijenti.pop(index_pacijenta)

    def izmena_pacijenta_u_snimanjima(self, novi_pacijent):
        for snimanje in self.__snimanja:
            if snimanje.pacijent not in self.__pacijenti:
                snimanje.pacijent = novi_pacijent

    def pretraga_pacijenta(self, text):
        if text == "":
            return self.__pacijenti
        lista_pacijenata_za_prikaz = []
        for pacijent in self.__pacijenti:
            if text in pacijent.ime or pacijent.prezime:
                lista_pacijenata_za_prikaz.append(pacijent)
        return lista_pacijenata_za_prikaz

    def pronadji_pacijenta_po_imenu(self, ime_pacijenta):
        for pacijent in self.pacijenti:
            if pacijent.ime + " " + pacijent.prezime == ime_pacijenta:
                return pacijent

    def pronadji_snimanje_pacijenta(self, pacijent, datum_i_vreme):  # funkcija koja vraca index snimanja u listi
        index = 0                                                       # snimanja konkretnog pacijenta
        for snimanje in pacijent.snimanja:
            if snimanje.datum_i_vreme == datum_i_vreme:
                return index
            index += 1

    def obrisi_snimanje(self, index):
        for pacijent in self.pacijenti:
            brojac = 0
            for snimak in pacijent.snimanja:
                if self.__snimanja[index] == snimak:
                    pacijent.snimanja.pop(brojac)
                brojac += 1

        self.__snimanja.pop(index)

    def sortiraj_pacijente(self):
        self.__pacijenti = sorted(self.__pacijenti, key=lambda pacijent: pacijent.prezime + pacijent.ime)

    def sortiraj_snimanja(self):
        self.__snimanja = sorted(self.__snimanja, key=lambda snimanje: snimanje.datum_i_vreme)
