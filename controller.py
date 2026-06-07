from tkinter import END
import models
import scraping
import map

view = None


def przypisz_widok(instancja_widoku):
    global view
    view = instancja_widoku


def sprawdz_logowanie(event=None):
    if view.entry_login.get() == models.USER_LOGIN and view.entry_haslo.get() == models.USER_PASS:
        view.ramka_logowania.pack_forget()
        view.rozszerz_i_uruchom_aplikacje()
    else:
        view.pokaz_komunikat("Błąd", "Nieprawidłowy login lub hasło!")


def zmieniono_zakladke(event):
    try:
        zakladka = event.widget.tab(event.widget.index("current"), "text")
        if zakladka == "Firmy":
            aktywuj_mape_firm()
        elif zakladka == "Pracownicy":
            aktywuj_mape_pracownikow()
        elif zakladka == "Baza Klientów":
            aktywuj_mape_firm()
    except Exception:
        pass


def sortuj_firmy(kryterium):
    if kryterium == 'nazwa':
        models.firmy.sort(key=lambda x: x['nazwa'].lower())
    else:
        models.firmy.sort(key=lambda x: x[kryterium])
    odswiez_firmy()


def sortuj_pracownikow(kryterium):
    models.pracownicy.sort(key=lambda x: x[kryterium])
    odswiez_pracownikow()


def sortuj_bazy(kryterium):
    models.bazy_klientow.sort(key=lambda x: x[kryterium])
    odswiez_bazy()


def odswiez_firmy():
    if view.listbox_firmy:
        view.listbox_firmy.delete(0, END)
        for f in models.firmy:
            view.listbox_firmy.insert(END, f" {f['nazwa']:<32} | ID: {f['id']}")
    if hasattr(view, 'listbox_f_pracownicy') and view.listbox_f_pracownicy:
        view.listbox_f_pracownicy.delete(0, END)
    if hasattr(view, 'listbox_f_klienci') and view.listbox_f_klienci:
        view.listbox_f_klienci.delete(0, END)
    if hasattr(view, 'lbl_f_wydarzenie_info') and view.lbl_f_wydarzenie_info:
        view.lbl_f_wydarzenie_info.config(text="Wydarzenie: Wybierz firmę z listy")


def dodaj_lub_edytuj_firme():
    nazwa = view.val_f_nazwa.get()
    lokalizacja = view.val_f_lokalizacja.get()
    wydarzenie = view.val_f_wydarzenie.get()
    try:
        podane_id = int(view.val_f_id.get())
    except ValueError:
        view.pokaz_komunikat("Błąd", "ID Firmy musi być liczbą!")
        return

    if not nazwa or not lokalizacja or not wydarzenie:
        view.pokaz_komunikat("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    wspolrzedne = scraping.pobierz_wspolrzedne(lokalizacja)

    if models.aktualna_firma_id is not None:
        for f in models.firmy:
            if f["id"] == models.aktualna_firma_id:
                f["id"] = podane_id
                f["nazwa"] = nazwa
                f["lokalizacja"] = lokalizacja
                f["wydarzenie"] = wydarzenie
                f["wspolrzedne"] = wspolrzedne
                break
        models.aktualna_firma_id = None
        view.pokaz_komunikat("Sukces", "Zaktualizowano dane firmy!")
    else:
        if any(f["id"] == podane_id for f in models.firmy):
            view.pokaz_komunikat("Błąd", "Firma o podanym ID już istnieje!")
            return
        models.firmy.append({
            "id": podane_id, "nazwa": nazwa, "lokalizacja": lokalizacja,
            "wydarzenie": wydarzenie, "wspolrzedne": wspolrzedne
        })
        view.pokaz_komunikat("Sukces", "Dodano nową firmę!")
    czysc_formularz_firmy()
    odswiez_firmy()


def usun_firme():
    try:
        idx = view.listbox_firmy.curselection()[0]
        id_usuwanej_firmy = models.firmy[idx]["id"]
        del models.firmy[idx]
        models.pracownicy = [p for p in models.pracownicy if p["firma_id"] != id_usuwanej_firmy]
        models.bazy_klientow = [b for b in models.bazy_klientow if b["firma_id"] != id_usuwanej_firmy]
        czysc_formularz_firmy()
        models.aktualna_firma_id = None
        odswiez_firmy()
        odswiez_pracownikow()
        odswiez_bazy()


        if map.aktualny_tryb == "firmy":
            map.pokaz_mape_firm()
        else:
            map.pokaz_mape_pracownikow()

        view.pokaz_komunikat("Sukces", "Usunięto firmę oraz przypisane do niej dane!")
    except IndexError:
        view.pokaz_komunikat("Wybór", "Wybierz firmę z listy do usunięcia!")


def laduj_do_edycji_firme():
    try:
        idx = view.listbox_firmy.curselection()[0]
        f = models.firmy[idx]
        models.aktualna_firma_id = f["id"]
        czysc_formularz_firmy()
        view.val_f_id.set(str(f["id"]))
        view.val_f_nazwa.set(f["nazwa"])
        view.val_f_lokalizacja.set(f["lokalizacja"])
        view.val_f_wydarzenie.set(f["wydarzenie"])
    except IndexError:
        view.pokaz_komunikat("Wybór", "Wybierz firmę z listy do edycji!")


def czysc_formularz_firmy():
    view.val_f_id.set("")
    view.val_f_nazwa.set("")
    view.val_f_lokalizacja.set("")
    view.val_f_wydarzenie.set("")


def pokaz_szczegoly_firmy(event=None):
    if not view.listbox_firmy.curselection():
        return
    idx = view.listbox_firmy.curselection()[0]
    firma = models.firmy[idx]
    view.lbl_f_wydarzenie_info.config(text=f"Wydarzenie: {firma['wydarzenie']}")

    view.listbox_f_pracownicy.delete(0, END)
    znalezieni_p = False
    for p in models.pracownicy:
        if p["firma_id"] == firma["id"]:
            view.listbox_f_pracownicy.insert(END, f" {p['imie']} {p['nazwisko']} ({p['lokalizacja']})")
            znalezieni_p = True
    if not znalezieni_p: view.listbox_f_pracownicy.insert(END, " Brak przypisanych pracowników.")

    view.listbox_f_klienci.delete(0, END)
    znalezieni_k = False
    for b in models.bazy_klientow:
        if b["firma_id"] == firma["id"]:
            view.listbox_f_klienci.insert(END, f" {b['nazwa']}")
            znalezieni_k = True
    if not znalezieni_k: view.listbox_f_klienci.insert(END, " Brak przypisanych klientów.")

    map.pokaz_mape_firm(wybrany_id=firma["id"])


def pokaz_szczegoly_pracownika(event=None):
    if not view.listbox_pracownicy.curselection():
        return
    idx = view.listbox_pracownicy.curselection()[0]
    pracownik = models.pracownicy[idx]
    map.pokaz_mape_pracownikow(wybrany_id=pracownik["id"])


def odswiez_pracownikow():
    if view.listbox_pracownicy:
        view.listbox_pracownicy.delete(0, END)
        for p in models.pracownicy:
            imie_nazw = f"{p['imie']} {p['nazwisko']}"
            view.listbox_pracownicy.insert(END, f" {imie_nazw:<25} | ID: {str(p['id']):<3} | ID firmy: {p['firma_id']}")


def dodaj_lub_edytuj_pracownika():
    imie, nazwisko, lokalizacja = view.val_p_imie.get(), view.val_p_nazwisko.get(), view.val_p_lokalizacja.get()
    try:
        podane_id, firma_id = int(view.val_p_id.get()), int(view.val_p_firma_id.get())
    except ValueError:
        view.pokaz_komunikat("Błąd", "ID Pracownika oraz ID Firmy muszą być liczbami!")
        return

    if not imie or not nazwisko or not lokalizacja:
        view.pokaz_komunikat("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    wspolrzedne = scraping.pobierz_wspolrzedne(lokalizacja)

    if models.aktualny_pracownik_id is not None:
        for p in models.pracownicy:
            if p["id"] == models.aktualny_pracownik_id:
                p["id"], p["imie"], p["nazwisko"] = podane_id, imie, nazwisko
                p["firma_id"], p["lokalizacja"], p["wspolrzedne"] = firma_id, lokalizacja, wspolrzedne
                break
        models.aktualny_pracownik_id = None
        view.pokaz_komunikat("Sukces", "Zaktualizowano dane pracownika!")
    else:
        if any(p["id"] == podane_id for p in models.pracownicy):
            view.pokaz_komunikat("Błąd", "Pracownik o podanym ID już istnieje!")
            return
        models.pracownicy.append({
            "id": podane_id, "imie": imie, "nazwisko": nazwisko,
            "firma_id": firma_id, "lokalizacja": lokalizacja, "wspolrzedne": wspolrzedne
        })
        view.pokaz_komunikat("Sukces", "Dodano nowego pracownika!")
    czysc_formularz_pracownika()
    odswiez_pracownikow()


def usun_pracownika():
    try:
        idx = view.listbox_pracownicy.curselection()[0]
        del models.pracownicy[idx]
        czysc_formularz_pracownika()
        models.aktualny_pracownik_id = None
        odswiez_pracownikow()


        if map.aktualny_tryb == "firmy":
            map.pokaz_mape_firm()
        else:
            map.pokaz_mape_pracownikow()

        view.pokaz_komunikat("Sukces", "Usunięto pracownika!")
    except IndexError:
        view.pokaz_komunikat("Wybór", "Wybierz pracownika z listy do usunięcia!")


def laduj_do_edycji_pracownika():
    try:
        idx = view.listbox_pracownicy.curselection()[0]
        p = models.pracownicy[idx]
        models.aktualny_pracownik_id = p["id"]
        czysc_formularz_pracownika()
        view.val_p_id.set(str(p["id"]))
        view.val_p_imie.set(p["imie"])
        view.val_p_nazwisko.set(p["nazwisko"])
        view.val_p_lokalizacja.set(p["lokalizacja"])
        view.val_p_firma_id.set(str(p["firma_id"]))
    except IndexError:
        view.pokaz_komunikat("Wybór", "Wybierz pracownika z listy do edycji!")


def czysc_formularz_pracownika():
    view.val_p_id.set("")
    view.val_p_imie.set("")
    view.val_p_nazwisko.set("")
    view.val_p_lokalizacja.set("")
    view.val_p_firma_id.set("")


def odswiez_bazy():
    if view.listbox_bazy:
        view.listbox_bazy.delete(0, END)
        for b in models.bazy_klientow:
            view.listbox_bazy.insert(END, f" {b['nazwa']:<30} | ID: {str(b['id']):<4} | ID firmy: {b['firma_id']}")
    if hasattr(view, 'listbox_b_pracownicy') and view.listbox_b_pracownicy:
        view.listbox_b_pracownicy.delete(0, END)
    if hasattr(view, 'lbl_b_firma_info') and view.lbl_b_firma_info:
        view.lbl_b_firma_info.config(text="Firma Marketingowa: Wybierz klienta z listy")
        view.lbl_b_wydarzenie_info.config(text="Wydarzenie: -")


def pokaz_szczegoly_klienta(event=None):
    if not view.listbox_bazy.curselection():
        return
    idx = view.listbox_bazy.curselection()[0]
    klient = models.bazy_klientow[idx]
    firma_mkt = None
    for f in models.firmy:
        if f["id"] == klient["firma_id"]:
            firma_mkt = f
            break
    if firma_mkt:
        view.lbl_b_firma_info.config(text=f"Firma Marketingowa: {firma_mkt['nazwa']}")
        view.lbl_b_wydarzenie_info.config(text=f"Wydarzenie: {firma_mkt['wydarzenie']}")
    else:
        view.lbl_b_firma_info.config(text="Firma Marketingowa: Brak przypisanej firmy")
        view.lbl_b_wydarzenie_info.config(text="Wydarzenie: -")
    view.listbox_b_pracownicy.delete(0, END)
    znalezieni = False
    for p in models.pracownicy:
        if p["firma_id"] == klient["firma_id"]:
            view.listbox_b_pracownicy.insert(END, f" {p['imie']} {p['nazwisko']} ({p['lokalizacja']})")
            znalezieni = True
    if not znalezieni:
        view.listbox_b_pracownicy.insert(END, " Brak powiązanych pracowników.")


def dodaj_lub_edytuj_baze():
    nazwa = view.val_b_nazwa.get()
    try:
        podane_id, firma_id = int(view.val_b_id.get()), int(view.val_b_firma_id.get())
    except ValueError:
        view.pokaz_komunikat("Błąd", "ID Klienta oraz ID firmy marketingowej muszą być liczbami!")
        return
    if not nazwa:
        view.pokaz_komunikat("Błąd", "Nazwa klienta nie może być pusta!")
        return
    if not any(f["id"] == firma_id for f in models.firmy):
        view.pokaz_komunikat("Błąd", f"Nie istnieje firma marketingowa o ID: {firma_id}!")
        return
    if models.aktualna_baza_id is not None:
        for b in models.bazy_klientow:
            if b["id"] == models.aktualna_baza_id:
                b["id"], b["nazwa"], b["firma_id"] = podane_id, nazwa, firma_id
                break
        models.aktualna_baza_id = None
        view.pokaz_komunikat("Sukces", "Zaktualizowano dane klienta!")
    else:
        if any(b["id"] == podane_id for b in models.bazy_klientow):
            view.pokaz_komunikat("Błąd", "Klient o podanym ID już istnieje w bazie!")
            return
        models.bazy_klientow.append({"id": podane_id, "nazwa": nazwa, "firma_id": firma_id})
        view.pokaz_komunikat("Sukces", "Dodano nowego klienta marketingowego!")
    czysc_formularz_baz()
    odswiez_bazy()


def usun_baze():
    try:
        idx = view.listbox_bazy.curselection()[0]
        del models.bazy_klientow[idx]
        czysc_formularz_baz()
        models.aktualna_baza_id = None
        odswiez_bazy()
        view.pokaz_komunikat("Sukces", "Usunięto klienta z bazy danych!")
    except IndexError:
        view.pokaz_komunikat("Błąd wyboru", "Wybierz klienta z listy do usunięcia!")


def laduj_do_edycji_baze():
    try:
        idx = view.listbox_bazy.curselection()[0]
        b = models.bazy_klientow[idx]
        models.aktualna_baza_id = b["id"]
        czysc_formularz_baz()
        view.val_b_id.set(str(b["id"]))
        view.val_b_nazwa.set(b["nazwa"])
        view.val_b_firma_id.set(str(b["firma_id"]))
    except IndexError:
        view.pokaz_komunikat("Błąd wyboru", "Wybierz klienta z listy do edycji!")


def czysc_formularz_baz():
    view.val_b_id.set("")
    view.val_b_nazwa.set("")
    view.val_b_firma_id.set("")


def aktywuj_mape_firm():
    map.pokaz_mape_firm()


def aktywuj_mape_pracownikow():
    map.pokaz_mape_pracownikow()


def filtruj_mape(event=None):
    miasto = view.entry_miasto_filtr.get().strip()
    if miasto and miasto != "Wpisz miasto...":
        if map.aktualny_tryb == "firmy":
            map.pokaz_mape_firm(miasto=miasto, wycentruj=True)
        else:
            map.pokaz_mape_pracownikow(miasto=miasto, wycentruj=True)


def resetuj_mape():
    view.entry_miasto_filtr.delete(0, END)
    view.entry_miasto_filtr.insert(0, "Wpisz miasto...")
    if map.aktualny_tryb == "firmy":
        map.pokaz_mape_firm()
    else:
        map.pokaz_mape_pracownikow()