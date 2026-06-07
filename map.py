import math
import models

map_widget = None
aktualny_tryb = "firmy"

def init_map(widget):
    global map_widget
    map_widget = widget

def pokaz_cala_polske():
    latitudes = []
    longitudes = []

    for f in models.firmy:
        latitudes.append(f["wspolrzedne"][0])
        longitudes.append(f["wspolrzedne"][1])

    for p in models.pracownicy:
        latitudes.append(p["wspolrzedne"][0])
        longitudes.append(p["wspolrzedne"][1])

    if not latitudes or not longitudes:
        map_widget.set_position(52.2297, 21.0122)
        map_widget.set_zoom(6)
        return

    min_lat = min(latitudes)
    max_lat = max(latitudes)
    min_lon = min(longitudes)
    max_lon = max(longitudes)

    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    map_widget.set_position(center_lat, center_lon)
    spread = max(max_lat - min_lat, max_lon - min_lon)

    if spread < 0.5: zoom = 9
    elif spread < 1: zoom = 8
    elif spread < 2: zoom = 7
    else: zoom = 6

    map_widget.set_zoom(zoom)

def przesun_marker(lat, lon, numer):
    if numer == 0:
        return lat, lon

    kat = numer * (math.pi / 4)
    promien = 0.02 + (0.01 * (numer // 8))

    nowy_lat = lat + (promien * math.cos(kat))
    nowy_lon = lon + (promien * math.sin(kat) * 1.5)

    return nowy_lat, nowy_lon

def wyznacz_zoom_i_centrum(znalezione_obiekty):
    if not znalezione_obiekty:
        return None

    if len(znalezione_obiekty) == 1:
        ob = znalezione_obiekty[0]
        return ob["wspolrzedne"][0], ob["wspolrzedne"][1], 13

    lats = [ob["wspolrzedne"][0] for ob in znalezione_obiekty]
    lons = [ob["wspolrzedne"][1] for ob in znalezione_obiekty]

    c_lat = sum(lats) / len(lats)
    c_lon = sum(lons) / len(lons)

    return c_lat, c_lon, 13

def pokaz_mape_firm(miasto="", wycentruj=False, wybrany_id=None):
    global aktualny_tryb
    aktualny_tryb = "firmy"
    map_widget.delete_all_marker()

    znalezione = []
    licznik_pozycji = {}

    for firma in models.firmy:
        if miasto and miasto.lower() not in firma["lokalizacja"].lower():
            continue

        znalezione.append(firma)
        lat = firma["wspolrzedne"][0]
        lon = firma["wspolrzedne"][1]

        klucz = firma["lokalizacja"].strip().lower()
        numer = licznik_pozycji.get(klucz, 0)
        lat, lon = przesun_marker(lat, lon, numer)
        licznik_pozycji[klucz] = numer + 1

        def klik(marker, f=firma):
            import controller
            if controller.view:
                controller.view.pokaz_okno_markera(f["wydarzenie"], f["nazwa"], f["lokalizacja"])

        kolor = "red" if wybrany_id == firma["id"] else "blue"

        map_widget.set_marker(
            lat, lon,
            text="",
            marker_color_outside=kolor,
            marker_color_circle="white",
            text_color="white",
            command=klik
        )

        if wybrany_id == firma["id"]:
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(13)

    if wycentruj and znalezione and not wybrany_id:
        wynik = wyznacz_zoom_i_centrum(znalezione)
        if wynik:
            lat, lon, zoom = wynik
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(zoom)

    if not miasto and not wybrany_id:
        pokaz_cala_polske()

def pokaz_mape_pracownikow(miasto="", wycentruj=False, wybrany_id=None):
    global aktualny_tryb
    aktualny_tryb = "pracownicy"
    map_widget.delete_all_marker()

    znalezione = []
    licznik_pozycji = {}

    for pracownik in models.pracownicy:
        if miasto and miasto.lower() not in pracownik["lokalizacja"].lower():
            continue

        znalezione.append(pracownik)
        lat = pracownik["wspolrzedne"][0]
        lon = pracownik["wspolrzedne"][1]

        klucz = pracownik["lokalizacja"].strip().lower()
        numer = licznik_pozycji.get(klucz, 0)
        lat, lon = przesun_marker(lat, lon, numer)
        licznik_pozycji[klucz] = numer + 1

        def klik(marker, p=pracownik):
            import controller
            firma_nazwa = "Nieznana"
            wydarzenie_nazwa = "Brak przypisanego wydarzenia"
            for f in models.firmy:
                if f["id"] == p["firma_id"]:
                    firma_nazwa = f["nazwa"]
                    wydarzenie_nazwa = f["wydarzenie"]
                    break

            if controller.view:
                controller.view.pokaz_okno_pracownika(f"{p['imie']} {p['nazwisko']}", firma_nazwa, wydarzenie_nazwa, p['lokalizacja'])

        kolor = "red" if wybrany_id == pracownik["id"] else "green"

        map_widget.set_marker(
            lat, lon,
            text="",
            marker_color_outside=kolor,
            marker_color_circle="white",
            text_color="white",
            command=klik
        )

        if wybrany_id == pracownik["id"]:
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(13)

    if wycentruj and znalezione and not wybrany_id:
        wynik = wyznacz_zoom_i_centrum(znalezione)
        if wynik:
            lat, lon, zoom = wynik
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(zoom)

    if not miasto and not wybrany_id:
        pokaz_cala_polske()