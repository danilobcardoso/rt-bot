# coding: latin-1

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram
import os
import shutil
import logging
import params
import requests
import datetime
import feed_validators as feed

logging.basicConfig(level=logging.INFO)

class TomcatBot:

    STATUS_MESSAGE = 'status'
    CHECK_MEMORY_MESSAGE = 'Verificar memória'
    CHECK_DISK_SPACE_MESSAGE = 'Verificar espaço em disco'
    RESTART_TOMCAT_MESSAGE = 'Reiniciar tomcat'
    CHECK_LAST_LOG_ENTRIES_MESSAGE = ' Verificar últimas mensagens no log'

    def __init__(self):
        logging.info("Iniciando conexão com o BOT")
        self.updater = Updater(token=params.BOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        echo_handler = MessageHandler(Filters.all, self.process_message)
        self.dispatcher.add_handler(echo_handler)

    def bot(self):
        return self.dispatcher.bot

    def start(self):
        logging.info("Iniciando monitoramento das mensagens")
        self.updater.start_polling()

    def send_options_massage(self, update, context):
        custom_keyboard = [[self.RESTART_TOMCAT_MESSAGE, self.CHECK_LAST_LOG_ENTRIES_MESSAGE],
                           [self.CHECK_DISK_SPACE_MESSAGE, self.CHECK_MEMORY_MESSAGE]]

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="O que desejas Oh Grande Mestre?",
                                 reply_markup=reply_markup)

    def restart_tomcat(self, update, context):
        reply_markup = telegram.ReplyKeyboardRemove()
        os.system(params.RESTART_TOMCAT_COMMAND)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Comando enviado",
                                     reply_markup=reply_markup)

    def last_log_lines(self, update, context):
        reply_markup = telegram.ReplyKeyboardRemove()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Isso ainda não sou capaz de fazer",
                                 reply_markup=reply_markup)

    def check_disk_space(self, update, context):
        reply_markup = telegram.ReplyKeyboardRemove()
        total, used, free = shutil.disk_usage("/")
        logging.debug(" <--- " + ("Total: %d GB" % (total // (2 ** 30))))
        logging.debug(" <--- " + ("Used: %d GB" % (used // (2 ** 30))))
        logging.debug(" <--- " + ("Free: %d GB" % (free // (2 ** 30))))

        return_string = ''
        return_string += ("Total: %d GB" % (total // (2 ** 30)))
        return_string += ("\nUsed: %d GB" % (used // (2 ** 30)))
        return_string += ("\nFree: %d GB" % (free // (2 ** 30)))
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=return_string,
                                 reply_markup=reply_markup)

    def check_memory(self, update, context):
        reply_markup = telegram.ReplyKeyboardRemove()
        return_string = ''
        with open('/proc/meminfo') as file:
            for line in file:
                logging.debug(" <--- " + line)
                return_string += line + '\n'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=return_string,
                                 reply_markup=reply_markup)

    def check_status(self, update, context):
        reply_markup = telegram.ReplyKeyboardRemove()
        URL = params.SERVICE_URL
        r = requests.get(url=URL)
        data = r.text
        if params.IS_FEED:
            report = feed.quick_report(data)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=report,
                                     reply_markup=reply_markup)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Eu estou vivo!",
                                     reply_markup=reply_markup)

    def is_reply_message(self, update, context):
        if update.message.reply_to_message is not None:
            if update.message.reply_to_message.from_user.username == context.bot.username:
                return True
        return False

    def process_reply_message(self, update, context):
        text_message = update.message.text
        if self.RESTART_TOMCAT_MESSAGE in text_message:
            logging.info("Comando REINICAR TOMCAT")
            self.restart_tomcat(update, context)

        if self.CHECK_LAST_LOG_ENTRIES_MESSAGE in text_message:
            logging.info("Comando ULTIMAS LINHAS DO LOG")
            self.last_log_lines(update, context)

        if self.CHECK_DISK_SPACE_MESSAGE in text_message:
            logging.info("Comando Espaço em Disco")
            self.check_disk_space(update, context)

        if self.CHECK_MEMORY_MESSAGE in text_message:
            logging.info("Comando verificar memória")
            self.check_memory(update, context)

    def is_directed_message(self, update, context):
        if update.message.bot.name in update.message.text:
            return True
        return False

    def process_broadcast_message(self, update, context):
        if self.STATUS_MESSAGE in update.message.text.lower():
            logging.info("Comando verificar status")
            self.check_status(update, context)

    def process_message(self, update, context):
        logging.debug("Mensagem recebida: " + update.message.text)

        if self.is_reply_message(update, context):
            self.process_reply_message(update, context)
        elif self.is_directed_message(update, context):
            self.send_options_massage(update, context)
        else:
            self.process_broadcast_message(update, context)


    def check_service(self):
        URL = params.SERVICE_URL
        r = requests.get(url=URL)
        data = r.text
        if self.service_hanged(data):
            self.dispatcher.bot.send_message(chat_id=-322840871, text="Atenção... serviço congelado!")
        if self.service_empty(data):
            self.dispatcher.bot.send_message(chat_id=-322840871, text="Atenção... serviço vazio!")

    def service_hanged(self, data):
        if params.IS_FEED:
            return feed.service_hanged(data)
        return False

    def service_empty(self, data):
        if params.IS_FEED:
            return feed.service_empty(data)
        return False

