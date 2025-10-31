import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# === CONFIGURACIÓN ===
TOKEN = os.environ["BOT_TOKEN"]
GRUPO_ID = -1002443349220
TOPIC_ID = 26431
STICKER_FILE_ID = "CAACAgQAAyEFAASRoozkAAJnV2j9BKH1Al2z96_OjzMAAbWrbkOA6AACaQEAAno2ig23KLlCi4SZUDYE"

# Ruta al logo PNG (debe estar en la misma carpeta)
LOGO_PATH = "logo_vip.png"

async def reenviar_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    if update.message.photo:
        photo = update.message.photo[-1]
        caption = update.message.caption or ""

        try:
            # 1. Descargar la imagen
            file = await context.bot.get_file(photo.file_id)
            image_bytes = await file.download_as_bytearray()

            # 2. Abrir la imagen con PIL
            img = Image.open(io.BytesIO(image_bytes))

            # 3. Cargar el logo
            logo = Image.open(LOGO_PATH).convert("RGBA")

            # 4. Redimensionar el logo (opcional)
            logo_width = int(img.width * 0.2)  # 20% del ancho de la imagen
            logo_height = int(logo.height * (logo_width / logo.width))
            logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

            # 5. Superponer el logo en la esquina inferior derecha
            position = (img.width - logo.width - 10, img.height - logo.height - 10)
            img.paste(logo, position, logo)  # El tercer argumento es la máscara de transparencia

            # 6. Guardar la imagen modificada en memoria
            output_buffer = io.BytesIO()
            img.save(output_buffer, format="JPEG", quality=85)
            output_buffer.seek(0)

            # 7. Reenviar la imagen modificada
            await context.bot.send_photo(
                chat_id=GRUPO_ID,
                photo=output_buffer,
                caption=caption,
                message_thread_id=TOPIC_ID
            )

            # 8. Enviar el mensaje decorativo
            await context.bot.send_message(
                chat_id=GRUPO_ID,
                text="━━━━━━━━━━━━━━━━━━━\n✅ Esta Información fue reenviada del Grupo VIP 👑",
                message_thread_id=TOPIC_ID
            )

            # 9. Enviar el sticker
            await context.bot.send_sticker(
                chat_id=GRUPO_ID,
                sticker=STICKER_FILE_ID,
                message_thread_id=TOPIC_ID
            )

            await update.message.reply_text("✅ Imagen modificada y enviada al tema correctamente.")

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("Por favor, envía una imagen como foto.")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, reenviar_imagen))
    print("✅ Bot activo. Envía una imagen para reenviarla + logo + mensaje + sticker.")
    app.run_polling()
