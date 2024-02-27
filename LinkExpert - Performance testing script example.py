import SASTestScenario
import os
import threading
import sys
import traceback
import time
from timeit import default_timer as timer

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


    def StopTest( self ):
        self.__IsRunning.clear()



    def __OnVScriptStatus(self, status):
        global VSE_output
        VSE_output = str(status)

    def __VSErun(self, dir_trace, dir_vse):
        VSE_output = ""
        self.__mytrace = self.__Engine.Api.OpenFile(dir_trace)
        self.__mytrace.RunVScript(dir_vse, self.__OnVScriptStatus, None)
        del self.__mytrace

    def __VSEtimestampcheck(self, dir_trace, dir_vse):
        self.__VSErun(dir_trace, dir_vse)
        return(VSE_output)

    def __VSEunexpecteddatacheck(self, dir_trace, dir_vse):
        self.__VSErun(dir_trace, dir_vse)
        return(VSE_output)

    def __RunWorker(self):
        try:
            with self.__Engine.Locker():
                self.__IsRunning.set()
                self.__CallMessageCallback("..Start test (VTKL-1082 6G SATA XF1230 / USB or TCP)")
                self.__Project = self.__Engine.Api.OpenProject(self.__Params["ProjectFile"])
                self.__CallMessageCallback("..Opened project: " + self.__Params["ProjectFile"])
                self.__Project.Assign(self.__Params["DeviceSerial"], self.__Engine.Api.EConnectionType.CONNECTION_TYPE_TCP, self.__ChainIndex, self.__DeviceIndex)
                self.__CallMessageCallback("..Assigned board to project")
                analyzer_setting = self.__Project.GetAnalyzerSettings(0)

                if not self.__IsRunning.isSet():
                    self.__CompleteTest( "", SASTestScenario.ETestResult.Stopped )
                    return

                session_folder = self.__Params["SessionFolder"]
                test_name = self.__Params["TestName"]
                test_name = test_name.replace(" ", "_")
                full_trace_path = os.path.join(session_folder, "{0}_trace.sxt".format(test_name))
                analyzer_setting.SetTraceFileName(full_trace_path)


                # Trace capture
                indexstarttime = timer()
                self.__Project.StartRecording(0,0,"",None,None,None,0)
                self.__CallMessageCallback("..Started recording")
                self.__Project.WaitForTraces(0)
                #self.__CallMessageCallback("..Trace is ready: " + full_trace_path)
                indexendtime = timer()
                time.sleep(1)


                failure = 0                
                # trace size checking
                tracesize = os.path.getsize(full_trace_path)/float(1<<10)
                if test_name == "M244_01GB":
                    expectedtracesize = 500000
                elif test_name == "M244_02GB":
                    expectedtracesize = 1000000
                elif test_name == "M244_04GB":
                    expectedtracesize = 2000000
                elif test_name == "M244_08GB":
                    expectedtracesize = 4000000
                elif test_name == "M244_16GB":
                    expectedtracesize = 8000000
                elif test_name == "M244_32GB":
                    expectedtracesize = 16000000
                elif test_name == "M244_64GB":
                    expectedtracesize = 32000000
                if tracesize >= expectedtracesize:
                    failure = failure + 0
                    self.__CallMessageCallback("..Trace size checking = passed (" + str(tracesize).split(".")[0] + "KB over the expected trace size " + str(expectedtracesize) + "KB)")
                else:
                    failure = failure + 1
                    self.__CallMessageCallback("..Trace size checking = failed (" + str(tracesize).split(".")[0] + "KB over the expected trace size " + str(expectedtracesize) + "KB)")


                # timestamp checking
                vsestarttime = timer()
                if self.__VSEtimestampcheck(full_trace_path, "C:\\Users\\Public\\Documents\\LeCroy\\LinkExpert\\Scripts\\SAS_Scripts\\check_neg_timestamp.py") == "VSEStatus.Success":
                    failure = failure + 0
                    self.__CallMessageCallback("..Timestamp checking = passed")
                else:
                    failure = failure + 1
                    self.__CallMessageCallback("..Timestamp checking = failed")


                # unexpected data checking
                if self.__VSEunexpecteddatacheck(full_trace_path, "C:\\Users\\Public\\Documents\\LeCroy\\LinkExpert\\Scripts\\SAS_Scripts\\check_unexpected_data.py") == "VSEStatus.Success":
                    failure = failure + 0
                    self.__CallMessageCallback("..Unexpected data checking = passed")
                else:
                    failure = failure + 1
                    self.__CallMessageCallback("..Unexpected data checking = failed")
                vseendtime = timer()


                # indexing performance checking
                self.__TraceX = self.__Engine.Api.OpenFile(full_trace_path)
                packetcount = self.__TraceX.GetCount()
                del self.__TraceX
                indexduration = indexendtime - indexstarttime
                indexperformance = round(packetcount/indexduration,2)
                if indexperformance < 115000: #7.85 SATA 6G read-write IO
                    failure = failure + 1
                    self.__CallMessageCallback("..Indexing performance checking = failed (" + str(indexperformance).split(".")[0] + " packet/s over the expected 115000-135000 packet/s @v7.85)")
                else:
                    self.__CallMessageCallback("..Indexing performance checking = passed (" + str(indexperformance).split(".")[0] + " packet/s over the expected 115000-135000 packet/s @v7.85)")


                # VSE performance checking
                vseduration = vseendtime - vsestarttime
                vseperformance = round(packetcount/vseduration,2)
                if vseperformance < 36500: #7.85 SATA 6G read-write IO
                    failure = failure + 1
                    self.__CallMessageCallback("..VSE processing performance checking = failed (" + str(vseperformance).split(".")[0] + " packet/s over the expected 36500-39500 packet/s @v7,85)")
                else:
                    self.__CallMessageCallback("..VSE processing performance checking = passed (" + str(vseperformance).split(".")[0] + " packet/s over the expected 36500-39500 packet/s @v7.85)")

                del self.__Project
                self.__Project = None


                # Trace backup
                trace_folder = "C:\\Users\\Public\\Documents\\LeCroy\\LinkExpert\\Scripts\\SAS_Scripts\\Traces\\" + session_folder.rsplit("/")[-1] + "\\"
                if os.path.isdir("C:\\Users\\Public\\Documents\\LeCroy\\LinkExpert\\Scripts\\SAS_Scripts\\Traces") == False:
                    os.mkdir("C:\\Users\\Public\\Documents\\LeCroy\\LinkExpert\\Scripts\\SAS_Scripts\\Traces")
                if os.path.isdir(trace_folder) == False:
                    os.mkdir(trace_folder)
                import shutil
                shutil.move(full_trace_path, trace_folder + "{0}_trace.sxt".format(test_name))
                self.__CallMessageCallback("..Saved trace in: " + trace_folder + "\\{0}_trace.sxt".format(test_name))


                if not self.__IsRunning.isSet():
                    self.__CompleteTest( "", SASTestScenario.ETestResult.Stopped )
                    return

                self.__CallMessageCallback("failure = " + str(failure))
                if failure == 0:
                    test_result = SASTestScenario.ETestResult.Success
                else:
                    test_result = SASTestScenario.ETestResult.Failed
                self.__CompleteTest( "", test_result)
                self.__CallMessageCallback("..Test done")


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

