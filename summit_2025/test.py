import ussl
import sys
print("Stai usando MicroPython versione: " + sys.version)
KEY_PATH = 'private.key'
CERT_PATH = 'cert.crt'
print("Tentativo di leggere la chiave privata da: " + KEY_PATH)
try:
    with open(KEY_PATH, 'r') as f:
        key_data = f.read()
    print("Lettura del file della chiave completata con successo.")
    # Stampiamo solo l'inizio e la fine per conferma, non l'intera chiave
    print("Inizio della chiave: " + key_data[:35])
    print("Fine della chiave: " + key_data[-35:])
except Exception as e:
    print("ERRORE CRITICO durante la lettura del file della chiave: ")
    print(e)
    # Se fallisce qui, il problema è il file o il filesystem.
if 'key_data' in locals():
    print("\nTentativo di leggere il certificato...")
    try:
        with open(CERT_PATH, 'r') as f:
            cert_data = f.read()
        print("Lettura del file del certificato completata.")
    except Exception as e:
        print("ERRORE CRITICO durante la lettura del file del certificato: ")
        print(e)
# --- IL TEST CRUCIALE ---
# Ora proviamo a inizializzare il contesto SSL.
# Se l'errore "invalid key" appare qui, il problema è al 100% nel file della chiave
# o in un bug della libreria ussl che non riesce a interpretarlo.
if 'key_data' in locals() and 'cert_data' in locals():
    print("\n>>> INIZIO TEST DI CARICAMENTO CHIAVE IN USSL <<<")
    try:
        ssl_params = {
            "key": key_data,
            "cert": cert_data,
            "server_side": False
        }
        # Questa riga non fa nulla di concreto ma forza il parsing.
        # Spesso l'errore non viene lanciato finché non si tenta di usarlo.
        # Creiamo un oggetto SSL per forzare il controllo.
        dummy_socket = ussl.wrap_socket(None, **ssl_params)
        print("\n>>> SUCCESSO! La chiave è stata caricata e interpretata correttamente da ussl.")
        print("Il problema NON è nel formato del file, ma probabilmente nella connessione di rete o nel client MQTT.")
    except Exception as e:
        print("\n>>> FALLIMENTO! Errore durante il caricamento della chiave in ussl: ")
        print(e)
        print("L'errore 'invalid key' è confermato. Il problema è quasi certamente nel file key.pem.")
