import os
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI(title="College Calendar")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["calendar_db"]
events_collection = db["events"]

class Event(BaseModel):
    title: str
    date: str  # YYYY-MM-DD
    time: str = ""  # HH:MM (optional)
    description: str = ""
    color: str = "#1a73e8"  # Google Calendar default blue

def serialize_event(doc):
    return {
        "id": str(doc["_id"]),
        "title": doc.get("title", ""),
        "date": doc.get("date", ""),
        "time": doc.get("time", ""),
        "description": doc.get("description", ""),
        "color": doc.get("color", "#1a73e8")
    }

@app.get("/")
def get_index():
    with open("index.html") as f:
        return HTMLResponse(f.read())

@app.get("/events")
def get_events():
    try:
        docs = events_collection.find()
        return [serialize_event(doc) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/events")
def add_event(ev: Event):
    try:
        data = ev.model_dump() if hasattr(ev, "model_dump") else ev.dict()
        result = events_collection.insert_one(data)
        data.pop("_id", None)  # pymongo injects ObjectId into data; FastAPI can't JSON-encode it
        return {"id": str(result.inserted_id), **data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/events/{ev_id}")
def edit_event(ev_id: str, ev: Event):
    if not ObjectId.is_valid(ev_id):
        raise HTTPException(status_code=400, detail="Invalid event ID")
    try:
        data = ev.model_dump() if hasattr(ev, "model_dump") else ev.dict()
        result = events_collection.update_one({"_id": ObjectId(ev_id)}, {"$set": data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"id": ev_id, **data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/events/{ev_id}")
def del_event(ev_id: str):
    if not ObjectId.is_valid(ev_id):
        raise HTTPException(status_code=400, detail="Invalid event ID")
    try:
        result = events_collection.delete_one({"_id": ObjectId(ev_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
