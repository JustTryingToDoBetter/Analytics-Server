from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.db import db_manager, HealthCheck, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    ##startup code
    print("Starting up...")
    Base.metadata.create_all(bind=db_manager.engine)
    print("Database tables created.")
    ## shutdown code
    yield
    print("Shutting down...")
    db_manager.engine.dispose()


app=FastAPI(lifespan=lifespan)

# dependency to get DB session
def get_db():
    with db_manager.get_session() as session:
        yield session

## endpoints to healthcheck
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Check if the database is working"""
    try:
        ## create ne hea;th heck entry
        health_record = HealthCheck(note="I am sick")
        db.add(health_record)
        db.commit()

        return {"status": "healthy", "message": "Database connection successful"}
         
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}


@app.get("/healthchecks")
async def get_healthchecks(db: Session = Depends(get_db)):
    """Get all health check records"""
    records = db.query(HealthCheck).all()
    return [{"id": r.id, "note": r.note, "created_at": r.created_at} for r in records]

@app.post("/healthcheck")
async def create_healthcheck(note: str, db: Session = Depends(get_db)):
    """Create a new health check record"""
    health_record = HealthCheck(note=note)
    db.add(health_record)
    db.commit()
    return {"message": "Health check created", "id": health_record.id}