import json


class Oseba:
    ime = None
    priimek = None
    email = None

    def polno_ime(self):
        return self.ime + " " + self.priimek


class Uporabnik(Oseba):
    je_blokiran = False

    def __init__(self, ime, priimek, email):
        self.ime = ime
        self.priimek = priimek
        self.email = email

    def shrani(self):
        ime_datoteke = self.ime + "-" + self.priimek + ".txt"
        with open(ime_datoteke, "w") as datoteka:
            podatki = self.__dict__
            datoteka.write(json.dumps(podatki))


class Moderator(Oseba):
    pravice = []

    def ima_pravico(self, pravica):
        return pravica in self.pravice


uporabnik1 = Uporabnik("Miha", "Novak", "miha.novak@email.si")
#uporabnik1.je_blokiran = False

uporabnik2 = Uporabnik("Mojca", "Koren", "mojca.koren@email.si")
uporabnik2.je_blokiran = True


print(uporabnik1.polno_ime())
print(uporabnik2.polno_ime())

uporabnik1.shrani()
uporabnik2.shrani()


mod1 = Moderator()
mod1.ime = "Ana"
mod1.priimek = "Novak"
mod1.email = "ana.novak@email.si"
mod1.pravice = ["izbris_uporabnikov", "sprememba_objav"]
