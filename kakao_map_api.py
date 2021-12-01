import requests
from secret import KEY


def get_place(place_name):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    params = {'query': place_name, 'page': 1}
    headers = {"Authorization": f"KakaoAK {KEY['KAKAO_REST_API']}"}

    places = requests.get(url, params=params, headers=headers).json()['documents']
    # print_arr(places)

    if not places:
        result = {}
    else:
        result = places[0]

    return result


def print_arr(arr):
    for element in arr:
        print(element)


# 스크래핑 결과에서 가져와야할 변수
# place_name, road_address_name

get_place("이레상회")


# TODO
# 스크래핑 결과로 얻은 '장소 이름' 로 search_place() 호출
# search_place() > places 결과 dict list 에서 스크래핑 결과로 얻은 '주소' 와 일치하는 장소 찾기 [스크래핑 주소 <-> places 들의 road_address_name] 비교


# 프론트에서 보내듯이 'FormData' 형식으로 데이터들을 담아서 보내기
# gLocationInfo
# gLocationInfo = {
#         "roadAddressName": locationInfoArray[0],
#         "placeName": locationInfoArray[1],
#         "xCoordinate": locationInfoArray[2],
#         "yCoordinate": locationInfoArray[3],
#         "categoryName": locationInfoArray[4]
#     }

# FormData
# let formData = new FormData();
# let locationJsonString = JSON.stringify(gLocationInfo)
# formData.append("text", $('#article-textarea').val());
# formData.append("location", locationJsonString);
# formData.append("tagNames", tagNames);
#
# Object.keys(imageFileDict).forEach(function(key)
# {
#     formData.append("imageFiles", imageFileDict[key]);
# });

# TODO
# User 를 어떻게 다르게 할 것 인지..?
