import requests
import os
from config import config

SEND_GRID_API_KEY = os.environ['SEND_GRID_API_KEY']
SEND_GRID_ENDPOINT_URL = 'https://api.sendgrid.com/v3/mail/send'


def get_graph_url(contract):
    return '{}contracts/{}'.format(config['etheroscope_frontend_url'], contract)


def get_email_message_notify(contract, variable):
    return ('<html>'
            '<p><strong><center>Hey there!</center></strong></p>'
            '<p>The {} graph for the contract with the address, {}, '
            'is now ready to view <a href="{}">here</a>.</p>'
            '<p>Love, Etheroscope</p>'
            '</html>'
            '').format(variable, contract, get_graph_url(contract))


def get_email_message_confirmation(contract):
    return ('<html>'
            '<p><strong><center>Hey there!</center></strong></p>'
            '<p>Just to confirm, we\'ve received your subscription. We\'ll '
            'drop you an email when we finish crunching the data to show '
            'you the graph for the graph for the contract with the address, '
            '{}.</p>'
            '<p>Love, Etheroscope</p>'
            '</html>'
            '').format(contract)


def send_email_confirmation(email_address, contract):
    html_message = get_email_message_confirmation(contract)
    to_field = [{'email': email_address}]
    subject = 'Your email has been subscribed'
    return send_email(html_message, to_field, subject)


def send_email_notify(email_addresses, contract, variable):
    html_message = get_email_message_notify(contract, variable)
    to_field = [{'email': email_address}
                for email_address in email_addresses]
    subject = 'The Etheroscope graph you requested is ready'
    return send_email(html_message, to_field, subject)


def send_email(html_message, to_field, subject):
    personalizations = [
        {
            'to': to_field
        }
    ]
    from_obj = {
        'email': 'notifications@etheroscope.info',
        'name': 'Etheroscope'
    }
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
