from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

class UserInfo(BaseModel):
    name: str
    email: str
    city: str

class ProductInfo(BaseModel):
    id: int
    title: str
    price: float

@app.post("/submit-form/")
async def submit_form(user_info: UserInfo, product_info: ProductInfo):
    try:
       
        send_email(user_info, product_info)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"message": "Form submitted successfully"}

# Function to send email
def send_email(user_info: UserInfo, product_info: ProductInfo):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'your email'
    smtp_pass = 'your password '
    sender_email = smtp_user
    receiver_email = 'your email again' 

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
