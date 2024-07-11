from .database import customer_collection
from .models import CustomerModel

async def verifyDataCI(customer_data: CustomerModel) -> dict:
    query = {
        "ci": customer_data.ci
    }
    user_data= await customer_collection.find_one(query)
    if user_data is None:
        return False
        
    else:
        return True
    

#Sergio has para el nombre de usuario repetido



#para el correo electronico repetido 