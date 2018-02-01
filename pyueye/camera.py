
import .ueye

class Camera():
    def __init__(self):
        

    
    def CaptureStatus(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_CaptureStatus(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def WaitEvent(self, which, nTimeout):
        return ueye.is_WaitEvent(self.hCam, which, nTimeout)
    
    def SetSaturation(self, ChromU, ChromV):
        return ueye.is_SetSaturation(self.hCam, ChromU, ChromV)
    
    def PrepareStealVideo(self, Mode, StealColorMode):
        return ueye.is_PrepareStealVideo(self.hCam, Mode, StealColorMode)
    
    def StopLiveVideo(self, Wait):
        return ueye.is_StopLiveVideo(self.hCam, Wait)
    
    def FreezeVideo(self, Wait):
        return ueye.is_FreezeVideo(self.hCam, Wait)
    
    def CaptureVideo(self, Wait):
        return ueye.is_CaptureVideo(self.hCam, Wait)
    
    def IsVideoFinish(self, pValue):
        return ueye.is_IsVideoFinish(self.hCam, pValue)
    
    def HasVideoStarted(self, pbo):
        return ueye.is_HasVideoStarted(self.hCam, pbo)
    
    def AllocImageMem(self, width, height, bitspixel, ppcImgMem, pid):
        return ueye.is_AllocImageMem(self.hCam, width, height, bitspixel, ppcImgMem, pid)
    
    def SetImageMem(self, pcMem, id):
        return ueye.is_SetImageMem(self.hCam, pcMem, id)
    
    def FreeImageMem(self, pcMem, id):
        return ueye.is_FreeImageMem(self.hCam, pcMem, id)
    
    def GetImageMem(self, pMem):
        return ueye.is_GetImageMem(self.hCam, pMem)
    
    def GetActiveImageMem(self, ppcMem, pnID):
        return ueye.is_GetActiveImageMem(self.hCam, ppcMem, pnID)
    
    def InquireImageMem(self, pcMem, nID, pnX, pnY, pnBits, pnPitch):
        return ueye.is_InquireImageMem(self.hCam, pcMem, nID, pnX, pnY, pnBits, pnPitch)
    
    def GetImageMemPitch(self, pPitch):
        return ueye.is_GetImageMemPitch(self.hCam, pPitch)
    
    def SetAllocatedImageMem(self, width, height, bitspixel, pcImgMem, pid):
        return ueye.is_SetAllocatedImageMem(self.hCam, width, height, bitspixel, pcImgMem, pid)
    
    def CopyImageMem(self, pcSource, nID, pcDest):
        return ueye.is_CopyImageMem(self.hCam, pcSource, nID, pcDest)
    
    def CopyImageMemLines(self, pcSource, nID, nLines, pcDest):
        return ueye.is_CopyImageMemLines(self.hCam, pcSource, nID, nLines, pcDest)
    
    def AddToSequence(self, pcMem, nID):
        return ueye.is_AddToSequence(self.hCam, pcMem, nID)
    
    def GetActSeqBuf(self, pnNum, ppcMem, ppcMemLast):
        return ueye.is_GetActSeqBuf(self.hCam, pnNum, ppcMem, ppcMemLast)
    
    def LockSeqBuf(self, nNum, pcMem):
        return ueye.is_LockSeqBuf(self.hCam, nNum, pcMem)
    
    def UnlockSeqBuf(self, nNum, pcMem):
        return ueye.is_UnlockSeqBuf(self.hCam, nNum, pcMem)
    
    def GetError(self, pErr, ppcErr):
        return ueye.is_GetError(self.hCam, pErr, ppcErr)
    
    def SetErrorReport(self, Mode):
        return ueye.is_SetErrorReport(self.hCam, Mode)
    
    def SetColorMode(self, Mode):
        return ueye.is_SetColorMode(self.hCam, Mode)
    
    def GetColorDepth(self, pnCol, pnColMode):
        return ueye.is_GetColorDepth(self.hCam, pnCol, pnColMode)
    
    def RenderBitmap(self, nMemID, hwnd, nMode):
        return ueye.is_RenderBitmap(self.hCam, nMemID, hwnd, nMode)
    
    def SetDisplayMode(self, Mode):
        return ueye.is_SetDisplayMode(self.hCam, Mode)
    
    def SetDisplayPos(self, x, y):
        return ueye.is_SetDisplayPos(self.hCam, x, y)
    
    def SetHwnd(self, hwnd):
        return ueye.is_SetHwnd(self.hCam, hwnd)
    
    def GetVsyncCount(self, pIntr, pActIntr):
        return ueye.is_GetVsyncCount(self.hCam, pIntr, pActIntr)
    
    def InitEvent(self, hEv, which):
        return ueye.is_InitEvent(self.hCam, hEv, which)
    
    def ExitEvent(self, which):
        return ueye.is_ExitEvent(self.hCam, which)
    
    def EnableEvent(self, which):
        return ueye.is_EnableEvent(self.hCam, which)
    
    def DisableEvent(self, which):
        return ueye.is_DisableEvent(self.hCam, which)
    
    def SetExternalTrigger(self, nTriggerMode):
        return ueye.is_SetExternalTrigger(self.hCam, nTriggerMode)
    
    def SetTriggerCounter(self, nValue):
        return ueye.is_SetTriggerCounter(self.hCam, nValue)
    
    def SetRopEffect(self, effect, param, reserved):
        return ueye.is_SetRopEffect(self.hCam, effect, param, reserved)
    
    def GetCameraInfo(self, pInfo):
        return ueye.is_GetCameraInfo(self.hCam, pInfo)
    
    def CameraStatus(self, nInfo, ulValue):
        return ueye.is_CameraStatus(self.hCam, nInfo, ulValue)
    
    def GetFrameTimeRange(self, min, max, intervall):
        return ueye.is_GetFrameTimeRange(self.hCam, min, max, intervall)
    
    def SetFrameRate(self, FPS, newFPS):
        return ueye.is_SetFrameRate(self.hCam, FPS, newFPS)
    
    def GetFramesPerSecond(self, dblFPS):
        return ueye.is_GetFramesPerSecond(self.hCam, dblFPS)
    
    def GetSensorInfo(self, pInfo):
        return ueye.is_GetSensorInfo(self.hCam, pInfo)
    
    def GetRevisionInfo(self, prevInfo):
        return ueye.is_GetRevisionInfo(self.hCam, prevInfo)
    
    def EnableAutoExit(self, nMode):
        return ueye.is_EnableAutoExit(self.hCam, nMode)
    
    def EnableMessage(self, which, hWnd):
        return ueye.is_EnableMessage(self.hCam, which, hWnd)
    
    def SetHardwareGain(self, nMaster, nRed, nGreen, nBlue):
        return ueye.is_SetHardwareGain(self.hCam, nMaster, nRed, nGreen, nBlue)
    
    def SetWhiteBalance(self, nMode):
        return ueye.is_SetWhiteBalance(self.hCam, nMode)
    
    def SetWhiteBalanceMultipliers(self, dblRed, dblGreen, dblBlue):
        return ueye.is_SetWhiteBalanceMultipliers(self.hCam, dblRed, dblGreen, dblBlue)
    
    def GetWhiteBalanceMultipliers(self, pdblRed, pdblGreen, pdblBlue):
        return ueye.is_GetWhiteBalanceMultipliers(self.hCam, pdblRed, pdblGreen, pdblBlue)
    
    def SetColorCorrection(self, nEnable, factors):
        return ueye.is_SetColorCorrection(self.hCam, nEnable, factors)
    
    def SetSubSampling(self, mode):
        return ueye.is_SetSubSampling(self.hCam, mode)
    
    def SetBinning(self, mode):
        return ueye.is_SetBinning(self.hCam, mode)
    
    def SetCameraID(self, nID):
        return ueye.is_SetCameraID(self.hCam, nID)
    
    def SetBayerConversion(self, nMode):
        return ueye.is_SetBayerConversion(self.hCam, nMode)
    
    def SetHardwareGamma(self, nMode):
        return ueye.is_SetHardwareGamma(self.hCam, nMode)
    
    def SetAutoParameter(self, param, pval1, pval2):
        return ueye.is_SetAutoParameter(self.hCam, param, pval1, pval2)
    
    def GetAutoInfo(self, pInfo):
        return ueye.is_GetAutoInfo(self.hCam, pInfo)
    
    def GetImageHistogram(self, nID, ColorMode, pHistoMem):
        return ueye.is_GetImageHistogram(self.hCam, nID, ColorMode, pHistoMem)
    
    def SetTriggerDelay(self, nTriggerDelay):
        return ueye.is_SetTriggerDelay(self.hCam, nTriggerDelay)
    
    def SetGainBoost(self, mode):
        return ueye.is_SetGainBoost(self.hCam, mode)
    
    def SetGlobalShutter(self, mode):
        return ueye.is_SetGlobalShutter(self.hCam, mode)
    
    def SetExtendedRegister(self, index, value):
        return ueye.is_SetExtendedRegister(self.hCam, index, value)
    
    def GetExtendedRegister(self, index, pwValue):
        return ueye.is_GetExtendedRegister(self.hCam, index, pwValue)
    
    def SetHWGainFactor(self, nMode, nFactor):
        return ueye.is_SetHWGainFactor(self.hCam, nMode, nFactor)
    
    def Renumerate(self, nMode):
        return ueye.is_Renumerate(self.hCam, nMode)
    
    def GetHdrMode(self, Mode):
        return ueye.is_GetHdrMode(self.hCam, Mode)
    
    def EnableHdr(self, Enable):
        return ueye.is_EnableHdr(self.hCam, Enable)
    
    def SetHdrKneepoints(self, KneepointArray, KneepointArraySize):
        return ueye.is_SetHdrKneepoints(self.hCam, KneepointArray, KneepointArraySize)
    
    def GetHdrKneepoints(self, KneepointArray, KneepointArraySize):
        return ueye.is_GetHdrKneepoints(self.hCam, KneepointArray, KneepointArraySize)
    
    def GetHdrKneepointInfo(self, KneepointInfo, KneepointInfoSize):
        return ueye.is_GetHdrKneepointInfo(self.hCam, KneepointInfo, KneepointInfoSize)
    
    def SetOptimalCameraTiming(self, Mode, Timeout, pMaxPxlClk, pMaxFrameRate):
        return ueye.is_SetOptimalCameraTiming(self.hCam, Mode, Timeout, pMaxPxlClk, pMaxFrameRate)
    
    def GetSupportedTestImages(self, SupportedTestImages):
        return ueye.is_GetSupportedTestImages(self.hCam, SupportedTestImages)
    
    def GetTestImageValueRange(self, TestImage, TestImageValueMin, TestImageValueMax):
        return ueye.is_GetTestImageValueRange(self.hCam, TestImage, TestImageValueMin, TestImageValueMax)
    
    def SetSensorTestImage(self, Param1, Param2):
        return ueye.is_SetSensorTestImage(self.hCam, Param1, Param2)
    
    def GetColorConverter(self, ColorMode, pCurrentConvertMode, pDefaultConvertMode, pSupportedConvertModes):
        return ueye.is_GetColorConverter(self.hCam, ColorMode, pCurrentConvertMode, pDefaultConvertMode, pSupportedConvertModes)
    
    def SetColorConverter(self, ColorMode, ConvertMode):
        return ueye.is_SetColorConverter(self.hCam, ColorMode, ConvertMode)
    
    def WaitForNextImage(self, timeout, ppcMem, imageID):
        return ueye.is_WaitForNextImage(self.hCam, timeout, ppcMem, imageID)
    
    def InitImageQueue(self, nMode):
        return ueye.is_InitImageQueue(self.hCam, nMode)
    
    def SetTimeout(self, nMode, Timeout):
        return ueye.is_SetTimeout(self.hCam, nMode, Timeout)
    
    def GetTimeout(self, nMode, pTimeout):
        return ueye.is_GetTimeout(self.hCam, nMode, pTimeout)
    
    def GetDuration(self, nMode, pnTime):
        return ueye.is_GetDuration(self.hCam, nMode, pnTime)
    
    def GetSensorScalerInfo(self, pSensorScalerInfo, nSensorScalerInfoSize):
        return ueye.is_GetSensorScalerInfo(self.hCam, pSensorScalerInfo, nSensorScalerInfoSize)
    
    def SetSensorScaler(self, nMode, dblFactor):
        return ueye.is_SetSensorScaler(self.hCam, nMode, dblFactor)
    
    def GetImageInfo(self, nImageBufferID, pImageInfo, nImageInfoSize):
        return ueye.is_GetImageInfo(self.hCam, nImageBufferID, pImageInfo, nImageInfoSize)
    
    def ImageFormat(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_ImageFormat(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def FaceDetection(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_FaceDetection(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def Focus(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_Focus(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def ImageStabilization(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_ImageStabilization(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def ScenePreset(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_ScenePreset(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def Zoom(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_Zoom(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def Sharpness(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_Sharpness(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def Saturation(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_Saturation(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def TriggerDebounce(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_TriggerDebounce(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def ColorTemperature(self, nCommand, pParam, nSizeOfParam):
        return ueye.is_ColorTemperature(self.hCam, nCommand, pParam, nSizeOfParam)
    
    def DirectRenderer(self, nMode, pParam, SizeOfParam):
        return ueye.is_DirectRenderer(self.hCam, nMode, pParam, SizeOfParam)
    
    def HotPixel(self, nMode, pParam, SizeOfParam):
        return ueye.is_HotPixel(self.hCam, nMode, pParam, SizeOfParam)
    
    def AOI(self, nCommand, pParam, SizeOfParam):
        return ueye.is_AOI(self.hCam, nCommand, pParam, SizeOfParam)
    
    def Transfer(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_Transfer(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def BootBoost(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_BootBoost(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def DeviceFeature(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_DeviceFeature(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def Exposure(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_Exposure(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def Trigger(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_Trigger(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def DeviceInfo(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_DeviceInfo(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def OptimalCameraTiming(self, u32Command, pParam, u32SizeOfParam):
        return ueye.is_OptimalCameraTiming(self.hCam, u32Command, pParam, u32SizeOfParam)
    
    def SetStarterFirmware(self, pcFilepath, uFilepathLen):
        return ueye.is_SetStarterFirmware(self.hCam, pcFilepath, uFilepathLen)
    
    def GetComportNumber(self, pComportNumber):
        return ueye.is_GetComportNumber(self.hCam, pComportNumber)
    
    def IO(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_IO(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def AutoParameter(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_AutoParameter(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def Convert(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_Convert(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def ParameterSet(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_ParameterSet(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def EdgeEnhancement(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_EdgeEnhancement(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def PixelClock(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_PixelClock(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def ImageFile(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_ImageFile(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def Blacklevel(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_Blacklevel(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def ImageBuffer(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_ImageBuffer(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def Measure(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_Measure(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def LUT(self, nCommand, pParam, cbSizeOfParams):
        return ueye.is_LUT(self.hCam, nCommand, pParam, cbSizeOfParams)
    
    def Gamma(self, nCommand, pParam, cbSizeOfParams):
        return ueye.is_Gamma(self.hCam, nCommand, pParam, cbSizeOfParams)
    
    def Multicast(self, nCommand, pParam, cbSizeOfParams):
        return ueye.is_Multicast(self.hCam, nCommand, pParam, cbSizeOfParams)
    
    def Sequencer(self, nCommand, pParam, cbSizeOfParams):
        return ueye.is_Sequencer(self.hCam, nCommand, pParam, cbSizeOfParams)
    
    def PersistentMemory(self, nCommand, pParam, cbSizeOfParam):
        return ueye.is_PersistentMemory(self.hCam, nCommand, pParam, cbSizeOfParam)
    
    def PowerDelivery(self, nCommand, pParam, cbSizeOfParams):
        return ueye.is_PowerDelivery(self.hCam, nCommand, pParam, cbSizeOfParams)
    