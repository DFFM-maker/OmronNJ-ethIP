import time
import sys
from aphyt import omron
from aphyt.cip.cip_datatypes import CIPStructure, CIPArray, CIPDataType
import binascii

def browse_structure(name, obj, level=0):
    """Esplora ricorsivamente una struttura o un array di aphyt"""
    indent = "  " * level
    
    if obj is None:
        print(f"{indent}[None] {name}")
        return

    # Se è una struttura (CIPStructure)
    if isinstance(obj, CIPStructure):
        print(f"{indent}[Struttura] {name} ({getattr(obj, 'variable_type_name', 'ST_UNKNOWN')})")
        # I membri sono in un dizionario
        for member_name, member_obj in obj.members.items():
            browse_structure(member_name, member_obj, level + 1)
            
    # Se è un array (CIPArray)
    elif isinstance(obj, CIPArray):
        # Nelle CIPArray di aphyt, number_of_elements è una lista di dimensioni
        dims = obj.number_of_elements 
        print(f"{indent}[Array] {name} : Dims {dims}")
        # Mostriamo lo schema dell'elemento base
        if hasattr(obj, 'local_cip_data_type_object'):
             browse_structure("-> Elemento", obj.local_cip_data_type_object, level + 1)
             
    # Tipi base
    else:
        type_name = type(obj).__name__
        print(f"{indent}[Dato] {name} : {type_name}")

def omron_browser():
    ip = '172.16.224.111'
    root_tag = 'ScadaInterface'
    
    print(f"--- Omron NJ/NX Structure Browser (EIP) ---")
    print(f"Server: {ip}")
    print(f"Esplorazione di: {root_tag}")
    
    try:
        # Usiamo il context manager di aphyt
        with omron.NSeries(ip) as plc:
            print("Connessione stabilita. Caricamento della struttura in corso...")
            
            # Chiamare read_variable forza lo scaricamento di tutti i metadati e dei dati
            # Per una struttura gerarchica, legge l'intera definizione dei tipi.
            start_time = time.time()
            
            # Leggiamo il valore. Questo popolerà la cache delle variabili nel dispatcher.
            plc.read_variable(root_tag)
            
            # Recuperiamo l'oggetto istanza (metadati + dati)
            # In aphyt, l'oggetto è memorizzato in connected_cip_dispatcher.variables
            dispatcher = plc.connected_cip_dispatcher
            structure_obj = dispatcher.variables.get(root_tag)
            
            elapsed = time.time() - start_time
            print(f"Struttura caricata in {elapsed:.2f}s.\n")
            
            if structure_obj:
                print(f"ALBERO DI {root_tag}:")
                browse_structure(root_tag, structure_obj)
            else:
                print(f"Errore: Tag '{root_tag}' non trovato nella cache dopo la lettura.")

    except Exception as e:
        print(f"\nErrore durante il browsing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    omron_browser()
