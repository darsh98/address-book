from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json

Base = declarative_base()

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


    def as_dict(self):
        '''
        This function is to convert object to dictionary
        '''
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def to_json(self):
        '''
        This function is to convert dictionary to json.
        '''
        return json.loads(json.dumps(self.as_dict(), default=self._datetime_handler))

    def _datetime_handler(self, obj):
        '''
        This function is to handel datetime object.
        '''
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        raise TypeError("Object of type {} is not JSON serializable".format(type(obj)))