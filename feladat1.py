from abc import ABC, abstractmethod
from datetime import date

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def info(self):
        pass

class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, utasszam):
        super().__init__(rendszam, tipus, berleti_dij)
        self.utasszam = utasszam

    def info(self):
        return f"Személyautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, Bérleti díj: {self.berleti_dij} Ft/nap, Utasok: {self.utasszam}"

class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, max_teher):
        super().__init__(rendszam, tipus, berleti_dij)
        self.max_teher = max_teher

    def info(self):
        return f"Teherautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, Bérleti díj: {self.berleti_dij} Ft/nap, Max. teher: {self.max_teher} kg"

class Berles:
    def __init__(self, auto, datum):
        self.auto = auto
        self.datum = datum

    def ar(self):
        return self.auto.berleti_dij

    def info(self):
        return f"Bérlés - Autó: {self.auto.rendszam}, Dátum: {self.datum}, Ár: {self.ar()} Ft"

class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def hozzaad_auto(self, auto):
        self.autok.append(auto)

    def berel_auto(self, rendszam, datum):
        if datum < date.today():
            return "Hibás dátum."
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                return "Az autó már foglalt ezen a napon."
        for auto in self.autok:
            if auto.rendszam == rendszam:
                uj_berles = Berles(auto, datum)
                self.berlesek.append(uj_berles)
                return f"Bérlés sikeres: {uj_berles.info()}"
        return "Nincs ilyen rendszámú autó."

    def lemond_berles(self, rendszam, datum):
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                self.berlesek.remove(berles)
                return "Bérlés lemondva."
        return "Nincs ilyen bérlés."

    def listaz_berlesek(self):
        if not self.berlesek:
            return "Nincsenek aktuális bérlések."
        return "\n".join([b.info() for b in self.berlesek])

# Előre betöltött adatok
kolcsonzo = Autokolcsonzo("Teszt Autókölcsönző")
kolcsonzo.hozzaad_auto(Szemelyauto("ABC-123", "Opel Astra", 10000, 5))
kolcsonzo.hozzaad_auto(Szemelyauto("XYZ-789", "Ford Focus", 12000, 5))
kolcsonzo.hozzaad_auto(Teherauto("TRK-456", "Mercedes Sprinter", 15000, 2000))
kolcsonzo.berel_auto("ABC-123", date.today())
kolcsonzo.berel_auto("XYZ-789", date.today())
kolcsonzo.berel_auto("TRK-456", date.today())
kolcsonzo.berel_auto("ABC-123", date.today().replace(day=date.today().day + 1))

# Egyszerű CLI
while True:
    print("\n1. Autó bérlése\n2. Bérlés lemondása\n3. Bérlések listázása\n0. Kilépés")
    valasztas = input("Választás: ")
    if valasztas == "1":
        rendszam = input("Rendszám: ")
        datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
        try:
            datum = date.fromisoformat(datum)
            print(kolcsonzo.berel_auto(rendszam, datum))
        except ValueError:
            print("Hibás dátumformátum.")
    elif valasztas == "2":
        rendszam = input("Rendszám: ")
        datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
        try:
            datum = date.fromisoformat(datum)
            print(kolcsonzo.lemond_berles(rendszam, datum))
        except ValueError:
            print("Hibás dátumformátum.")
    elif valasztas == "3":
        print(kolcsonzo.listaz_berlesek())
    elif valasztas == "0":
        break
    else:
        print("Érvénytelen választás.")