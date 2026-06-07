
USER_LOGIN = "admin"
USER_PASS = "admin"

firmy = [
    {
        "id": 1,
        "nazwa": "AdVance",
        "lokalizacja": "Lublin",
        "wydarzenie": "Konferencja Biznesowa 2026",
        "wspolrzedne": [51.2464, 22.5684]
    },
    {
        "id": 2,
        "nazwa": "WarsawAds",
        "lokalizacja": "Warszawa",
        "wydarzenie": "BrandVision Summit",
        "wspolrzedne": [52.2297, 21.0122]
    },
    {
        "id": 3,
        "nazwa": "Marketing4u",
        "lokalizacja": "Kraków",
        "wydarzenie": "Social Media Summit",
        "wspolrzedne": [50.0614, 19.9366]
    },
    {
        "id": 4,
        "nazwa": "M&S marketing",
        "lokalizacja": "Gdańsk",
        "wydarzenie": "Sales and Marketing Summit 2026",
        "wspolrzedne": [54.3520, 18.6466]
    },
    {
        "id": 5,
        "nazwa": "Talent Corp",
        "lokalizacja": "Poznań",
        "wydarzenie": "HR & Marketing Tech",
        "wspolrzedne": [52.4064, 16.9252]
    },
{
        "id": 6,
        "nazwa": "GrowLab",
        "lokalizacja": "Łódź",
        "wydarzenie": "Marketing Sandbox",
        "wspolrzedne": [51.7592, 19.4560]
    },
{
        "id": 7,
        "nazwa": "TheView",
        "lokalizacja": "Wrocław",
        "wydarzenie": "Targi Pracy Wrocław 2026",
        "wspolrzedne": [51.1077, 17.0385]
    },
{
        "id": 8,
        "nazwa": "Pryzmat",
        "lokalizacja": "Olsztyn",
        "wydarzenie": "Staregie sukcesu - panel dyskusyjny",
        "wspolrzedne": [53.7784, 20.4801]
    }
]

pracownicy = [
    {"id": 1, "imie": "Jan", "nazwisko": "Kowalski", "firma_id": 1, "lokalizacja": "Lublin", "wspolrzedne": [51.2464, 22.5684]},
    {"id": 2, "imie": "Anna", "nazwisko": "Nowak", "firma_id": 2, "lokalizacja": "Warszawa", "wspolrzedne": [52.2297, 21.0122]},
    {"id": 3, "imie": "Piotr", "nazwisko": "Wiśniewski", "firma_id": 3, "lokalizacja": "Kraków", "wspolrzedne": [50.0614, 19.9366]},
    {"id": 4, "imie": "Maria", "nazwisko": "Wójcik", "firma_id": 4, "lokalizacja": "Gdańsk", "wspolrzedne": [54.3520, 18.6466]},
    {"id": 5, "imie": "Krzysztof", "nazwisko": "Kowalczyk", "firma_id": 1, "lokalizacja": "Lublin", "wspolrzedne": [51.2464, 22.5684]},
    {"id": 6, "imie": "Barbara", "nazwisko": "Wójcik", "firma_id": 2, "lokalizacja": "Warszawa", "wspolrzedne": [52.2297, 21.0122]},
    {"id": 7, "imie": "Agnieszka", "nazwisko": "Kamińska", "firma_id": 4, "lokalizacja": "Sopot", "wspolrzedne": [54.4416, 18.5601]},
    {"id": 8, "imie": "Michał", "nazwisko": "Lewandowski", "firma_id": 2, "lokalizacja": "Warszawa", "wspolrzedne": [52.2297, 21.0122]},
    {"id": 9, "imie": "Paweł", "nazwisko": "Dorociński", "firma_id": 1, "lokalizacja": "Warszawa", "wspolrzedne": [52.2297, 21.0122]},
    {"id": 10, "imie": "Weronika", "nazwisko": "Masłowska", "firma_id": 1, "lokalizacja": "Radom", "wspolrzedne": [51.4027, 21.1471]},
    {"id": 11, "imie": "Ewa", "nazwisko": "Zając", "firma_id": 5, "lokalizacja": "Poznań", "wspolrzedne": [52.4064, 16.9252]},
    {"id": 12, "imie": "Marcin", "nazwisko": "Sikorski", "firma_id": 6, "lokalizacja": "Łódź", "wspolrzedne": [51.7592, 19.4560]},
    {"id": 13, "imie": "Zuzanna", "nazwisko": "Domańska", "firma_id": 7, "lokalizacja": "Wrocław", "wspolrzedne": [51.1077, 17.0385]},
    {"id": 14, "imie": "Adam", "nazwisko": "Królikowski", "firma_id": 7, "lokalizacja": "Lubin", "wspolrzedne": [51.4026, 16.2066]},
    {"id": 15, "imie": "Iga", "nazwisko": "Dąbrowska-Król", "firma_id": 7, "lokalizacja": "Legnica", "wspolrzedne": [51.2069, 16.1619]},
    {"id": 16, "imie": "Wiktor", "nazwisko": "Wolski", "firma_id": 3, "lokalizacja": "Tarnów", "wspolrzedne": [50.0105, 20.9859]},
    {"id": 17, "imie": "Karolina", "nazwisko": "Wierzbicka", "firma_id": 2, "lokalizacja": "Warszawa", "wspolrzedne": [52.2297, 21.0122]},
    {"id": 18, "imie": "Wiktoria", "nazwisko": "Rutkowska", "firma_id": 6, "lokalizacja": "Częstochowa", "wspolrzedne": [50.8118, 19.1203]},
    {"id": 19, "imie": "Marek", "nazwisko": "Szymański", "firma_id": 6, "lokalizacja": "Kalisz", "wspolrzedne": [51.7611, 18.0936]},
    {"id": 20, "imie": "Maria", "nazwisko": "Kuźmierz", "firma_id": 5, "lokalizacja": "Zielona Góra", "wspolrzedne": [51.9356, 15.5062]},
    {"id": 21, "imie": "Aleksander", "nazwisko": "Zieliński", "firma_id": 5, "lokalizacja": "Piła", "wspolrzedne": [53.1511, 16.7371]},
    {"id": 22, "imie": "Aleksandra", "nazwisko": "Ostrowska", "firma_id": 8, "lokalizacja": "Olsztyn", "wspolrzedne": [53.7784, 20.4802]},
    {"id": 23, "imie": "Piotr", "nazwisko": "Pawlak", "firma_id": 8, "lokalizacja": "Olsztyn", "wspolrzedne": [53.7784, 20.4802]},
    {"id": 24, "imie": "Alicja", "nazwisko": "Pomorska", "firma_id": 3, "lokalizacja": "Kraków", "wspolrzedne": [50.0614, 19.9366]},
    {"id": 25, "imie": "Jan", "nazwisko": "Kurek", "firma_id": 4, "lokalizacja": "Gdynia", "wspolrzedne": [54.5189, 18.5305]},
    {"id": 26, "imie": "Zofia", "nazwisko": "Modrzewska", "firma_id": 8, "lokalizacja": "Białystok", "wspolrzedne": [53.1325, 23.1688]},
    {"id": 27, "imie": "Amelia", "nazwisko": "Nieściór", "firma_id": 3, "lokalizacja": "Rzeszów", "wspolrzedne": [50.0412, 21.9991]}
]



bazy_klientow = [
    {"id": 101, "nazwa": "Herbapol Lublin", "firma_id": 1},
    {"id": 102, "nazwa": "Maczfit", "firma_id": 1},
    {"id": 103, "nazwa": "Trafford IT", "firma_id": 2},
    {"id": 104, "nazwa": "Panattoni Polska", "firma_id": 3},
    {"id": 105, "nazwa": "Media Expert", "firma_id": 4},
    {"id": 106, "nazwa": "LUXMED", "firma_id": 5},
    {"id": 107, "nazwa": "Polskie Linie Lotnicze LOT", "firma_id": 2},
    {"id": 108, "nazwa": "Polbruk", "firma_id": 4},
    {"id": 109, "nazwa": "Inglot", "firma_id": 2},
    {"id": 110, "nazwa": "Lidl Polska", "firma_id": 7},
    {"id": 111, "nazwa": "x-kom", "firma_id": 8},
    {"id": 112, "nazwa": "Apart", "firma_id": 6},
    {"id": 113, "nazwa": "Castorama", "firma_id": 3},
    {"id": 114, "nazwa": "Rossmann", "firma_id": 6},
    {"id": 115, "nazwa": "Orange Polska", "firma_id": 7},
    {"id": 116, "nazwa": "PKO BP", "firma_id": 5},
    {"id": 117, "nazwa": "PZU", "firma_id": 8}

]

aktualna_firma_id = None
aktualny_pracownik_id = None
aktualna_baza_id = None