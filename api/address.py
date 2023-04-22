from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from models import Address
from schemas import AddressSchema, CreateAddressSchema
from geopy.distance import geodesic
from core.db import get_db
import core.messages as message
from core.response import ResponseInfo
from typing import List


router = APIRouter()


@router.post('/addresses', status_code=status.HTTP_201_CREATED)
def create_address(
    address: CreateAddressSchema, 
    db: Session = Depends(get_db)
):
    '''
    This API is to create address.
    '''
    db_address = Address(name=address.name, latitude=address.latitude, longitude=address.longitude)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    response = ResponseInfo(data=db_address.to_json(), status_code=status.HTTP_201_CREATED, 
                            message=message.ADDRESS_CREATED)
    return response.success_res()




@router.put('/addresses/{address_id}', status_code=status.HTTP_200_OK)
def update_address(
    address_id: int, 
    address: CreateAddressSchema, 
    db: Session = Depends(get_db)
):
    '''
    This API is to update address.
    '''
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if not db_address:
        return ResponseInfo(status_code=status.HTTP_404_NOT_FOUND, 
                            message=message.ADDRESS_NOT_FOUND, success=False).error_res()

    db_address.name = address.name
    db_address.latitude = address.latitude
    db_address.longitude = address.longitude        
    db.commit()
    db.refresh(db_address)
    response = ResponseInfo(data=db_address.to_json(), status_code=status.HTTP_200_OK, 
                            message=message.ADDRESS_UPDATED)
    return response.success_res()



@router.delete('/addresses/{address_id}', status_code=status.HTTP_200_OK)
def delete_address(
    address_id: int, 
    db: Session = Depends(get_db)
):
    '''
    This API is to delete address.
    '''
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if not db_address:
        return ResponseInfo(status_code=status.HTTP_404_NOT_FOUND, 
                            message=message.ADDRESS_NOT_FOUND, success=False).errro_res()
    db.delete(db_address)
    db.commit()
    return ResponseInfo(data=[], status_code=status.HTTP_200_OK, 
                        message=message.ADDRESS_DELETED).success_res()



@router.get('/addresses', response_model=List[AddressSchema], status_code=status.HTTP_200_OK)
def get_addresses_within_distance(
    distance: float, 
    latitude: float, 
    longitude: float, 
    db: Session = Depends(get_db)
):
    '''
    This API is used to get addresses within a certain distance from given coordinates.
    It utilizes the geopy package to convert the provided coordinates to kilometers 
    and checks if the calculated distance is less than or equal to the distance parameter passed.
    '''
    if distance <= 0:        
        return ResponseInfo(status_code=status.HTTP_400_BAD_REQUEST, 
                            message=message.DISTANCE_NOT_ZERO, success=False).errro_res()
        
    addresses = db.query(Address).all()
    
    addresses_within_distance = list(
        map(
            lambda address: address.to_json(),
            filter(
                lambda address: geodesic((latitude, longitude), (address.latitude, address.longitude)).km <= distance,
                addresses
            )
        )
    )

    response = ResponseInfo(data=addresses_within_distance, status_code=status.HTTP_200_OK, 
                        message=message.SUCCESS)
    return response.success_res()













# @router.get('/addresses', response_model=List[AddressSchema], status_code=status.HTTP_200_OK)
# def get_addresses(
#     distance: float, 
#     latitude: float, 
#     longitude: float, 
#     db: Session = Depends(get_db)
# ):
#     # addresses = db.query(Address).all()
#     # print(addresses)
#     # addresses_within_distance = []
#     # for address in addresses:
#     #     coords = (address.latitude, address.longitude)
#     #     distance_to_address = great_circle(coords, (latitude, longitude)).km
#     #     if distance_to_address <= distance:
#     #         addresses_within_distance.append(address)
#     # return addresses_within_distance

#     addresses = db.query(Address).filter(
#         func.ST_DistanceSphere(
#             Address.latitude,
#             Address.longitude,
#             latitude,
#             longitude
#         ) <= distance * 1000  # Convert distance from km to meters
#     ).all()
#     response = ResponseInfo(data=addresses, status_code=status.HTTP_200_OK, 
#                         message=message.SUCCESS)
#     return response.success_res()
