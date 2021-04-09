# Importing necessary lib packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq



root = tk.Tk()
root.configure(bg="yellow")
root.title('Ronnie \'s Simple To-Do List')
root.geometry("400x250+500+300")

# Connecting to my database and table creation for tasks
conn = sq.connect('todo.db')
cur = conn.cursor()
cur.execute('create table if not exists tasks (title text)')

# my task container
task = []


# add task functionality
def add_task():
    word = entry.get()
    if len(word) == 0:
        messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        task.append(word)
        cur.execute('insert into tasks values (?)', (word,))
        list_update()
        entry.delete(0, 'end')


# updating the list
def list_update():
    clear_list()
    for i in task:
        task_box.insert('end', i)


# delete one task
def delete_one():
    try:
        val = task_box.get(task_box.curselection())
        if val in task:
            task.remove(val)
            list_update()
            cur.execute('delete from tasks where title = ?', (val,))
    except:
        messagebox.showinfo('Cannot Delete', 'No Task Item Selected')


# select all and delete
def delete_all():
    mb = messagebox.askyesno('Delete All', 'Are you sure?')
    if mb:
        while len(task) != 0:
            task.pop()
        cur.execute('delete from tasks')
        list_update()


# clearing list - sub function
def clear_list():
    task_box.delete(0, 'end')


# exit
def close():
    print(task)
    root.destroy()


# database data retrieval
def retrieve_db():
    while len(task) != 0:
        task.pop()
    for row in cur.execute('select title from tasks'):
        task.append(row[0])


# Buttons and labels


list_one = ttk.Label(root, text='To-Do List')
list_two = ttk.Label(root, text='Enter task title: ')
entry = ttk.Entry(root, width=21)
task_box = tk.Listbox(root, height=11, selectmode='SINGLE')
add_button = ttk.Button(root, text='Add task', width=20, command=add_task)
delete_button = ttk.Button(root, text='Delete', width=20, command=delete_one)
delete_all_button = ttk.Button(root, text='Delete all', width=20, command=delete_all)
exit_button = ttk.Button(root, text='Exit', width=20, command=close)


retrieve_db()
list_update()

# Place geometry in the window
list_two.place(x=50, y=50)
entry.place(x=50, y=80)
add_button.place(x=50, y=110)
delete_button.place(x=50, y=140)
delete_all_button.place(x=50, y=170)
exit_button.place(x=50, y=200)
list_one.place(x=50, y=10)
task_box.place(x=220, y=50)



# keep window running
root.mainloop()

# Closing and Commiting to the database
conn.commit()
cur.close()
