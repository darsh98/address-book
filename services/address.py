from geopy.distance import geodesic
from typing import List
from schemas import AddressSchema


def get_address_by_distance(
    distance: float,
    latitude: float,
    longitude: float,
    addresses: List[AddressSchema]
):
    
    return list(
        map(
            lambda address: address.to_json(),
            filter(
                lambda address: geodesic((latitude, longitude), (address.latitude, address.longitude)).km <= distance,
                addresses
            )
        )
    )