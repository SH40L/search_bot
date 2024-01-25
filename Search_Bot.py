from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6765569169:AAHprwR9umVHnzA8W15xMSjoF_BhomQZoQw'
updater = Updater(token=bot_token, use_context=True)

# Replace 'YOUR_CHANNEL_ID' with the actual channel ID (should start with '@')
channel_id = '@-1002028988180'

# Replace 'YOUR_GROUP_CHAT_ID' with the actual group chat ID
group_chat_id = '-1001999784815'

def search_and_forward(update: Update, context: CallbackContext) -> None:
    # Get the text message from the user
    search_text = update.message.text.lower()

    # Check if the user provided a post number
    if search_text.isdigit():
        post_number = int(search_text)
        # Fetch the post from the channel based on the post number
        messages = context.bot.get_chat_history(chat_id=channel_id, limit=post_number + 1)
        if messages:
            post_to_forward = messages[-1]
            # Forward the post to the group
            context.bot.forward_message(chat_id=group_chat_id, from_chat_id=channel_id, message_id=post_to_forward.message_id)
        else:
            update.message.reply_text("Post not found.")
    else:
        # Search for messages in the channel containing the search text
        messages = context.bot.get_chat_history(chat_id=channel_id, limit=100)
        matching_messages = [message for message in messages if search_text in message.text.lower()]

        if matching_messages:
            # Forward the first matching post to the group
            context.bot.forward_message(chat_id=group_chat_id, from_chat_id=channel_id, message_id=matching_messages[0].message_id)
        else:
            update.message.reply_text("No matching posts found.")

# Handle messages in the group
updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.group, search_and_forward))

# Start the bot
updater.start_polling()
updater.idle()
