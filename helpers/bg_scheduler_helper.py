from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from helpers import database_helper, twitter_helper
import json
import requests
import csv

from helpers.email_helper import send_email

url = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208" \
      "-d8744dca8fc6/download/violations.csv"


# le cron est configuré pour s'executer tout les jours a minuit
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=synchronise_data, trigger="cron", day='*', hour='0', minute='23', second='0')
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


# orchestrateur
def synchronise_data():
    print("Lancement de la detection de changement")
    flag = detection_nouvelles_addition()
    if flag:
        # met a jour la base de donnee
        database_helper.synchronize_data()
        print("synchronisation effectué avec success")
    else:
        print("pas de nouvelles données")


# compare la liste de la bd avec la nouvelle liste. si il trouve au moins un nouvel element. il envoi la liste
# par email et sur twitter
def detection_nouvelles_addition():
    with requests.get(url, stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())
        csvreader = csv.reader(lines)
        headers = next(csvreader)
        data_list = [dict(zip(headers, row)) for row in csvreader]
        liste_api = json.dumps(data_list)
        liste_bd = database_helper.requete_select_json("select * from violations")
        # transforme les 2 listes en listes json
        new_items = compare_json_lists(json.loads(liste_api), json.loads(liste_bd))
        count = len(new_items)
        if count > 0:
            print(f"Il y'a {count} nouvelles contraventions")
            send_email(new_items)
            twitter_helper.send_tweet(new_items)
            return True
        else:
            return False


# compare l'ancienne et nouvelle liste a partir de leur cle primaire.
def compare_json_lists(liste_api, liste_bd):
    api_ids = {item["id_poursuite"] for item in liste_api}
    bd_ids = {str(item["id_poursuite"]) for item in liste_bd}
    new_ids = api_ids - bd_ids
    return [item for item in liste_api if item["id_poursuite"] in new_ids]
