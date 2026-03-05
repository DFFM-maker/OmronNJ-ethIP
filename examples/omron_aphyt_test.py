from aphyt import omron
import time

def read_omron_aphyt():
    ip = '172.16.224.111'
    tag_name = 'ScadaInterface.Egress.IsRunning'
    
    print(f"--- Omron NJ/NX Test con APHYT su {ip} ---")
    
    try:
        # NSeries è l'oggetto specifico per NJ/NX
        with omron.NSeries(ip) as eip_conn:
            print("Connessione stabilita.")
            
            # Lettura variabile
            val = eip_conn.read_variable(tag_name)
            print(f"\nSUCCESSO! Valore '{tag_name}': {val}")
            
            # Proviamo a leggere anche un altro tag dal file scada.txt se disponibile
            tag_name_2 = 'ScadaInterface.Egress.ActualRecipeIndex'
            print(f"Lettura tag: {tag_name_2}...")
            val_2 = eip_conn.read_variable(tag_name_2)
            print(f"Valore '{tag_name_2}': {val_2}")
            
    except Exception as e:
        print(f"\nERRORE: {e}")

if __name__ == "__main__":
    read_omron_aphyt()
