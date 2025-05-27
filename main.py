from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import remove_members as rm
import add_members as am
import polygon as pg
from creds import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"👋 Welcome! 👋 \nI'm {BOT_NAME}, your friendly assistant. 🤖 \n\n" \
        f"I'm here to assist you with managing your subscriptions at {SERVICE_NAME}. 👀 \n\n" \
        f"For more details about subscriptions, type /info \n\n" \
        f"To subscribe or learn more about your current plan, type /service \n\n"

    await update.message.reply_text(text)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"\n\nTo subscribe to {SERVICE_NAME}, send 💸 30 USDT 💸 to {OUR_WALLET} to receive a 🗓 30-day subscription.\n\n" \
        "Each additional USDT adds an extra day.\n\n" \
        "You can check the remaining days using /service again once you've subscribed. Ensure you send the funds from the wallet you've linked using this command!"

    await update.message.reply_text(text)


async def service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("addresses.json", mode="r") as addresses_raw:
        ads = json.load(addresses_raw)

    user = str(update.message.from_user.id)
    if user not in ads:
        text = f"It looks like you haven't subscribed to {SERVICE_NAME} with this account yet.\n" \
            "To get started, please provide your email address and USDT public key using the following command:\n\n" \
            "/addinfo your_email your_usdt_public_key"
    
    else:
        email, wallet, days_remaining, _ = ads[user]
        if days_remaining <= 3:
            emoji = "🟥"
        elif days_remaining <= 13:
            emoji = "🟨"
        else:
            emoji = "🟩"

        text = f"Your registered USDT wallet is: {wallet}\n" \
            f"Your registered email is: {email}\n\n" \
            f"Remaining days: {emoji} {days_remaining}\n\n" \
            f"To update your email and public key, use the following command:\n/addinfo your_email your_usdt_public_key"

    await update.message.reply_text(text)


async def addinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    user = str(update.message.from_user.id)

    if not len(args) == 2:
        text = "Incorrect format. Please write the email first, followed by a space, and then your wallet's public key."
        await update.message.reply_text(text)
        return

    wallet = args[1].lower()
    email = args[0]

    with open("addresses.json", mode="r") as addresses_raw:
        ads = json.load(addresses_raw)

    for k, v in ads.items():
        if v[1] == wallet:
            text = "This wallet already exists!"
            await update.message.reply_text(text)
            return

    additional_text = ""
    if user not in ads:
        ads[user] = [email, wallet, 0, pg.check_total_balances(wallet)]
        additional_text = f"\n\nTo subscribe to {SERVICE_NAME}, send 💸 30 USDT 💸 to {OUR_WALLET} to receive a 🗓 30-day subscription.\n\n" \
                        "Each additional USDT adds an extra day.\n\n" \
                        "You can check the remaining days using /service again once you've subscribed. Ensure you send the funds from the wallet you've linked using this command!"

    else:
        rm.main(ads[user][0])
        ads[user][0] = email
        ads[user][1] = wallet

        if ads[user][2] > 0:
            am.main(email)
    
    with open("addresses.json", mode="w") as addresses_raw:
        json.dump(ads, addresses_raw)
    
    text = f"Your email address has been successfully updated to '{email}'. Your wallet address has also been updated to '{wallet}' {additional_text}"
    await update.message.reply_text(text)


# Errorhandling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} has caused an error: {context.error}")

def main():
    # Create application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("service", service))
    application.add_handler(CommandHandler("addinfo", addinfo))

    # protocoll errors
    application.add_error_handler(error)

    # Bot start
    application.run_polling()

if __name__ == '__main__':
    main()
