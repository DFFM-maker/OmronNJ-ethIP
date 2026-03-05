from aphyt import omron
import time

def read_omron_complex():
    ip = '172.16.224.111'
    
    print(f"--- Omron NJ/NX - Test Lettura Strutture ed Array ---")
    
    try:
        with omron.NSeries(ip) as eip_conn:
            print("Connessione stabilita.")
            
            # 1. Lettura dell'array di allarmi WORD[0..80]
            tag_alarms = 'ScadaInterface.Egress.Alarms_Packed'
            print(f"\n--- Lettura array: {tag_alarms} ---")
            alarms_val = eip_conn.read_variable(tag_alarms)
            
            if isinstance(alarms_val, (list, tuple)):
                print(f"L'array contiene {len(alarms_val)} elementi.")
                print(f"Primi 10 valori: {alarms_val[:10]}")
            else:
                print(f"Valore ricevuto: {alarms_val}")

            # 2. Lettura di RecipeList
            tag_recipe = 'ScadaInterface.Egress.RecipeList'
            print(f"\n--- Lettura variabile: {tag_recipe} ---")
            try:
                recipe_val = eip_conn.read_variable(tag_recipe)
                print(f"Valore di RecipeList: {recipe_val}")
            except Exception as e_recipe:
                print(f"Impossibile leggere RecipeList direttamente (potrebbe essere troppo grande o complessa): {e_recipe}")
                
            # Proviamo anche con un campo specifico di RecipeList se lo conosciamo
            # Per ora proviamo la lettura diretta.
            
    except Exception as e:
        print(f"\nERRORE: {e}")

if __name__ == "__main__":
    read_omron_complex()
