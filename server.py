from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from aiogram import Bot
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

engine = create_engine("sqlite:///contact_requests.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

table = Table(
    "contact_requests",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("full_name", String),
    Column("email", String),
    Column("message", String),
)

metadata.create_all(engine)

session = SessionLocal()


class ContactForm(BaseModel):
    full_name: str
    email: str
    message: str


@app.post("/contact/")
async def create_contact_form(form: ContactForm, request: Request):
    try:
        session.execute(
            table.insert().values(
                full_name=form.full_name, email=form.email, message=form.message
            )
        )
        session.commit()
        session.close()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Could not save contact form.")

    # Send message to Telegram chat
    try:
        await bot.send_message(
            TELEGRAM_CHAT_ID,
            f'New contact request from "{form.full_name}" ({form.email}): \n{form.message}',
            parse_mode="HTML",
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Message saved. Could not send message to Admin."
        )

    return "success"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
