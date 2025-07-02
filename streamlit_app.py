from openpyxl import Workbook

# ──────────────── Aliments disponibles (sans allergènes) ────────────────
aliments = {
    "poulet_grille": {"calories": 165, "proteines": 31, "lipides": 3.6, "glucides": 0, "fibres": 0, "prep": "Assaisonner et griller 5 min/face."},
    "cabillaud": {"calories": 82, "proteines": 18, "lipides": 0.7, "glucides": 0, "fibres": 0, "prep": "Cuire au four à 180°C pendant 15 min."},
    "tofu": {"calories": 76, "proteines": 8, "lipides": 4.8, "glucides": 1.9, "fibres": 0.3, "prep": "Saisir 4 min/face à la poêle."},
    "tempeh": {"calories": 193, "proteines": 20, "lipides": 11, "glucides": 9, "fibres": 1.4, "prep": "Griller 3 min de chaque côté."},
    "seitan": {"calories": 143, "proteines": 25, "lipides": 1.9, "glucides": 5.1, "fibres": 0.6, "prep": "Poêler avec sauce soja 4 min."},
    "lentilles_cuites": {"calories": 116, "proteines": 9, "lipides": 0.4, "glucides": 20, "fibres": 8, "prep": "Cuire dans l’eau 15 min."},
    "quinoa": {"calories": 120, "proteines": 4.4, "lipides": 1.9, "glucides": 21.3, "fibres": 2.8, "prep": "Cuire dans 2 volumes d’eau pendant 15 min."},
    "riz_complet": {"calories": 112, "proteines": 2.6, "lipides": 0.9, "glucides": 23, "fibres": 1.8, "prep": "Cuire 35–40 min à couvert."},
    "patate_douce": {"calories": 86, "proteines": 1.6, "lipides": 0.1, "glucides": 20.1, "fibres": 3, "prep": "Cuire à l’eau 20 min ou au four 30 min."},
    "brocolis": {"calories": 34, "proteines": 2.8, "lipides": 0.4, "glucides": 6.6, "fibres": 2.6, "prep": "Cuire vapeur 6–9 min."},
    "carottes_vapeur": {"calories": 35, "proteines": 0.8, "lipides": 0.1, "glucides": 8.2, "fibres": 2.9, "prep": "Cuire vapeur 10–12 min."},
    "courgette_poelee": {"calories": 17, "proteines": 1.2, "lipides": 0.3, "glucides": 3.1, "fibres": 1, "prep": "Faire revenir 8 min à la poêle."},
    "houmous": {"calories": 177, "proteines": 4.5, "lipides": 8.6, "glucides": 20, "fibres": 4, "prep": "À tartiner ou servir en accompagnement."},
    "sauce_tomate_maison": {"calories": 50, "proteines": 1.5, "lipides": 1.8, "glucides": 7, "fibres": 1.5, "prep": "Mijoter tomates + herbes 20 min."},
}

# ──────────────── Plan fixe pour 3 jours (exemple) ────────────────
plan_repas = {
    1: {
        "Petit-déjeuner": [("tofu", 100), ("quinoa", 150), ("courgette_poelee", 100), ("houmous", 50)],
        "Déjeuner": [("poulet_grille", 120), ("patate_douce", 150), ("brocolis", 100), ("sauce_tomate_maison", 50)],
        "Dîner": [("cabillaud", 130), ("riz_complet", 150), ("carottes_vapeur", 100), ("houmous", 40)],
    },
    2: {
        "Petit-déjeuner": [("tempeh", 100), ("quinoa", 140), ("brocolis", 100), ("sauce_tomate_maison", 50)],
        "Déjeuner": [("seitan", 130), ("patate_douce", 150), ("carottes_vapeur", 100), ("houmous", 40)],
        "Dîner": [("lentilles_cuites", 150), ("riz_complet", 140), ("courgette_poelee", 100), ("sauce_tomate_maison", 60)],
    },
    3: {
        "Petit-déjeuner": [("tofu", 100), ("quinoa", 130), ("carottes_vapeur", 100), ("houmous", 40)],
        "Déjeuner": [("poulet_grille", 150), ("patate_douce", 150), ("brocolis", 100), ("sauce_tomate_maison", 50)],
        "Dîner": [("seitan", 130), ("riz_complet", 120), ("courgette_poelee", 100), ("houmous", 50)],
    }
}

# ──────────────── Création du fichier Excel ────────────────
wb = Workbook()
ws = wb.active
ws.title = "Plan de repas"
ws.append(["Jour", "Repas", "Aliment", "Quantité (g)", "Calories", "Protéines", "Lipides", "Glucides", "Fibres", "Préparation"])

for jour, repas_dict in plan_repas.items():
    for repas_nom, aliments_liste in repas_dict.items():
        for alim, quantite in aliments_liste:
            info = aliments.get(alim, {})
            cal = round(info["calories"] * quantite / 100, 1)
            prot = round(info["proteines"] * quantite / 100, 1)
            lip = round(info["lipides"] * quantite / 100, 1)
            gluc = round(info["glucides"] * quantite / 100, 1)
            fib = round(info["fibres"] * quantite / 100, 1)
            prep = info["prep"]
            ws.append([
                f"Jour {jour}", repas_nom,
                alim.replace("_", " ").capitalize(),
                quantite, cal, prot, lip, gluc, fib, prep
            ])

# ──────────────── Sauvegarde du fichier Excel ────────────────
fichier_excel = "plan_repas_sportif.xlsx"
wb.save(fichier_excel)
print(f"✅ Plan de repas sauvegardé dans : {fichier_excel}")