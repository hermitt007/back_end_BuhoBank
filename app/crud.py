from .database import customer_collection
from .models import CustomerModel
from .models import LogInModel
from bson import ObjectId
import bcrypt

async def add_customer(customer_data: CustomerModel) -> dict:
    # Verificar si el email, CI o usuario ya existe
    existing_customer = await customer_collection.find_one({
        "$or": [
            {"email": customer_data.email},
            {"ci": customer_data.ci},
            {"user": customer_data.user}
        ]
    })
    
    if existing_customer:
        raise ValueError("El CI, usuario o email ya existe")

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

    return new_customer

async def checkData(customer_data: CustomerModel) -> bool:
    query = {
        "email": customer_data.email,
        "password": customer_data.password
    }
    exists = await customer_collection.find_one(query)
    return exists is not None
