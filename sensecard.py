import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from senseui import *
from multiprocessing import Process
from flaskWebServer import *

import json

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)        
        self.setupUi(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(True)
        self._server_started= False
        self._config = self.ReadConfig()        
        self.dispalyRules()        
        self.pushButton_3.setDisabled(True)        
    
    def dispalyRules(self):
        self.lineEdit.setText(self._config['url'])
        self.lineEdit_2.setText(str(self._config['senseport']))
        self.lineEdit_3.setText(self._config['senseip'])
        rules = self._config['rules']
        count = len(rules)
        self.tableWidget.setRowCount(count+1)
        for i, key in enumerate(rules):
            it0 = QtWidgets.QTableWidgetItem(key)
            it1 = QtWidgets.QTableWidgetItem(rules[key])
            self.tableWidget.setItem(i,0,it0)
            self.tableWidget.setItem(i,1,it1)
        #last line should remain blank
        blank0 = QtWidgets.QTableWidgetItem('')
        blank1 = QtWidgets.QTableWidgetItem('')
        self.tableWidget.setItem(count,0,blank0)
        self.tableWidget.setItem(count,1,blank1)


    def StartServer(self):
        if self._server_started== False :
            self._webServer = WebServer( host= self._config['senseip'] ,port=self._config['senseport'])
            self._webServer.setConfig(self._config)
            self._webServer.process()
            self._server_started= True
            self.pushButton.setDisabled(True)
            self.pushButton_2.setDisabled(True)
            self.pushButton_3.setDisabled(False)


    def CloseServer(self):
        if self._server_started== True :
            self._webServer.close()
            self._server_started= False
            self.pushButton.setDisabled(False)
            self.pushButton_2.setDisabled(False)
            self.pushButton_3.setDisabled(True)


    def UpdateConfig(self):
        self._config['url'] = self.lineEdit.text()
        self._config['senseport'] = int(self.lineEdit_2.text())
        self._config['senseip'] = self.lineEdit_3.text()
        newRules = {}
        rowcount = self.tableWidget.rowCount()
        for i in range(rowcount):
            if self.tableWidget.item(i,0) != None and self.tableWidget.item(i,0) !=None:
                if  len( self.tableWidget.item(i,0).text() ) == 0 or len( self.tableWidget.item(i,1).text() ) == 0:
                    continue
                newRules[self.tableWidget.item(i,0).text()] = self.tableWidget.item(i,1).text()

        self._config['rules'] =  newRules
        self.dispalyRules()
        #print(self._config)
        with open("config.json","w") as f:
            json.dump(self._config,f)

    
    def ReadConfig(self):
        with open("config.json", 'r') as f:
            temp = json.loads(f.read())            
            return temp

    # def __del__( self ):
    #     self._webServer.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())