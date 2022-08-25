import streamlit as st
from streamlit_option_menu import option_menu
from GEP_Downloader import gep_downloader
from Capella_Cron import Capella_Cron

with st.sidebar:
    choose = option_menu("Menu", ["GEP Downloader", "Capella Cron"],
                         icons=['cloud-download', 'cloud-download'],
                         menu_icon="app-indicator", default_index=0, 
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "GEP Downloader":
    gep_downloader.view()
elif choose == "Capella Cron":
    Capella_Cron.view()