import time
from aphyt import omron

def to_int(val):
    """Converte in intero qualsiasi cosa arrivi da aphyt (bytes o CustomInt)"""
    if isinstance(val, bytes):
        return int.from_bytes(val, 'little')
    try:
        return int(val)
    except:
        return 0

def read_omron_final():
    ip = '172.16.224.111'
    TAG_ALARMS = 'ScadaInterface.Egress.Alarms_Packed'
    TAG_RECIPES = 'ScadaInterface.Egress.RecipeList'
    
    print(f"--- Connettore NJ/NX Omron Avanzato (EIP) ---")
    
    try:
        with omron.NSeries(ip) as plc:
            print("Connessione OK.\n")
            
            # --- Lettura Allarmi ---
            print(f"Lettura {TAG_ALARMS}...")
            alarms_array = plc.read_variable(TAG_ALARMS)
            
            active_alarms = []
            for i, word in enumerate(alarms_array):
                val = to_int(word)
                if val != 0:
                    active_alarms.append((i, f"0x{val:04X}"))

            if active_alarms:
                print(f"  Allarmi attivi (parola: bitmask):")
                for pos, mask in active_alarms:
                    print(f"    - Parola {pos:02}: {mask}")
            else:
                print("  Nessun allarme attivo.")

            # --- Lettura Lista Ricette ---
            print(f"\nLettura {TAG_RECIPES}...")
            recipe_list = plc.read_variable(TAG_RECIPES)
            
            valid_recipes = []
            for r in recipe_list:
                # 'r.members' contiene campi di tipo CustomInt o CustomString
                idx = to_int(r.members['Index'])
                name = str(r.members['Name']).strip()
                
                if name: 
                    valid_recipes.append((idx, name))

            print(f"  Trovate {len(valid_recipes)} ricette popolate:")
            for idx, name in valid_recipes[:15]:
                print(f"    - [Idx {idx:02}]: {name}")
            
            if len(valid_recipes) > 15:
                print(f"    ... + altri {len(valid_recipes) - 15} record.")
                
    except Exception as e:
        print(f"\nErrore durante la lettura: {e}")

if __name__ == "__main__":
    read_omron_final()
