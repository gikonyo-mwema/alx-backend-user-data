#!/usr/bin/env python3
"""
Module for handling PII
"""
from typing import List
import re
import logging
from os import environ
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns a log message obfuscated """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using filter_dataum """
        record.msg = filter_datum(self.fields, self.REDUCTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ = '__main__':
    main()
