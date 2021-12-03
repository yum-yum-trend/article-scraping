import os
import json
import time

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

        with open(file, 'r') as f:
            article_data = json.load(f)  # json_data = dict

        for row_num in article_data:
            cnt = cnt + 1
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
                    "placeName":  location["place_name"],
                    "xCoordinate":  location["x"],
                    "yCoordinate":  location["y"],
                    "categoryName":  location["category_name"]
                }

            image_files = []
            image_urls = article_data[row_num]["imageFiles"]
            for url in image_urls:
                response = requests.get(url)
                file_name = url.split("/")[-1].split("?")[0]
                print(file_name)
                image_files.append(('imageFiles', (file_name, response.content, 'image/*')))
                time.sleep(1)

                # tmp_image_files = [
                #     ('imageFiles', ('a.png', response.content, 'image/png')),
                #     ('imageFiles', ('a.png', response.content, 'image/png'))]

            payload = {
                "text": text,
                "tagNames": tag_names,
                "location": json.dumps(location_info),
            }

            header = {
                "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJOYXllb25Ld29uIiwiZXhwIjoxNjM4Mzk3ODY1LCJpYXQiOjE2MzgzNzk4NjV9.-v_PMcRXc1iaUHESHFnOLGgfOS3wws991HrKhwIYCST81HbKFKqtKqQMm4rvx4W0RZAjeXhvFdid5rdABgsl9Q"
            }

            response = requests.post('http://localhost:8080/articles', headers=header, files=image_files, data=payload)

            time.sleep(3)


find_files('json_data')
get_data()
