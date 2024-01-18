from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class Crypto:
  def get_top_25(self):
      url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
      parameters = {
        'start':'1',
        'limit':'25',
        'convert':'USD'
      }
      headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'a2725ecf-abca-416b-86e2-89df6b69522b',
      }

      session = Session()
      session.headers.update(headers)

      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      return data['data']