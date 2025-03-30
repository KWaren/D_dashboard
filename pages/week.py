import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.markdown("# Tri par semaine 🗓️")
st.sidebar.markdown("# Tri par semaine 🗓️")

st.write("Importez un fichier Excel, choisissez une ou plusieurs feuilles. Visualisez vos données sous forme de graphiques interactifs pour une analyse claire et rapide.")

@st.cache_data
def load_excel(uploaded_file):
    return pd.read_excel(uploaded_file, sheet_name=None)

uploaded_file = st.file_uploader("📤 Importer votre fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    sheets = load_excel(uploaded_file)
    selected_sheets = st.multiselect("Choisissez les feuilles à utiliser :", sheets.keys())

    if selected_sheets:
        data_list = [sheets[sheet] for sheet in selected_sheets]
        data = pd.concat(data_list)  # Fusionner toutes les feuilles sélectionnées
        data.columns = [str(col).upper() for col in data.columns]
        
        st.success(f"✅ Données des feuilles {', '.join(selected_sheets)} chargées")
        st.write(data)
        
        # Vérifier si la colonne ZONES existe
        if "ZONES" in data.columns:
            metrics = {
                "Montant Cash In": ["MONTANT CASH IN REALISE", "MONTANT CASH IN TARGET"],
                "Montant Cash Out": ["MONTANT CASH OUT REALISE", "MONTANT CASH OUT TARGET"],
                "Montant Cico": ["MONTANT CICO REALISE", "MONTANT CICO TARGET"],
                "Agent App Actif": ["AGENT APP ACTIF REALISE", "AGENT APP ACTIF TARGET"],
                "Agent App Cico": ["AGENT APP CICO REALISE", "AGENT APP CICO TARGET"]
            }
            
            tabs = st.tabs(metrics.keys())
            
            for i, (tab_name, cols) in enumerate(metrics.items()):
                with tabs[i]:
                    if all(col in data.columns for col in cols):
                        zone_data = data.groupby("ZONES")[cols].sum().reset_index()
                        fig = go.Figure()
                        
                        fig.add_trace(go.Bar(x=zone_data["ZONES"], y=zone_data[cols[0]], name=f"{tab_name} Réalisé", marker_color="hsl(44.23, 98.16%, 57.45%)"))
                        fig.add_trace(go.Bar(x=zone_data["ZONES"], y=zone_data[cols[1]], name=f"{tab_name} Target", marker_color="hsl(198, 73.17%, 32.16%)"))
                        
                        fig.update_layout(xaxis_title="Zones", yaxis_title="Montants / Agents", barmode="group")
                        st.plotly_chart(fig)
                    else:
                        st.warning(f"Les colonnes {cols} sont absentes des données.")
    else:
        st.warning("Veuillez sélectionner au moins une feuille.")
else:
    st.warning("Veuillez importer un fichier Excel.")
