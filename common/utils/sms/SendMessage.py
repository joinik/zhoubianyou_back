import json

from ronglian_sms_sdk import SmsSDK

# accId = '8aaf0708780055cd0178d32e770f4fc6'
# accToken = '0b7fe4917cf7487f89d8dcfbd68d80f8'
# appId = '8aaf0708780055cd0178d32e77db4fcd'

# lzy
accId = '8aaf0708780055cd0178d32fb5654fd9'
accToken = '2da21647480645d2b6e694f25aaa2be2'
appId = '8a216da878005a800178d330f79d4ffa'



class Sms:
    def __new__(cls, *args, **kwargs):
        if not hasattr(Sms, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
            # 创建一个SmsSDK对象 这里只执行一次 所以SmsSDK对象只有一个
            cls._instance.sms_sdk = SmsSDK(accId, accToken, appId)
        return cls._instance

    def send_message(self, mobile='15532272912', datas=(111111,5), tid="1"):
        # tid = '容联云通讯创建的模板'
        # mobile = '手机号1,手机号2'
        # datas = ('变量1', '变量2')

        resp = self.sms_sdk.sendMessage(tid, mobile, datas)
        resp_dict = json.loads(resp)
        print('>>>>>>>>短信函数')
        # {"statusCode":"000000","templateSMS":{"smsMessageSid":"04983ea5ab374e95b84eece5f43e1f08","dateCreated":"20210415091559"}}
        if resp_dict.get("statusCode") == "000000":
            print("发送短信成功")
            return 0
        else:
            print("发送短信失败")
            return 1



        # print(resp)


if __name__ == '__main__':

    Sms().send_message()
