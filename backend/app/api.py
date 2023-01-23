from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

todos = [
    {
        "id": "1",
        "item": "Read a book."
    },
    {
        "id": "2",
        "item": "Cycle around town."
    }
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": todos }

@app.get("/config")
async def get_config() -> dict:
    return {
        "publishableKey":os.getenv("STRIPE_PUBLISHABLE_KEY")
    }


@app.post("/create-payment-intent")
async def get_config() -> dict:
    # return {"clientSecret":"yes"}
    try:
        paymentIntent = stripe.PaymentIntent.create(
            amount=2000,
            currency="usd",
            payment_method="pm_card_visa"
        )
        return {"clientSecret": paymentIntent['client_secret']}
    except Exception as error:
        return {"error":{"message":error}}
