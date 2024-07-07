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

class LogInModel(BaseModel):
    email: EmailStr
    password: str
