from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:3000",  
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Define Pydantic models for user info and product info
class UserInfo(BaseModel):
    name: str
    email: str
    city: str

class ProductInfo(BaseModel):
    id: int
    title: str
    price: float

# Endpoint to handle form submission
@app.post("/submit-form/")
async def submit_form(user_info: UserInfo, product_info: ProductInfo):
    try:
        # No need to manually call validate() on Pydantic models
        # If data doesn't match the model schema, FastAPI will automatically raise a ValidationError
        send_email(user_info, product_info)
    except ValidationError as e:
        # If validation fails, return a 422 Unprocessable Entity error with the details
        raise HTTPException(status_code=422, detail=str(e))

    return {"message": "Form submitted successfully"}

# Function to send email
def send_email(user_info: UserInfo, product_info: ProductInfo):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'f_adjissi@estin.dz'
    smtp_pass = 'sama7niyaraby'
    sender_email = smtp_user
    receiver_email = 'f_adjissi@estin.dz'  # Email address where you want to receive notifications

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'New Form Submission'

    email_body = f"""
    New Form Submission:
    Name: {user_info.name}
    Email: {user_info.email}
    City: {user_info.city}

    Product Info:
    id: {product_info.id}
    Title: {product_info.title}
    Price: {product_info.price}
    """

    message.attach(MIMEText(email_body, 'plain'))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(message)
