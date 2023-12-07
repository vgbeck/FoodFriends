import requests
import json
import os
import sqlite3
import ssl
import pprint
import matplotlib.pyplot as plt


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_country_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS country (id INTEGER PRIMARY KEY, country_id TEXT, name TEXT)")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    conn.commit()

def add_country(filename, cur, conn):
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    data = json.loads(file_data)
    
    try:
        cur.execute(
            """
                SELECT id 
                FROM country
                WHERE id = (SELECT MAX(id) FROM country)
            """
        )
        start = cur.fetchone()
        start = start[0]
    except:
        start = 0

    temp = start

    for item in data[start:start+25]:
        id = temp
        temp += 1
        country_id = item["countryCode"]
        name = item["name"]
        cur.execute("INSERT OR IGNORE INTO country (id, country_id, name) VALUES (?,?,?)", (id, country_id, name, ))
        conn.commit()

def create_holiday_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS holiday (id INTEGER PRIMARY KEY, country_id INTEGER, date TEXT, local_name TEXT, name TEXT)")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn.commit()





def main():
    cur, conn = setUpDatabase('country.db')
    create_country_table(cur, conn)
    response_API = requests.get('https://date.nager.at/api/v3/AvailableCountries', verify = False)
    data = json.loads(response_API.text)
    with open("country.json", "w") as write_file:
        json.dump(data, write_file, indent=4)

    add_country("country.json", cur, conn)
    add_country("country.json", cur, conn)
    add_country("country.json", cur, conn)
    add_country("country.json", cur, conn)
    add_country("country.json", cur, conn)

    holiday_count = 1
    country_id = cur.execute("SELECT country_id FROM country")
    fetching = cur.fetchall()
    create_holiday_table(cur, conn)

#QUESTION ON THIS seperate 25
    for item in fetching:
        json_name = item[0] + ".json"
        
        # if(item[0] == "AD"):
        #     print("HERE")

        #use a call from item[0] to the country table to decide
        cur.execute(
        f"""
            SELECT id
            FROM country
            WHERE country_id = (?)

        """, (item[0],)
        )
        res = cur.fetchone()
 


        response_country = requests.get('https://date.nager.at/api/v3/PublicHolidays/2024/' + str(item[0]), verify=False)
        data2 = json.loads(response_country.text)
        with open(json_name, "w") as write_file:
            json.dump(data2, write_file, indent=4)
        
        f = open(json_name)
        data = json.load(f)
        for holiday in data:
            date = str(holiday["date"])
            local_name = str(holiday["localName"])
            name = str(holiday["name"])

            cur.execute("INSERT OR IGNORE INTO holiday (id, country_id, date, local_name, name) VALUES (?,?,?,?,?)", (holiday_count, res[0], date, local_name, name))
            holiday_count += 1
            conn.commit()

    
        
# def christmas(cur, conn):
        
#     cur.execute(
#         """
#             SELECT country.name
#             FROM country
#             JOIN holiday
#             ON holiday.country_id = country.country_id
#             WHERE holiday.name = 'Christmas Day'
#         """
#     )
#     res = cur.fetchall()
#     conn.commit()
#     return res

# def independance_day(cur, conn):
#     cur.execute(
#         """
#             SELECT country.name
#             FROM country
#             JOIN holiday
#             ON holiday.country_id = country.country_id
#             WHERE holiday.name = 'Independence Day'
#         """
#     )
#     res2 = cur.fetchall()
#     conn.commit()
#     return res2

# def may_day(cur, conn):
#     cur.execute(
#         """
#             SELECT country.name
#             FROM country
#             JOIN holiday
#             ON holiday.country_id = country.country_id
#             WHERE holiday.name = 'May Day'
#         """
#     )
#     res3 = cur.fetchall()
#     conn.commit()
#     return res3

# def stephen_day(cur, conn):
#     cur.execute(
#         """
#             SELECT country.name
#             FROM country
#             JOIN holiday
#             ON holiday.country_id = country.country_id
#             WHERE holiday.name = 'Constitution Day'
#         """
#     )
#     res3 = cur.fetchall()
#     conn.commit()
#     return res3

# def patrick_day(cur, conn):
#     cur.execute(
#         """
#             SELECT country.name
#             FROM country
#             JOIN holiday
#             ON holiday.country_id = country.country_id
#             WHERE holiday.name = 'Easter Sunday'
#         """
#     )
#     res3 = cur.fetchall()
#     conn.commit()
#     return res3

# def first_half_us(cur,conn):
#     cur.execute(
#         """
#             SELECT holiday.name
#             FROM holiday
#             JOIN country
#             ON holiday.country_id = country.country_id
#             WHERE holiday.date <'2024-07-02' AND country.name = 'United States'
#         """
#     )
#     res = cur.fetchall()
#     conn.commit()
#     return res

# def second_half_us(cur,conn):
#     cur.execute(
#         """
#             SELECT holiday.name
#             FROM holiday
#             JOIN country
#             ON holiday.country_id = country.country_id
#             WHERE holiday.date > '2024-07-02' AND country.name = 'United States'
#         """
#     )
#     res = cur.fetchall()
#     conn.commit()
#     return res


# def first_half_canada(cur,conn):
#     cur.execute(
#         """
#             SELECT holiday.name
#             FROM holiday
#             JOIN country
#             ON holiday.country_id = country.country_id
#             WHERE holiday.date <'2024-07-02' AND country.name = 'Canada'
#         """
#     )
#     res = cur.fetchall()
#     conn.commit()
#     return res

# def second_half_canada(cur,conn):
#     cur.execute(
#         """
#             SELECT holiday.name
#             FROM holiday
#             JOIN country
#             ON holiday.country_id = country.country_id
#             WHERE holiday.date > '2024-07-02' AND country.name = 'Canada'
#         """
#     )
#     res = cur.fetchall()
#     conn.commit()
#     return res


if __name__ == "__main__":
    main()