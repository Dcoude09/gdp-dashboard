# plan_repas.py
import streamlit as st
import random

# ─────────────────────────────────────────────────────────────
# 1. Base d'aliments : macro-nutriments pour 100 g + instructions rapides
#    (ajoute ou modifie librement les aliments selon tes besoins)
# ─────────────────────────────────────────────────────────────
aliments = {
    "poulet_grille": {
        "calories": 165, "proteines": 31, "lipides": 3.6,
        "glucides": 0, "fibres": 0,
        "tags": [],
        "prep": "Assaisonner 150 g de blanc de poulet (sel, poivre, herbes) et griller "
                "5 min de chaque côté à feu moyen-vif jusqu’à 74 °C à cœur."
    },
    "cabillaud": {
        "calories": 82, "proteines": 18, "lipides": 0.7,
        "glucides": 0, "fibres": 0,
        "tags": ["poisson_blanc"],
        "prep": "Placer le filet dans un plat, arroser de jus de citron, sel, poivre, herbes. "
                "Cuire 15-20 min à 180 °C."
    },
    "tofu": {
        "calories": 76, "proteines": 8, "lipides": 4.8,
        "glucides": 1.9, "fibres": 0.3,
        "tags": [],
        "prep": "Presser le tofu 10 min. Mariner (sauce soja, ail, gingembre) 30 min, puis "
                "saisir 4 min par face."
    },
    "quinoa": {
        "calories": 120, "proteines": 4.4, "lipides": 1.9,
        "glucides": 21.3, "fibres": 2.8,
        "tags": [],
        "prep": "Rincer 1 volume de quinoa. Cuire dans 2 volumes d’eau bouillante 12-15 min, "
                "puis égoutter."
    },
    "riz_complet": {
        "calories": 112, "proteines": 2.6, "lipides": 0.9,
        "glucides": 23, "fibres": 1.8,
        "tags": [],
        "prep": "Rincer, puis cuire 1 volume de riz complet dans 2 volumes d’eau 35-40 min."
    },
    "brocolis": {
        "calories": 34, "proteines": 2.8, "lipides": 0.4,
        "glucides": 6.6, "fibres": 2.6,
        "tags": [],
        "prep": "Cuire les fleurons 5-6 min à la vapeur (croquant) ou 8-9 min (fondant)."
    },
    "patate_douce": {
        "calories": 86, "proteines": 1.6, "lipides": 0.1,
        "glucides": 20.1, "fibres": 3,
        "tags": [],
        "prep": "Éplucher, couper en dés. Cuire 20 min à l’eau bouillante ou rôtir 25 min "
                "à 200 °C avec un filet d’huile."
    },
    "lentilles_cuites": {
        "calories": 116, "proteines": 9, "lipides": 0.4,
        "glucides": 20, "fibres": 8,
        "tags": [],
        "prep": "Rincer les lentilles corail, cuire 15 min dans 3 volumes d’eau. "
                "Assaisonner (sel, curry, herbes)."
    },
    "amandes": {
        "calories": 579, "proteines": 21, "lipides": 50,
        "glucides": 22, "fibres": 12,
        "tags": ["noix"],
        "prep": "À consommer nature (30 g ≈ 1 poignée) ou concassées sur un plat/salade."
    },
    "huile_olive": {
        "calories": 884, "proteines": 0, "lipides": 100,
        "glucides": 0, "fibres": 0,
        "tags": [],
        "prep": "Ajouter 1 c. à s. (≈ 10 g) en assaisonnement ou pour cuisson douce."
    },
    # Allergènes à exclure si cochés
    "oeuf": {
        "calories": 155, "proteines": 13, "lipides": 11,
        "glucides": 1.1, "fibres": 0,
        "tags": ["oeuf"],
        "prep": "Cuire 7 min à l’eau bouillante (œuf mollet) ou 9-10 min (dur)."
    },
    "saumon": {  # poisson gras
        "calories": 208, "proteines": 20, "lipides": 13,
        "glucides": 0, "fibres": 0,
        "tags": ["poisson_gras"],
        "prep": "Cuire au four 15 min à 180 °C ou poêler 4 min par face."
    },
    "crevettes": {  # fruit de mer
        "calories": 99, "proteines": 24, "lipides": 0.3,
        "glucides": 0.2, "fibres": 0,
        "tags": ["fruit_de_mer"],
        "prep": "Sauter 3 min dans une poêle chaude avec ail & huile."
    },
    "arachides": {  # allergène
        "calories": 567, "proteines": 25, "lipides": 49,
        "glucides": 16, "fibres": 8.5,
        "tags": ["arachide"],
        "prep": "À grignoter nature ou en purée (beurre de cacahuète)."
    },
    "moutarde": {  # allergène
        "calories": 66, "proteines": 4.4, "lipides": 4.4,
        "glucides": 5.8, "fibres": 3.3,
        "tags": ["moutarde"],
        "prep": "Utiliser 1-2 c. à c. pour relever les sauces/vinaigrettes."
    },
}

# Dictionnaire allergènes <libellé affiché> : <tag interne>
allergenes_possibles = {
    "Œufs": "oeuf",
    "Arachides": "arachide",
    "Moutarde": "moutarde",
    "Poissons gras": "poisson_gras",
    "Fruits de mer": "fruit_de_mer",
    "Noix (ex : amandes)": "noix"
}

# ─────────────────────────────────────────────────────────────
# 2. Fonctions utilitaires
# ─────────────────────────────────────────────────────────────
def filtrer_aliments(tags_allergies):
    """Retourne la liste des aliments autorisés (aucun tag interdit)."""
    return [
        nom for nom, data in aliments.items()
        if not any(tag in tags_allergies for tag in data["tags"])
    ]

def generer_repas(cal_cible, alim_autorises):
    """Sélectionne 4 aliments et ajuste la portion pour approcher cal_cible."""
    if len(alim_autorises) < 4:
        return [], {k: 0 for k in ["calories", "proteines", "lipides", "glucides", "fibres"]}
    choix = random.sample(alim_autorises, 4)
    total = {k: 0 for k in ["calories", "proteines", "lipides", "glucides", "fibres"]}
    repas = []
    for alim in choix:
        portion = round((cal_cible / 4) / aliments[alim]["calories"] * 100)  # g
        repas.append((alim, portion))
        for k in total:
            total[k] += aliments[alim][k] * portion / 100
    return repas, total

def afficher_repas(repas, total):
    """Affichage Streamlit d'un repas + macros + étapes de préparation."""
    for alim, g in repas:
        st.write(f"- **{alim.replace('_', ' ').capitalize()}** : {g} g")
    st.write(
        f"**Calories :** {total['calories']:.0f} kcal &nbsp;&nbsp;|&nbsp;&nbsp;"
        f"**Prot :** {total['proteines']:.1f} g | **Lip :** {total['lipides']:.1f} g | "
        f"**Gluc :** {total['glucides']:.1f} g | **Fibres :** {total['fibres']:.1f} g"
    )
    with st.expander("Étapes de préparation", expanded=False):
        for alim, _ in repas:
            st.markdown(f"**{alim.replace('_', ' ').capitalize()}** : {aliments[alim]['prep']}")

# ─────────────────────────────────────────────────────────────
# 3. Interface Streamlit
# ─────────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="Plan Repas Personnalisé", page_icon="🥗", layout="wide")
    st.title("🥗 Générateur de plan repas multi-jours")
    st.write("Filtre les allergènes, fixe tes calories par repas et obtiens des menus équilibrés "
             "avec macros et instructions cuisine.")

    # Barre latérale : paramètres utilisateur
    st.sidebar.header("Paramètres")
    nb_jours = st.sidebar.number_input(
        "Nombre de jours", 1, 14, value=5, step=1,
        help="Plan jusqu’à 2 semaines"
    )
    cal_repas = st.sidebar.slider(
        "Calories par repas", 200, 1200, value=600, step=50,
        help="Objectif énergétique pour chaque repas"
    )

    st.sidebar.subheader("Sélectionnez vos allergies")
    allergie_tags = [
        tag for libelle, tag in allergenes_possibles.items()
        if st.sidebar.checkbox(libelle, value=False)
    ]

    alim_ok = filtrer_aliments(allergie_tags)
    if len(alim_ok) < 4:
        st.error("Aucun aliment disponible après filtrage. Décochez certains allergènes ou "
                 "ajoutez plus d'aliments dans la base.")
        st.stop()

    # Génération et affichage du plan
    st.success(
        f"Plan généré : **{nb_jours} jours** · **3 repas/jour** · "
        f"≈ **{cal_repas} kcal**/repas"
    )
    for jour in range(1, nb_jours + 1):
        st.markdown(f"## 📅 Jour {jour}")
        for repas_nom in ["Petit-déjeuner", "Déjeuner", "Dîner"]:
            st.markdown(f"### {repas_nom}")
            repas, total = generer_repas(cal_repas, alim_ok)
            if repas:
                afficher_repas(repas, total)
            else:
                st.warning("Pas assez d'aliments pour ce repas.")
        st.markdown("---")

if __name__ == "__main__":
    main()