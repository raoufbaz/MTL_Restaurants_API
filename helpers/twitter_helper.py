from requests_oauthlib import OAuth1Session

# Authenticate your credentials
consumer_key = '6DRCk9QtmLhG0ss6J9thMzvA7'
consumer_secret = 'QEY9NLxP23kRZOwuMJZ93Q379fZbzUQ5rH20Bqee0I7WCPeISh'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAH%2BGmwEAAAAA1eekzMPA5LPE8EZYZtbX8sXdbb8' \
               '%3DeAjkXYkPdbXiy75brORLG4PLdCMaAoFS37ww9SRwXzmkixCh2C'
access_token = '1649347748171325443-ZXauufGlMNm2gTs97oMPkqT0s2bR4c'
access_token_secret = 'qrONYyyybTIzAQahrMJxgzDhFk9n9NIY44DevDsBpk8Lh'
client_id = 'WnVXRk9PcmNsUkF4aWxuOHNsVV86MTpjaQ'
client_secret = '9whM-_TSInOA0QV2C0ZkN5xAjGxOIId2hr6zu7WBvvK1QQwMJJ'
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
access_token_url = "https://api.twitter.com/oauth/access_token"

# Get request token
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )


# Construire la requete
def send_tweet(liste):
    body = 'Au moins un nouveau constat a été enregistré ! les contrevenants sont : \n \n'
    for item in liste:
        body = body + 'établissement : ' + item["etablissement"] + ', \n'
        body = body + 'montant : ' + item["montant"] + '$, \n \n'
    payload = {"text": body}

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

