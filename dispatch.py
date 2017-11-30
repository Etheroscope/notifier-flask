import requests
import os


SEND_GRID_API_KEY = os.environ['SEND_GRID_API_KEY']
SEND_GRID_ENDPOINT_URL = 'https://api.sendgrid.com/v3/mail/send'


def get_graph_url(contract, variable):
    # TODO: url in etheroscope which links straight to the graph for the given
    # variable and contract
    return 'http://etheroscope.info'


def get_email_message(contract, variable):
    return '<html>The {} graph for the contract with the address, {}, is now ' \
           'ready ' \
           'to view <a href="{}">here</a>.</html>'.format(variable, contract,
                                                   get_graph_url(contract,
                                                                 variable))


def send_email(email_addresses, contract, variable):
    personalizations = [
        {
            'to': [
                {
                    'email': email_address
                }
                for email_address in email_addresses
            ]
        }
    ]
    from_obj = {
        'email': 'notifications@etheroscope.info',
        'name': 'Etheroscope'
    }

    subject = 'The Etheroscope graph you requested is ready'
    html_message = get_email_message(contract, variable)

    headers = {
        'Authorization': 'Bearer {}'.format(SEND_GRID_API_KEY),
        'Content-Type': 'application/json'
    }
    payload = {
        'personalizations': personalizations,
        'from': from_obj,
        'subject': subject,
        'content': [{
            'type': 'text/html',
            'value': html_message
        }]
    }
    return requests.post(url=SEND_GRID_ENDPOINT_URL, headers=headers,
                         json=payload)
