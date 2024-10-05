import mysql.connector
from datetime import datetime
from gutenbergpy.textget import get_text_by_id

# MySQL ühendus orbital-bookstore andmebaasiga
db = mysql.connector.connect(
    host="localhost",
    user="root",     # asenda oma kasutajanimega
    password="Juunior12",  # asenda oma parooliga
    database="orbital-bookstore"
)

cursor = db.cursor()

# Funktsioon raamatute salvestamiseks andmebaasi
def save_book_to_db(book_id, title, author):
    # Laadi raamat Project Gutenbergist alla
    content = get_text_by_id(book_id).decode('utf-8')

    # Salvesta raamat MySQL andmebaasi
    sql = "INSERT INTO books (title, author, content, download_date) VALUES (%s, %s, %s, %s)"
    val = (title, author, content, datetime.now().date())
    cursor.execute(sql, val)
    db.commit()

    print(f"Book '{title}' by {author} is added to the database!")

# Näiteks lisame mõned raamatud
save_book_to_db(1342, "Pride and Prejudice", "Jane Austen")  # Pride and Prejudice ID
save_book_to_db(11, "Alice's Adventures in Wonderland", "Lewis Carroll")  # Alice in Wonderland ID

cursor.close()
db.close()
