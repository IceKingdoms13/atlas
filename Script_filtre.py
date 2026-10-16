import json

def main():
    fichier_entree = "economie_items.json"
    fichier_sortie = "economie_items_filtres.json"
    
    print(f"1. Lecture du fichier {fichier_entree}...")
    try:
        with open(fichier_entree, "r", encoding="utf-8") as f:
            items = json.load(f)
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{fichier_entree}' est introuvable. Avez-vous bien lancé le premier script ?")
        return
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")
        return

    print("2. Nettoyage des données (suppression des prix <= 0)...")
    # On garde uniquement les items dont le prix est strictement supérieur à 0
    items_filtres = [item for item in items if item.get("minPrice", 0) > 0]
    
    items_supprimes = len(items) - len(items_filtres)

    print(f"3. Sauvegarde dans {fichier_sortie}...")
    with open(fichier_sortie, "w", encoding="utf-8") as f:
        json.dump(items_filtres, f, indent=4, ensure_ascii=False)
        
    print(f"✅ Terminé ! {items_supprimes} items ont été retirés.")
    print(f"📊 Il reste désormais {len(items_filtres)} items valides dans le nouveau fichier.")

if __name__ == "__main__":
    main()