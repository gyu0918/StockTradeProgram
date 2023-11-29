from PyQt5.QtCore import *         # 쓰레드 함수를 불러온다.
from kiwoom import Kiwoom          # 로그인을 위한 클래스
from PyQt5.QtWidgets import *      #PyQt import


class Thread1(QThread):
    def __init__(self, parent):   # 부모의 윈도우 창을 가져올 수 있다.
        super().__init__(parent)  # 부모의 윈도우 창을 초기화 한다.
        self.parent = parent      # 부모의 윈도우를 사용하기 위한 조건


        ################## 키움서버 함수를 사용하기 위해서 kiwoom의 능력을 상속 받는다.
        self.k = Kiwoom()
        ##################

        ################## 사용되는 변수
        self.Acc_Screen = "1000"         # 계좌평가잔고내역을 받기위한 스크린

        ###### 슬롯
        self.k.kiwoom.OnReceiveTrData.connect(self.trdata_slot)  # 내가 알고 있는 Tr 슬롯에다 특정 값을 던져 준다.
        ###### EventLoop
        self.detail_account_info_event_loop = QEventLoop()  # 계좌 이벤트루프
        ###### 계좌정보 가져오기
        self.getItemList()               # 종목 이름 받아오기

    #################################### 텍스트 라벨에 집어 넣기

        self.parent.label_1.setText(str(totalBuyingPrice))
        self.parent.label_2.setText(str(currentTotalPrice))
        self.parent.label_3.setText(str(balanceAsset))
        self.parent.label_4.setText(str(totalEstimateProfit))
        self.parent.label_5.setText(str(total_profit_loss_rate))

    def getItemList(self):
        marketList = ["0", "10"]

        for market in marketList:
            codeList = self.k.kiwoom.dynamicCall("GetCodeListByMarket(QString)", market).split(";")[:-1]

            for code in codeList:
                name = self.k.kiwoom.dynamicCall("GetMasterCodeName(QString)", code)
                self.k.All_Stock_Code.update({code: {"종목명": name}})

    def detail_acount_mystock(self, sPrevNext="0"):

        print("계좌평가잔고내역 조회")
        account = self.parent.accComboBox.currentText()  # 콤보박스 안에서 가져오는 부분
        self.account_num = account
        print("최종 선택 계좌는 %s" % self.account_num)

        self.k.kiwoom.dynamicCall("SetInputValue(String, String)", "계좌번호", account)
        self.k.kiwoom.dynamicCall("SetInputValue(String, String)", "비밀번호", "0000")  # 모의투자 0000
        self.k.kiwoom.dynamicCall("SetInputValue(String, String)", "비밀번호입력매체구분", "00")
        self.k.kiwoom.dynamicCall("SetInputValue(String, String)", "조회구분", "2")
        self.k.kiwoom.dynamicCall("CommRqData(String, String, int, String)", "계좌평가잔고내역요청", "opw00018", sPrevNext, self.Acc_Screen)
        self.detail_account_info_event_loop.exec_()
