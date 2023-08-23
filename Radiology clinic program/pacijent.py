class Pacijent:
    def __init__(self, lbo, ime, prezime, datum_rodjenja):
        self.__lbo = lbo
        self.__ime = ime
        self.__prezime = prezime
        self.__datum = datum_rodjenja
        self.__snimanja = []

    @property
    def lbo(self):
        return self.__lbo

    @property
    def ime(self):
        return self.__ime

    @property
    def prezime(self):
        return self.__prezime

    @property
    def datum_rodjenja(self):
        return self.__datum

    @property
    def snimanja(self):
        return self.__snimanja


class Snimanje:
    def __init__(self, pacijent, datum_i_vreme, tip, lekar, snimak=None):
        self.__pacijent = pacijent
        self.__datum_i_vreme = datum_i_vreme
        self.__tip = tip
        self.__lekar = lekar
        self.__snimak = snimak

    @property
    def pacijent(self):
        return self.__pacijent

    @pacijent.setter
    def pacijent(self, pacijent):
        self.__pacijent = pacijent

    @property
    def datum_i_vreme(self):
        return self.__datum_i_vreme

    @property
    def tip(self):
        return self.__tip

    @property
    def lekar(self):
        return self.__lekar

    @property
    def snimak(self):
        return self.__snimak


class Snimak:

    def __init__(self, putanja):
        self.__putanja = putanja
