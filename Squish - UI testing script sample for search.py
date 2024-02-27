# -*- coding: utf-8 -*-

import names
import folder_config as fc
import os
import time

def main():
    # Handling of crash which locks the AUT from the previous test run
    try:
        os.system("taskkill /f /im SASx.exe")
    except:
        ""
    time.sleep(1)
    startApplication("SASx", "", -1, 120) # 2 minutes timeout
    #Handling of minimized SAS4 windows
    try:
        setWindowState(waitForObject(names.sASMainWindow_CSASMainWindow), WindowState.Maximize)
    except:
        ""
    clickButton(waitForObject(names.sASMainWindow_Preferences_QToolButton))
    clickButton(waitForObject(names.preferencesDialog_RestoreBtn_QPushButton))
    clickButton(waitForObject(names.sAS4_Protocol_Suite_OK_QPushButton))
    clickButton(waitForObject(names.preferencesDialog_OKBtn_QPushButton))
    clickButton(waitForObject(names.sASMainWindow_OpenFile_QToolButton))
    type(waitForObject(names.fileNameEdit_QLineEdit), fc.getExampleFolder() + r"\Traces\24G repeated pattern with FEC.sxt")
    clickButton(waitForObject(names.qFileDialog_Open_QPushButton))
    clickButton(waitForObject(names.sASMainWindow_Find_QToolButton))
    clickButton(waitForObject(names.o_AutoSuggestionSearchFilterButton_QPushButton))
    try:
        sendEvent("QMoveEvent", waitForObject(names.cSearchDialog_CSASSearchDialog), 428, 234, 816, 251)
    except:
        ""
    time.sleep(0.5)
    mouseClick(waitForObjectItem(names.cSearchDialog_FilterLineEdit_CMatchTreeView, "Address"), 40, 6, Qt.NoModifier, Qt.LeftButton)
    time.sleep(0.2)
    type(waitForObject(names.cSearchDialog_FilterLineEdit_CMatchTreeView), "<Right>") #Per Mehdi request
    time.sleep(0.2)
    mouseClick(waitForObjectItem(names.cSearchDialog_FilterLineEdit_CMatchTreeView, "Address.All"), -10, 9, Qt.NoModifier, Qt.LeftButton)
    dragAndDrop(waitForObject(names.all_5000c500591c0235_QModelIndex_2), 70, 6, names.cSearchDialog_CFieldsMatchTreeView, 186, 69, Qt.CopyAction)
    clickButton(waitForObject(names.groupBoxFrom_radioButtonStart_QRadioButton_2))
    clickButton(waitForObject(names.cSearchDialog_RoundedFindPushButton_QPushButton))
    mouseClick(waitForObjectItem(names.cSearchDialog_CFieldsMatchTreeView, "Address.All.5000c500591c0235"), 62, 3, Qt.NoModifier, Qt.LeftButton)
    #clickButton(waitForObject(names.mainWindowSplitter_RoundedPushButton_QPushButton_2))
    dragAndDrop(waitForObject(names.all_5000e85000000010_QModelIndex_2), 49, 10, names.cSearchDialog_CFieldsMatchTreeView, 235, 75, Qt.CopyAction)
    clickButton(waitForObject(names.groupBoxFrom_radioButtonStart_QRadioButton_2))
    clickButton(waitForObject(names.cSearchDialog_RoundedFindPushButton_QPushButton))
    mouseClick(waitForObjectItem(names.cSearchDialog_CFieldsMatchTreeView, "Address.All.5000e85000000010"), 42, 12, Qt.NoModifier, Qt.LeftButton)
    #clickButton(waitForObject(names.mainWindowSplitter_RoundedPushButton_QPushButton_2))
    dragAndDrop(waitForObject(names.all_5000e85000000100_QModelIndex_2), 77, 7, names.cSearchDialog_CFieldsMatchTreeView, 117, 176, Qt.CopyAction)
    clickButton(waitForObject(names.groupBoxFrom_radioButtonStart_QRadioButton_2))
    clickButton(waitForObject(names.cSearchDialog_RoundedFindPushButton_QPushButton))
    test.compare(waitForObjectExists(names.tableWidget_0_5_QModelIndex_2).text, "5000e85000000100")
    time.sleep(0.5)
    test.compare(waitForObjectExists(names.tableWidget_0_5_QModelIndex_2).row, 0)
    test.compare(waitForObjectExists(names.tableWidget_0_5_QModelIndex_2).column, 5)
    #clickButton(waitForObject(names.mainWindowSplitter_RoundedPushButton_QPushButton))
    # activateItem(waitForObjectItem(names.sASMainWindow_menuBar_QMenuBar, "File")) #for Jenkins
    # activateItem(waitForObjectItem(names.sASMainWindow_menuFile_QMenu, "Close Trace")) #for Jenkins
