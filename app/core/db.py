from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import contextmanager


app = FastAPI()
load_dotenv()  # take environment variables from .env.
Base = declarative_base()



class DatabaseManager:
    def __init__(self):
        ## get db from env var
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL environment variable not set")
        ## create the engine
        self.engine = create_engine(db_url, 
                                    pool_pre_ping=True, ##test connecttion beofer using it

                                    pool_size=10, ## keep this many connections readt
                                    max_overflow=20, ## allow this many over the pool size
                                    pool_timeout=30, ## wait this lofn for a coneection
                                    pool_recycle=1800, ## referesh conecitons every hr
                                    
                                    )
        ## create a configured "Session" class
        ##make indiviusla conversations
        self.SessionLocal = sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=self.engine)

        """
            Context manager for database sessions.
            This is the "conversation handler" - it:
            1. Opens a conversation with the database
            2. Lets you do your work
            3. Automatically closes the conversation (even if something breaks)
        """
    @contextmanager
    def get_session(self):
        
        session = self.SessionLocal()

        try:
            yield session ## do my work
            session.commit() ## save changes

        except Exception as e:
            session.rollback() ## cancel cnhanges inf something went wrong
            raise

        finally:
            session.close() ## close the convo


## create a global instase
db_manager = DatabaseManager()

## convention function for easy access
def get_db_session():
    ## get a dabase session

    return db_manager.get_session()
         

from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.sql import func
        
         
         
class HealthCheck(Base):
    __tablename__ = "healthcheck"

    id = Column(Integer, primary_key=True,  autoincrement=True)
    note = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    
    









