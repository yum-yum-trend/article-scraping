import os
import json
import time
import random

import requests
from kakao_map_api import get_place

files = []
tokens = [
    "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJuYXllb24iLCJleHAiOjE2NDA5NTQ5MTcsImlhdCI6MTY0MDY5NTcxN30.jsKdLp2RPJmAu3470_j9ywsaQ29Uue7wH17wgAx7pqd7JibXzN9n2RgCZgqhGvIjjTKc6-IwIcawCdVUeCn2NQ"
]


# 폴더 하위의 (JSON) 파일 이름들 가져오기
def find_files(dir_name):
    file_names = os.listdir(dir_name)
    for file_name in file_names:
        full_filename = os.path.join(dir_name, file_name)
        files.append(full_filename)


def get_data():
    file = files[0]
    # for file in files:

    with open(file, 'r') as f:
        article_data = json.load(f)  # json_data = dict

    for row_num in article_data:
        place_name = article_data[row_num]['location']
        location = get_place(place_name)
        time.sleep(1)

        text = article_data[row_num]['text']
        tag_names = []
        for tagStr in article_data[row_num]['tagNames']:
            tag_names = tag_names + tagStr.split(',')

        location_info = {}
        if location:
            location_info = {
                "roadAddressName": location["road_address_name"],
                "placeName": location["place_name"],
                "xCoordinate": location["x"],
                "yCoordinate": location["y"],
                "categoryName": location["category_name"]
            }

        image_req_header = {
            "Authorization": f"Bearer {tokens[random.randrange(0, len(tokens))]}"
        }

        image_ids = []
        image_urls = article_data[row_num]["imageFiles"]
        for url in image_urls:
            response = requests.get(url)
            file_name = url.split("/")[-1].split("?")[0]
            image_file = {'imageFile': (file_name, response.content, 'image/*')}

            image_object = requests.post('http://localhost:8080/article/image', files=image_file, headers=image_req_header)
            image = image_object.json()
            image_ids.append(image['id'])

            time.sleep(3)

            # tmp_image_files = [
            #     ('imageFiles', ('a.png', response.content, 'image/png')),
            #     ('imageFiles', ('a.png', response.content, 'image/png'))]
        print(f'image_ids={image_ids}')

        payload = {
            "text": text,
            "tagNames": tag_names,
            "location": json.dumps(location_info),
            "imageIds": image_ids
        }

        article_req_header = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {tokens[random.randrange(0, len(tokens))]}"
        }

        response = requests.post(
            'http://localhost:8080/articles', headers=article_req_header, data=json.dumps(payload))

        print(response)
        print(response.json())


find_files('json_data')
get_data()
