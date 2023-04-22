import datetime
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, json, jsonify, Response
from helpers import database_helper, bg_scheduler_helper, twitter_helper

app = Flask(__name__)

# lance le background scheduler
bg_scheduler_helper.start_scheduler()


def validateur_date(date_debut, date_fin):
    # date format
    date_format = '%Y-%m-%d'
    try:
        date_object_debut = datetime.datetime.strptime(date_debut, date_format)
        date_object_fin = datetime.datetime.strptime(date_fin, date_format)

    # si il y'a erreur
    except ValueError:
        return False
    if date_object_debut > date_object_fin:
        return False
    else:
        return True


@app.route('/')
def get_data():
    return render_template('index.html'), 200


# recheche principal par nom,proprietaire,adresse
@app.route('/recherche', methods=["GET"])
def recherche():
    string = request.args.get('search')
    liste = database_helper.select_constats(string)
    liste = json.loads(liste)
    return render_template('resultats.html', constats=liste), 200


# recherche par 2 dates
@app.route('/api/contrevenants', methods=["GET"])
def date_recherche():
    start_date = request.args.get('du')
    end_date = request.args.get('au')
    if not start_date or not end_date:
        return jsonify({"error": "Donnée manquante, 2 parametres dates sont attendu"}), 400
    if not validateur_date(start_date, end_date):
        return jsonify({"error": "la date de debut est plus grande que la date de fin"}), 403
    data = database_helper.select_avec_dates(start_date, end_date)
    if not data or data == "null":
        return jsonify({"error": "Aucune donnee ne correspond a vos criteres de recherche"}), 400
    return jsonify(data), 200


# auto completion avec les noms d'etablissements
@app.route('/autocomplete', methods=["POST"])
def auto_complete():
    if request.method == 'POST':
        keyword = request.form['keyword']
        if not keyword:
            return jsonify({"error": "Donnée manquante, un parametres string est attendu"}), 400
        data = database_helper.select_auto_complete(keyword)
        if not data or data == "null":
            return jsonify({"error": "Aucune donnee ne correspond a vos criteres de recherche"}), 400
        return jsonify(data), 200


@app.route('/api/etablissement', methods=["POST"])
def nav_recherche():
    if request.method == 'POST':
        nom = request.form['nom']
        if not nom or nom == "null":
            return jsonify({"error": "Donnée invalide, un parametres string est attendu"}), 400
        data = database_helper.select_nav_search(nom)
        if not data or data == "null":
            return jsonify({"error": "Aucune donnee ne correspond a vos criteres de recherche"}), 400
        return jsonify(data), 200


@app.route('/api/top_contrevenants', methods=["GET", "POST"])
def top_contrevenants():
    data = database_helper.select_top_contrevenants()
    if not data or data == "null":
        return jsonify({"error": "la requete n'a pas retournée de donnée."}), 500
    return jsonify(data), 200


@app.route('/api/top_contrevenants_xml', methods=["GET", "POST"])
def top_contrevenants_xml():
    data = database_helper.select_top_contrevenants()
    if not data or data == "null":
        return jsonify({"error": "la requete n'a pas retournée de donnée."}), 500

    root = ET.Element('top_etablissements')
    data = json.loads(data)
    for row in data:
        etablissement = ET.SubElement(root, 'etablissement')
        nom = ET.SubElement(etablissement, 'nom')
        nom.text = row['etablissement']
        nombre_infractions = ET.SubElement(etablissement, 'nombre_infractions')
        nombre_infractions.text = str(row['nbr'])
    xml_string = ET.tostring(root, encoding='UTF-8')

    return Response(xml_string, mimetype='text/xml',
                    headers={'Content-Disposition': 'attachment;filename=top_etablissements.xml'})


@app.route('/doc')
def doc():
    return render_template('doc.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
