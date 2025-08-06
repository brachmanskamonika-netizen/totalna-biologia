import streamlit as st
import pandas as pd

# Wczytanie atlasu Totalnej Biologii
@st.cache_data
def load_data():
    return pd.read_csv("atlas_totalnej_biologii.csv")

df = load_data()

# Wyświetl kolumny w logach aby uniknąć KeyError
st.write("Dostępne kolumny:", list(df.columns))

st.set_page_config(page_title="🌸 Agent AI Totalnej Biologii", layout="wide")
st.title("🌸 Agent AI Totalnej Biologii")
st.write("Wpisz objaw, organ lub wybierz układ ciała, aby znaleźć konflikt biologiczny i jego znaczenie.")

# Sprawdź czy nazwy kolumn są zgodne z oczekiwaniami
expected_columns = ["Organ", "Konflikt biologiczny", "Układ", "Faza aktywna", "Faza zdrowienia"]

for col in expected_columns:
    if col not in df.columns:
        st.error(f"Brak kolumny w pliku CSV: {col}")

# Tryby pracy
mode = st.radio("Wybierz tryb:", ["🔍 Konsultacja", "📖 Atlas Układów"], horizontal=True)

if mode == "🔍 Konsultacja":
    query = st.text_input("Podaj objaw lub organ (np. 'żołądek', 'kaszel', 'biegunka'):")

    if query:
        results = df[df.apply(lambda row: query.lower() in row.to_string().lower(), axis=1)]
        
        if not results.empty:
            st.write("### Wyniki wyszukiwania:")
            for _, row in results.iterrows():
                organ = row.get('Organ', 'Nieznany organ')
                konflikt = row.get('Konflikt biologiczny', 'Brak danych')
                with st.expander(f"{organ} – {konflikt}"):
                    st.write(f"**Układ:** {row.get('Układ','Brak danych')}")
                    st.write(f"**Faza aktywna:** {row.get('Faza aktywna','Brak danych')}")
                    st.write(f"**Faza zdrowienia:** {row.get('Faza zdrowienia','Brak danych')}")
        else:
            st.warning("Brak wyników dla podanego zapytania.")

elif mode == "📖 Atlas Układów":
    if "Układ" not in df.columns:
        st.error("Brak kolumny 'Układ' w pliku CSV")
    else:
        układy = df["Układ"].unique()
        selected = st.selectbox("Wybierz układ ciała:", układy)

        results = df[df["Układ"] == selected]

        st.write(f"### Atlas dla: {selected}")
        
        for _, row in results.iterrows():
            organ = row.get('Organ', 'Nieznany organ')
            konflikt = row.get('Konflikt biologiczny', 'Brak danych')
            with st.expander(f"{organ} – {konflikt}"):
                st.write(f"**Faza aktywna:** {row.get('Faza aktywna','Brak danych')}")
                st.write(f"**Faza zdrowienia:** {row.get('Faza zdrowienia','Brak danych')}")
                st.write(f"**Opis:** {row.get('Opis','Brak dodatkowego opisu')} ")