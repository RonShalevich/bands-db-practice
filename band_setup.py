import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Band(Base):
    __tablename__ = 'band'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    bio = Column(String(250))
    music = Column(String(250))
    video = Column(String(250))
    pic = Column(String(250))
    track = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'bio': self.bio,
            'music': self.music,
            'video': self.video,
            'pic': self.pic,
            'track': self.track,
        }


engine = create_engine('sqlite:///bands.db')

Base.metadata.create_all(engine)
