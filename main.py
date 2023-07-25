from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd
import numpy as np
import pickle
from create_similarity import SIMILARITY

TOKEN: Final = "6389620358:AAGOPTlX2-IHfK8SxNdNDq3_Ulac3mewdbg"
BOT_USERNAME: Final = '@movie_botrec'
# SIMILARITY = pickle.load(open("similarity.pkl", "rb")), similarity.pkl was too big, created it in create_similarity.py and imported it instead
MOVIE_DICT = pickle.load(open("movie_dict.pkl", "rb"))
MOVIES = pd.DataFrame(MOVIE_DICT)

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! What movie have you watched recently? ")
    print(MOVIES["title"])


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type in movie titles so I can recommend some similar ones!")


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot stopped")



#Responses
def handle_response(text: str) -> str:
    # processed: str = text.lower()
    try:
        sb = "The list of similar movies can be found below: \n"
        arr = recommend(text)
        if arr:
            for i in arr:
                sb += i + "\n"
            return sb[:-1]
    except IndexError:
        sb = "Please input the full name of the movie"
    return sb

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


#Generate Recs
def recommend(movie):
    arr = []
    movie_idx = MOVIES[MOVIES['title'] == movie].index[0]
    distances = SIMILARITY[movie_idx]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in similar_movies:
        arr.append(MOVIES.iloc[i[0]].title)
    return arr

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", stop_command))

    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Polling...")
    app.run_polling(poll_interval=3)
