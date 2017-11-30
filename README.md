# Etheroscope Notifier

A simple Flask microservice which sends email notifications to users
who have subscribed to a variable of a particular contract.

MongoDB is used to store email addresses and subscriptions.

## API

### POST */store*
To store a new subscriber's email address.

**Request body** *(application/x-www-form-urlencoded)*

| Argument | Value | Example | Required? |
| -------- | ----- | ------- | --------- |
| `email_address` | email address of the subscriber | `will_is_kool@etheroscope.info` | **Yes** |
| `contract` | contract address | `0x123ABC456DEF` | **Yes** |
| `variable` | contract variable | `total` | **Yes** |

### POST */notify*
To send an email notification to all subscribers to a given variable.

**Request body** *(application/x-www-form-urlencoded)*

| Argument | Value | Example | Required? |
| -------- | ----- | ------- | --------- |
| `contract` | contract address | `0x123ABC456DEF` | **Yes** |
| `variable` | contract variable | `total` | **Yes** |

## TODO
- [] Implement `get_graph_url()` method in `dispatch.py`
