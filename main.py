from urllib import response
from typing import List
from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'http://localhost:3000'
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['Content-Type','application/xml'],
)

DATABASE_URL = "postgresql://jajekzvdqtfyrh:e437bf33634dfd8a905cf65d99edf51cbc36a7e67c720245425537cbf157896e@ec2-54-82-205-3.compute-1.amazonaws.com:5432/d8g1ah013qjnrg"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)

class Note(BaseModel):
    id: int
    text: str
    completed: bool

class NoteIn(BaseModel):
    text: str
    completed: bool
 


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
  

@app.get("/notes/", response_model=List[Note])   
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query) 

@app.post("/notes/", response_model=List[Note])   
async def create_notes(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}