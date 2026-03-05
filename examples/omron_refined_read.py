from aphyt import omron
import time
import binascii

def word_to_int(word_bytes):
    """Converte un WORD (2 byte) da little-endian a intero"""
    return int.from_bytes(word_bytes, byteorder='little')

def read_omron_refined():
    ip = '172.16.224.111'
    
    print(f"--- Lettura Raffinata Omron NJ/NX ---")
    
    try:
        with omron.NSeries(ip) as eip_conn:
            # 1. Lettura Allarmi (WORD[81])
            tag_alarms = 'ScadaInterface.Egress.Alarms_Packed'
            alarms_bytes = eip_conn.read_variable(tag_alarms)
            
            print(f"\n--- Tag: {tag_alarms} (WORD[81]) ---")
            if isinstance(alarms_bytes, list):
                # Convertiamo ogni WORD in un intero (presumendo little-endian)
                alarms_ints = [word_to_int(b) for b in alarms_bytes]
                # Mostriamo solo quelli attivi (diversi da 0) per brevità
                active_indexes = [(i, val) for i, val in enumerate(alarms_ints) if val != 0]
                
                if active_indexes:
                    print(f"Allarmi attivi (Indice: Valore):")
                    for idx, val in active_indexes:
                        print(f" - Indice {idx}: {val:04x}") # Esadecimale per i Bitmask dei WORD
                else:
                    print("Tutti i WORD degli allarmi sono a zero.")
            else:
                print(f"Ricevuto formato inatteso per allarmi: {type(alarms_bytes)}")

            # 2. Lettura RecipeList
            # Proviamo a capirne la struttura.
            tag_recipe = 'ScadaInterface.Egress.RecipeList'
            print(f"\n--- Tag: {tag_recipe} ---")
            
            try:
                recipe_data = eip_conn.read_variable(tag_recipe)
                
                if isinstance(recipe_data, list):
                    print(f"Trovata lista di {len(recipe_data)} elementi in RecipeList.")
                    # Mostriamo i primi 2 record in modo leggibile
                    for i, item in enumerate(recipe_data[:2]):
                        print(f" - Ricetta [{i}]: {item}")
                else:
                    print(f"Ricevuto formato: {type(recipe_data)}")
                    print(f"Dati: {recipe_data}") # Se è un unico record
            except Exception as e_recipe:
                print(f"Errore lettura RecipeList: {e_recipe}")

    except Exception as e:
        print(f"\nERRORE: {e}")

if __name__ == "__main__":
    read_omron_refined()
