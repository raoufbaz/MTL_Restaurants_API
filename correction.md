
<pre>
CODE PERMANENT : BAAR11059705
NOM            : Raouf Baaziz
COURRIEL       : raoufbaaziz@outlook.com
</pre>
___________________________________________

Guide de correction - INF5190-20 H23
========================================
## A1
* La base de donnée utilisé pour les test se trouve dans le repertoire principal.
* les scripts de créations de la bd se trouvent dans ./database
* pour tester le telechargement de données de l'API et insertion, 
faire appel à la fonction ci-dessous à partir de la route principal.

Ca devrait print: "Total 6575 Insertion reussi  dans la table violations" 
```py
@app.route('/')
def get_data():
    database_helper.telecharge_donnee_de_api()
    return render_template('index.html'), 200

```
## A2
* Tester la recherche principal (milieu de la page). On est redirigé vers la page "resultats.html". Il faut cliquer sur un element du tableau afin de dévoiler la description de chacuns des constats.

```py
#la route qui gere cette requete
@app.route('/recherche', methods=["GET"])
```
## A3

* Pour tester le Background scheduler, il suffit de changer les valeurs du cron pour l'heure, minute et seconde souhaité
* A noter qu'il faut specifier la seconde aussi pour ne pas qu'il s'execute plusieurs fois. Il faut aussi s'assurer que 
flask ne roule pas en mode Debuggage (FLASK_DEBUG). Sinon le script se lance 2 fois.
* Pour simuler une synchro, il suffit de supprimer un/des elements de la base de donnée. Car celle-ci se met a jour seulement lorsqu'elle
est desynchronisé.
```py
#la fonction synchronise_data() se charge de la synchronisation
@app.route('/')
def get_data():
    bg_scheduler_helper.synchronise_data()
    return render_template('index.html'), 200
```
* Il est aussi possible de tester à ce niveau l'envoi de email en modifiant le fichier config.yaml
 et de valider l'envoi du tweet sur. https://twitter.com/raoufBaz

## A4

* validation de la date mise en place et message d'erreurs specifique.
```py
#la route qui gere cette requete
@app.route('/contrevenants', methods=["GET"])
```
## A5
* le formulaire de recherche par date est dans la page d'accueil. La requete est fait par un script Ajax qui se trouve dans /static/ajax.js.
* La requete est la meme que celle utilisée dans A4. le nombre de constats par etablissement est calculé avec JS
```py
#la route qui gere cette requete
@app.route('/contrevenants', methods=["GET"])
```
## A6
* le formulaire de recherche par nom est dans le search bar en haut a droite. La requete vers cette route est faite par
ajax. lorsqu'on clique sur une suggestion et clique sur la recherche. Un modal s'ouvre avec l'historique du contrevenant
```py
@app.route('/autocomplete', methods=["POST"])
@app.route('/nav_recherche', methods=["POST"])
```
## B1
* la fonction ci dessous telecharge la liste des donnees et la compare a la liste de la bd. Si elle trouve une difference
, une synchronisation doit etre faite. Les nouvelles données sont d'abord envoyé par courriel avant la synchro.

```py
bg_scheduler_helper.`detection_nouvelles_addition()
email_helper.send_email()`
```
## B2
Quand des nouvelles données sont détéctés. elles sont envoyer en tweet avant la synchro.
```py
twitter_helper.send_tweet()
```
## C1
Le service est documenté sur /doc
```py
@app.route('/api/top_contrevenants', methods=["GET", "POST"])
```
## C2
Le service est documenté sur /doc
```py
@app.route('/api/top_contrevenants_xml', methods=["GET", "POST"])
```
## F1
Mon application roule sur le serveur pythonanywhere
```py
raoufbaaziz.pythonanywhere.com
```