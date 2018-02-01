#!/usr/bin/env python

#------------------------------------------------------------------------------
#                 PyuEye - uEye API Python bindings
#
# Copyright (c) 2017 by IDS Imaging Development Systems GmbH.
# All rights reserved.
#
# PyuEye is a lean wrapper implementation of Python function objects that
# represent uEye API functions. These bindings could be used as is.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#------------------------------------------------------------------------------

__author__     = "IDS Imaging Development Systems GmbH"
__copyright__  = "Copyright 2017, IDS Imaging Development Systems GmbH"
__maintainer__ = "IDS Imaging Development Systems GmbH"

import ctypes
import logging

from .dll import load_dll
from . import ueye


get_dll_file, _bind = load_dll("uEye_tools", ["uEye_tools_64", "uEye_tools"], "PYUEYE_TOOLS_DLL_PATH")

logger = logging.getLogger(__name__)

HIDS = ueye.c_uint



IS_FILE_ACCESS_MODE_WRITE = 0x01
IS_FILE_ACCESS_MODE_READ = 0x02
IS_AVI_CM_RGB32 = 0
IS_AVI_CM_RGB24 = 1
IS_AVI_CM_Y8 = 6
IS_AVI_CM_BAYER = 11
IS_AVI_SET_EVENT_FRAME_SAVED = 1
ISAVIERRBASE = 300
IS_AVI_NO_ERR = 0
IS_AVI_ERR_INVALID_FILE = (ISAVIERRBASE + 1)
IS_AVI_ERR_NEW_FAILED = (ISAVIERRBASE + 2)
IS_AVI_ERR_CREATESTREAM = (ISAVIERRBASE + 3)
IS_AVI_ERR_PARAMETER = (ISAVIERRBASE + 4)
IS_AVI_ERR_NO_CODEC_AVAIL = (ISAVIERRBASE + 5)
IS_AVI_ERR_INVALID_ID = (ISAVIERRBASE + 6)
IS_AVI_ERR_COMPRESS = (ISAVIERRBASE + 7)
IS_AVI_ERR_DECOMPRESS = (ISAVIERRBASE + 8)
IS_AVI_ERR_CAPTURE_RUNNING = (ISAVIERRBASE + 9)
IS_AVI_ERR_CAPTURE_NOT_RUNNING = (ISAVIERRBASE + 10)
IS_AVI_ERR_PLAY_RUNNING = (ISAVIERRBASE + 11)
IS_AVI_ERR_PLAY_NOT_RUNNING = (ISAVIERRBASE + 12)
IS_AVI_ERR_WRITE_INFO = (ISAVIERRBASE + 13)
IS_AVI_ERR_INVALID_VALUE = (ISAVIERRBASE + 14)
IS_AVI_ERR_ALLOC_MEMORY = (ISAVIERRBASE + 15)
IS_AVI_ERR_INVALID_CM = (ISAVIERRBASE + 16)
IS_AVI_ERR_COMPRESSION_RUN = (ISAVIERRBASE + 17)
IS_AVI_ERR_INVALID_SIZE = (ISAVIERRBASE + 18)
IS_AVI_ERR_INVALID_POSITION = (ISAVIERRBASE + 19)
IS_AVI_ERR_INVALID_UEYE = (ISAVIERRBASE + 20)
IS_AVI_ERR_EVENT_FAILED = (ISAVIERRBASE + 21)
IS_AVI_ERR_EXCEPTION = (ISAVIERRBASE + 22)
IS_AVI_ERR_GENERIC = (ISAVIERRBASE + 23)
IS_AVI_ERR_NOT_SUPPORTED = (ISAVIERRBASE + 24)
IS_AVI_ERR_FILE_NOT_OPEN = (ISAVIERRBASE + 25)
IS_AVI_ERR_WRITE_FAILED = (ISAVIERRBASE + 26)
IS_AVI_ERR_READ_FAILED = (ISAVIERRBASE + 27)
IS_AVI_ERR_SEEK_FAILED = (ISAVIERRBASE + 28)


_isavi_InitAVI = _bind("isavi_InitAVI", [ctypes.POINTER(ctypes.c_int), ctypes.c_uint], ctypes.c_int)


def isavi_InitAVI(pnAviID, hu):
    """
    :param pnAviID: c_int (aka c-type: INT \*)
    :param hu: c_uint (aka c-type: HIDS)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_InitAVI is None:
        raise NotImplementedError()

    _hu = ueye._value_cast(hu, ctypes.c_uint)

    ret = _isavi_InitAVI(ctypes.byref(pnAviID), _hu)

    return ret


_isavi_ExitAVI = _bind("isavi_ExitAVI", [ctypes.c_int], ctypes.c_int)


def isavi_ExitAVI(nAviID):
    """
    :param nAviID: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_ExitAVI is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)

    ret = _isavi_ExitAVI(_nAviID)

    return ret


_isavi_SetImageSize = _bind("isavi_SetImageSize", [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int], ctypes.c_int)


def isavi_SetImageSize(nAviID, cMode, Width, Height, PosX, PosY, LineOffset):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param cMode: c_int (aka c-type: INT)
    :param Width: c_int (aka c-type: INT)
    :param Height: c_int (aka c-type: INT)
    :param PosX: c_int (aka c-type: INT)
    :param PosY: c_int (aka c-type: INT)
    :param LineOffset: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_SetImageSize is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _cMode = ueye._value_cast(cMode, ctypes.c_int)
    _Width = ueye._value_cast(Width, ctypes.c_int)
    _Height = ueye._value_cast(Height, ctypes.c_int)
    _PosX = ueye._value_cast(PosX, ctypes.c_int)
    _PosY = ueye._value_cast(PosY, ctypes.c_int)
    _LineOffset = ueye._value_cast(LineOffset, ctypes.c_int)

    ret = _isavi_SetImageSize(_nAviID, _cMode, _Width, _Height, _PosX, _PosY, _LineOffset)

    return ret


_isavi_OpenAVI = _bind("isavi_OpenAVI", [ctypes.c_int, ctypes.c_char_p], ctypes.c_int)


def isavi_OpenAVI(nAviID, strFileName):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param strFileName: c_char_p (aka c-type: const char \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_OpenAVI is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _strFileName = ueye._value_cast(strFileName, ctypes.c_char_p)

    ret = _isavi_OpenAVI(_nAviID, _strFileName)

    return ret


_isavi_OpenAVIW = _bind("isavi_OpenAVIW", [ctypes.c_int, ctypes.c_wchar_p], ctypes.c_int)


def isavi_OpenAVIW(nAviID, strFileName):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param strFileName: c_wchar_p (aka c-type: const wchar_t \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_OpenAVIW is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _strFileName = ueye._value_cast(strFileName, ctypes.c_wchar_p)

    ret = _isavi_OpenAVIW(_nAviID, _strFileName)

    return ret


_isavi_StartAVI = _bind("isavi_StartAVI", [ctypes.c_int], ctypes.c_int)


def isavi_StartAVI(nAviID):
    """
    :param nAviID: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_StartAVI is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)

    ret = _isavi_StartAVI(_nAviID)

    return ret


_isavi_StopAVI = _bind("isavi_StopAVI", [ctypes.c_int], ctypes.c_int)


def isavi_StopAVI(nAviID):
    """
    :param nAviID: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_StopAVI is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)

    ret = _isavi_StopAVI(_nAviID)

    return ret


_isavi_AddFrame = _bind("isavi_AddFrame", [ctypes.c_int, ueye.c_mem_p], ctypes.c_int)


def isavi_AddFrame(nAviID, pcImageMem):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param pcImageMem: c_mem_p (aka c-type: char \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_AddFrame is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)

    ret = _isavi_AddFrame(_nAviID, pcImageMem)

    return ret


_isavi_SetFrameRate = _bind("isavi_SetFrameRate", [ctypes.c_int, ctypes.c_double], ctypes.c_int)


def isavi_SetFrameRate(nAviID, fr):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param fr: c_double (aka c-type: double)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_SetFrameRate is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _fr = ueye._value_cast(fr, ctypes.c_double)

    ret = _isavi_SetFrameRate(_nAviID, _fr)

    return ret


_isavi_SetImageQuality = _bind("isavi_SetImageQuality", [ctypes.c_int, ctypes.c_int], ctypes.c_int)


def isavi_SetImageQuality(nAviID, q):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param q: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_SetImageQuality is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _q = ueye._value_cast(q, ctypes.c_int)

    ret = _isavi_SetImageQuality(_nAviID, _q)

    return ret


_isavi_GetAVISize = _bind("isavi_GetAVISize", [ctypes.c_int, ctypes.POINTER(ctypes.c_float)], ctypes.c_int)


def isavi_GetAVISize(nAviID, size):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param size: c_float (aka c-type: float \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_GetAVISize is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)

    ret = _isavi_GetAVISize(_nAviID, ctypes.byref(size))

    return ret


_isavi_GetAVIFileName = _bind("isavi_GetAVIFileName", [ctypes.c_int, ctypes.c_char_p], ctypes.c_int)


def isavi_GetAVIFileName(nAviID, strName):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param strName: c_char_p (aka c-type: char \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_GetAVIFileName is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _strName = ueye._value_cast(strName, ctypes.c_char_p)

    ret = _isavi_GetAVIFileName(_nAviID, _strName)

    return ret


_isavi_GetAVIFileNameW = _bind("isavi_GetAVIFileNameW", [ctypes.c_int, ctypes.c_wchar_p], ctypes.c_int)


def isavi_GetAVIFileNameW(nAviID, strName):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param strName: c_wchar_p (aka c-type: wchar_t \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_GetAVIFileNameW is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _strName = ueye._value_cast(strName, ctypes.c_wchar_p)

    ret = _isavi_GetAVIFileNameW(_nAviID, _strName)

    return ret


_isavi_GetnCompressedFrames = _bind("isavi_GetnCompressedFrames", [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)], ctypes.c_int)


def isavi_GetnCompressedFrames(nAviID, nFrames):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param nFrames: c_uint (aka c-type: unsigned long \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_GetnCompressedFrames is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)

    ret = _isavi_GetnCompressedFrames(_nAviID, ctypes.byref(nFrames))

    return ret


_isavi_GetnLostFrames = _bind("isavi_GetnLostFrames", [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)], ctypes.c_int)


def isavi_GetnLostFrames(nAviID, nLostFrames):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param nLostFrames: c_uint (aka c-type: unsigned long \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_GetnLostFrames is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)

    ret = _isavi_GetnLostFrames(_nAviID, ctypes.byref(nLostFrames))

    return ret


_isavi_ResetFrameCounters = _bind("isavi_ResetFrameCounters", [ctypes.c_int], ctypes.c_int)


def isavi_ResetFrameCounters(nAviID):
    """
    :param nAviID: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_ResetFrameCounters is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)

    ret = _isavi_ResetFrameCounters(_nAviID)

    return ret


_isavi_CloseAVI = _bind("isavi_CloseAVI", [ctypes.c_int], ctypes.c_int)


def isavi_CloseAVI(nAviID):
    """
    :param nAviID: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_CloseAVI is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)

    ret = _isavi_CloseAVI(_nAviID)

    return ret


_isavi_InitEvent = _bind("isavi_InitEvent", [ctypes.c_int, ctypes.c_void_p, ctypes.c_int], ctypes.c_int)


def isavi_InitEvent(nAviID, hEv, which):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param hEv: c_void_p (aka c-type: HANDLE)
    :param which: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_InitEvent is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _hEv = ueye._pointer_cast(hEv, ctypes.c_void_p)
    _which = ueye._value_cast(which, ctypes.c_int)

    ret = _isavi_InitEvent(_nAviID, _hEv, _which)

    return ret


_isavi_EnableEvent = _bind("isavi_EnableEvent", [ctypes.c_int, ctypes.c_int], ctypes.c_int)


def isavi_EnableEvent(nAviID, which):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param which: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_EnableEvent is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _which = ueye._value_cast(which, ctypes.c_int)

    ret = _isavi_EnableEvent(_nAviID, _which)

    return ret


_isavi_DisableEvent = _bind("isavi_DisableEvent", [ctypes.c_int, ctypes.c_int], ctypes.c_int)


def isavi_DisableEvent(nAviID, which):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param which: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_DisableEvent is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _which = ueye._value_cast(which, ctypes.c_int)

    ret = _isavi_DisableEvent(_nAviID, _which)

    return ret


_isavi_ExitEvent = _bind("isavi_ExitEvent", [ctypes.c_int, ctypes.c_int], ctypes.c_int)


def isavi_ExitEvent(nAviID, which):
    """
    :param nAviID: c_int (aka c-type: INT)
    :param which: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _isavi_ExitEvent is None:
        raise NotImplementedError()

    _nAviID = ueye._value_cast(nAviID, ctypes.c_int)
    _which = ueye._value_cast(which, ctypes.c_int)

    ret = _isavi_ExitEvent(_nAviID, _which)

    return ret


_israw_InitFile = _bind("israw_InitFile", [ctypes.POINTER(ctypes.c_uint), ctypes.c_int], ctypes.c_int)


def israw_InitFile(punFileID, nAccessMode):
    """
    :param punFileID: c_uint (aka c-type: UINT \*)
    :param nAccessMode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_InitFile is None:
        raise NotImplementedError()

    _nAccessMode = ueye._value_cast(nAccessMode, ctypes.c_int)

    ret = _israw_InitFile(ctypes.byref(punFileID), _nAccessMode)

    return ret


_israw_ExitFile = _bind("israw_ExitFile", [ctypes.c_uint], ctypes.c_int)


def israw_ExitFile(unFileID):
    """
    :param unFileID: c_uint (aka c-type: UINT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_ExitFile is None:
        raise NotImplementedError()

    _unFileID = ueye._value_cast(unFileID, ctypes.c_uint)

    ret = _israw_ExitFile(_unFileID)

    return ret


_israw_SetImageInfo = _bind("israw_SetImageInfo", [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], ctypes.c_int)


def israw_SetImageInfo(unFileID, unWidth, unHeight, unBitsPerPixel):
    """
    :param unFileID: c_uint (aka c-type: UINT)
    :param unWidth: c_uint (aka c-type: UINT)
    :param unHeight: c_uint (aka c-type: UINT)
    :param unBitsPerPixel: c_uint (aka c-type: UINT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_SetImageInfo is None:
        raise NotImplementedError()

    _unFileID = ueye._value_cast(unFileID, ctypes.c_uint)
    _unWidth = ueye._value_cast(unWidth, ctypes.c_uint)
    _unHeight = ueye._value_cast(unHeight, ctypes.c_uint)
    _unBitsPerPixel = ueye._value_cast(unBitsPerPixel, ctypes.c_uint)

    ret = _israw_SetImageInfo(_unFileID, _unWidth, _unHeight, _unBitsPerPixel)

    return ret


_israw_GetImageInfo = _bind("israw_GetImageInfo", [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)], ctypes.c_int)


def israw_GetImageInfo(unFileID, punWidth, punHeight, punBitsPerPixel):
    """
    :param unFileID: c_uint (aka c-type: UINT)
    :param punWidth: c_uint (aka c-type: UINT \*)
    :param punHeight: c_uint (aka c-type: UINT \*)
    :param punBitsPerPixel: c_uint (aka c-type: UINT \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_GetImageInfo is None:
        raise NotImplementedError()

    _unFileID = ueye._value_cast(unFileID, ctypes.c_uint)

    ret = _israw_GetImageInfo(_unFileID, ctypes.byref(punWidth), ctypes.byref(punHeight), ctypes.byref(punBitsPerPixel))

    return ret


_israw_OpenFile = _bind("israw_OpenFile", [ctypes.c_uint, ctypes.c_char_p], ctypes.c_int)


def israw_OpenFile(unFileID, strFileName):
    """
    :param unFileID: c_uint (aka c-type: UINT)
    :param strFileName: c_char_p (aka c-type: const char \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_OpenFile is None:
        raise NotImplementedError()

    _unFileID = ueye._value_cast(unFileID, ctypes.c_uint)
    _strFileName = ueye._value_cast(strFileName, ctypes.c_char_p)

    ret = _israw_OpenFile(_unFileID, _strFileName)

    return ret


_israw_CloseFile = _bind("israw_CloseFile", [ctypes.c_uint], ctypes.c_int)


def israw_CloseFile(unFileID):
    """
    :param unFileID: c_uint (aka c-type: UINT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_CloseFile is None:
        raise NotImplementedError()

    _unFileID = ueye._value_cast(unFileID, ctypes.c_uint)

    ret = _israw_CloseFile(_unFileID)

    return ret


_israw_AddFrame = _bind("israw_AddFrame", [ctypes.c_uint, ueye.c_mem_p, ctypes.c_longlong], ctypes.c_int)


def israw_AddFrame(unFileID, pcData, unTimestampDevice):
    """
    :param unFileID: c_uint (aka c-type: UINT)
    :param pcData: c_mem_p (aka c-type: const char \*)
    :param unTimestampDevice: c_longlong (aka c-type: UINT64)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_AddFrame is None:
        raise NotImplementedError()

    _unFileID = ueye._value_cast(unFileID, ctypes.c_uint)
    _unTimestampDevice = ueye._value_cast(unTimestampDevice, ctypes.c_longlong)

    ret = _israw_AddFrame(_unFileID, pcData, _unTimestampDevice)

    return ret


_israw_GetFrame = _bind("israw_GetFrame", [ctypes.c_uint, ueye.c_mem_p, ctypes.POINTER(ctypes.c_longlong)], ctypes.c_int)


def israw_GetFrame(unFileID, pData, punTimestampDevice):
    """
    :param unFileID: c_uint (aka c-type: UINT)
    :param pData: c_mem_p (aka c-type: char \*)
    :param punTimestampDevice: c_longlong (aka c-type: UINT64 \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_GetFrame is None:
        raise NotImplementedError()

    _unFileID = ueye._value_cast(unFileID, ctypes.c_uint)

    ret = _israw_GetFrame(_unFileID, pData, ctypes.byref(punTimestampDevice))

    return ret


_israw_SeekFrame = _bind("israw_SeekFrame", [ctypes.c_uint, ctypes.c_uint], ctypes.c_int)


def israw_SeekFrame(unFileID, unFrame):
    """
    :param unFileID: c_uint (aka c-type: UINT)
    :param unFrame: c_uint (aka c-type: UINT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_SeekFrame is None:
        raise NotImplementedError()

    _unFileID = ueye._value_cast(unFileID, ctypes.c_uint)
    _unFrame = ueye._value_cast(unFrame, ctypes.c_uint)

    ret = _israw_SeekFrame(_unFileID, _unFrame)

    return ret


_israw_GetSize = _bind("israw_GetSize", [ctypes.c_uint, ctypes.POINTER(ctypes.c_float)], ctypes.c_int)


def israw_GetSize(unFileID, pfSize):
    """
    :param unFileID: c_uint (aka c-type: UINT)
    :param pfSize: c_float (aka c-type: float \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _israw_GetSize is None:
        raise NotImplementedError()

    _unFileID = ueye._value_cast(unFileID, ctypes.c_uint)

    ret = _israw_GetSize(_unFileID, ctypes.byref(pfSize))

    return ret




