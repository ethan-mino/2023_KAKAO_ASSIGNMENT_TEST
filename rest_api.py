from apiUtil import api_request

BASE_URL = "https://68ecj67379.execute-api.ap-northeast-2.amazonaws.com/api"
auth_key = None
x_auth_token = "5dcefca295572a3d03b373d2c53cec10"

# 문제를 풀기 위한 key를 발급
def start_api(problem):
    return api_request(BASE_URL + "/start",
                       type="POST",
                       token=x_auth_token,
                       json={'problem': problem})

# 현재 날짜에 새로 들어온 예약 요청의 정보를 반환
def new_request_api() :
    return api_request(BASE_URL + "/new_requests",
                       type="GET",
                       auth=auth_key)["reservations_info"]

# 특정 예약 요청에 대한 승낙 / 거절을 답변
def reply_api(replies) :
    return api_request(BASE_URL + "/reply",
                       type="PUT",
                       auth=auth_key,
                       json={"replies" : replies})

def simulate_api(room_assign) :
    return api_request(BASE_URL + "/simulate",
                       type="PUT",
                       auth=auth_key,
                       json={"room_assign" : room_assign})



def score_api() :
    return api_request(BASE_URL + "/score",
                       type="GET",
                       auth=auth_key)