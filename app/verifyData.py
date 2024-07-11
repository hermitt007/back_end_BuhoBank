from .database import customer_collection
from .models import CustomerModel

async def verifyDataCI(customer_data: CustomerModel) -> dict:
    query = {
        "ci": customer_data.ci
    }
    user_data= await customer_collection.find_one(query)
    return user_data is None
       

#para el nombre de usuario repetido
async def verifyDataUser(customer_data: CustomerModel) -> bool:
    query = {
        "user": customer_data.user
    }
    user_data = await customer_collection.find_one(query)
    return user_data is not None



#para el correo electronico repetido 
async def verifyDataEmail(customer_data: CustomerModel) -> bool:
    query = {
        "email": customer_data.email
    }
    user_data = await customer_collection.find_one(query)
    return user_data is not None