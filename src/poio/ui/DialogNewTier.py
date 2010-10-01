from PyQt4 import QtCore, QtGui
from Ui_NewTier import Ui_DialogNewTier

class DialogNewTier(QtGui.QDialog):

    def __init__(self, parentTier,  tierType, tierDefaultLocale, tierParticipant,  *args):
        QtGui.QDialog.__init__(self, *args)
        self.ui = Ui_DialogNewTier()
        self.ui.setupUi(self)
        self.ui.labelParentTier.setText(parentTier)
        self.ui.lineeditTierType.setText(tierType)
        self.ui.lineeditParticipant.setText(tierParticipant)
        self.ui.lineeditDefaultLocale.setText(tierDefaultLocale)
        
    def accept(self):
        self.tierType = unicode(self.ui.lineeditTierType.text())
        self.tierId = unicode(self.ui.lineeditTierId.text())
        self.tierDefaultLocale = unicode(self.ui.lineeditDefaultLocale.text())
        self.tierParticipant = unicode(self.ui.lineeditParticipant.text())
        if  self.tierType == '' or self.tierId == '' or self.tierDefaultLocale == '':
            QtGui.QMessageBox.critical(self, "No ID and type", "Please enter an ID, a type and a locale for the tier.", QtGui.QMessageBox.Ok)
        else:
            return QtGui.QDialog.accept(self)
