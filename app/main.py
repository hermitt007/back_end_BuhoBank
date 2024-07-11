from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .models import CustomerModel, LogInModel
from .crud import add_customer
from .crud import checkData
from fastapi.encoders import jsonable_encoder
from .verifyData import verifyDataCI, verifyDataEmail,verifyDataUser


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
    ci=await verifyDataCI(customer)
    if ci:
        response=jsonable_encoder({"code":"CI_REPEAT"})
        return JSONResponse(status_code=201, content=response)
    elif await verifyDataUser(customer):
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
