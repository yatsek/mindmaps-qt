 import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from math import log10
class Form(QDialog):
    def __init__(self,parent=None):
        super(Form, self).__init__(parent)
        self.principal = QDoubleSpinBox()
        self.principal.setPrefix("$ ")
        self.principal.setMaximum(999999999)
        self.rate = QDoubleSpinBox()
        self.rate.setSuffix("%")
        self.amount = QLabel("$ ")
        def populate_combo():
            temp=QComboBox()
            x=1
            for x in range(1,5):
                temp.addItem("%s years"%x)
            return temp
        self.years=populate_combo()
        def init_grid():
            grid = QGridLayout()
            grid.addWidget(QLabel('Principal'),0,0)
            grid.addWidget(QLabel("Rate"),1,0)
            grid.addWidget(self.principal,0,1)
            grid.addWidget(self.rate,1,1)
            grid.addWidget(QLabel("Years"),2,0)
            grid.addWidget(self.years,2,1)
            grid.addWidget(self.amount,3,0)
            return grid
        self.setLayout(init_grid())
        self.connect(self.principal, SIGNAL("valueChanged(double)"),self.changeStep)
        self.connect(self.principal, SIGNAL("valueChanged(double)"),self.updateUI)
        self.connect(self.rate, SIGNAL("valueChanged(double)"),self.updateUI)
        self.connect(self.years, SIGNAL("currentIndexChanged(int)"), self.updateUI)
    def updateUI(self):
        calc = lambda princ,rate,years: str(princ*((1+(rate/100.0)**years)))
        val=calc(self.principal.value(),self.rate.value(),self.years.currentIndex()+1)
        self.amount.setText(val)
        
    def changeStep(self):
        #adjust step of principal qdoublespinbox
        try:
            if self.principal.value() < 2 :
                return
            zeros=lambda x: 10**int(log10(x)-1)
            self.principal.setSingleStep(zeros(self.principal.value()))
        except:
            pass
app = QApplication(sys.argv)
form=Form()
form.show()
app.exec_()