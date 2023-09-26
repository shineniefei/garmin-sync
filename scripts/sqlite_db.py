#!/usr/bin/env python3
# coding:utf-8

import sqlite3
import traceback
import os
from config import DB_DIR


class SqliteDB(object):

    def __init__(self,
                 database='sqlitedb',
                 isolation_level='',
                 ignore_exc=False):
        self.database = database
        self.isolation_level = isolation_level
        self.ignore_exc = ignore_exc
        self.connection = None
        self.cursor = None

        if not os.path.exists(DB_DIR):
            os.mkdir(DB_DIR)

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(
                database=os.path.join(DB_DIR, self.database),
                isolation_level=self.isolation_level)
            self.cursor = self.connection.cursor()
            return self.cursor
        except Exception as ex:
            traceback.print_exc()
            raise ex

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.connection.rollback()
                return self.ignore_exc
            else:
                self.connection.commit()
        except Exception as ex:
            traceback.print_exc()
            raise ex
        finally:
            self.cursor.close()
            self.connection.close()
