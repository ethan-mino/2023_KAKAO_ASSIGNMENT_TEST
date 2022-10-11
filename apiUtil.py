import requests

def api_request(base_url, type="GET",
                token = None, auth = None, content_type = None,
                params=None, data=None, json=None):
    # params 옵션을 사용하면 쿼리 스트링을 사전 형태로 넘길 수 있음
    # response = requests.get("", params = {"userId" : 1})
    if params is None : params = {}

    # data 옵션을 사용하면, Content-Type 요청 헤더는 application/x-www-form-urlencoded로 자동 설정
    # response = requests.post(data = {'name' : 'Test User'})
    if data is None : params = {}

    # json 옵션을 사용하면, Content-Type 요청 헤더는 application/json로 자동 설정
    # requests.post("https://jsonplaceholder.typicode.com/users", json={'name': 'Test User'})
    if json is None : json = {}

    headers = {}

    if auth is not None:
        headers["Authorization"] = auth

    if token is not None:
        headers["X-Auth-Token"] = token

    if content_type is not None:
        headers["Content-Type"] = content_type

    if type == "GET":
        response = requests.get(base_url, headers=headers, data=data, params=params)
    elif type == "POST":
        response = requests.post(base_url, headers=headers, data=data, json=json, params=params)
    elif type == 'PUT':
        response = requests.put(base_url, headers=headers, data=data, json=json, params=params)
    elif type == "DELETE":
        response = requests.delete(base_url, headers=headers, data=data, json=json, params=params)

    # response
    # response.content : 바이너리 원문
    # response.text : 인코딩 문자열
    # response.json() : dict 객체
    # response.headers : dict 객체
    # response.status_code : 상태 코드
    if response.status_code is not 200 :
        raise Exception("Request Error : " + response.text)
    else :
        return response.json()

# https://github.com/cpm0722/kakao-2022-round2/blob/master/solve.py