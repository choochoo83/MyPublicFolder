# -*- coding: utf-8 -*-

import names
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
    clickButton(waitForObject(names.sASMainWindow_Preferences_QToolButton))
    clickButton(waitForObject(names.preferencesDialog_RestoreBtn_QPushButton))
    clickButton(waitForObject(names.sAS4_Protocol_Suite_OK_QPushButton))
    clickButton(waitForObject(names.preferencesDialog_OKBtn_QPushButton))
    activateItem(waitForObjectItem(names.sASMainWindow_menuBar_QMenuBar, "Setup"))
    activateItem(waitForObjectItem(names.sASMainWindow_menuSetup_QMenu, "Device Management"))
    
    time.sleep(15)
    SerialNumber = 16820 #M244
    if str(waitForObjectExists(names.o0_0_QModelIndex).text) == "SierraSAS M244 : " + str(SerialNumber): 
        mouseClick(waitForObjectItem(names.cDeviceManagementDlg_CDeviceProductTableView, "0/0"), 5, 11, Qt.NoModifier, Qt.LeftButton) #select from row 0
    elif str(waitForObjectExists(names.o1_0_QModelIndex).text) == "SierraSAS M244 : " + str(SerialNumber):
        mouseClick(waitForObjectItem(names.cDeviceManagementDlg_CDeviceProductTableView, "1/0"), 5, 11, Qt.NoModifier, Qt.LeftButton) #select from row 1
    elif str(waitForObjectExists(names.o2_0_QModelIndex).text) == "SierraSAS M244 : " + str(SerialNumber):
        mouseClick(waitForObjectItem(names.cDeviceManagementDlg_CDeviceProductTableView, "2/0"), 5, 11, Qt.NoModifier, Qt.LeftButton) #select from row 2
    elif str(waitForObjectExists(names.o3_0_QModelIndex).text) == "SierraSAS M244 : " + str(SerialNumber):
        mouseClick(waitForObjectItem(names.cDeviceManagementDlg_CDeviceProductTableView, "3/0"), 5, 11, Qt.NoModifier, Qt.LeftButton) #select from row 3
    elif str(waitForObjectExists(names.o4_0_QModelIndex).text) == "SierraSAS M244 : " + str(SerialNumber):
        mouseClick(waitForObjectItem(names.cDeviceManagementDlg_CDeviceProductTableView, "4/0"), 5, 11, Qt.NoModifier, Qt.LeftButton) #select from row 4
    elif str(waitForObjectExists(names.o5_0_QModelIndex).text) == "SierraSAS M244 : " + str(SerialNumber):
        mouseClick(waitForObjectItem(names.cDeviceManagementDlg_CDeviceProductTableView, "5/0"), 5, 11, Qt.NoModifier, Qt.LeftButton) #select from row 5
    elif str(waitForObjectExists(names.o6_0_QModelIndex).text) == "SierraSAS M244 : " + str(SerialNumber):
        mouseClick(waitForObjectItem(names.cDeviceManagementDlg_CDeviceProductTableView, "6/0"), 5, 11, Qt.NoModifier, Qt.LeftButton) #select from row 6
    elif str(waitForObjectExists(names.o7_0_QModelIndex).text) == "SierraSAS M244 : " + str(SerialNumber):
        mouseClick(waitForObjectItem(names.cDeviceManagementDlg_CDeviceProductTableView, "7/0"), 5, 11, Qt.NoModifier, Qt.LeftButton) #select from row 7
    clickButton(waitForObject(names.cDeviceManagementDlg_ConnectBtn_QPushButton)) #connect
    try:
        clickButton(waitForObject(names.no_QPushButton)) #handling of aborting the last bad running session
    except:
        ""
    time.sleep(5)
    clickButton(waitForObject(names.cDeviceManagementDlg_CloseBtn_QPushButton)) #close

    # copy the PG files
    import folder_config as fc
    fc.makePGReady(os.getcwd() + r"\STP_24.ppf", os.getcwd() + r"\PG_SAS24.txt")

    ### open trigger project
    clickButton(waitForObject(names.sASMainWindow_OpenFile_QToolButton))
    type(waitForObject(names.fileNameEdit_QLineEdit), os.getcwd() + "\\trigger_command_identify_device.sxp")
    clickButton(waitForObject(names.qFileDialog_Open_QPushButton))
    # assign    
    openContextMenu(waitForObject(names.projectViewTransparentWidget_M244_QLabel_2), 28, 0, Qt.NoModifier)
    mouseClick(waitForObject(names.projectViewTransparentWidget_SierraSAS_M244_16820_16820_QLabel), 89, 16, Qt.NoModifier, Qt.LeftButton) #select board
    # 7.90 transceiver setting update
    try:
        clickButton(waitForObject(names.yes_QPushButton))
    except:
        pass
    time.sleep(20)



    ### set trace file name according to the trigger test
    sendEvent("QMouseEvent", waitForObject(names.projectViewTransparentWidget_SliderManagerButton_CPrjBufferSizeSliderWidget), QEvent.MouseButtonPress, 123, 11, Qt.LeftButton, 1, 0)
    type(waitForObject(names.cSASRecordSettingDlg_lineEditTarcePath_QLineEdit), "<Ctrl+A>") #improvement for Mehdi
    time.sleep(1)
    from datetime import datetime
    type(waitForObject(names.cSASRecordSettingDlg_lineEditTarcePath_QLineEdit), os.getcwd() + "\\Squish_trigger_command_identify_device_" + datetime.now().strftime('%H%M%S') + ".sxt")
    clickButton(waitForObject(names.cSASRecordSettingDlg_RoundedPushButton_QPushButton))
    # recording
    clickButton(waitForObject(names.projectViewTransparentWidget_ProjectPushButton_QPushButton))
    time.sleep(10)


    # Go to trigger - 8.20
    mouseClick(waitForObjectItem(names.table_View_TableWidget_CSASSpreadSheetWidget, "4/0"), 29, 8, Qt.NoModifier, Qt.LeftButton)
    clickButton(waitForObject(names.sASMainWindow_GotoTrigger_QToolButton))
    time.sleep(0.5)

    
    ### verification the relevant trigger pattern
    test.compare(waitForObjectExists(names.tableWidget_0_9_QModelIndex).column, 9)
    test.compare(waitForObjectExists(names.tableWidget_0_9_QModelIndex).text, "0xEC:Identify Device ; Status=Normal Output")
    test.compare(waitForObjectExists(names.tableWidget_0_9_QModelIndex).row, 0)
    # save trace and close project
    activateItem(waitForObjectItem(names.sASMainWindow_menuBar_QMenuBar, "File"))
    time.sleep(0.5)
    activateItem(waitForObjectItem(names.sASMainWindow_menuFile_QMenu, "Save Trace"))
    time.sleep(10)
    activateItem(waitForObjectItem(names.sASMainWindow_menuBar_QMenuBar, "File"))
    time.sleep(0.5)
    activateItem(waitForObjectItem(names.sASMainWindow_menuFile_QMenu, "Close Project"))
    time.sleep(0.5)
    clickButton(waitForObject(names.sAS4_Protocol_Suite_Discard_QPushButton))
    time.sleep(0.5)