from django.conf import settings
import requests

# iamport 에서 토큰을 얻어옴
def get_token():
    access_data = {
        'imp_key': settings.IAMPORT_KEY,
        'imp_secret': settings.IAMPORT_SECRET
    }

    url = "https://api.iamport.kr/users/getToken"
    # requests : 특정 서버와 http통신을 하게 해주는 모듈. 토큰 가져와라
    req = requests.post(url,data=access_data) #url에 접속해서 토큰 가져와. access_Data도 이용
    access_res = req.json() #api는 json 형식을 이용해 해석하겠다

    if access_res['code'] is 0:
        return access_res['response']['access_token'] #우리가 필요한 토큰 값
    else:
        return None #제대로 응답 못할 시

# 결제할 준비를 하는 함수 - iamport 에 주문번호와 금액을 미리 전송. 어떤 order_id로 amount만큼 결제할건지 알려줌
def payments_prepare(order_id,amount,*args,**kwargs):
    access_token = get_token() #토큰 받아옴
    if access_token:
        access_data = {
            'merchant_uid':order_id, #우리가 설정한 order_id. 아임포트에 전달해서 유니크한 걸로 보냄
            'amount':amount
        }

        url = "https://api.iamport.kr/payments/prepare"
        headers = {
            'Authorization':access_token
        }
        #데이터는 access_data
        req = requests.post(url, data=access_data, headers=headers)
        res = req.json()

        if res['code'] != 0:
            raise ValueError("API 통신 오류")
    else: #액세스 토큰 관련 esle.
        raise ValueError("토큰 오류")


# 결제가 이루어졌음을 확인해주는 함수 - 실 결제 정보를 iamport에서 가져옴. 우리가 요청한 금액으로 결제됐는지?
def find_transaction(order_id,*args,**kwargs):
    access_token = get_token()
    if access_token:
        url = "https://api.iamport.kr/payments/find/"+order_id

        headers = {
            'Authorization':access_token
        }

        req = requests.post(url, headers=headers)
        res = req.json()

        if res['code'] is 0:
            context = {
                'imp_id':res['response']['imp_uid'],
                'merchant_order_id':res['response']['merchant_uid'],
                'amount':res['response']['amount'],
                'status':res['response']['status'],
                'type':res['response']['pay_method'],
                'receipt_url':res['response']['receipt_url']
            }
            return context
        else:
            return None
    else:
        raise ValueError("토큰 오류")