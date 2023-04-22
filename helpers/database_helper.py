import csv
import sqlite3
import json
import requests

url = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208" \
      "-d8744dca8fc6/download/violations.csv"


# insert les donnees en changeant le type pour date
def insertion_donnees(liste):
    for r in liste:
        r[2] = r[2][0:4] + "-" + r[2][4:6] + "-" + r[2][6:8]
        r[5] = r[5][0:4] + "-" + r[5][4:6] + "-" + r[5][6:8]
        r[11] = r[11][0:4] + "-" + r[11][4:6] + "-" + r[11][6:8]
    try:
        sqlite_insert_query = """INSERT INTO violations
                          (id_poursuite, business_id, date, description, adresse, date_jugement, etablissement, montant,
                          proprietaire, ville, status, date_status, categorie) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        sqlite_connection = sqlite3.connect('database.db')
        cursor = sqlite_connection.cursor()
        cursor.executemany(sqlite_insert_query, liste)
        sqlite_connection.commit()
        print("Total", cursor.rowcount, "Insertion reussi  dans la table violations ")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert multiple records into sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# télécharge les données en CSV et les convertit en list avant de les envoyer à insertion
def telecharge_donnee_de_api():
    with requests.get(url, stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())
        csvreader = csv.reader(lines)
        next(csvreader)
        data_list = list(csvreader)
        insertion_donnees(data_list)


def requete_select(requete):
    liste = "null"
    connection = sqlite3.connect('database.db')
    try:
        cursor = connection.cursor()
        liste = list(cursor.execute(requete))

    except sqlite3.Error as error:
        print("Failed to select records.", error)
    finally:
        if connection:
            connection.close()
    return liste


def requete_select_json(requete):
    liste = "null"
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    try:
        cursor = connection.cursor()
        liste = list(cursor.execute(requete))

    except sqlite3.Error as error:
        print("Failed to select records.", error)
    finally:
        if connection:
            connection.close()
    liste = json.dumps([dict(ix) for ix in liste])
    return liste


def select_constats(string):
    liste = requete_select_json(f"""select * from violations where etablissement LIKE '%{string}%' OR 
                                    proprietaire LIKE '%{string}%' OR adresse LIKE '%{string}%'""")
    return liste


def synchronize_data():
    connection = sqlite3.connect('database.db')
    connection.cursor().execute("DROP TABLE IF EXISTS violations;")
    connection.cursor().execute("CREATE TABLE violations(id_poursuite integer primary key, business_id integer,"
                                "date date,description varchar(300),adresse varchar(60),date_jugement date,"
                                "etablissement varchar(200),montant integer,proprietaire  varchar(200),ville varchar("
                                "100),status varchar(100),date_status date,categorie varchar(50));")
    connection.close()
    telecharge_donnee_de_api()


def select_avec_dates(start_date, end_date):
    data = requete_select_json(
        f"""select * from violations where DATE(date) BETWEEN DATE('{start_date}') AND DATE('{end_date}') """
        f"""ORDER BY date ASC""")
    return data


def select_auto_complete(auto_complete):
    data = requete_select_json(
        f"""select etablissement from violations where etablissement LIKE '%{auto_complete}%' """
        f"""GROUP BY date LIMIT 0,5 """)
    return data


def select_nav_search(word):
    data = requete_select_json(f"""select * from violations where etablissement LIKE '%{word}%' order by etablissement
    """)
    return data


def select_top_contrevenants():
    data = requete_select_json(
        f"""select etablissement,count(*) as nbr from violations group by etablissement ORDER BY"""
        """ nbr DESC """)
    return data
