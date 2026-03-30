from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class PazienteBase(BaseModel):
    nome: str
    cognome: str
    codice_fiscale: str
    email: Optional[str] = None
    telefono: Optional[str] = None

class PazienteCreate(PazienteBase):
    pass

class PazienteUpdate(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    codice_fiscale: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None

class PazienteRead(PazienteBase):
    id: int
    class Config:
        from_attributes = True


class PrestazioneBase(BaseModel):
    nome: str
    tipo: Optional[str] = None
    durata_minuti: Optional[int] = None

class PrestazioneCreate(PrestazioneBase):
    pass

class PrestazioneUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    durata_minuti: Optional[int] = None

class PrestazioneRead(PrestazioneBase):
    id: int
    class Config:
        from_attributes = True


class PrenotazioneBase(BaseModel):
    data_visita: date
    ora_visita: time
    stato: Optional[str] = None
    id_paziente: int
    id_medico: int
    id_prestazione: int
    id_sede: int

class PrenotazioneCreate(PrenotazioneBase):
    pass

class PrenotazioneUpdate(BaseModel):
    data_visita: Optional[date] = None
    ora_visita: Optional[time] = None
    stato: Optional[str] = None
    id_paziente: Optional[int] = None
    id_medico: Optional[int] = None
    id_prestazione: Optional[int] = None
    id_sede: Optional[int] = None

class PrenotazioneRead(PrenotazioneBase):
    id: int
    class Config:
        from_attributes = True


class SedeBase(BaseModel):
    nome: str
    indirizzo: Optional[str] = None
    citta: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    tipo_struttura: Optional[str] = None
    numero_posti_letto: Optional[int] = None

class SedeCreate(SedeBase):
    pass

class SedeUpdate(BaseModel):
    nome: Optional[str] = None
    indirizzo: Optional[str] = None
    citta: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    tipo_struttura: Optional[str] = None
    numero_posti_letto: Optional[int] = None

class SedeRead(SedeBase):
    id: int
    class Config:
        from_attributes = True


class RepartoBase(BaseModel):
    nome: str
    piano: Optional[int] = None
    area: Optional[str] = None
    id_sede: int

class RepartoCreate(RepartoBase):
    pass

class RepartoUpdate(BaseModel):
    nome: Optional[str] = None
    piano: Optional[int] = None
    area: Optional[str] = None
    id_sede: Optional[int] = None

class RepartoRead(RepartoBase):
    id: int
    class Config:
        from_attributes = True


class MedicoBase(BaseModel):
    nome: str
    cognome: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    specializzazione: Optional[str] = None
    codice_fiscale: str
    id_reparto: int

class MedicoCreate(MedicoBase):
    pass

class MedicoUpdate(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    specializzazione: Optional[str] = None
    codice_fiscale: Optional[str] = None
    id_reparto: Optional[int] = None

class MedicoRead(MedicoBase):
    id: int
    class Config:
        from_attributes = True


class TurnoBase(BaseModel):
    data: date
    ora_inizio: time
    ora_fine: time
    tipo_turno: Optional[str] = None
    id_medico: int
    id_sede: int

class TurnoCreate(TurnoBase):
    pass

class TurnoUpdate(BaseModel):
    data: Optional[date] = None
    ora_inizio: Optional[time] = None
    ora_fine: Optional[time] = None
    tipo_turno: Optional[str] = None
    id_medico: Optional[int] = None
    id_sede: Optional[int] = None

class TurnoRead(TurnoBase):
    id: int
    class Config:
        from_attributes = True


class TeleconsulenzaBase(BaseModel):
    data: date
    ora: time
    stato: Optional[str] = None
    motivo: Optional[str] = None
    id_paziente: int
    id_medico: int

class TeleconsulenzaCreate(TeleconsulenzaBase):
    pass

class TeleconsulenzaUpdate(BaseModel):
    data: Optional[date] = None
    ora: Optional[time] = None
    stato: Optional[str] = None
    motivo: Optional[str] = None
    id_paziente: Optional[int] = None
    id_medico: Optional[int] = None

class TeleconsulenzaRead(TeleconsulenzaBase):
    id: int
    class Config:
        from_attributes = True


class RicoveroBase(BaseModel):
    data_ingresso: date
    data_dimissione: Optional[date] = None
    motivo: Optional[str] = None
    stato: Optional[str] = None
    id_paziente: int
    id_reparto: int
    id_sede: int
    id_medico_responsabile: Optional[int] = None

class RicoveroCreate(RicoveroBase):
    pass

class RicoveroUpdate(BaseModel):
    data_ingresso: Optional[date] = None
    data_dimissione: Optional[date] = None
    motivo: Optional[str] = None
    stato: Optional[str] = None
    id_paziente: Optional[int] = None
    id_reparto: Optional[int] = None
    id_sede: Optional[int] = None
    id_medico_responsabile: Optional[int] = None

class RicoveroRead(RicoveroBase):
    id: int
    class Config:
        from_attributes = True


class OperazioneBase(BaseModel):
    data_operazione: date
    ora_operazione: time
    tipo: str
    esito: Optional[str] = None
    id_paziente: int
    id_medico: int
    id_reparto: int
    id_sede: int

class OperazioneCreate(OperazioneBase):
    pass

class OperazioneUpdate(BaseModel):
    data_operazione: Optional[date] = None
    ora_operazione: Optional[time] = None
    tipo: Optional[str] = None
    esito: Optional[str] = None
    stato: Optional[str] = None
    id_paziente: Optional[int] = None
    id_medico: Optional[int] = None
    id_reparto: Optional[int] = None
    id_sede: Optional[int] = None

class OperazioneRead(OperazioneBase):
    id: int
    stato: Optional[str] = None
    class Config:
        from_attributes = True


class RefertoBase(BaseModel):
    data_referto: date
    descrizione: str
    esito: Optional[str] = None
    file_pdf: Optional[str] = None
    id_prenotazione: int

class RefertoCreate(RefertoBase):
    pass

class RefertoUpdate(BaseModel):
    data_referto: Optional[date] = None
    descrizione: Optional[str] = None
    esito: Optional[str] = None
    file_pdf: Optional[str] = None
    id_prenotazione: Optional[int] = None

class RefertoRead(RefertoBase):
    id: int
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    role: str

class UserCreate(BaseModel):
    email: str
    password: str
    role: str
    paziente_id: Optional[int] = None
    medico_id: Optional[int] = None

class UserRead(UserBase):
    id: int
    medico_id: Optional[int] = None
    paziente_id: Optional[int] = None
    is_active: Optional[bool] = None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
