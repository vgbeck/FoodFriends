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

def visualize(cur, conn):

    data = dict()
    # colors = []
    # bar(color = colors)
    data["Christmas Day"] = len(christmas(cur, conn))
    data["Independance Day"] = len(independance_day(cur, conn))
    data["Saint Stephens Day"] = len(stephen_day(cur, conn))
    data["Saint Patricks Day"] = len(patrick_day(cur, conn))
    data["May Day"] = len(may_day(cur, conn))
    names = list(data.keys())
    vals = list(data.values())
    plt.bar(names,vals)
    plt.xlabel("Holiday")
    plt.ylabel("Number of occurances across all countries")
    plt.title("Holiday count")
   
    plt.show()


def visualize_pi(cur, conn):

    us1 = len(first_half_us(cur,conn))
    us2 = len(second_half_us(cur,conn))
    canada1 = len(first_half_canada(cur,conn))
    canada2 = len(second_half_canada(cur,conn))

    # fig, axs = plt.pie(1, 2)

    y = [us1, us2]
    x = ["First half of the year", "Second half of the year"]
    plt.pie(y, labels = x)
    plt.show()
    

    y2 = [canada1, canada2]
    x2 = ["First half of the year", "Second half of the year"]

    plt.pie(y2, labels = x2)
    plt.title("# of Holidays in each Half of the Year")
    
    plt.show()

def main():
    cur, conn = setUpDatabase("country.db")
    visualize(cur, conn)
    visualize_pi(cur, conn)


if __name__ == "__main__":
    main()