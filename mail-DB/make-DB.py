import sqlite3

# .dbを作成
conn = sqlite3.connect("mail.db")

# sql実行のためのcursorオブジェクト生成
c = conn.cursor()

print("Database opened successfully")

c.execute("""CREATE TABLE data (name TEXT, email TEXT)""")

print("table created successfully")

# コネクションを閉じる
conn.close()