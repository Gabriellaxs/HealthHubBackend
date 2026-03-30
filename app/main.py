from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .database import Base, engine
from .routers import (
    patients,
    appointments,
    medici,
    prestazioni,
    sedi,
    reparti,
    turni,
    teleconsulenze,
    ricoveri,
    operazioni,
    referti,
    stats,
    auth
)


def migrate_db():
    """Apply schema migrations to existing DB without losing data."""
    with engine.connect() as conn:
        # Referti: rename/add columns if using old schema
        try:
            conn.execute(text("SELECT data_referto FROM referti LIMIT 1"))
        except Exception:
            # Old schema has data_emissione and contenuto - rename them
            try:
                conn.execute(text("ALTER TABLE referti ADD COLUMN data_referto DATE"))
                conn.execute(text("UPDATE referti SET data_referto = data_emissione"))
                conn.commit()
            except Exception:
                pass
            try:
                conn.execute(text("ALTER TABLE referti ADD COLUMN descrizione TEXT"))
                conn.execute(text("UPDATE referti SET descrizione = contenuto"))
                conn.commit()
            except Exception:
                pass

        # Referti: remove legacy columns (data_emissione, contenuto) that cause NOT NULL errors.
        # SQLite does not support DROP COLUMN on older versions, so recreate the table.
        try:
            result = conn.execute(text("PRAGMA table_info(referti)"))
            columns = [row[1] for row in result.fetchall()]
            if "data_emissione" in columns:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS referti_new (
                        id INTEGER PRIMARY KEY,
                        data_referto DATE NOT NULL,
                        descrizione TEXT NOT NULL,
                        esito VARCHAR,
                        file_pdf VARCHAR,
                        id_prenotazione INTEGER NOT NULL UNIQUE REFERENCES prenotazioni(id)
                    )
                """))
                conn.execute(text("""
                    INSERT INTO referti_new (id, data_referto, descrizione, esito, file_pdf, id_prenotazione)
                    SELECT id,
                           COALESCE(data_referto, data_emissione),
                           COALESCE(descrizione, contenuto, ''),
                           esito,
                           file_pdf,
                           id_prenotazione
                    FROM referti
                """))
                conn.execute(text("DROP TABLE referti"))
                conn.execute(text("ALTER TABLE referti_new RENAME TO referti"))
                conn.commit()
        except Exception:
            pass

        # Referti: add file_pdf if not exists
        try:
            conn.execute(text("SELECT file_pdf FROM referti LIMIT 1"))
        except Exception:
            try:
                conn.execute(text("ALTER TABLE referti ADD COLUMN file_pdf VARCHAR"))
                conn.commit()
            except Exception:
                pass

        # Operazioni: add stato if not exists
        try:
            conn.execute(text("SELECT stato FROM operazioni LIMIT 1"))
        except Exception:
            try:
                conn.execute(text("ALTER TABLE operazioni ADD COLUMN stato VARCHAR DEFAULT 'programmata'"))
                conn.commit()
            except Exception:
                pass


def init_db():
    Base.metadata.create_all(bind=engine)
    migrate_db()


app = FastAPI(
    title="HealthHub API",
    description="Backend per gestione struttura sanitaria, percorso clinico e dashboard",
    version="1.0.0"
)

init_db()

app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(medici.router)
app.include_router(prestazioni.router)
app.include_router(sedi.router)
app.include_router(reparti.router)
app.include_router(turni.router)
app.include_router(teleconsulenze.router)
app.include_router(ricoveri.router)
app.include_router(operazioni.router)
app.include_router(referti.router)
app.include_router(stats.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "HealthHub API running"}
