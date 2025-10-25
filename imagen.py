import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# === CONFIGURACIÓN ===
TOKEN = os.environ["BOT_TOKEN"]          # ¡Esta variable DEBE estar en Railway!
GRUPO_ID = -1002443349220                # ID del grupo (con -100)
TOPIC_ID = 26431                         # ID del tema
STICKER_FILE_ID = "CAACAgQAAyEFAASRoozkAAJnV2j9BKH1Al2z96_OjzMAAbWrbkOA6AACaQEAAno2ig23KLlCi4SZUDYE"

async def reenviar_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    if update.message.photo:
        photo = update.message.photo[-1]
        caption = update.message.caption or ""

        try:
            await context.bot.send_photo(
                chat_id=GRUPO_ID,
                photo=photo.file_id,
                caption=caption,
                message_thread_id=TOPIC_ID
            )
            await context.bot.send_message(
                chat_id=GRUPO_ID,
                text="━━━━━━━━━━━━━━━━━━━\n✅ Esta Información fue reenviada del Grupo VIP 👑",
                message_thread_id=TOPIC_ID
            )
            await context.bot.send_sticker(
                chat_id=GRUPO_ID,
                sticker=STICKER_FILE_ID,
                message_thread_id=TOPIC_ID
            )
            await update.message.reply_text("✅ Imagen y sticker enviados al tema correctamente.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("Por favor, envía una imagen como foto.")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, reenviar_imagen))
    print("✅ Bot activo. Envía una imagen para reenviarla + mensaje + sticker.")
    app.run_polling()
