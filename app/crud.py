from .database import customer_collection
from .models import CustomerModel
from .models import LogInModel
from bson import ObjectId
import bcrypt

async def add_customer(customer_data: CustomerModel) -> dict:
    # Hashear la contraseña antes de almacenarla
    hashed_password = bcrypt.hashpw(customer_data.password.encode('utf-8'), bcrypt.gensalt())
   # Convertir el modelo a un diccionario serializable
    customer_dict = customer_data.dict(by_alias=True)
    customer_dict['password'] = hashed_password.decode('utf-8')  # Almacenar la contraseña hasheada
    # Insertar el cliente en la base de datos y obtener el ID insertado
    result = await customer_collection.insert_one(customer_dict)
    inserted_id = result.inserted_id

    # Buscar el cliente recién insertado
    new_customer = await customer_collection.find_one({"_id": inserted_id})

    # Convertir el _id de ObjectId a str
    if new_customer:
        new_customer['_id'] = str(new_customer['_id'])
        
    type(new_customer)

    return new_customer


async def checkData(credentials: LogInModel) -> bool:
    query = {
        "user": credentials.user
    }
    user = await customer_collection.find_one(query)
    if user is None:
        print(f"Usuario {credentials.user} no encontrado")
        return False
    else:
        print(f"Usuario {credentials.user} encontrado con exito")
    
    hashed_password=user.get('password','')
    if bcrypt.checkpw(credentials.password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True
    else:
        return False
    
