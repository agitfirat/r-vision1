import streamlit as st
import pandas as pd
from pathlib import Path
from html import escape
import textwrap

# ----------------- CONFIG GLOBALE -----------------
st.set_page_config(
    page_title="Réseaux Flashcards",
    page_icon="🧠",
    layout="centered",
)

# ----------------- STYLES -----------------
st.markdown(
    """
    <style>
    .main {
        background: radial-gradient(circle at top left, #020617 0, #020617 40%, #000000 100%);
        color: #e5e7eb;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     "Segoe UI", sans-serif;
    }

    h1 {
        font-weight: 800 !important;
        letter-spacing: 0.04em;
        margin-bottom: 1.5rem;
    }

    .flashcard-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .flashcard {
        background: radial-gradient(circle at top left, #111827 0, #020617 55%, #020617 100%);
        border-radius: 28px;
        padding: 2.8rem 3rem;
        box-shadow:
            0 35px 80px rgba(0,0,0,0.85),
            0 0 0 1px rgba(148,163,184,0.06);
        max-width: 900px;
        width: 100%;
    }

    .flashcard-text {
        font-size: 1.6rem;
        line-height: 1.5;
        font-weight: 500;
        color: #f9fafb;
    }

    .flashcard-answer-title {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #9ca3af;
    }

    div.stButton > button {
        border-radius: 999px !important;
        padding: 0.5rem 1.6rem !important;
        font-size: 0.95rem !important;
        border: 1px solid rgba(148,163,184,0.5) !important;
    }

    .stProgress > div > div > div > div {
        height: 5px;
        border-radius: 999px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- DATA -----------------
@st.cache_data
def load_flashcards(csv_path: str):
    df = pd.read_csv(csv_path, header=None)
    df.columns = ["question", "answer"]
    return df

DATA_PATH = Path("flashcards-2.csv")
df = load_flashcards(str(DATA_PATH))
n_cards = len(df)

# ----------------- SESSION STATE -----------------
if "index" not in st.session_state:
    st.session_state.index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

def next_card():
    st.session_state.index = (st.session_state.index + 1) % n_cards
    st.session_state.show_answer = False

def prev_card():
    st.session_state.index = (st.session_state.index - 1) % n_cards
    st.session_state.show_answer = False

# ----------------- UI -----------------
st.title("🧠 Réseaux Flashcards")

current = df.iloc[st.session_state.index]

# 2 STR : front (question) / back (question + réponse)
q = escape(str(current["question"]))
a = escape(str(current["answer"]))

front = q
back = f"""{q}<br><br><span class="flashcard-answer-title">Réponse</span><br>{a}"""

content = back if st.session_state.show_answer else front

card_html = f"""
<div class="flashcard-wrapper">
  <div class="flashcard">
    <div class="flashcard-text">
      {content}
    </div>
  </div>
</div>
"""
card_html = textwrap.dedent(card_html)

st.markdown(card_html, unsafe_allow_html=True)

# Bouton afficher / masquer
label = "Masquer la réponse" if st.session_state.show_answer else "Afficher la réponse"
if st.button(label, key="toggle-answer-btn"):
    st.session_state.show_answer = not st.session_state.show_answer

# Barre de progression
progress = (st.session_state.index + 1) / n_cards
st.progress(progress)
st.caption(f"Carte {st.session_state.index + 1} / {n_cards}")

# Navigation
col1, _, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Précédent", key="prev-btn"):
        prev_card()

with col3:
    if st.button("Suivant ➡️", key="next-btn"):
        next_card()
