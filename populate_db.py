"""
Script per popolare il database HealthHub con dati di esempio realistici.
Eseguire questo script dalla cartella healthhub-backend:
  python populate_db.py
"""

import requests
import random
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

# Dati di esempio
CITTA = ["Roma", "Milano", "Napoli", "Torino", "Bologna", "Firenze", "Bari", "Genova"]

SEDI_DATA = [
    {
        "nome": "Ospedale San Raffaele",
        "indirizzo": "Via Olgettina 60",
        "citta": "Milano",
        "telefono": "02-26431",
        "email": "info@sanraffaele.it",
        "tipo_struttura": "ospedale",
        "numero_posti_letto": 1350
    },
    {
        "nome": "Policlinico Gemelli",
        "indirizzo": "Largo Agostino Gemelli 8",
        "citta": "Roma",
        "telefono": "06-30151",
        "email": "info@policlinicogemelli.it",
        "tipo_struttura": "ospedale",
        "numero_posti_letto": 1500
    },
    {
        "nome": "Clinica Humanitas",
        "indirizzo": "Via Manzoni 56",
        "citta": "Milano",
        "telefono": "02-82241",
        "email": "info@humanitas.it",
        "tipo_struttura": "clinica_privata",
        "numero_posti_letto": 600
    }
]

REPARTI_DATA = [
    {"nome": "Cardiologia", "piano": 2, "area": "Medicina"},
    {"nome": "Ortopedia", "piano": 3, "area": "Chirurgia"},
    {"nome": "Neurologia", "piano": 4, "area": "Medicina"},
    {"nome": "Pediatria", "piano": 1, "area": "Medicina"},
    {"nome": "Oncologia", "piano": 5, "area": "Medicina"},
    {"nome": "Ginecologia", "piano": 2, "area": "Chirurgia"},
]

MEDICI_DATA = [
    {"nome": "Mario", "cognome": "Rossi", "specializzazione": "Cardiologia", "email": "m.rossi@hospital.it", "telefono": "333-1234567", "codice_fiscale": "RSSMRA70A01H501Z", "password": "password123"},
    {"nome": "Laura", "cognome": "Bianchi", "specializzazione": "Ortopedia", "email": "l.bianchi@hospital.it", "telefono": "333-2345678", "codice_fiscale": "BNCLRA75B02F205Y", "password": "password123"},
    {"nome": "Giuseppe", "cognome": "Verdi", "specializzazione": "Neurologia", "email": "g.verdi@hospital.it", "telefono": "333-3456789", "codice_fiscale": "VRDGPP80C03L219X", "password": "password123"},
    {"nome": "Anna", "cognome": "Ferrari", "specializzazione": "Pediatria", "email": "a.ferrari@hospital.it", "telefono": "333-4567890", "codice_fiscale": "FRRANN85D04A794W", "password": "password123"},
    {"nome": "Marco", "cognome": "Romano", "specializzazione": "Oncologia", "email": "m.romano@hospital.it", "telefono": "333-5678901", "codice_fiscale": "RMNMRC78E05H501V", "password": "password123"},
]

PAZIENTI_DATA = [
    {"nome": "Luca", "cognome": "Conti", "codice_fiscale": "CNTLCU90F06L736U", "email": "luca.conti@email.it", "telefono": "340-1111111", "password": "password123"},
    {"nome": "Sofia", "cognome": "Galli", "codice_fiscale": "GLLSFO88G07F839T", "email": "sofia.galli@email.it", "telefono": "340-2222222", "password": "password123"},
    {"nome": "Alessandro", "cognome": "Ricci", "codice_fiscale": "RCCLSS92H08H501S", "email": "alex.ricci@email.it", "telefono": "340-3333333", "password": "password123"},
    {"nome": "Giulia", "cognome": "Marino", "codice_fiscale": "MRNGLL95I09F205R", "email": "giulia.marino@email.it", "telefono": "340-4444444", "password": "password123"},
    {"nome": "Davide", "cognome": "Greco", "codice_fiscale": "GRCDVD87J10L219Q", "email": "davide.greco@email.it", "telefono": "340-5555555", "password": "password123"},
    {"nome": "Francesca", "cognome": "Bruno", "codice_fiscale": "BRNFNC93K11A794P", "email": "f.bruno@email.it", "telefono": "340-6666666", "password": "password123"},
]

PRESTAZIONI_DATA = [
    {"nome": "Visita Cardiologica", "tipo": "visita_specialistica", "durata_minuti": 30},
    {"nome": "Ecografia Addominale", "tipo": "ecografia", "durata_minuti": 20},
    {"nome": "Radiografia Torace", "tipo": "radiografia", "durata_minuti": 15},
    {"nome": "Risonanza Magnetica", "tipo": "risonanza", "durata_minuti": 45},
    {"nome": "Analisi del Sangue Complete", "tipo": "analisi_sangue", "durata_minuti": 10},
    {"nome": "Elettrocardiogramma", "tipo": "ecg", "durata_minuti": 15},
    {"nome": "TAC Total Body", "tipo": "tac", "durata_minuti": 30},
]


def create_entity(endpoint, data):
    """Crea un'entità tramite API"""
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}/", json=data)
        if response.status_code in [200, 201]:
            print(f"✅ Creato {endpoint}: {data.get('nome', data.get('id', ''))}")
            return response.json()
        else:
            print(f"❌ Errore {endpoint}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Errore connessione {endpoint}: {e}")
        return None


def populate_database():
    """Popola il database con dati di esempio"""
    print("\n🏥 POPOLAMENTO DATABASE HEALTHHUB\n" + "="*50)
    
    # 1. SEDI
    print("\n📍 Creazione Sedi...")
    sedi = []
    for sede_data in SEDI_DATA:
        sede = create_entity("sedi", sede_data)
        if sede:
            sedi.append(sede)
    
    if not sedi:
        print("❌ Impossibile creare sedi. Interrompo.")
        return
    
    # 2. REPARTI
    print("\n🏢 Creazione Reparti...")
    reparti = []
    for reparto_data in REPARTI_DATA:
        reparto_data["id_sede"] = random.choice(sedi)["id"]
        reparto = create_entity("reparti", reparto_data)
        if reparto:
            reparti.append(reparto)
    
    # 3. MEDICI
    print("\n👨‍⚕️ Creazione Medici...")
    medici = []
    for medico_data in MEDICI_DATA:
        if reparti:
            medico_data["id_reparto"] = random.choice(reparti)["id"]
        medico = create_entity("medici", medico_data)
        if medico:
            medici.append(medico)
    
    # 4. PAZIENTI
    print("\n👤 Creazione Pazienti...")
    pazienti = []
    for paziente_data in PAZIENTI_DATA:
        paziente = create_entity("pazienti", paziente_data)
        if paziente:
            pazienti.append(paziente)
    
    # 5. PRESTAZIONI
    print("\n💉 Creazione Prestazioni...")
    prestazioni = []
    for prestazione_data in PRESTAZIONI_DATA:
        prestazione = create_entity("prestazioni", prestazione_data)
        if prestazione:
            prestazioni.append(prestazione)
    
    # 6. PRENOTAZIONI
    print("\n📅 Creazione Prenotazioni...")
    if pazienti and medici and prestazioni and sedi:
        for i in range(15):  # 15 prenotazioni
            giorni_futuro = random.randint(1, 30)
            data_visita = (datetime.now() + timedelta(days=giorni_futuro)).strftime("%Y-%m-%d")
            ora_visita = f"{random.randint(9, 17):02d}:{random.choice(['00', '30'])}:00"
            
            prenotazione_data = {
                "data_visita": data_visita,
                "ora_visita": ora_visita,
                "id_paziente": random.choice(pazienti)["id"],
                "id_medico": random.choice(medici)["id"],
                "id_prestazione": random.choice(prestazioni)["id"],
                "id_sede": random.choice(sedi)["id"],
                "stato": random.choice(["prenotata", "confermata"])
            }
            create_entity("prenotazioni", prenotazione_data)
    
    # 7. TURNI
    print("\n⏰ Creazione Turni...")
    if medici and sedi:
        for i in range(20):  # 20 turni
            giorni_futuro = random.randint(-7, 14)
            data = (datetime.now() + timedelta(days=giorni_futuro)).strftime("%Y-%m-%d")
            
            turno_data = {
                "id_medico": random.choice(medici)["id"],
                "data": data,
                "ora_inizio": "08:00:00",
                "ora_fine": "16:00:00",
                "id_sede": random.choice(sedi)["id"],
                "tipo_turno": random.choice(["mattina", "pomeriggio", "guardia"])
            }
            create_entity("turni", turno_data)
    
    # 8. RICOVERI
    print("\n🛏️ Creazione Ricoveri...")
    if pazienti and medici and sedi and reparti:
        for i in range(5):  # 5 ricoveri attivi
            giorni_passati = random.randint(1, 10)
            data_ingresso = (datetime.now() - timedelta(days=giorni_passati)).strftime("%Y-%m-%d")
            
            ricovero_data = {
                "id_paziente": random.choice(pazienti)["id"],
                "id_medico_responsabile": random.choice(medici)["id"],
                "id_sede": random.choice(sedi)["id"],
                "id_reparto": random.choice(reparti)["id"],
                "data_ingresso": data_ingresso,
                "motivo": random.choice([
                    "Intervento chirurgico programmato",
                    "Osservazione post-operatoria",
                    "Terapia intensiva",
                    "Monitoraggio condizioni"
                ]),
                "stato": "attivo"
            }
            create_entity("ricoveri", ricovero_data)
    
    # 9. OPERAZIONI
    print("\n🏥 Creazione Operazioni...")
    if pazienti and medici and sedi and reparti:
        for i in range(8):  # 8 operazioni
            giorni_futuro = random.randint(1, 20)
            data_op = (datetime.now() + timedelta(days=giorni_futuro)).strftime("%Y-%m-%d")
            ora_op = f"{random.randint(8, 15):02d}:00:00"
            
            operazione_data = {
                "id_paziente": random.choice(pazienti)["id"],
                "id_medico": random.choice(medici)["id"],
                "id_sede": random.choice(sedi)["id"],
                "id_reparto": random.choice(reparti)["id"],
                "data_operazione": data_op,
                "ora_operazione": ora_op,
                "tipo": random.choice([
                    "cardiochirurgia",
                    "ortopedia",
                    "neurochirurgia",
                    "chirurgia_addominale"
                ]),
                "descrizione": "Intervento programmato",
                "stato_intervento": "programmata",
                "durata_prevista": random.choice([60, 90, 120, 180])
            }
            create_entity("operazioni", operazione_data)
    
    # 10. TELECONSULENZE
    print("\n💻 Creazione Teleconsulenze...")
    if pazienti and medici:
        for i in range(6):  # 6 teleconsulenze
            giorni_futuro = random.randint(1, 15)
            data_tc = (datetime.now() + timedelta(days=giorni_futuro)).strftime("%Y-%m-%d")
            
            tc_data = {
                "id_paziente": random.choice(pazienti)["id"],
                "id_medico": random.choice(medici)["id"],
                "data_richiesta": data_tc,
                "tipo": random.choice(["video", "telefonica", "chat"]),
                "descrizione_problema": "Consulto medico a distanza",
                "stato": random.choice(["richiesta", "programmata"])
            }
            create_entity("teleconsulenze", tc_data)
    
    print("\n" + "="*50)
    print("✅ POPOLAMENTO COMPLETATO CON SUCCESSO!")
    print("\nRiepilogo:")
    print(f"  📍 Sedi: {len(sedi)}")
    print(f"  🏢 Reparti: {len(reparti)}")
    print(f"  👨‍⚕️ Medici: {len(medici)}")
    print(f"  👤 Pazienti: {len(pazienti)}")
    print(f"  💉 Prestazioni: {len(prestazioni)}")
    print(f"  📅 Prenotazioni: 15")
    print(f"  ⏰ Turni: 20")
    print(f"  🛏️ Ricoveri: 5")
    print(f"  🏥 Operazioni: 8")
    print(f"  💻 Teleconsulenze: 6")
    print("\n🎉 Ora puoi testare l'applicazione con dati realistici!")


if __name__ == "__main__":
    print("⚠️  ATTENZIONE: Questo script popolerà il database con dati di esempio.")
    print("    Assicurati che il backend sia in esecuzione su http://127.0.0.1:8000")
    input("\n👉 Premi INVIO per continuare o CTRL+C per annullare...")
    populate_database()