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
    cur.execute("CREATE TABLE IF NOT EXISTS country (id INTEGER PRIMARY KEY, country_id INTEGER, name TEXT)")
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

def add_holiday(cur, conn):
    pass




def main():
    #SET UP
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
    woah = cur.fetchall()
    create_holiday_table(cur, conn)

    # most_holidays = dict()



    for item in woah:
        json_name = item[0] + ".json"

        response_country = requests.get('https://date.nager.at/api/v3/PublicHolidays/2024/' + str(item[0]), verify=False)
        data2 = json.loads(response_country.text)
        with open(json_name, "w") as write_file:
            json.dump(data2, write_file, indent=4)
        
        f = open(json_name)
        data = json.load(f)
        # most_holidays[item[0]] = most_holidays.get(item[0], 0) + len(data)
        for holiday in data:
            date = str(holiday["date"])
            local_name = str(holiday["localName"])
            name = str(holiday["name"])

            cur.execute("INSERT OR IGNORE INTO holiday (id, country_id, date, local_name, name) VALUES (?,?,?,?,?)", (holiday_count, item[0], date, local_name, name))
            holiday_count += 1
            conn.commit()
    print("most holidays")
    # visualize(cur, conn)
    visualize_pi(cur, conn)

    # christmas_len = len(christmas(cur,conn))
    # independance_day_len  = len(independance_day(cur, conn))
    # stephen_len = len(stephen_day(cur, conn))
    # may_len = len(may_day(cur, conn))
    # patrick_len = len(patrick_day(cur, conn))


def visualize(cur, conn):

    data = dict()
    data["Christmas Day"] = len(christmas(cur, conn))
    data["Independance Day"] = len(independance_day(cur, conn))
    data["Saint Stephens Day"] = len(stephen_day(cur, conn))
    data["Saint Patricks Day"] = len(patrick_day(cur, conn))
    data["May Day"] = len(may_day(cur, conn))
    names = list(data.keys())
    vals = list(data.values())
    fig = plt.figure(figsize = (10,5))
    plt.bar(names,vals,color = 'maroon', width=0.4)
    plt.xlabel("Holiday")
    plt.ylabel("Number of occurances across all countries")
    plt.title("Holiday count")
    plt.show()
    
        
def christmas(cur, conn):
        
    cur.execute(
        """
            SELECT country.name
            FROM country
            JOIN holiday
            ON holiday.country_id = country.country_id
            WHERE holiday.name = 'Christmas Day'
        """
    )
    res = cur.fetchall()
    conn.commit()
    return res

def independance_day(cur, conn):
    cur.execute(
        """
            SELECT country.name
            FROM country
            JOIN holiday
            ON holiday.country_id = country.country_id
            WHERE holiday.name = 'Independence Day'
        """
    )
    res2 = cur.fetchall()
    conn.commit()
    return res2

def may_day(cur, conn):
    cur.execute(
        """
            SELECT country.name
            FROM country
            JOIN holiday
            ON holiday.country_id = country.country_id
            WHERE holiday.name = 'May Day'
        """
    )
    res3 = cur.fetchall()
    conn.commit()
    return res3

def stephen_day(cur, conn):
    cur.execute(
        """
            SELECT country.name
            FROM country
            JOIN holiday
            ON holiday.country_id = country.country_id
            WHERE holiday.name = 'Constitution Day'
        """
    )
    res3 = cur.fetchall()
    conn.commit()
    return res3

def patrick_day(cur, conn):
    cur.execute(
        """
            SELECT country.name
            FROM country
            JOIN holiday
            ON holiday.country_id = country.country_id
            WHERE holiday.name = 'Easter Sunday'
        """
    )
    res3 = cur.fetchall()
    conn.commit()
    return res3

def first_half_us(cur,conn):
    cur.execute(
        """
            SELECT holiday.name
            FROM holiday
            JOIN country
            ON holiday.country_id = country.country_id
            WHERE holiday.date <'2024-07-02' AND country.name = 'United States'
        """
    )
    res = cur.fetchall()
    conn.commit()
    return res

def second_half_us(cur,conn):
    cur.execute(
        """
            SELECT holiday.name
            FROM holiday
            JOIN country
            ON holiday.country_id = country.country_id
            WHERE holiday.date > '2024-07-02' AND country.name = 'United States'
        """
    )
    res = cur.fetchall()
    conn.commit()
    return res


def first_half_canada(cur,conn):
    cur.execute(
        """
            SELECT holiday.name
            FROM holiday
            JOIN country
            ON holiday.country_id = country.country_id
            WHERE holiday.date <'2024-07-02' AND country.name = 'Canada'
        """
    )
    res = cur.fetchall()
    conn.commit()
    return res

def second_half_canada(cur,conn):
    cur.execute(
        """
            SELECT holiday.name
            FROM holiday
            JOIN country
            ON holiday.country_id = country.country_id
            WHERE holiday.date > '2024-07-02' AND country.name = 'Canada'
        """
    )
    res = cur.fetchall()
    conn.commit()
    return res

def visualize_pi(cur, conn):

    us1 = len(first_half_us(cur,conn))
    us2 = len(second_half_us(cur,conn))
    canada1 = len(first_half_canada(cur,conn))
    canada2 = len(second_half_canada(cur,conn))

    y = [us1, us2]
    x = ["First half of the year", "Second half of the year"]
    plt.pie(y, labels = x)
    

    y2 = [canada1, canada2]
    x2 = ["First half of the year", "Second half of the year"]

    plt.pie(y2, labels = x2)
    
    plt.show()


if __name__ == "__main__":
    main()