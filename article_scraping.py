from bs4 import BeautifulSoup
import json
from collections import OrderedDict

divs = ['busan', 'chungang', 'daegu', 'dongjak', 'goyang', 'gwangju', 'incheon', 'seoul']

for div in divs:
    with open(f'scraping_raw_data/{div}.html', 'r', encoding='utf-8') as taget :
        html_string = taget.read()

    soup = BeautifulSoup(html_string, "html.parser").select(".pSc_C")

    data_set = OrderedDict()
    locations = OrderedDict()

    for i in range(len(soup)):
        data = OrderedDict()

        data["text"] = soup[i].select("._205XE > span")[0].text + " by " + soup[i].select(".AzIBM")[0].text
        locations[i] = data["location"] = soup[i].select("._2tr2m")[0].text
        data["tagNames"] = [soup[i].select("._2yVb9")[0].text, soup[i].select("._2yVb9")[1].text.split(' ')[-1]]
        data["imageFiles"] = [url['style'].split('("')[1].split('")')[0] for url in soup[i].select("._3iz62")]
        data["위치(동)"] = soup[i].select("._2yVb9")[1].text

        data_set[i] = data


    with open(f'json_data/{div}.json', 'w', encoding="utf-8") as make_file:
        json.dump(data_set, make_file, ensure_ascii=False, indent="\t")
    
    with open(f'location_json_data/{div}.json', 'w', encoding="utf-8") as make_file:
        json.dump(locations, make_file, ensure_ascii=False, indent="\t")