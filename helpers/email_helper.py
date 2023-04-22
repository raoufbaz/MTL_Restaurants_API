import smtplib
from email.mime.text import MIMEText
import yaml

# Load YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Access email address
email = config['email']

# Set up email information
sender_email = 'raoufbaaziz01@gmail.com'
sender_password = 'rdofgxdageuzzuzi'
recipient_email = email
subject = 'Ajout de constats d\'infraction restaurants de Montréal'


def send_email(liste):
    body = 'Une ou plusieurs contraventions ont été enregistré ! \n \n'
    for item in liste:
        body = body + 'etablissement : ' + item["etablissement"] + ', \n'
        body = body + 'date : ' + item["date"][0:4] + '-' + item["date"][4:6] + '-' + item["date"][6:8] + ', \n'
        body = body + 'description : ' + item["description"] + ', \n '
        body = body + 'adresse : ' + item["adresse"] + ', \n '
        body = body + 'date_jugement : ' + item["date_jugement"][0:4] + '-' + \
               item["date_jugement"][4:6] + '-' + item["date_jugement"][6:8] + ', \n'
        body = body + 'montant : ' + item["montant"] + '$, \n '
        body = body + 'proprietaire : ' + item["proprietaire"] + ', \n '
        body = body + 'ville : ' + item["ville"] + ', \n '
        body = body + 'statut : ' + item["statut"] + ', \n '
        body = body + 'date_statut : ' + item["date_statut"][0:4] + '-' + item["date_statut"][4:6] + '-' + \
               item["date_statut"][6:8] + ', \n'
        body = body + 'categorie : ' + item["categorie"] + ', \n \n'
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
