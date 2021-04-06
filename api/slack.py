import requests
import json


class Slack:

    def __init__(self, program, token):
        self.program = program
        self.token = token

    # def notification(self, pretext=None, title=None, fallback=None, text=None):
    #     attachments_dict = dict()
    #     attachments_dict['pretext'] = pretext #test1
    #     attachments_dict['title'] = title #test2
    #     attachments_dict['fallback'] = fallback #test3
    #     attachments_dict['text'] = text #test4
    #
    #     attachments = [attachments_dict]
    #
    #     slack = Slacker(self.token)
    #     slack.chat.post_message(channel='#stock', text=None, attachments=attachments, as_user=None)

    def notification(self, channel="#stock", text=None):
        response = requests.post("https://slack.com/api/chat.postMessage",
                                 headers={"Authorization": "Bearer " + self.token},
                                 data={"channel": channel, "text": text}
                                 )

        response_text = json.loads(response.text)
        if response.status_code != 200 or response_text.get("error"):
            self.program.logging("slack request error%s  %s: " % (response.status_code, response_text["error"]))

    # 송수신 메세지 get
    def msg_slot(self, sScrNo, sRQName, sTrCode, msg):
        self.program.logging("스크린: %s, 요청이름: %s, tr코드: %s --- %s" % (sScrNo, sRQName, sTrCode, msg))
