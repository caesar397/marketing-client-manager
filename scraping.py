import requests
import controller

def pobierz_wspolrzedne(lokalizacja: str) -> list:
    czysta_lokalizacja = lokalizacja.strip()

    if not czysta_lokalizacja:
        return [52.2297, 21.0122]

    try:
        url = f"https://nominatim.openstreetmap.org/search?q={czysta_lokalizacja},Poland&format=json&limit=1"
        headers = {'User-Agent': 'SystemMarketingowy/1.0'}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()

        if data:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            print(f"Sukces API dla '{czysta_lokalizacja}': [{latitude}, {longitude}]")
            return [latitude, longitude]

        raise Exception("Brak wyników w bazie geograficznej")

    except Exception as e:
        print(f"Błąd pobierania dla '{lokalizacja}': {e}")
        if controller.view:
            controller.view.pokaz_komunikat("Błąd geolokalizacji", f"Nie znaleziono miejscowości '{lokalizacja}'. Przypisano pozycję domyślną (Warszawa).")
        return [52.2297, 21.0122]