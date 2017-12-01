import re
from flask import Flask
from flask import request
from pymongo import MongoClient
from dispatch import send_email

ERROR_400 = 400

app = Flask(__name__)
client = MongoClient()
db = client['notifier']


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/store', methods=['PUT'])
def store_notification_waiter():
    if 'contract' not in request.args.keys():
        return 'No contract address provided', ERROR_400

    if 'variable' not in request.args.keys():
        return 'No variable provided', ERROR_400

    contract = request.args.get('contract')
    if not (contract or re.match(r'0x[0-9ABCDEF]+', contract)):
        return 'Invalid contract address', ERROR_400

    variable = request.args.get('variable')
    email_address = (request.args.get('email_address')
                     if 'email_address' in request.args.keys()
                     else None)

    # Insert email into database
    email_obj = {
        'email_address': email_address,
        'contract': contract,
        'variable': variable
    }
    db_emails = db['emails']
    db_emails.insert_one(email_obj)

    return 'Success! Will notify the user when the data is ready '


@app.route('/notify', methods=['POST'])
def notify_waiter():
    data = request.get_json()
    if 'contract' not in data:
        return 'No contract address provided', ERROR_400

    if 'variable' not in data:
        return 'No variable provided', ERROR_400

    contract = data['contract']
    variable = data['variable']

    # Get and remove emails stored in database which are awaiting the data for
    # the variable for this contract
    email_addresses = [email_obj['email_address']
                       for email_obj
                       in db['emails'].find(
            {'contract': contract, 'variable': variable})]
    db['emails'].delete_many({'contract': contract, 'variable': variable})

    send_email(email_addresses, contract, variable)

    return 'Success! The user has been notified'

if __name__ == '__main__':
    app.run()
