import json


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


firma = {"stan_konta": 0, "stan_magazynu": {}, "historia": []}

manager = Manager(firma)


@manager.assign("saldo")
def saldo(manager):
    operacja = input("Czy chcesz dodać (+) czy odjąć (-) kwotę? ")
    kwota = float(input("Podaj kwotę: "))
    if operacja == "+":
        manager.firma["stan_konta"] += kwota
    elif operacja == "-":
        manager.firma["stan_konta"] -= kwota
    else:
        return "err"
    manager.firma["historia"].append([manager.firma["stan_konta"], kwota])


@manager.assign("sprzedaz")
def sprzedaz(manager):
    nazwa_produktu = input("Podaj nazwę produktu: ")

    if nazwa_produktu in manager.firma["stan_magazynu"]:
        cena = float(input("Podaj cenę: "))
        ilosc = float(input("Podaj ilość sztuk: "))

        if ilosc <= manager.firma["stan_magazynu"][nazwa_produktu]["ilosc"]:
            manager.firma["stan_konta"] += ilosc * cena
            manager.firma["stan_magazynu"][nazwa_produktu]["ilosc"] -= ilosc
            manager.firma["historia"].append(["sprzedaz", nazwa_produktu, ilosc, cena])
        else:
            return "Nie można sprzedać tylu sztuk. Nie ma wystarczającej ilości produktu na magazynie."
    else:
        return "Produkt nie jest dostępny na magazynie."


@manager.assign("zakup")
def zakup(manager):
    nazwa_produktu = input(str("Podaj nazwę produktu: "))
    cena = float(input("Podaj cenę produktu: "))
    ilosc = float(input("Podaj ilość sztuk: "))

    # Oblicz koszt zakupu i zaktualizuj stan konta

    koszt = cena * ilosc

    if manager.firma["stan_konta"] < koszt:
        return "Nie można dokonać zakupu - brak wystarczających środków na koncie."
    else:
        manager.firma["stan_konta"] -= koszt
        manager.firma["historia"].append(["zakup", nazwa_produktu, ilosc, cena])

    # Dodaj produkt do magazynu lub zwiększ jego ilość

    if nazwa_produktu not in manager.firma["stan_magazynu"]:
        manager.firma["stan_magazynu"][nazwa_produktu] = {"ilosc": 0}
    manager.firma["stan_magazynu"][nazwa_produktu]["ilosc"] += ilosc


@manager.assign("konto")
def konto(manager):
    print(f"Aktualny stan konta: {manager.firma['stan_konta']} zł")


@manager.assign("lista")
def lista(manager):
    print("Magazyn:")
    for nazwa_produktu in firma["stan_magazynu"]:
        print(
            f"{nazwa_produktu}  ilość: {manager.firma['stan_magazynu'][nazwa_produktu]['ilosc']}"
        )


@manager.assign("przeglad")
def przeglad(manager):
    start = input('Podaj "od": ').strip()
    koniec = input('Podaj "do": ').strip()

    if start:
        start = int(start)
    if koniec:
        koniec = int(koniec)

    print(f"Wyswietlam historie od {start} do {koniec}:")
    for wpis in manager.firma["historia"][start:koniec]:
        print(wpis)


with open("firma.json", "w") as f:
    json.dump(manager.firma, f)

DOSTEPNE_AKCJE = ["saldo", "sprzedaz", "zakup", "konto", "lista", "przeglad"]

while True:
    print('Lista dostępnych akcji: \n"saldo"\n, "sprzedaz"\n, "zakup"\n, "konto"\n, "lista"\n, "przeglad"\n')
    akcja = input("Podaj akcje: ")
    if akcja not in DOSTEPNE_AKCJE:
        print("Akcja niedostepna...")
        quit()
    else:
        manager.execute(akcja)
