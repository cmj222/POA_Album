import json
import os
import os.path
import sys

from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QDir, QSize  # 걍 다 임포트하게 되네 그래도 빨간줄 생기니 걍 냅두자
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import *
from easydict import EasyDict
from win32api import GetSystemMetrics

# 하단이미지뷰의 이미지를 새창에 띄우기


# 하단 3이미지를 새창에서 띄우기 위한 클래스
class NewImageWinidow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    
    # 외부에서 NewImageWinidow(변수) 를 치면 변수를 filePath로 입력받는다
    def __init__(self, filenPath):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)
        images = ["jpg", "png", "tga", "jpeg"]
        videos = ["avi", "mp4", "FLV", "MPEG", "WMV", "Ogg", "WebM"]
        ext = str(filenPath).split('.')[-1]  # 경로포함 파일명을 . 으로 나눠서 리스트로 만들고 맨 마지막놈[= 확장자]를 가져온다.
        ext = ext.lower()  # 만약을 대비해서 확장자를 소문자로 전환시킨다.

        # 이미지파일이 너무 큰 경우를 대비. 움짤인 경우와 공유되는 부분임
        QP = QPixmap(filenPath)
        w = QPixmap(filenPath).width()
        h = QPixmap(filenPath).height()
        # 만약 w가 화면의 너비보다 크거나 h가 화면의 높이보다 크다면 스케일드를 한다.
        if w > GetSystemMetrics(0):
            FQP = QP.scaledToWidth(GetSystemMetrics(0) * 0.95)
        elif h > GetSystemMetrics(1):
            FQP = QP.scaledToHeight(GetSystemMetrics(1) * 0.95)
        else:
            FQP = QP

        if ext in images:  # 만약 이미지확장자에 포함된다면
            self.label.setPixmap(FQP)
            # 새창이 화면 중앙에 뜨게하기
            self.move(GetSystemMetrics(0) / 2 - FQP.width() / 2, GetSystemMetrics(1) / 2 - FQP.height() / 2)
        elif ext == 'gif':
            movie = QMovie(filenPath)
            self.label.setMovie(movie)  # 라벨에 움짤 세팅하고 재생시킨다.
            movie.start()
            # self.move(GetSystemMetrics(0) / 2 - FQP.width() / 2, GetSystemMetrics(1) / 2 - FQP.height() / 2)
            # todo Qmovie는 사이즈조절이 어렵다...일단 패스하자. 졸라 큰 gif 를 자주 쓸것도 아니고...여차하면 리사이즈해라. 일단 패스

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def __del__(self):  # 클래스가 종료될때 = 이미 뜬 상태라 close()가 발동할때.
        WindowClass.window_imgae_poa = None


# json 저장 불러오기용 클래스. 건들기 ㄴㄴ
class JsonConfigFileManager:  # 외부파일 json 과 연결하는 클래스. 건들기 ㄴㄴ
    # https://m.blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221540272941&proxyReferer=https:%2F%2Fwww.google.com%2F
    """Json설정파일을 관리한다"""

    def __init__(self, file_path):
        self.values = EasyDict()
        if file_path:
            self.file_path = file_path  # 파일경로 저장
            self.reload()

    def reload(self):
        """설정을 리셋하고 설정파일을 다시 로딩한다"""
        self.clear()
        if self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as f:  # 한글로저장해도 오류안뜸.
                self.values.update(json.load(f))

    def clear(self):
        """설정을 리셋한다"""
        self.values.clear()

    def update(self, in_dict):
        """기존 설정에 새로운 설정을 업데이트한다(최대 3레벨까지만)"""
        for (k1, v1) in in_dict.items():
            if isinstance(v1, dict):
                for (k2, v2) in v1.items():
                    if isinstance(v2, dict):
                        for (k3, v3) in v2.items():
                            self.values[k1][k2][k3] = v3
                    else:
                        self.values[k1][k2] = v2
            else:
                self.values[k1] = v1

    def export(self, save_file_name):
        """설정값을 json파일로 저장한다"""
        if save_file_name:
            with open(save_file_name, 'w', encoding='utf-8') as f:  # 한글저장해도 오류안뜸.
                json.dump(dict(self.values), f, ensure_ascii=False)  # 한글로 저장됨.

# 옆의 main.ui의 카피패스로 경로를 따온다.
# 폼클래스를 정의한다. uic에서 ui타입을 로딩한다. 대상은 경로와 같다.


# form_class = uic.loadUiType("./main.ui")[0] 작동했던 원본. 하지만 exe로 전환시 문제됨.
# FileNotFoundError: [Errno 2] No such file or directory: './main.ui'
form_class = uic.loadUiType(r'F:\POA_program\main.ui')[0]
#uic.loadUi(r'F:\POA_program\main.ui', self)

# 편집창에서 5요소 같이 숫자있을때 숫자전환시 강제종료됨...흠.... 패스해 시발. 개같이 구네.
# todo 이전에 작업했던 경로를 기억했다가 실행시 탐색기가 자동으로 해당경로 선택하고 있게 하기??
# 정확히는 이전에 폴드 언폴드했던 정보를 저장하고 이후 프로그램실행시 이를 가져와서 시행.
# todo 단축키 설명문 작성. 컨트롤탭은 모드전환. 컨트롤에스는 저장. 키패드는 하단이미지 이동, 새창. 0은 보기가리기. .은 다음드러내기
class WindowClass(QMainWindow, form_class):
    # 윈도우클래스는 q메인윈도우를 상속받아서 폼클래스로 전달할 것이다.

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ##################
        ### 변수선언구간 ###
        ##################

        # 파일경로 관련 변수
        self.model = QFileSystemModel()  # 탐색기시스템
        self.tree = self.tree_view  # 오브젝트와 연결
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 실행파일이 있는 폴더
        self.PoaMemo = str(self.BASE_DIR) + '/PoaMemo'  # 메모내용들이 담길 폴더
        self.PoaList = str(self.BASE_DIR) + '/PoaList'
        self.crawler = ''  # 탐색기에서 선택한 대상의 경로포함 폴더이름
        self.current_path = ''  # 탐색기로 경로지정해서 열은 현재 폴더경로

        # 중앙 상단 이미지 표기 관련 변수
        self.imgs = []  # 경로상 파일들의 경로포함이름[../경영학/1역사발전/0001.jpg]들을 포함할 리스트
        self.current_page = 0  # 현재 페이지

        # 상단 이미지의 정보 표기 관련 변수
        self.showOrHidden = 'hidden'  # 처음에는 초성, 키워드, 추가설명, 아래의 3이미지 모두 감춤상태. 보기모드시 show로 전환
        self.viewPhase = 0  # 아무것도 안보임. 1 숫자는 보임. + 아래의 3이미지도 보임. 2 단어도 보임. 3 모두 보임.


        ### 리스트 기능에 쓰일 변수들.
        self.word_type = ''  # 문자가 몇글자짜리인지를 체크해서 2~6글자여부를 저장
        self.person = ''
        self.object = ''
        self.Taction = ''
        self.Jaction = ''
        self.current_page_P = 0  # 리스트뷰에서 현재 그림의 순서
        self.current_page_O = 0
        self.current_page_A = 0
        self.current_page_poa = 0  # 페이지이동시 쓰일 중간매개변수

        # 리스트뷰시 파일들 목록들. 진입시에 초기화하고 다시 획득하는 과정 거침.
        # 다음 이전 버튼시에는 획득한 리스트의 파일들 안에서 순환
        self.imgsP = []
        self.imgsO = []
        self.imgsTa = []
        self.imgsJa = []

        # 리스트뷰시 파일들을 가져올 경로. 폴더열기에도 활용됨.
        self.pathP = ''
        self.pathO = ''
        self.pathTa = ''
        self.pathJa = ''
        # 정보창[우상단]에 띄울 내용들
        self.value_number = ''
        self.value_word = ''
        self.value_extra = ''
        self.value_memo = ''

        ####################
        ### 자동실행 함수들 ###
        ####################

        # 첫실행여부 체크구간 #
        self.MakeDir()  # 같은 폴더에 필수폴더 없을시 필수폴더 생성함수
        # 필수외부파일인 PoaMemo.json 여부 체크 및 없으면 생성
        self.MakeJson()
        # json 전용 변수. 맨위에 놓으면 순서상 오류발생???
        self.conf = JsonConfigFileManager('./PoaMemo.json')  # json 파일의 내용을 읽어서 변수로 넣음.
        # 첫화면 #
        self.FileSystem(self.PoaMemo)  # basePath를 받아서 파일탐색기를 띄워라

        ###########################
        ### 버튼 트리거, 반응 구간 ###
        ###########################

        # 폴더보기 버튼을 누르면 선택한 폴더를 새창에서 연다
        self.button_openFolder.clicked.connect(self.openMemoFolder)
        # 보기모드 버튼을 누르면 보기모드라는 함수를 시행한다.
        self.button_view.clicked.connect(self.viewPage)

        # 보기모드의 버튼들
        self.button_next_view.clicked.connect(self.view_show_next)
        self.button_pre_view.clicked.connect(self.view_show_pre)
        self.button_number_view.clicked.connect(self.view_show_number)
        self.button_viewOrHidden.clicked.connect(self.viewMode_onOff)  # 보기 감추기 모드 전환
        self.button_nextPhase_view.clicked.connect(self.view_nextPhase)  # 감추기모드에서 하나씩 밝혀나감.
        self.button_from_view_to_edit.clicked.connect(self.editPage)

        # 버튼을 누르면 편집모드라는 함수를 시행한다.
        self.button_edit.clicked.connect(self.editPage)

        # 편집모드의 버튼들
        self.button_next_edit.clicked.connect(self.edit_show_next)
        self.button_pre_edit.clicked.connect(self.edit_show_pre)
        self.button_number_edit.clicked.connect(self.edit_show_number)
        self.button_save_edit.clicked.connect(self.edit_save)
        self.button_word_to_number.clicked.connect(
            lambda state, situlation='from_word_edit': self.word_to_number(situlation))
        self.button_make_next_edit.clicked.connect(self.CreateNewImage_Edit)
        self.button_screenshot_edit.clicked.connect(self.screenshot)
        self.button_from_edit_to_view.clicked.connect(self.viewPage)
        # 입력창에 엔터치면 문자나 숫자에 맞는 p o a 띄우기 관련 신호들
        self.POA_number.editingFinished.connect(lambda which='': self.viewPOA(which))
        self.word_edit.editingFinished.connect(
            lambda situlation='from_word_edit': self.word_to_number(situlation))  # 단어창에 엔터치면 숫자란 자동입력
        self.word_edit.editingFinished.connect(lambda which='editMode': self.viewPOA(which))  # 편집창 숫자란의 숫자를 리스트 숫자란에
        self.number_edit.editingFinished.connect(lambda which='editMode': self.viewPOA(which))

        # 리스트뷰 버튼그룹의 버튼 신호들
        self.view_next_person.clicked.connect(
            lambda state, poa='person', isnext='true': self.viewPOA_next_pre(poa, isnext))
        self.view_pre_person.clicked.connect(
            lambda state, poa='person', isnext='false': self.viewPOA_next_pre(poa, isnext))
        self.view_next_object.clicked.connect(
            lambda state, poa='object', isnext='true': self.viewPOA_next_pre(poa, isnext))
        self.view_pre_object.clicked.connect(
            lambda state, poa='object', isnext='false': self.viewPOA_next_pre(poa, isnext))
        self.view_next_action.clicked.connect(
            lambda state, poa='action', isnext='true': self.viewPOA_next_pre(poa, isnext))
        self.view_pre_action.clicked.connect(
            lambda state, poa='action', isnext='false': self.viewPOA_next_pre(poa, isnext))
        self.view_folder_person.clicked.connect(lambda state, poa='person': self.openFolder(poa))
        self.view_folder_object.clicked.connect(lambda state, poa='object': self.openFolder(poa))
        self.view_folder_action.clicked.connect(lambda state, poa='action': self.openFolder(poa))
        self.view_new_person.clicked.connect(lambda state, poa='person': self.viewNewWindow(poa))
        self.view_new_object.clicked.connect(lambda state, poa='object': self.viewNewWindow(poa))
        self.view_new_action.clicked.connect(lambda state, poa='action': self.viewNewWindow(poa))

        # 새창 띄우기에 필요한 변수수
        self.window_imgae_poa = None  # 현재 창이 떠지지 않은 상태임을 나타냄.

        # self.actionTest.triggered.connect(self.test)
        # self.actionTest2.triggered.connect(self.test2)

        # # 만약 탐색기에서 선택한 폴더에 이미지파일이 하나도 없다면 경고창을 띄운다.
        # self.getSelected()  # 탐색기상 선택한 폴더를 self.crawler로 반환
        # imgs = []
        # self.getFolderImages(self.crawler, imgs) #  폴더내의 이미지파일의 이름들을 리스트에 반환
        # if imgs:
        #     return  # 이미지가 있으면 선택한 모드에 맞는 함수대로 진행함.
        # answer = self.noImagemessageBox()
        # if answer == QMessageBox.Yes:
        #     self.createNewImageFile(self.crawler, 'img001')
        #     self.editPage()
        #     self.img_view.setText('임시이미지파일 생성 완료. 우상단의 스샷버튼 누르면 스크린샷이미지로 대체됨')

    def CreateNewImage_Edit(self):
        answer = self.noImagemessageBox()
        if answer == QMessageBox.Yes:
            lastFile = self.imgs[-1]  # 맨 마지막놈의 경로포함이름
            ext = str(lastFile).split('.')[-1]  # 확장자
            name = str(lastFile).split('.')[-2]  # 확장자 제외 이름
            last3 = name[-3:] # 확장자 제외 이름에서 뒤에서 3글자 추출
            if last3.isdigit():  # 만약 숫자라면 +1만 해주자.
                last3 = str(int(last3) + 1)
                newname = name[:-3] + last3  # 뒤에서3글자 제거한 이름 + 뒤에서3글자에1더한수[문자열]
            else:
                newname = name + '_000'
            f = open(newname + '.' + ext, 'w')
            f.close()
            self.newImageFile = newname + '.' + ext
            self.getFolderImages(self.crawler, self.imgs)  # 파일추가된 걸 반영하기 위해서 목록 새로고침
            self.current_page = len(self.imgs) - 1
            self.page_number_edit.setText(str(len(self.imgs)))
            self.page_all_edit.setText('/ ' + str(len(self.imgs)))
            self.showimage()
            self.setValueFromJson()
            self.img_view.setText('임시이미지파일 생성 완료. 우상단의 스샷버튼 누르면 스크린샷이미지로 대체됨')

    # 새로운이미지생성할꺼냐? 메시지박스
    def noImagemessageBox(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("지정된 지점에 이미지파일이 없습니다.")
        msgBox.setText("새로운 이미지파일을 생성하시겠습니까? .")
        msgBox.setInformativeText("이후 편집모드의 스크린샷 기능으로 대체 가능합니다.")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Yes)
        return msgBox.exec_()

    # 경로와 파일이름을 받아서 경로에 파일이름 + .png 새로운 이미지파일을 만들고 반환한다.
    def createNewImageFile(self, path, filename):
        filename = filename + '.png'
        f = open(os.path.join(path, filename), 'w')
        f.close()
        self.newImageFile = os.path.join(path, filename)

    # 버튼이 눌렸으니 5초 뒤에 스크린샷함수를 시행해라.
    def screenshot(self):
        import threading
        timer = threading.Timer(5, self.GetScreenshot)  # 5초간 대기했다가
        timer.start()

    # [5초가 지난] 지금의 스크린샷을 찍고 저장.
    def GetScreenshot(self):
        from PIL import ImageGrab
        img = ImageGrab.grab()
        saveas = 'screenshot.png'
        saveas = self.imgs[self.current_page]
        img.save(saveas)
        self.getFolderImages(self.crawler, self.imgs)
        self.showimage()
        import winsound
        duration = 500  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)
        # todo 이전의 파일 보관해놓고 있다가 스샷대입완료 후 메시지로 복원할 것이냐고 물어보기.

    ### 첫실행인 경우 [ 폴더생성 ]

    # 실행파일과 같은 폴더에 필수폴더가 없는 경우 = 첫실행시 ㄱㄱ~ㅎㅎ 생성. poamemo 생성
    def MakeDir(self):
        if not os.path.exists("./PoaList"):
            os.mkdir("./PoaList")
            for i in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']:
                for m in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']:
                    os.mkdir("./PoaList/" + str(i) + str(m) + 'p')
                    os.mkdir("./PoaList/" + str(i) + str(m) + 'o')
                    os.mkdir("./PoaList/" + str(i) + str(m) + 'ta')
                    os.mkdir("./PoaList/" + str(i) + str(m) + 'ja')
        if not os.path.exists("./PoaMemo"):
            os.mkdir("./PoaMemo")

    def MakeJson(self):
        if not os.path.exists('./PoaMemo.json'):
            f = open('./PoaMemo.json', 'w')
            f.write('{}')
            f.close()

    ### 탐색기 ~ 경로선택
    # 좌상단에 탐색기를 띄운다
    def FileSystem(self, basePath):
        ### 파일탐색기를 트리뷰에 띄우는 부분임. ###
        self.model.setRootPath(QDir.rootPath())  # 이유는 모르겠지만 이게 빠지면 아무것도 안뜬다.
        self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)  # 탐색기에 폴더만 뜨게함
        self.tree.setModel(self.model)  # 이거 위치 잘못배치해서 3시간 헤맴 ㅅㅂ
        # self.tree.setRootIndex(self.model.index(QDir.currentPath())) # 이러면 py가 있는 폴더를 제시함
        self.tree.setRootIndex(self.model.index(basePath))  # init 에서 변수선언.
        self.tree.setAnimated(False)
        self.tree.setIndentation(10)  # 이름옆의 화살표가 얼마나 띄어써지는지.
        self.tree.setSortingEnabled(True)
        self.tree.setColumnHidden(1, True)  # 사이즈 열을 가린다.
        self.tree.setColumnHidden(2, True)  # 타입설명 열을 가린다.
        self.tree.setColumnHidden(3, True)  # 수정날짜 열을 가린다.
        self.show()

    # 탐색기에서 선택한 항목을 경로포함이름으로 self.crawler에 반환
    def getSelected(self):
        index = self.tree.currentIndex()
        self.crawler = self.model.filePath(index)
        print(self.crawler)
        #  F:/POA_program/PoaMemo/경영학/1. 경영학입문  비록 반환을 \\없이 하지만 이를 경로상으로 입력해도 알아서 인식하네.

    ### 경로선택시 jsob에서 데이터 추출 및 대입
    # json 에서 값 가져오기 함수
    def getValueFromJson(self):
        # 현재이미지의 경로포함파일명을 가져와서 태그로 쓴다.
        tagName = self.imgs[self.current_page]
        # 그 태그 아래의 값들을 가져다가 변수에 대입한다.
        if self.conf.values.get(tagName):  # tagName이라는 키값이 있는지 = 이전에 값들을 작성하여 json에 저장하였는지 체크
            self.value_number = self.conf.values[tagName]['number']  # 존재하지 않는 걸 찾으니 발광하는 느낌인데...
            self.value_word = self.conf.values[tagName]['word']
            self.value_extra = self.conf.values[tagName]['extra']
            self.value_memo = self.conf.values[tagName]['memo']
        else:  # 저장된 값이 없으면 공백으로 리셋시킨다.
            self.value_number = ''
            self.value_word = ''
            self.value_extra = ''
            self.value_memo = ''

    # 가져온 값을 저장하고 상황[self.viewPhase]에 따라 텍스트란에 입력. 화면전환시에도 작동
    def setValueFromJson(self):
        self.getValueFromJson()

        # 편집모드에서는 보기 가리기 의미없으니 걍 바로 대입
        self.number_edit.setText(self.value_number)
        self.word_edit.setText(self.value_word)
        self.extra_edit.setText(self.value_extra)
        self.memo_edit.setText(self.value_memo)

        # 보기모드의 값들 상황에 따라 채워넣기
        if self.showOrHidden == 'show':  # 만약 보기모드라면 걍 보여주고 함수를 넘긴다.
            self.number_view.setText(self.value_number)
            self.word_view.setText(self.value_word)
            self.extra_view.setText(self.value_extra)
            self.memo_view.setText(self.value_memo)
            return
        # 아니라면 일단 가린 다음에 단계를 확인하며 드러낸다.
        self.number_view.setText('????')
        self.word_view.setText('????')
        self.extra_view.setText('????')
        if self.value_memo == '':
            self.memo_view.setFontPointSize(12)
            self.memo_view.setText('내용 無')
        else:
            self.memo_view.setFontPointSize(20)
            self.memo_view.setText('추가 메모 있음')
        # if self.showOrHidden == 'hidden':
        #     return  # 감추기면 모두 ????인 상태로 패스해버려라.
        if self.viewPhase == 1: # 숫자와 아래의 3이미지가 보임
            self.number_view.setText(self.value_number)
            self.extra_view.setText(self.value_extra)
            # self.reveal_3images
        if self.viewPhase == 2:  # 단어전체도 보임
            self.number_view.setText(self.value_number)
            self.word_view.setText(self.value_word)
            self.extra_view.setText(self.value_extra)
        if self.viewPhase == 3:  # 모두 보임.
            self.number_view.setText(self.value_number)
            self.word_view.setText(self.value_word)
            self.extra_view.setText(self.value_extra)
            self.memo_view.setText(self.value_memo)

        # 편집모드의 값들 채워넣기
        self.number_edit.setText(self.value_number)
        self.word_edit.setText(self.value_word)
        self.extra_edit.setText(self.value_extra)
        self.memo_edit.setText(self.value_memo)

    # 좌상단의 탐색기창의 폴더를 새창에서 연다.
    def openMemoFolder(self):
        self.getSelected()
        path = os.path.realpath(self.crawler)
        os.startfile(path)

    # 만약 보기모드나 편집모드를 눌렀을때 빈폴더면 메시지박스 뜨게하는 함수. 모드버튼함수의 마지막에 조건부로 시행됨.
    def CreateNewImage_Browser(self):
        answer = self.noImagemessageBox()
        if answer == QMessageBox.Yes:
            self.createNewImageFile(self.crawler, 'img001')
            self.editPage()
            self.img_view.setText('임시이미지파일 생성 완료. 우상단의 스샷버튼 누르면 스크린샷이미지로 대체됨')


    ### 보기모드의 함수들 ###
    # 보기모드 버튼 누르면 작동 -> 탐색기에서 선택된 폴더를 체크 -> 선택된 경로의 이미지들을 목록화 -> 목록 중 첫째를 선택 -> 라벨에 띄운다.
    def viewPage(self):
        self.getSelected()  # 클릭되어있는 경로 체크
        if not self.current_path == self.crawler:
            self.current_page = 0
        if not self.crawler == '':  # 선택한 상태라 다른것이 반환되었다면...
            self.getFolderImages(self.crawler, self.imgs)  # 선택한 폴더의 경로포함 이미지파일 이름들 반환.
            if self.imgs:
                self.current_path = self.crawler
                self.view_edit.setCurrentIndex(0)  # 우상단의 편집창이 보기모드가 되게함.
                self.showimage()  # 위 리스트의 첫째를 화면에 뜨게함
                self.page_number_view.setText(str(self.current_page + 1))  # 현재페이지수를 반환하는 함수. 커런트페이지보다 1 크게.
                self.page_all_view.setText('/ ' + str(len(self.imgs)))  # 전체그림수를 반환하는 함수
                self.setValueFromJson()  # 빈칸들 채워넣기
                self.viewPOA('viewMode')
            elif not self.imgs:
                self.CreateNewImage_Browser()

    ### 보기모드의 버튼 관련 함수들 ###
    # 다음 이미지 표기
    def view_show_next(self):
        if not str(len(self.imgs) - 1) == str(self.current_page):
            self.current_page += 1
            self.showimage()
            self.page_number_view.setText(str(self.current_page + 1))
            self.setValueFromJson()  # 빈칸들 채워넣기
            self.viewPOA('viewMode')
        else:
            pass

    # 이전 이미지 표기
    def view_show_pre(self):
        if not 0 == self.current_page:
            self.current_page -= 1
            self.showimage()
            self.page_number_view.setText(str(self.current_page + 1))
            self.setValueFromJson()  # 빈칸들 채워넣기
            self.viewPOA('viewMode')
        else:
            pass

    # 번호 이동버튼시 반응
    def view_show_number(self):
        if self.page_number_view.text().isdigit:  # 입력란에 숫자가 입력되어있고
            if int(self.page_number_view.text()) >= 0:  # 입력란에 0이상의 숫자가 입력되어있으며
                if int(self.page_number_view.text()) < len(self.imgs):  # 파일들의 개수 이하인 숫자가 입력외어있다면
                    self.current_page = int(self.page_number_view.text()) - 1  # 후 int 안달았다고 지랄이라니...
                    self.showimage()
                    self.setValueFromJson()  # 빈칸들 채워넣기
                    self.viewPOA('viewMode')
        else:
            pass

    # 처음에는 감춤상태. 보기모드시 show로 전환
    def viewMode_onOff(self):
        if self.showOrHidden == 'hidden':
            self.showOrHidden = 'show'
           # self.button_viewOrHidden.setText('확인모드') # 셋텍스트로 글자바꾸면 디자이너의 단축키지정이 풀린다...
        else:
            self.showOrHidden = 'hidden'
           # self.button_viewOrHidden.setText('시험모드')
        self.setValueFromJson()
        self.viewPOA('viewMode')  # 바뀐 설정에 따라 아래의 poa가 표기되거나 가려짐.

    # 버튼누를때마다 차례대로 드러남. 아무것도 안보임. 1 숫자는 보임. 2 단어도 보임. 3 모두 보임.
    def view_nextPhase(self):
        self.viewPhase += 1
        if self.viewPhase == 4:  # 모두보임 상태에서 다시 다음으로 누르면...초기값 0으로
            self.viewPhase = 0
        print(self.viewPhase)
        self.setValueFromJson()
        self.viewPOA('viewMode')

    ### 편집모드 버튼 관련 함수들 ###
    # 편집모드 버튼 누르면 작동 -> 탐색기에서 선택된 폴더를 체크 -> 선택된 경로의 이미지들을 목록화 -> 목록 중 첫째를 선택 -> 라벨에 띄운다.
    def editPage(self):
        self.getSelected()
        if not self.current_path == self.crawler:  # 현재 보고있는 폴더와 다른 폴더를 본다면 첫페이지로 돌아간다.
            self.current_page = 0
        if not self.crawler == '':  # 선택한 상태라 다른것이 반환되었다면...
            self.getFolderImages(self.crawler, self.imgs)  # 선택한 폴더의 경로포함 이미지파일 이름들 반환.
            if self.imgs:
                self.current_path = self.crawler
                self.view_edit.setCurrentIndex(1)  # 우상단의 편집창이 편집모드가 되게함.
                self.showimage()  # 위 리스트의 첫째를 화면에 뜨게함
                self.page_number_edit.setText(str(self.current_page + 1))  # 현재페이지수를 반환하는 함수. 커런트페이지보다 1 크게.
                self.page_all_edit.setText('/ ' + str(len(self.imgs)))  # 전체그림수를 반환하는 함수
                self.setValueFromJson()  # 빈칸들 채워넣기
                self.viewPOA('editMode')
            elif not self.imgs:
                self.CreateNewImage_Browser()
    # 다음버튼시 반응. 다음 이미지 표기
    def edit_show_next(self):
        if not str(len(self.imgs) - 1) == str(self.current_page):
            self.current_page += 1
            self.showimage()
            self.page_number_edit.setText(str(self.current_page + 1))
            self.setValueFromJson()  # 빈칸들 채워넣기
            self.viewPOA('editMode')
        else:
            pass

    # 이전버튼시 반응. 이전 이미지 표기
    def edit_show_pre(self):
        if not 0 == self.current_page:
            self.current_page -= 1
            self.showimage()
            self.page_number_edit.setText(str(self.current_page + 1))
            self.setValueFromJson()  # 빈칸들 채워넣기
            self.viewPOA('editMode')
        else:
            pass

    # 번호 이동버튼시 반응. 번호 이미지 표기
    def edit_show_number(self):
        if self.page_number_edit.text().isdigit:  # 입력란에 숫자가 입력되어있고
            if int(self.page_number_edit.text()) >= 0:  # 입력란에 0이상의 숫자가 입력되어있으며
                if int(self.page_number_edit.text()) < len(self.imgs):  # 파일들의 개수 이하인 숫자가 입력외어있다면
                    self.current_page = int(self.page_number_edit.text()) - 1  # 후 int 안달았다고 지랄이라니...
                    self.showimage()
                    self.setValueFromJson()  # 빈칸들 채워넣기
                    self.viewPOA('editMode')
        else:
            pass

    # 저장버튼시 반응
    def edit_save(self):
        # 먼저 jsonM으로 저장할 원본을 부른다.
        self.conf = JsonConfigFileManager('./PoaMemo.json')
        print('제이손 로딩완료')
        print(self.conf.values)
        # 먼저 현재 현재 보고있는 이미지를 경로포함파일명...tagname 를 구한다.
        tagName = self.imgs[self.current_page]
        # number_edit, word_edit, extra_edit, memo_edit 를 구하고 value_~ 라 한다.
        self.value_number = self.number_edit.text()
        self.value_word = self.word_edit.text()
        self.value_extra = self.extra_edit.text()
        self.value_memo = self.memo_edit.toPlainText()
        # json은 키값을 동적으로 변환 안시켜주는 병신이라 중간과정이 필요하다.
        node1 = self.conf.values  # 이건 중간과정을 위한 매개체다. json파일의 내용물을 대입한다.
        subsub = {}  # json은 키값을 동적으로 변환 안시켜주는 병신이라 중간과정이 필요하다. 중간과정용 사전이다.
        name = ['number', 'word', 'extra', 'memo']
        value = [self.value_number, self.value_word, self.value_extra, self.value_memo]
        for x in range(len(name)):  # 그 중간과정
            subsub[name[x]] = value[x]
        node1[tagName] = subsub  # 흠...사전[변수] = 사전 형식으로 다층구조의 값을 가진 동적인 키를 만든다.
        print(node1)  # 내가 원하는 그 스타일이 되었다. 키 = 경로포함파일명, 값1 : 번호, 값2 : 단어...인 스타일의.
        self.conf.values = node1  # 역으로 주입해준다. 이제 easydic 을 쉽게 활용할 수 있따....
        self.conf.export('./PoaMemo.json')
        self.viewPOA('editMode')
        self.memo_view.clearFocus()

    # 단어를 숫자로 전환하는 함수. 버튼을 누르거나 단어창에서 엔터를 치면 발동.
    # 좌하단 입력란에 단어 입력 후 엔터시에도 발동.
    def word_to_number(self, situlation):
        print('신호는 도달함')
        word = '초기값'
        if situlation == 'from_word_edit':
            word = self.word_edit.text()
            output = self.number_edit
        elif situlation == 'from_POA_number':
            word = self.POA_number.text()
            output = self.POA_number
        print('워드투넘버 함수의 변환할 텍스트는 ' + word)
        CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        w_to_k = {'ㄱ': '1', 'ㄲ': '1', 'ㄴ': '2', 'ㄷ': '3', 'ㄸ': '3', 'ㄹ': '4', 'ㅁ': '5', 'ㅂ': '6',
                  'ㅃ': '6', 'ㅅ': '7', 'ㅇ': '8', 'ㅈ': '9', 'ㅉ': '9', 'ㅊ': '9.', 'ㅋ': '1.', 'ㅌ': '3.', 'ㅍ': '6.',
                  'ㅎ': '0'}
        chosung = []
        num = ''
        for w in list(word.strip()):
            if '가' <= w <= '힣':
                ch1 = (ord(w) - ord('가')) // 588
                chosung.append(CHOSUNG_LIST[ch1])
            else:
                chosung.append([w])   # 초성 리스트는 ['5', 'ㅇ',...]
        for i in chosung:
            if i in w_to_k.keys():
                num += w_to_k[i]

        output.setText(num)
        self.value_number = num  # 나중에 활용할때 참고하는 자료는 밸류_넘버임. 이걸 빼트려서 삽질함.
        print('문자에서 숫자전환 전환 완료.결과는 ' + num)
        # 뭔가 구조가 순환구조스럽게 구리게 만들어지는 기분인데...
        if situlation == 'from_word_edit':
            self.viewPOA('editMode')
        elif situlation == 'from_POA_number':
            self.viewPOA('')

    ### 상단이미지표기관련 보기, 편집 공통함수
    # 제시한 경로의 폴더의 이미지파일[경로포함]들을 제시한 목록에 반환한다.
    def getFolderImages(self, path, fileList):
        fileList.clear()  # 리스트를 비운다. 무식하게 fileList = [] 로 하면 튕기더라고...
        for f in os.listdir(path):  # 폴더까지 개체로 포함시킨다.
            if os.path.isfile(os.path.join(path, f)):  # 파일만 추려서
                fileList.append(str((path) + '/' + f))  # 리스트에 추가하기

    # 상단 이미지창에 이미지 표기
    def showimage(self):
        self.pixmap = QPixmap()
        self.img_view.setPixmap(QPixmap(self.imgs[self.current_page]))  # 이건 되네 시발...마찬가지로 경로가 음...

    ##########################
    ### 리스트뷰[하단 3이미지] ###
    ##########################

    ### 작업할 수치확보
    # 숫자를 분석하고 p o a 값 반환하기
    def wordToPoa(self, number):
        print(number)
        length = len(number)
        print(length)
        if length >= 6:
            self.word_type = '6'
            self.person = number[0:2]
            self.object = number[2:4]
            self.Taction = number[4:6]
            self.Jaction = ''
        if length == 5:
            self.word_type = '5'
            self.person = number[0:2]
            self.object = number[1:3]
            self.Taction = number[3:5]
            self.Jaction = ''
        if length == 4:
            self.word_type = '4'
            self.person = number[0:2]
            self.object = ''
            self.Taction = ''
            self.Jaction = number[2:4]
        if length == 3:
            self.word_type = '3'
            self.person = number[0:2]
            self.object = number[1:3]
            self.Taction = number[3] + number[4]
            self.Jaction = ''
        if length == 2:
            self.word_type = '2'
            self.person = '@' + number[0]
            self.object = ''
            self.Taction = ''
            self.Jaction = '@' + number[1]

    # 하단의 gif 포함한 이미지를 p o a에 따라 적합한 곳에 표기하는 함수. 자주 활용됨.
    def showImageWithGif(self, filename, label):
        # todo 영상을 보기 위해서 스택위젯을 활용할테니 스택위젯관련된 오브젝트 변수란...보다는 label을 받아서 이름 갈아치워도
        #  작동하게 만들자
        images = ["jpg", "png", "tga", "jpeg"]
        videos = ["avi", "mp4", "FLV", "MPEG", "WMV", "Ogg", "WebM"]
        ext = str(filename).split('.')[-1]  # 경로포함 파일명을 . 으로 나눠서 리스트로 만들고 맨 마지막놈[= 확장자]를 가져온다.
        ext = ext.lower()  # 만약을 대비해서 확장자를 소문자로 전환시킨다.
        if ext in videos:
            pass  # todo 스택위젯을 영상있는 쪽으로 돌리고 영상표기함수

        else:
            pass  # 스택위젯을 이미지 쪽으로 돌린다.
        if ext in images:  # 만약 이미지확장자에 포함된다면
            label.setPixmap(QPixmap(filename))
        elif ext == 'gif':
            movie = QMovie(filename)  # 움짤을 불러올 QMovie 파일 불러오고 변수로 지정
            movie.setScaledSize(QSize(label.size().width(), label.size().height()))  # 라벨창의 크기에 맞게 움짤사이즈 조정
            label.setMovie(movie)  # 라벨에 움짤 세팅하고 재생시킨다.
            movie.start()

    # 하단의 p o a 이미지를 표기하라는 명령을 받았을때 수행함수. 이후 다음이전 버튼과는 별개임.
    # 하나의 함수에 너무 많은 기능이 내포됨...분할하자
    def viewPOA(self, which):  # 어느 모드에서 시행하느냐에 따라 which에 eidtMode 혹은 viewMode가 옴.
            # 명령을 받은 상태에 따라 어느 곳의 숫자를 가져다가 숫자란에 대입할 건지 결정.
            if which == 'editMode':
                # self.POA_number.setText(self.number_edit.text())
                self.POA_number.setText(self.value_number)
            elif which == 'viewMode':
                self.POA_number.setText(self.value_number)
                # self.POA_number.setText(self.number_view.text())
            elif which == '':  # 상단의 앨범모드에서 보는게 아니라 좌단의 입력란에 숫자나 문자 입력시.
                gettext = str(self.POA_number.text())
                if not gettext.isdigit():  # 만약 숫자입력란에 숫자가 아니라 문자를 입력했다면
                    self.word_to_number('from_POA_number')  # 입력란의 문자를 숫자로 전환한다.
            # 좌하단의 숫자를 입력값으로 하여 p o a를 반환하게 함.
            number = self.POA_number.text().replace(".", "")  # . 이 있는걸 처리할때는 씹도록 만든다.

            # 새로 진입함을 가정하니 리스트를 비워준다.
            self.imgsP = []
            self.imgsO = []
            self.imgsTa = []
            self.imgsJa = []
            # 리스트뷰에서 볼 파일의 순번 초기화
            self.current_page_P = 0
            self.current_page_O = 0
            self.current_page_A = 0

            self.wordToPoa(number)  # 입력값의 길이를 토대로 self.person 등에 맞는 숫자를 대입한다.
            self.pathP = str(self.PoaList) + '/' + self.person + 'p'  # 반환된 숫자를 토대로 경로를 구한다.
            self.pathO = str(self.PoaList) + '/' + self.object + 'o'
            self.pathTa = str(self.PoaList) + '/' + self.Taction + 'ta'
            self.pathJa = str(self.PoaList) + '/' + self.Jaction + 'ja'
            case5 = str(self.PoaList) + '/' + self.object + 'p'  # 5글자일때 오브젝트를 2~3번째 숫자의 인물로 대입

            # 경로상의 이미지파일목록을 구하고 리스트에 추가.
            # 리스트가 비었으면 라벨에 '자료없음' 표기. 있으면 이미지,움짤,영상 표기

            def infunction(PathPoa, ListPoa, label):
                List = []
                # 경로상의 이미지들을 경로포함이름으로 리스트에 추가한다.
                self.getFolderImages(PathPoa, List)
                for i in List:  # 주의!!! 리스트 = 리스트는 대입이 아니구나 시발. 대입하려면 이렇게 해야함.
                    ListPoa.append(i)
                # 만약 리스트가 비어있다면 라벨을 '자료없음'으로 바꾼다.
                if not ListPoa:
                    label.setText('자료없음')
                # 있다면 주어진 라벨에 이미지, 움짤, 영상을 표기한다.
                else:
                    self.showImageWithGif(ListPoa[0], label)
                return ListPoa

            def POA_label_show():  # 아래의 poa의 3라벨 각각에 이미지를 표기한다.
                if str(self.word_type) in ['3', '6']:  # 조건문 주의사항...시발. == '3' or '5' 면 무조건 참이구나.
                    infunction(self.pathP, self.imgsP, self.img_person_label)
                    infunction(self.pathO, self.imgsO, self.img_object_label)
                    infunction(self.pathTa, self.imgsTa, self.img_action_label)
                if str(self.word_type) == '5':  # 5글자일때 오브젝트를 2~3번째 숫자의 인물로 대입
                    infunction(self.pathP, self.imgsP, self.img_person_label)
                    infunction(case5, self.imgsO, self.img_object_label)  # 흠 이거 참...
                    infunction(self.pathTa, self.imgsTa, self.img_action_label)
                elif str(self.word_type) in ['4', '2']:
                    infunction(self.pathP, self.imgsP, self.img_person_label)
                    self.img_object_label.setText('자료없음')
                    infunction(self.pathJa, self.imgsJa, self.img_action_label)
            if which == 'viewMode' and self.showOrHidden == 'show':  # 뷰모드이면서 동시에 보임상태라면...
                POA_label_show()
                pass  # poa를 보여주면 된다. 이걸로 끝
            else:  # 보기모드가 아니라면 시험모드다. 하지만 첫페이즈를 제외한 경우에는 보여야한다.
                if which == 'viewMode' and self.viewPhase == 0:  # 뷰모드이면서 동시에 첫페이즈라면...
                    self.img_person_label.setText('단계별확인 클릭으로 확인')
                    self.img_object_label.setText('단계별확인 클릭으로 확인')
                    self.img_action_label.setText('단계별확인 클릭으로 확인')
                else:  # 두번째 페이즈부터는 이미 초성이 보이는 상태니 poa이미지도 걍 노출한다.
                    POA_label_show()
            self.viewPOA_show_number()
            self.POA_number.clearFocus()  # 입력창의 자판입력 대기 상태를 해제
            self.word_edit.clearFocus()

    ### 좌하단 작업창의 수치와 버튼들

    # 하단의 p o a 이미지표기 패널의 이미지 수와 현재페이지 표기 패널에 값 입력.
    # 아래이미지 표기함수 및 아래이미지 다음이전버튼 함수시마다 마지막에 재활용.
    def viewPOA_show_number(self):
        self.view_pageNum_person.setText(str(self.current_page_P + 1) + ' / ' + str(len(self.imgsP)))
        self.view_pageNum_object.setText(str(self.current_page_O + 1) + ' / ' + str(len(self.imgsO)))
        if str(self.word_type) in ['3', '5', '6']:
            self.view_pageNum_action.setText(str(self.current_page_A + 1) + ' / ' + str(len(self.imgsTa)))
        elif str(self.word_type) in ['4', '2']:
            self.view_pageNum_action.setText(str(self.current_page_A + 1) + ' / ' + str(len(self.imgsJa)))

    # 하단이미지뷰어의 이미지파일이 있는 폴더 열기
    def openFolder(self, poa):
        if poa == 'person':
            path = self.pathP
        if poa == 'object':
            path = self.pathO
        if poa == 'action':
            if self.word_type in ['3', '5', '6']:
                path = self.pathTa
            else:
                path = self.pathJa
        path = os.path.realpath(path)
        os.startfile(path)

    # 하단의 p o a 이미지표기 패널에서 다음 혹은 이전 버튼을 누른 경우
    def viewPOA_next_pre(self, poa, isnext):
        # 패널에는 people object action 중 하나가, 어느버튼은 true(다음), false 중 하나가 온다.
        # self.imgsP O Ta Ja 중 하나를 택하게 해서 매개변수인 viewPOA에 대입하고 그 길이를 측정.
        if poa == 'person':
            label = self.img_person_label
            self.current_page_poa = self.current_page_P
            viewPOA = self.imgsP
        if poa == 'object':
            label = self.img_object_label
            self.current_page_poa = self.current_page_O
            viewPOA = self.imgsO
        if poa == 'action':
            label = self.img_action_label
            self.current_page_poa = self.current_page_A
            if self.word_type in ['3', '5', '6']:
                viewPOA = self.imgsTa
            else:
                viewPOA = self.imgsJa
        # 고민 : 조건에 따라서 셀프.커런트페이지피오에이 라는 중간변수에 셀프커런트페이지피를 넣는다
        # 그리고 다음버튼일 경우 중간변수를 활용하고 숫자를 +1 시킨다. 하지만 중간변수의 원본은 그대로다...
        # 결국 다시 다음, 이전 버튼을 누르면 그대로인 원본을 중간변수에 덮어서 +1 시킨게 리셋된다.
        # 그래서 무식하게 if 문을 상황별로 추가했지만 깔끔하지가 않다...
        if isnext == 'true':  # 다음버튼신호를 받음
            if not str(len(viewPOA) - 1) == str(self.current_page_poa):  # 매개페이지수와 매개페이지번호가 같지않으면
                self.current_page_poa += 1
                self.showImageWithGif(viewPOA[self.current_page_poa], label)
                if poa == 'person':
                    self.current_page_P += 1
                if poa == 'object':
                    self.current_page_O += 1
                if poa == 'action':
                    self.current_page_A += 1
            else:  # 이미 마지막이라 버튼 씹힘.
                pass
        elif isnext == 'false':  # 이전버튼신호를 받음.
            print('이전버튼신호 확인')
            print('이값은 1이여야하는데 값이' + str(self.current_page_poa))  # 0이 나온다. 어딘가에서 초기화가 되고있다.
            ### 뷰리스트함수의 과정에서 변수가 초기화되는 과정이 있다...시발...뷰리스트가 제일 문제구만
            if not str(self.current_page_poa) == '0':
                self.current_page_poa -= 1
                print(self.current_page_poa)
                self.showImageWithGif(viewPOA[self.current_page_poa], label)
                if poa == 'person':
                    self.current_page_P -= 1
                if poa == 'object':
                    self.current_page_O -= 1
                if poa == 'action':
                    self.current_page_A -= 1
            pass
        self.viewPOA_show_number()

    # 하단이미지를 새창에서 보기
    def viewNewWindow(self, poa):
        if poa == 'person':
            filePath = self.imgsP[self.current_page_P]
        if poa == 'object':
            filePath = self.imgsO[self.current_page_O]
        if poa == 'action':
            if self.word_type in ['3', '5', '6']:
                filePath = self.imgsTa[self.current_page_A]
            else:
                filePath = self.imgsJa[self.current_page_A]
        if self.window_imgae_poa is None:  # 창이 없는 상태면 창이 뜬다.
            self.window_imgae_poa = NewImageWinidow(filePath)
            self.window_imgae_poa.show()

        else:  # 이미 창이 뜬 상태에서 다시 누르면 닫힌다.
            self.window_imgae_poa.close()
            self.window_imgae_poa = None
        # self.imgsP[self.current_page_P]
        # self.imgsO[self.current_page_O]
        # self.imgsTa[self.current_page_A]
        # self.imgsJa[self.current_page_poa]



app = QApplication(sys.argv)
# 앱을 만든다 = 어플리케이션을 실행할.
mainWindow = WindowClass()
# 메인윈도우 실행
mainWindow.showMaximized()  # 화면가득차게 띄우기
mainWindow.show()
# 메인윈도우 보여줌.
app.exec_()
# 위에서 만들고 선언한 앱을 실행
