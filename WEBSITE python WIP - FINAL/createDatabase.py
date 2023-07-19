import sqlite3
connection = sqlite3.connect("parkSupp_DATABASE.db")
cursor = connection.cursor()

#command to create user_Table first
commandUserTable = """CREATE TABLE IF NOT EXISTS user_Table (
    user_id VARCHAR(99) PRIMARY KEY UNIQUE NOT NULL,
    user_firstName VARCHAR(99) NOT NULL,
    user_middleName VARCHAR(99) NOT NULL,
    user_LastName VARCHAR(99) NOT NULL,
    user_userName VARCHAR(99) NOT NULL,
    user_password VARCHAR(99) NOT NULL,
    user_type VARCHAR(99) NOT NULL,
    user_validID VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_registrationDate VARCHAR(99) NOT NULL
)"""


commandAdminTable = """ CREATE TABLE IF NOT EXISTS admin_Table(
    admin_id VARCHAR(99) PRIMARY KEY UNIQUE NOT NULL,
    admin_username VARCHAR(99) NOT NULL,
    admin_password VARCHAR(99) NOT NULL,
    user_firstName VARCHAR(99) NOT NULL,
    user_middleName VARCHAR(99) NOT NULL,
    user_LastName VARCHAR(99) NOT NULL
)"""

commandGuestCodes = """CREATE TABLE IF NOT EXISTS guestCodes_Table(
    guestCode_id VARCHAR(5) UNIQUE NOT NULL,
    guestCode_timeCreated VARCHAR(99) NOT NULL
)"""
#cursor.execute(commandGuestCodes)