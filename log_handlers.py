import datetime
from logging import Handler
from traceback import print_exc
import db
from upload_data import write_log_to_db


class DBHandler(Handler):
    def __init__(self, level=0):
        super().__init__(level)

    def emit(self, record):
        try:
            message = self.format(record)
            try:
                new_log = db.Log(module=record.module,
                                 message=message,
                                 datetime=datetime.datetime.now())
                write_log_to_db(new_log)
            except:
                print_exc()
        except:
            print_exc()
