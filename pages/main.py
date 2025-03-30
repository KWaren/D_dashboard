import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.markdown("# Acceuil ")
st.sidebar.markdown("# Acceuil ")
st.write("Importez un fichier Excel, choisissez la feuille et sélectionnez les colonnes à comparer. Visualisez vos données sous forme de graphiques interactifs pour une analyse claire et rapide.")
# Chargement des données
DATE_COLUMN = 'date/time'

@st.cache_data
def load_excel(uploaded_file):
    return pd.read_excel(uploaded_file, sheet_name=None)

uploaded_file = st.file_uploader("📤 Importer votre fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    sheets = load_excel(uploaded_file)
    sheet = st.selectbox("Choisissez la feuille à utiliser :", sheets.keys())

    if sheet:
        data = sheets[sheet]
        data.columns = [str(col).upper() for col in data.columns]
        if DATE_COLUMN in data.columns:
            data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

        st.success(f"✅ Données de la feuille '{sheet}' chargées")
        st.write(data)
        
        # Sélection des deux colonnes à afficher
        available_columns = [col for col in data.columns if col != "ZONES"]
        selected_columns = st.multiselect("Choisissez deux colonnes :", available_columns, default=available_columns[:2])
        
        if len(selected_columns) == 2:
            col1, col2 = selected_columns
            
            # Vérification que "ZONES" est présent
            if "ZONES" in data.columns:
                zone_data = data.groupby("ZONES")[[col1, col2]].sum().reset_index()

                # Création du graphique avec barres groupées
                fig = go.Figure()

                # Ajout des barres pour la première colonne
                fig.add_trace(go.Bar(
                    x=zone_data["ZONES"],
                    y=zone_data[col1],
                    name=col1,
                    marker_color="hsl(44.23, 98.16%, 57.45%)"
                ))

                # Ajout des barres pour la deuxième colonne
                fig.add_trace(go.Bar(
                    x=zone_data["ZONES"],
                    y=zone_data[col2],
                    name=col2,
                    marker_color="hsl(198, 73.17%, 32.16%)"
                ))

                # Mise en page du graphique
                fig.update_layout(
                    xaxis_title="Zones",
                    yaxis_title="Valeurs (somme par zone)",
                    barmode="group"  # Permet d'afficher les barres côte à côte
                )

                # Affichage du graphique
                st.plotly_chart(fig)
            else:
                st.error("⚠️ La colonne 'ZONES' est manquante dans le fichier.")
        else:
            st.warning("Veuillez sélectionner exactement **deux colonnes**.")
