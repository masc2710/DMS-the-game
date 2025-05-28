'''
    todo:
    - separate output shell
    - grafisch darstellung
    - konstantes Leaderboard

'''

import random
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table

# Initialisiere Colorama und Rich
init()
console = Console()

farben = ["Herz", "Eck", "Schaufel", "Kreuz"]
werte = ["6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]

karten = [f"{farbe} {wert}" for farbe in farben for wert in werte]

# Fixe Zuordnung der Effekte zu Karten (jede Karte hat immer denselben Effekt)
karten_effekte = {
    "Herz Ass": "Start: Alle Spieler trinken 4 Schlücke", #todo: Starteffekte implementieren
    "Herz König": "Königs-Komplex: Der Spieler der auf dieser Karte landet muss eine Regel erstellen. Besagte Regel gilt aber nur bis ein neuer Spieler eine Regel erstellen muss",
    "Herz Dame": "Z’Mami: Einen Shot für den Spieler. TO GET FUCKING LOW!!!!",
    "Herz Bube": "„unfreiwilliger Arbeitshelfer“: Der Spieler muss einen anderen zu seinem Arbeitsgehilfen ernennen. Wenn einer der beiden Spieler trinken muss, trinkt der Andere stets mit. Diese Beziehung besteht so lange bis jemand einen eigenen „Arbeitshelfer“ auswählen muss.",
    "Herz 10": "Binär 2: Der Spieler trink von nun an für eine Runde das Doppelte von dem was er trinken muss",
    "Herz 9": "Platztausch: Der Spieler fängt beim letzten Spieler(der, der am weitesten auf den Spielbrett zurückliegt ) an den Spielerfiguren entlang zu zählen bis er bei der Spielfigur angekommen ist, der seiner gewürfelten Augenzahl entspricht. Die beiden Spieler wechseln daraufhin Platz auf dem Spielbrett", #todo: Platztausch implementieren
    "Herz 8": "Der Gastronom: Der Spieler bedient von nun an die Anderen. Dies muss er aber nur wenn er von einem anderen Spieler höflich dazu aufgefordert wird. Der Spieler ist so lange Gastronom bis jemand anderes die Herz 8 betritt und somit die Funktion übernimmt.",
    "Herz 7": "Verjüngung: Der Spieler muss das Spiel verjüngen, d.h. der Spieler muss 1-3 Getränke extra in die Mitte stellen.",
    "Herz 6": "Klein wie ein Flo: Der Spieler muss eine Runden lang mit seinem Kinn den Tisch berühren. Er darf seinen Kopf nur zum Trinken hochheben",
    "Eck Ass": "„20i-Challengen“: Der Spieler feiert seinen 20. Geburtstag und trinkt deshalb zwei Runden lang alles was die Anderen trinken müssen mit.", 
    "Eck König": "6 Schlücke trinken",
    "Eck Dame": "6 Schlücke trinken",
    "Eck Bube": "5 Schlücke trinken",
    "Eck 10": "5 Schlücke trinken",
    "Eck 9": "4 Schlücke trinken",
    "Eck 8": "4 Schlücke trinken",
    "Eck 7": "3 Schlücke trinken",
    "Eck 6": "3 Schlücke trinken",
    "Schaufel Ass": "Hangover: Der Spieler hat sich entschieden eine kleine Pussy zu sein und darf somit eine Runde lang nicht mittrinken und muss 1x aussetzten..", #todo: Hangover
    "Schaufel König": "6 Schlücke verteilen",
    "Schaufel Dame": "6 Schlücke verteilen",
    "Schaufel Bube": "5 Schlücke verteilen",
    "Schaufel 10": "5 Schlücke verteilen",
    "Schaufel 9": "4 Schlücke verteilen",
    "Schaufel 8": "4 Schlücke verteilen",
    "Schaufel 7": "3 Schlücke verteilen",
    "Schaufel 6": "3 Schlücke verteilen",
    "Kreuz Ass": "Hangover: Der Spieler hat sich entschieden eine kleine Pussy zu sein und darf somit eine Runde lang nicht mittrinken und muss 1x aussetzten..", #todo: hangover
    "Kreuz König": "6 Schlücke verteilen",
    "Kreuz Dame": "6 Schlücke verteilen",
    "Kreuz Bube": "5 Schlücke verteilen",
    "Kreuz 10": "5 Schlücke verteilen",
    "Kreuz 9": "4 Schlücke verteilen",
    "Kreuz 8": "4 Schlücke verteilen",
    "Kreuz 7": "3 Schlücke verteilen",
    "Kreuz 6": "3 Schlücke verteilen"
}

# Mische die Karten (Reihenfolge zufällig, Effekte bleiben fix)
karten.remove("Herz Ass")  # Startfeld immer zuerst
random.shuffle(karten)
karten.insert(0, "Herz Ass")  # Startfeld an Position 0

feld_dict = {karte: karten_effekte[karte] for karte in karten}

class Feld:
    def __init__(self, karte, effekt=None):
        self.karte = karte
        self.effekt = effekt
        self.aufgedeckt = karte == "Herz Ass"  # Startfeld ist aufgedeckt

    def __str__(self):
        return f"{self.karte}: {self.effekt if self.aufgedeckt else '???'}"

class Spieler:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.laufmeter = 0

    def __str__(self):
        return f"{self.name} | Pos: {self.position} | Laufmeter: {self.laufmeter}"

class Spiel:
    def __init__(self, feld_dict):
        self.brett = [Feld(karte, feld_dict[karte]) for karte in feld_dict]
        self.spieler = [Spieler(f"Spieler {i+1}") for i in range(4)]
        self.runde = 0
        self.active = [True]*4

    def zeige_spielfeld(self):
        """Zeigt das Spielfeld in einer kreisförmigen Anordnung."""
        spielfeld = [" " for _ in range(36)]  # Leeres Spielfeld mit 36 Feldern

        # Spieler auf dem Spielfeld platzieren
        for sp in self.spieler:
            spielfeld[sp.position] = sp.name[0]  # Nutze den ersten Buchstaben des Spielernamens

        # Kreisförmige Darstellung
        print("\n" + " " * 10 + f"{spielfeld[0]}---{spielfeld[1]}---{spielfeld[2]}---{spielfeld[3]}---{spielfeld[4]}")
        print(" " * 8 + f"|                           |")
        print(" " * 8 + f"|   {spielfeld[35]}                 {spielfeld[5]}   |")
        print(" " * 8 + f"|                           |")
        print(" " * 10 + f"{spielfeld[34]}                 {spielfeld[6]}")
        print(" " * 8 + f"|                           |")
        print(" " * 8 + f"|   {spielfeld[33]}                 {spielfeld[7]}   |")
        print(" " * 8 + f"|                           |")
        print(" " * 10 + f"{spielfeld[32]}---{spielfeld[31]}---{spielfeld[30]}---{spielfeld[29]}---{spielfeld[28]}")

        print("\nLegende:")
        for sp in self.spieler:
            print(f"{sp.name[0]}: {sp.name}")

    def wurf(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def runde_spielen(self):
        print(Fore.MAGENTA + f"\n--- Runde {self.runde + 1} ---" + Style.RESET_ALL)
        for i, sp in enumerate(self.spieler):
            if not self.active[i]:
                print(Fore.YELLOW + f"{sp.name} setzt aus." + Style.RESET_ALL)
                self.active[i] = True
                continue

            input(Fore.CYAN + f"{sp.name}, drücke Enter zum Würfeln..." + Style.RESET_ALL)
            wurf = self.wurf()
            print(Fore.GREEN + f"{sp.name} würfelt eine {wurf}!" + Style.RESET_ALL)

            alte_position = sp.position
            neue_position = (sp.position + wurf) % 36

            # Prüfe, ob Spieler direkt auf Start landet
            if neue_position == 0:
                distanz = -alte_position
                print(Fore.CYAN + f"{sp.name} landet direkt auf Start!" + Style.RESET_ALL)
            else:
                # Prüfe, ob Spieler über Start gegangen ist
                if neue_position < alte_position:
                    distanz = (36 - alte_position) + neue_position
                    print(Fore.YELLOW + f"{sp.name} ist über Start gegangen und alle Spieler trinken 2 Schlücke!" + Style.RESET_ALL)
                else:
                    distanz = neue_position - alte_position

            # Prüfe, ob Feld bereits besetzt ist
            besetzte_positionen = [spieler.position for spieler in self.spieler if spieler != sp]
            while neue_position in besetzte_positionen:
                print(Fore.RED + f"Feld {neue_position} ist bereits besetzt! {sp.name} rückt ein Feld weiter." + Style.RESET_ALL)
                neue_position = (neue_position + 1) % 36
                distanz += 1

            sp.position = neue_position
            sp.laufmeter += distanz

            feld = self.brett[sp.position]
            if not feld.aufgedeckt:
                feld.aufgedeckt = True
                print(Fore.BLUE + f"{sp.name} hat ein neues Feld aufgedeckt: {feld.karte} - {feld.effekt}" + Style.RESET_ALL)
            else:
                print(Fore.BLUE + f"{sp.name} ist auf {feld}" + Style.RESET_ALL)

            self.feld_aktion(i, feld.effekt, wurf)

        self.runde += 1
        self.zeige_spielfeld()  # Zeige das Spielfeld nach jeder Runde

    def feld_aktion(self, i, effekt, wurf):
        sp = self.spieler[i]
        if effekt.startswith("Hangover"):
            self.active[i] = False
        elif effekt == "Platztausch: Der Spieler fängt beim letzten Spieler(der, der am weitesten auf den Spielbrett zurückliegt ) an den Spielerfiguren entlang zu zählen bis er bei der Spielfigur angekommen ist, der seiner gewürfelten Augenzahl entspricht. Die beiden Spieler wechseln daraufhin Platz auf dem Spielbrett":
            self.platztausch(i, wurf)
        # Weitere Effekte implementierbar...

    def platztausch(self, aktueller_spieler_index, wurf):
        sortierte_spieler = sorted(self.spieler, key=lambda x: x.laufmeter)
        aktueller_spieler = self.spieler[aktueller_spieler_index]

        # Beginne beim Spieler mit den wenigsten Laufmetern
        index = 0
        zaehler = 1  # Starte Zählung bei 1 (erster Spieler ist bereits gezählt)

        # Zähle bis zum n-ten Spieler (n = wurf)
        while zaehler < wurf:
            index = (index + 1) % len(sortierte_spieler)
            zaehler += 1

        ziel_spieler = sortierte_spieler[index]

        # Tausche Position und Laufmeter
        aktueller_spieler.position, ziel_spieler.position = ziel_spieler.position, aktueller_spieler.position
        aktueller_spieler.laufmeter, ziel_spieler.laufmeter = ziel_spieler.laufmeter, aktueller_spieler.laufmeter

        print(f"{aktueller_spieler.name} tauscht Platz mit {ziel_spieler.name}!")

    def status(self):
        for sp in self.spieler:
            print(sp)

    def start(self):
        print("Spiel gestartet! 4 Spieler, Ziel: am weitesten laufen!")
        self.zeige_spielfeld()  # Zeige das Spielfeld zu Beginn
        while True:
            self.runde_spielen()
            self.status()
            befehl = input("Drücke Enter für nächste Runde oder 'q' zum Beenden: ")
            if befehl.lower() == 'q':
                break
        self.gewinner_anzeigen()

    def gewinner_anzeigen(self):
        print("\nSpiel beendet! Gewinner:")
        max_lauf = max(self.spieler, key=lambda x: x.laufmeter)
        for sp in self.spieler:
            print(sp)
        print(f"🏆 Gewinner: {max_lauf.name} mit {max_lauf.laufmeter} Schritten!")


if __name__ == "__main__":
    spiel = Spiel(feld_dict)
    spiel.start()
