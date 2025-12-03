import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------- CONFIG GLOBALE -----------------
st.set_page_config(
    page_title="Réseaux Flashcards",
    page_icon="🧠",
    layout="centered",
)

# ----------------- CHARGER LES DONNÉES -----------------
@st.cache_data
def load_flashcards(csv_path: str):
    # Ton fichier n'a pas de vraie ligne d'en-tête,
    # donc on met header=None et on renomme les colonnes.
    df = pd.read_csv(csv_path, header=None)
    df.columns = ["question", "answer"]
    return df

DATA_PATH = Path("flashcards-2.csv")  # mets le fichier à côté de app.py
df = load_flashcards(str(DATA_PATH))
n_cards = len(df)

# ----------------- SESSION STATE -----------------
if "index" not in st.session_state:
    st.session_state.index = 0      # carte actuelle
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False  # question ou réponse ?

def flip_card():
    st.session_state.show_answer = not st.session_state.show_answer

def next_card():
    st.session_state.index = (st.session_state.index + 1) % n_cards
    st.session_state.show_answer = False

def prev_card():
    st.session_state.index = (st.session_state.index - 1) % n_cards
    st.session_state.show_answer = False

# ----------------- STYLE (carte + fond) -----------------
st.markdown(
    """
    <style>
    .main {
        background: radial-gradient(circle at top left, #111827 0, #020617 45%, #000000 100%);
    }
    div.stButton > button.flashcard {
        background: #111827;
        background-image: radial-gradient(circle at top left, #1f2937, #020617);
        color: #f9fafb;
        padding: 4rem 3rem;
        border-radius: 24px;
        border: none;
        font-size: 1.6rem;
        line-height: 1.4;
        box-shadow: 0 25px 40px rgba(0,0,0,0.6);
        width: 100%;
        height: auto;
        white-space: normal;
        cursor: pointer;
    }
    div.stButton > button.flashcard:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 30px 50px rgba(0,0,0,0.7);
    }
    div.stButton > button.nav-btn {
        border-radius: 999px;
        padding: 0.5rem 1.5rem;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- UI -----------------
st.title("🧠 Réseaux Flashcards")

current = df.iloc[st.session_state.index]
card_text = current["answer"] if st.session_state.show_answer else current["question"]

st.write("")
st.write("Clique sur la carte pour la retourner.")

# Carte cliquable (bouton stylé comme une carte)
if st.button(card_text, key="flashcard", use_container_width=True):
    flip_card()

# Barre de progression
progress = (st.session_state.index + 1) / n_cards
st.progress(progress)
st.caption(f"Carte {st.session_state.index + 1} / {n_cards}")

# Boutons Précédent / Suivant
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Précédent", key="prev", help="Carte précédente", kwargs=None):
        prev_card()

with col3:
    if st.button("Suivant ➡️", key="next", help="Carte suivante", kwargs=None):
        next_card()
