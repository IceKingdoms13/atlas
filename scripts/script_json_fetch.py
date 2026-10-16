import pandas as pd
import requests
import json
import math

def main():
    excel_file = "WetstonRP - Économie.xlsx"
    sheet_name = "Liste"
    output_file = "economie_items.json"
    
    print("1. Lecture du fichier Excel...")
    try:
        # Chargement de l'onglet contenant les items
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{excel_file}' est introuvable.")
        return
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")
        return

    # Noms exacts des colonnes dans le fichier Excel
    col_nom = '🧊 Bloc / Item'
    col_prix_min = '📉 Prix de vente\nMin'
    
    # Nettoyage : retirer les lignes où le nom de l'item est vide
    df = df.dropna(subset=[col_nom])
    
    print("2. Récupération des données de stack depuis l'API Minecraft...")
    # URL contenant les données brutes des items (Minecraft 1.20)
    api_url = "https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/pc/1.20/items.json"
    stack_sizes = {}
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        items_api_data = response.json()
        
        # Création d'un dictionnaire pour associer le nom de l'item (en minuscules) à sa taille de stack max
        for item in items_api_data:
            nom_api_minuscule = item.get('displayName', '').lower()
            stack_sizes[nom_api_minuscule] = item.get('stackSize', 64)
    except Exception as e:
        print(f"⚠️ Avertissement : Impossible de récupérer les tailles de stack ({e}). La valeur par défaut (64) sera appliquée.")
    
    print("3. Croisement des données et formatage...")
    result_data = []
    
    for index, row in df.iterrows():
        item_name = str(row[col_nom]).strip()
        
        # Ignorer les séparateurs ou données non valides
        if item_name.lower() == 'nan' or not item_name:
            continue
            
        prix_min = row[col_prix_min]
        # Vérification si le prix est un nombre valide, sinon on le met à 0
        if pd.isna(prix_min) or not isinstance(prix_min, (int, float)):
            prix_min = 0.0
            
        # Chercher le max stack (on passe par défaut à 64 si l'item a un nom modifié ou n'est pas trouvé)
        max_stack = stack_sizes.get(item_name.lower(), 64)
        
        item_data = {
            "name": item_name,
            "minPrice": round(float(prix_min), 2),
            "max_stack": max_stack
        }
        result_data.append(item_data)
        
    print(f"4. Sauvegarde dans {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=4, ensure_ascii=False)
        
    print(f"✅ Succès ! {len(result_data)} items ont été exportés avec succès.")

if __name__ == "__main__":
    main()