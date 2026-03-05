import time
import csv
from aphyt import omron

def parse_scada_tags(file_path):
    """Estrae i nomi dei tag da un file scada.txt separato da tab"""
    tags = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader) # Salta l'intestazione
            for row in reader:
                if len(row) > 1:
                    tag_name = row[1].strip()
                    if tag_name:
                        tags.append(tag_name)
    except Exception as e:
        print(f"Errore caricamento file {file_path}: {e}")
    return tags

def run_omron_connector():
    PLC_IP = '172.16.224.111'
    SCADA_FILE = r'src/scada.txt'
    
    print(f"--- Omron NJ/NX Connector (Protocollo EtherNet/IP via aphyt) ---")
    print(f"Caricamento tag da: {SCADA_FILE}")
    
    tags = parse_scada_tags(SCADA_FILE)
    if not tags:
        print("Nessun tag trovato nel file. Verificare il percorso.")
        return

    # Filtriamo i tag per il monitoraggio (limitiamo i primi 20 per velocità di test)
    # aphyt gestisce bene le strutture e gli array.
    tags_to_monitor = [t for t in tags if "[" not in t]
    
    print(f"Connessione a {PLC_IP}...")
    
    try:
        with omron.NSeries(PLC_IP) as plc:
            print("Connesso al PLC!")
            print(f"Monitoraggio di {len(tags_to_monitor)} variabili...\n")
            
            while True:
                print(f"--- Aggiornamento {time.strftime('%H:%M:%S')} ---")
                print(f"{'VAR NAME':<50} | {'VALUE':<20}")
                print("-" * 75)
                
                for tag in tags_to_monitor[:20]: # Monitoriamo i primi 20 tag
                    try:
                        val = plc.read_variable(tag)
                        print(f"{tag:<50} | {val}")
                    except Exception as tag_err:
                        print(f"{tag:<50} | ERRORE: {tag_err}")
                
                print("-" * 75)
                time.sleep(5) # Intervallo di 5 secondi
                
    except KeyboardInterrupt:
        print("\nMonitoraggio interrotto dall'utente.")
    except Exception as e:
        print(f"\nErrore connessione: {e}")

if __name__ == "__main__":
    run_omron_connector()
