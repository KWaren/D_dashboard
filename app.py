import streamlit as st
import pages

main_page = st.Page("pages/main.py", title="Acceuil", icon="🎈")
target = st.Page("pages/target.py", title="Tri par target", icon="📈")
page_3 = st.Page("pages/week.py", title="Tri par semaine", icon="🗓️")

# Set up navigation
pg = st.navigation([main_page, target, page_3])
pg.run()