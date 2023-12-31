import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Charger les données à partir du fichier Excel

uploaded_file = st.file_uploader("Choisissez le fichier Excel 'Data F-V'", type="xlsx")
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file, decimal='.')
else:
    st.warning("Veuillez charger un fichier Excel 'Data F-V'.")

st.title("Interprétation des profils F-V")
st.subheader("Graphique en quadrants des qualités de V0 et de F0 des joueurs par équipe et/ou par poste")

# Filtrer par équipe et poste
equipes_selectionnees = st.multiselect('Sélectionnez les équipes', data['Equipes'].unique())
if equipes_selectionnees:
    data = data[data['Equipes'].isin(equipes_selectionnees)]

postes_selectionnes = st.multiselect('Sélectionnez les postes', data['Poste'].unique())
if postes_selectionnes:
    data = data[data['Poste'].isin(postes_selectionnes)]

# Filtrer par numéro de sprint
num_sprint_selectionne = st.multiselect('Sélectionnez le numéro de sprint', options=data['Num Sprint'].unique())
if num_sprint_selectionne:
    data = data[data['Num Sprint'].isin(num_sprint_selectionne)]

date_test = st.multiselect('Sélectionnez la date du test', options=data['Date du test'].unique())
if date_test:
    data=data[data['Date du test'].isin(date_test)]

# Valeurs prédéfinies pour F0 et V0
F0_predit = 7.7
V0_predit = 9.2

# Extraire les colonnes V0, F0 et "NOM Prénom"
V0 = data["V0 (m/s)"]
F0 = data["F0 (N/kg)"]
noms = data["NOM Prénom"]

nom = data["NOM"]



# Créer un premier graphique avec 4 quadrants basés sur les valeurs prédéfinies
fig1, ax1 = plt.subplots()

# Quadrant 1 (en haut à droite)
quadrant1 = (V0 > V0_predit) & (F0 > F0_predit)
ax1.scatter(V0[quadrant1], F0[quadrant1], label='Quadrant 1')

# Quadrant 2 (en haut à gauche)
quadrant2 = (V0 <= V0_predit) & (F0 > F0_predit)
ax1.scatter(V0[quadrant2], F0[quadrant2], label='Quadrant 2')

# Quadrant 3 (en bas à droite)
quadrant3 = (V0 > V0_predit) & (F0 <= F0_predit)
ax1.scatter(V0[quadrant3], F0[quadrant3], label='Quadrant 3')

# Quadrant 4 (en bas à gauche)
quadrant4 = (V0 <= V0_predit) & (F0 <= F0_predit)
ax1.scatter(V0[quadrant4], F0[quadrant4], label='Quadrant 4')

# Ajouter des lignes pointillées pour délimiter les quadrants
ax1.axhline(F0_predit, linestyle='--', color='gray', label='Limite F0')
ax1.axvline(V0_predit, linestyle='--', color='gray', label='Limite V0')

# Ajouter des étiquettes d'axes
ax1.set_xlabel('V0 (m/s)')
ax1.set_ylabel('F0 (N/kg)')

# Ajouter des étiquettes pour chaque point avec les noms des joueurs
afficher_etiquettes = st.checkbox("Afficher les étiquettes des noms des joueurs sur le graphique 1", value=True)
if afficher_etiquettes:
    for nom, x, y in zip(nom, V0, F0):
        ax1.annotate(nom, (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=5)

# Afficher le premier graphique dans Streamlit
st.pyplot(fig1)
st.text("Les valeurs utilisées pour définir les quadrants sont les valeurs moyennes")
st.text("trouvées dans la littérature pour des joueurs de foot pro.")
st.text("F0 = 7.7 N/kg & V0 = 9.2 m/s")

st.subheader("Graphique en nuage de points des données individuelles de V0 et de F0")

# Liste de tous les noms/prénoms (sans doublons)
options_nom_prenom = data['NOM'].drop_duplicates().tolist()

# Afficher la liste déroulante avec toutes les options
nom_prenom_selectionne = st.multiselect("Sélectionnez un NOM Prénom", options=options_nom_prenom)

#filtre numéro de sprint
#options_num_sprint = data ['Num Sprint'].drop_duplicates().to_list()
#num_sprint = st.multiselect('Sélectionnez un numéro de sprint', options=options_num_sprint)
#if num_sprint:
#    data=data[data['Num Sprint'].isin(num_sprint)]

#filtre date du test
#option_date_test = data ['Date du test'].drop_duplicates().to_list()
#date_test_select = st.multiselect('Sélectionnez la date du test', options = option_date_test, key="date_test_select_unique_key")
#if date_test_select:
#    data=data[data['Date du test'].isin(date_test_select)]

# Créer un deuxième graphique en nuage de points
if nom_prenom_selectionne:
    # Filtrer les données en fonction de la sélection
    data_selectionnee = data[data['NOM'].isin(nom_prenom_selectionne)]
    
    # Extraire les colonnes V0, F0 et "NOM Prénom" pour le deuxième graphique
    V0_selectionne = data_selectionnee["V0 (m/s)"]
    F0_selectionne = data_selectionnee["F0 (N/kg)"]
    noms_selectionne = data_selectionnee["NOM"]

    fig2, ax2 = plt.subplots()

    # Nuage de points
    ax2.scatter(V0_selectionne, F0_selectionne, label='Profil F-V')

# Ajouter des lignes pointillées pour délimiter les quadrants
    ax2.axhline(F0_predit, linestyle='--', color='gray', label='Limite F0')
    ax2.axvline(V0_predit, linestyle='--', color='gray', label='Limite V0')

    # Ajouter des étiquettes d'axes
    ax2.set_xlabel('V0 (m/s)')
    ax2.set_ylabel('F0 (N/kg)')

    # Ajouter des étiquettes pour chaque point avec les noms des joueurs
    for nom, x, y in zip(noms_selectionne, V0_selectionne, F0_selectionne):
        ax2.annotate(nom, (x, y), textcoords="offset points", xytext=(0, 5), ha='center')

    # Afficher le deuxième graphique dans Streamlit
    st.pyplot(fig2)






def force_velocity_graph(player_data):
    V0 = player_data["V0 (m/s)"]
    F0 = player_data["F0 (N/kg)"]

    # Calcul des coefficients de la droite linéaire
    m, c = np.polyfit([0, V0], [F0, 0], 1)

    # Création des données pour la droite linéaire
    x_line = np.linspace(0, V0, 100)
    y_line = m * x_line + c

    # Créer une nouvelle figure et de nouveaux axes
    fig, ax = plt.subplots()

    # Tracer du graphique
    ax.plot([0, V0], [F0, 0], 'o')
    ax.plot(x_line, y_line)

    # Configurations du graphique
    ax.set_xlabel('Vitesse (m/s)')
    ax.set_ylabel('Force (N/kg)')
    ax.legend()

# Définir les limites des axes pour inclure zéro
    ax.set_xlim(0, max(V0, V0_predit))
    ax.set_ylim(0, max(F0, F0_predit))
    return fig

def main():
    st.subheader('Relation Force-Vitesse')

    # Liste déroulante pour sélectionner des joueurs
    #players_without_duplicates = data['NOM'].drop_duplicates()
    #selected_players = st.multiselect('Sélectionnez des joueurs', options=players_without_duplicates)

    # Liste déroulante pour sélectionner une date
    #selected_date = st.selectbox('Sélectionnez la date du test', options=data['Date du test'].drop_duplicates())

    # Liste déroulante pour sélectionner un numéro de sprint
    #selected_sprint = st.selectbox('Sélectionnez un numéro de sprint', options=data['Num Sprint'].drop_duplicates())


    if nom_prenom_selectionne: # and selected_date and selected_sprint:
        # Convertir la colonne 'Date du test' en type datetime si elle ne l'est pas déjà
        data['Date du test'] = pd.to_datetime(data['Date du test'])

        # Filtrer les données en fonction des sélections
        selected_data = data[(data['NOM'].isin(nom_prenom_selectionne))]# & (data['Date du test'] == selected_date) & (data['Num Sprint'] == selected_sprint)]

        # Créer une seule figure pour tous les joueurs sélectionnés
        fig, ax = plt.subplots()

        # Liste pour stocker les données de chaque joueur
        lines = []

        # Ajouter les courbes de chaque joueur à la liste
        for _, player_data in selected_data.iterrows():
            lines.extend(force_velocity_graph(player_data, ax))

        # Configurations du graphique
        ax.set_xlabel('Vitesse (m/s)')
        ax.set_ylabel('Force (N/kg)')

        # Tracer toutes les courbes en une seule fois
        for line in lines:
            ax.plot(line['x'], line['y'], '-', label=line['label'])

        ax.legend()

        # Affichage du graphique à l'aide de st.pyplot
        st.pyplot(fig)

def force_velocity_graph(player_data, ax):
    V0 = player_data["V0 (m/s)"]
    F0 = player_data["F0 (N/kg)"]

    # Calcul des coefficients de la droite linéaire
    m, c = np.polyfit([0, V0], [F0, 0], 1)

    # Création des données pour la droite linéaire
    x_line = np.linspace(0, V0, 100)
    y_line = m * x_line + c

    # Création d'une structure pour stocker les données du joueur
    player_line = {
        'x': x_line,
        'y': y_line,
        'label': player_data['NOM'] 
    }

    return [player_line]

if __name__ == "__main__":
    main()
