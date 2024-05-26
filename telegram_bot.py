from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram import Update
import logging
from reddit import get_random_reddit_post, create_audio, create_video, test
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TEXT, CONFIRMATION = range(2)
text = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Use /create_random to create a random Reddit video or /create_text <text> to create a video from the provided text.")


async def create_reddit_tiktok_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Send me a text!')
    return TEXT


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global text
    text = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Confirm? (yes or no)')
    return CONFIRMATION


async def create_random_reddit_tiktok_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Retrieving random reddit post.')
    global text
    text = get_random_reddit_post()
    if text == "":
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Error has occurred! Please try again..')
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Confirm? (yes or no)')
    return CONFIRMATION


async def confirmation_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text.lower()
    if user_response == 'yes':
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Creating audio...')
        audio_file, time_points= create_audio(text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Creating video...')
        video_path = create_video(audio_file, time_points)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Sending video...')
        await context.bot.send_document(
            chat_id=update.message.chat_id, 
            document=open(video_path, 'rb'),
            read_timeout=300,
            write_timeout=300,
            connect_timeout=300
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Video sent!')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='OK! Let me know if you want to create a video')
    
    return ConversationHandler.END
    

        
def main():
    print('starting bot...')
    application = ApplicationBuilder().token(TOKEN)\
                                      .read_timeout(300)\
                                      .write_timeout(300)\
                                      .connect_timeout(300)\
                                      .build()
    
    start_handler = CommandHandler('start', start)
    create_random_handler = ConversationHandler(
        entry_points=[CommandHandler('create_random', create_random_reddit_tiktok_video)],
        states={
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmation_response)]
        },
        fallbacks=[]
    )
    create_text_handler = ConversationHandler(
        entry_points=[CommandHandler('create_text', create_reddit_tiktok_video)],
        states={
            TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmation_response)]
        },
        fallbacks=[]
    )

    application.add_handler(start_handler)
    application.add_handler(create_random_handler)
    application.add_handler(create_text_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()
