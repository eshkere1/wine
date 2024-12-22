from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
from pprint import pprint


wines = pandas.read_excel('wine3.xlsx', na_values=['N/A', 'NA'], keep_default_na=False).to_dict('records')

dict_of_lists = collections.defaultdict(list)
for wine in wines:
    dict_of_lists[wine["Категория"]].append(wine)
pprint(dict_of_lists)


def get_year():
    now = datetime.datetime.now()
    current_year = now.year - 1920
    return current_year

def get_correct_word(current_year):
    if current_year == 100:
        return "лет"
    elif current_year == 101:
        return "год"
    elif current_year == 102:
        return "года"
    elif current_year == 11:
        return "лет"

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


rendered_page = template.render(
    year=get_year(),
    correct_word=get_correct_word(get_year()),
    all_drinks=dict_of_lists
)
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()




