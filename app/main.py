from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .models import CustomerModel, LogInModel
from .crud import add_customer,update_customer,checkData, update_password
from fastapi.encoders import jsonable_encoder
from .verifyData import verifyDataCI, verifyDataEmail,verifyDataUser, verify_password_requirements



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/register_user", response_description="Add new customer", response_model=CustomerModel)
async def create_customer(customer: CustomerModel):
    ci,credentials=await verifyDataCI(customer)
    if ci:
        if credentials:
            response=jsonable_encoder({"code":"CI_REPEAT"})
            return JSONResponse(status_code=201, content=response)
        else:        
            if await verifyDataUser(customer):
                response = jsonable_encoder({"code": "USER_REPEAT"})
                return JSONResponse(status_code=201, content=response)
            else:
                update = await update_customer(customer)
                if update:
                    response=jsonable_encoder({"code":"USER_CREATE"})
                    return JSONResponse(status_code=201, content=response)
    else:
        if await verifyDataUser(customer):
            response = jsonable_encoder({"code": "USER_REPEAT"})
            return JSONResponse(status_code=201, content=response)
        elif await verifyDataEmail(customer):
            response = jsonable_encoder({"code": "EMAIL_REPEAT"})
            return JSONResponse(status_code=201, content=response)
        else:
            new_customer = await add_customer(customer)
            if new_customer:
                response=jsonable_encoder({"code":"USER_CREATE"})
                return JSONResponse(status_code=201, content=response)
        
                    
        

@app.post("/login", response_model=dict)
async def logIn (Credentials: LogInModel):
    authenticate = await checkData(Credentials)
    response_data = {"authenticated": authenticate}

    # Convierte el diccionario en JSON serializable
    response_json = jsonable_encoder(response_data)

    # Devuelve la respuesta como JSONResponse
    return JSONResponse(status_code=201, content=response_json)

#Funcion para cambiar la contraseña
@app.post("/change_password", response_model=dict)
async def change_password(user_id: str, current_password: str, new_password: str):
    # Verificar que la nueva contraseña cumpla con los requisitos mínimos
    is_valid, message = verify_password_requirements(new_password)
    if not is_valid:
        return JSONResponse(status_code=400, content={"message": message, "error_code": "INVALID_NEW_PASSWORD"})

    try:
        result = await update_password(user_id, current_password, new_password)
        if "error_code" in result:
            if result["error_code"] == "INCORRECT_CURRENT_PASSWORD":
                return JSONResponse(status_code=400, content={"message": "La contraseña actual es incorrecta", "error_code": "INCORRECT_CURRENT_PASSWORD"})
        return JSONResponse(status_code=200, content=result)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})