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
        color: #f9fafb;
        padding: 3rem 2.5rem;
        border-radius: 24px;
        box-shadow: 0 25px 40px rgba(0,0,0,0.6);
        max-width: 800px;
        width: 100%;
        font-size: 1.4rem;
        line-height: 1.5;
    }
    .flashcard-question {
        font-weight: 500;
    }
    .flashcard-separator {
        margin: 1.5rem 0 1rem 0;
        border: none;
        border-top: 1px solid rgba(249,250,251,0.15);
    }
    .flashcard-answer {
        font-size: 1.2rem;
        color: #e5e7eb;
    }
    div.stButton > button.answer-btn {
        border-radius: 999px;
        padding: 0.4rem 1.4rem;
        font-size: 1rem;
    }
    div.stButton > button.nav-btn {
        border-radius: 999px;
        padding: 0.4rem 1.4rem;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- UI -----------------
st.title("🧠 Réseaux Flashcards")

current = df.iloc[st.session_state.index]

# Carte question + (éventuellement) réponse
if st.session_state.show_answer:
    answer_html = f"""
        <hr class="flashcard-separator" />
        <div class="flashcard-answer">{current['answer']}</div>
    """
else:
    answer_html = ""

card_html = f"""
<div class="flashcard-container">
  <div class="flashcard">
    <div class="flashcard-question">{current['question']}</div>
    {answer_html}
  </div>
</div>
"""
st.markdown(card_html, unsafe_allow_html=True)

# Bouton "Afficher la réponse" / "Masquer la réponse"
label = "Masquer la réponse" if st.session_state.show_answer else "Afficher la réponse"
if st.button(label, key="show_answer", type="secondary"):
    st.session_state.show_answer = not st.session_state.show_answer

# Barre de progression
progress = (st.session_state.index + 1) / n_cards
st.progress(progress)
st.caption(f"Carte {st.session_state.index + 1} / {n_cards}")

# Boutons Précédent / Suivant
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Précédent", key="prev", help="Carte précédente", type="secondary"):
        prev_card()

with col3:
    if st.button("Suivant ➡️", key="next", help="Carte suivante", type="secondary"):
        next_card()
