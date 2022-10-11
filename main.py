import rest_api
from rest_api import *
from heapq import heappush, heappop, heapify
from queue import PriorityQueue

# 호텔에 머무는 단체 손님들은 인원수만큼의 인접한 객실을 배정받기를 원합니다.
# 최대한 많은 손님이 방을 배정받을 수 있도록 예약을 관리
# 호텔의 객실 이용률을 목표치 이상으로 만들어야 합니다.
# 호텔의 객실 이용률이 목표치 이상이 되도록 예약을 관리하거나 객실을 배정하면서, 객실 수가 많은 예약은 최대한 거절하지 않아야 함

# * 호텔 제약 사항
# 한 층에 W개의 객실이 있는 H층 건물
# 객실 번호는 "ABBB" 혹은 "AABBB" 형태으로, 고유함
# A는 객실의 층, B는 객실의 위치에 따라 정해집니다.
# 번호가 서로 인접한 객실은 위치도 인접
# 모든 객실의 체크아웃 시각은 오전 11시, 체크인 시각은 오후 2시입니다. 즉, 어떤 객실에서 체크아웃이 발생한 날짜에 바로 체크인이 가능


# 예약 제한사항
# 체크인 날짜는 예약 요청이 들어온 날짜로부터 최소 1일 뒤, 최대 21일 뒤

# 예약 관리
# 각 예약 요청의 답변 기한까지 예약을 승낙할지 거절할지 정해 답변
# 예약 요청의 답변 기한 = min(예약 요청이 들어온 날짜 + 14 , 체크인 날짜 - 1)
# 기한까지 답변을 하지 않은 예약은 거절한 것으로 처리
# 도착한 손님이 예약한 객실 수만큼의 비어있는 객실을 배정해야 합니다. 이때 객실들은 같은 층에서 인접한 연속된 객실이어야 합니다.

def index_to_room_num(x, y, rooms) :
    n = len(rooms)
    m = len(rooms[0])

    floorNum = str(x + 1).zfill(2)
    roomNum = str(y + 1).zfill(3)

    return floorNum + roomNum

# 기존 예약과 새로운 예약이 겹치지 않는 지 확인하는 함수
def reservation_avail(origin, new) :
    origin_checkin, origin_checkout = origin
    new_checkin, new_checkout = new

    if new_checkout <= origin_checkin or origin_checkout <= new_checkin :
        return True
    else : return False

# x, y부터 amount개의 방에 예역을 진행
def reserve(x, y, amount, new, rooms) :
    for offset in range(amount) :
        rooms[x][y + offset].append(new)

# 체크아웃할 예약을 지움
def checkout(rooms, curDay) :
    for rowIdx, row in enumerate(rooms):
        for colIdx, col in enumerate(row):
            # 예약하려는 각 방의 기존 예약을 확인하여, 예약 가능한 지 확인
            for idx, origin in enumerate(rooms[rowIdx][colIdx]):
                origin_checkout = origin[1]
                if origin_checkout <= curDay :
                    rooms[rowIdx][colIdx].remove(origin)

def availRoomCnt(rooms, chekcin, checkout) :
    roomCnt = 0
    for rowIdx, row in enumerate(rooms):
        for colIdx, col in enumerate(row):
            stX = rowIdx
            stY = colIdx

            avail = True
            # 예약하려는 각 방의 기존 예약을 확인하여, 예약 가능한 지 확인
            for origin in rooms[stX][stY]:
                if not reservation_avail(origin, new):
                    avail = False
                    break
            if avail :
                roomCnt += 1

    return roomCnt

def worst_fit(rooms, room_cnt, new) :
    n = len(rooms)
    m = len(rooms[0])
    fit_list = []

    for rowIdx, row in enumerate(rooms) :
        for colIdx, col in enumerate(row) :
            stX = rowIdx
            stY = colIdx

            cnt = 0
            for offset in range(0, m - stY) :
                # 호텔의 방번호를 벗어나는 경우
                if stY + offset >= m :
                    break

                avail = True

                # 예약하려는 각 방의 기존 예약을 확인하여, 예약 가능한 지 확인
                for origin in rooms[stX][stY + offset] :
                    if not reservation_avail(origin, new) :
                        avail = False
                        break

                if not avail : break
                cnt+=1

            if cnt >= room_cnt :
                fit_list.append((cnt, stX, stY))

    heapify(fit_list)

    if len(fit_list) == 0 :
        print("NOT AVAIL")
        return [False, False]
    else :
        print("AVAIL")
        worst = fit_list[len(fit_list) - 1]
        return [worst[1], worst[2]]

def best_fit(rooms, room_cnt, new) :
    n = len(rooms)
    m = len(rooms[0])
    fit_list = []

    for rowIdx, row in enumerate(rooms) :
        for colIdx, col in enumerate(row) :
            stX = rowIdx
            stY = colIdx

            cnt = 0
            for offset in range(0, m - stY) :
                # 호텔의 방번호를 벗어나는 경우
                if stY + offset >= m :
                    break

                avail = True

                # 예약하려는 각 방의 기존 예약을 확인하여, 예약 가능한 지 확인
                for origin in rooms[stX][stY + offset] :
                    if not reservation_avail(origin, new) :
                        avail = False
                        break

                if not avail : break
                cnt+=1

            if cnt >= room_cnt :
                fit_list.append((cnt, stX, stY))

    heapify(fit_list)

    if len(fit_list) == 0 :
        print("NOT AVAIL")
        return [False, False]
    else :
        print("AVAIL")
        best = fit_list[0]
        return [best[1], best[2]]

def first_fit(rooms, room_cnt, new) :
    n = len(rooms)
    m = len(rooms[0])

    for rowIdx, row in enumerate(rooms) :
        for colIdx, col in enumerate(row) :
            stX = rowIdx
            stY = colIdx
            avail = True

            for offset in range(room_cnt) :
                # 호텔의 방번호를 벗어나는 경우
                if stY + offset >= m :
                    avail = False
                    break

                # 예약하려는 각 방의 기존 예약을 확인하여, 예약 가능한 지 확인
                for origin in rooms[stX][stY + offset] :
                    if not reservation_avail(origin, new) :
                        avail = False
                        break

            if avail :
                return [stX, stY]

    return [False, False]

# 시나리오 1, minRoomPercentage = 0, first_fit = 398
# 시나리오 1, minRoomPercentage = 0, best_fit = 406
# 시나리오 1, minRoomPercentage = 0, worst_fit = 29x.xx

# 시나리오 2, minRoomPercentage = 0, first_fit = 488.1
# 시나리오 2, minRoomPercentage = 2.5, first_fit = 465.xx


if __name__ == '__main__':
    problem = 1
    rest_api.auth_key = start_api(problem)["auth_key"]

    if problem == 1 :
        col_nums = 20
        row_nums = 3
        maxDay = 200
        minRoomPercentage = 10
        fit = 1
    else :
        col_nums = 200
        row_nums = 10
        maxDay = 1000
        minRoomPercentage = 2.5
        fit = 0

    minRoom = col_nums * (minRoomPercentage / 100)
    rooms = [[[] for col in range(col_nums)] for row in range(row_nums)]
    day = 1
    reservations = dict()
    pre_reservation = dict();

    while True :
        # 체크아웃할 예약을 지움
        checkout(rooms, day)

        if day > maxDay : break

        # 예약 요청 확인
        # 현재 날짜에 새로 들어온 예약 요청의 정보를 반환
        reservation_requests = new_request_api();
        print(reservation_requests)

        replies = []    # 예약에 대한 승낙, 거절 정보

        # 예약을 확인
        for reservation in reservation_requests :
            # 동적할당 알고리즘과 비슷
            # 각 예약을 확인하면서
            reservation_id = reservation["id"]
            amount = reservation["amount"]
            check_in_date = reservation["check_in_date"]
            check_out_date = reservation["check_out_date"]

            availRoom = availRoomCnt(rooms, check_in_date, check_out_date)

            # 최소 방 개수보다 방이 더 적은 경우
            # if availRoom < (col_nums * row_nums) / 6 and amount < minRoom:
            #     replies.append({"id": reservation["id"], "reply": "refused"})
            #     continue;

            new = (check_in_date, check_out_date)

            if fit == 0 :
                x, y = first_fit(rooms, amount, new)
            elif fit == 1 :
                x, y = best_fit(rooms, amount, new)
            else :
                x, y = worst_fit(rooms, amount, new)

            if x is not False:   # 예약할 수 있는 경우
                roomNum = index_to_room_num(x, y, rooms);

                print(reservation_id)
                print("first fit : ", [x, y])
                #print("roomNum : ", roomNum)

                reserve(x, y, amount, new, rooms)  # 실제 예약을 진행
                replies.append({"id" : reservation["id"], "reply" : "accepted"})

                if check_in_date not in reservations :
                    reservations[check_in_date] = []

                reservations[check_in_date].append(dict({"x" : x, "y" : y, "amount" : amount, "new" : new, "id": reservation["id"], "room_number": roomNum}))
            else :  # 예약할 수 없는 경우 예약 거절
                replies.append({"id": reservation["id"], "reply": "refused"})

        # 현재 날짜
        # 특정 예약 요청에 대한 승낙 / 거절을 답변
        reply_api(replies)["day"]
        #print("replies : ", replies)

        room_assign = []

        # 현재 날짜인 예약을 실제 방 배정 진행
        if day in reservations :
            for reservation in reservations[day] :
                room_assign.append({"id" : reservation["id"], "room_number" : reservation["room_number"]}) # 승낙한 예약에 대한 방 배정 정보

        print("room_assign", room_assign)

        simul_response = simulate_api(room_assign=room_assign)
        day = simul_response["day"]
        print(simul_response)
        print("\n")

    print(score_api())


"""
        for reservation in reservation_requests :
            reservation_id = reservation["id"]
            check_out_date = reservation["check_out_date"]

            deadline = min(day + 13, check_out_date - 1)
            if deadline not in pre_reservation :
                pre_reservation[deadline] = []
            pre_reservation[deadline].append(reservation)


        todayReservation = []
        if day in pre_reservation :
            todayReservation = pre_reservation[day]
"""