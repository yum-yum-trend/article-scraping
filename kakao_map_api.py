import requests
from secret import KEY

MAX_PAGE_NUM = 3

def search_place(place_name):
    places = []

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    for page_num in range(1, MAX_PAGE_NUM+1):
        params = {'query': place_name, 'page': page_num}
        headers = {"Authorization": f"KakaoAK {KEY['KAKAO_REST_API']}"}

        result = requests.get(url, params=params, headers=headers).json()['documents']
        print('##### PLACES #####')
        print_arr(result)

        places += result
        print(len(places))

    print_arr(places)

    # 제공받을 수 있는 장소들의 최대 개수
    total = requests.get(url, params=params, headers=headers).json()['meta']['total_count']
    print('##### TOTAL #####')
    print(total)

    if total > 45:
        print(total, '개 중 45개 데이터밖에 가져오지 못했습니다!')
    else:
        print('모든 데이터를 가져왔습니다!')

    return places


# return location
def get_place(places, road_address_name):
    for place in places:
        if place['road_address_name'] == road_address_name:
            return place


def print_arr(arr):
    for element in arr:
        print(element)


# 스크래핑 결과에서 가져와야할 변수
# place_name, road_address_name

places = search_place("소바")
place = get_place(places, "road_address_name")


# TODO
# 스크래핑 결과로 얻은 '장소 이름' 으로 search_place() 호출
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
