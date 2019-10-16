# coding: latin-1

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram
import os
import shutil
import logging
import params

logging.basicConfig(level=logging.INFO)

class TomcatBot:

    def __init__(self):
        logging.info("Iniciando conexão com o BOT")
        self.updater = Updater(token=params.BOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        echo_handler = MessageHandler(Filters.all, self.process_message)
        self.dispatcher.add_handler(echo_handler)

    def start(self):
        logging.info("Iniciando monitoramento das mensagens")
        self.updater.start_polling()

    def send_options_massage(self, update, context):
        custom_keyboard = [['Reiniciar Tomcat', 'Ultimas linhas do log'],
                           ['Verificar espaço disco', 'Verificar memoria']]

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
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Eu estou vivo!",
                                 reply_markup=reply_markup)

    def process_message(self, update, context):
        text_message = update.message.text
        logging.debug("Mensagem recebida: " + text_message)
        if update.message.bot.name in text_message:
            self.send_options_massage(update, context)

        if 'Reiniciar Tomcat' in text_message:
            logging.info("Comando REINICAR TOMCAT")
            self.restart_tomcat(update, context)

        if 'Ultimas linhas do log' in text_message:
            logging.info("Comando ULTIMAS LINHAS DO LOG")
            self.last_log_lines(update, context)

        if 'Verificar espaço disco' in text_message:
            logging.info("Comando Espaço em Disco")
            self.check_disk_space(update, context)

        if 'Verificar memória' in text_message:
            logging.info("Comando verificar memória")
            self.check_memory(update, context)

        if 'Status' in text_message:
            logging.info("Comando verificar status")
            self.check_status(update, context)





