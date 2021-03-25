from pykiwoom.kiwoom import Kiwoom


class HughKiwoom(Kiwoom):
    def __init__(self, program, login=False):
        super().__init__(login)
        self.program = program

    '''
    Override 함수들
    '''

    def _handler_login(self, err_code):
        super()._handler_login(err_code)
        self.program.handler_login(err_code)

    def _handler_condition_load(self, ret, msg):
        super()._handler_condition_load(ret, msg)
        self.program.handler_condition_load(ret, msg)

    def _handler_tr_condition(self, screen_no, code_list, cond_name, cond_index, next):
        super()._handler_tr_condition(screen_no, code_list, cond_name, cond_index, next)
        self.program.handler_tr_condition(screen_no, code_list, cond_name, cond_index, next)

    def _handler_tr(self, screen, rqname, trcode, record, next):
        super()._handler_tr(screen, rqname, trcode, record, next)
        self.program.handler_tr(screen, rqname, trcode, record, next)

    def _handler_msg(self, screen, rqname, trcode, msg):
        super()._handler_msg(screen, rqname, trcode, msg)
        self.program.handler_msg(screen, rqname, trcode, msg)

    def _handler_chejan(self, gubun, item_cnt, fid_list):
        super()._handler_chejan(gubun, item_cnt, fid_list)
        self.program.handler_chejan(gubun, item_cnt, fid_list)

    def _set_signals_slots(self):
        super()._set_signals_slots()

    def CommConnect(self, block=True):
        return super().CommConnect(block)

    def CommRqData(self, rqname, trcode, next, screen):
        return super().CommRqData(rqname, trcode, next, screen)

    def GetLoginInfo(self, tag):
        return super().GetLoginInfo(tag)

    def SendOrder(self, rqname, screen, accno, order_type, code, quantity, price, hoga, order_no):
        return super().SendOrder(rqname, screen, accno, order_type, code, quantity, price, hoga, order_no)

    def SetInputValue(self, id, value):
        return super().SetInputValue(id, value)

    def DisconnectRealData(self, screen):
        return super().DisconnectRealData(screen)

    def GetRepeatCnt(self, trcode, rqname):
        return super().GetRepeatCnt(trcode, rqname)

    def CommKwRqData(self, arr_code, next, code_count, type, rqname, screen):
        return super().CommKwRqData(arr_code, next, code_count, type, rqname, screen)

    def GetAPIModulePath(self):
        return super().GetAPIModulePath()

    def GetCodeListByMarket(self, market):
        return super().GetCodeListByMarket(market)

    def GetConnectState(self):
        return super().GetConnectState()

    def GetMasterCodeName(self, code):
        return super().GetMasterCodeName(code)

    def GetMasterListedStockCnt(self, code):
        return super().GetMasterListedStockCnt(code)

    def GetMasterConstruction(self, code):
        return super().GetMasterConstruction(code)

    def GetMasterListedStockDate(self, code):
        return super().GetMasterListedStockDate(code)

    def GetMasterLastPrice(self, code):
        return super().GetMasterLastPrice(code)

    def GetMasterStockState(self, code):
        return super().GetMasterStockState(code)

    def GetDataCount(self, record):
        return super().GetDataCount(record)

    def GetOutputValue(self, record, repeat_index, item_index):
        return super().GetOutputValue(record, repeat_index, item_index)

    def GetCommData(self, trcode, rqname, index, item):
        return super().GetCommData(trcode, rqname, index, item)

    def GetCommRealData(self, code, fid):
        return super().GetCommRealData(code, fid)

    def GetChejanData(self, fid):
        return super().GetChejanData(fid)

    def GetThemeGroupList(self, type=1):
        return super().GetThemeGroupList(type)

    def GetThemeGroupCode(self, theme_code):
        return super().GetThemeGroupCode(theme_code)

    def GetFutureList(self):
        return super().GetFutureList()

    def GetCommDataEx(self, trcode, record):
        return super().GetCommDataEx(trcode, record)

    def block_request(self, *args, **kwargs):
        return super().block_request(*args, **kwargs)

    def SetRealReg(self, screen, code_list, fid_list, real_type):
        return super().SetRealReg(screen, code_list, fid_list, real_type)

    def SetRealRemove(self, screen, del_code):
        return super().SetRealRemove(screen, del_code)

    def GetConditionLoad(self, block=True):
        return super().GetConditionLoad(block)

    def GetConditionNameList(self):
        return super().GetConditionNameList()

    def SendCondition(self, screen, cond_name, cond_index, search):
        return super().SendCondition(screen, cond_name, cond_index, search)

    def SendConditionStop(self, screen, cond_name, index):
        return super().SendConditionStop(screen, cond_name, index)

    def GetCommDataEx(self, trcode, rqname):
        return super().GetCommDataEx(trcode, rqname)

    def SendOrder(self, rqname, screen, accno, order_type, code, quantity, price, hoga, order_no):
        return super().SendOrder(rqname, screen, accno, order_type, code, quantity, price, hoga, order_no)

    '''
    신규생성 함수
    '''