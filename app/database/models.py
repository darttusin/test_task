from sqlalchemy import (Column, Integer, String, TIMESTAMP,
                        PrimaryKeyConstraint)
from sqlalchemy.orm import declarative_base


base = declarative_base()


# модель для бд
class Texts(base):
    __tablename__ = 'texts'

    text_id = Column(String, nullable=False)
    rubrics = Column(String, nullable=False)
    text_ = Column(String, nullable=False)
    created_date = Column(TIMESTAMP(timezone=False), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('text_id'),
    )
