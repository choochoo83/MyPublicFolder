import SASTestScenario
import os
import threading
import sys
import traceback
import time
import re

class QA_Scenario(SASTestScenario.SASTestScenario):
    def __init__(self):
        self.__Trace = None
        self.__Project = None
        self.__MainTask = None
        self.__IsRunning = threading.Event()
        self.__ResetCallbacks()

    def __del__(self):
        self.Wait()

    def Wait(self):
        if self.__MainTask:
            self.__MainTask.join()

    def __ResetCallbacks(self):
        self.__ResultCallback = None
        self.__ProgressCallback = None
        self.__MessageCallback = None
        self.__TraceCreatedCallback = None

    def __CallResultCallback( self, status ):
        if self.__ResultCallback:
            self.__ResultCallback( status )

    def __CallProgressCallback( self, progress ):
        if self.__ProgressCallback:
            self.__ProgressCallback( progress )

    def __CallMessageCallback( self, msg ):
        if self.__MessageCallback:
            self.__MessageCallback( msg )

    def __CallTraceCreatedCallback( self, trace_path ):
        if self.__TraceCreatedCallback:
            self.__TraceCreatedCallback( trace_path )

    def StartTest(self, params, result_callback, progress_callback, message_callback, trace_created_callback):
        try:
            if self.__MainTask:
                 self.__MainTask.join()

            self.__Trace = None
            self.__Project = None
            self.__MainTask = None

            self.__ResultCallback = result_callback
            self.__ProgressCallback = progress_callback
            self.__MessageCallback = message_callback
            self.__TraceCreatedCallback = trace_created_callback
            self.__Params = params
            self.__ChainIndex = self.__Params["ChainIndex"]
            self.__DeviceIndex = self.__Params["DeviceIndex"]
            self.__Engine = self.__Params["Engine"]
            self.__MainTask = threading.Thread( target = self.__RunWorker )
            self.__MainTask.start()
        except:
            self.CompleteTest( self.__MsgFromException(), SASTestScenario.ETestResult.Failed )

    def __OnVscriptStatus(self, Status):
        global S
        print(Status)
        S = Status

    def __OnVScriptProgress(self, Progress):
        global P
        print(Progress)
        P = Progress

    def __OnLogAppended(self, Log):
       global L
       print(Log)
       L = Log            

    def StopTest( self ):
        self.__IsRunning.clear()

    def __RunWorker(self):
        try:
            with self.__Engine.Locker():


                self.__IsRunning.set()
                test_name = self.__Params["TestName"]
                test_trace = "C:\\Users\\Public\\Documents\\LeCroy\\SAS4 Protocol Suite\\Examples\\Traces\\24G repeated pattern.sxt"
                test_project = self.__Params["ProjectFile"]
                test_vse = self.__Params["VerificationScript"]    
                
                if test_name == "GetVersion":
                    my_version = ""
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    GetVersion = self.__Engine.Api.GetVersion() 
                    my_version = GetVersion.split(".")[0] + "." + GetVersion.split(".")[1]
                    if my_version != "":
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Version = " + str(GetVersion))
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Version = " + str(GetVersion))  

                elif test_name == "GetCount":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    GetCount = self.__Trace.GetCount()
                    self.__Trace.Close()
                    del self.__Trace
                    if GetCount == 12277:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual GetCount = " + str(GetCount) + " against the expected 12277")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual GetCount = " + str(GetCount) + " against the expected 12277") 
                
                elif test_name == "GetStartDateTimestamp":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    GetStartDateTimestamp = self.__Trace.GetStartDateTimestamp()
                    self.__Trace.Close()
                    del self.__Trace
                    if GetStartDateTimestamp == 1494581931:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual GetStartDateTimestamp = " + str(GetStartDateTimestamp) + " against the expected 1494581931")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual GetStartDateTimestamp = " + str(GetStartDateTimestamp) + " against the expected 1494581931")
                   
                elif test_name == "GetEndDateTimestamp":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    GetEndDateTimestamp = self.__Trace.GetEndDateTimestamp()
                    self.__Trace.Close()
                    del self.__Trace
                    if GetEndDateTimestamp == 1494581931:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual GetEndDateTimestamp = " + str(GetEndDateTimestamp) + " against the expected 1494581931")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual GetEndDateTimestamp = " + str(GetEndDateTimestamp) + " against the expected 1494581931")
                        
                elif test_name == "GetTriggerDateTimestamp":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    GetTriggerDateTimestamp = self.__Trace.GetTriggerDateTimestamp()
                    self.__Trace.Close()
                    del self.__Trace
                    if GetTriggerDateTimestamp == 1494581931:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual GetTriggerDateTimestamp = " + str(GetTriggerDateTimestamp) + " against the expected 1494581931")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual GetTriggerDateTimestamp = " + str(GetTriggerDateTimestamp) + " against the expected 1494581931")

                elif test_name == "GetPacket":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    Packet = self.__Trace.GetPacket(9)
                    self.__Trace.Close()
                    del self.__Trace
                    if Packet.GetType() == 4:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Packet.GetType = " + str(Packet.GetType()) + " against the expected SSP Frame")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual Packet.GetType = " + str(Packet.GetType()) + " against the expected SSP Frame")                            

                elif test_name == "GetTimeStamp":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    Packet = self.__Trace.GetPacket(9)
                    self.__Trace.Close()
                    del self.__Trace
                    if Packet.GetTimeStamp() == 11872179688: #by 7.70
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Packet.GetType = " + str(Packet.GetTimeStamp()) + " against the expected TimeStamp 11872180000")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual Packet.GetType = " + str(Packet.GetTimeStamp()) + " against the expected TimeStamp 11872180000") 

                elif test_name == "GetChannel":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    Packet = self.__Trace.GetPacket(9)
                    self.__Trace.Close()
                    del self.__Trace
                    if Packet.GetChannel() == 0:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Packet.GetChannel = " + str(Packet.GetChannel()) + " against the expected Channel")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual Packet.GetChannel = " + str(Packet.GetChannel()) + " against the expected Channel")

                elif test_name == "GetSpeed":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    Packet = self.__Trace.GetPacket(9)
                    self.__Trace.Close()
                    del self.__Trace
                    if Packet.GetSpeed() == 4:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Packet.GetSpeed = " + str(Packet.GetSpeed()) + "G")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual Packet.GetSpeed = " + str(Packet.GetSpeed()) + "G")

                elif test_name == "GetType":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    Packet = self.__Trace.GetPacket(9)
                    self.__Trace.Close()
                    del self.__Trace
                    if Packet.GetType() == 4:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Packet.GetType = " + str(Packet.GetType()) + " against the expected SSP Frame")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual Packet.GetType = " + str(Packet.GetType()) + " against the expected SSP Frame")  

                elif test_name == "GetData":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    Packet = self.__Trace.GetPacket(5)
                    self.__Trace.Close()
                    del self.__Trace
                    if Packet.GetData() == bytearray(b'\xbc\xf0\xf0\xf0\x01\x00\x00\x00'):
                        test_result = SASTestScenario.ETestResult.Success
                        #self.__CallMessageCallback("..Actual Packet.GetType = " + str(Packet.GetType()) + " against the expected SSP Frame")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        #self.__CallMessageCallback("..Actual Packet.GetType = " + str(Packet.GetType()) + " against the expected SSP Frame")                         

                elif test_name == "SetBookmark":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    Packet = self.__Trace.GetPacket(10)
                    Packet.SetBookmark("HelloWorld")
                    self.__Trace.Close()
                    del self.__Trace
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    Packet = self.__Trace.GetPacket(10)
                    if Packet.GetBookmark() == "HelloWorld":
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Packet.SetBookmark = " + Packet.GetBookmark() + " against the expected 'HelloWorld'")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual Packet.SetBookmark = " + Packet.GetBookmark() + " against the expected 'HelloWorld'")    
                    self.__Trace.Close()
                    del self.__Trace
                        
                elif test_name == "GetBookmark":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    Packet = self.__Trace.GetPacket(12)
                    Packet.SetBookmark("HelloWorld")
                    self.__Trace.Close()
                    del self.__Trace
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    Packet = self.__Trace.GetPacket(12)
                    if Packet.GetBookmark() == "HelloWorld":
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Packet.GetBookmark = " + Packet.GetBookmark() + " against the expected 'HelloWorld'")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual Packet.GetBookmark = " + Packet.GetBookmark() + " against the expected 'HelloWorld'")    
                    self.__Trace.Close()
                    del self.__Trace
    
                elif test_name == "ExportToCSV":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    Packet = self.__Trace.ExportToCSV("C:\\Users\\Public\\Documents\\LeCroy\\SAS4 Protocol Suite\\Examples\\Traces\\24G repeated pattern.CSV", None )
                    self.__Trace.Close()
                    del self.__Trace
                    tracesize = os.path.getsize("C:\\Users\\Public\\Documents\\LeCroy\\SAS4 Protocol Suite\\Examples\\Traces\\24G repeated pattern.CSV")/float(1<<10)
                    if tracesize >= 800:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual CSV Size from ExportToCSV = " + str(tracesize).split(".")[0] + "KB against the expected 800KB")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual CSV Size from ExportToCSV = " + str(tracesize).split(".")[0] + "KB against the expected 800KB")                    

                elif test_name == "RunVScript":
                    self.__CallMessageCallback("..Test starts: " + test_name)
                    self.__Trace = self.__Engine.Api.OpenFile(test_trace)
                    self.__CallMessageCallback("..Open trace: " + test_trace)
                    self.__Trace.RunVScript(test_vse, self.__OnVscriptStatus, self.__OnVScriptProgress, self.__OnLogAppended)
                    self.__Trace.Close()
                    del self.__Trace
                    failure = 0
                    if re.search("Success", str(S)):
                        failure = failure + 0
                        self.__CallMessageCallback("..Pass: Actual VSE Callback Status = " + str(S) + " against the expected 'VSEStatus.Success'") 
                    else:
                        failure = failure + 1
                        self.__CallMessageCallback("..Failed: Actual VSE Callback Status = " + str(S) + " against the expected 'VSEStatus.Success'")
                    if re.search("Number of UnexpectedData is 149", str(L)):
                        failure = failure + 0
                        self.__CallMessageCallback("..Pass: Actual VSE Callback Log = " + str(L) + " against the expected 'Number of UnexpectedData is 149'")
                    else:
                        failure = failure + 1
                        self.__CallMessageCallback("..Failed: Actual VSE Callback Log = " + str(L) + " against the expected 'Number of UnexpectedData is 149'")
                    if P == 100:
                        failure = failure + 0
                        self.__CallMessageCallback("..Pass: Actual VSE Callback Progress = " + str(P) + " against the expected '100'")
                    else:
                        failure = failure + 1
                        self.__CallMessageCallback("..Failed: Actual VSE Callback Progress = " + str(P) + " against the expected '100'")
                    
                    if failure == 0:
                        test_result = SASTestScenario.ETestResult.Success
                    else:
                        test_result = SASTestScenario.ETestResult.Failed

                elif test_name == "GetChainCount":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    GetChainCount = self.__Project.GetChainCount()
                    if GetChainCount == 1:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual GetChainCount = " + str(GetChainCount) + " against the expected '1'(Unit Board)")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual GetChainCount = " + str(GetChainCount) + " against the expected '1'(Unit Board)")
                    del self.__Project
                    self.__Project = None        

                elif test_name == "GetDeviceCount":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    GetDeviceCount = self.__Project.GetDeviceCount(0)
                    if GetDeviceCount == 1:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual GetDeviceCount = " + str(GetDeviceCount) + " against the expected '1'(Chain Index)")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual GetDeviceCount = " + str(GetDeviceCount) + " against the expected '1'(Chain Index)")
                    del self.__Project
                    self.__Project = None

                elif test_name == "GetPairPortCount":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    GetPairPortCount = self.__Project.GetPairPortCount(0,0)
                    if GetPairPortCount == 4:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual GetPairPortCount = " + str(GetPairPortCount) + " against the expected '4' Total Ports")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual GetPairPortCount = " + str(GetPairPortCount) + " against the expected ''4' Total Ports")
                    del self.__Project
                    self.__Project = None  

                elif test_name == "GetAnalyzerSettings":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    Setting = self.__Project.GetAnalyzerSettings(0)
                    if Setting.GetSegmentBufferSize(0) > 0:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..GetAnalyzerSettings is called correctly")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..GetAnalyzerSettings cannot be called")    
                    del self.__Project
                    self.__Project = None  

                elif test_name == "SetGetSegmentBufferSize":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    Setting = self.__Project.GetAnalyzerSettings(0)
                    Setting.SetSegmentBufferSize(0, 99999)
                    if Setting.GetSegmentBufferSize(0) == 99999:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual buffer size by SetSegmentBufferSize = " + str(Setting.GetSegmentBufferSize(0)) + "KB against the expected 99999KB")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual buffer size by SetSegmentBufferSize = " + str(Setting.GetSegmentBufferSize(0)) + "KB against the expected 99999KB")    
                    del self.__Project
                    self.__Project = None

                elif test_name == "SetGetNumberOfSegment":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    Setting = self.__Project.GetAnalyzerSettings(0)
                    Setting.SetNumberOfSegment(32)
                    if Setting.GetNumberOfSegment() == 32:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual segment by SetNumberOfSegment = " + str(Setting.GetNumberOfSegment()) + " segments against the expected 32 segments")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual segment by SetNumberOfSegment = " + str(Setting.GetNumberOfSegment()) + " segments against the expected 32 segments")    
                    del self.__Project
                    self.__Project = None
                    
                elif test_name == "SetGetTrigMode":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    Setting = self.__Project.GetAnalyzerSettings(0)
                    Setting.SetTrigMode(0) ## 0 - Snapshot ; 1 - Trigger 
                    if Setting.GetTrigMode() == 0:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Trigger by SetTrigMode = " + str(Setting.GetTrigMode()) + " against the expected '0' = Snapshot")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual segment by SetTrigMode = " + str(Setting.GetTrigMode()) + " against the expected '0' = Snapshot")    
                    del self.__Project
                    self.__Project = None                    

                elif test_name == "SetGetTrigPosition":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    Setting = self.__Project.GetAnalyzerSettings(0)
                    Setting.SetTrigPosition(0,50) 
                    if Setting.GetTrigPosition(0) == 50:
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Trigger by GetTrigPosition = " + str(Setting.GetTrigPosition(0)) + "% against the expected 50 % trigger")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual segment by GetTrigPosition = " + str(Setting.GetTrigPosition(0)) + "% against the expected 50 % trigger")    
                    del self.__Project
                    self.__Project = None
                    
                elif test_name == "SetGetTraceFileName":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    Setting = self.__Project.GetAnalyzerSettings(0)
                    Setting.SetTraceFileName("C:\\Users\\Public\\Documents\\LeCroy\\SAS4 Protocol Suite\\user\\Trace_11.sxt")
                    if Setting.GetTraceFileName() == "C:\\Users\\Public\\Documents\\LeCroy\\SAS4 Protocol Suite\\user\\Trace_11.sxt":
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("..Actual Trace name by GetTraceFileName = Trace" + str(Setting.GetTraceFileName()).split("_")[1] + " against the expected 'Trace_11.sxt'")
                    else:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("..Actual Trace name by GetTraceFileName = Trace" + str(Setting.GetTraceFileName()).split("_")[1] + " against the expected 'Trace_11.sxt'")    
                    del self.__Project
                    self.__Project = None
    
                elif test_name == "StartStopRecording":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    self.__Project.Assign(self.__Params["DeviceSerial"], self.__Engine.Api.EConnectionType.CONNECTION_TYPE_TCP, self.__ChainIndex, self.__DeviceIndex)
                    self.__CallMessageCallback("..assigned")
                    try:
                        self.__Project.StartRecording(0,0,"",None,None,None,0)
                        self.__CallMessageCallback("Start Recording")
                        time.sleep(3)
                        self.__Project.StopRecording(0,0)
                        self.__CallMessageCallback("Stop Recording")
                        time.sleep(3)
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("Pass")      
                        #return (0)
                    except:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("Fail")                        
                        #return (1)
                            
                elif test_name == "StartStopJammer":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    self.__Project.Assign(self.__Params["DeviceSerial"], self.__Engine.Api.EConnectionType.CONNECTION_TYPE_TCP, self.__ChainIndex, self.__DeviceIndex)
                    self.__CallMessageCallback("..assigned")
                    try:
                        self.__Project.StartJammer(0,0,0, "New Scenario", None, None, None)
                        self.__CallMessageCallback("Start Jammer")
                        time.sleep(3)
                        self.__Project.StopJammer(0,0,0)
                        self.__CallMessageCallback("Stop Jammer")
                        time.sleep(3)
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("Pass")      
                        #return (0)
                    except:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("Fail")                        
                        #return (1) 
						
                elif test_name == "StartStopExerciser":
                    self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                    self.__CallMessageCallback("..Project opened")
                    self.__Project.Assign(self.__Params["DeviceSerial"], self.__Engine.Api.EConnectionType.CONNECTION_TYPE_TCP, self.__ChainIndex, self.__DeviceIndex)
                    self.__CallMessageCallback("..assigned")
                    try:
                        self.__Project.StartExerciser(0,0,0, "Exerciser_Test", None, None, None)
                        self.__CallMessageCallback("Start Exerciser")
                        time.sleep(3)
                        self.__Project.StopExerciser(0,0,0)
                        self.__CallMessageCallback("Stop Exerciser")
                        time.sleep(3)
                        test_result = SASTestScenario.ETestResult.Success
                        self.__CallMessageCallback("Pass")      
                        #return (0)
                    except:
                        test_result = SASTestScenario.ETestResult.Failed
                        self.__CallMessageCallback("Fail")                        
                        #return (1)             
                self.__CallMessageCallback("..Test done")
                self.__CompleteTest( "", test_result)
        
        except:
            self.__CompleteTest( self.__MsgFromException(), SASTestScenario.ETestResult.Stopped )

    def __OnTraceCreated(self, trace_type, trace_name):
        pass

    def __OnReportRecordingStatus(self, chain, status, value):
        self.__CallProgressCallback(int(value * 0.5))

    def __OnTraceReport(self, msg):
        self.__CallMessageCallback(msg)

    def __OnError(self, chain, value):
        self.__CompleteTest( "OnError({}, {})".format(chain, value), SASTestScenario.ETestResult.Failed )

    def __OnTraceStatus(self, status):
        test_result = None
        if status == self.__Engine.Api.VSEStatus.Error or status == self.__Engine.Api.VSEStatus.Failed:
            test_result = SASTestScenario.ETestResult.Failed
        if status == self.__Engine.Api.VSEStatus.Success:
            test_result = SASTestScenario.ETestResult.Success

        if test_result:
            self.__CompleteTest( "", test_result )

    def __OnTraceProgress(self, progress):
        self.__CallProgressCallback(int(50 + progress * 0.5))

    def __CompleteTest(self, msg, status ):
        if self.__Project:
            with self.__Engine.Locker():
                self.__Project.Close()
                del self.__Project
                self.__Project = None
        if msg:
            self.__MessageCallback( msg )
        self.__CallProgressCallback(100)
        self.__CallResultCallback( status.value )
        self.__ResetCallbacks()
        self.__IsRunning.clear()

    def __MsgFromException(self):
        ex_type, ex_value, ex_traceback = sys.exc_info()
        return  "Type: {0}; Msg: {1}".format( ex_type.__name__, ex_value)

