import pandas as pd  # type: ignore
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from telegram.error import TimedOut

BOT_TOKEN = 'TOKEN'  # Replace with your actual bot token 
COLUMNS_TO_DROP = ['unnamed: 0']

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Send me a CSV file and I’ll clean it for you.\n"
        "I will remove duplicates, fill missing values, clean headers, and send you a summary report."
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Just send a .csv file. I’ll:\n"
        "- Clean headers\n"
        "- Drop duplicates\n"
        "- Fill missing values (mean/mode)\n"
        "- Drop irrelevant columns\n"
        "- Send back cleaned data and a summary"
    )

# Handle CSV
async def handle_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document.file_name.endswith('.csv'):
        await update.message.reply_text("❌ Please send a valid .csv file.")
        return

    try:
        file = await document.get_file()
        file_path = "uploaded.csv"
        await file.download_to_drive(file_path)

        df = pd.read_csv(file_path)
        original_shape = df.shape

        # Clean headers
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "")

        # Drop specified columns
        df.drop(columns=[col for col in COLUMNS_TO_DROP if col in df.columns], inplace=True, errors='ignore')

        # Drop duplicates
        df.drop_duplicates(inplace=True)

        # Fill missing values
        for col in df.columns:
            if df[col].dtype == 'object':
                mode_val = df[col].mode()
                df[col].fillna(mode_val[0] if not mode_val.empty else "Unknown", inplace=True)
            else:
                df[col].fillna(df[col].mean(), inplace=True)

        # Drop fully empty rows
        df.dropna(how='all', inplace=True)
        cleaned_shape = df.shape

        # Save cleaned file
        cleaned_file_path = "cleaned_data.csv"
        df.to_csv(cleaned_file_path, index=False)

        # Summary report
        report_path = "cleaning_summary.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("🧼 Data Cleaning Summary\n\n")
            f.write(f"Original Shape: {original_shape}\n")
            f.write(f"Cleaned Shape: {cleaned_shape}\n\n")
            f.write("Null values (after cleaning):\n")
            f.write(str(df.isnull().sum()))
            f.write("\n\nData Types:\n")
            f.write(str(df.dtypes))
            f.write("\n")

        await update.message.reply_text("✅ Cleaning complete! Here's your cleaned file and summary report.")
        await update.message.reply_document(document=open(cleaned_file_path, "rb"))
        await update.message.reply_document(document=open(report_path, "rb"))

    except TimedOut:
        await update.message.reply_text("⚠️ Timeout while downloading the file. Please try again.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ An error occurred: {str(e)}")


# ✅ MAIN ENTRY (sync-style with async inside)
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_csv))

    print("🤖 Bot is running...")
    # No asyncio.run() — let `run_polling()` manage the event loop itself
    app.run_polling()
