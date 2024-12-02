from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Process(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Связь с итерациями
    iterations = relationship("Iteration", back_populates="process", cascade="all, delete-orphan")

class Iteration(Base):
    __tablename__ = "iterations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"))

    # Связь с этапами
    stages = relationship("Stage", back_populates="iteration", cascade="all, delete-orphan")

    # Связь с процессом
    process = relationship("Process", back_populates="iterations")

class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    iteration_id = Column(Integer, ForeignKey("iterations.id"))
    timer_start = Column(DateTime, nullable=True)
    timer_end = Column(DateTime, nullable=True)

    # Связь с итерацией
    iteration = relationship("Iteration", back_populates="stages")