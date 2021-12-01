import os
import json
from urllib.request import urlopen

from PIL import Image
from io import BytesIO

import requests
from kakao_map_api import get_place

files = []
articles = []


# 폴더 하위의 (JSON) 파일 이름들 가져오기
def find_files(dir_name):
    file_names = os.listdir(dir_name)
    for file_name in file_names:
        full_filename = os.path.join(dir_name, file_name)
        files.append(full_filename)


def get_data():

    for file in files:

        cnt = 0;

        with open(file, 'r') as f:
            article_data = json.load(f)  # json_data = dict

        for row_num in article_data:
            cnt = cnt + 1
            place_name = article_data[row_num]['location']
            location = get_place(place_name)

            text = article_data[row_num]['text']
            tag_names = []
            for tagStr in article_data[row_num]['tagNames']:
                tag_names = tag_names + tagStr.split(',')

            location_info = {}
            if location:
                location_info = {
                    "roadAddressName": location["road_address_name"],
                    "placeName":  location["place_name"],
                    "xCoordinate":  location["x"],
                    "yCoordinate":  location["y"],
                    "categoryName":  location["category_name"]
                }

            image_files = {
                "imageFiles": []
            }

            # image_urls = article_data[row_num]["imageFiles"]
            # for image_url in image_urls:
            #     r = requests.get(image_url, stream=True)
            #     # response = requests.get(image_url)
            #     # image = Image.open(BytesIO(response.content))
            #     # image_files["imageFiles"].append(image)
            #     image_file = Image.open(requests.get(image_url, stream=True).raw)
            #     image_files.append(image_file)

            payload = {
                "text": text,
                "tagNames": tag_names,
                "location": json.dumps(location_info),

            }

            image_url = article_data[row_num]["imageFiles"][0]
            print(image_url)
            # r = requests.get(image_url, stream=True)
            # payload["imageFiles"] = Image.open(requests.get(image_url, stream=True).raw)
            # image_files["imageFiles"] = Image.open(requests.get(image_url, stream=True).raw)



            response = requests.get(image_url)
            print(response)
            image = BytesIO(response.content)
            image_files["imageFiles"].append(image)
            image_files["imageFiles"].append(image)
            print(image)

            tmp_image_files = [
                               ('imageFiles', ('a.png', response.content, 'image/png')),
                               ('imageFiles', ('a.png', response.content, 'image/png'))]

            print(payload)

            header = {
                # "Content-Type": "multipart/form-data;",
                # 'Content-Disposition': 'form-data',
                "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJOYXllb25Ld29uIiwiZXhwIjoxNjM4Mzc5NjY4LCJpYXQiOjE2MzgzNjE2Njh9.2cWiLjFltgMAO6knV72Sp6nL_x5TQz1xkLWbipKMB0fnckoKH0bzmbocvC7fvKE95o8kFPSpTLHHRCNgOmk16w"
            }

            # response = requests.post('http://localhost:8080/articles', files=multipart_form_data)
            # session = requests.Session()
            response = requests.post('http://localhost:8080/articles', headers=header, files=tmp_image_files, data=payload)

            print("########## response ##########")
            print(response)

            # print(article_data[row_num])
            # print(location_info)

            if cnt == 1: break

        if cnt == 1: break


find_files('json_data')
get_data()