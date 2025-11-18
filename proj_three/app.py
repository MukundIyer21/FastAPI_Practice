from fastapi import FastAPI
from classes import Base, engine, sessionmaker
import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="To-Do List API", version="1.0.0")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app.include_router(auth.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)