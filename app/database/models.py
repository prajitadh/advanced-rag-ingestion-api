#SQLAlchemy model == Python x SQL Table
from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from datetime import datetime

from app.database.db import Base

#think of models as tables
#this is  a document model
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    file_type = Column(String, nullable=False)

    chunking_strategy = Column(String, nullable=False)

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    #Booking Model (same as SQL Table)
    class Booking(Base):
        __tablename__ = "bookings"

        id = Column(Integer, primary_key=True, index=True)

        name = Column(String, nullable=False)

        email = Column(String, nullable=False)

        interview_date = Column(Date, nullable=False)

        interview_time = Column(Time, nullable=False)

        created_at = Column(
            DateTime,
            default=datetime.utcnow
    )

    #these are model definition, they are not created yet, it should be called inside main.py for creation.