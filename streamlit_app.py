import streamlit as st
import random

# ───────────────────────────────────────────────
# 1. Base ALIMENTS : valeurs /100 g + tags allergènes + étapes de préparation
# ───────────────────────────────────────────────
aliments = {
    # Sources protéiques
    "poulet_grille":      {"calories": 165, "proteines": 31, "lipides": 3.6, "glucides": 0,   "fibres": 0,   "tags": [],               "prep": "Assaisonner (sel, poivre, herbes) et griller 5 min/face."},
    "cabillaud":          {"calories":  82, "proteines": 18, "lipides": 0.7, "glucides": 0,   "fibres": 0,   "tags": ["poisson_blanc"], "prep": "Four 180 °C 15 min ou vapeur 10 min, citron + herbes."},
    "dinde_sautee":       {"calories": 120, "proteines": 27, "lipides": 2,   "glucides": 0,   "fibres": 0,   "tags": [],               "prep": "Couper en lanières ; poêler 6-8 min avec paprika."},
    "steak_hache_5%":     {"calories": 133, "proteines": 20, "lipides": 5,   "glucides": 0,   "fibres": 0,   "tags": [],               "prep": "Poêler 4-5 min/face à feu moyen-fort."},
    "tofu":               {"calories":  76, "proteines":  8, "lipides": 4.8, "glucides": 1.9, "fibres": 0.3, "tags": [],               "prep": "Presser, mariner (soja-gingembre), saisir 4 min/face."},
    "tempeh":             {"calories": 193, "proteines": 20, "lipides":11,   "glucides": 9,   "fibres": 1.4, "tags": [],               "prep": "Griller 3 min/face après marinade."},
    "seitan":             {"calories": 143, "proteines": 25, "lipides": 1.9, "glucides": 5.1, "fibres": 0.6, "tags": [],               "prep": "Poêler 3-4 min avec sauce soja."},
    "lentilles_cuites":   {"calories": 116, "proteines":  9, "lipides": 0.4, "glucides":20,   "fibres": 8,   "tags": [],               "prep": "Cuire 15 min dans 3 vol. d’eau, assaisonner."},
    "pois_chiches_cuits": {"calories": 164, "proteines":  9, "lipides": 2.6, "glucides":27,   "fibres": 7.6, "tags": [],               "prep": "Égoutter, rissoler 5 min avec cumin & coriandre."},

    # Féculents
    "quinoa":             {"calories": 120, "proteines": 4.4,"lipides": 1.9,"glucides":21.3, "fibres": 2.8,"tags": [], "prep": "Rincer, cuire 12-15 min dans 2 vol. d’eau."},
    "riz_complet":        {"calories": 112, "proteines": 2.6,"lipides": 0.9,"glucides":23,   "fibres": 1.8,"tags": [], "prep": "Cuire 35-40 min dans 2,5 vol. d’eau."},
    "patate_douce":       {"calories":  86, "proteines": 1.6,"lipides": 0.1,"glucides":20.1, "fibres": 3,  "tags": [], "prep": "Dés vapeur 20 min ou four 30 min 200 °C."},
    "pates_legumineuses": {"calories": 135, "proteines":13,  "lipides": 2,  "glucides":20,   "fibres": 6,  "tags": [], "prep": "Cuire 6-8 min à l’eau bouillante."},

    # Légumes & accompagnements
    "brocolis":           {"calories":  34, "proteines": 2.8,"lipides": 0.4,"glucides": 6.6,"fibres": 2.6,"tags": [], "prep": "Vapeur 6-8 min."},
    "courgette_poelee":   {"calories":  17, "proteines": 1.2,"lipides": 0.3,"glucides": 3.1,"fibres": 1,  "tags": [], "prep": "Rondelles sautées 8 min huile olive + ail."},
    "carottes_vapeur":    {"calories":  35, "proteines": 0.8,"lipides": 0.1,"glucides": 8.2,"fibres": 2.9,"tags": [], "prep": "Vapeur 10-12 min."},

    # Graisses / sauces
    "houmous":            {"calories": 177, "proteines":4.5,"lipides": 8.6,"glucides":20,"fibres":4,"tags": [], "prep": "À tartiner (30-50 g) ou dip crudités."},
    "sauce_tomate":       {"calories":  50, "proteines":1.5,"lipides": 1.8,"glucides": 7,"fibres":1.5,"tags": [], "prep": "Tomates + oignons mijotés 25 min."},

    # Allergènes à exclure
    "oeuf":         {"calories":155,"proteines":13,"lipides":11,"glucides":1.1,"fibres":0,"tags":["oeuf"],"prep":"Œuf dur 10 min."},
    "saumon":       {"calories":208,"proteines":20,"lipides":13,"glucides":0,"fibres":0,"tags":["poisson_gras"],"prep":"Four 15 min 180 °C."},
    "crevettes":    {"calories": 99,"proteines":24,"lipides":0.3,"glucides":0.2,"fibres":0,"tags":["fruit_de_mer"],"prep":"Sauter 3 min."},
    "arachides":    {"calories":567,"proteines":25,"lipides":49,"glucides":16,"fibres":8.5,"tags":["arachide"],"prep":"Snack."},
    "moutarde":     {"calories": 66,"proteines":4.4,"lipides":4.4,"glucides":5.8,"fibres":3.3,"tags":["moutarde"],"prep":"…"},
    "amandes":      {"calories":579,"proteines":21,"lipides":50,"glucides":22,"fibres":12,"tags":["noix"],"prep":"30 g nature."},
}

# Allergènes proposés à l’utilisateur
allergenes_ui = {
    "Œufs": "oeuf",
    "Arachides": "arachide",
    "Moutarde": "moutarde",
    "Poissons gras": "poisson_gras",
    "Fruits de mer": "fruit_de_mer",
    "Noix (amandes, etc.)": "noix",
}

# ───────────────────────────────────────────────
# 2. Fonctions utilitaires
# ───────────────────────────────────────────────
def filtrer_aliments(tags_allergies):
    """Retourne une liste d'aliments autorisés (aucun tag interdit)."""
    return [
        nom for nom, data in aliments.items()
        if not any(tag in tags_allergies for tag in data["tags"])
    ]

def generer_repas(calories_cible, alim_ok):
    """Génère un repas de 4 aliments dont ≥2 sources ≥10 g prot/100 g."""
    high_prot = [a for a in alim_ok if aliments[a]["proteines"] >= 10]
    autres    = [a for a in alim_ok if a not in high_prot]
    if len(high_prot) < 2 or len(alim_ok) < 4:
        return [], {k: 0 for k in ["calories","proteines","lipides","glucides","fibres"]}
    choix = random.sample(high_prot, 2) + random.sample(autres if len(autres) >= 2 else high_prot, 2)
    repas, total = [], {k: 0 for k in ["calories","proteines","lipides","glucides","fibres"]}
    for alim in choix:
        portion = round((calories_cible / 4) / aliments[alim]["calories"] * 100)  # g
        repas.append((alim, portion))
        for k in total:
            total[k] += aliments[alim][k] * portion / 100
    return repas, total

def afficher_repas(repas, total):
    for alim, g in repas:
        st.write(f"- **{alim.replace('_',' ').capitalize()}** : {g} g")
    st.write(f"**{total['calories']:.0f} kcal** · P {total['proteines']:.1f} g | L {total['lipides']:.1f} g | G {total['glucides']:.1f} g | Fibres {total['fibres']:.1f} g")
    with st.expander("Étapes de préparation"):
        for alim, _ in repas:
            st.markdown(f"**{alim.replace('_',' ').capitalize()}** : {aliments[alim]['prep']}")

# ───────────────────────────────────────────────
# 3. Interface Streamlit
# ───────────────────────────────────────────────
def main():
    st.set_page_config(page_title="Plan repas sportif", page_icon="🥗", layout="wide")
    st.title("🥗 Générateur de plan repas sportif – allergies & protéines")

    # ── Sidebar paramètres ──
    st.sidebar.header("Paramètres")
    nb_jours = st.sidebar.number_input("Nombre de jours", 1, 14, 5)
    calories = st.sidebar.slider("Calories par repas", 300, 1200, 650, 50)

    st.sidebar.subheader("Coche tes allergies")
    allergies_sel = [
        tag for lib, tag in allergenes_ui.items()
        if st.sidebar.checkbox(lib, value=False)
    ]

    # Filtrage aliments
    alim_ok = filtrer_aliments(allergies_sel)
    if len(alim_ok) < 4:
        st.error("Plus assez d'aliments après filtrage. Décoche quelques allergies ou ajoute d'autres aliments.")
        st.stop()

    st.success(f"Plan **{nb_jours} jours** • 3 repas/jour • ≈ {calories} kcal/repas")

    # Génération et affichage
    for jour in range(1, nb_jours + 1):
        st.header(f"📅 Jour {jour}")
        for moment in ["Petit-déjeuner", "Déjeuner", "Dîner"]:
            st.subheader(moment)
            repas, total = generer_repas(calories, alim_ok)
            afficher_repas(repas, total)
        st.markdown("---")

if __name__ == "__main__":
    main()