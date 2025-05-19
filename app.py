import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sumátor času", page_icon="⏱️")

st.title("⏱️ Sumátor času v CSV")
st.write("Nahraj CSV soubor obsahující sloupec **'Čas v hodinách'**. Aplikace automaticky spočítá celkový čas a přidá nový řádek.")

uploaded_file = st.file_uploader("Vyber CSV soubor", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'Čas v hodinách' not in df.columns:
        st.error("❌ Sloupec 'Čas v hodinách' nebyl nalezen.")
    else:
        df['Čas v hodinách'] = pd.to_numeric(df['Čas v hodinách'], errors='coerce')
        total = df['Čas v hodinách'].sum()

        # Přidání nového řádku
        new_row = {col: "" for col in df.columns}
        first_col = df.columns[0]
        new_row[first_col] = "Celkem hodin:"
        new_row['Čas v hodinách'] = total
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        st.success(f"✅ Celkový čas: {total} hodin")
        st.dataframe(df, use_container_width=True)

        # Možnost stáhnout CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Stáhnout upravený CSV",
            data=csv,
            file_name="upraveny_soubor.csv",
            mime="text/csv"
        )
