from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine, asc
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import calendar


engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def menu():
    print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')

def make_choice(user_choice, today):
    if user_choice == "1":
        print(today_task(today))
    if user_choice == "2":
        check_tasks(today)
    if user_choice == "3":
        all_task()
    if user_choice == '4':
        check_missed()
    if user_choice == "5":
        print('Enter task: ')
        new_task = input()
        print('Enter deadline: ')
        deadline = input()
        add_new_task(new_task, deadline)
    if user_choice == '6':
        rows = session.query(Table).order_by(Table.deadline).all()
        print(delete_task(rows))
    if user_choice == "0":
        end()

def today_task(today):
    today_date = f"Today {today.day} {today.strftime('%b')}" # today date and short month
    rows = session.query(Table).filter(Table.deadline == today).all() # check all rows with base Today
    print(today_date)
    if not rows:
        return 'Nothing to do!'
    else:
        return rows

def check_tasks(today):
    for day in range(0, 7): # for loop in each day
        next_day = today + timedelta(days=day)
        rows = session.query(Table).filter(Table.deadline == next_day.strftime('%Y-%m-%d')).all()
        print(f"{calendar.day_name[next_day.weekday()]} {next_day.day} {next_day.strftime('%b')}")
        print(rows)
        print()

def add_new_task(new_task, dl):
    new_row = Table(task=f'{new_task}',
                    deadline=datetime.strptime(f'{dl}', '%Y-%m-%d').date())
    session.add(new_row) # commited
    session.commit()

def all_task():
    rows = session.query(Table).order_by(asc(Table.deadline)).all() # by alphabet
    if len(rows) <= 0:
        print("Nothing to do!")
    else:
        print("All tasks:")
        count = 1
        for i in range(len(rows)):
            print(f'{count}. {rows[i].task}. {rows[i].deadline.strftime("%d %b")}')
            count += 1
    print()

def end():
    print()
    print('Bye!')
    exit()

def delete_task(rows):
    if not rows:
        return 'Nothing to delete'
    else:
        print('Chose the number of the task you want to delete:')
        for i in range(len(rows)):
            print(f'{i + 1}. {rows[i].task}. {rows[i].deadline.strftime("%d %b")}')
    task_number = int(input())
    specific_row = rows[task_number - 1] # in case rows is not empty
    session.delete(specific_row)
    session.commit()
    return 'The task has been deleted!'

def check_missed():
    print()
    print('Missed tasks:')
    missed = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    if not missed:
        print('''Missed tasks:
Nothing is missed!''')
    else:
        for i in range(len(missed)):
            print(f'{i + 1}. {missed[i]}. {missed[i].deadline.strftime("%d %b")}')
    print()
today = datetime.today()

# main loop
if __name__ == '__main__':
    while True:
        menu()
        user_choice = input()
        make_choice(user_choice, today)
