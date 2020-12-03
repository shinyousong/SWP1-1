from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QTextEdit, QLineEdit, QComboBox, QToolButton
import pickle
import datetime

class Calendar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 저장소 할당
        # 기본 5개
        self.dailyRoutineSave = []
        self.weeklyRoutineSave = []
        self.daySave = []
        self.weekSave = []
        self.etcSave = []
        # 기본 5개 통합저장소
        self.allSave = []

        # Routine del 기능을 위한 저장소
        self.dailyRoutineTemSave = []
        self.weeklyRoutineTemSave = []

        # 저장소들을 종류별로 List에 넣음
        self.saveList = [self.dailyRoutineSave, self.weeklyRoutineSave, self.daySave, self.weekSave, self.etcSave, self.allSave]
        self.temSaveList = [self.dailyRoutineTemSave, self.weeklyRoutineTemSave]

        # 저장 파일에서 일정을 읽어와 저장
        self.fileName = ["daily.txt", "weekly.txt", "day.txt", "week.txt", "etc.txt", "all.txt"]
        for i in range(0, len(self.saveList)):
            openedFile = open(self.fileName[i], 'rb')
            self.saveList[i] = pickle.load(openedFile)
            openedFile.close

        # 날짜 파일에서 기준 날짜를 읽어옴
        self.dateFileName = "date.txt"
        openedFile = open(self.dateFileName, 'rb')
        standarddate = pickle.load(openedFile)
        openedFile.close

        # 기준일로부터 하루 이상 지났을 시 기준일 업데이트하고 daily_routine 업데이트, 현재는 하루에 한번 프로그램 열람 가정
        self.temFileName = ["daily_routine.txt", "weekly_routine.txt"]
        if datetime.datetime.today() >= standarddate[0] + datetime.timedelta(days = 1):
            openedFile = open(self.fileName[0], 'rb')
            self.temSaveList[0] = pickle.load(openedFile)
            openedFile.close

            standarddate[0] = standarddate[0] + datetime.timedelta(days = 1)
            openedFile = open(self.dateFileName, 'wb')
            pickle.dump(standarddate, openedFile)
            openedFile.close
        else: # 기준일이 지나지 않았으면 업데이트하지 않음
            openedFile = open(self.temFileName[0], 'rb')
            self.temSaveList[0] = pickle.load(openedFile)
            openedFile.close
        # 기준일로부터 일주일 이상 지났을 시 기준일 업데이트하고 daily_routine 업데이트
        if datetime.datetime.today() >= standarddate[1]+datetime.timedelta(days = 7):
            openedFile = open(self.fileName[1], 'rb')
            self.temSaveList[1] = pickle.load(openedFile)
            openedFile.close

            standarddate[1] = standarddate[1] + datetime.timedelta(days = 7)
            openedFile = open(self.dateFileName, 'wb')
            pickle.dump(standarddate, openedFile)
            openedFile.close
        else: # 기준일이 지나지 않았으면 업데이트하지 않음
            openedFile = open(self.temFileName[1], 'rb')
            self.temSaveList[1] = pickle.load(openedFile)
            openedFile.close

        # UI생성
        # 일정 출력 Layout 생성
        windowLayout = QGridLayout()

        self.calendarWindow = QTextEdit()
        self.calendarWindow.setReadOnly(True)
        self.calendarWindow.setAlignment(Qt.AlignLeft)
        windowLayout.addWidget(self.calendarWindow, 0, 0) # UI 배치
        # 일정 출력 Layout 설정 완료
        
        # 기눙 관련 Layout 생성
        functionLayout = QGridLayout()

        self.dateComboBox = QComboBox() # 날짜 관련 속성박스
        self.dateComboBox.addItems(["daily routine", "weekly routine", "day", "week", "etc", "all"])
        functionLayout.addWidget(self.dateComboBox, 0, 0, 1, 2) # UI 배치

        self.sortComboBox = QComboBox() # 정렬 관련 속성박스
        self.sortComboBox.addItems(["fast day", "most important"])
        functionLayout.addWidget(self.sortComboBox, 1, 0, 1, 2) # UI 배치

        self.saveButton = QToolButton() # Save 버튼
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.ButtonClicked)
        functionLayout.addWidget(self.saveButton, 2, 0, 1, 2) # UI 배치

        self.editButton = QToolButton() # Edit 버튼
        self.editButton.setText("Edit")
        self.editButton.clicked.connect(self.ButtonClicked)
        functionLayout.addWidget(self.editButton, 3, 0, 1, 2) # UI 배치

        self.delButton = QToolButton() # Del 버튼
        self.delButton.setText("Del")
        self.delButton.clicked.connect(self.ButtonClicked)
        functionLayout.addWidget(self.delButton, 4, 0) # UI 배치

        self.routineDelButton = QToolButton() # Routine Del 버튼
        self.routineDelButton.setText("Routine Del")
        self.routineDelButton.clicked.connect(self.ButtonClicked)
        functionLayout.addWidget(self.routineDelButton, 4, 1) # UI 배치

        self.ShowButton = QToolButton() # Show 버튼
        self.ShowButton.setText("Show")
        self.ShowButton.clicked.connect(self.ButtonClicked)
        functionLayout.addWidget(self.ShowButton, 5, 0, 1, 1) # UI 배치

        self.showDetailButton = QToolButton() # ShowDetail 버튼
        self.showDetailButton.setText("Show Detail")
        self.showDetailButton.clicked.connect(self.ButtonClicked)
        functionLayout.addWidget(self.showDetailButton, 5, 1, 1, 1) # UI 배치
        # 기능 관련 Layout 설정 완료

        # 정보입력 관련 Layout 생성
        inforLayout = QGridLayout()

        nameLabel = QLabel("name:")
        monthLabel = QLabel("month:")
        dayLabel = QLabel("day:")
        importantLabel = QLabel("important:")
        self.nameLineEdit = QLineEdit()
        self.monthLineEdit = QLineEdit()
        self.dayLineEdit = QLineEdit()
        self.importantLineEdit = QLineEdit()
        inforLayout.addWidget(nameLabel, 0, 0)
        inforLayout.addWidget(self.nameLineEdit, 0, 1, 1, 2)
        inforLayout.addWidget(monthLabel, 1, 0)
        inforLayout.addWidget(self.monthLineEdit, 1, 1)
        inforLayout.addWidget(dayLabel, 2, 0)
        inforLayout.addWidget(self.dayLineEdit, 2, 1)
        inforLayout.addWidget(importantLabel, 3, 0)
        inforLayout.addWidget(self.importantLineEdit, 3, 1)
        # 정보입력 관련 Layout 설정 완료
        
        # 세부사항 입력 Layout 생성
        detailLayout = QGridLayout()

        detailLabel = QLabel("detail:")
        self.detailTextEdit = QTextEdit()
        inforLayout.addWidget(detailLabel, 0, 3)
        detailLayout.addWidget(self.detailTextEdit, 0, 4)
        # 세부사항 입력 Layout 설정 완료
        
        # 통합 Layout 생성
        mainLayout = QGridLayout()
        
        mainLayout.addLayout(windowLayout, 0, 0, 2, 4)
        mainLayout.addLayout(functionLayout, 0, 4, 2, 1)
        mainLayout.addLayout(inforLayout, 2, 0, 1, 2)
        mainLayout.addLayout(detailLayout, 2, 2, 1, 3)
        # 통합 Layout 설정 완료
        
        # 시작
        self.setLayout(mainLayout)
        self.setWindowTitle("Calendar")

    def closeEvent(self, event):
        self.saveData()

    def saveData(self):
        for i in range(0, len(self.saveList)):
            openedFile = open(self.fileName[i], 'wb')
            pickle.dump(self.saveList[i], openedFile)
            openedFile.close()
        for i in range(0, len(self.temSaveList)):
            openedFile = open(self.temFileName[i], 'wb')
            pickle.dump(self.temSaveList[i], openedFile)
            openedFile.close()
        #기준일 정립을 위한 최초 1회 시행 코드, 이후 주석
        """
        standardtime_day = datetime.datetime(2020, 11,30)
        standardtime_week = datetime.datetime(2020, 11, 30)
        standardtime = []
        standardtime.append(standardtime_day)
        standardtime.append(standardtime_week)
        dateFile = open(self.dateFileName, 'wb')
        pickle.dump(standardtime, dateFile)
        dateFile.close()
        """

    def comboBoxKeyDivision(self, lst): # 날짜 관련 속성박스 값에 따라 인자로 받아온 정보 list를 다른 Save에 저장하는 함수|정보 list 형태 =[[이름, 월, 일, 중요도], [세부]]
        key = self.dateComboBox.currentText()
        validKeys = ["daily routine", "weekly routine", "day", "week", "etc"] # all 제외
        for i in range(0, len(validKeys)):
            if validKeys[i] == key: # 저장소 확인
                # 1. 중복삭제
                for j in range(0, len(self.saveList[i])): # 기존과 중복되는 이름이 있으면 삭제
                    if self.saveList[i][j][0][0] == lst[0][0]:
                        del self.saveList[i][j] # 일반저장소 중복값 삭제
                        for k in range(0, len(self.saveList[5])): # all 저장소 중복값 삭제
                            if self.saveList[5][k][0][0] == lst[0][0]:
                                del self.saveList[5][k]
                                break
                        if i == 0: # daily routine 저장소 중복값 삭제
                            try: # routine del 시 없을 수 있음
                                del self.temSaveList[i][j]
                            except: # 없으면 아무것도 하지 않음
                                pass
                        if i == 1: # weekly routine 저장소 중복값 삭제
                            try: # routine del 시 없을 수 있음
                                del self.temSaveList[i][j]
                            except: # 없으면 아무것도 하지 않음
                                pass
                        break
                # 2. 저장
                self.saveList[i].append(lst) # 일반 저장소 저장
                self.saveList[5].append(lst) # all 저장소 저장
                if i == 0: # daily routine일 시, routine 저장소에도 저장
                    self.temSaveList[0].append(lst)
                if i == 1: # weekly routine일 시, routine 저장소에도 저장
                    self.temSaveList[1].append(lst)

    def comboBoxKeyShow(self): # 날짜, 정렬 관련 속성박스 값에 따라 Calendar 화면을 업데이트함
        self.calendarWindow.clear()
        key_date = self.dateComboBox.currentText()
        key_sort = self.sortComboBox.currentText()
        temList_forsort = []
        validKeys_date = ["daily routine", "weekly routine", "day", "week", "etc", "all"] # all 포함
        for i in range(0, len(validKeys_date)):
            if validKeys_date[i] == key_date: # 저장소 확인
                # 1. 정렬
                if i <= 1:
                    for j in range(0, len(self.temSaveList[i])):  # 정렬을 위한 임시 리스트로 옮김
                        temList_forsort.append(self.temSaveList[i][j])
                else:
                    for j in range(0, len(self.saveList[i])): # 정렬을 위한 임시 리스트로 옮김
                        temList_forsort.append(self.saveList[i][j])

                for k in range(0, len(temList_forsort)): #버블정렬
                    for l in range(0, len(temList_forsort)-1):
                        if key_sort == "fast day": #정렬기준
                            if int(temList_forsort[l][0][1]) * 31 + int(temList_forsort[l][0][2]) > int(temList_forsort[l+1][0][1]) * 31 + int(temList_forsort[l+1][0][2]): # 달, 일을 종합적으로 따져서 정렬
                                temList_forsort[l], temList_forsort[l+1] = temList_forsort[l+1], temList_forsort[l]
                        if key_sort == "most important": #정렬기준
                            if int(temList_forsort[l][0][3]) < int(temList_forsort[l+1][0][3]): # 중요도를 따져 정렬
                                temList_forsort[l], temList_forsort[l+1] = temList_forsort[l+1], temList_forsort[l]
                #2. 출력
                for j in range(0, len(temList_forsort)):
                    work = "이름: " + str(temList_forsort[j][0][0]) + ", 월: " + str(temList_forsort[j][0][1]) + ", 일: " + str(temList_forsort[j][0][2]) + ", 중요도: " + str(temList_forsort[j][0][3])
                    self.calendarWindow.append(work)

    def ButtonClicked(self):
        button = self.sender()
        key = button.text()

        if key == "Save": # save 버튼 클릭 시 관련 정보들 모두 저장
            # LineEdit으로부터 정보들을 얻어옴
            name = self.nameLineEdit.text()

            month = self.monthLineEdit.text()
            if month.isdigit() == False:
                self.detailTextEdit.setText("month must be int")
                return;
            if 1 > int(month) or int(month) > 12:
                self.detailTextEdit.setText("month must be 1~12")
                return;

            day = self.dayLineEdit.text()
            if day.isdigit() == False:
                self.detailTextEdit.setText("day must be int")
                return;
            if 1 > int(day) or int(day) > 31:
                self.detailTextEdit.setText("day must be 1~31")
                return;

            important = self.importantLineEdit.text()
            if important.isdigit() == False:
                self.detailTextEdit.setText("important must be int")
                return;

            detail = self.detailTextEdit.toPlainText()

            # 현재 저장소 제외 모든 일반 저장소들에서 이름 중복 검사
            for i in range(0, 5):
                if ["daily routine", "weekly routine", "day", "week", "etc"][i] == self.dateComboBox.currentText():
                    continue
                for j in range(0, len(self.saveList[i])):
                    if self.saveList[i][j][0][0] == name:
                        self.detailTextEdit.setText("Duplicate name")
                        return;

            # 얻어온 정보들을 저장함
            showInfor = [] # 출력되는 정보
            for infor in [name, month, day, important]:
                showInfor.append(infor)

            nonshowInfor = [] # 출력되지 않는 정보
            nonshowInfor.append(detail)

            infor = [] # 통합 정보
            infor.append(showInfor)
            infor.append(nonshowInfor)

            # 저장 후 Calendar 화면 업데이트
            self.comboBoxKeyDivision(infor)
            self.comboBoxKeyShow()

        if key == "Edit": # edit 버튼 클릭 시 해당 저장소 내 이름이 일치하는 것의 정보를 받아옴
            name = self.nameLineEdit.text()
            key = self.dateComboBox.currentText()
            validKeys = ["daily routine", "weekly routine", "day", "week", "etc"] # all 제외
            for i in range(0, len(validKeys)):
                if validKeys[i] == key: # 키 확인
                    for j in range(0, len(self.saveList[i])):
                        if self.saveList[i][j][0][0] == name: # 이름 일치 시 정보 받아옴
                            self.monthLineEdit.setText(self.saveList[i][j][0][1])
                            self.dayLineEdit.setText(self.saveList[i][j][0][2])
                            self.importantLineEdit.setText(self.saveList[i][j][0][3])
                            self.detailTextEdit.setText(self.saveList[i][j][1][0])

        if key == "Del": # del 버튼 클릭 시 저장소별로 이름이 일치하는 것들을 지움
            name = self.nameLineEdit.text()
            key = self.dateComboBox.currentText()
            validKeys = ["daily routine", "weekly routine", "day", "week", "etc"] # all 제외
            for i in range(0, len(validKeys)):
                if validKeys[i] == key: # 키 확인
                    for j in range(0, len(self.saveList[i])):
                        if self.saveList[i][j][0][0] == name: # 이름 일치 시 삭제
                            del self.saveList[i][j] # 일반저장소 일치값 삭제
                            for k in range(0, len(self.saveList[5])):  # all 저장소 일치값 삭제
                                if self.saveList[5][k][0][0] == name:
                                    del self.saveList[5][k]
                                    break
                            if i == 0:  # daily routine 저장소 일치값 삭제
                                try:
                                    del self.temSaveList[i][j]
                                except:
                                    pass
                            if i == 1:  # weekly routine 저장소 일치값 삭제
                                try:
                                    del self.temSaveList[i][j]
                                except:
                                    pass
                            self.comboBoxKeyShow()
                            break

        if key == "Routine Del": # routine del 버튼 클릭 시 routine 저장소에 있는 것을 보여주기식으로 지움
            name = self.nameLineEdit.text()
            key = self.dateComboBox.currentText()
            validKeys = ["daily routine", "weekly routine"]
            for i in range(0, len(validKeys)):
                if validKeys[i] == key: # 키 확인
                    for j in range(0, len(self.temSaveList[i])):
                        if self.temSaveList[i][j][0][0] == name: # 이름 일치 시 삭제
                            del self.temSaveList[i][j] # 임시저장소값 삭제
                            self.comboBoxKeyShow()
                            break

        if key == "Show": #Show 버튼 클릭 시 모든 것을 보여줌
            self.comboBoxKeyShow()

        if key == "Show Detail": # 이름과 일치하는 Detail값 받아옴
            name = self.nameLineEdit.text()
            key = self.dateComboBox.currentText()
            validKeys = ["daily routine", "weekly routine", "day", "week", "etc", "all"]
            for i in range(0, len(validKeys)):
                if validKeys[i] == key:
                    for j in range(0, len(self.saveList[i])):
                        if self.saveList[i][j][0][0] == name:
                            self.detailTextEdit.setText(self.saveList[i][j][1][0])
            

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    cal = Calendar()
    cal.show()
    cal.comboBoxKeyShow()
    sys.exit(app.exec_())