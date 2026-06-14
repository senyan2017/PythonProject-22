from tkinter import *
import pymysql

from gui_helpers import run


def build(root):
    entry = Entry(root)
    entry.pack()

    def save():
        con = pymysql.connect(host="localhost", user="root", db="pythongui")
        mycursor = con.cursor()
        name = entry.get()
        mycursor.execute("INSERT INTO detail(name) VALUES ( %s)", (name))
        print("data inserted successfully")
        con.commit()
        con.close()
        print(name)

    Button(root, text="Message Box", command=save).pack()


if __name__ == "__main__":
    run(build, title="Save to database", geometry="300x200+300+200")
