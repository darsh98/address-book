from pydantic import BaseModel, validator
from fastapi import status
from datetime import datetime
from core.response import ResponseInfo
import core.messages as message



class AddressSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    name: str
    latitude: float
    longitude: float


class CreateAddressSchema(BaseModel):
    '''
    This schema is used for creating and updating addresses.
    It also includes validators to validate the input data.
    '''
    name: str
    latitude: float
    longitude: float
    
    
    @validator('name')
    def validate_name(cls, name):
        if not name or not name.strip():
            return ResponseInfo(status_code=status.HTTP_400_BAD_REQUEST, success=False, 
                                message=message.NAME_VALIDATE).errro_res()
        return name

    @validator('latitude')
    def validate_latitude(cls, latitude):
        if latitude < -90 or latitude > 90:
            return ResponseInfo(status_code=status.HTTP_400_BAD_REQUEST, success=False, 
                    message=message.LATITUDE_VALIDATE).errro_res()
        return latitude

    @validator('longitude') 
    def validate_longitude(cls, longitude):
        if longitude < -180 or longitude > 180:
            return ResponseInfo(status_code=status.HTTP_400_BAD_REQUEST, success=False, 
                    message=message.LONGITUDE_VALIDATE).errro_res()
        return longitude

