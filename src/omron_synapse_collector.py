from speedbeesynapse.component.base import HiveComponentBase, HiveComponentInfo, DataType
import time
import json
import binascii
from aphyt import omron

# --- CONFIGURAZIONE COMPONENTE ---
@HiveComponentInfo(
    uuid='f3a2b1c0-d9e8-4a7b-b6c5-1e2f3a4b5c6d', 
    name='Omron Advanced EthIP Collector', 
    tag='collector',
    inports=1,  # Ingressi dallo script logic (comandi da scrivere sul PLC)
    outports=1  # Uscite verso Synapse (dati letti dal PLC)
)
class HiveComponent(HiveComponentBase):

    def main(self, param):
        """
        Collector avanzato per Omron NJ/NX via EtherNet/IP (CIP Symbolic).
        Risolve strutture annidate e gestisce array complessi.
        """
        try:
            config = json.loads(param)
            plc_ip = config.get("PLC_IP", "172.16.224.111")
            poll_interval = config.get("Polling_Interval_ms", 1000) / 1000.0
            
            # Mappatura Alias per evitare il troncamento dei 32 caratteri nella UI di Synapse
            # Formato: "Nome_Breve_DB": "Percorso.Completo.Tag.PLC"
            self.tag_map = {
                "IsRunning": "ScadaInterface.Egress.IsRunning",
                "IsAlarmActive": "ScadaInterface.Egress.IsAlarmActive",
                "RecipeACK": "ScadaInterface.Egress.RecipeChangeACK",
                "RecipeIdx": "ScadaInterface.Egress.ActualRecipeIndex",
                "ActualSpeed": "ScadaInterface.Egress.ActualSpeed",
                "AlarmsPacked": "ScadaInterface.Egress.Alarms_Packed"
            }
        except Exception as e:
            self.log.error(f"Errore caricamento parametri: {str(e)}")
            return

        # --- Definizione Colonne in Uscita (Lettura dal PLC) ---
        self.cols = {}
        self.cols["IsRunning"] = self.out_port1.Column("IsRunning", DataType.BOOLEAN)
        self.cols["IsAlarmActive"] = self.out_port1.Column("IsAlarmActive", DataType.BOOLEAN)
        self.cols["RecipeACK"] = self.out_port1.Column("RecipeACK", DataType.BOOLEAN)
        self.cols["RecipeIdx"] = self.out_port1.Column("RecipeIdx", DataType.INT32)
        self.cols["ActualSpeed"] = self.out_port1.Column("ActualSpeed", DataType.FLOAT)
        # Array degli allarmi (WORD[81])
        self.cols["AlarmsPacked"] = self.out_port1.Column("AlarmsPacked", DataType.UINT16, data_array=81)

        self.log.info(f"Tentativo di connessione a PLC Omron NJ @ {plc_ip}...")

        try:
            # Utilizzo della libreria aphyt per la sessione CIP
            with omron.NSeries(plc_ip) as plc:
                self.log.info("Connessione EtherNet/IP stabilita.")

                while self.is_runnable():
                    ts = self.get_timestamp()

                    # 1. CICLO DI LETTURA (EGRESS)
                    for alias, full_tag in self.tag_map.items():
                        try:
                            val = plc.read_variable(full_tag)
                            
                            # Conversione specifica per l'array di WORD (allarme bitmask)
                            if alias == "AlarmsPacked":
                                clean_val = [int.from_bytes(b, 'little') if isinstance(b, bytes) else b for b in val]
                                self.cols[alias].insert(clean_val, ts)
                            else:
                                self.cols[alias].insert(val, ts)
                                
                        except Exception as tag_err:
                            self.log.warning(f"Errore lettura tag {full_tag}: {tag_err}")

                    # 2. CICLO DI SCRITTURA (INGRESS)
                    # Controlla se ci sono richieste pendenti dalla in_port1
                    self._handle_writes(plc)

                    time.sleep(poll_interval)

        except Exception as conn_err:
            self.log.error(f"Errore connessione EtherNet/IP: {conn_err}")
            # Segnala l'errore alla Status Timeline di Synapse
            status = self.Status()
            status.add_error("NETWORK_ACCESS_ERROR", [plc_ip])
            self.register_status(status)

    def _handle_writes(self, plc):
        """Legge i comandi dalla porta d'ingresso e li scrive fisicamente nel PLC."""
        # Il ContinuousReader legge i dati inviati dagli altri componenti (es. il Manager SQL)
        with self.in_port1.ContinuousReader(start=self.get_timestamp()) as reader:
            window_data = reader.read()
            if window_data and window_data.records:
                for record in window_data.records:
                    for d in record.data:
                        try:
                            # Mapping dei comandi Ingress basato sulle specifiche Industry 4.0
                            if d.name == "RecipeChangeRequest":
                                plc.write_variable("ScadaInterface.Ingress.RecipeChangeRequest", d.value)
                            elif d.name == "RecipeIndexRequest":
                                plc.write_variable("ScadaInterface.Ingress.RecipeIndexRequest", int(d.value))
                            elif d.name == "RecipeCodeRequest":
                                plc.write_variable("ScadaInterface.Ingress.RecipeProductionCodeRequest", int(d.value))
                        except Exception as write_err:
                            self.log.error(f"Errore scrittura PLC (Tag Ingress): {write_err}")