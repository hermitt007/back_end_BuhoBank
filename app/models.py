from pydantic import BaseModel, EmailStr
from typing import Optional, List
from typing import Union

class AddressModel(BaseModel):
    street: str
    city: str
    state: str
    zip: str

class CustomerModel(BaseModel):
    firstName: str
    lastName: str
    address: AddressModel
    phoneNumber: str
    email: EmailStr
    user:str
    password:str
    accounts: Optional[List[str]] = []

class UpdateCustomerModel(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    address: Optional[AddressModel]
    phoneNumber: Optional[str]
    email: Optional[EmailStr]
    accounts: Optional[List[str]]
