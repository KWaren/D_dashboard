import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.markdown("# Tri par objectif 📈")
st.sidebar.markdown("# Tri par objectif 📈")

st.write("Importez un fichier Excel, choisissez la feuille. Visualisez vos données sous forme de graphiques interactifs pour une analyse claire et rapide.")
# Chargement des données
DATE_COLUMN = 'date/time'

@st.cache_data
def load_excel(uploaded_file):
    # Charge toutes les feuilles d'un coup dans un dictionnaire de DataFrames
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
else:
    st.warning("Veuillez importer un fichier Excel.")

# Montant total encaissé par Zone
if uploaded_file:
    # Regrouper les données par zone
    zone_data = data.groupby("ZONES")[["MONTANT CASH IN REALISE", "MONTANT CASH IN TARGET"]].sum().reset_index()

    # Création du graphique avec barres groupées
    fig = go.Figure()

    # Ajout des barres pour Cash In Réalisé (rouge)
    fig.add_trace(go.Bar(
        x=zone_data["ZONES"],
        y=zone_data["MONTANT CASH IN REALISE"],
        name="Cash In Réalisé",
        marker_color="hsl(44.23, 98.16%, 57.45%)"
    ))

    # Ajout des barres pour Cash In Target (bleu)
    fig.add_trace(go.Bar(
        x=zone_data["ZONES"],
        y=zone_data["MONTANT CASH IN TARGET"],
        name="Cash In Target",
        marker_color="hsl(198, 73.17%, 32.16%)"
    ))

    # Mise en page du graphique
    fig.update_layout(
        # title="Comparaison Cash In Réalisé vs Target par Zone",
        xaxis_title="Zones",
        yaxis_title="Montants (somme par zone)",
        barmode="group"  # Permet d'afficher les barres côte à côte
    )


# Montant total retiré par Zone
if uploaded_file:
    # Regrouper les données par zone
    zone_data1 = data.groupby("ZONES")[["MONTANT CASH OUT REALISE", "MONTANT CASH OUT TARGET"]].sum().reset_index()

    # Création du graphique avec barres groupées
    fig1 = go.Figure()

    # Ajout des barres pour Cash OUT Réalisé (rouge)
    fig1.add_trace(go.Bar(
        x=zone_data1["ZONES"],
        y=zone_data1["MONTANT CASH OUT REALISE"],
        name="Cash OUT Réalisé",
        marker_color="hsl(44.23, 98.16%, 57.45%)"
    ))

    # Ajout des barres pour Cash OUT Target (bleu)
    fig1.add_trace(go.Bar(
        x=zone_data1["ZONES"],
        y=zone_data1["MONTANT CASH OUT TARGET"],
        name="Cash OUT Target",
        marker_color="hsl(198, 73.17%, 32.16%)"
    ))

    # Mise en page du graphique
    fig1.update_layout(
        # title="Comparaison Cash out Réalisé vs Target par Zone",
        xaxis_title="Zones",
        yaxis_title="Montants (somme par zone)",
        barmode="group"  # Permet d'afficher les barres côte à côte
    )


# Montant total CICO par Zone
if uploaded_file:
    # Regrouper les données par zone
    zone_data1 = data.groupby("ZONES")[["MONTANT CICO REALISE", "MONTANT CICO TARGET"]].sum().reset_index()

    # Création du graphique avec barres groupées
    fig2 = go.Figure()

    # Ajout des barres pour Cash OUT Réalisé (rouge)
    fig2.add_trace(go.Bar(
        x=zone_data1["ZONES"],
        y=zone_data1["MONTANT CICO REALISE"],
        name="Cico Réalisé",
        marker_color="hsl(44.23, 98.16%, 57.45%)"
    ))

    # Ajout des barres pour Cash OUT Target (bleu)
    fig2.add_trace(go.Bar(
        x=zone_data1["ZONES"],
        y=zone_data1["MONTANT CICO TARGET"],
        name="Cico Target",
        marker_color="hsl(198, 73.17%, 32.16%)"
    ))

    # Mise en page du graphique
    fig2.update_layout(
        # title="Comparaison Cash out Réalisé vs Target par Zone",
        xaxis_title="Zones",
        yaxis_title="Montants (somme par zone)",
        barmode="group"  # Permet d'afficher les barres côte à côte
    )


# Agent actifs
if uploaded_file:
    # Regrouper les données par zone
    zone_data = data.groupby("ZONES")[["AGENT APP ACTIF TARGET", "AGENT APP ACTIF REALISE"]].sum().reset_index()

    # Création du graphique avec barres groupées
    fig3 = go.Figure()

    # Ajout des barres pour Cash In Réalisé (rouge)
    fig3.add_trace(go.Bar(
        x=zone_data["ZONES"],
        y=zone_data["AGENT APP ACTIF REALISE"],
        name="Agent réellement Actif",
        marker_color="hsl(44.23, 98.16%, 57.45%)"
    ))

    # Ajout des barres pour Cash In Target (bleu)
    fig3.add_trace(go.Bar(
        x=zone_data["ZONES"],
        y=zone_data["AGENT APP ACTIF TARGET"],
        name="Agent Actif Target",
        marker_color="hsl(198, 73.17%, 32.16%)"
    ))

    # Mise en page du graphique
    fig3.update_layout(
        # title="Comparaison Cash In Réalisé vs Target par Zone",
        xaxis_title="Zones",
        yaxis_title="Agents actifs par zones",
        barmode="group"  # Permet d'afficher les barres côte à côte
    )


# Agent actifs ayant réalisé un cico
if uploaded_file:
    # Regrouper les données par zone
    zone_data = data.groupby("ZONES")[["AGENT APP CICO TARGET", "AGENT APP CICO REALISE"]].sum().reset_index()

    # Création du graphique avec barres groupées
    fig4 = go.Figure()

    # Ajout des barres pour Cash In Réalisé (rouge)
    fig4.add_trace(go.Bar(
        x=zone_data["ZONES"],
        y=zone_data["AGENT APP CICO REALISE"],
        name="Agent ayant réalisé un cico",
        marker_color="hsl(44.23, 98.16%, 57.45%)"
    ))

    # Ajout des barres pour Cash In Target (bleu)
    fig4.add_trace(go.Bar(
        x=zone_data["ZONES"],
        y=zone_data["AGENT APP CICO TARGET"],
        name="Objectif d'agent ayant réalisé un cico",
        marker_color="hsl(198, 73.17%, 32.16%)"
    ))

    # Mise en page du graphique
    fig4.update_layout(
        # title="Comparaison Cash In Réalisé vs Target par Zone",
        xaxis_title="Zones",
        yaxis_title="Agents actifs par zones",
        barmode="group"  # Permet d'afficher les barres côte à côte
    )



if uploaded_file:
    tab__1 , tab__2,tab__3,tab__4,tab__5= st.tabs(["Montant Cash In", "Montant Cash Out","Montant Cico","Agent App Actif","Agent App Cico"])
    with tab__1 :
        st.title("Montant total encaissé par Zone")
        st.plotly_chart(fig)
    with tab__2 :
        st.title("Montant total retiré par Zone")
        st.plotly_chart(fig1)
    with tab__3 :
        st.title("Total des transactions cico par zone")
        st.plotly_chart(fig2)

    with tab__4 :
        st.title("Nombre d'agents réellement actifs  par zone")
        st.plotly_chart(fig3)
    with tab__5 :    
        st.title("Somme des agents ayant effectué au moins une opération Cico")
        st.plotly_chart(fig4)