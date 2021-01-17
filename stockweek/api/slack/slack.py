from slacker import Slacker

class Slack():
    def __init__(self):
        self.token = 'xoxb-1126585321985-1114180369955-#####################'

    def notification(self, pretext=None, title=None, fallback=None, text=None):
        attachments_dict = dict()
        attachments_dict['pretext'] = pretext #test1
        attachments_dict['title'] = title #test2
        attachments_dict['fallback'] = fallback #test3
        attachments_dict['text'] = text #test4

        attachments = [attachments_dict]

        slack = Slacker(self.token)
        slack.chat.post_message(channel='#realmessage', text=None, attachments=attachments, as_user=None)


    #송수신 메세지 get
    def msg_slot(self, sScrNo, sRQName, sTrCode, msg):
        self.logging.logger.debug("스크린: %s, 요청이름: %s, tr코드: %s --- %s" %(sScrNo, sRQName, sTrCode, msg))

