
from .ueye import *

class Camera():
    def __init__(self):
        pass
    
    _is_StopLiveVideo = _bind("is_StopLiveVideo", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_StopLiveVideo(self, Wait):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Wait: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_StopLiveVideo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _Wait = _value_cast(Wait, ctypes.c_int)
    
        ret = _is_StopLiveVideo(_hCam, _Wait)
    
        return ret
    
    
    _is_FreezeVideo = _bind("is_FreezeVideo", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_FreezeVideo(self, Wait):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Wait: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_FreezeVideo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _Wait = _value_cast(Wait, ctypes.c_int)
    
        ret = _is_FreezeVideo(_hCam, _Wait)
    
        return ret
    
    
    _is_CaptureVideo = _bind("is_CaptureVideo", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_CaptureVideo(self, Wait):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Wait: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_CaptureVideo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _Wait = _value_cast(Wait, ctypes.c_int)
    
        ret = _is_CaptureVideo(_hCam, _Wait)
    
        return ret
    
    
    _is_IsVideoFinish = _bind("is_IsVideoFinish", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_IsVideoFinish(self, pValue):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pValue: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_IsVideoFinish is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_IsVideoFinish(_hCam, ctypes.byref(pValue))
    
        return ret
    
    
    _is_HasVideoStarted = _bind("is_HasVideoStarted", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_HasVideoStarted(self, pbo):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pbo: c_int (aka c-type: BOOL \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_HasVideoStarted is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_HasVideoStarted(_hCam, ctypes.byref(pbo))
    
        return ret
    
    
    _is_AllocImageMem = _bind("is_AllocImageMem", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(c_mem_p), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_AllocImageMem(self, width, height, bitspixel, ppcImgMem, pid):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param width: c_int (aka c-type: INT)
        :param height: c_int (aka c-type: INT)
        :param bitspixel: c_int (aka c-type: INT)
        :param ppcImgMem: c_mem_p (aka c-type: char \* \*)
        :param pid: c_int (aka c-type: int \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_AllocImageMem is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _width = _value_cast(width, ctypes.c_int)
        _height = _value_cast(height, ctypes.c_int)
        _bitspixel = _value_cast(bitspixel, ctypes.c_int)
    
        ret = _is_AllocImageMem(_hCam, _width, _height, _bitspixel, ctypes.byref(ppcImgMem), ctypes.byref(pid))
    
        return ret
    
    
    _is_SetImageMem = _bind("is_SetImageMem", [ctypes.c_uint, c_mem_p, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetImageMem(self, pcMem, id):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pcMem: c_mem_p (aka c-type: char \*)
        :param id: c_int (aka c-type: int)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetImageMem is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _id = _value_cast(id, ctypes.c_int)
    
        ret = _is_SetImageMem(_hCam, pcMem, _id)
    
        return ret
    
    
    _is_FreeImageMem = _bind("is_FreeImageMem", [ctypes.c_uint, c_mem_p, ctypes.c_int], ctypes.c_int)
    
    
    def is_FreeImageMem(self, pcMem, id):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pcMem: c_mem_p (aka c-type: char \*)
        :param id: c_int (aka c-type: int)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_FreeImageMem is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _id = _value_cast(id, ctypes.c_int)
    
        ret = _is_FreeImageMem(_hCam, pcMem, _id)
    
        return ret
    
    
    _is_GetImageMem = _bind("is_GetImageMem", [ctypes.c_uint, ctypes.POINTER(c_mem_p)], ctypes.c_int)
    
    
    def is_GetImageMem(self, pMem):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pMem: c_mem_p (aka c-type: VOID \* \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetImageMem is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetImageMem(_hCam, ctypes.byref(pMem))
    
        return ret
    
    
    _is_GetActiveImageMem = _bind("is_GetActiveImageMem", [ctypes.c_uint, ctypes.POINTER(c_mem_p), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_GetActiveImageMem(self, ppcMem, pnID):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param ppcMem: c_mem_p (aka c-type: char \* \*)
        :param pnID: c_int (aka c-type: int \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetActiveImageMem is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetActiveImageMem(_hCam, ctypes.byref(ppcMem), ctypes.byref(pnID))
    
        return ret
    
    
    _is_InquireImageMem = _bind("is_InquireImageMem", [ctypes.c_uint, c_mem_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_InquireImageMem(self, pcMem, nID, pnX, pnY, pnBits, pnPitch):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pcMem: c_mem_p (aka c-type: char \*)
        :param nID: c_int (aka c-type: int)
        :param pnX: c_int (aka c-type: int \*)
        :param pnY: c_int (aka c-type: int \*)
        :param pnBits: c_int (aka c-type: int \*)
        :param pnPitch: c_int (aka c-type: int \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_InquireImageMem is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nID = _value_cast(nID, ctypes.c_int)
    
        ret = _is_InquireImageMem(_hCam, pcMem, _nID, ctypes.byref(pnX) if pnX is not None else None, ctypes.byref(pnY) if pnY is not None else None, ctypes.byref(pnBits) if pnBits is not None else None, ctypes.byref(pnPitch) if pnPitch is not None else None)
    
        return ret
    
    
    _is_GetImageMemPitch = _bind("is_GetImageMemPitch", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_GetImageMemPitch(self, pPitch):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pPitch: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetImageMemPitch is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetImageMemPitch(_hCam, ctypes.byref(pPitch))
    
        return ret
    
    
    _is_SetAllocatedImageMem = _bind("is_SetAllocatedImageMem", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, c_mem_p, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_SetAllocatedImageMem(self, width, height, bitspixel, pcImgMem, pid):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param width: c_int (aka c-type: INT)
        :param height: c_int (aka c-type: INT)
        :param bitspixel: c_int (aka c-type: INT)
        :param pcImgMem: c_mem_p (aka c-type: char \*)
        :param pid: c_int (aka c-type: int \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetAllocatedImageMem is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _width = _value_cast(width, ctypes.c_int)
        _height = _value_cast(height, ctypes.c_int)
        _bitspixel = _value_cast(bitspixel, ctypes.c_int)
    
        ret = _is_SetAllocatedImageMem(_hCam, _width, _height, _bitspixel, pcImgMem, ctypes.byref(pid))
    
        return ret
    
    
    _is_CopyImageMem = _bind("is_CopyImageMem", [ctypes.c_uint, c_mem_p, ctypes.c_int, c_mem_p], ctypes.c_int)
    
    
    def is_CopyImageMem(self, pcSource, nID, pcDest):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pcSource: c_mem_p (aka c-type: char \*)
        :param nID: c_int (aka c-type: int)
        :param pcDest: c_mem_p (aka c-type: char \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_CopyImageMem is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nID = _value_cast(nID, ctypes.c_int)
    
        ret = _is_CopyImageMem(_hCam, pcSource, _nID, pcDest)
    
        return ret
    
    
    _is_CopyImageMemLines = _bind("is_CopyImageMemLines", [ctypes.c_uint, c_mem_p, ctypes.c_int, ctypes.c_int, c_mem_p], ctypes.c_int)
    
    
    def is_CopyImageMemLines(self, pcSource, nID, nLines, pcDest):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pcSource: c_mem_p (aka c-type: char \*)
        :param nID: c_int (aka c-type: int)
        :param nLines: c_int (aka c-type: int)
        :param pcDest: c_mem_p (aka c-type: char \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_CopyImageMemLines is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nID = _value_cast(nID, ctypes.c_int)
        _nLines = _value_cast(nLines, ctypes.c_int)
    
        ret = _is_CopyImageMemLines(_hCam, pcSource, _nID, _nLines, pcDest)
    
        return ret
    
    
    _is_AddToSequence = _bind("is_AddToSequence", [ctypes.c_uint, c_mem_p, ctypes.c_int], ctypes.c_int)
    
    
    def is_AddToSequence(self, pcMem, nID):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pcMem: c_mem_p (aka c-type: char \*)
        :param nID: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_AddToSequence is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nID = _value_cast(nID, ctypes.c_int)
    
        ret = _is_AddToSequence(_hCam, pcMem, _nID)
    
        return ret
    
    
    _is_ClearSequence = _bind("is_ClearSequence", [ctypes.c_uint], ctypes.c_int)
    
    
    def is_ClearSequence(self):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ClearSequence is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_ClearSequence(_hCam)
    
        return ret
    
    
    _is_GetActSeqBuf = _bind("is_GetActSeqBuf", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(c_mem_p), ctypes.POINTER(c_mem_p)], ctypes.c_int)
    
    
    def is_GetActSeqBuf(self, pnNum, ppcMem, ppcMemLast):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pnNum: c_int (aka c-type: INT \*)
        :param ppcMem: c_mem_p (aka c-type: char \* \*)
        :param ppcMemLast: c_mem_p (aka c-type: char \* \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetActSeqBuf is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetActSeqBuf(_hCam, ctypes.byref(pnNum) if pnNum is not None else None, ctypes.byref(ppcMem) if ppcMem is not None else None, ctypes.byref(ppcMemLast) if ppcMemLast is not None else None)
    
        return ret
    
    
    _is_LockSeqBuf = _bind("is_LockSeqBuf", [ctypes.c_uint, ctypes.c_int, c_mem_p], ctypes.c_int)
    
    
    def is_LockSeqBuf(self, nNum, pcMem):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nNum: c_int (aka c-type: INT)
        :param pcMem: c_mem_p (aka c-type: char \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_LockSeqBuf is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nNum = _value_cast(nNum, ctypes.c_int)
    
        ret = _is_LockSeqBuf(_hCam, _nNum, pcMem)
    
        return ret
    
    
    _is_UnlockSeqBuf = _bind("is_UnlockSeqBuf", [ctypes.c_uint, ctypes.c_int, c_mem_p], ctypes.c_int)
    
    
    def is_UnlockSeqBuf(self, nNum, pcMem):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nNum: c_int (aka c-type: INT)
        :param pcMem: c_mem_p (aka c-type: char \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_UnlockSeqBuf is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nNum = _value_cast(nNum, ctypes.c_int)
    
        ret = _is_UnlockSeqBuf(_hCam, _nNum, pcMem)
    
        return ret
    
    
    _is_GetError = _bind("is_GetError", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_char_p)], ctypes.c_int)
    
    
    def is_GetError(self, pErr, ppcErr):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pErr: c_int (aka c-type: INT \*)
        :param ppcErr: c_char_p (aka c-type: IS_CHAR \* \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetError is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetError(_hCam, ctypes.byref(pErr), ctypes.byref(ppcErr))
    
        return ret
    
    
    _is_SetErrorReport = _bind("is_SetErrorReport", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetErrorReport(self, Mode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Mode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetErrorReport is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _Mode = _value_cast(Mode, ctypes.c_int)
    
        ret = _is_SetErrorReport(_hCam, _Mode)
    
        return ret
    
    
    _is_SetColorMode = _bind("is_SetColorMode", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetColorMode(self, Mode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Mode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetColorMode is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _Mode = _value_cast(Mode, ctypes.c_int)
    
        ret = _is_SetColorMode(_hCam, _Mode)
    
        return ret
    
    
    _is_GetColorDepth = _bind("is_GetColorDepth", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_GetColorDepth(self, pnCol, pnColMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pnCol: c_int (aka c-type: INT \*)
        :param pnColMode: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetColorDepth is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetColorDepth(_hCam, ctypes.byref(pnCol), ctypes.byref(pnColMode))
    
        return ret
    
    
    _is_RenderBitmap = _bind("is_RenderBitmap", [ctypes.c_uint, ctypes.c_int, ctypes.c_void_p, ctypes.c_int], ctypes.c_int)
    
    
    def is_RenderBitmap(self, nMemID, hwnd, nMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMemID: c_int (aka c-type: INT)
        :param hwnd: c_void_p (aka c-type: HWND)
        :param nMode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_RenderBitmap is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMemID = _value_cast(nMemID, ctypes.c_int)
        _hwnd = _pointer_cast(hwnd, ctypes.c_void_p)
        _nMode = _value_cast(nMode, ctypes.c_int)
    
        ret = _is_RenderBitmap(_hCam, _nMemID, _hwnd, _nMode)
    
        return ret
    
    
    _is_SetDisplayMode = _bind("is_SetDisplayMode", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetDisplayMode(self, Mode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Mode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetDisplayMode is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _Mode = _value_cast(Mode, ctypes.c_int)
    
        ret = _is_SetDisplayMode(_hCam, _Mode)
    
        return ret
    
    
    _is_SetDisplayPos = _bind("is_SetDisplayPos", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetDisplayPos(self, x, y):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param x: c_int (aka c-type: INT)
        :param y: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetDisplayPos is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _x = _value_cast(x, ctypes.c_int)
        _y = _value_cast(y, ctypes.c_int)
    
        ret = _is_SetDisplayPos(_hCam, _x, _y)
    
        return ret
    
    
    _is_SetHwnd = _bind("is_SetHwnd", [ctypes.c_uint, ctypes.c_void_p], ctypes.c_int)
    
    
    def is_SetHwnd(self, hwnd):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param hwnd: c_void_p (aka c-type: HWND)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetHwnd is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _hwnd = _pointer_cast(hwnd, ctypes.c_void_p)
    
        ret = _is_SetHwnd(_hCam, _hwnd)
    
        return ret
    
    
    _is_GetVsyncCount = _bind("is_GetVsyncCount", [ctypes.c_uint, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)], ctypes.c_int)
    
    
    def is_GetVsyncCount(self, pIntr, pActIntr):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pIntr: c_long (aka c-type: long \*)
        :param pActIntr: c_long (aka c-type: long \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetVsyncCount is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetVsyncCount(_hCam, ctypes.byref(pIntr), ctypes.byref(pActIntr))
    
        return ret
    
    
    _is_GetDLLVersion = _bind("is_GetDLLVersion", None, ctypes.c_int)
    
    
    def is_GetDLLVersion():
        """
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetDLLVersion is None:
            raise NotImplementedError()
    
        ret = _is_GetDLLVersion()
    
        return ret
    
    
    _is_InitEvent = _bind("is_InitEvent", [ctypes.c_uint, ctypes.c_void_p, ctypes.c_int], ctypes.c_int)
    
    
    def is_InitEvent(self, hEv, which):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param hEv: c_void_p (aka c-type: HANDLE)
        :param which: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_InitEvent is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _hEv = _pointer_cast(hEv, ctypes.c_void_p)
        _which = _value_cast(which, ctypes.c_int)
    
        ret = _is_InitEvent(_hCam, _hEv, _which)
    
        return ret
    
    
    _is_ExitEvent = _bind("is_ExitEvent", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_ExitEvent(self, which):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param which: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ExitEvent is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _which = _value_cast(which, ctypes.c_int)
    
        ret = _is_ExitEvent(_hCam, _which)
    
        return ret
    
    
    _is_EnableEvent = _bind("is_EnableEvent", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_EnableEvent(self, which):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param which: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_EnableEvent is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _which = _value_cast(which, ctypes.c_int)
    
        ret = _is_EnableEvent(_hCam, _which)
    
        return ret
    
    
    _is_DisableEvent = _bind("is_DisableEvent", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_DisableEvent(self, which):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param which: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_DisableEvent is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _which = _value_cast(which, ctypes.c_int)
    
        ret = _is_DisableEvent(_hCam, _which)
    
        return ret
    
    
    _is_SetExternalTrigger = _bind("is_SetExternalTrigger", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetExternalTrigger(self, nTriggerMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nTriggerMode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetExternalTrigger is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nTriggerMode = _value_cast(nTriggerMode, ctypes.c_int)
    
        ret = _is_SetExternalTrigger(_hCam, _nTriggerMode)
    
        return ret
    
    
    _is_SetTriggerCounter = _bind("is_SetTriggerCounter", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetTriggerCounter(self, nValue):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nValue: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetTriggerCounter is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nValue = _value_cast(nValue, ctypes.c_int)
    
        ret = _is_SetTriggerCounter(_hCam, _nValue)
    
        return ret
    
    
    _is_SetRopEffect = _bind("is_SetRopEffect", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetRopEffect(self, effect, param, reserved):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param effect: c_int (aka c-type: INT)
        :param param: c_int (aka c-type: INT)
        :param reserved: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetRopEffect is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _effect = _value_cast(effect, ctypes.c_int)
        _param = _value_cast(param, ctypes.c_int)
        _reserved = _value_cast(reserved, ctypes.c_int)
    
        ret = _is_SetRopEffect(_hCam, _effect, _param, _reserved)
    
        return ret
    
    
    _is_InitCamera = _bind("is_InitCamera", [ctypes.POINTER(ctypes.c_uint), ctypes.c_void_p], ctypes.c_int)
    
    
    def is_InitCamera(phCam, hWnd):
        """
        :param phCam: c_uint (aka c-type: HIDS \*)
        :param hWnd: c_void_p (aka c-type: HWND)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_InitCamera is None:
            raise NotImplementedError()
    
        _hWnd = _pointer_cast(hWnd, ctypes.c_void_p)
    
        ret = _is_InitCamera(ctypes.byref(phCam), _hWnd)
    
        return ret
    
    
    _is_ExitCamera = _bind("is_ExitCamera", [ctypes.c_uint], ctypes.c_int)
    
    
    def is_ExitCamera(self):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ExitCamera is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_ExitCamera(_hCam)
    
        return ret
    
    
    _is_GetCameraInfo = _bind("is_GetCameraInfo", [ctypes.c_uint, ctypes.POINTER(CAMINFO)], ctypes.c_int)
    
    
    def is_GetCameraInfo(self, pInfo):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pInfo: CAMINFO (aka c-type: PCAMINFO)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetCameraInfo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetCameraInfo(_hCam, ctypes.byref(pInfo))
    
        return ret
    
    
    _is_CameraStatus = _bind("is_CameraStatus", [ctypes.c_uint, ctypes.c_int, ctypes.c_uint], ctypes.c_int)
    
    
    def is_CameraStatus(self, nInfo, ulValue):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nInfo: c_int (aka c-type: INT)
        :param ulValue: c_uint (aka c-type: ULONG)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_CameraStatus is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nInfo = _value_cast(nInfo, ctypes.c_int)
        _ulValue = _value_cast(ulValue, ctypes.c_uint)
    
        ret = _is_CameraStatus(_hCam, _nInfo, _ulValue)
    
        return ret
    
    
    _is_GetCameraType = _bind("is_GetCameraType", [ctypes.c_uint], ctypes.c_int)
    
    
    def is_GetCameraType(self):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetCameraType is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetCameraType(_hCam)
    
        return ret
    
    
    _is_GetNumberOfCameras = _bind("is_GetNumberOfCameras", [ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_GetNumberOfCameras(pnNumCams):
        """
        :param pnNumCams: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetNumberOfCameras is None:
            raise NotImplementedError()
    
        ret = _is_GetNumberOfCameras(ctypes.byref(pnNumCams))
    
        return ret
    
    
    _is_GetUsedBandwidth = _bind("is_GetUsedBandwidth", [ctypes.c_uint], ctypes.c_int)
    
    
    def is_GetUsedBandwidth(self):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetUsedBandwidth is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetUsedBandwidth(_hCam)
    
        return ret
    
    
    _is_GetFrameTimeRange = _bind("is_GetFrameTimeRange", [ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)], ctypes.c_int)
    
    
    def is_GetFrameTimeRange(self, min, max, intervall):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param min: c_double (aka c-type: double \*)
        :param max: c_double (aka c-type: double \*)
        :param intervall: c_double (aka c-type: double \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetFrameTimeRange is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetFrameTimeRange(_hCam, ctypes.byref(min), ctypes.byref(max), ctypes.byref(intervall))
    
        return ret
    
    
    _is_SetFrameRate = _bind("is_SetFrameRate", [ctypes.c_uint, ctypes.c_double, ctypes.POINTER(ctypes.c_double)], ctypes.c_int)
    
    
    def is_SetFrameRate(self, FPS, newFPS):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param FPS: c_double (aka c-type: double)
        :param newFPS: c_double (aka c-type: double \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetFrameRate is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _FPS = _value_cast(FPS, ctypes.c_double)
    
        ret = _is_SetFrameRate(_hCam, _FPS, ctypes.byref(newFPS))
    
        return ret
    
    
    _is_GetFramesPerSecond = _bind("is_GetFramesPerSecond", [ctypes.c_uint, ctypes.POINTER(ctypes.c_double)], ctypes.c_int)
    
    
    def is_GetFramesPerSecond(self, dblFPS):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param dblFPS: c_double (aka c-type: double \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetFramesPerSecond is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetFramesPerSecond(_hCam, ctypes.byref(dblFPS))
    
        return ret
    
    
    _is_GetSensorInfo = _bind("is_GetSensorInfo", [ctypes.c_uint, ctypes.POINTER(SENSORINFO)], ctypes.c_int)
    
    
    def is_GetSensorInfo(self, pInfo):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pInfo: SENSORINFO (aka c-type: PSENSORINFO)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetSensorInfo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetSensorInfo(_hCam, ctypes.byref(pInfo))
    
        return ret
    
    
    _is_GetRevisionInfo = _bind("is_GetRevisionInfo", [ctypes.c_uint, ctypes.POINTER(REVISIONINFO)], ctypes.c_int)
    
    
    def is_GetRevisionInfo(self, prevInfo):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param prevInfo: REVISIONINFO (aka c-type: PREVISIONINFO)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetRevisionInfo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetRevisionInfo(_hCam, ctypes.byref(prevInfo))
    
        return ret
    
    
    _is_EnableAutoExit = _bind("is_EnableAutoExit", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_EnableAutoExit(self, nMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_EnableAutoExit is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_int)
    
        ret = _is_EnableAutoExit(_hCam, _nMode)
    
        return ret
    
    
    _is_EnableMessage = _bind("is_EnableMessage", [ctypes.c_uint, ctypes.c_int, ctypes.c_void_p], ctypes.c_int)
    
    
    def is_EnableMessage(self, which, hWnd):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param which: c_int (aka c-type: INT)
        :param hWnd: c_void_p (aka c-type: HWND)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_EnableMessage is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _which = _value_cast(which, ctypes.c_int)
        _hWnd = _pointer_cast(hWnd, ctypes.c_void_p)
    
        ret = _is_EnableMessage(_hCam, _which, _hWnd)
    
        return ret
    
    
    _is_SetHardwareGain = _bind("is_SetHardwareGain", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetHardwareGain(self, nMaster, nRed, nGreen, nBlue):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMaster: c_int (aka c-type: INT)
        :param nRed: c_int (aka c-type: INT)
        :param nGreen: c_int (aka c-type: INT)
        :param nBlue: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetHardwareGain is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMaster = _value_cast(nMaster, ctypes.c_int)
        _nRed = _value_cast(nRed, ctypes.c_int)
        _nGreen = _value_cast(nGreen, ctypes.c_int)
        _nBlue = _value_cast(nBlue, ctypes.c_int)
    
        ret = _is_SetHardwareGain(_hCam, _nMaster, _nRed, _nGreen, _nBlue)
    
        return ret
    
    
    _is_SetWhiteBalance = _bind("is_SetWhiteBalance", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetWhiteBalance(self, nMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetWhiteBalance is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_int)
    
        ret = _is_SetWhiteBalance(_hCam, _nMode)
    
        return ret
    
    
    _is_SetWhiteBalanceMultipliers = _bind("is_SetWhiteBalanceMultipliers", [ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_double], ctypes.c_int)
    
    
    def is_SetWhiteBalanceMultipliers(self, dblRed, dblGreen, dblBlue):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param dblRed: c_double (aka c-type: double)
        :param dblGreen: c_double (aka c-type: double)
        :param dblBlue: c_double (aka c-type: double)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetWhiteBalanceMultipliers is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _dblRed = _value_cast(dblRed, ctypes.c_double)
        _dblGreen = _value_cast(dblGreen, ctypes.c_double)
        _dblBlue = _value_cast(dblBlue, ctypes.c_double)
    
        ret = _is_SetWhiteBalanceMultipliers(_hCam, _dblRed, _dblGreen, _dblBlue)
    
        return ret
    
    
    _is_GetWhiteBalanceMultipliers = _bind("is_GetWhiteBalanceMultipliers", [ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)], ctypes.c_int)
    
    
    def is_GetWhiteBalanceMultipliers(self, pdblRed, pdblGreen, pdblBlue):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pdblRed: c_double (aka c-type: double \*)
        :param pdblGreen: c_double (aka c-type: double \*)
        :param pdblBlue: c_double (aka c-type: double \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetWhiteBalanceMultipliers is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetWhiteBalanceMultipliers(_hCam, ctypes.byref(pdblRed), ctypes.byref(pdblGreen), ctypes.byref(pdblBlue))
    
        return ret
    
    
    _is_SetColorCorrection = _bind("is_SetColorCorrection", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_double)], ctypes.c_int)
    
    
    def is_SetColorCorrection(self, nEnable, factors):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nEnable: c_int (aka c-type: INT)
        :param factors: c_double (aka c-type: double \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetColorCorrection is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nEnable = _value_cast(nEnable, ctypes.c_int)
    
        ret = _is_SetColorCorrection(_hCam, _nEnable, ctypes.byref(factors))
    
        return ret
    
    
    _is_SetSubSampling = _bind("is_SetSubSampling", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetSubSampling(self, mode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param mode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetSubSampling is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _mode = _value_cast(mode, ctypes.c_int)
    
        ret = _is_SetSubSampling(_hCam, _mode)
    
        return ret
    
    
    _is_ForceTrigger = _bind("is_ForceTrigger", [ctypes.c_uint], ctypes.c_int)
    
    
    def is_ForceTrigger(self):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ForceTrigger is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_ForceTrigger(_hCam)
    
        return ret
    
    
    _is_GetBusSpeed = _bind("is_GetBusSpeed", [ctypes.c_uint], ctypes.c_int)
    
    
    def is_GetBusSpeed(self):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetBusSpeed is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetBusSpeed(_hCam)
    
        return ret
    
    
    _is_SetBinning = _bind("is_SetBinning", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetBinning(self, mode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param mode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetBinning is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _mode = _value_cast(mode, ctypes.c_int)
    
        ret = _is_SetBinning(_hCam, _mode)
    
        return ret
    
    
    _is_ResetToDefault = _bind("is_ResetToDefault", [ctypes.c_uint], ctypes.c_int)
    
    
    def is_ResetToDefault(self):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ResetToDefault is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_ResetToDefault(_hCam)
    
        return ret
    
    
    _is_SetCameraID = _bind("is_SetCameraID", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetCameraID(self, nID):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nID: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetCameraID is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nID = _value_cast(nID, ctypes.c_int)
    
        ret = _is_SetCameraID(_hCam, _nID)
    
        return ret
    
    
    _is_SetBayerConversion = _bind("is_SetBayerConversion", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetBayerConversion(self, nMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetBayerConversion is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_int)
    
        ret = _is_SetBayerConversion(_hCam, _nMode)
    
        return ret
    
    
    _is_SetHardwareGamma = _bind("is_SetHardwareGamma", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetHardwareGamma(self, nMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetHardwareGamma is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_int)
    
        ret = _is_SetHardwareGamma(_hCam, _nMode)
    
        return ret
    
    
    _is_GetCameraList = _bind("is_GetCameraList", [ctypes.POINTER(_UEYE_CAMERA_LIST)], ctypes.c_int)
    
    
    def is_GetCameraList(pucl):
        """
        :param pucl: UEYE_CAMERA_LIST (aka c-type: PUEYE_CAMERA_LIST)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetCameraList is None:
            raise NotImplementedError()
    
        ret = _is_GetCameraList(ctypes.cast(ctypes.pointer(pucl), ctypes.POINTER(_UEYE_CAMERA_LIST)))
    
        return ret
    
    
    _is_SetAutoParameter = _bind("is_SetAutoParameter", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)], ctypes.c_int)
    
    
    def is_SetAutoParameter(self, param, pval1, pval2):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param param: c_int (aka c-type: INT)
        :param pval1: c_double (aka c-type: double \*)
        :param pval2: c_double (aka c-type: double \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetAutoParameter is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _param = _value_cast(param, ctypes.c_int)
    
        ret = _is_SetAutoParameter(_hCam, _param, ctypes.byref(pval1), ctypes.byref(pval2))
    
        return ret
    
    
    _is_GetAutoInfo = _bind("is_GetAutoInfo", [ctypes.c_uint, ctypes.POINTER(UEYE_AUTO_INFO)], ctypes.c_int)
    
    
    def is_GetAutoInfo(self, pInfo):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pInfo: UEYE_AUTO_INFO (aka c-type: UEYE_AUTO_INFO \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetAutoInfo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetAutoInfo(_hCam, ctypes.byref(pInfo))
    
        return ret
    
    
    _is_GetImageHistogram = _bind("is_GetImageHistogram", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_uint)], ctypes.c_int)
    
    
    def is_GetImageHistogram(self, nID, ColorMode, pHistoMem):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nID: c_int (aka c-type: int)
        :param ColorMode: c_int (aka c-type: INT)
        :param pHistoMem: c_uint_Array_x (aka c-type: DWORD \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetImageHistogram is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nID = _value_cast(nID, ctypes.c_int)
        _ColorMode = _value_cast(ColorMode, ctypes.c_int)
    
        ret = _is_GetImageHistogram(_hCam, _nID, _ColorMode, ctypes.cast(pHistoMem, ctypes.POINTER(ctypes.c_uint)))
    
        return ret
    
    
    _is_SetTriggerDelay = _bind("is_SetTriggerDelay", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetTriggerDelay(self, nTriggerDelay):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nTriggerDelay: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetTriggerDelay is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nTriggerDelay = _value_cast(nTriggerDelay, ctypes.c_int)
    
        ret = _is_SetTriggerDelay(_hCam, _nTriggerDelay)
    
        return ret
    
    
    _is_SetGainBoost = _bind("is_SetGainBoost", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetGainBoost(self, mode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param mode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetGainBoost is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _mode = _value_cast(mode, ctypes.c_int)
    
        ret = _is_SetGainBoost(_hCam, _mode)
    
        return ret
    
    
    _is_SetGlobalShutter = _bind("is_SetGlobalShutter", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetGlobalShutter(self, mode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param mode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetGlobalShutter is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _mode = _value_cast(mode, ctypes.c_int)
    
        ret = _is_SetGlobalShutter(_hCam, _mode)
    
        return ret
    
    
    _is_SetExtendedRegister = _bind("is_SetExtendedRegister", [ctypes.c_uint, ctypes.c_int, ctypes.c_ushort], ctypes.c_int)
    
    
    def is_SetExtendedRegister(self, index, value):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param index: c_int (aka c-type: INT)
        :param value: c_ushort (aka c-type: WORD)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetExtendedRegister is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _index = _value_cast(index, ctypes.c_int)
        _value = _value_cast(value, ctypes.c_ushort)
    
        ret = _is_SetExtendedRegister(_hCam, _index, _value)
    
        return ret
    
    
    _is_GetExtendedRegister = _bind("is_GetExtendedRegister", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_ushort)], ctypes.c_int)
    
    
    def is_GetExtendedRegister(self, index, pwValue):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param index: c_int (aka c-type: INT)
        :param pwValue: c_ushort (aka c-type: WORD \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetExtendedRegister is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _index = _value_cast(index, ctypes.c_int)
    
        ret = _is_GetExtendedRegister(_hCam, _index, ctypes.byref(pwValue))
    
        return ret
    
    
    _is_SetHWGainFactor = _bind("is_SetHWGainFactor", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetHWGainFactor(self, nMode, nFactor):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_int (aka c-type: INT)
        :param nFactor: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetHWGainFactor is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_int)
        _nFactor = _value_cast(nFactor, ctypes.c_int)
    
        ret = _is_SetHWGainFactor(_hCam, _nMode, _nFactor)
    
        return ret
    
    
    _is_Renumerate = _bind("is_Renumerate", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_Renumerate(self, nMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Renumerate is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_int)
    
        ret = _is_Renumerate(_hCam, _nMode)
    
        return ret
    
    
    _is_WriteI2C = _bind("is_WriteI2C", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int], ctypes.c_int)
    
    
    def is_WriteI2C(self.hCam, nDeviceAddr, nRegisterAddr, pbData, nLen):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nDeviceAddr: c_int (aka c-type: INT)
        :param nRegisterAddr: c_int (aka c-type: INT)
        :param pbData: c_ubyte_Array_x (aka c-type: BYTE \*)
        :param nLen: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_WriteI2C is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nDeviceAddr = _value_cast(nDeviceAddr, ctypes.c_int)
        _nRegisterAddr = _value_cast(nRegisterAddr, ctypes.c_int)
        _nLen = _value_cast(nLen, ctypes.c_int)
    
        ret = _is_WriteI2C(_hCam, _nDeviceAddr, _nRegisterAddr, ctypes.cast(pbData, ctypes.POINTER(ctypes.c_ubyte)), _nLen)
    
        return ret
    
    
    _is_ReadI2C = _bind("is_ReadI2C", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int], ctypes.c_int)
    
    
    def is_ReadI2C(self.hCam, nDeviceAddr, nRegisterAddr, pbData, nLen):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nDeviceAddr: c_int (aka c-type: INT)
        :param nRegisterAddr: c_int (aka c-type: INT)
        :param pbData: c_ubyte_Array_x (aka c-type: BYTE \*)
        :param nLen: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ReadI2C is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nDeviceAddr = _value_cast(nDeviceAddr, ctypes.c_int)
        _nRegisterAddr = _value_cast(nRegisterAddr, ctypes.c_int)
        _nLen = _value_cast(nLen, ctypes.c_int)
    
        ret = _is_ReadI2C(_hCam, _nDeviceAddr, _nRegisterAddr, ctypes.cast(pbData, ctypes.POINTER(ctypes.c_ubyte)), _nLen)
    
        return ret
    
    
    _is_GetHdrMode = _bind("is_GetHdrMode", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_GetHdrMode(self, Mode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Mode: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetHdrMode is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetHdrMode(_hCam, ctypes.byref(Mode))
    
        return ret
    
    
    _is_EnableHdr = _bind("is_EnableHdr", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_EnableHdr(self, Enable):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Enable: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_EnableHdr is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _Enable = _value_cast(Enable, ctypes.c_int)
    
        ret = _is_EnableHdr(_hCam, _Enable)
    
        return ret
    
    
    _is_SetHdrKneepoints = _bind("is_SetHdrKneepoints", [ctypes.c_uint, ctypes.POINTER(KNEEPOINTARRAY), ctypes.c_int], ctypes.c_int)
    
    
    def is_SetHdrKneepoints(self, KneepointArray, KneepointArraySize):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param KneepointArray: KNEEPOINTARRAY (aka c-type: KNEEPOINTARRAY \*)
        :param KneepointArraySize: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetHdrKneepoints is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _KneepointArraySize = _value_cast(KneepointArraySize, ctypes.c_int)
    
        ret = _is_SetHdrKneepoints(_hCam, ctypes.byref(KneepointArray), _KneepointArraySize)
    
        return ret
    
    
    _is_GetHdrKneepoints = _bind("is_GetHdrKneepoints", [ctypes.c_uint, ctypes.POINTER(KNEEPOINTARRAY), ctypes.c_int], ctypes.c_int)
    
    
    def is_GetHdrKneepoints(self, KneepointArray, KneepointArraySize):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param KneepointArray: KNEEPOINTARRAY (aka c-type: KNEEPOINTARRAY \*)
        :param KneepointArraySize: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetHdrKneepoints is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _KneepointArraySize = _value_cast(KneepointArraySize, ctypes.c_int)
    
        ret = _is_GetHdrKneepoints(_hCam, ctypes.byref(KneepointArray), _KneepointArraySize)
    
        return ret
    
    
    _is_GetHdrKneepointInfo = _bind("is_GetHdrKneepointInfo", [ctypes.c_uint, ctypes.POINTER(KNEEPOINTINFO), ctypes.c_int], ctypes.c_int)
    
    
    def is_GetHdrKneepointInfo(self, KneepointInfo, KneepointInfoSize):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param KneepointInfo: KNEEPOINTINFO (aka c-type: KNEEPOINTINFO \*)
        :param KneepointInfoSize: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetHdrKneepointInfo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _KneepointInfoSize = _value_cast(KneepointInfoSize, ctypes.c_int)
    
        ret = _is_GetHdrKneepointInfo(_hCam, ctypes.byref(KneepointInfo), _KneepointInfoSize)
    
        return ret
    
    
    _is_SetOptimalCameraTiming = _bind("is_SetOptimalCameraTiming", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)], ctypes.c_int)
    
    
    def is_SetOptimalCameraTiming(self, Mode, Timeout, pMaxPxlClk, pMaxFrameRate):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Mode: c_int (aka c-type: INT)
        :param Timeout: c_int (aka c-type: INT)
        :param pMaxPxlClk: c_int (aka c-type: INT \*)
        :param pMaxFrameRate: c_double (aka c-type: double \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetOptimalCameraTiming is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _Mode = _value_cast(Mode, ctypes.c_int)
        _Timeout = _value_cast(Timeout, ctypes.c_int)
    
        ret = _is_SetOptimalCameraTiming(_hCam, _Mode, _Timeout, ctypes.byref(pMaxPxlClk), ctypes.byref(pMaxFrameRate))
    
        return ret
    
    
    _is_GetSupportedTestImages = _bind("is_GetSupportedTestImages", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_GetSupportedTestImages(self, SupportedTestImages):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param SupportedTestImages: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetSupportedTestImages is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetSupportedTestImages(_hCam, ctypes.byref(SupportedTestImages))
    
        return ret
    
    
    _is_GetTestImageValueRange = _bind("is_GetTestImageValueRange", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_GetTestImageValueRange(self, TestImage, TestImageValueMin, TestImageValueMax):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param TestImage: c_int (aka c-type: INT)
        :param TestImageValueMin: c_int (aka c-type: INT \*)
        :param TestImageValueMax: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetTestImageValueRange is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _TestImage = _value_cast(TestImage, ctypes.c_int)
    
        ret = _is_GetTestImageValueRange(_hCam, _TestImage, ctypes.byref(TestImageValueMin), ctypes.byref(TestImageValueMax))
    
        return ret
    
    
    _is_SetSensorTestImage = _bind("is_SetSensorTestImage", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetSensorTestImage(self, Param1, Param2):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param Param1: c_int (aka c-type: INT)
        :param Param2: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetSensorTestImage is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _Param1 = _value_cast(Param1, ctypes.c_int)
        _Param2 = _value_cast(Param2, ctypes.c_int)
    
        ret = _is_SetSensorTestImage(_hCam, _Param1, _Param2)
    
        return ret
    
    
    _is_GetColorConverter = _bind("is_GetColorConverter", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_GetColorConverter(self, ColorMode, pCurrentConvertMode, pDefaultConvertMode, pSupportedConvertModes):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param ColorMode: c_int (aka c-type: INT)
        :param pCurrentConvertMode: c_int (aka c-type: INT \*)
        :param pDefaultConvertMode: c_int (aka c-type: INT \*)
        :param pSupportedConvertModes: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetColorConverter is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _ColorMode = _value_cast(ColorMode, ctypes.c_int)
    
        ret = _is_GetColorConverter(_hCam, _ColorMode, ctypes.byref(pCurrentConvertMode), ctypes.byref(pDefaultConvertMode), ctypes.byref(pSupportedConvertModes))
    
        return ret
    
    
    _is_SetColorConverter = _bind("is_SetColorConverter", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)
    
    
    def is_SetColorConverter(self, ColorMode, ConvertMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param ColorMode: c_int (aka c-type: INT)
        :param ConvertMode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetColorConverter is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _ColorMode = _value_cast(ColorMode, ctypes.c_int)
        _ConvertMode = _value_cast(ConvertMode, ctypes.c_int)
    
        ret = _is_SetColorConverter(_hCam, _ColorMode, _ConvertMode)
    
        return ret
    
    
    _is_WaitForNextImage = _bind("is_WaitForNextImage", [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(c_mem_p), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_WaitForNextImage(self, timeout, ppcMem, imageID):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param timeout: c_uint (aka c-type: UINT)
        :param ppcMem: c_mem_p (aka c-type: char \* \*)
        :param imageID: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_WaitForNextImage is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _timeout = _value_cast(timeout, ctypes.c_uint)
    
        ret = _is_WaitForNextImage(_hCam, _timeout, ctypes.byref(ppcMem), ctypes.byref(imageID))
    
        return ret
    
    
    _is_InitImageQueue = _bind("is_InitImageQueue", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)
    
    
    def is_InitImageQueue(self, nMode):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_InitImageQueue is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_int)
    
        ret = _is_InitImageQueue(_hCam, _nMode)
    
        return ret
    
    
    _is_ExitImageQueue = _bind("is_ExitImageQueue", [ctypes.c_uint], ctypes.c_int)
    
    
    def is_ExitImageQueue(self):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ExitImageQueue is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_ExitImageQueue(_hCam)
    
        return ret
    
    
    _is_SetTimeout = _bind("is_SetTimeout", [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], ctypes.c_int)
    
    
    def is_SetTimeout(self, nMode, Timeout):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_uint (aka c-type: UINT)
        :param Timeout: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetTimeout is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_uint)
        _Timeout = _value_cast(Timeout, ctypes.c_uint)
    
        ret = _is_SetTimeout(_hCam, _nMode, _Timeout)
    
        return ret
    
    
    _is_GetTimeout = _bind("is_GetTimeout", [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)], ctypes.c_int)
    
    
    def is_GetTimeout(self, nMode, pTimeout):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_uint (aka c-type: UINT)
        :param pTimeout: c_uint (aka c-type: UINT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetTimeout is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_uint)
    
        ret = _is_GetTimeout(_hCam, _nMode, ctypes.byref(pTimeout))
    
        return ret
    
    
    _is_GetDuration = _bind("is_GetDuration", [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)
    
    
    def is_GetDuration(self, nMode, pnTime):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_uint (aka c-type: UINT)
        :param pnTime: c_int (aka c-type: INT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetDuration is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_uint)
    
        ret = _is_GetDuration(_hCam, _nMode, ctypes.byref(pnTime))
    
        return ret
    
    
    _is_GetSensorScalerInfo = _bind("is_GetSensorScalerInfo", [ctypes.c_uint, ctypes.POINTER(SENSORSCALERINFO), ctypes.c_int], ctypes.c_int)
    
    
    def is_GetSensorScalerInfo(self, pSensorScalerInfo, nSensorScalerInfoSize):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pSensorScalerInfo: SENSORSCALERINFO (aka c-type: SENSORSCALERINFO \*)
        :param nSensorScalerInfoSize: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetSensorScalerInfo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nSensorScalerInfoSize = _value_cast(nSensorScalerInfoSize, ctypes.c_int)
    
        ret = _is_GetSensorScalerInfo(_hCam, ctypes.byref(pSensorScalerInfo), _nSensorScalerInfoSize)
    
        return ret
    
    
    _is_SetSensorScaler = _bind("is_SetSensorScaler", [ctypes.c_uint, ctypes.c_uint, ctypes.c_double], ctypes.c_int)
    
    
    def is_SetSensorScaler(self, nMode, dblFactor):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_uint (aka c-type: UINT)
        :param dblFactor: c_double (aka c-type: double)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetSensorScaler is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_uint)
        _dblFactor = _value_cast(dblFactor, ctypes.c_double)
    
        ret = _is_SetSensorScaler(_hCam, _nMode, _dblFactor)
    
        return ret
    
    
    _is_GetImageInfo = _bind("is_GetImageInfo", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(UEYEIMAGEINFO), ctypes.c_int], ctypes.c_int)
    
    
    def is_GetImageInfo(self, nImageBufferID, pImageInfo, nImageInfoSize):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nImageBufferID: c_int (aka c-type: INT)
        :param pImageInfo: UEYEIMAGEINFO (aka c-type: UEYEIMAGEINFO \*)
        :param nImageInfoSize: c_int (aka c-type: INT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetImageInfo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nImageBufferID = _value_cast(nImageBufferID, ctypes.c_int)
        _nImageInfoSize = _value_cast(nImageInfoSize, ctypes.c_int)
    
        ret = _is_GetImageInfo(_hCam, _nImageBufferID, ctypes.byref(pImageInfo), _nImageInfoSize)
    
        return ret
    
    
    _is_ImageFormat = _bind("is_ImageFormat", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_ImageFormat(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ImageFormat is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_ImageFormat(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_FaceDetection = _bind("is_FaceDetection", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_FaceDetection(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_FaceDetection is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_FaceDetection(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_Focus = _bind("is_Focus", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Focus(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Focus is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_Focus(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_ImageStabilization = _bind("is_ImageStabilization", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_ImageStabilization(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ImageStabilization is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_ImageStabilization(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_ScenePreset = _bind("is_ScenePreset", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_ScenePreset(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ScenePreset is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_ScenePreset(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_Zoom = _bind("is_Zoom", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Zoom(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Zoom is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_Zoom(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_Sharpness = _bind("is_Sharpness", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Sharpness(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Sharpness is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_Sharpness(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_Saturation = _bind("is_Saturation", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Saturation(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Saturation is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_Saturation(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_TriggerDebounce = _bind("is_TriggerDebounce", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_TriggerDebounce(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_TriggerDebounce is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_TriggerDebounce(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_ColorTemperature = _bind("is_ColorTemperature", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_ColorTemperature(self, nCommand, pParam, nSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param nSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ColorTemperature is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)
    
        ret = _is_ColorTemperature(_hCam, _nCommand, _pParam, _nSizeOfParam)
    
        return ret
    
    
    _is_DirectRenderer = _bind("is_DirectRenderer", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_DirectRenderer(self, nMode, pParam, SizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param SizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_DirectRenderer is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _SizeOfParam = _value_cast(SizeOfParam, ctypes.c_uint)
    
        ret = _is_DirectRenderer(_hCam, _nMode, _pParam, _SizeOfParam)
    
        return ret
    
    
    _is_HotPixel = _bind("is_HotPixel", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_HotPixel(self, nMode, pParam, SizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nMode: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param SizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_HotPixel is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nMode = _value_cast(nMode, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _SizeOfParam = _value_cast(SizeOfParam, ctypes.c_uint)
    
        ret = _is_HotPixel(_hCam, _nMode, _pParam, _SizeOfParam)
    
        return ret
    
    
    _is_AOI = _bind("is_AOI", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_AOI(self, nCommand, pParam, SizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param SizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_AOI is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _SizeOfParam = _value_cast(SizeOfParam, ctypes.c_uint)
    
        ret = _is_AOI(_hCam, _nCommand, _pParam, _SizeOfParam)
    
        return ret
    
    
    _is_Transfer = _bind("is_Transfer", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Transfer(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Transfer is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_Transfer(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_BootBoost = _bind("is_BootBoost", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_BootBoost(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_BootBoost is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_BootBoost(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_DeviceFeature = _bind("is_DeviceFeature", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_DeviceFeature(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_DeviceFeature is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_DeviceFeature(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_Exposure = _bind("is_Exposure", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Exposure(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Exposure is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_Exposure(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_Trigger = _bind("is_Trigger", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Trigger(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Trigger is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_Trigger(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_DeviceInfo = _bind("is_DeviceInfo", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_DeviceInfo(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_DeviceInfo is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_DeviceInfo(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_OptimalCameraTiming = _bind("is_OptimalCameraTiming", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_OptimalCameraTiming(self, u32Command, pParam, u32SizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param u32Command: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param u32SizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_OptimalCameraTiming is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _u32Command = _value_cast(u32Command, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _u32SizeOfParam = _value_cast(u32SizeOfParam, ctypes.c_uint)
    
        ret = _is_OptimalCameraTiming(_hCam, _u32Command, _pParam, _u32SizeOfParam)
    
        return ret
    
    
    _is_SetStarterFirmware = _bind("is_SetStarterFirmware", [ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_SetStarterFirmware(self, pcFilepath, uFilepathLen):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pcFilepath: c_char_p (aka c-type: const CHAR \*)
        :param uFilepathLen: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetStarterFirmware is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _pcFilepath = _value_cast(pcFilepath, ctypes.c_char_p)
        _uFilepathLen = _value_cast(uFilepathLen, ctypes.c_uint)
    
        ret = _is_SetStarterFirmware(_hCam, _pcFilepath, _uFilepathLen)
    
        return ret
    
    
    _is_SetPacketFilter = _bind("is_SetPacketFilter", [ctypes.c_int, ctypes.c_uint], ctypes.c_int)
    
    
    def is_SetPacketFilter(iAdapterID, uFilterSetting):
        """
        :param iAdapterID: c_int (aka c-type: INT)
        :param uFilterSetting: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_SetPacketFilter is None:
            raise NotImplementedError()
    
        _iAdapterID = _value_cast(iAdapterID, ctypes.c_int)
        _uFilterSetting = _value_cast(uFilterSetting, ctypes.c_uint)
    
        ret = _is_SetPacketFilter(_iAdapterID, _uFilterSetting)
    
        return ret
    
    
    _is_GetComportNumber = _bind("is_GetComportNumber", [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)], ctypes.c_int)
    
    
    def is_GetComportNumber(self, pComportNumber):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param pComportNumber: c_uint (aka c-type: UINT \*)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_GetComportNumber is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
    
        ret = _is_GetComportNumber(_hCam, ctypes.byref(pComportNumber))
    
        return ret
    
    
    _is_IpConfig = _bind("is_IpConfig", [ctypes.c_int, UEYE_ETH_ADDR_MAC, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_IpConfig(iID, mac, nCommand, pParam, cbSizeOfParam):
        """
        :param iID: c_int (aka c-type: INT)
        :param mac: UEYE_ETH_ADDR_MAC (aka c-type: UEYE_ETH_ADDR_MAC)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_IpConfig is None:
            raise NotImplementedError()
    
        _iID = _value_cast(iID, ctypes.c_int)
        _mac = mac
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_IpConfig(_iID, _mac, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_Configuration = _bind("is_Configuration", [ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Configuration(nCommand, pParam, cbSizeOfParam):
        """
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Configuration is None:
            raise NotImplementedError()
    
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_Configuration(_nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_IO = _bind("is_IO", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_IO(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_IO is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_IO(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_AutoParameter = _bind("is_AutoParameter", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_AutoParameter(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_AutoParameter is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_AutoParameter(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_Convert = _bind("is_Convert", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Convert(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Convert is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_Convert(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_ParameterSet = _bind("is_ParameterSet", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_ParameterSet(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ParameterSet is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_ParameterSet(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_EdgeEnhancement = _bind("is_EdgeEnhancement", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_EdgeEnhancement(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_EdgeEnhancement is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_EdgeEnhancement(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_PixelClock = _bind("is_PixelClock", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_PixelClock(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_PixelClock is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_PixelClock(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_ImageFile = _bind("is_ImageFile", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_ImageFile(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ImageFile is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_ImageFile(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_Blacklevel = _bind("is_Blacklevel", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Blacklevel(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Blacklevel is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_Blacklevel(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_ImageBuffer = _bind("is_ImageBuffer", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_ImageBuffer(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_ImageBuffer is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_ImageBuffer(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_Measure = _bind("is_Measure", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Measure(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Measure is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_Measure(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_LUT = _bind("is_LUT", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_LUT(self, nCommand, pParam, cbSizeOfParams):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParams: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_LUT is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParams = _value_cast(cbSizeOfParams, ctypes.c_uint)
    
        ret = _is_LUT(_hCam, _nCommand, _pParam, _cbSizeOfParams)
    
        return ret
    
    
    _is_Gamma = _bind("is_Gamma", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Gamma(self, nCommand, pParam, cbSizeOfParams):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParams: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Gamma is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParams = _value_cast(cbSizeOfParams, ctypes.c_uint)
    
        ret = _is_Gamma(_hCam, _nCommand, _pParam, _cbSizeOfParams)
    
        return ret
    
    
    _is_Memory = _bind("is_Memory", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Memory(hf, nCommand, pParam, cbSizeOfParam):
        """
        :param hf: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Memory is None:
            raise NotImplementedError()
    
        _hf = _value_cast(hf, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_Memory(_hf, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_Multicast = _bind("is_Multicast", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Multicast(self, nCommand, pParam, cbSizeOfParams):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParams: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Multicast is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParams = _value_cast(cbSizeOfParams, ctypes.c_uint)
    
        ret = _is_Multicast(_hCam, _nCommand, _pParam, _cbSizeOfParams)
    
        return ret
    
    
    _is_Sequencer = _bind("is_Sequencer", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_Sequencer(self, nCommand, pParam, cbSizeOfParams):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParams: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_Sequencer is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParams = _value_cast(cbSizeOfParams, ctypes.c_uint)
    
        ret = _is_Sequencer(_hCam, _nCommand, _pParam, _cbSizeOfParams)
    
        return ret
    
    
    _is_PersistentMemory = _bind("is_PersistentMemory", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_PersistentMemory(self, nCommand, pParam, cbSizeOfParam):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParam: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_PersistentMemory is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)
    
        ret = _is_PersistentMemory(_hCam, _nCommand, _pParam, _cbSizeOfParam)
    
        return ret
    
    
    _is_PowerDelivery = _bind("is_PowerDelivery", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)
    
    
    def is_PowerDelivery(self, nCommand, pParam, cbSizeOfParams):
        """
        :param hCam: c_uint (aka c-type: HIDS)
        :param nCommand: c_uint (aka c-type: UINT)
        :param pParam: c_void_p (aka c-type: void \*)
        :param cbSizeOfParams: c_uint (aka c-type: UINT)
        :returns: success, or no success, that is the answer
        :raises NotImplementedError: if function could not be loaded
        """
        if _is_PowerDelivery is None:
            raise NotImplementedError()
    
        _hCam = _value_cast(self.hCam, ctypes.c_uint)
        _nCommand = _value_cast(nCommand, ctypes.c_uint)
        _pParam = _pointer_cast(pParam, ctypes.c_void_p)
        _cbSizeOfParams = _value_cast(cbSizeOfParams, ctypes.c_uint)
    
        ret = _is_PowerDelivery(_hCam, _nCommand, _pParam, _cbSizeOfParams)
    
        return ret
    
    
    
    
