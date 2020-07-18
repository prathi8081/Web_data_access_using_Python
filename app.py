from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

'''
    http://127.0.0.1:5000/
'''
@app.route('/')
def api_index():
    
    result = {
        'city' : 'Chennai'
    }

    return result

'''
    http://127.0.0.1:5000/get/movie/data
    http://127.0.0.1:5000/get/movie/data?link=https://en.wikipedia.org/wiki/Frozen_II
'''
@app.route('/get/movie/data')
def api_get_movie_data():

    movie_link = request.values.get("link")
    # url = 'https://en.wikipedia.org/wiki/Frozen_II'
    response=requests.get(movie_link)
    soup=BeautifulSoup(response.text,'html.parser')
    m_name=soup.find("i").text
    table = soup.find("table")
    table_data_full = []
    for tr in table.find_all("tr"):
        table_data_full.append(tr.text.replace('\n', ' ').strip())

    # print(table_data_full)

    t_headers = []
    for th in table.find_all("th"):
        t_headers.append(th.text.replace('\n', ' ').strip())
    #t_headers = t_headers[1:]
    # print(t_headers)
    t_headers[0] = 'Movie Name'

    table_data = []
    for td in table.tbody.find_all("td"): # find all tr's from table's tbody
        table_data.append(td.text.replace('\n', ' ').strip())

    #data[t_headers] = table_data
    table_data = table_data[0:]
    
    #print(table_data)
    # table_data[0] = m_name
    # print(table_data)
    headers_length = len(t_headers)

    movie_dict = {}
    for index in range(0, headers_length):
    #     print(t_headers[index], end = "")
    #     print(":", end = "")
    #     print(table_data[index])

        movie_dict[t_headers[index]] = table_data[index]
    
    result = {
        'movie_link' : movie_link,
        'movie_name' : m_name,
        'release_date' : movie_dict['Release date'],
        'lead_actors' : movie_dict['Starring'],
        'music_director' : movie_dict['Music by'],
        'director' : movie_dict['Directed by']
    }

    return result

def main():
    pass

if __name__ == "__main__":
    app.run(debug=True)     
