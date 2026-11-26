"""Posh PicNic – klikbare mock-up van het bestelsysteem (WS04).

Start lokaal met:  streamlit run app.py
"""

from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Basisinstellingen
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Posh PicNic", page_icon="🧺", layout="wide")

LOGO = Path(__file__).parent / "assets" / "logo.png"

GROEN = "#2F4A3A"
GROEN_LICHT = "#3E5E4B"
ROZE = "#E8A9A0"
ROZE_LICHT = "#F6DCD7"
CREME = "#FBF6EF"
GOUD = "#C9A45C"

WEEKENDTOESLAG = 0.10  # 10 % extra op zaterdag en zondag (projectmandaat)

# ---------------------------------------------------------------------------
# Opmaak: groen en roze uit het logo, met een geruit (gingham) patroon
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

    /* Geruit roze patroon als achtergrond van de pagina */
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

    /* Geruite band (zoals het kleedje in het logo) */
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

    .subtitel {{
        text-align: center;
        letter-spacing: .35em;
        color: #A8843F;
        font-size: .85rem;
        margin-top: -.5rem;
    }}
    .sectie {{
        font-family: 'Cardo', serif;
        font-size: 1.6rem;
        color: {GROEN};
        border-bottom: 3px solid {ROZE};
        padding-bottom: .2rem;
        margin: 1.2rem 0 .8rem 0;
    }}

    /* Knoppen: groen met roze accent */
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

    /* Menukaarten */
    .menukaart {{
        background: #FFFFFF;
        border: 2px solid {ROZE_LICHT};
        border-top: 8px solid {GROEN};
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        min-height: 255px;
    }}
    .menukaart h4 {{ margin: 0 0 .3rem 0; font-size: 1.35rem; }}
    .menukaart ul {{ margin: .4rem 0 .6rem 1.1rem; padding: 0; }}
    .menukaart li {{ font-size: .9rem; margin-bottom: .1rem; }}
    .prijs {{ font-weight: 600; color: {GROEN}; }}
    .weekend {{ font-size: .85rem; color: #7A6A5A; }}
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
        margin-bottom: 1.2rem;
        font-size: .92rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Voorbeelddata: de tien standaardmenu's (fictief)
# ---------------------------------------------------------------------------
MENUS = [
    {
        "nr": 1, "naam": "Klassieke Picknick", "prijs": 18.00, "labels": [],
        "beschrijving": "De tijdloze favoriet voor elk gezelschap.",
        "inhoud": ["Belegde broodjes (ham, kaas, kip)", "Huisgemaakte koolsla", "Seizoensfruit", "Verse limonade"],
    },
    {
        "nr": 2, "naam": "Mediterraanse Zomer", "prijs": 22.00, "labels": ["vegetarisch optie"],
        "beschrijving": "Zonnige smaken uit het zuiden.",
        "inhoud": ["Focaccia met tapenade", "Tomaat-mozzarella", "Gegrilde groenten", "Tiramisu in een potje"],
    },
    {
        "nr": 3, "naam": "Vegetarisch Tuinfeest", "prijs": 19.00, "labels": ["vegetarisch"],
        "beschrijving": "Kleurrijk, fris en volledig vleesloos.",
        "inhoud": ["Quiche met spinazie en feta", "Couscoussalade", "Groentesticks met hummus", "Fruitspiesjes"],
    },
    {
        "nr": 4, "naam": "Kinderfeestje", "prijs": 14.00, "labels": ["kinderen"],
        "beschrijving": "Speels en lekker voor de kleinste gasten.",
        "inhoud": ["Mini-sandwiches", "Kippennuggets (koud)", "Fruitsalade", "Chocolademelk"],
    },
    {
        "nr": 5, "naam": "Brunch in het Gras", "prijs": 20.00, "labels": [],
        "beschrijving": "Een uitgebreide brunch in open lucht.",
        "inhoud": ["Croissants en pistolets", "Gerookte zalm en roomkaas", "Yoghurt met granola", "Vers sinaasappelsap"],
    },
    {
        "nr": 6, "naam": "Zomerse Grillpicknick", "prijs": 24.00, "labels": [],
        "beschrijving": "Koude grillgerechten, klaar om te delen.",
        "inhoud": ["Kippenbouten en spareribs (koud)", "Aardappelsalade", "Maïskolfjes", "Ijsthee"],
    },
    {
        "nr": 7, "naam": "Luxe Champagnepicknick", "prijs": 35.00, "labels": ["luxe"],
        "beschrijving": "Voor de speciale momenten, met bubbels.",
        "inhoud": ["Oesters en zeevruchten", "Fijne kazen en charcuterie", "Macarons", "Fles champagne (per 4 personen)"],
    },
    {
        "nr": 8, "naam": "Business Lunch", "prijs": 21.00, "labels": ["weekdag"],
        "beschrijving": "Verzorgde lunch voor teams en vergaderingen.",
        "inhoud": ["Wraps en clubsandwiches", "Salade van het seizoen", "Dessert van de chef", "Water en koffie"],
    },
    {
        "nr": 9, "naam": "Vegan Groen", "prijs": 19.00, "labels": ["vegan"],
        "beschrijving": "Volledig plantaardig en vol smaak.",
        "inhoud": ["Falafel met tahinsaus", "Quinoasalade", "Groentechips", "Havermelk-smoothie"],
    },
    {
        "nr": 10, "naam": "Seizoenspicknick", "prijs": 23.00, "labels": ["wisselend"],
        "beschrijving": "Elke maand andere seizoensproducten.",
        "inhoud": ["Verrassingsgerechten van de chef", "Seizoenssoep in een thermos", "Taart van het seizoen", "Huisgemaakte drank"],
    },
]


# ---------------------------------------------------------------------------
# Navigatie
# ---------------------------------------------------------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "home"


def ga_naar(pagina: str) -> None:
    st.session_state.pagina = pagina


def nog_niet_beschikbaar(functie: str) -> None:
    st.toast(f"‘{functie}’ is nog niet beschikbaar in deze mock-up.", icon="🧺")


def euro(bedrag: float) -> str:
    return f"€ {bedrag:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def koptekst(titel: str | None = None, logo_breedte: int = 300) -> None:
    links, midden, rechts = st.columns([1, 2, 1])
    with midden:
        if LOGO.exists():
            # Logo gecentreerd tonen
            _, logo_kolom, _ = st.columns([1, 3, 1])
            with logo_kolom:
                st.image(str(LOGO), width=logo_breedte)
        else:
            st.markdown(f"<h1 style='text-align:center'>Posh PicNic</h1>", unsafe_allow_html=True)
    st.markdown("<div class='gingham'></div>", unsafe_allow_html=True)
    if titel:
        st.markdown(f"<h2 style='text-align:center'>{titel}</h2>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Pagina: hoofdpagina
# ---------------------------------------------------------------------------
def toon_home() -> None:
    koptekst()
    st.markdown(
        "<p style='text-align:center;font-size:1.05rem'>"
        "Welkom bij Posh PicNic! Stel je ideale picknick samen, voor familie, vrienden of collega's."
        "</p>",
        unsafe_allow_html=True,
    )

    # Klantgedeelte (het systeem vertrekt vanuit het perspectief van de klant)
    st.markdown("<div class='sectie'>Voor klanten</div>", unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    with k1:
        st.button("Menu's raadplegen", icon=":material/restaurant_menu:", on_click=ga_naar, args=("menu",), width="stretch")
        st.button("Mijn contracten", icon=":material/contract:", on_click=nog_niet_beschikbaar, args=("Mijn contracten",), width="stretch")
    with k2:
        st.button("Standaardpicknick bestellen", icon=":material/shopping_basket:", on_click=nog_niet_beschikbaar, args=("Standaardpicknick bestellen",), width="stretch")
        st.button("Mijn gegevens", icon=":material/person:", on_click=nog_niet_beschikbaar, args=("Mijn gegevens",), width="stretch")
    with k3:
        st.button("Speciaal verzoek indienen", icon=":material/cake:", on_click=nog_niet_beschikbaar, args=("Speciaal verzoek indienen",), width="stretch")
        st.button("Mijn loyaliteitspunten", icon=":material/loyalty:", on_click=nog_niet_beschikbaar, args=("Mijn loyaliteitspunten",), width="stretch")

    # Medewerkersgedeelte
    st.markdown("<div class='sectie'>Voor medewerkers</div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.button("Klantgegevens beheren", icon=":material/badge:", on_click=nog_niet_beschikbaar, args=("Klantgegevens beheren",), width="stretch")
        st.button("Contracten opvolgen", icon=":material/notifications_active:", on_click=nog_niet_beschikbaar, args=("Contracten opvolgen",), width="stretch")
    with m2:
        st.button("Speciale verzoeken ramen", icon=":material/request_quote:", on_click=nog_niet_beschikbaar, args=("Speciale verzoeken ramen",), width="stretch")
        st.button("Leveringen beheren", icon=":material/local_shipping:", on_click=nog_niet_beschikbaar, args=("Leveringen beheren",), width="stretch")
    with m3:
        st.button("Producten bestellen", icon=":material/inventory_2:", on_click=nog_niet_beschikbaar, args=("Producten bestellen",), width="stretch")
        st.button("Marketingoverzicht", icon=":material/insights:", on_click=nog_niet_beschikbaar, args=("Marketingoverzicht",), width="stretch")

    st.markdown("<div class='gingham' style='margin-top:2rem'></div>", unsafe_allow_html=True)
    st.caption("Mock-up voor WS04 · fictieve gegevens")


# ---------------------------------------------------------------------------
# Pagina: menu's raadplegen
# ---------------------------------------------------------------------------
def toon_menus() -> None:
    koptekst("Onze standaardmenu's", logo_breedte=200)

    st.button("Terug naar de hoofdpagina", icon=":material/arrow_back:", on_click=ga_naar, args=("home",))

    st.markdown(
        "<div class='infobalk'>"
        "<b>Goed om te weten</b><br>"
        "• Op zaterdag en zondag geldt een weekendtoeslag van 10 %.<br>"
        "• Je verdient 1 loyaliteitspunt per bestelde picknick; 10 punten geven € 10 korting op je volgende bestelling.<br>"
        "• Iets speciaals erbij, zoals een verjaardagstaart of een cadeau? Dien een speciaal verzoek in."
        "</div>",
        unsafe_allow_html=True,
    )

    zoek = st.text_input("Zoek een menu", placeholder="bv. vegan, brunch, kinderen…")
    weekend = st.toggle("Toon weekendprijzen (zaterdag en zondag)")

    gefilterd = [
        m for m in MENUS
        if not zoek
        or zoek.lower() in m["naam"].lower()
        or zoek.lower() in m["beschrijving"].lower()
        or any(zoek.lower() in label for label in m["labels"])
        or any(zoek.lower() in item.lower() for item in m["inhoud"])
    ]

    if not gefilterd:
        st.info("Geen menu gevonden. Probeer een andere zoekterm.")
        return

    kolommen = st.columns(2)
    for i, menu in enumerate(gefilterd):
        prijs = menu["prijs"] * (1 + WEEKENDTOESLAG) if weekend else menu["prijs"]
        labels = "".join(f"<span class='label'>{l}</span>" for l in menu["labels"])
        inhoud = "".join(f"<li>{item}</li>" for item in menu["inhoud"])
        dag = "weekendprijs" if weekend else "weekdagprijs"
        with kolommen[i % 2]:
            st.markdown(
                f"<div class='menukaart'>"
                f"<h4>Menu {menu['nr']} · {menu['naam']}</h4>"
                f"{labels}"
                f"<p style='margin:.5rem 0 0 0'><i>{menu['beschrijving']}</i></p>"
                f"<ul>{inhoud}</ul>"
                f"<span class='prijs'>{euro(prijs)} per persoon</span> "
                f"<span class='weekend'>({dag})</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.button(
                f"Bestel menu {menu['nr']}",
                key=f"bestel_{menu['nr']}",
                icon=":material/add_shopping_cart:",
                on_click=nog_niet_beschikbaar,
                args=(f"Bestel menu {menu['nr']}",),
                width="stretch",
            )


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if st.session_state.pagina == "menu":
    toon_menus()
else:
    toon_home()
