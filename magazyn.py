import json
import os

# if not os.path.exists('firma.json):
#     firma = {
#         'stan_konta':0,
#         'stan_magazynu':{},
#         'historia': []
# }

class Manager:
    def __init__(self, firma):
        self.actions = {}
        self.firma = firma

    def assign(self, name):
        def decorate(func):
            self.actions[name] = func

        return decorate

    def execute(self, name):
        if name not in self.actions:
            print("Action not defined")
        else:
            self.actions[name](self)


firma = {
            'stan_konta': 0,
            'stan_magazynu': {},
            'historia': []
        }
manager = Manager(firma)

@manager.assign("saldo")
def saldo(manager):
    operacja = input("Czy chcesz dodać (+) czy odjąć (-) kwotę? ")
    kwota = float(input("Podaj kwotę: "))
    if operacja == "+":
        firma['stan_konta'] += kwota
        print(f"Dodano {kwota} zł do stanu konta.")
        firma['historia'].append([firma['stan_konta'], kwota])
    elif operacja == "-":
        firma['stan_konta'] -= kwota
        print(f"Odjęto {kwota} zł od stanu konta.")
        firma['historia'].append([firma['stan_konta'], kwota])
    else:
        print("Nieznana operacja, spróbuj ponownie.")

@manager.assign("sprzedaż")
def sprzedaz(manager):
    nazwa_produktu = input("Podaj nazwę produktu: ")

    if nazwa_produktu in firma['stan_magazynu']:

        cena = float(input("Podaj cenę: "))

        ilosc = float(input("Podaj ilość sztuk: "))

        if ilosc <= firma['stan_magazynu'][nazwa_produktu]["ilosc"]:

            firma['stan_konta'] += ilosc * cena

            firma['stan_magazynu'][nazwa_produktu]["ilosc"] -= ilosc

            print(f"Sprzedano {ilosc} sztuk produktu {nazwa_produktu} za {ilosc * cena} zł.")

            firma['historia'].append(["sprzedaz", nazwa_produktu, ilosc, cena])

        else:

            print("Nie można sprzedać tylu sztuk. Nie ma wystarczającej ilości produktu na magazynie.")

    else:

        print("Produkt nie jest dostępny na magazynie.")


@manager.assign("zakup")
def zakup(self):
    nazwa_produktu = input(str("Podaj nazwę produktu: "))

    cena = float(input("Podaj cenę produktu: "))

    ilosc = float(input("Podaj ilość sztuk: "))

    # Dodaj produkt do magazynu lub zwiększ jego ilość

    if nazwa_produktu in firma['stan_magazynu']:

        firma['stan_magazynu'][nazwa_produktu]['ilosc'] += ilosc

    else:

        firma['stan_magazynu'][nazwa_produktu] = {'ilosc': ilosc}

    # Oblicz koszt zakupu i zaktualizuj stan konta

    koszt = cena * ilosc

    if firma['stan_konta'] - koszt < 0:

        print("Nie można dokonać zakupu - brak wystarczających środków na koncie.")

    else:

        firma['stan_konta'] -= koszt

        print(f"Zakupiono {ilosc} sztuk produktu {nazwa_produktu} za {koszt} zł. Stan konta: {firma['stan_konta']} zł.")
        firma['historia'].append(['zakup', nazwa_produktu, ilosc, cena])


@manager.assign("konto")
def konto(manager):
    print(f"Aktualny stan konta: {self.firma['stan_konta']} zł")

@manager.assign("lista")
def lista(manager):
    print("Magazyn:")
    for nazwa_produktu in firma['stan_magazynu']:
        print(f"{nazwa_produktu}  ilość: {firma['stan_magazynu'][nazwa_produktu][ilosc]}")

@manager.assign("przeglad")
def przeglad(manager):
    start = input('Podaj "od": ').strip()
    koniec = input('Podaj "do": ').strip()

    if start:
        start = int(start)
    if koniec:
        koniec = int(koniec)

    print(f'Wyswietlam historie od {start} do {koniec}:')
    for wpis in firma['historia'][start:koniec]:
        print(wpis)

with open('firma.json', 'w') as f:
    json.dump(firma, f)

dostepne_akcje = ["saldo", "sprzedaż", "zakup", "konto", "lista","przeglad"]
akcja = input("Podaj akcje: ")

if akcja not in dostepne_akcje:
    print("Akcja niedostepna...")
    quit()
else:
    manager.execute(akcja)


