import streamlit as st
import pandas as pd

# Wczytanie atlasu Totalnej Biologii
@st.cache_data
def load_data():
    return pd.read_csv("atlas_totalnej_biologii.csv")

df = load_data()

st.title("🌸 Agent AI Totalnej Biologii")
st.write("Wpisz objaw, organ lub wybierz układ ciała, aby znaleźć konflikt biologiczny i jego znaczenie.")

# Tryby pracy
mode = st.radio("Wybierz tryb:", ["🔍 Konsultacja", "📖 Atlas Układów"])

if mode == "🔍 Konsultacja":
    query = st.text_input("Podaj objaw lub organ (np. 'żołądek', 'kaszel', 'biegunka'):")

    if query:
        results = df[df.apply(lambda row: query.lower() in row.to_string().lower(), axis=1)]
        
        if not results.empty:
            st.write("### Wyniki wyszukiwania:")
            st.dataframe(results)
        else:
            st.warning("Brak wyników dla podanego zapytania.")

elif mode == "📖 Atlas Układów":
    układy = df["Układ"].unique()
    selected = st.selectbox("Wybierz układ ciała:", układy)

    results = df[df["Układ"] == selected]
    st.write(f"### Atlas dla: {selected}")
    st.dataframe(results)

