from ronglian_sms_sdk import SmsSDK

accId = '8aaf0708790d65aa01791b66be910632'
accToken = '88fbf6bf797a4c49b16bec60f35a410c'
appId = '8aaf0708790d65aa01791b66bf6e0639'

def send_message(mobile,datas,tid = '1'):
    sdk = SmsSDK(accId, accToken, appId)
    # tid = '1'
    # mobile = '19810824612'
    # datas = ('1234', '5')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)

if __name__ == '__main__':
    mobile = '19810824612'
    datas = ('1234', '5')
    send_message(mobile,datas)
