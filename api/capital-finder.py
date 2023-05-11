from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        url_components = parse.urlsplit(s)
        query_string_list = parse.parse_qsl(url_components.query)
        dic = dict(query_string_list)
        capital_city = ""
        country_name = ""

        if "name" in dic:
            url = "https://restcountries.com/v3.1/name/"
            country_req = requests.get(url + dic["name"])
            country_data = country_req.json()
            capital_city = country_data[0]["capital"][0]
        if "capital" in dic:
            url = "https://restcounrtires.com/v3.1/capital/"
            capital_req = requests.get(url + dic["capital"])
            capital_data = capital_req.json()
            country_name = capital_data[0]["name"]["common"][0]

        if capital_city and not country_name:
            message = f"The capital of {dic['name']} is {capital_city}."
        elif country_name and not capital_city:
            message = f"{dic['capital']} is the capital of {country_name}."

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(message.encode())

        return
