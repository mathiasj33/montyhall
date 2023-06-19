import sqlite3
import time
import random

con = sqlite3.connect('instance/montyhall.db')
cur = con.cursor()

# for i in range(1000):
#     switched = random.random() > 0.5
#     won = random.random() > (0.33 if switched else 0.66)
#     cur.execute('INSERT INTO played_game(switched, won) VALUES (?, ?)', (int(switched), int(won)))
#     con.commit()
    # print(won)
    # time.sleep(1.3)

for i in range(100):
    num = random.randint(1, 6)
    cur.execute('INSERT INTO random_number(number, guessed) VALUES (?, ?)', (int(num), 0))
    con.commit()

con.close()
