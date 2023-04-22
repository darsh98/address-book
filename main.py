from fastapi import FastAPI
from api.address import router


# This is the main FastAPI application instance for the Address Book API.
app = FastAPI(
    title="Address Book API",
    description="An API for managing addresses in an address book",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/",
    redoc_url="/redoc",
)

'''
This is the router instance for the 'Address' tag in the Address Book API.
It includes endpoints for managing addresses, such as creating, updating, retrieving, and deleting addresses.
'''
app.include_router(router, tags=["Address"])
