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
    # Le CSV n'a pas d'en-tête, donc header=None
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
    st.session_state.show_answer = False  # afficher la réponse ou non

def next_card():
    st.session_state.index = (st.session_state.index + 1) % n_cards
    st.session_state.show_answer = False

def prev_card():
    st.session_state.index = (st.session_state.index - 1) % n_cards
    st.session_state.show_answer = False

# ----------------- STYLE -----------------
st.markdown(
    """
    <style>
    .main {
        background: radial-gradient(circle at top left, #111827 0, #020617 45%, #000000 100%);
    }
    .flashcard-container {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    .flashcard {
        background: #111827;
        background-image: radial-gradient(circle at top left, #1f2937, #020617);
