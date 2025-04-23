from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from fastapi.routing import APIRouter
import json
from pathlib import Path
from typing import List, Optional 

# === MODELE DE DONNEE ===
class DashboardInfo(BaseModel):
    ip_locale: str
    hostname: str
    devices_count: int
    latence_wan: str
    version_app: str
    devices: Optional[List[dict]] = []  # ✅ On ajoute les résultats ici


class Sonde(BaseModel):
    id: int
    name: str
    status: str 
    ip_address: str
    dashboard_info: DashboardInfo
    last_scan: Optional[str] = None

# === CHEMIN VERS LE FICHIER JSON ===
DATA_FILE = Path("data/sondes.json")

# === FONCTIONS DE LECTURE/SAUVEGARDE ===
def load_sondes() -> List[Sonde]:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Sonde(**s) for s in data]
            except json.JSONDecodeError:
                return []
    return []

def save_sondes(sondes: List[Sonde]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([s.dict() for s in sondes], f, indent=4, ensure_ascii=False)

# === BASE DE DONNEES CHARGÉE EN MÉMOIRE ===
sondes_db: List[Sonde] = load_sondes()

# === ROUTEUR API ===
router = APIRouter()

@router.get("/", response_model=List[Sonde])
def get_sondes():
    return sondes_db

@router.get("/{sonde_id}/dernier-scan")
def get_dernier_scan(sonde_id: int):
    for sonde in sondes_db:
        if sonde.id == sonde_id:
            return {
                "hostname": sonde.dashboard_info.hostname,
                "ip": sonde.ip_address,
                "devices": sonde.dashboard_info.devices
            }
    raise HTTPException(status_code=404, detail="Sonde non trouvée")

@router.get("/{sonde_id}", response_model=Sonde)
def get_sonde(sonde_id: int):
    for sonde in sondes_db:
        if sonde.id == sonde_id:
            return sonde
    raise HTTPException(status_code=404, detail="Sonde non trouvée")

@router.post("/", response_model=dict)
def create_sonde(sonde: Sonde = Body(...)):
    # Vérifie si une sonde avec la même IP existe déjà
    for i, s in enumerate(sondes_db):
        if s.ip_address == sonde.ip_address:
            sonde.id = s.id  # Conserve l’ancien ID
            sondes_db[i] = sonde  # Mise à jour
            save_sondes(sondes_db)
            return {"message": "Sonde mise à jour", "sonde": sonde}

    # Attribue un nouvel ID automatiquement
    sonde.id = max([s.id for s in sondes_db], default=0) + 1
    sondes_db.append(sonde)
    save_sondes(sondes_db)
    return {"message": "Nouvelle sonde ajoutée", "sonde": sonde}

@router.put("/{sonde_id}", response_model=Sonde)
def update_sonde(sonde_id: int, updated_sonde: Sonde = Body(...)):
    for i, sonde in enumerate(sondes_db):
        if sonde.id == sonde_id:
            sondes_db[i] = updated_sonde
            save_sondes(sondes_db)
            return updated_sonde
    raise HTTPException(status_code=404, detail="Sonde non trouvée")

@router.delete("/{sonde_id}")
def delete_sonde(sonde_id: int):
    for i, sonde in enumerate(sondes_db):
        if sonde.id == sonde_id:
            del sondes_db[i]
            save_sondes(sondes_db)
            return {"message": "Sonde supprimée"}
    raise HTTPException(status_code=404, detail="Sonde non trouvée")

# === APP FASTAPI ===
app = FastAPI(title="API Seahawks Nester")
app.include_router(router, prefix="/sondes", tags=["sondes"])