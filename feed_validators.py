import datetime
import logging
import params


def extract_timestamp(data):
    index = data.find("timestamp:")
    value = data[index + 11:index + 21]
    return datetime.datetime.fromtimestamp(int(value))


def extract_data_qty(data):
    return data.count('entity')


def quick_report(data):
    return "Última atualização {0} \n Número de entidades {1}".format(extract_timestamp(data), extract_data_qty(data))


def service_hanged(data):
    feed_date = extract_timestamp(data)
    valid_date = datetime.datetime.now() + datetime.timedelta(minutes=-params.VALID_PERIOD)
    logging.info("Feed date {0} -- Reference date {1} ".format(feed_date, valid_date))
    return feed_date < valid_date


def service_empty(data):
    return extract_data_qty(data) <= 0