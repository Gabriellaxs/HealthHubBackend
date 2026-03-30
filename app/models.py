from sqlalchemy import Boolean, Column, Enum, Integer, String, Date, Time, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base


# =======================
#         SEDE
# =======================

class Sede(Base):
    __tablename__ = "sedi"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    indirizzo = Column(String)
    citta = Column(String)
    telefono = Column(String)
    email = Column(String)
    tipo_struttura = Column(String)
    numero_posti_letto = Column(Integer)

    reparti = relationship("Reparto", back_populates="sede", cascade="all, delete")
    prenotazioni = relationship("Prenotazione", back_populates="sede", cascade="all, delete")
    turni = relationship("Turno", back_populates="sede", cascade="all, delete")
    ricoveri = relationship("Ricovero", back_populates="sede", cascade="all, delete")
    operazioni = relationship("Operazione", back_populates="sede", cascade="all, delete")


# =======================
#        REPARTO
# =======================

class Reparto(Base):
    __tablename__ = "reparti"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    piano = Column(Integer)
    area = Column(String)

    id_sede = Column(Integer, ForeignKey("sedi.id"), nullable=False)
    sede = relationship("Sede", back_populates="reparti")

    medici = relationship("Medico", back_populates="reparto", cascade="all, delete")
    ricoveri = relationship("Ricovero", back_populates="reparto", cascade="all, delete")
    operazioni = relationship("Operazione", back_populates="reparto", cascade="all, delete")


# =======================
#        MEDICO
# =======================

class Medico(Base):
    __tablename__ = "medici"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    email = Column(String)
    telefono = Column(String)
    specializzazione = Column(String)
    codice_fiscale = Column(String, unique=True)

    id_reparto = Column(Integer, ForeignKey("reparti.id"), nullable=False)
    reparto = relationship("Reparto", back_populates="medici")

    turni = relationship("Turno", back_populates="medico", cascade="all, delete")
    prenotazioni = relationship("Prenotazione", back_populates="medico", cascade="all, delete")
    teleconsulenze = relationship("Teleconsulenza", back_populates="medico", cascade="all, delete")
    operazioni = relationship("Operazione", back_populates="medico", cascade="all, delete")
    ricoveri_responsabile = relationship("Ricovero", back_populates="medico_responsabile", cascade="all, delete")


# =======================
#         TURNO
# =======================

class Turno(Base):
    __tablename__ = "turni"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    ora_inizio = Column(Time, nullable=False)
    ora_fine = Column(Time, nullable=False)
    tipo_turno = Column(String)

    id_medico = Column(Integer, ForeignKey("medici.id"), nullable=False)
    id_sede = Column(Integer, ForeignKey("sedi.id"), nullable=False)

    medico = relationship("Medico", back_populates="turni")
    sede = relationship("Sede", back_populates="turni")


# =======================
#      PAZIENTE
# =======================

class Paziente(Base):
    __tablename__ = "pazienti"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    codice_fiscale = Column(String, unique=True)
    email = Column(String)
    telefono = Column(String)

    prenotazioni = relationship("Prenotazione", back_populates="paziente", cascade="all, delete")
    teleconsulenze = relationship("Teleconsulenza", back_populates="paziente", cascade="all, delete")
    ricoveri = relationship("Ricovero", back_populates="paziente", cascade="all, delete")
    operazioni = relationship("Operazione", back_populates="paziente", cascade="all, delete")


# =======================
#     PRESTAZIONE
# =======================

class Prestazione(Base):
    __tablename__ = "prestazioni"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String)
    durata_minuti = Column(Integer)

    prenotazioni = relationship("Prenotazione", back_populates="prestazione", cascade="all, delete")


# =======================
#     PRENOTAZIONE
# =======================

class Prenotazione(Base):
    __tablename__ = "prenotazioni"
    __table_args__ = (
        UniqueConstraint("id_medico", "data_visita", "ora_visita", name="uq_medico_slot_prenotazione"),
    )

    id = Column(Integer, primary_key=True, index=True)
    data_visita = Column(Date, nullable=False)
    ora_visita = Column(Time, nullable=False)
    stato = Column(String)

    id_paziente = Column(Integer, ForeignKey("pazienti.id"), nullable=False)
    id_medico = Column(Integer, ForeignKey("medici.id"), nullable=False)
    id_prestazione = Column(Integer, ForeignKey("prestazioni.id"), nullable=False)
    id_sede = Column(Integer, ForeignKey("sedi.id"), nullable=False)

    paziente = relationship("Paziente", back_populates="prenotazioni")
    medico = relationship("Medico", back_populates="prenotazioni")
    prestazione = relationship("Prestazione", back_populates="prenotazioni")
    sede = relationship("Sede", back_populates="prenotazioni")

    referto = relationship("Referto", back_populates="prenotazione", uselist=False, cascade="all, delete")


# =======================
#   TELECONSULENZA
# =======================

class Teleconsulenza(Base):
    __tablename__ = "teleconsulenze"
    __table_args__ = (
        UniqueConstraint("id_medico", "data", "ora", name="uq_medico_slot_teleconsulenza"),
    )

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    ora = Column(Time, nullable=False)
    stato = Column(String)
    motivo = Column(String)

    id_paziente = Column(Integer, ForeignKey("pazienti.id"), nullable=False)
    id_medico = Column(Integer, ForeignKey("medici.id"), nullable=False)

    paziente = relationship("Paziente", back_populates="teleconsulenze")
    medico = relationship("Medico", back_populates="teleconsulenze")


# =======================
#      RICOVERO
# =======================

class Ricovero(Base):
    __tablename__ = "ricoveri"

    id = Column(Integer, primary_key=True, index=True)
    data_ingresso = Column(Date, nullable=False)
    data_dimissione = Column(Date, nullable=True)
    motivo = Column(String)
    stato = Column(String)

    id_paziente = Column(Integer, ForeignKey("pazienti.id"), nullable=False)
    id_reparto = Column(Integer, ForeignKey("reparti.id"), nullable=False)
    id_sede = Column(Integer, ForeignKey("sedi.id"), nullable=False)

    # opzionale: medico responsabile del ricovero
    id_medico_responsabile = Column(Integer, ForeignKey("medici.id"), nullable=True)

    paziente = relationship("Paziente", back_populates="ricoveri")
    reparto = relationship("Reparto", back_populates="ricoveri")
    sede = relationship("Sede", back_populates="ricoveri")
    medico_responsabile = relationship("Medico", back_populates="ricoveri_responsabile")


# =======================
#      OPERAZIONE
# =======================

class Operazione(Base):
    __tablename__ = "operazioni"

    id = Column(Integer, primary_key=True, index=True)
    data_operazione = Column(Date, nullable=False)
    ora_operazione = Column(Time, nullable=False)
    tipo = Column(String, nullable=False)
    esito = Column(String)
    stato = Column(String, default="programmata")

    id_paziente = Column(Integer, ForeignKey("pazienti.id"), nullable=False)
    id_medico = Column(Integer, ForeignKey("medici.id"), nullable=False)
    id_reparto = Column(Integer, ForeignKey("reparti.id"), nullable=False)
    id_sede = Column(Integer, ForeignKey("sedi.id"), nullable=False)

    paziente = relationship("Paziente", back_populates="operazioni")
    medico = relationship("Medico", back_populates="operazioni")
    reparto = relationship("Reparto", back_populates="operazioni")
    sede = relationship("Sede", back_populates="operazioni")


# =======================
#        REFERTO
# =======================

class Referto(Base):
    __tablename__ = "referti"

    id = Column(Integer, primary_key=True, index=True)
    data_referto = Column(Date, nullable=False)
    descrizione = Column(Text, nullable=False)
    esito = Column(String)
    file_pdf = Column(String, nullable=True)

    id_prenotazione = Column(Integer, ForeignKey("prenotazioni.id"), nullable=False, unique=True)
    prenotazione = relationship("Prenotazione", back_populates="referto")

class UserRole(str, Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # collegamenti opzionali
    paziente_id = Column(Integer, ForeignKey("pazienti.id"), nullable=True)
    medico_id = Column(Integer, ForeignKey("medici.id"), nullable=True)

    paziente = relationship("Paziente")
    medico = relationship("Medico")

    is_active = Column(Boolean, default=True)