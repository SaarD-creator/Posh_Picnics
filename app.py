"""Posh PicNic – mock-up van het bestelsysteem vanuit de receptionist (WS04).

Volgens het projectmandaat:
- Een klant belt; de receptionist beschrijft de tien standaardmenu's.
- Boekt de klant, dan registreert de receptionist de klantgegevens
  (naam, adres, telefoonnummer…) en de picknick (plaats, datum, tijd,
  standaardmenu, totaalprijs) op een contract.
- De standaardprijs geldt op weekdagen; op zaterdag en zondag komt er
  10 % weekendtoeslag bij.
- Eén contract kan meerdere picknicks bevatten, zolang leverdatum en
  tijdstip hetzelfde zijn.
- Een speciaal verzoek noteert de receptionist en geeft hij door aan de
  menumanager; daarna belt hij de klant terug met de prijs.

Werkend in deze mock-up: hoofdpagina en "Menu's raadplegen"
(menukaart + prijsberekening). De andere knoppen zijn nog niet uitgewerkt.

Start lokaal met:  streamlit run app.py
"""

from datetime import date, time, timedelta
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Basisinstellingen
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Posh PicNic – Receptie", page_icon="🧺", layout="wide")

LOGO = Path(__file__).parent / "assets" / "logo.png"

GROEN = "#2F4A3A"
ROZE = "#E8A9A0"
ROZE_LICHT = "#F6DCD7"
CREME = "#FBF6EF"

WEEKENDTOESLAG = 0.10        # 10 % extra op zaterdag en zondag
LOYALITEITSKORTING = 10.00   # 10 punten geven automatisch € 10 korting

# ---------------------------------------------------------------------------
# Opmaak: groen en roze uit het logo, met het geruite (gingham) patroon
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cardo:wght@400;700&family=Montserrat:wght@400;600&display=swap');

    html, body, [class*="css"], .stMarkdown, p, li, label {{
        font-family: 'Montserrat', sans-serif;
        color: #24382C;
    }}
    h1, h2, h3, h4 {{
        font-family: 'Cardo', serif !important;
        color: {GROEN} !important;
    }}

    .stApp {{
        background-color: {CREME};
        background-image:
            linear-gradient(90deg, rgba(232,169,160,.18) 50%, transparent 50%),
            linear-gradient(rgba(232,169,160,.18) 50%, transparent 50%);
        background-size: 48px 48px;
    }}
    .block-container {{
        background: {CREME};
        border-radius: 18px;
        padding: 2rem 2.5rem 3rem 2.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 4px 24px rgba(47,74,58,.10);
        max-width: 1100px;
    }}

    .gingham {{
        height: 22px;
        border-radius: 6px;
        margin: .5rem 0 1.5rem 0;
        background-color: {CREME};
        background-image:
            linear-gradient(90deg, rgba(200,102,79,.45) 50%, transparent 50%),
            linear-gradient(rgba(200,102,79,.45) 50%, transparent 50%);
        background-size: 22px 22px;
        border: 2px solid {ROZE};
    }}

    .rolbalk {{
        text-align: center;
        font-size: 1.05rem;
        margin-bottom: .5rem;
    }}
    .rolbalk span {{
        background: {GROEN};
        color: #FFFFFF;
        border-radius: 999px;
        padding: .25rem .9rem;
        font-size: .85rem;
        font-weight: 600;
    }}
    .sectie {{
        font-family: 'Cardo', serif;
        font-size: 1.6rem;
        color: {GROEN};
        border-bottom: 3px solid {ROZE};
        padding-bottom: .2rem;
        margin: 1.4rem 0 .4rem 0;
    }}
    .sectie-uitleg {{
        font-size: .9rem;
        color: #5B6B60;
        margin-bottom: .8rem;
    }}

    .stButton > button {{
        width: 100%;
        min-height: 3.4rem;
        background: {GROEN};
        color: #FFFFFF;
        border: 2px solid {GROEN};
        border-radius: 12px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        box-shadow: 0 3px 0 {ROZE};
        transition: all .15s ease-in-out;
    }}
    .stButton > button:hover {{
        background: {ROZE};
        color: {GROEN};
        border-color: {ROZE};
    }}
    .stButton > button p {{ color: inherit; }}

    .stTabs [data-baseweb="tab"] {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        color: {GROEN};
    }}

    .menukaart {{
        background: #FFFFFF;
        border: 2px solid {ROZE_LICHT};
        border-top: 8px solid {GROEN};
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        min-height: 250px;
    }}
    .menukaart h4 {{ margin: 0 0 .3rem 0; font-size: 1.35rem; }}
    .menukaart ul {{ margin: .4rem 0 .6rem 1.1rem; padding: 0; }}
    .menukaart li {{ font-size: .9rem; margin-bottom: .1rem; }}
    .prijs {{ font-weight: 600; color: {GROEN}; }}
    .prijsinfo {{ font-size: .85rem; color: #7A6A5A; }}
    .label {{
        display: inline-block;
        background: {ROZE_LICHT};
        color: {GROEN};
        border-radius: 999px;
        padding: .1rem .6rem;
        font-size: .75rem;
        font-weight: 600;
        margin-right: .3rem;
    }}
    .infobalk {{
        background: {ROZE_LICHT};
        border-left: 6px solid {GROEN};
        border-radius: 10px;
        padding: .8rem 1rem;
        margin: .8rem 0 1.2rem 0;
        font-size: .92rem;
    }}

    .totaalkader {{
        background: #FFFFFF;
        border: 2px solid {ROZE};
        border-radius: 14px;
        padding: 1rem 1.3rem;
    }}
    .totaalkader table {{ width: 100%; border-collapse: collapse; font-size: .95rem; }}
    .totaalkader td {{ padding: .3rem 0; }}
    .totaalkader td.bedrag {{ text-align: right; white-space: nowrap; padding-left: 1rem; }}
    .totaalkader tr.totaal td {{
        border-top: 2px solid {GROEN};
        font-weight: 700;
        font-size: 1.15rem;
        color: {GROEN};
        padding-top: .5rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Voorbeelddata: de tien standaardmenu's (fictieve inhoud en prijzen)
# Prijs = standaardprijs per picknick op een weekdag.
# ---------------------------------------------------------------------------
MENUS = [
    {"nr": 1, "naam": "Klassieke Picknick", "prijs": 320.00, "labels": [],
     "beschrijving": "De tijdloze favoriet voor elk gezelschap.",
     "inhoud": ["Belegde broodjes (ham, kaas, kip)", "Huisgemaakte koolsla", "Seizoensfruit", "Verse limonade"]},
    {"nr": 2, "naam": "Mediterraanse Zomer", "prijs": 390.00, "labels": ["vegetarische optie"],
     "beschrijving": "Zonnige smaken uit het zuiden.",
     "inhoud": ["Focaccia met tapenade", "Tomaat-mozzarella", "Gegrilde groenten", "Tiramisu in een potje"]},
    {"nr": 3, "naam": "Vegetarisch Tuinfeest", "prijs": 340.00, "labels": ["vegetarisch"],
     "beschrijving": "Kleurrijk, fris en volledig vleesloos.",
     "inhoud": ["Quiche met spinazie en feta", "Couscoussalade", "Groentesticks met hummus", "Fruitspiesjes"]},
    {"nr": 4, "naam": "Kinderfeestje", "prijs": 260.00, "labels": ["kinderen"],
     "beschrijving": "Speels en lekker voor de kleinste gasten.",
     "inhoud": ["Mini-sandwiches", "Kippennuggets (koud)", "Fruitsalade", "Chocolademelk"]},
    {"nr": 5, "naam": "Brunch in het Gras", "prijs": 360.00, "labels": [],
     "beschrijving": "Een uitgebreide brunch in open lucht.",
     "inhoud": ["Croissants en pistolets", "Gerookte zalm en roomkaas", "Yoghurt met granola", "Vers sinaasappelsap"]},
    {"nr": 6, "naam": "Zomerse Grillpicknick", "prijs": 420.00, "labels": [],
     "beschrijving": "Koude grillgerechten, klaar om te delen.",
     "inhoud": ["Kippenbouten en spareribs (koud)", "Aardappelsalade", "Maïskolfjes", "Ijsthee"]},
    {"nr": 7, "naam": "Luxe Champagnepicknick", "prijs": 650.00, "labels": ["luxe"],
     "beschrijving": "Voor de speciale momenten, met bubbels.",
     "inhoud": ["Oesters en zeevruchten", "Fijne kazen en charcuterie", "Macarons", "Champagne"]},
    {"nr": 8, "naam": "Business Lunch", "prijs": 240.00, "labels": ["zakelijk"],
     "beschrijving": "Verzorgde lunch voor teams en vergaderingen.",
     "inhoud": ["Wraps en clubsandwiches", "Salade van het seizoen", "Dessert van de chef", "Water en koffie"]},
    {"nr": 9, "naam": "Vegan Groen", "prijs": 340.00, "labels": ["vegan"],
     "beschrijving": "Volledig plantaardig en vol smaak.",
     "inhoud": ["Falafel met tahinsaus", "Quinoasalade", "Groentechips", "Havermelk-smoothie"]},
    {"nr": 10, "naam": "Seizoenspicknick", "prijs": 400.00, "labels": ["wisselend"],
     "beschrijving": "Elke maand andere seizoensproducten.",
     "inhoud": ["Verrassingsgerechten van de chef", "Seizoenssoep in een thermos", "Taart van het seizoen", "Huisgemaakte drank"]},
]
MENU_PER_NR = {m["nr"]: m for m in MENUS}

DAGEN = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]


# ---------------------------------------------------------------------------
# Hulpfuncties
# ---------------------------------------------------------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "home"


def ga_naar(pagina: str) -> None:
    st.session_state.pagina = pagina


def nog_niet_beschikbaar(functie: str) -> None:
    st.toast(f"‘{functie}’ is nog niet beschikbaar in deze mock-up.", icon="🧺")


def euro(bedrag: float) -> str:
    return f"€ {bedrag:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def is_weekend(dag: date) -> bool:
    return dag.weekday() >= 5  # 5 = zaterdag, 6 = zondag


def koptekst(titel: str | None = None, logo_breedte: int = 260) -> None:
    _, midden, _ = st.columns([1, 2, 1])
    with midden:
        if LOGO.exists():
            _, logo_kolom, _ = st.columns([1, 3, 1])
            with logo_kolom:
                st.image(str(LOGO), width=logo_breedte)
        else:
            st.markdown("<h1 style='text-align:center'>Posh PicNic</h1>", unsafe_allow_html=True)
    st.markdown("<div class='rolbalk'><span>Receptie · ingelogd als receptionist</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='gingham'></div>", unsafe_allow_html=True)
    if titel:
        st.markdown(f"<h2 style='text-align:center'>{titel}</h2>", unsafe_allow_html=True)


def sectie(titel: str, uitleg: str) -> None:
    st.markdown(f"<div class='sectie'>{titel}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sectie-uitleg'>{uitleg}</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Pagina: overzicht van de receptionist
# ---------------------------------------------------------------------------
def toon_home() -> None:
    koptekst()

    sectie(
        "Klant aan de lijn",
        "Een klant belt: beschrijf de standaardmenu's en zet de picknick op een contract.",
    )
    k1, k2, k3 = st.columns(3)
    with k1:
        st.button("Menu's raadplegen", icon=":material/restaurant_menu:",
                  on_click=ga_naar, args=("menu",), width="stretch")
        st.caption("Menu's beschrijven en de totaalprijs berekenen.")
    with k2:
        st.button("Klantgegevens registreren", icon=":material/person_add:",
                  on_click=nog_niet_beschikbaar, args=("Klantgegevens registreren",), width="stretch")
        st.caption("Naam, adres, telefoonnummer… van de klant.")
    with k3:
        st.button("Contract opstellen", icon=":material/contract:",
                  on_click=nog_niet_beschikbaar, args=("Contract opstellen",), width="stretch")
        st.caption("Plaats, datum, tijd, standaardmenu en totaalprijs.")

    sectie(
        "Speciale verzoeken",
        "Iets speciaals erbij, zoals een verjaardagstaart, een kaart of een cadeau?",
    )
    s1, s2 = st.columns(2)
    with s1:
        st.button("Speciaal verzoek registreren", icon=":material/cake:",
                  on_click=nog_niet_beschikbaar, args=("Speciaal verzoek registreren",), width="stretch")
        st.caption("De wens van de klant noteren en doorgeven aan de menumanager.")
    with s2:
        st.button("Prijsvoorstellen opvolgen", icon=":material/request_quote:",
                  on_click=nog_niet_beschikbaar, args=("Prijsvoorstellen opvolgen",), width="stretch")
        st.caption("De klant terugbellen met de prijs: aanvaard of aanpassing gevraagd.")

    st.markdown("<div class='gingham' style='margin-top:2rem'></div>", unsafe_allow_html=True)
    st.caption("Mock-up voor WS04 · fictieve gegevens")


# ---------------------------------------------------------------------------
# Pagina: menu's raadplegen (menukaart + prijsberekening)
# ---------------------------------------------------------------------------
def toon_menukaart() -> None:
    st.markdown(
        "<div class='infobalk'>"
        "<b>Te vermelden aan de klant</b><br>"
        "• De standaardprijs geldt op weekdagen (maandag tot vrijdag). "
        "Op zaterdag en zondag komt er 10 % weekendtoeslag bij.<br>"
        "• Eén contract kan meerdere picknicks bevatten, zolang leverdatum en tijdstip hetzelfde zijn.<br>"
        "• Iets speciaals erbij? Registreer een speciaal verzoek voor de menumanager."
        "</div>",
        unsafe_allow_html=True,
    )

    zoek_kolom, schakel_kolom = st.columns([2, 1])
    with zoek_kolom:
        zoek = st.text_input("Zoek een menu", placeholder="bv. vegan, brunch, kinderen…")
    with schakel_kolom:
        st.write("")
        weekend = st.toggle("Toon weekendprijzen")

    term = zoek.lower().strip()
    gefilterd = [
        m for m in MENUS
        if not term
        or term in m["naam"].lower()
        or term in m["beschrijving"].lower()
        or any(term in label for label in m["labels"])
        or any(term in item.lower() for item in m["inhoud"])
    ]

    if not gefilterd:
        st.info("Geen menu gevonden. Probeer een andere zoekterm.")
        return

    kolommen = st.columns(2)
    for i, menu in enumerate(gefilterd):
        prijs = menu["prijs"] * (1 + WEEKENDTOESLAG) if weekend else menu["prijs"]
        uitleg = "per picknick, weekend (+10 %)" if weekend else "per picknick, standaardprijs weekdag"
        labels = "".join(f"<span class='label'>{l}</span>" for l in menu["labels"])
        inhoud = "".join(f"<li>{item}</li>" for item in menu["inhoud"])
        with kolommen[i % 2]:
            st.markdown(
                f"<div class='menukaart'>"
                f"<h4>Menu {menu['nr']} · {menu['naam']}</h4>"
                f"{labels}"
                f"<p style='margin:.5rem 0 0 0'><i>{menu['beschrijving']}</i></p>"
                f"<ul>{inhoud}</ul>"
                f"<span class='prijs'>{euro(prijs)}</span> "
                f"<span class='prijsinfo'>{uitleg}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )


def toon_prijsberekening() -> None:
    st.markdown(
        "<div class='infobalk'>"
        "Bereken tijdens het gesprek de totaalprijs voor de klant. "
        "Eén contract geldt voor één leverdatum en één tijdstip."
        "</div>",
        unsafe_allow_html=True,
    )

    invoer, resultaat = st.columns([3, 2], gap="large")

    with invoer:
        d1, d2 = st.columns(2)
        with d1:
            leverdatum = st.date_input(
                "Leverdatum",
                value=date.today() + timedelta(days=7),
                min_value=date.today(),
                format="DD/MM/YYYY",
            )
        with d2:
            tijdstip = st.time_input("Tijdstip", value=time(12, 0), step=timedelta(minutes=30))

        gekozen = st.multiselect(
            "Gekozen standaardmenu's",
            options=[m["nr"] for m in MENUS],
            format_func=lambda nr: f"Menu {nr} · {MENU_PER_NR[nr]['naam']} ({euro(MENU_PER_NR[nr]['prijs'])})",
            placeholder="Kies één of meer menu's",
        )

        aantallen = {}
        for nr in gekozen:
            aantallen[nr] = st.number_input(
                f"Aantal picknicks · menu {nr} {MENU_PER_NR[nr]['naam']}",
                min_value=1, max_value=100, value=1, step=1, key=f"aantal_{nr}",
            )

        korting = st.checkbox(
            "Klant heeft 10 loyaliteitspunten (automatische korting van € 10)",
        )

    with resultaat:
        weekend = is_weekend(leverdatum)
        dagnaam = DAGEN[leverdatum.weekday()]
        st.markdown(
            f"**Levering:** {dagnaam} {leverdatum.strftime('%d/%m/%Y')} om {tijdstip.strftime('%H:%M')}  \n"
            f"**Tarief:** {'weekend (+10 %)' if weekend else 'weekdag (standaardprijs)'}"
        )

        if not gekozen:
            st.info("Kies een menu om de totaalprijs te berekenen.")
            return

        regels = ""
        subtotaal = 0.0
        for nr in gekozen:
            menu = MENU_PER_NR[nr]
            bedrag = menu["prijs"] * aantallen[nr]
            subtotaal += bedrag
            regels += (
                f"<tr><td>{aantallen[nr]} × menu {nr} {menu['naam']}</td>"
                f"<td class='bedrag'>{euro(bedrag)}</td></tr>"
            )

        toeslag = subtotaal * WEEKENDTOESLAG if weekend else 0.0
        if weekend:
            regels += f"<tr><td>Weekendtoeslag (10 %)</td><td class='bedrag'>{euro(toeslag)}</td></tr>"

        totaal = subtotaal + toeslag
        if korting:
            totaal -= LOYALITEITSKORTING
            regels += f"<tr><td>Loyaliteitskorting</td><td class='bedrag'>− {euro(LOYALITEITSKORTING)}</td></tr>"

        st.markdown(
            f"<div class='totaalkader'><table>"
            f"{regels}"
            f"<tr class='totaal'><td>Totaalprijs</td><td class='bedrag'>{euro(totaal)}</td></tr>"
            f"</table></div>",
            unsafe_allow_html=True,
        )
        st.caption(f"Voorschot na ondertekening (50 %): {euro(totaal / 2)}")

        st.button("Op contract zetten", icon=":material/contract_edit:",
                  on_click=nog_niet_beschikbaar, args=("Op contract zetten",), width="stretch")


def toon_menus() -> None:
    koptekst("Menu's raadplegen", logo_breedte=180)
    st.button("Terug naar het overzicht", icon=":material/arrow_back:", on_click=ga_naar, args=("home",))

    tab_kaart, tab_prijs = st.tabs(["Menukaart", "Prijs berekenen"])
    with tab_kaart:
        toon_menukaart()
    with tab_prijs:
        toon_prijsberekening()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if st.session_state.pagina == "menu":
    toon_menus()
else:
    toon_home()
