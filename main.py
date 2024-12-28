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
    if 2 <= current_year %10 <= 4:
        if current_year//10 %10 == 1:
            return "лет"
        else:
            return "года"
    elif 5 <= current_year %10 <= 10:
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




