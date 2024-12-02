from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from time import time

app = FastAPI()

# Models
class StageDTO(BaseModel):
    name: str
    duration_seconds: float = 0.0  # Текущее общее время
    timer_start: Optional[float] = None  # Время старта секундомера

class IterationDTO(BaseModel):
    name: str
    stages: List[StageDTO] = []

class ProcessDTO(BaseModel):
    name: str
    iterations: List[IterationDTO] = []

# Словарь для хранения данных
processes_db = {}

# Обработчик для корневого маршрута
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# API для создания нового процесса
@app.post("/processes/")
async def create_process(process: ProcessDTO):
    process_id = len(processes_db) + 1
    processes_db[process_id] = process
    return {"process_id": process_id}

# API для получения списка процессов
@app.get("/processes/", response_model=List[ProcessDTO])
async def get_processes():
    return list(processes_db.values())

# API для добавления этапа в процесс
@app.post("/processes/{process_id}/stages/")
async def add_stage(process_id: int, stage: StageDTO):
    if process_id not in processes_db:
        raise HTTPException(status_code=404, detail="Process not found")
    processes_db[process_id].stages.append(stage)
    return {"message": "Stage added successfully"}


# API для начала секундомера на этапе
@app.post("/processes/{process_id}/stages/{stage_id}/start")
async def start_timer(process_id: int, stage_id: int):
    if process_id not in processes_db:
        raise HTTPException(status_code=404, detail="Process not found")
    
    process = processes_db[process_id]
    if stage_id >= len(process.stages):
        raise HTTPException(status_code=404, detail="Stage not found")
    
    stage = process.stages[stage_id]
    if stage.start_time is not None:
        raise HTTPException(status_code=400, detail="Timer already started")
    
    stage.start_time = time()  # Запускаем таймер
    return {"message": f"Timer started for stage {stage_id}"}

# API для остановки секундомера на этапе
@app.post("/processes/{process_id}/stages/{stage_id}/stop")
async def stop_timer(process_id: int, stage_id: int):
    if process_id not in processes_db:
        raise HTTPException(status_code=404, detail="Process not found")
    
    process = processes_db[process_id]
    if stage_id >= len(process.stages):
        raise HTTPException(status_code=404, detail="Stage not found")
    
    stage = process.stages[stage_id]
    if stage.start_time is None:
        raise HTTPException(status_code=400, detail="Timer has not been started")
    
    stage.end_time = time()  # Останавливаем таймер
    elapsed_time = stage.end_time - stage.start_time
    return {"message": f"Timer stopped for stage {stage_id}", "elapsed_time": elapsed_time}

# API для получения информации о процессе
@app.get("/processes/{process_id}")
async def get_process(process_id: int):
    if process_id not in processes_db:
        raise HTTPException(status_code=404, detail="Process not found")
    return processes_db[process_id]