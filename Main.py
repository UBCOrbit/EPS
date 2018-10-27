#This is the main
#Created on Oct 10, 2018
#This is the main
# import sys
#
# #Enter the season (Summer, Winter, Fall, Spring)
# print sys.argv[1]
#
# #Enter the Location
#     #Northern hemisphere bright as NHB
#     #Northern hemisphere dark as NHD
#     #Southern hemisphere bright as SHB
#     #Southern hemisphere dark as SHD
# print sys.argv[2]
#
# if (sys.argv[2] == NHB)

import sys
from PyQt4 import QtGui

def window():
   app = QtGui.QApplication(sys.argv)
   w = QtGui.QWidget()
   b = QtGui.QLabel(w)
   b.setText("Hello World!")
   w.setGeometry(100,100,200,50)
   b.move(50,20)
   w.setWindowTitle("PyQt")
   w.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   window()
