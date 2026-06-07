import sys
from tkinter import *
from tkinter import ttk

import tkintermapview

import controller
import map
import models

root = Tk()
root.title("System Marketingowy - DB Client Manager")
root.configure(bg="#1e2124")


listbox_firmy, listbox_pracownicy, listbox_bazy = None, None, None
listbox_f_pracownicy, listbox_f_klienci = None, None
lbl_f_wydarzenie_info, lbl_b_firma_info, lbl_b_wydarzenie_info = None, None, None
entry_miasto_filtr = None

val_f_id, val_f_nazwa, val_f_lokalizacja, val_f_wydarzenie = StringVar(), StringVar(), StringVar(), StringVar()
val_p_id, val_p_imie, val_p_nazwisko, val_p_lokalizacja, val_p_firma_id = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
val_b_id, val_b_nazwa, val_b_firma_id = StringVar(), StringVar(), StringVar()

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background="#1e2124")
style.configure("TLabelframe", background="#2f3136", foreground="#ffffff")
style.configure("TLabelframe.Label", background="#2f3136", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
style.configure("TLabel", background="#2f3136", foreground="#ffffff", font=("Segoe UI", 10))

style.configure("TNotebook", background="#1e2124", borderwidth=0)
style.configure("TNotebook.Tab", background="#292b2f", foreground="#aaaaaa", padding=[20, 8],
                font=("Segoe UI", 10, "bold"), borderwidth=0)
style.map("TNotebook.Tab", background=[("selected", "#5865f2"), ("active", "#3ba55c")],
          foreground=[("selected", "#ffffff"), ("active", "#ffffff")])

style.configure("Blue.TButton", background="#5865f2", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
style.map("Blue.TButton", background=[("active", "#4752c4")])
style.configure("Green.TButton", background="#2e8b57", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
style.map("Green.TButton", background=[("active", "#246b43")])
style.configure("Red.TButton", background="#d32f2f", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
style.map("Red.TButton", background=[("active", "#b71c1c")])
style.configure("TButton", background="#4f545c", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
style.map("TButton", background=[("active", "#686d73")])


def pokaz_komunikat(tytul, wiadomosc):
    okno = Toplevel(root)
    okno.title(tytul)
    okno.geometry("400x160")
    okno.configure(bg="#2f3136")
    okno.transient(root)
    okno.grab_set()
    root.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - 200
    y = root.winfo_y() + (root.winfo_height() // 2) - 80
    okno.geometry(f"+{x}+{y}")
    Label(okno, text=wiadomosc, bg="#2f3136", fg="#ffffff", font=("Segoe UI", 11), wraplength=350, justify=CENTER).pack(
        expand=True, pady=10)
    ttk.Button(okno, text="OK", command=okno.destroy, style="Blue.TButton").pack(pady=10)


def pokaz_okno_markera(wydarzenie, firma, miejsce):
    okno = Toplevel(root)
    okno.title("Szczegóły Wydarzenia")
    okno.geometry("500x240")
    okno.configure(bg="#2f3136")
    okno.transient(root)
    okno.grab_set()
    root.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - 250
    y = root.winfo_y() + (root.winfo_height() // 2) - 120
    okno.geometry(f"+{x}+{y}")
    Label(okno, text=wydarzenie.upper(), bg="#2f3136", fg="#5865f2", font=("Segoe UI", 16, "bold"),
          wraplength=450).pack(pady=(20, 10))
    Label(okno, text=f"Organizuje: {firma}", bg="#2f3136", fg="#ffffff", font=("Segoe UI", 12)).pack(pady=5)
    Label(okno, text=f"Lokalizacja: {miejsce}", bg="#2f3136", fg="#aaaaaa", font=("Segoe UI", 11, "italic")).pack(
        pady=5)
    ttk.Button(okno, text="Zamknij", command=okno.destroy, style="Blue.TButton").pack(side=BOTTOM, pady=20)


def pokaz_okno_pracownika(imie_nazwisko, firma_nazwa, wydarzenie, miejsce):
    okno = Toplevel(root)
    okno.title("Szczegóły Pracownika")
    okno.geometry("500x280")
    okno.configure(bg="#2f3136")
    okno.transient(root)
    okno.grab_set()
    root.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - 250
    y = root.winfo_y() + (root.winfo_height() // 2) - 140
    okno.geometry(f"+{x}+{y}")
    Label(okno, text=imie_nazwisko.upper(), bg="#2f3136", fg="#2e8b57", font=("Segoe UI", 16, "bold"),
          wraplength=450).pack(pady=(20, 10))
    Label(okno, text=f"Pracuje dla: {firma_nazwa}", bg="#2f3136", fg="#ffffff", font=("Segoe UI", 12)).pack(pady=2)
    Label(okno, text=f"Obsługuje wydarzenie: {wydarzenie}", bg="#2f3136", fg="#00b0f4", font=("Segoe UI", 11)).pack(
        pady=2)
    Label(okno, text=f"Lokalizacja: {miejsce}", bg="#2f3136", fg="#aaaaaa", font=("Segoe UI", 11, "italic")).pack(
        pady=10)
    ttk.Button(okno, text="Zamknij", command=okno.destroy, style="Green.TButton").pack(side=BOTTOM, pady=20)


def wycentruj_okno(w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = int((ws / 2) - (w / 2))
    y = int((hs / 2) - (h / 2))
    root.geometry(f"{w}x{h}+{x}+{y}")


def inicjalizuj_okno_logowania():
    global ramka_logowania, entry_login, entry_haslo
    wycentruj_okno(450, 400)
    ramka_logowania = Frame(root, bg="#1e2124")
    ramka_logowania.pack(expand=True, fill=BOTH)
    Frame(ramka_logowania, bg="#1e2124", height=40).pack()
    Label(ramka_logowania, text="Logowanie do Systemu", bg="#1e2124", fg="#ffffff", font=("Segoe UI", 18, "bold")).pack(
        pady=20)

    Label(ramka_logowania, text="Login:", bg="#1e2124", fg="#ffffff", font=("Segoe UI", 11)).pack(pady=(10, 0))
    entry_login = ttk.Entry(ramka_logowania, font=("Segoe UI", 11), width=25, justify=CENTER)
    entry_login.pack(pady=5)
    entry_login.insert(0, models.USER_LOGIN)

    Label(ramka_logowania, text="Hasło:", bg="#1e2124", fg="#ffffff", font=("Segoe UI", 11)).pack(pady=(10, 0))
    entry_haslo = ttk.Entry(ramka_logowania, show="*", font=("Segoe UI", 11), width=25, justify=CENTER)
    entry_haslo.pack(pady=5)
    entry_haslo.insert(0, models.USER_PASS)

    ttk.Button(ramka_logowania, text="Zaloguj się", command=controller.sprawdz_logowanie, style="Blue.TButton").pack(
        pady=30, ipadx=20, ipady=5)
    root.bind('<Return>', controller.sprawdz_logowanie)


def rozszerz_i_uruchom_aplikacje():
    root.unbind('<Return>')
    wycentruj_okno(1450, 850)
    inicjalizuj_glowne_okno()


def inicjalizuj_glowne_okno():
    global listbox_firmy, listbox_pracownicy, listbox_bazy, listbox_f_pracownicy, listbox_f_klienci, lbl_f_wydarzenie_info
    global listbox_b_pracownicy, lbl_b_firma_info, lbl_b_wydarzenie_info, entry_miasto_filtr

    ramka_glowna = Frame(root, bg="#1e2124")
    ramka_glowna.pack(fill=BOTH, expand=True, padx=15, pady=15)

    ramka_zarzadzania = Frame(ramka_glowna, bg="#1e2124", width=540)
    ramka_zarzadzania.pack_propagate(False)
    ramka_zarzadzania.pack(side=LEFT, fill=Y, padx=(0, 15))

    notebook = ttk.Notebook(ramka_zarzadzania)
    notebook.pack(fill=BOTH, expand=True)
    notebook.bind("<<NotebookTabChanged>>", controller.zmieniono_zakladke)

    tab_firmy = ttk.Frame(notebook)
    tab_pracownicy = ttk.Frame(notebook)
    tab_bazy = ttk.Frame(notebook)
    notebook.add(tab_firmy, text="Firmy")
    notebook.add(tab_pracownicy, text="Pracownicy")
    notebook.add(tab_bazy, text="Baza Klientów")





    lf_firmy = ttk.LabelFrame(tab_firmy, text=" Zarządzanie Firmami ")
    lf_firmy.pack(fill=BOTH, expand=True, padx=10, pady=10)

    FrameFormularzFirmy = Frame(lf_firmy, bg="#2f3136")
    FrameFormularzFirmy.pack(fill=X, padx=15, pady=15)
    FrameFormularzFirmy.columnconfigure(1, weight=1)
    ttk.Label(FrameFormularzFirmy, text="ID Firmy:").grid(row=0, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzFirmy, textvariable=val_f_id).grid(row=0, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(FrameFormularzFirmy, text="Nazwa:").grid(row=1, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzFirmy, textvariable=val_f_nazwa).grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(FrameFormularzFirmy, text="Lokalizacja:").grid(row=2, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzFirmy, textvariable=val_f_lokalizacja).grid(row=2, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(FrameFormularzFirmy, text="Wydarzenie:").grid(row=3, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzFirmy, textvariable=val_f_wydarzenie).grid(row=3, column=1, sticky="ew", pady=5, padx=5)

    FramePrzyciskiFirmy = Frame(lf_firmy, bg="#2f3136")
    FramePrzyciskiFirmy.pack(fill=X, padx=15, pady=5)
    ttk.Button(FramePrzyciskiFirmy, text="Dodaj / Popraw", command=controller.dodaj_lub_edytuj_firme,
               style="Blue.TButton").pack(side=LEFT, expand=True, fill=X, padx=2)
    ttk.Button(FramePrzyciskiFirmy, text="Edytuj", command=controller.laduj_do_edycji_firme,
               style="Green.TButton").pack(side=LEFT, expand=True, fill=X, padx=2)
    ttk.Button(FramePrzyciskiFirmy, text="Usuń", command=controller.usun_firme, style="Red.TButton").pack(side=LEFT,
                                                                                                          expand=True,
                                                                                                          fill=X,
                                                                                                          padx=2)

    FrameSortFirmy = Frame(lf_firmy, bg="#2f3136")
    FrameSortFirmy.pack(fill=X, padx=15, pady=(0, 5))
    Label(FrameSortFirmy, text="Sortuj listę po:", bg="#2f3136", fg="#aaaaaa", font=("Segoe UI", 9, "italic")).pack(
        side=LEFT, padx=(0, 5))
    ttk.Button(FrameSortFirmy, text="ID Firmy", command=lambda: controller.sortuj_firmy('id'), style="TButton").pack(
        side=LEFT, expand=True, fill=X, padx=2)
    ttk.Button(FrameSortFirmy, text="Nazwa", command=lambda: controller.sortuj_firmy('nazwa'), style="TButton").pack(
        side=LEFT, expand=True, fill=X, padx=2)

    listbox_firmy = Listbox(lf_firmy, bg="#202225", fg="#ffffff", selectbackground="#5865f2", font=("Consolas", 10),
                            height=8, borderwidth=0, highlightthickness=1)
    listbox_firmy.pack(fill=BOTH, expand=True, padx=15, pady=(5, 10))
    listbox_firmy.bind("<<ListboxSelect>>", controller.pokaz_szczegoly_firmy)

    lbl_f_wydarzenie_info = Label(lf_firmy, text="Wydarzenie: Wybierz firmę z listy", bg="#2f3136", fg="#00b0f4",
                                  font=("Segoe UI", 11, "bold"))
    lbl_f_wydarzenie_info.pack(anchor=W, padx=15, pady=(0, 10))

    frame_szczegoly_firmy = Frame(lf_firmy, bg="#2f3136")
    frame_szczegoly_firmy.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))
    frame_f_pracownicy = Frame(frame_szczegoly_firmy, bg="#2f3136")
    frame_f_pracownicy.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
    Label(frame_f_pracownicy, text="Pracownicy przypisani:", bg="#2f3136", fg="#aaaaaa",
          font=("Segoe UI", 9, "italic")).pack(anchor=W)
    listbox_f_pracownicy = Listbox(frame_f_pracownicy, bg="#202225", fg="#aaaaaa", selectbackground="#5865f2",
                                   font=("Consolas", 10), height=4, borderwidth=0, highlightthickness=1)
    listbox_f_pracownicy.pack(fill=BOTH, expand=True)

    frame_f_klienci = Frame(frame_szczegoly_firmy, bg="#2f3136")
    frame_f_klienci.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
    Label(frame_f_klienci, text="Obsługiwani klienci:", bg="#2f3136", fg="#aaaaaa",
          font=("Segoe UI", 9, "italic")).pack(anchor=W)
    listbox_f_klienci = Listbox(frame_f_klienci, bg="#202225", fg="#aaaaaa", selectbackground="#5865f2",
                                font=("Consolas", 10), height=4, borderwidth=0, highlightthickness=1)
    listbox_f_klienci.pack(fill=BOTH, expand=True)






    lf_pracownicy = ttk.LabelFrame(tab_pracownicy, text=" Zarządzanie Pracownikami ")
    lf_pracownicy.pack(fill=BOTH, expand=True, padx=10, pady=10)

    FrameFormularzPracownicy = Frame(lf_pracownicy, bg="#2f3136")
    FrameFormularzPracownicy.pack(fill=X, padx=15, pady=15)
    FrameFormularzPracownicy.columnconfigure(1, weight=1)
    ttk.Label(FrameFormularzPracownicy, text="ID Pracownika:").grid(row=0, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzPracownicy, textvariable=val_p_id).grid(row=0, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(FrameFormularzPracownicy, text="Imię:").grid(row=1, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzPracownicy, textvariable=val_p_imie).grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(FrameFormularzPracownicy, text="Nazwisko:").grid(row=2, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzPracownicy, textvariable=val_p_nazwisko).grid(row=2, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(FrameFormularzPracownicy, text="Lokalizacja:").grid(row=3, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzPracownicy, textvariable=val_p_lokalizacja).grid(row=3, column=1, sticky="ew", pady=5,
                                                                             padx=5)
    ttk.Label(FrameFormularzPracownicy, text="ID firmy marketingowej:").grid(row=4, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzPracownicy, textvariable=val_p_firma_id).grid(row=4, column=1, sticky="ew", pady=5, padx=5)

    FramePrzyciskiPracownicy = Frame(lf_pracownicy, bg="#2f3136")
    FramePrzyciskiPracownicy.pack(fill=X, padx=15, pady=5)
    ttk.Button(FramePrzyciskiPracownicy, text="Dodaj / Popraw", command=controller.dodaj_lub_edytuj_pracownika,
               style="Blue.TButton").pack(side=LEFT, expand=True, fill=X, padx=2)
    ttk.Button(FramePrzyciskiPracownicy, text="Edytuj", command=controller.laduj_do_edycji_pracownika,
               style="Green.TButton").pack(side=LEFT, expand=True, fill=X, padx=2)
    ttk.Button(FramePrzyciskiPracownicy, text="Usuń", command=controller.usun_pracownika, style="Red.TButton").pack(
        side=LEFT, expand=True, fill=X, padx=2)

    FrameSortPracownicy = Frame(lf_pracownicy, bg="#2f3136")
    FrameSortPracownicy.pack(fill=X, padx=15, pady=(0, 5))
    Label(FrameSortPracownicy, text="Sortuj listę po:", bg="#2f3136", fg="#aaaaaa",
          font=("Segoe UI", 9, "italic")).pack(side=LEFT, padx=(0, 5))
    ttk.Button(FrameSortPracownicy, text="ID Pracownika", command=lambda: controller.sortuj_pracownikow('id'),
               style="TButton").pack(side=LEFT, expand=True, fill=X, padx=2)
    ttk.Button(FrameSortPracownicy, text="ID firmy marketingowej",
               command=lambda: controller.sortuj_pracownikow('firma_id'), style="TButton").pack(side=LEFT, expand=True,
                                                                                                fill=X, padx=2)

    listbox_pracownicy = Listbox(lf_pracownicy, bg="#202225", fg="#ffffff", selectbackground="#5865f2",
                                 font=("Consolas", 10), borderwidth=0, highlightthickness=1)
    listbox_pracownicy.pack(fill=BOTH, expand=True, padx=15, pady=15)
    listbox_pracownicy.bind("<<ListboxSelect>>", controller.pokaz_szczegoly_pracownika)





    lf_bazy = ttk.LabelFrame(tab_bazy, text=" Baza Klientów Marketingowych ")
    lf_bazy.pack(fill=BOTH, expand=True, padx=10, pady=10)

    FrameFormularzBazy = Frame(lf_bazy, bg="#2f3136")
    FrameFormularzBazy.pack(fill=X, padx=15, pady=15)
    FrameFormularzBazy.columnconfigure(1, weight=1)
    ttk.Label(FrameFormularzBazy, text="ID Klienta:").grid(row=0, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzBazy, textvariable=val_b_id).grid(row=0, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(FrameFormularzBazy, text="Nazwa Klienta:").grid(row=1, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzBazy, textvariable=val_b_nazwa).grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(FrameFormularzBazy, text="ID firmy marketingowej:").grid(row=2, column=0, sticky=W, pady=5, padx=5)
    ttk.Entry(FrameFormularzBazy, textvariable=val_b_firma_id).grid(row=2, column=1, sticky="ew", pady=5, padx=5)

    FramePrzyciskiBazy = Frame(lf_bazy, bg="#2f3136")
    FramePrzyciskiBazy.pack(fill=X, padx=15, pady=5)
    ttk.Button(FramePrzyciskiBazy, text="Dodaj / Popraw", command=controller.dodaj_lub_edytuj_baze,
               style="Blue.TButton").pack(side=LEFT, expand=True, fill=X, padx=2)
    ttk.Button(FramePrzyciskiBazy, text="Edytuj", command=controller.laduj_do_edycji_baze, style="Green.TButton").pack(
        side=LEFT, expand=True, fill=X, padx=2)
    ttk.Button(FramePrzyciskiBazy, text="Usuń", command=controller.usun_baze, style="Red.TButton").pack(side=LEFT,
                                                                                                        expand=True,
                                                                                                        fill=X, padx=2)

    FrameSortBazy = Frame(lf_bazy, bg="#2f3136")
    FrameSortBazy.pack(fill=X, padx=15, pady=(0, 5))
    Label(FrameSortBazy, text="Sortuj listę po:", bg="#2f3136", fg="#aaaaaa", font=("Segoe UI", 9, "italic")).pack(
        side=LEFT, padx=(0, 5))
    ttk.Button(FrameSortBazy, text="ID Klienta", command=lambda: controller.sortuj_bazy('id'), style="TButton").pack(
        side=LEFT, expand=True, fill=X, padx=2)
    ttk.Button(FrameSortBazy, text="ID firmy marketingowej", command=lambda: controller.sortuj_bazy('firma_id'),
               style="TButton").pack(side=LEFT, expand=True, fill=X, padx=2)

    listbox_bazy = Listbox(lf_bazy, bg="#202225", fg="#ffffff", selectbackground="#5865f2", font=("Consolas", 10),
                           height=6, borderwidth=0, highlightthickness=1)
    listbox_bazy.pack(fill=BOTH, expand=True, padx=15, pady=5)
    listbox_bazy.bind("<<ListboxSelect>>", controller.pokaz_szczegoly_klienta)

    lbl_b_firma_info = Label(lf_bazy, text="Firma Marketingowa: Wybierz klienta z listy", bg="#2f3136", fg="#00b0f4",
                             font=("Segoe UI", 11, "bold"))
    lbl_b_firma_info.pack(anchor=W, padx=15, pady=(5, 0))
    lbl_b_wydarzenie_info = Label(lf_bazy, text="Wydarzenie: -", bg="#2f3136", fg="#aaaaaa", font=("Segoe UI", 10))
    lbl_b_wydarzenie_info.pack(anchor=W, padx=15, pady=(2, 0))

    Label(lf_bazy, text="Pracownicy obsługujący:", bg="#2f3136", fg="#aaaaaa", font=("Segoe UI", 9, "italic")).pack(
        anchor=W, padx=15, pady=(5, 0))
    listbox_b_pracownicy = Listbox(lf_bazy, bg="#202225", fg="#aaaaaa", selectbackground="#5865f2",
                                   font=("Consolas", 10), height=3, borderwidth=0, highlightthickness=1)
    listbox_b_pracownicy.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))





    ramka_mapy = Frame(ramka_glowna, bg="#2f3136")
    ramka_mapy.pack(side=RIGHT, fill=BOTH, expand=True)

    map_top_frame = Frame(ramka_mapy, bg="#2f3136")
    map_top_frame.pack(fill=X, padx=5, pady=10)

    ttk.Button(map_top_frame, text="Mapa Wydarzeń", command=controller.aktywuj_mape_firm, style="TButton").pack(side=LEFT,
                                                                                                            padx=2)
    ttk.Button(map_top_frame, text="Mapa Pracowników", command=controller.aktywuj_mape_pracownikow,
               style="TButton").pack(side=LEFT, padx=2)

    separator = ttk.Separator(map_top_frame, orient="vertical")
    separator.pack(side=LEFT, fill=Y, padx=15)

    entry_miasto_filtr = ttk.Entry(map_top_frame, width=20)
    entry_miasto_filtr.pack(side=LEFT, fill=X, expand=True, padx=5)
    entry_miasto_filtr.insert(0, "Wpisz miasto...")
    entry_miasto_filtr.bind("<FocusIn>", lambda e: entry_miasto_filtr.delete(0, "end"))
    entry_miasto_filtr.bind("<Return>", controller.filtruj_mape)

    ttk.Button(map_top_frame, text="Filtruj", command=controller.filtruj_mape, style="TButton").pack(side=LEFT, padx=2)
    ttk.Button(map_top_frame, text="Reset", command=controller.resetuj_mape, style="TButton").pack(side=LEFT, padx=2)

    info_frame = Frame(ramka_mapy, bg="#2f3136")
    info_frame.pack(fill=X, padx=10, pady=(0, 5))
    Label(info_frame, text="Kliknij na wygenerowany znacznik na mapie, aby dowiedzieć się więcej o obiekcie.",
          bg="#2f3136", fg="#00b0f4", font=("Segoe UI", 12, "bold")).pack(expand=True, pady=5)

    widget_mapy = tkintermapview.TkinterMapView(ramka_mapy, width=800, height=600, corner_radius=10)
    widget_mapy.pack(fill=BOTH, expand=True, padx=10, pady=(5, 10))

    map.init_map(widget_mapy)

    controller.odswiez_firmy()
    controller.odswiez_pracownikow()
    controller.odswiez_bazy()

    map.pokaz_mape_firm()


controller.przypisz_widok(sys.modules[__name__])
inicjalizuj_okno_logowania()

root.mainloop()