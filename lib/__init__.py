# lib/__init__.py
import sqlite3

CONN = sqlite3.connect('lube_lab_express.db')
CURSOR = CONN.cursor()
