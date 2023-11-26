from sqlalchemy import create_engine, inspect, select
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import stripe
from telebot import TeleBot

from config import DB_URL, STRIPE_API_KEY, TELEGRAM_ADMIN_ID, TELEGRAM_BOT_TOKEN, TELEGRAM_PREMIUM_CHANNEL_ID

from db.base import Base
from db.models import Users

stripe.api_key = STRIPE_API_KEY
bot = TeleBot(TELEGRAM_BOT_TOKEN)

engine = create_engine(DB_URL, echo=True)
exist = inspect(engine).has_table("users")

if not exist:
   print("Running for the first time. Creating table - users")
   Base.metadata.create_all(engine)
else:
   print("Table users - already exists")

def main_job():
   print("running....")
   try:
      with engine.connect() as conn:
         
         # get users with valid_until < now()
         sql = select(Users).where(Users.valid_until < datetime.utcnow())
         result = conn.execute(sql)
         for user in result:
            print(user)
            
            # delete stripe subscription
            if user.payment_method == "stripe":
               print("deleting stripe subscription")
               stripe.Subscription.delete(user.subscription_id)

            # delete user from db
            print("deleting user from db")
            sql = Users.__table__.delete().where(Users.telegram_id == user.telegram_id)
            conn.execute(sql)
            conn.commit()
            
            # send message to admin
            print("sending message to admin")
            bot.send_message(TELEGRAM_ADMIN_ID, f"User {user.telegram_id} has been kicked from the group because his subscription has expired")
            
            # kick user from the group
            print("kicking user from the group")
            bot.unban_chat_member(TELEGRAM_PREMIUM_CHANNEL_ID, user.telegram_id)
            
            
   except Exception as e:
      print("Error when connecting to the database", e)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main_job, 'interval', hours=1)
    scheduler.start()