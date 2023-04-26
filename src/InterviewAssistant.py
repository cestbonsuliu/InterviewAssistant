import sys
import os
import random
import datetime

from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QDesktopWidget,QFileDialog,QLineEdit
from PyQt5 import QtCore, QtGui, QtMultimedia
from PyQt5.QtCore import QThread, pyqtSignal

from Gui import InterviewAssistantGui
import parse_interview_questions




# 设置面试题路径
def setFilePath(mainUi,Ui):

    # 弹出文件选择框
    filename, _ = QFileDialog.getOpenFileName(mainUi, '选择文件', '.', 'Text Files (*.md)')

    print(filename)

    if filename:
        Ui.lineEdit_3.setText(filename)


# 设置录音保存路径
def setSaveRecordPath(mainUi):

    # 弹出文件选择框
    fname = QFileDialog.getExistingDirectory(mainUi, '选择文件夹')

    print(fname)

    if fname:
        # 将选中的文件夹路径显示在LineEdit上
        mainUi.findChild(QLineEdit,"lineEdit_2").setText(fname)



# 获取面试题
def selectRandomQuestion(Ui):

    # 获取面试题路径
    path = Ui.lineEdit_3.text()

    if os.path.exists(path):

        try:
            # 获取问题对字典列表
            question_answer_list = parse_interview_questions.parse_markdown_file(path)
            print(question_answer_list)
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setText("读取文件失败")
            msgBox.exec_()

        # 随机获取一个问题
        random_question = random.choice(question_answer_list)
        question = random_question['question']
        print(question)

        Ui.lineEdit.setText(question)

        # 更改出题按钮
        if Ui.lineEdit.text() != "问题":
            Ui.pushButton.setText("下一题")

    else:
        msgBox = QMessageBox()
        msgBox.setText("选择的题库文件不合法!")
        msgBox.exec_()




# 获取面试题答案
def getAnswer(Ui):

    path = Ui.lineEdit_3.text()
    question = Ui.lineEdit.text()

    if os.path.exists(path) and question != "问题":

        try:
            question_answer_list = parse_interview_questions.parse_markdown_file(path)
            print(question_answer_list)
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setText("读取文件失败")
            msgBox.exec_()

        # 获取问题获取问题答案字典元素
        answer_dict = [qa for qa in question_answer_list if qa.get("question") == question][0]
        answer = answer_dict.get("answer")
        print(answer)

        Ui.textEdit.setText(answer)

    else:
        msgBox = QMessageBox()
        msgBox.setText("没有问题!")
        msgBox.exec_()

# 开始录音
def startRecording(Ui,AudioRecorder):

    question = Ui.lineEdit.text()
    date  = datetime.date.today()
    now = datetime.datetime.now()

    if question != "问题":

        # 配置录音设置
        audioSettings = QtMultimedia.QAudioEncoderSettings()
        audioSettings.setCodec("audio/amr")  # 设置编码格式
        audioSettings.setQuality(QtMultimedia.QMultimedia.NormalQuality)  # 设置音质
        AudioRecorder.setEncodingSettings(audioSettings)

        # 设置录音保存位置
        recording_path = Ui.lineEdit_2.text()
        if recording_path:
            outputPath = os.path.join(recording_path, f'{question}-{date}-{now.hour}-{now.minute}')
        else:
            #设置默认位置
            if not os.path.isdir("../Recordings/"):
                os.makedirs("../Recordings/")
            recordings = os.path.abspath("../Recordings/")
            outputPath = os.path.join(recordings, f'{question}-{date}-{now.hour}-{now.minute}')
        print(outputPath)
        AudioRecorder.setOutputLocation(QtCore.QUrl.fromLocalFile(outputPath))

        # 开始录音
        AudioRecorder.record()

        # 更新按钮状态
        Ui.pushButton_2.setText("正在录音")
        Ui.pushButton_2.setEnabled(False)
        Ui.pushButton_3.setEnabled(True)

    else:
        msgBox = QMessageBox()
        msgBox.setText("没有问题!")
        msgBox.exec_()

# 停止录音
def stopRecording(Ui,AudioRecorder):

    if Ui.lineEdit.text() != "问题":

        AudioRecorder.stop()

        # 更新按钮状态
        Ui.pushButton_2.setText("开始答题")
        Ui.pushButton_2.setEnabled(True)
        Ui.pushButton_3.setEnabled(False)
    else:
        msgBox = QMessageBox()
        msgBox.setText("没有问题!")
        msgBox.exec_()

if __name__ == '__main__':
    # 解决QTDesigner界面开发时预览和实际运行效果不同
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()

    ui = InterviewAssistantGui.Ui_MainWindow()
    # 向主窗口上添加控件
    ui.setupUi(mainWindow)


    ui.pushButton_8.clicked.connect(lambda: setFilePath(mainWindow,ui))
    ui.pushButton_7.clicked.connect(lambda: setSaveRecordPath(mainWindow))
    ui.pushButton.clicked.connect(lambda: selectRandomQuestion(ui))
    ui.pushButton_4.clicked.connect(lambda: getAnswer(ui))

    audioRecorder = QtMultimedia.QAudioRecorder()
    ui.pushButton_3.setEnabled(False)
    ui.pushButton_2.clicked.connect(lambda: startRecording(ui,audioRecorder))
    ui.pushButton_3.clicked.connect(lambda: stopRecording(ui,audioRecorder))




    # 让窗口在屏幕中央显示,因为使用了win11状态栏透明工具,所以向上移动了30px
    screen = QDesktopWidget().screenGeometry()
    size = mainWindow.geometry()
    mainWindow.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2 - 30)

    mainWindow.show()
    sys.exit(app.exec_())