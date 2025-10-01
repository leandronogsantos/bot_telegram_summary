import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from io import BytesIO
import PyPDF2
from auth import get_auth
from inference import predict

limit_characters = 5000
default_message = f"👋 Send me a PDF file and I'll generate a summary for you! Limited by {limit_characters} characters"
client, tl_token = get_auth()
system_prompt = "You are a helpful assistant that summarizes PDF documents."
user_prompt = "Please provide a concise summary of the following text:\n"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(default_message)


async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if document.mime_type != "application/pdf":
        await update.message.reply_text("⚠️ Please send a PDF file.")
        return

    # Download file into memory
    file = await context.bot.get_file(document.file_id)
    file_bytes = BytesIO()
    await file.download_to_memory(out=file_bytes)

    # Reset pointer
    file_bytes.seek(0)

    # Extract text from PDF
    reader = PyPDF2.PdfReader(file_bytes)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    # Use your model to summarize
    prompt = text[:limit_characters]  # limit text length to avoid overload
    await update.message.reply_text(f"📄 Received: {document.file_name}\nGenerating summary...")

    # Dummy call (replace with your predict function)
    summary = predict(client, system_prompt, user_prompt + prompt)
    formatted_summary = "📌 **Resumo do PDF:**\n\n" + summary.strip()
    await update.message.reply_text(formatted_summary, parse_mode="Markdown")

async def handle_non_pdfs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ I only work with PDF files. Please send me a PDF.")


def main():
    app = Application.builder().token(tl_token).build()

    app.add_handler(CommandHandler("start", start))
    # Only PDF documents
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))

    app.add_handler(MessageHandler(~filters.Document.ALL, handle_non_pdfs))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
