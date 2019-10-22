import tomcat_bot
import threading
import time
import schedule


# def thread_function(bot):
    # time.sleep(30)
    # bot.send_message(chat_id=-322840871, text="Deu certo caralho!")


#  print("Thread %s: finishing", param)


if __name__ == '__main__':
    tomcat_bot = tomcat_bot.TomcatBot()
    tomcat_bot.start()
    schedule.every().minute.do(tomcat_bot.check_service)
    while True:
        schedule.run_pending()
        time.sleep(1)

