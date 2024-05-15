import re
import logging

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError

def filter_datum(fields, redaction, message, separator):
    return re.sub(r'({})'.format('|'.join(map(re.escape, fields))), redaction, message).split(separator)

class LogFilter:
    def __init__(self, fields):
        self.fields = fields

    def format(self, message, separator):
        redaction = 'REDACTED'
        filtered_fields = filter_datum(self.fields, redaction, message, separator)
        return separator.join(filtered_fields)


def filter_datum(fields, redaction, message, separator):
    return re.sub(r'({})'.format('|'.join(map(re.escape, fields))), redaction, message).split(separator)