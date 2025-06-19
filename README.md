# Data-Cleaning-bot
# 🧼 Telegram CSV Cleaner Bot

This is a Telegram bot that automatically cleans CSV files sent by users. It performs common data cleaning operations such as:

- Removing duplicate rows
- Filling missing values (with mean/mode)
- Cleaning column headers
- Dropping irrelevant columns
- Generating a summary report of the cleaned data

## 🚀 Features

- ✅ Accepts `.csv` files sent by users
- 🧹 Cleans headers (strips spaces, lowers case, removes unwanted characters)
- 🗑️ Drops duplicates and unnecessary columns (e.g., `unnamed: 0`)
- 🧠 Fills missing values:
  - Mean for numeric columns
  - Mode (most common) for categorical columns
- 📄 Generates a summary text report
- 📦 Sends back both the cleaned CSV and the summary report

## 📦 Requirements

Make sure you have Python 3.8+ installed. Install the required dependencies:

```bash
pip install python-telegram-bot pandas
