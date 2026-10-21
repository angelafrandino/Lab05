import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label="Tipo", expand=True)
    input_marca = ft.TextField(label="Marca", expand=True)
    input_anno = ft.TextField(label="Anno", expand=True)

    txt_valore = ft.Text("0", size=20, weight=ft.FontWeight.BOLD, width=50, text_align=ft.TextAlign.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        lista_strumenti.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento

    # pulsanti per diminuire e aumentare il prezzo dello strumento che si sta inserendo
    def decrementa_valore(e):
        valore_attuale = int(txt_valore.value)
        if valore_attuale > 0:
            txt_valore.value = str(valore_attuale -5)
            txt_valore.update()

    def incrementa_valore(e):
        valor_attuale = int(txt_valore.value)
        txt_valore.value = str(valor_attuale +5)
        txt_valore.update()

    #aggiunta nuovo strumento
    def aggiungi_strumento(e):
        tipo = input_tipo.value.strip() if input_tipo.value else ""
        marca = input_marca.value.strip() if input_marca.value else ""
        anno_str = input_anno.value.strip() if input_anno.value else ""

        if not tipo or not marca or not anno_str:
            alert.show_alert("compilare tutti i campi")
            return

        try:
            anno_acquisto = int(anno_str)
        except ValueError:
            alert.show_alert("inserisci un valore numerico valido")
            return

        valore = float(txt_valore.value)
        deposito.aggiungi_strumento(tipo, marca, anno_acquisto, valore)

        #resetto i campi
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        txt_valore.value = "0"

        input_tipo.update()
        input_marca.update()
        input_anno.update()
        txt_valore.update()
        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    bottone_meno = ft.IconButton(ft.Icons.REMOVE, on_click=decrementa_valore)
    bottone_piu = ft.IconButton(ft.Icons.ADD, on_click=incrementa_valore)
    btn_aggiungi_strumento = ft.Button("aggiungi strumento", on_click=aggiungi_strumento)

    contatore_valore = ft.Row(
        controls=[
            bottone_meno,
            ft.Container(content=txt_valore, width=50),
            bottone_piu
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(
            controls=[input_tipo, input_marca, input_anno, contatore_valore],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(),
        ft.Row(
            controls=[btn_aggiungi_strumento],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
