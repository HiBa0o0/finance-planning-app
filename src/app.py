import streamlit as st # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
import plotly.graph_objects as go # type: ignore
import matplotlib.pyplot as plt # type: ignore
import plotly.io as pio # type: ignore
from io import BytesIO
import plotly.graph_objects as go # type: ignore
import tempfile
import os
import tempfile
from fpdf import FPDF # type: ignore
from datetime import datetime

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return  # Pas d'en-tête sur la page de garde
        self.set_font("Arial", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Rapport généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, "R")
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

# Couleurs harmonisées
COLOR_PRIMARY = (31, 119, 180)      # Bleu principal
COLOR_SECONDARY = (44, 160, 44)     # Vert
COLOR_ACCENT = (214, 39, 40)        # Rouge
COLOR_BG = (245, 247, 250)          # Fond très clair
COLOR_TABLE_HEADER = (220, 230, 241)
COLOR_TABLE_BORDER = (180, 180, 180)

# Fonction pour titres de section harmonisés

def section_title(title, color=COLOR_PRIMARY, align="L"):
    pdf.ln(6)
    pdf.set_font("Arial", "B", 15)
    pdf.set_text_color(*color)
    if align == "C":
        pdf.cell(0, 12, title, ln=True, align="C")
    else:
        pdf.cell(0, 12, title, ln=True)
    pdf.set_text_color(0,0,0)
    pdf.set_draw_color(*color)
    pdf.set_line_width(0.7)
    y = pdf.get_y()
    pdf.line(10, y, 200, y)
    pdf.ln(4)

# Configuration de la page avec un thème personnalisé
st.set_page_config(
    page_title="Plan de Financement", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS améliorés
st.markdown("""
<style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: #ffffff;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f0f2f6;
    }
    .financial-table {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        background-color: white;
    }
    .metric-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    /* Sidebar custom style */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #e3f0ff 0%, #f8f9fa 100%);
        border-radius: 8px 0 0 8px;
        box-shadow: 2px 0 12px rgba(31, 119, 180, 0.08);
        padding-top: 30px;
        padding-bottom: 30px;
        min-width: 270px;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        color: #1f77b4;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stRadio {
        color: #1f77b4;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Sidebar custom style for dark and light mode */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #232b36 0%, #1a1d23 100%);
        border-radius: 8px 0 0 8px;
        box-shadow: 2px 0 12px rgba(31, 119, 180, 0.12);
        padding-top: 30px;
        padding-bottom: 30px;
        min-width: 270px;
    }
    [data-testid="stSidebar"] .css-1d391kg, /* Sidebar title */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #90caf9 !important;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stRadio, [data-testid="stSidebar"] .stRadio label {
        color: #e3f2fd !important;
        font-size: 1.1rem;
    }
    [data-testid="stSidebar"] .stRadio > div {
        background: #232b36;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    [data-testid="stSidebar"] .stRadio > div:hover {
        background: #1f77b4;
        color: #fff !important;
    }
    /* Main area text color for dark mode */
    @media (prefers-color-scheme: dark) {
        .main, .stApp, .stMarkdown, .stDataFrame, .stTable, .stText, .stMetric {
            color: #e3f2fd !important;
        }
        .stDataFrame, .stTable {
            background: #232b36 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* ...existing code... */
    /* Tabs style for dark mode */
    @media (prefers-color-scheme: dark) {
        .stTabs [data-baseweb="tab"] {
            background: #232b36 !important;
            color: #e3f2fd !important;
            border-radius: 5px;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: #1f77b4 !important;
            color: #fff !important;
        }
        .stTabs [aria-selected="true"] {
            background: #1f77b4 !important;
            color: #fff !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Structure du plan de financement
EMPLOIS = {
    'Reliquat des plans antérieurs': ['Reliquat', 'Plans antérieurs'],
    'Investissements': ['Matériels', 'Équipements', 'Construction', 'Rénovation', 'Brevets', 'Licences'],
    'Remboursement emprunts': ['Remboursement', 'Échéance'],
    'BFR': ['BFR', 'Fonds de roulement', 'Stocks', 'Créances', 'Dettes'],
    'Dividendes': ['Dividendes', 'Rémunération actionnaires']
}

RESSOURCES = {
    'CAF': ['Capacité autofinancement', 'Bénéfices', 'Amortissements'],
    'Subventions': ['Subventions', 'Aides'],
    'Augmentation capital': ['Capital', 'Apport'],
    'Emprunts LMT': ['Emprunt', 'Crédit'],
    'Cessions actifs': ['Cession', 'Vente'],
    'Prélèvement FR': ['Prélèvement', 'Fonds roulement']
}

# Initialisation de l'état de session
if 'plans' not in st.session_state:
    st.session_state.plans = []
if 'current_plan' not in st.session_state:
    st.session_state.current_plan = None

# Ajout de la barre latérale pour le menu
def show_menu():
    st.sidebar.title("Menu")
    menu_choice = st.sidebar.radio(
        "Choisissez une fonctionnalité:",
        ["Plan de Financement", "Analyse Financière", "Étude Comparative"]
    )
    return menu_choice

def display_financial_status(solde):
    """Affiche le statut financier (Excédent/Déficit) avec explications"""
    if solde > 0:
        st.success(f"""
        ### ✅ Excédent Financier: {solde:,.2f} DA
        L'entreprise dispose d'un surplus de financement qui peut être utilisé pour:
        - Renforcer sa trésorerie
        - Investir davantage
        - Réduire ses dettes
        """)
    else:
        st.error(f"""
        ### ⚠️ Déficit Financier: {solde:,.2f} DA
        L'entreprise fait face à un besoin de financement supplémentaire.
        **Attention**: Un déficit répété ou trop important peut mettre en péril la solvabilité de l'entreprise.
        """)

def display_financial_table(data, year):
    """Affiche les données sous forme de tableau de plan de financement"""
    st.markdown(f"### Plan de Financement - Année {year}")
    # Création du tableau détaillé
    table_data = []
    # Section Emplois
    table_data.append(["EMPLOIS", "Montant (DA)", "RESSOURCES", "Montant (DA)"])
    max_len = max(len(data['Emplois']), len(data['Ressources']))
    emplois_items = list(data['Emplois'].items())
    ressources_items = list(data['Ressources'].items())
    for i in range(max_len):
        emp_row = emplois_items[i] if i < len(emplois_items) else ("", 0)
        res_row = ressources_items[i] if i < len(ressources_items) else ("", 0)
        table_data.append([
            emp_row[0], 
            f"{emp_row[1]:,.2f} DA" if emp_row[1] else "",
            res_row[0], 
            f"{res_row[1]:,.2f} DA" if res_row[1] else ""
        ])
    # Totaux
    total_emplois = sum(data['Emplois'].values())
    total_ressources = sum(data['Ressources'].values())
    table_data.append([
        "Total Emplois", 
        f"{total_emplois:,.2f} DA",
        "Total Ressources", 
        f"{total_ressources:,.2f} DA"
    ])
    # Création du DataFrame avec des noms de colonnes uniques
    df_table = pd.DataFrame(
        table_data,
        columns=["Type_Emplois", "Montant_Emplois", "Type_Ressources", "Montant_Ressources"]
    )
    # Style sobre : gris clair pour l'entête et la ligne des totaux, blanc pour le reste
    def style_rows(row):
        if row.name == 0 or row.name == len(df_table)-1:
            return ["background-color: #ececec; font-weight: bold; color: #222;" for _ in row]
        else:
            return ["background-color: #fff; color: #222;" for _ in row]
    styled_df = df_table.style.apply(style_rows, axis=1)
    st.dataframe(styled_df, height=400)
    # Calcul et affichage du solde
    solde = total_ressources - total_emplois
    display_financial_status(solde)

def load_excel_file(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        
        # Réorganiser les données selon la structure
        organized_data = {
            'Emplois': {},
            'Ressources': {}
        }
        
        # Traitement des emplois
        for category, keywords in EMPLOIS.items():
            mask = df.index.str.contains('|'.join(keywords), case=False, na=False)
            organized_data['Emplois'][category] = df[mask].sum()
            
        # Traitement des ressources
        for category, keywords in RESSOURCES.items():
            mask = df.index.str.contains('|'.join(keywords), case=False, na=False)
            organized_data['Ressources'][category] = df[mask].sum()
            
        return pd.DataFrame(organized_data)
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier: {str(e)}")
        return None

def calculate_metrics(df):
    """Calcule les métriques financières"""
    # Calcul des soldes
    emplois_total = df['Emplois'].sum()
    ressources_total = df['Ressources'].sum()
    solde_annuel = ressources_total - emplois_total
    
    # Calcul des ratios et indicateurs
    metrics = {
        'Solde annuel': solde_annuel,
        'Total Emplois': emplois_total,
        'Total Ressources': ressources_total,
        'Taux de couverture': (ressources_total / emplois_total * 100) if emplois_total != 0 else 0,
        'Marge de sécurité': solde_annuel if solde_annuel > 0 else 0
    }
    
    return metrics

def calculate_financial_ratios(data_emplois, data_ressources):
    """Calcule les ratios financiers avec leurs formules"""
    ratios = {}
    
    # Calcul des totaux
    total_emplois = sum(data_emplois.values())
    total_ressources = sum(data_ressources.values())
    
    # Taux de couverture = (Total Ressources / Total Emplois) × 100
    ratios['taux_couverture'] = (total_ressources / total_emplois * 100) if total_emplois > 0 else 0
    
    # Ratio d'autonomie financière = (CAF / Total Emplois) × 100
    caf = data_ressources.get('CAF', 0)
    ratios['autonomie'] = (caf / total_emplois * 100) if total_emplois > 0 else 0
    
    # Ratio d'endettement = (Emprunts / Total Ressources) × 100
    emprunts = data_ressources.get('Emprunts LMT', 0)
    ratios['endettement'] = (emprunts / total_ressources * 100) if total_ressources > 0 else 0
    
    return ratios

def display_financial_analysis(data, year):
    """Affiche l'analyse financière pour une année donnée"""
    st.markdown(f"### 📊 Analyse Financière - Année {year}")
    
    # Calcul des ratios avec les dictionnaires complets
    ratios = calculate_financial_ratios(data['Emplois'], data['Ressources'])
    
    # Calculs des totaux
    total_emplois = sum(data['Emplois'].values())
    total_ressources = sum(data['Ressources'].values())
    solde = total_ressources - total_emplois
    
    # Affichage des métriques principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Emplois", f"{total_emplois:,.2f} DA")
    with col2:
        st.metric("Total Ressources", f"{total_ressources:,.2f} DA")
    with col3:
        st.metric("Solde", f"{solde:,.2f} DA")
    
    # Affichage des ratios avec formules
    st.markdown("""
    #### 📐 Ratios Financiers
    
    1. **Taux de Couverture**
    ```
    Taux de Couverture = (Total Ressources / Total Emplois) × 100
    ```
    Résultat: {:.2f}%
    
    2. **Ratio d'Autonomie Financière**
    ```
    Autonomie = (CAF / Total Emplois) × 100
    ```
    Résultat: {:.2f}%
    
    3. **Ratio d'Endettement**
    ```
    Endettement = (Emprunts LMT / Total Ressources) × 100
    ```
    Résultat: {:.2f}%
    """.format(
        ratios['taux_couverture'],
        ratios['autonomie'],
        ratios['endettement']
    ))
    
    # Analyse et recommandations
    st.markdown("#### 📋 Analyse et Recommandations")
    
    # Analyse du taux de couverture
    if ratios['taux_couverture'] >= 100:
        st.success(f"""
        ✅ **Taux de Couverture**: {ratios['taux_couverture']:.2f}%
        - Les ressources couvrent entièrement les emplois
        - Marge de sécurité: {(ratios['taux_couverture'] - 100):.2f}%
        """)
    else:
        st.error(f"""
        ⚠️ **Taux de Couverture**: {ratios['taux_couverture']:.2f}%
        - Déficit de couverture: {(100 - ratios['taux_couverture'])::.2f}%
        - Besoin de financement complémentaire: {(total_emplois - total_ressources):,.2f} DA
        """)
    
    # Analyse de l'autonomie financière
    if ratios['autonomie'] >= 30:
        st.success(f"""
        ✅ **Autonomie Financière**: {ratios['autonomie']:.2f}%
        - Bonne capacité d'autofinancement
        """)
    else:
        st.warning(f"""
        📊 **Autonomie Financière**: {ratios['autonomie']:.2f}%
        - Dépendance aux financements externes
        - Recommandation: Renforcer la CAF
        """)
    
    # Analyse de l'endettement
    if ratios['endettement'] <= 50:
        st.success(f"""
        ✅ **Endettement**: {ratios['endettement']:.2f}%
        - Niveau d'endettement maîtrisé
        """)
    else:
        st.warning(f"""
        📊 **Endettement**: {ratios['endettement']:.2f}%
        - Niveau d'endettement élevé
        - Recommandation: Limiter le recours à l'emprunt
        """)

def create_plan(data, plan_name, num_years):
    """Crée un plan de financement structuré avec des données différentes par année"""
    yearly_data = {}
    
    for year in range(1, num_years + 1):
        yearly_data[f'Année {year}'] = {
            'Emplois': {},
            'Ressources': {}
        }
        for category in EMPLOIS.keys():
            yearly_data[f'Année {year}']['Emplois'][category] = data['Emplois'].get(f'{category}_an{year}', 0)
        for category in RESSOURCES.keys():
            yearly_data[f'Année {year}']['Ressources'][category] = data['Ressources'].get(f'{category}_an{year}', 0)
    
    return {'name': plan_name, 'data': pd.DataFrame.from_dict(yearly_data, orient='index'), 'years': num_years}

def calculate_cumulative_metrics(df):
    """Calcule les métriques cumulées sur plusieurs années"""
    yearly_metrics = []
    cumulative_solde = 0  # Pour suivre le solde cumulé
    
    for idx, row in df.iterrows():
        emplois = sum(row['Emplois'].values())
        ressources = sum(row['Ressources'].values())
        solde_annuel = ressources - emplois
        cumulative_solde += solde_annuel  # Accumulation du solde
        
        yearly_metrics.append({
            'Année': idx,
            'Emplois': emplois,
            'Ressources': ressources,
            'Solde annuel': solde_annuel,
            'Solde cumulé': cumulative_solde,
            'Taux de couverture': (ressources / emplois * 100) if emplois != 0 else 0
        })
    
    return pd.DataFrame(yearly_metrics)

def create_editable_table(num_years):
    """Crée un tableau éditable et dynamique pour le plan de financement"""
    st.markdown("### Tableau de Saisie du Plan de Financement")

    # Initialisation de l'état de session pour les lignes dynamiques
    if 'emplois_rows' not in st.session_state or not isinstance(st.session_state.emplois_rows, list):
        st.session_state.emplois_rows = list(EMPLOIS.keys())
    if 'ressources_rows' not in st.session_state or not isinstance(st.session_state.ressources_rows, list):
        st.session_state.ressources_rows = list(RESSOURCES.keys())

    # --- Exemple réaliste ---
    if st.button("Remplir avec un exemple", key="fill_example"):
        # Exemple de montants pour chaque catégorie et chaque année
        emplois_ex = {
            'Reliquat des plans antérieurs': [500_000, 0, 0, 0, 0],
            'Investissements': [2_000_000, 1_000_000, 500_000, 0, 0],
            'Remboursement emprunts': [0, 200_000, 200_000, 200_000, 200_000],
            'BFR': [300_000, 350_000, 400_000, 450_000, 500_000],
            'Dividendes': [0, 0, 0, 100_000, 150_000],
        }
        ressources_ex = {
            'CAF': [1_500_000, 1_600_000, 1_700_000, 1_800_000, 1_900_000],
            'Subventions': [500_000, 0, 0, 0, 0],
            'Augmentation capital': [1_000_000, 0, 0, 0, 0],
            'Emprunts LMT': [0, 1_000_000, 0, 0, 0],
            'Cessions actifs': [0, 0, 200_000, 0, 0],
            'Prélèvement FR': [0, 0, 0, 0, 0],
        }
        n = num_years
        st.session_state.emplois_data = [
            [cat] + emplois_ex.get(cat, [0]*n)[:n] for cat in st.session_state.emplois_rows
        ]
        st.session_state.ressources_data = [
            [cat] + ressources_ex.get(cat, [0]*n)[:n] for cat in st.session_state.ressources_rows
        ]
        st.rerun()

    # --- Emplois ---
    st.markdown("#### Emplois")
    col_add_emploi, col_btn_emploi = st.columns([4, 1])
    with col_add_emploi:
        new_emploi = st.text_input("Ajouter une catégorie Emploi", key="new_emploi")
    with col_btn_emploi:
        if st.button("Ajouter Emploi"):
            if new_emploi and new_emploi not in st.session_state.emplois_rows:
                st.session_state.emplois_rows.append(new_emploi)
                if "emplois_data" in st.session_state:
                    st.session_state.emplois_data.append([new_emploi] + [0.0] * num_years)
                st.rerun()

    # Construction du DataFrame emplois
    columns = ["Catégorie"] + [f"Année {i+1}" for i in range(num_years)]
    if "emplois_data" not in st.session_state or len(st.session_state.emplois_data) != len(st.session_state.emplois_rows):
        st.session_state.emplois_data = [
            [cat] + [0.0] * num_years for cat in st.session_state.emplois_rows
        ]
    emplois_df = pd.DataFrame(st.session_state.emplois_data, columns=columns)
    edited_emplois = st.data_editor(
        emplois_df,
        key="emplois_editor",
        num_rows="dynamic",
        column_config={
            "Catégorie": st.column_config.TextColumn(
                "Catégorie",
                help="Type d'emploi",
                width="medium",
                disabled=True
            ),
            **{
                f"Année {i+1}": st.column_config.NumberColumn(
                    f"Année {i+1}",
                    help=f"Montant pour l'année {i+1}",
                    min_value=0,
                    format="%.2f DA"
                )
                for i in range(num_years)
            }
        }
    )
    st.session_state.emplois_data = edited_emplois.values.tolist()

    # --- Ressources ---
    st.markdown("#### Ressources")
    col_add_res, col_btn_res = st.columns([4, 1])
    with col_add_res:
        new_ressource = st.text_input("Ajouter une catégorie Ressource", key="new_ressource")
    with col_btn_res:
        if st.button("Ajouter Ressource"):
            if new_ressource and new_ressource not in st.session_state.ressources_rows:
                st.session_state.ressources_rows.append(new_ressource)
                if "ressources_data" in st.session_state:
                    st.session_state.ressources_data.append([new_ressource] + [0.0] * num_years)
                st.rerun()

    if "ressources_data" not in st.session_state or len(st.session_state.ressources_data) != len(st.session_state.ressources_rows):
        st.session_state.ressources_data = [
            [cat] + [0.0] * num_years for cat in st.session_state.ressources_rows
        ]
    ressources_df = pd.DataFrame(st.session_state.ressources_data, columns=columns)
    edited_ressources = st.data_editor(
        ressources_df,
        key="ressources_editor",
        num_rows="dynamic",
        column_config={
            "Catégorie": st.column_config.TextColumn(
                "Catégorie",
                help="Type de ressource",
                width="medium",
                disabled=True
            ),
            **{
                f"Année {i+1}": st.column_config.NumberColumn(
                    f"Année {i+1}",
                    help=f"Montant pour l'année {i+1}",
                    min_value=0,
                    format="%.2f DA"
                )
                for i in range(num_years)
            }
        }
    )
    st.session_state.ressources_data = edited_ressources.values.tolist()

    return edited_emplois, edited_ressources

def calculate_comparative_metrics(metrics, plan_data):
    """Calcule les métriques comparatives pour un plan"""
    total_emplois = metrics['Emplois'].sum()
    total_ressources = metrics['Ressources'].sum()
    
    # Calcul des valeurs CAF et Emprunts depuis les données du plan
    total_caf = sum(year_data['Ressources'].get('CAF', 0) 
                   for _, year_data in plan_data['data'].iterrows())
    total_emprunts = sum(year_data['Ressources'].get('Emprunts LMT', 0) 
                        for _, year_data in plan_data['data'].iterrows())
    
    return {
        'Plan': metrics['Plan'].iloc[0],
        'Solde cumulé final': metrics['Solde cumulé'].iloc[-1],
        'Taux couverture moyen': metrics['Taux de couverture'].mean(),
        'Autonomie financière': (total_caf / total_emplois * 100) if total_emplois > 0 else 0,
        'Endettement moyen': (total_emprunts / total_ressources * 100) if total_ressources > 0 else 0,
        'Total Emplois': total_emplois,
        'Total Ressources': total_ressources
    }

def comparative_analysis():
    """Analyse comparative des plans"""

    
    if len(st.session_state.plans) < 2:
        st.warning("⚠️ Créez au moins deux plans pour effectuer une comparaison")
        return
        
    selected_plans = st.multiselect(
        "Sélectionner les plans à comparer",
        options=[p['name'] for p in st.session_state.plans],
        default=[p['name'] for p in st.session_state.plans[:2]]
    )
    
    if selected_plans:
        tab1, tab2, tab3 = st.tabs(["📈 Évolution", "📊 Comparaison", "📋 Recommandations"])
        
        comparison_data = []
        metrics_data = []
        for plan_name in selected_plans:
            plan = next(p for p in st.session_state.plans if p['name'] == plan_name)
            metrics = calculate_cumulative_metrics(plan['data'])
            metrics['Plan'] = plan_name
            comparison_data.append(metrics)
            metrics_data.append(calculate_comparative_metrics(metrics, plan))
        
        comparison_df = pd.DataFrame(metrics_data)
        
        with tab1:
            # Graphiques d'évolution
            fig1 = go.Figure()
            for metrics in comparison_data:
                fig1.add_trace(go.Scatter(
                    x=metrics['Année'],
                    y=metrics['Solde cumulé'],
                    name=f"{metrics['Plan']}",
                    mode='lines+markers'
                ))
            fig1.update_layout(
                title="Évolution des Soldes Cumulés",
                xaxis_title="Année",
                yaxis_title="Montant (DA)",
                height=500
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = go.Figure()
            for metrics in comparison_data:
                fig2.add_trace(go.Bar(
                    x=metrics['Année'],
                    y=metrics['Taux de couverture'],
                    name=f"{metrics['Plan']}"
                ))
            fig2.update_layout(
                title="Taux de Couverture par Année",
                xaxis_title="Année",
                yaxis_title="Taux (%)",
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)

        with tab2:
            st.markdown("### Tableau Comparatif")
            st.dataframe(
                comparison_df.style.format({
                    'Solde cumulé final': '{:,.2f} DA',
                    'Taux couverture moyen': '{:.1f}%',
                    'Autonomie financière': '{:.1f}%',
                    'Endettement moyen': '{:.1f}%',
                    'Total Emplois': '{:,.2f} DA',
                    'Total Ressources': '{:,.2f} DA'
                }),
                height=200
            )

        with tab3:
            # Analyse et recommandations
            # 1. Éliminer les plans à solde cumulé final négatif
            valid_plans = comparison_df[comparison_df['Solde cumulé final'] >= 0].copy()
            # 2. Appliquer les critères financiers
            valid_plans = valid_plans[
                (valid_plans['Taux couverture moyen'] >= 100) &
                (valid_plans['Autonomie financière'] >= 30) &
                (valid_plans['Endettement moyen'] <= 50)
            ]
            if not valid_plans.empty:
                # 3. Choisir celui avec le meilleur solde cumulé final
                best_plan = valid_plans.loc[valid_plans['Solde cumulé final'].idxmax()]
                st.success(f"""
                ### 📌 Analyse Comparative
                Le plan **{best_plan['Plan']}** est recommandé car il respecte les grands équilibres financiers :
                - Solde cumulé final positif ({best_plan['Solde cumulé final']:,.2f} DA)
                - Taux de couverture moyen ≥ 100 % ({best_plan['Taux couverture moyen']:.1f} %)
                - Autonomie financière ≥ 30 % ({best_plan['Autonomie financière']:.1f} %)
                - Endettement moyen ≤ 50 % ({best_plan['Endettement moyen']:.1f} %)
                """)
            else:
                # 4. Sinon, recommander le plan le moins risqué
                # Critère : solde cumulé final le moins négatif, puis endettement le plus faible
                fallback = comparison_df.copy()
                fallback = fallback.sort_values(['Solde cumulé final', 'Endettement moyen'], ascending=[False, True])
                best_plan = fallback.iloc[0]
                st.warning(f"""
                ### 📌 Analyse Comparative
                Aucun plan ne respecte tous les équilibres financiers recommandés.
                Le plan **{best_plan['Plan']}** est le moins risqué parmi les options :
                - Solde cumulé final : {best_plan['Solde cumulé final']:,.2f} DA
                - Taux de couverture moyen : {best_plan['Taux couverture moyen']:.1f} %
                - Autonomie financière : {best_plan['Autonomie financière']:.1f} %
                - Endettement moyen : {best_plan['Endettement moyen']:.1f} %
                """)
            st.info("La recommandation prend en compte le solde cumulé, le taux de couverture, l'autonomie financière et l'endettement, conformément aux principes comptables et financiers.")

def display_financial_summary_table(plan_data):
    """Affiche un tableau récapitulatif multi-années avec totaux et soldes"""
    years = [f"Année {i+1}" for i in range(plan_data['years'])]
    emplois = plan_data['data'].apply(lambda row: pd.Series(row['Emplois']), axis=1).T
    ressources = plan_data['data'].apply(lambda row: pd.Series(row['Ressources']), axis=1).T
    emplois.columns = years
    ressources.columns = years
    emplois['Type'] = 'Emplois'
    ressources['Type'] = 'Ressources'
    emplois = emplois.reset_index().rename(columns={'index': 'Catégorie'})
    ressources = ressources.reset_index().rename(columns={'index': 'Catégorie'})
    # Calcul du solde par année
    total_emplois = emplois[years].sum()
    total_ressources = ressources[years].sum()
    solde = total_ressources - total_emplois
    # DataFrame final
    df = pd.concat([emplois, ressources], ignore_index=True)
    df_totaux = pd.DataFrame({
        'Catégorie': ['Total Emplois', 'Total Ressources', 'Solde'],
        'Type': ['', '', ''],
        **{year: [total_emplois[year], total_ressources[year], solde[year]] for year in years}
    })
    df = pd.concat([df, df_totaux], ignore_index=True)
    # Format DA
    for year in years:
        df[year] = df[year].apply(lambda x: f"{x:,.2f} DA" if pd.notnull(x) else "")
    # Style sobre
    def style_rows(row):
        if row['Catégorie'] in ['Total Emplois', 'Total Ressources', 'Solde']:
            return ['background-color: #ececec; font-weight: bold; color: #222;' for _ in row]
        elif row.name == 0 or row['Type'] == 'Emplois' or row['Type'] == 'Ressources':
            return ['background-color: #f7f7f7; color: #222;' for _ in row]
        else:
            return ['' for _ in row]
    st.markdown('### Tableau récapitulatif multi-années')
    st.dataframe(df.style.apply(style_rows, axis=1), height=500)

def display_financial_classic_tables(plan_data):
    """Affiche les Emplois puis les Ressources puis le solde, avec sections bien séparées et un style sobre"""
    years = [f"Année {i+1}" for i in range(plan_data['years'])]
    # Emplois
    emplois = plan_data['data'].apply(lambda row: pd.Series(row['Emplois']), axis=1).T
    emplois.columns = years
    emplois = emplois.fillna(0)
    emplois['Total'] = emplois.sum(axis=1)
    emplois = emplois.reset_index().rename(columns={'index': 'Catégorie'})
    total_emplois = emplois[years].sum()
    emplois.loc[len(emplois)] = ['Total'] + list(total_emplois) + [total_emplois.sum()]
    # Ressources
    ressources = plan_data['data'].apply(lambda row: pd.Series(row['Ressources']), axis=1).T
    ressources.columns = years
    ressources = ressources.fillna(0)
    ressources['Total'] = ressources.sum(axis=1)
    ressources = ressources.reset_index().rename(columns={'index': 'Catégorie'})
    total_ressources = ressources[years].sum()
    ressources.loc[len(ressources)] = ['Total'] + list(total_ressources) + [total_ressources.sum()]
    # Solde par année (en colonnes)
    solde = total_ressources - total_emplois
    solde_total = solde.sum()
    solde_row = pd.DataFrame([['Solde'] + list(solde) + [solde_total]], columns=['Catégorie'] + years + ['Total'])
    # Format DA
    for year in years + ['Total']:
        emplois[year] = emplois[year].apply(lambda x: f"{x:,.2f} DA" if pd.notnull(x) else "")
        ressources[year] = ressources[year].apply(lambda x: f"{x:,.2f} DA" if pd.notnull(x) else "")
        solde_row[year] = solde_row[year].apply(lambda x: f"{x:,.2f} DA" if pd.notnull(x) else "")
    # Style sobre
    def style_table(row):
        if row['Catégorie'] == 'Total' or row['Catégorie'] == 'Solde':
            return ['background-color: #ececec; font-weight: bold; color: #222;' for _ in row]
        else:
            return ['' for _ in row]
    st.markdown('### Emplois (Besoins)')
    st.dataframe(emplois.style.apply(style_table, axis=1), height=350)
    st.markdown('### Ressources')
    st.dataframe(ressources.style.apply(style_table, axis=1), height=350)
    st.markdown('### Solde par année')
    st.dataframe(solde_row.style.apply(style_table, axis=1), height=80)

def main():
    menu_choice = show_menu()
    
    if menu_choice == "Plan de Financement":
        st.markdown("""
        # 📝 Plan de Financement
        ### Saisissez les données de votre plan
        """)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            num_years = st.number_input("Nombre d'années du plan", 1, 5, 3)
        with col2:
            plan_name = st.text_input("Nom du plan", "Plan 1")
        
        # Création du tableau éditable
        emplois_df, ressources_df = create_editable_table(num_years)
        
        if st.button("Créer le Plan", type="primary"):
            # Conversion des données du tableau en format plan
            plan_data = {
                'Emplois': {},
                'Ressources': {}
            }
            
            # Traitement des emplois
            for idx, row in emplois_df.iterrows():
                category = row['Catégorie']
                for year in range(num_years):
                    plan_data['Emplois'][f'{category}_an{year+1}'] = row[f'Année {year+1}']
            
            # Traitement des ressources
            for idx, row in ressources_df.iterrows():
                category = row['Catégorie']
                for year in range(num_years):
                    plan_data['Ressources'][f'{category}_an{year+1}'] = row[f'Année {year+1}']
            
            plan = create_plan(plan_data, plan_name, num_years)
            st.session_state.plans.append(plan)
            st.success(f"Plan '{plan_name}' créé avec succès!")
            
            # Affichage classique : Emplois, puis Ressources, puis Solde par année
            display_financial_classic_tables(plan)

    elif menu_choice == "Analyse Financière":
        st.markdown("""
        # 📊 Analyse Financière
        Analysez en détail votre plan de financement
        """)
        
        if not st.session_state.plans:
            st.warning("Aucun plan n'a été créé. Veuillez d'abord créer un plan.")
            return
        
        plan_to_analyze = st.selectbox(
            "Sélectionner le plan à analyser",
            options=[p['name'] for p in st.session_state.plans]
        )
        
        if plan_to_analyze:
            plan = next(p for p in st.session_state.plans if p['name'] == plan_to_analyze)
            
            # Affichage du tableau pour chaque année
            for year in range(1, plan['years'] + 1):
                year_data = {
                    'Emplois': plan['data'].loc[f'Année {year}', 'Emplois'],
                    'Ressources': plan['data'].loc[f'Année {year}', 'Ressources']
                }
                display_financial_table(year_data, year)
                display_financial_analysis(year_data, year)
                
                st.markdown("---")
            
            if st.button("Générer le rapport PDF général", key="pdf_global"):
                pdf = PDF()
                pdf.add_page()
                pdf.set_fill_color(*COLOR_BG)
                pdf.rect(0, 0, 210, 297, 'F')
                pdf.set_font("Arial", "B", 22)
                pdf.set_text_color(*COLOR_PRIMARY)
                pdf.cell(0, 60, "", ln=True)  # Espace vertical
                pdf.cell(0, 18, "Rapport d'Analyse Financière", ln=True, align="C")
                pdf.set_font("Arial", "", 16)
                pdf.cell(0, 12, f"Plan : {plan_to_analyze}", ln=True, align="C")
                pdf.set_font("Arial", "I", 12)
                pdf.cell(0, 10, f"Généré le : {datetime.now().strftime('%d/%m/%Y à %H:%M')}", ln=True, align="C")
                pdf.ln(10)
                pdf.set_font("Arial", "", 12)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(0, 10, "Ce rapport présente une synthèse détaillée du plan de financement sélectionné, incluant les tableaux, graphiques, ratios et recommandations pour une meilleure prise de décision.")
                pdf.set_text_color(0, 0, 0)
                pdf.add_page()
                
                # --- Préparation des données ---
                years = [f"Année {i+1}" for i in range(plan['years'])]
                emplois = [sum(plan['data'].loc[year, 'Emplois'].values()) for year in years]
                ressources = [sum(plan['data'].loc[year, 'Ressources'].values()) for year in years]
                solde = [r - e for r, e in zip(ressources, emplois)]
                solde_cumule = [sum(solde[:i+1]) for i in range(len(solde))]
                taux_couverture = [(r / e * 100) if e != 0 else 0 for r, e in zip(ressources, emplois)]
                
                # --- Fonction de section ---
                def section_title(title, color=COLOR_PRIMARY, align="L"):
                    pdf.ln(6)
                    pdf.set_font("Arial", "B", 15)
                    pdf.set_text_color(*color)
                    if align == "C":
                        pdf.cell(0, 12, title, ln=True, align="C")
                    else:
                        pdf.cell(0, 12, title, ln=True)
                    pdf.set_text_color(0,0,0)
                    pdf.set_draw_color(*color)
                    pdf.set_line_width(0.7)
                    y = pdf.get_y()
                    pdf.line(10, y, 200, y)
                    pdf.ln(4)
                
                # --- Tableau Emplois ---
                section_title("Tableau Emplois (Besoins)")
                pdf.set_font("Arial", "", 11)
                emplois_categories = list(plan['data'].loc[years[0], 'Emplois'].keys())
                pdf.cell(60, 8, "Catégorie", 1, 0, "C", fill=True)
                for year in years:
                    pdf.cell(30, 8, year, 1, 0, "C", fill=True)
                pdf.ln()
                for cat in emplois_categories:
                    pdf.cell(60, 8, cat, 1)
                    for year in years:
                        val = plan['data'].loc[year, 'Emplois'].get(cat, 0)
                        pdf.cell(30, 8, f"{val:,.0f}", 1, 0, "R")
                    pdf.ln()
                pdf.ln(3)
                
                # --- Tableau Ressources ---
                section_title("Tableau Ressources")
                pdf.set_font("Arial", "", 11)
                ressources_categories = list(plan['data'].loc[years[0], 'Ressources'].keys())
                pdf.cell(60, 8, "Catégorie", 1, 0, "C", fill=True)
                for year in years:
                    pdf.cell(30, 8, year, 1, 0, "C", fill=True)
                pdf.ln()
                for cat in ressources_categories:
                    pdf.cell(60, 8, cat, 1)
                    for year in years:
                        val = plan['data'].loc[year, 'Ressources'].get(cat, 0)
                        pdf.cell(30, 8, f"{val:,.0f}", 1, 0, "R")
                    pdf.ln()
                pdf.ln(3)
                
                # --- Tableau Solde par année ---
                section_title("Solde par année")
                pdf.set_font("Arial", "", 11)
                pdf.cell(30, 8, "Année", 1, 0, "C", fill=True)
                pdf.cell(40, 8, "Emplois", 1, 0, "C", fill=True)
                pdf.cell(40, 8, "Ressources", 1, 0, "C", fill=True)
                pdf.cell(40, 8, "Solde", 1, 0, "C", fill=True)
                pdf.cell(40, 8, "Taux Couverture (%)", 1, 0, "C", fill=True)
                pdf.ln()
                for i, year in enumerate(years):
                    pdf.cell(30, 8, year, 1)
                    pdf.cell(40, 8, f"{emplois[i]:,.0f}", 1, 0, "R")
                    pdf.cell(40, 8, f"{ressources[i]:,.0f}", 1, 0, "R")
                    pdf.cell(40, 8, f"{solde[i]:,.0f}", 1, 0, "R")
                    pdf.cell(40, 8, f"{taux_couverture[i]:.1f}", 1, 0, "R")
                    pdf.ln()
                pdf.ln(3)
                
                # --- Graphiques ---
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                    plt.figure(figsize=(7, 4))
                    plt.plot(years, solde_cumule, marker='o', color="#2ca02c")
                    plt.title("Évolution du Solde cumulé")
                    plt.xlabel("Année")
                    plt.ylabel("Montant (DA)")
                    plt.grid(True, linestyle="--", alpha=0.5)
                    plt.tight_layout()
                    plt.savefig(tmpfile.name)
                    plt.close()
                    tmpfile_path = tmpfile.name
                
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile2:
                    plt.figure(figsize=(7, 4))
                    plt.bar(years, taux_couverture, color="#1f77b4")
                    plt.title("Taux de Couverture par Année")
                    plt.xlabel("Année")
                    plt.ylabel("Taux (%)")
                    plt.ylim(0, max(110, max(taux_couverture) + 10))
                    plt.grid(axis='y', linestyle="--", alpha=0.5)
                    plt.tight_layout()
                    plt.savefig(tmpfile2.name)
                    plt.close()
                    tmpfile2_path = tmpfile2.name
                
                pdf.ln(5)
                section_title("Graphique : Évolution du Solde cumulé", color=COLOR_SECONDARY, align="C")
                pdf.image(tmpfile_path, w=170, x=20)
                pdf.ln(5)
                section_title("Graphique : Taux de Couverture par Année", color=COLOR_SECONDARY, align="C")
                pdf.image(tmpfile2_path, w=170, x=20)
                
                os.unlink(tmpfile_path)
                os.unlink(tmpfile2_path)
                
                # --- Analyse et Recommandations ---
                pdf.add_page()
                section_title("Analyse et Recommandations", color=COLOR_ACCENT)
                pdf.set_font("Arial", "", 12)
                pdf.set_text_color(0,0,0)
                
                for i, year in enumerate(years):
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, f"{year} :", ln=True)
                    pdf.set_font("Arial", "", 11)
                    if taux_couverture[i] >= 100:
                        pdf.set_text_color(*COLOR_SECONDARY)
                        pdf.multi_cell(0, 8, f"[OK] Taux de Couverture : {taux_couverture[i]:.2f}%\n- Les ressources couvrent les emplois.\n- Marge de sécurité : {taux_couverture[i] - 100:.2f}%")
                    else:
                        pdf.set_text_color(*COLOR_ACCENT)
                        pdf.multi_cell(0, 8, f"[Attention] Taux de Couverture : {taux_couverture[i]::.2f}%\n- Déficit de couverture : {100 - taux_couverture[i]:.2f}%\n- Besoin de financement complémentaire : {emplois[i] - ressources[i]:,.0f} DA")
                    pdf.set_text_color(0,0,0)
                    pdf.ln(2)
                
                # --- Téléchargement ---
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                    pdf.output(tmpfile.name)
                    with open(tmpfile.name, "rb") as f:
                        st.download_button(
                            label="📥 Télécharger le rapport PDF général",
                            data=f,
                            file_name=f"rapport_analyse_financiere_{plan_to_analyze}.pdf",
                            mime="application/pdf"
                        )


    elif menu_choice == "Étude Comparative":
        st.markdown("""
        # 🔄 Étude Comparative
        Comparez différents plans de financement
        """)
        
        if len(st.session_state.plans) < 2:
            st.warning("⚠️ Créez au moins deux plans pour effectuer une comparaison")
            return
        
        comparative_analysis()

if __name__ == "__main__":
    main()