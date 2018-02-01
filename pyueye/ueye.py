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

from __future__ import division

__author__     = "IDS Imaging Development Systems GmbH"
__copyright__  = "Copyright 2017, IDS Imaging Development Systems GmbH"
__maintainer__ = "IDS Imaging Development Systems GmbH"

import ctypes
import enum
import logging
import sys

try:
    import numpy
except ImportError:
    numpy = None

from .dll import load_dll

get_dll_file, _bind = load_dll("ueye_api", ["ueye_api_64", "ueye_api"], "PYUEYE_DLL_PATH")

logger = logging.getLogger(__name__)

create_string_buffer = ctypes.create_string_buffer
create_unicode_buffer = ctypes.create_unicode_buffer
memmove = ctypes.memmove


def new_mem_p(size):
    _size = size
    
    if isinstance(size, ctypes._SimpleCData):
        _size = size.value
    
    return ctypes.cast(ctypes.create_string_buffer(_size), c_mem_p)


def sizeof(obj_or_type):
    _obj_or_type = obj_or_type
    
    if isinstance(obj_or_type, _CtypesEnum):
        _obj_or_type = ctypes.c_uint(obj_or_type.value)
        
    return ctypes.sizeof(_obj_or_type)


def get_data(image_mem, x, y, bits, pitch, copy):
    data = None

    if copy:
        mem = ctypes.create_string_buffer(y * pitch)
        ctypes.memmove(mem, image_mem, y * pitch)
        data = numpy.frombuffer(mem, dtype = numpy.uint8) if numpy else mem
    else:
        data = numpy.ctypeslib.as_array(ctypes.cast(image_mem, ctypes.POINTER(ctypes.c_ubyte)), (y * pitch, )) if numpy else image_mem

    return data


def _pointer_cast(from_obj, to_type):
    _to_obj = from_obj

    if from_obj is not None and not isinstance(from_obj, to_type):
        if isinstance(from_obj, ctypes.c_void_p) or isinstance(from_obj, ctypes.c_wchar_p) or \
            isinstance(from_obj, ctypes.c_char_p) or isinstance(from_obj, ctypes.Array):
            _to_obj = ctypes.cast(from_obj, to_type)
        else:
            _to_obj = ctypes.cast(ctypes.pointer(from_obj), to_type)

    return _to_obj


def _value_cast(from_obj, to_type):
    _to_obj = from_obj

    if not isinstance(from_obj, ctypes._SimpleCData):
        _to_obj = to_type(from_obj)
    elif not isinstance(from_obj, to_type):
        _to_obj = to_type(from_obj.value)

    return _to_obj


_bool = bool
_int = int
_float = float    

if sys.version_info > (3,):
    _long = _int
else:
    _long = long
    
    
class _IntEnum(_long, enum.Enum):
    """ """
    
    pass


class _CtypesEnum(_IntEnum):
    @classmethod
    def from_param(cls, obj):
        return _long(obj)


class _PointerMixin(object):
    """
    """
    __slots__ = ()

    def __int__(self):
        """
        """
        return _int(self.value)

    def __long__(self):
        """
        """
        return _long(self.value)

    def __eq__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 == value2

    def __ne__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 != value2


class _StructureAndUnionMixin(object):
    """
    """
    __slots__ = ()
    _map = {}

    def __getattribute__(self, name):
        """
        """
        _map = ctypes.Structure.__getattribute__(self, '_map')
        value = ctypes.Structure.__getattribute__(self, name)
        
        if name in _map:
            EnumClass = _map[name]
        
            if isinstance(value, ctypes.Array):
                return [EnumClass(x) for x in value]
            else:
                return EnumClass(value)
        else:
            return value

    def __str__(self):
        """
        """
        result = []
        result.append("struct {0} {{".format(self.__class__.__name__))
        
        for field in self._fields_:
            attr_name, attr_type = field
        
            if attr_name in self._map:
                attr_type = self._map[attr_name]
        
            value = getattr(self, attr_name)
            result.append("    {0} [{1}] = {2!r};".format(attr_name, attr_type.__name__, value))
        
        result.append("};")
        return '\n'.join(result)

    __repr__ = __str__

    def __eq__(self, other):
        """
        """
        for field in self._fields_:
            attr_name = field[0]
        
            a = getattr(self, attr_name)
        
            try:
                b = getattr(other, attr_name)
            except AttributeError:
                return False
        
            if isinstance(a, ctypes.Array) and a[:] != b[:]:
                return False
            elif isinstance(a, ctypes._Pointer):
                try:
                    a_value = a.contents
                except ValueError:
                    a_value = None
        
                try:
                    b_value = b.contents
                except ValueError:
                    b_value = None
        
                if a_value != b_value:
                    return False
            elif a != b:
                return False
        
        return True

    def __ne__(self, other):
        """
        """
        for field in self._fields_:
            attr_name = field[0]
        
            a = getattr(self, attr_name)
        
            try:
                b = getattr(other, attr_name)
            except AttributeError:
                return True
        
            if isinstance(a, ctypes.Array) and a[:] != b[:]:
                return True
            elif isinstance(a, ctypes._Pointer):
                try:
                    a_value = a.contents
                except ValueError:
                    a_value = None
        
                try:
                    b_value = b.contents
                except ValueError:
                    b_value = None
        
                if a_value != b_value:
                    return True
            elif a != b:
                return True
        
        return False


class _StringMixin(object):
    """
    """
    __slots__ = ()

    def __str__(self):
        """
        """
        return str(self.value)


class _CompareMixin(object):
    """
    """
    __slots__ = ()

    def __eq__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 == value2

    def __ne__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 != value2

    def __lt__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 < value2

    def __le__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 <= value2

    def __gt__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 > value2

    def __ge__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 >= value2

    def __bool__(self):
        """
        """
        return _bool(0 < self.value)


class _ConvertMixin(object):
    """
    """
    __slots__ = ()

    def __int__(self):
        """
        """
        return _int(self.value)

    def __long__(self):
        """
        """
        return _long(self.value)

    def __float__(self):
        """
        """
        return _float(self.value)

    def __complex__(self):
        """
        """
        return complex(self.value)

    def __coerce__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        if isinstance(value1, _float):
            return value1, _float(value2)
        elif isinstance(value2, _float):
            return _float(value1), value2
        
        return _int(value1), _int(value2)


class _NumberMixin(object):
    """
    """
    __slots__ = ()

    def __hex__(self):
        """
        """
        return hex(self.value)

    def __oct__(self):
        """
        """
        return oct(self.value)

    def __pos__(self):
        """
        """
        return self

    def __neg__(self):
        """
        """
        return type(self)(-self.value)

    def __abs__(self):
        """
        """
        return type(self)(abs(self.value))

    def __invert__(self):
        """
        """
        return type(self)(~self.value)

    def __add__(self, other):
        """
        """
        summand1 = self.value
        summand2 = 0
        
        try:
            summand2 = other.value
        except AttributeError:
            try:
                summand2 = other
            except TypeError:
                return NotImplemented
        
        return summand1 + summand2

    def __radd__(self, other):
        """
        """
        return self + other

    def __sub__(self, other):
        """
        """
        minuend = self.value
        subtrahend = 0
        
        try:
            subtrahend = other.value
        except AttributeError:
            try:
                subtrahend = other
            except TypeError:
                return NotImplemented
        
        return minuend - subtrahend

    def __rsub__(self, other):
        """
        """
        minuend = 0
        subtrahend = self.value
        
        try:
            minuend = other.value
        except AttributeError:
            try:
                minuend = other
            except TypeError:
                return NotImplemented
        
        return minuend - subtrahend

    def __mul__(self, other):
        """
        """
        multiplikand = self.value
        multiplikator = 0
        
        try:
            multiplikator = other.value
        except AttributeError:
            try:
                multiplikator = other
            except TypeError:
                return NotImplemented
        
        return multiplikand * multiplikator

    def __rmul__(self, other):
        """
        """
        return self * other

    def __truediv__(self, other):
        """
        """
        dividend = self.value
        divisor = 0
        
        try:
            divisor = other.value
        except AttributeError:
            try:
                divisor = other
            except TypeError:
                return NotImplemented
        
        return dividend / divisor

    def __rtruediv__(self, other):
        """
        """
        dividend = 0
        divisor = self.value
        
        try:
            dividend = other.value
        except AttributeError:
            try:
                dividend = other
            except TypeError:
                return NotImplemented
        
        return dividend / divisor

    def __floordiv__(self, other):
        """
        """
        dividend = self.value
        divisor = 0
        
        try:
            divisor = other.value
        except AttributeError:
            try:
                divisor = other
            except TypeError:
                return NotImplemented
        
        return dividend // divisor

    def __rfloordiv__(self, other):
        """
        """
        dividend = 0
        divisor = self.value
        
        try:
            dividend = other.value
        except AttributeError:
            try:
                dividend = other
            except TypeError:
                return NotImplemented
        
        return dividend // divisor

    def __and__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 & value2

    def __rand__(self, other):
        """
        """
        return self & other

    def __or__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 | value2

    def __ror__(self, other):
        """
        """
        return self | other

    def __xor__(self, other):
        """
        """
        value1 = self.value
        value2 = 0
        
        try:
            value2 = other.value
        except AttributeError:
            try:
                value2 = other
            except TypeError:
                return NotImplemented
        
        return value1 ^ value2

    def __xror__(self, other):
        """
        """
        return self ^ other

    def __iadd__(self, other):
        """
        """
        summand = 0
        
        try:
            summand = other.value
        except AttributeError:
            try:
                summand = other
            except TypeError:
                return NotImplemented
        
        self.value += summand
        
        return self

    def __isub__(self, other):
        """
        """
        subtrahend = 0
        
        try:
            subtrahend = other.value
        except AttributeError:
            try:
                subtrahend = other
            except TypeError:
                return NotImplemented
        
        self.value -= subtrahend
        
        return self

    def __imul__(self, other):
        """
        """
        multiplikator = 0
        
        try:
            multiplikator = other.value
        except AttributeError:
            try:
                multiplikator = other
            except TypeError:
                return NotImplemented
        
        self.value *= multiplikator
        
        return self

    def __itruediv__(self, other):
        """
        """
        divisor = 0
        
        try:
            divisor = other.value
        except AttributeError:
            try:
                divisor = other
            except TypeError:
                return NotImplemented
        
        try:
            self.value /= divisor
        except TypeError:
            self.value //= divisor
        
        return self

    def __ifloordiv__(self, other):
        """
        """
        divisor = 0
        
        try:
            divisor = other.value
        except AttributeError:
            try:
                divisor = other
            except TypeError:
                return NotImplemented
        
        self.value //= divisor
        
        return self

    def __iand__(self, other):
        """
        """
        value = 0
        
        try:
            value = other.value
        except AttributeError:
            try:
                value = other
            except TypeError:
                return NotImplemented
        
        self.value &= value
        
        return self

    def __ior__(self, other):
        """
        """
        value = 0
        
        try:
            value = other.value
        except AttributeError:
            try:
                value = other
            except TypeError:
                return NotImplemented
        
        self.value |= value
        
        return self

    def __ixor__(self, other):
        """
        """
        value = 0
        
        try:
            value = other.value
        except AttributeError:
            try:
                value = other
            except TypeError:
                return NotImplemented
        
        self.value ^= value
        
        return self


class c_ulonglong(ctypes.c_ulonglong, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


ulonglong = c_ulonglong
ULONGLONG = c_ulonglong
UINT64 = c_ulonglong
uint64_t = c_ulonglong


class c_void_p(ctypes.c_void_p, _PointerMixin):
    """
    Ctypes wrapper with additional functionality
    """


void_p = c_void_p
LPCVOID = c_void_p
LPVOID = c_void_p
HWND = c_void_p
HANDLE = c_void_p
HDC = c_void_p


class c_int(ctypes.c_int, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


int = c_int
INT = c_int
BOOL = c_int
LONG = c_int
int32_t = c_int


class c_double(ctypes.c_double, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


double = c_double
DOUBLE = c_double


class c_ssize_t(ctypes.c_ssize_t, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


ssize_t = c_ssize_t


class c_ulong(ctypes.c_ulong, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


ulong = c_ulong


class c_wchar_p(ctypes.c_wchar_p, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


wchar_p = c_wchar_p
LPCWSTR = c_wchar_p
LPWSTR = c_wchar_p


class c_float(ctypes.c_float, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


float = c_float
FLOAT = c_float


class c_long(ctypes.c_long, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


long = c_long


class c_size_t(ctypes.c_size_t, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


size_t = c_size_t


class c_char(ctypes.c_char):
    """
    Ctypes wrapper with additional functionality
    """


char = c_char
CHAR = c_char


class _Structure(ctypes.Structure, _StructureAndUnionMixin):
    """
    Ctypes wrapper with additional functionality
    """


class c_mem_p(ctypes.c_void_p, _PointerMixin):
    """
    Ctypes wrapper with additional functionality
    """


mem_p = c_mem_p


class c_char_p(ctypes.c_char_p, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


char_p = c_char_p
LPCSTR = c_char_p
LPSTR = c_char_p


class c_longlong(ctypes.c_longlong, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


longlong = c_longlong
LONGLONG = c_longlong
INT64 = c_longlong
int64_t = c_longlong


class c_byte(ctypes.c_byte, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


byte = c_byte
int8_t = c_byte


class c_ubyte(ctypes.c_ubyte, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


ubyte = c_ubyte
BYTE = c_ubyte
BOOLEAN = c_ubyte
uint8_t = c_ubyte


class c_short(ctypes.c_short, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


short = c_short
SHORT = c_short
int16_t = c_short


class c_wchar(ctypes.c_wchar):
    """
    Ctypes wrapper with additional functionality
    """


wchar = c_wchar
WCHAR = c_wchar


class c_bool(ctypes.c_bool, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


bool = c_bool


class c_uint(ctypes.c_uint, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


uint = c_uint
UINT = c_uint
DWORD = c_uint
HIDS = c_uint
ULONG = c_uint
uint32_t = c_uint


class _Union(ctypes.Union, _StructureAndUnionMixin):
    """
    Ctypes wrapper with additional functionality
    """


class c_longdouble(ctypes.c_longdouble, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


longdouble = c_longdouble


class c_ushort(ctypes.c_ushort, _ConvertMixin, _CompareMixin, _NumberMixin, _StringMixin):
    """
    Ctypes wrapper with additional functionality
    """


ushort = c_ushort
WORD = c_ushort
USHORT = c_ushort
uint16_t = c_ushort


class BAYER_PIXEL(_CtypesEnum):
    BAYER_PIXEL_RED = 0
    BAYER_PIXEL_GREEN = 1
    BAYER_PIXEL_BLUE = 2


BAYER_PIXEL_RED = BAYER_PIXEL.BAYER_PIXEL_RED
BAYER_PIXEL_GREEN = BAYER_PIXEL.BAYER_PIXEL_GREEN
BAYER_PIXEL_BLUE = BAYER_PIXEL.BAYER_PIXEL_BLUE


class UEYE_CAPTURE_STATUS(_CtypesEnum):
    IS_CAP_STATUS_API_NO_DEST_MEM = 162
    IS_CAP_STATUS_API_CONVERSION_FAILED = 163
    IS_CAP_STATUS_API_IMAGE_LOCKED = 165
    IS_CAP_STATUS_DRV_OUT_OF_BUFFERS = 178
    IS_CAP_STATUS_DRV_DEVICE_NOT_READY = 180
    IS_CAP_STATUS_USB_TRANSFER_FAILED = 199
    IS_CAP_STATUS_DEV_MISSED_IMAGES = 229
    IS_CAP_STATUS_DEV_TIMEOUT = 214
    IS_CAP_STATUS_DEV_FRAME_CAPTURE_FAILED = 217
    IS_CAP_STATUS_ETH_BUFFER_OVERRUN = 228
    IS_CAP_STATUS_ETH_MISSED_IMAGES = 229


IS_CAP_STATUS_API_NO_DEST_MEM = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_API_NO_DEST_MEM
IS_CAP_STATUS_API_CONVERSION_FAILED = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_API_CONVERSION_FAILED
IS_CAP_STATUS_API_IMAGE_LOCKED = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_API_IMAGE_LOCKED
IS_CAP_STATUS_DRV_OUT_OF_BUFFERS = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_DRV_OUT_OF_BUFFERS
IS_CAP_STATUS_DRV_DEVICE_NOT_READY = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_DRV_DEVICE_NOT_READY
IS_CAP_STATUS_USB_TRANSFER_FAILED = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_USB_TRANSFER_FAILED
IS_CAP_STATUS_DEV_MISSED_IMAGES = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_DEV_MISSED_IMAGES
IS_CAP_STATUS_DEV_TIMEOUT = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_DEV_TIMEOUT
IS_CAP_STATUS_DEV_FRAME_CAPTURE_FAILED = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_DEV_FRAME_CAPTURE_FAILED
IS_CAP_STATUS_ETH_BUFFER_OVERRUN = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_ETH_BUFFER_OVERRUN
IS_CAP_STATUS_ETH_MISSED_IMAGES = UEYE_CAPTURE_STATUS.IS_CAP_STATUS_ETH_MISSED_IMAGES


class CAPTURE_STATUS_CMD(_CtypesEnum):
    IS_CAPTURE_STATUS_INFO_CMD_RESET = 1
    IS_CAPTURE_STATUS_INFO_CMD_GET = 2
    IS_CAPTURE_STATUS_CRC_ERROR_COUNT_GET = 3


IS_CAPTURE_STATUS_INFO_CMD_RESET = CAPTURE_STATUS_CMD.IS_CAPTURE_STATUS_INFO_CMD_RESET
IS_CAPTURE_STATUS_INFO_CMD_GET = CAPTURE_STATUS_CMD.IS_CAPTURE_STATUS_INFO_CMD_GET
IS_CAPTURE_STATUS_CRC_ERROR_COUNT_GET = CAPTURE_STATUS_CMD.IS_CAPTURE_STATUS_CRC_ERROR_COUNT_GET


class AUTO_SHUTTER_PHOTOM(_CtypesEnum):
    AS_PM_NONE = 0
    AS_PM_SENS_CENTER_WEIGHTED = 1
    AS_PM_SENS_CENTER_SPOT = 2
    AS_PM_SENS_PORTRAIT = 4
    AS_PM_SENS_LANDSCAPE = 8
    AS_PM_SENS_CENTER_AVERAGE = 16


AS_PM_NONE = AUTO_SHUTTER_PHOTOM.AS_PM_NONE
AS_PM_SENS_CENTER_WEIGHTED = AUTO_SHUTTER_PHOTOM.AS_PM_SENS_CENTER_WEIGHTED
AS_PM_SENS_CENTER_SPOT = AUTO_SHUTTER_PHOTOM.AS_PM_SENS_CENTER_SPOT
AS_PM_SENS_PORTRAIT = AUTO_SHUTTER_PHOTOM.AS_PM_SENS_PORTRAIT
AS_PM_SENS_LANDSCAPE = AUTO_SHUTTER_PHOTOM.AS_PM_SENS_LANDSCAPE
AS_PM_SENS_CENTER_AVERAGE = AUTO_SHUTTER_PHOTOM.AS_PM_SENS_CENTER_AVERAGE


class AUTO_GAIN_PHOTOM(_CtypesEnum):
    AG_PM_NONE = 0
    AG_PM_SENS_CENTER_WEIGHTED = 1
    AG_PM_SENS_CENTER_SPOT = 2
    AG_PM_SENS_PORTRAIT = 4
    AG_PM_SENS_LANDSCAPE = 8


AG_PM_NONE = AUTO_GAIN_PHOTOM.AG_PM_NONE
AG_PM_SENS_CENTER_WEIGHTED = AUTO_GAIN_PHOTOM.AG_PM_SENS_CENTER_WEIGHTED
AG_PM_SENS_CENTER_SPOT = AUTO_GAIN_PHOTOM.AG_PM_SENS_CENTER_SPOT
AG_PM_SENS_PORTRAIT = AUTO_GAIN_PHOTOM.AG_PM_SENS_PORTRAIT
AG_PM_SENS_LANDSCAPE = AUTO_GAIN_PHOTOM.AG_PM_SENS_LANDSCAPE


class ANTI_FLICKER_MODE(_CtypesEnum):
    ANTIFLCK_MODE_OFF = 0
    ANTIFLCK_MODE_SENS_AUTO = 1
    ANTIFLCK_MODE_SENS_50_FIXED = 2
    ANTIFLCK_MODE_SENS_60_FIXED = 4


ANTIFLCK_MODE_OFF = ANTI_FLICKER_MODE.ANTIFLCK_MODE_OFF
ANTIFLCK_MODE_SENS_AUTO = ANTI_FLICKER_MODE.ANTIFLCK_MODE_SENS_AUTO
ANTIFLCK_MODE_SENS_50_FIXED = ANTI_FLICKER_MODE.ANTIFLCK_MODE_SENS_50_FIXED
ANTIFLCK_MODE_SENS_60_FIXED = ANTI_FLICKER_MODE.ANTIFLCK_MODE_SENS_60_FIXED


class WHITEBALANCE_MODE(_CtypesEnum):
    WB_MODE_DISABLE = 0
    WB_MODE_AUTO = 1
    WB_MODE_ALL_PULLIN = 2
    WB_MODE_INCANDESCENT_LAMP = 4
    WB_MODE_FLUORESCENT_DL = 8
    WB_MODE_OUTDOOR_CLEAR_SKY = 16
    WB_MODE_OUTDOOR_CLOUDY = 32
    WB_MODE_FLUORESCENT_LAMP = 64
    WB_MODE_FLUORESCENT_NL = 128


WB_MODE_DISABLE = WHITEBALANCE_MODE.WB_MODE_DISABLE
WB_MODE_AUTO = WHITEBALANCE_MODE.WB_MODE_AUTO
WB_MODE_ALL_PULLIN = WHITEBALANCE_MODE.WB_MODE_ALL_PULLIN
WB_MODE_INCANDESCENT_LAMP = WHITEBALANCE_MODE.WB_MODE_INCANDESCENT_LAMP
WB_MODE_FLUORESCENT_DL = WHITEBALANCE_MODE.WB_MODE_FLUORESCENT_DL
WB_MODE_OUTDOOR_CLEAR_SKY = WHITEBALANCE_MODE.WB_MODE_OUTDOOR_CLEAR_SKY
WB_MODE_OUTDOOR_CLOUDY = WHITEBALANCE_MODE.WB_MODE_OUTDOOR_CLOUDY
WB_MODE_FLUORESCENT_LAMP = WHITEBALANCE_MODE.WB_MODE_FLUORESCENT_LAMP
WB_MODE_FLUORESCENT_NL = WHITEBALANCE_MODE.WB_MODE_FLUORESCENT_NL


class UEYE_GET_ESTIMATED_TIME_MODE(_CtypesEnum):
    IS_SE_STARTER_FW_UPLOAD = 1
    IS_CP_STARTER_FW_UPLOAD = 2
    IS_STARTER_FW_UPLOAD = 4


IS_SE_STARTER_FW_UPLOAD = UEYE_GET_ESTIMATED_TIME_MODE.IS_SE_STARTER_FW_UPLOAD
IS_CP_STARTER_FW_UPLOAD = UEYE_GET_ESTIMATED_TIME_MODE.IS_CP_STARTER_FW_UPLOAD
IS_STARTER_FW_UPLOAD = UEYE_GET_ESTIMATED_TIME_MODE.IS_STARTER_FW_UPLOAD


class IMAGE_FORMAT_CMD(_CtypesEnum):
    IMGFRMT_CMD_GET_NUM_ENTRIES = 1
    IMGFRMT_CMD_GET_LIST = 2
    IMGFRMT_CMD_SET_FORMAT = 3
    IMGFRMT_CMD_GET_ARBITRARY_AOI_SUPPORTED = 4
    IMGFRMT_CMD_GET_FORMAT_INFO = 5


IMGFRMT_CMD_GET_NUM_ENTRIES = IMAGE_FORMAT_CMD.IMGFRMT_CMD_GET_NUM_ENTRIES
IMGFRMT_CMD_GET_LIST = IMAGE_FORMAT_CMD.IMGFRMT_CMD_GET_LIST
IMGFRMT_CMD_SET_FORMAT = IMAGE_FORMAT_CMD.IMGFRMT_CMD_SET_FORMAT
IMGFRMT_CMD_GET_ARBITRARY_AOI_SUPPORTED = IMAGE_FORMAT_CMD.IMGFRMT_CMD_GET_ARBITRARY_AOI_SUPPORTED
IMGFRMT_CMD_GET_FORMAT_INFO = IMAGE_FORMAT_CMD.IMGFRMT_CMD_GET_FORMAT_INFO


class CAPTUREMODE(_CtypesEnum):
    CAPTMODE_FREERUN = 1
    CAPTMODE_SINGLE = 2
    CAPTMODE_TRIGGER_SOFT_SINGLE = 16
    CAPTMODE_TRIGGER_SOFT_CONTINUOUS = 32
    CAPTMODE_TRIGGER_HW_SINGLE = 256
    CAPTMODE_TRIGGER_HW_CONTINUOUS = 512


CAPTMODE_FREERUN = CAPTUREMODE.CAPTMODE_FREERUN
CAPTMODE_SINGLE = CAPTUREMODE.CAPTMODE_SINGLE
CAPTMODE_TRIGGER_SOFT_SINGLE = CAPTUREMODE.CAPTMODE_TRIGGER_SOFT_SINGLE
CAPTMODE_TRIGGER_SOFT_CONTINUOUS = CAPTUREMODE.CAPTMODE_TRIGGER_SOFT_CONTINUOUS
CAPTMODE_TRIGGER_HW_SINGLE = CAPTUREMODE.CAPTMODE_TRIGGER_HW_SINGLE
CAPTMODE_TRIGGER_HW_CONTINUOUS = CAPTUREMODE.CAPTMODE_TRIGGER_HW_CONTINUOUS


class FDT_CAPABILITY_FLAGS(_CtypesEnum):
    FDT_CAP_INVALID = 0
    FDT_CAP_SUPPORTED = 1
    FDT_CAP_SEARCH_ANGLE = 2
    FDT_CAP_SEARCH_AOI = 4
    FDT_CAP_INFO_POSX = 16
    FDT_CAP_INFO_POSY = 32
    FDT_CAP_INFO_WIDTH = 64
    FDT_CAP_INFO_HEIGHT = 128
    FDT_CAP_INFO_ANGLE = 256
    FDT_CAP_INFO_POSTURE = 512
    FDT_CAP_INFO_FACENUMBER = 1024
    FDT_CAP_INFO_OVL = 2048
    FDT_CAP_INFO_NUM_OVL = 4096
    FDT_CAP_INFO_OVL_LINEWIDTH = 8192


FDT_CAP_INVALID = FDT_CAPABILITY_FLAGS.FDT_CAP_INVALID
FDT_CAP_SUPPORTED = FDT_CAPABILITY_FLAGS.FDT_CAP_SUPPORTED
FDT_CAP_SEARCH_ANGLE = FDT_CAPABILITY_FLAGS.FDT_CAP_SEARCH_ANGLE
FDT_CAP_SEARCH_AOI = FDT_CAPABILITY_FLAGS.FDT_CAP_SEARCH_AOI
FDT_CAP_INFO_POSX = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_POSX
FDT_CAP_INFO_POSY = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_POSY
FDT_CAP_INFO_WIDTH = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_WIDTH
FDT_CAP_INFO_HEIGHT = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_HEIGHT
FDT_CAP_INFO_ANGLE = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_ANGLE
FDT_CAP_INFO_POSTURE = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_POSTURE
FDT_CAP_INFO_FACENUMBER = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_FACENUMBER
FDT_CAP_INFO_OVL = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_OVL
FDT_CAP_INFO_NUM_OVL = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_NUM_OVL
FDT_CAP_INFO_OVL_LINEWIDTH = FDT_CAPABILITY_FLAGS.FDT_CAP_INFO_OVL_LINEWIDTH


class FDT_CMD(_CtypesEnum):
    FDT_CMD_GET_CAPABILITIES = 0
    FDT_CMD_SET_DISABLE = 1
    FDT_CMD_SET_ENABLE = 2
    FDT_CMD_SET_SEARCH_ANGLE = 3
    FDT_CMD_GET_SEARCH_ANGLE = 4
    FDT_CMD_SET_SEARCH_ANGLE_ENABLE = 5
    FDT_CMD_SET_SEARCH_ANGLE_DISABLE = 6
    FDT_CMD_GET_SEARCH_ANGLE_ENABLE = 7
    FDT_CMD_SET_SEARCH_AOI = 8
    FDT_CMD_GET_SEARCH_AOI = 9
    FDT_CMD_GET_FACE_LIST = 10
    FDT_CMD_GET_NUMBER_FACES = 11
    FDT_CMD_SET_SUSPEND = 12
    FDT_CMD_SET_RESUME = 13
    FDT_CMD_GET_MAX_NUM_FACES = 14
    FDT_CMD_SET_INFO_MAX_NUM_OVL = 15
    FDT_CMD_GET_INFO_MAX_NUM_OVL = 16
    FDT_CMD_SET_INFO_OVL_LINE_WIDTH = 17
    FDT_CMD_GET_INFO_OVL_LINE_WIDTH = 18
    FDT_CMD_GET_ENABLE = 19
    FDT_CMD_GET_SUSPEND = 20
    FDT_CMD_GET_HORIZONTAL_RESOLUTION = 21
    FDT_CMD_GET_VERTICAL_RESOLUTION = 22


FDT_CMD_GET_CAPABILITIES = FDT_CMD.FDT_CMD_GET_CAPABILITIES
FDT_CMD_SET_DISABLE = FDT_CMD.FDT_CMD_SET_DISABLE
FDT_CMD_SET_ENABLE = FDT_CMD.FDT_CMD_SET_ENABLE
FDT_CMD_SET_SEARCH_ANGLE = FDT_CMD.FDT_CMD_SET_SEARCH_ANGLE
FDT_CMD_GET_SEARCH_ANGLE = FDT_CMD.FDT_CMD_GET_SEARCH_ANGLE
FDT_CMD_SET_SEARCH_ANGLE_ENABLE = FDT_CMD.FDT_CMD_SET_SEARCH_ANGLE_ENABLE
FDT_CMD_SET_SEARCH_ANGLE_DISABLE = FDT_CMD.FDT_CMD_SET_SEARCH_ANGLE_DISABLE
FDT_CMD_GET_SEARCH_ANGLE_ENABLE = FDT_CMD.FDT_CMD_GET_SEARCH_ANGLE_ENABLE
FDT_CMD_SET_SEARCH_AOI = FDT_CMD.FDT_CMD_SET_SEARCH_AOI
FDT_CMD_GET_SEARCH_AOI = FDT_CMD.FDT_CMD_GET_SEARCH_AOI
FDT_CMD_GET_FACE_LIST = FDT_CMD.FDT_CMD_GET_FACE_LIST
FDT_CMD_GET_NUMBER_FACES = FDT_CMD.FDT_CMD_GET_NUMBER_FACES
FDT_CMD_SET_SUSPEND = FDT_CMD.FDT_CMD_SET_SUSPEND
FDT_CMD_SET_RESUME = FDT_CMD.FDT_CMD_SET_RESUME
FDT_CMD_GET_MAX_NUM_FACES = FDT_CMD.FDT_CMD_GET_MAX_NUM_FACES
FDT_CMD_SET_INFO_MAX_NUM_OVL = FDT_CMD.FDT_CMD_SET_INFO_MAX_NUM_OVL
FDT_CMD_GET_INFO_MAX_NUM_OVL = FDT_CMD.FDT_CMD_GET_INFO_MAX_NUM_OVL
FDT_CMD_SET_INFO_OVL_LINE_WIDTH = FDT_CMD.FDT_CMD_SET_INFO_OVL_LINE_WIDTH
FDT_CMD_GET_INFO_OVL_LINE_WIDTH = FDT_CMD.FDT_CMD_GET_INFO_OVL_LINE_WIDTH
FDT_CMD_GET_ENABLE = FDT_CMD.FDT_CMD_GET_ENABLE
FDT_CMD_GET_SUSPEND = FDT_CMD.FDT_CMD_GET_SUSPEND
FDT_CMD_GET_HORIZONTAL_RESOLUTION = FDT_CMD.FDT_CMD_GET_HORIZONTAL_RESOLUTION
FDT_CMD_GET_VERTICAL_RESOLUTION = FDT_CMD.FDT_CMD_GET_VERTICAL_RESOLUTION


class FOCUS_CAPABILITY_FLAGS(_CtypesEnum):
    FOC_CAP_INVALID = 0
    FOC_CAP_AUTOFOCUS_SUPPORTED = 1
    FOC_CAP_MANUAL_SUPPORTED = 2
    FOC_CAP_GET_DISTANCE = 4
    FOC_CAP_SET_AUTOFOCUS_RANGE = 8
    FOC_CAP_AUTOFOCUS_FDT_AOI = 16
    FOC_CAP_AUTOFOCUS_ZONE = 32


FOC_CAP_INVALID = FOCUS_CAPABILITY_FLAGS.FOC_CAP_INVALID
FOC_CAP_AUTOFOCUS_SUPPORTED = FOCUS_CAPABILITY_FLAGS.FOC_CAP_AUTOFOCUS_SUPPORTED
FOC_CAP_MANUAL_SUPPORTED = FOCUS_CAPABILITY_FLAGS.FOC_CAP_MANUAL_SUPPORTED
FOC_CAP_GET_DISTANCE = FOCUS_CAPABILITY_FLAGS.FOC_CAP_GET_DISTANCE
FOC_CAP_SET_AUTOFOCUS_RANGE = FOCUS_CAPABILITY_FLAGS.FOC_CAP_SET_AUTOFOCUS_RANGE
FOC_CAP_AUTOFOCUS_FDT_AOI = FOCUS_CAPABILITY_FLAGS.FOC_CAP_AUTOFOCUS_FDT_AOI
FOC_CAP_AUTOFOCUS_ZONE = FOCUS_CAPABILITY_FLAGS.FOC_CAP_AUTOFOCUS_ZONE


class FOCUS_RANGE(_CtypesEnum):
    FOC_RANGE_NORMAL = 1
    FOC_RANGE_ALLRANGE = 2
    FOC_RANGE_MACRO = 4


FOC_RANGE_NORMAL = FOCUS_RANGE.FOC_RANGE_NORMAL
FOC_RANGE_ALLRANGE = FOCUS_RANGE.FOC_RANGE_ALLRANGE
FOC_RANGE_MACRO = FOCUS_RANGE.FOC_RANGE_MACRO


class FOCUS_STATUS(_CtypesEnum):
    FOC_STATUS_UNDEFINED = 0
    FOC_STATUS_ERROR = 1
    FOC_STATUS_FOCUSED = 2
    FOC_STATUS_FOCUSING = 4
    FOC_STATUS_TIMEOUT = 8
    FOC_STATUS_CANCEL = 16


FOC_STATUS_UNDEFINED = FOCUS_STATUS.FOC_STATUS_UNDEFINED
FOC_STATUS_ERROR = FOCUS_STATUS.FOC_STATUS_ERROR
FOC_STATUS_FOCUSED = FOCUS_STATUS.FOC_STATUS_FOCUSED
FOC_STATUS_FOCUSING = FOCUS_STATUS.FOC_STATUS_FOCUSING
FOC_STATUS_TIMEOUT = FOCUS_STATUS.FOC_STATUS_TIMEOUT
FOC_STATUS_CANCEL = FOCUS_STATUS.FOC_STATUS_CANCEL


class FOCUS_ZONE_WEIGHT(_CtypesEnum):
    FOC_ZONE_WEIGHT_DISABLE = 0
    FOC_ZONE_WEIGHT_WEAK = 33
    FOC_ZONE_WEIGHT_MIDDLE = 50
    FOC_ZONE_WEIGHT_STRONG = 66


FOC_ZONE_WEIGHT_DISABLE = FOCUS_ZONE_WEIGHT.FOC_ZONE_WEIGHT_DISABLE
FOC_ZONE_WEIGHT_WEAK = FOCUS_ZONE_WEIGHT.FOC_ZONE_WEIGHT_WEAK
FOC_ZONE_WEIGHT_MIDDLE = FOCUS_ZONE_WEIGHT.FOC_ZONE_WEIGHT_MIDDLE
FOC_ZONE_WEIGHT_STRONG = FOCUS_ZONE_WEIGHT.FOC_ZONE_WEIGHT_STRONG


class FOCUS_ZONE_AOI_PRESET(_CtypesEnum):
    FOC_ZONE_AOI_PRESET_CENTER = 0
    FOC_ZONE_AOI_PRESET_UPPER_LEFT = 1
    FOC_ZONE_AOI_PRESET_BOTTOM_LEFT = 2
    FOC_ZONE_AOI_PRESET_UPPER_RIGHT = 4
    FOC_ZONE_AOI_PRESET_BOTTOM_RIGHT = 8
    FOC_ZONE_AOI_PRESET_UPPER_CENTER = 16
    FOC_ZONE_AOI_PRESET_BOTTOM_CENTER = 32
    FOC_ZONE_AOI_PRESET_CENTER_LEFT = 64
    FOC_ZONE_AOI_PRESET_CENTER_RIGHT = 128


FOC_ZONE_AOI_PRESET_CENTER = FOCUS_ZONE_AOI_PRESET.FOC_ZONE_AOI_PRESET_CENTER
FOC_ZONE_AOI_PRESET_UPPER_LEFT = FOCUS_ZONE_AOI_PRESET.FOC_ZONE_AOI_PRESET_UPPER_LEFT
FOC_ZONE_AOI_PRESET_BOTTOM_LEFT = FOCUS_ZONE_AOI_PRESET.FOC_ZONE_AOI_PRESET_BOTTOM_LEFT
FOC_ZONE_AOI_PRESET_UPPER_RIGHT = FOCUS_ZONE_AOI_PRESET.FOC_ZONE_AOI_PRESET_UPPER_RIGHT
FOC_ZONE_AOI_PRESET_BOTTOM_RIGHT = FOCUS_ZONE_AOI_PRESET.FOC_ZONE_AOI_PRESET_BOTTOM_RIGHT
FOC_ZONE_AOI_PRESET_UPPER_CENTER = FOCUS_ZONE_AOI_PRESET.FOC_ZONE_AOI_PRESET_UPPER_CENTER
FOC_ZONE_AOI_PRESET_BOTTOM_CENTER = FOCUS_ZONE_AOI_PRESET.FOC_ZONE_AOI_PRESET_BOTTOM_CENTER
FOC_ZONE_AOI_PRESET_CENTER_LEFT = FOCUS_ZONE_AOI_PRESET.FOC_ZONE_AOI_PRESET_CENTER_LEFT
FOC_ZONE_AOI_PRESET_CENTER_RIGHT = FOCUS_ZONE_AOI_PRESET.FOC_ZONE_AOI_PRESET_CENTER_RIGHT


class FOCUS_CMD(_CtypesEnum):
    FOC_CMD_GET_CAPABILITIES = 0
    FOC_CMD_SET_DISABLE_AUTOFOCUS = 1
    FOC_CMD_SET_ENABLE_AUTOFOCUS = 2
    FOC_CMD_GET_AUTOFOCUS_ENABLE = 3
    FOC_CMD_SET_AUTOFOCUS_RANGE = 4
    FOC_CMD_GET_AUTOFOCUS_RANGE = 5
    FOC_CMD_GET_DISTANCE = 6
    FOC_CMD_SET_MANUAL_FOCUS = 7
    FOC_CMD_GET_MANUAL_FOCUS = 8
    FOC_CMD_GET_MANUAL_FOCUS_MIN = 9
    FOC_CMD_GET_MANUAL_FOCUS_MAX = 10
    FOC_CMD_GET_MANUAL_FOCUS_INC = 11
    FOC_CMD_SET_ENABLE_AF_FDT_AOI = 12
    FOC_CMD_SET_DISABLE_AF_FDT_AOI = 13
    FOC_CMD_GET_AF_FDT_AOI_ENABLE = 14
    FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE = 15
    FOC_CMD_GET_AUTOFOCUS_STATUS = 16
    FOC_CMD_SET_AUTOFOCUS_ZONE_AOI = 17
    FOC_CMD_GET_AUTOFOCUS_ZONE_AOI = 18
    FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_DEFAULT = 19
    FOC_CMD_GET_AUTOFOCUS_ZONE_POS_MIN = 20
    FOC_CMD_GET_AUTOFOCUS_ZONE_POS_MAX = 21
    FOC_CMD_GET_AUTOFOCUS_ZONE_POS_INC = 22
    FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_MIN = 23
    FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_MAX = 24
    FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_INC = 25
    FOC_CMD_SET_AUTOFOCUS_ZONE_WEIGHT = 26
    FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT = 27
    FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT_COUNT = 28
    FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT_DEFAULT = 29
    FOC_CMD_SET_AUTOFOCUS_ZONE_AOI_PRESET = 30
    FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_PRESET = 31
    FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_PRESET_DEFAULT = 32
    FOC_CMD_GET_AUTOFOCUS_ZONE_ARBITRARY_AOI_SUPPORTED = 33
    FOC_CMD_SET_MANUAL_FOCUS_RELATIVE = 34


FOC_CMD_GET_CAPABILITIES = FOCUS_CMD.FOC_CMD_GET_CAPABILITIES
FOC_CMD_SET_DISABLE_AUTOFOCUS = FOCUS_CMD.FOC_CMD_SET_DISABLE_AUTOFOCUS
FOC_CMD_SET_ENABLE_AUTOFOCUS = FOCUS_CMD.FOC_CMD_SET_ENABLE_AUTOFOCUS
FOC_CMD_GET_AUTOFOCUS_ENABLE = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ENABLE
FOC_CMD_SET_AUTOFOCUS_RANGE = FOCUS_CMD.FOC_CMD_SET_AUTOFOCUS_RANGE
FOC_CMD_GET_AUTOFOCUS_RANGE = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_RANGE
FOC_CMD_GET_DISTANCE = FOCUS_CMD.FOC_CMD_GET_DISTANCE
FOC_CMD_SET_MANUAL_FOCUS = FOCUS_CMD.FOC_CMD_SET_MANUAL_FOCUS
FOC_CMD_GET_MANUAL_FOCUS = FOCUS_CMD.FOC_CMD_GET_MANUAL_FOCUS
FOC_CMD_GET_MANUAL_FOCUS_MIN = FOCUS_CMD.FOC_CMD_GET_MANUAL_FOCUS_MIN
FOC_CMD_GET_MANUAL_FOCUS_MAX = FOCUS_CMD.FOC_CMD_GET_MANUAL_FOCUS_MAX
FOC_CMD_GET_MANUAL_FOCUS_INC = FOCUS_CMD.FOC_CMD_GET_MANUAL_FOCUS_INC
FOC_CMD_SET_ENABLE_AF_FDT_AOI = FOCUS_CMD.FOC_CMD_SET_ENABLE_AF_FDT_AOI
FOC_CMD_SET_DISABLE_AF_FDT_AOI = FOCUS_CMD.FOC_CMD_SET_DISABLE_AF_FDT_AOI
FOC_CMD_GET_AF_FDT_AOI_ENABLE = FOCUS_CMD.FOC_CMD_GET_AF_FDT_AOI_ENABLE
FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE = FOCUS_CMD.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE
FOC_CMD_GET_AUTOFOCUS_STATUS = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_STATUS
FOC_CMD_SET_AUTOFOCUS_ZONE_AOI = FOCUS_CMD.FOC_CMD_SET_AUTOFOCUS_ZONE_AOI
FOC_CMD_GET_AUTOFOCUS_ZONE_AOI = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_AOI
FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_DEFAULT = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_DEFAULT
FOC_CMD_GET_AUTOFOCUS_ZONE_POS_MIN = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_POS_MIN
FOC_CMD_GET_AUTOFOCUS_ZONE_POS_MAX = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_POS_MAX
FOC_CMD_GET_AUTOFOCUS_ZONE_POS_INC = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_POS_INC
FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_MIN = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_MIN
FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_MAX = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_MAX
FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_INC = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_SIZE_INC
FOC_CMD_SET_AUTOFOCUS_ZONE_WEIGHT = FOCUS_CMD.FOC_CMD_SET_AUTOFOCUS_ZONE_WEIGHT
FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT
FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT_COUNT = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT_COUNT
FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT_DEFAULT = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_WEIGHT_DEFAULT
FOC_CMD_SET_AUTOFOCUS_ZONE_AOI_PRESET = FOCUS_CMD.FOC_CMD_SET_AUTOFOCUS_ZONE_AOI_PRESET
FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_PRESET = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_PRESET
FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_PRESET_DEFAULT = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_AOI_PRESET_DEFAULT
FOC_CMD_GET_AUTOFOCUS_ZONE_ARBITRARY_AOI_SUPPORTED = FOCUS_CMD.FOC_CMD_GET_AUTOFOCUS_ZONE_ARBITRARY_AOI_SUPPORTED
FOC_CMD_SET_MANUAL_FOCUS_RELATIVE = FOCUS_CMD.FOC_CMD_SET_MANUAL_FOCUS_RELATIVE


class IMGSTAB_CAPABILITY_FLAGS(_CtypesEnum):
    IMGSTAB_CAP_INVALID = 0
    IMGSTAB_CAP_IMAGE_STABILIZATION_SUPPORTED = 1


IMGSTAB_CAP_INVALID = IMGSTAB_CAPABILITY_FLAGS.IMGSTAB_CAP_INVALID
IMGSTAB_CAP_IMAGE_STABILIZATION_SUPPORTED = IMGSTAB_CAPABILITY_FLAGS.IMGSTAB_CAP_IMAGE_STABILIZATION_SUPPORTED


class IMGSTAB_CMD(_CtypesEnum):
    IMGSTAB_CMD_GET_CAPABILITIES = 0
    IMGSTAB_CMD_SET_DISABLE = 1
    IMGSTAB_CMD_SET_ENABLE = 2
    IMGSTAB_CMD_GET_ENABLE = 3


IMGSTAB_CMD_GET_CAPABILITIES = IMGSTAB_CMD.IMGSTAB_CMD_GET_CAPABILITIES
IMGSTAB_CMD_SET_DISABLE = IMGSTAB_CMD.IMGSTAB_CMD_SET_DISABLE
IMGSTAB_CMD_SET_ENABLE = IMGSTAB_CMD.IMGSTAB_CMD_SET_ENABLE
IMGSTAB_CMD_GET_ENABLE = IMGSTAB_CMD.IMGSTAB_CMD_GET_ENABLE


class SCENE_CMD(_CtypesEnum):
    SCENE_CMD_GET_SUPPORTED_PRESETS = 1
    SCENE_CMD_SET_PRESET = 2
    SCENE_CMD_GET_PRESET = 3
    SCENE_CMD_GET_DEFAULT_PRESET = 4


SCENE_CMD_GET_SUPPORTED_PRESETS = SCENE_CMD.SCENE_CMD_GET_SUPPORTED_PRESETS
SCENE_CMD_SET_PRESET = SCENE_CMD.SCENE_CMD_SET_PRESET
SCENE_CMD_GET_PRESET = SCENE_CMD.SCENE_CMD_GET_PRESET
SCENE_CMD_GET_DEFAULT_PRESET = SCENE_CMD.SCENE_CMD_GET_DEFAULT_PRESET


class SCENE_PRESET(_CtypesEnum):
    SCENE_INVALID = 0
    SCENE_SENSOR_AUTOMATIC = 1
    SCENE_SENSOR_PORTRAIT = 2
    SCENE_SENSOR_SUNNY = 4
    SCENE_SENSOR_ENTERTAINMENT = 8
    SCENE_SENSOR_NIGHT = 16
    SCENE_SENSOR_SPORTS = 64
    SCENE_SENSOR_LANDSCAPE = 128


SCENE_INVALID = SCENE_PRESET.SCENE_INVALID
SCENE_SENSOR_AUTOMATIC = SCENE_PRESET.SCENE_SENSOR_AUTOMATIC
SCENE_SENSOR_PORTRAIT = SCENE_PRESET.SCENE_SENSOR_PORTRAIT
SCENE_SENSOR_SUNNY = SCENE_PRESET.SCENE_SENSOR_SUNNY
SCENE_SENSOR_ENTERTAINMENT = SCENE_PRESET.SCENE_SENSOR_ENTERTAINMENT
SCENE_SENSOR_NIGHT = SCENE_PRESET.SCENE_SENSOR_NIGHT
SCENE_SENSOR_SPORTS = SCENE_PRESET.SCENE_SENSOR_SPORTS
SCENE_SENSOR_LANDSCAPE = SCENE_PRESET.SCENE_SENSOR_LANDSCAPE


class ZOOM_CMD(_CtypesEnum):
    ZOOM_CMD_GET_CAPABILITIES = 0
    ZOOM_CMD_DIGITAL_GET_NUM_LIST_ENTRIES = 1
    ZOOM_CMD_DIGITAL_GET_LIST = 2
    ZOOM_CMD_DIGITAL_SET_VALUE = 3
    ZOOM_CMD_DIGITAL_GET_VALUE = 4
    ZOOM_CMD_DIGITAL_GET_VALUE_RANGE = 5
    ZOOM_CMD_DIGITAL_GET_VALUE_DEFAULT = 6


ZOOM_CMD_GET_CAPABILITIES = ZOOM_CMD.ZOOM_CMD_GET_CAPABILITIES
ZOOM_CMD_DIGITAL_GET_NUM_LIST_ENTRIES = ZOOM_CMD.ZOOM_CMD_DIGITAL_GET_NUM_LIST_ENTRIES
ZOOM_CMD_DIGITAL_GET_LIST = ZOOM_CMD.ZOOM_CMD_DIGITAL_GET_LIST
ZOOM_CMD_DIGITAL_SET_VALUE = ZOOM_CMD.ZOOM_CMD_DIGITAL_SET_VALUE
ZOOM_CMD_DIGITAL_GET_VALUE = ZOOM_CMD.ZOOM_CMD_DIGITAL_GET_VALUE
ZOOM_CMD_DIGITAL_GET_VALUE_RANGE = ZOOM_CMD.ZOOM_CMD_DIGITAL_GET_VALUE_RANGE
ZOOM_CMD_DIGITAL_GET_VALUE_DEFAULT = ZOOM_CMD.ZOOM_CMD_DIGITAL_GET_VALUE_DEFAULT


class ZOOM_CAPABILITY_FLAGS(_CtypesEnum):
    ZOOM_CAP_INVALID = 0
    ZOOM_CAP_DIGITAL_ZOOM = 1


ZOOM_CAP_INVALID = ZOOM_CAPABILITY_FLAGS.ZOOM_CAP_INVALID
ZOOM_CAP_DIGITAL_ZOOM = ZOOM_CAPABILITY_FLAGS.ZOOM_CAP_DIGITAL_ZOOM


class SHARPNESS_CMD(_CtypesEnum):
    SHARPNESS_CMD_GET_CAPABILITIES = 0
    SHARPNESS_CMD_GET_VALUE = 1
    SHARPNESS_CMD_GET_MIN_VALUE = 2
    SHARPNESS_CMD_GET_MAX_VALUE = 3
    SHARPNESS_CMD_GET_INCREMENT = 4
    SHARPNESS_CMD_GET_DEFAULT_VALUE = 5
    SHARPNESS_CMD_SET_VALUE = 6


SHARPNESS_CMD_GET_CAPABILITIES = SHARPNESS_CMD.SHARPNESS_CMD_GET_CAPABILITIES
SHARPNESS_CMD_GET_VALUE = SHARPNESS_CMD.SHARPNESS_CMD_GET_VALUE
SHARPNESS_CMD_GET_MIN_VALUE = SHARPNESS_CMD.SHARPNESS_CMD_GET_MIN_VALUE
SHARPNESS_CMD_GET_MAX_VALUE = SHARPNESS_CMD.SHARPNESS_CMD_GET_MAX_VALUE
SHARPNESS_CMD_GET_INCREMENT = SHARPNESS_CMD.SHARPNESS_CMD_GET_INCREMENT
SHARPNESS_CMD_GET_DEFAULT_VALUE = SHARPNESS_CMD.SHARPNESS_CMD_GET_DEFAULT_VALUE
SHARPNESS_CMD_SET_VALUE = SHARPNESS_CMD.SHARPNESS_CMD_SET_VALUE


class SHARPNESS_CAPABILITY_FLAGS(_CtypesEnum):
    SHARPNESS_CAP_INVALID = 0
    SHARPNESS_CAP_SHARPNESS_SUPPORTED = 1


SHARPNESS_CAP_INVALID = SHARPNESS_CAPABILITY_FLAGS.SHARPNESS_CAP_INVALID
SHARPNESS_CAP_SHARPNESS_SUPPORTED = SHARPNESS_CAPABILITY_FLAGS.SHARPNESS_CAP_SHARPNESS_SUPPORTED


class SATURATION_CMD(_CtypesEnum):
    SATURATION_CMD_GET_CAPABILITIES = 0
    SATURATION_CMD_GET_VALUE = 1
    SATURATION_CMD_GET_MIN_VALUE = 2
    SATURATION_CMD_GET_MAX_VALUE = 3
    SATURATION_CMD_GET_INCREMENT = 4
    SATURATION_CMD_GET_DEFAULT_VALUE = 5
    SATURATION_CMD_SET_VALUE = 6


SATURATION_CMD_GET_CAPABILITIES = SATURATION_CMD.SATURATION_CMD_GET_CAPABILITIES
SATURATION_CMD_GET_VALUE = SATURATION_CMD.SATURATION_CMD_GET_VALUE
SATURATION_CMD_GET_MIN_VALUE = SATURATION_CMD.SATURATION_CMD_GET_MIN_VALUE
SATURATION_CMD_GET_MAX_VALUE = SATURATION_CMD.SATURATION_CMD_GET_MAX_VALUE
SATURATION_CMD_GET_INCREMENT = SATURATION_CMD.SATURATION_CMD_GET_INCREMENT
SATURATION_CMD_GET_DEFAULT_VALUE = SATURATION_CMD.SATURATION_CMD_GET_DEFAULT_VALUE
SATURATION_CMD_SET_VALUE = SATURATION_CMD.SATURATION_CMD_SET_VALUE


class SATURATION_CAPABILITY_FLAGS(_CtypesEnum):
    SATURATION_CAP_INVALID = 0
    SATURATION_CAP_SATURATION_SUPPORTED = 1


SATURATION_CAP_INVALID = SATURATION_CAPABILITY_FLAGS.SATURATION_CAP_INVALID
SATURATION_CAP_SATURATION_SUPPORTED = SATURATION_CAPABILITY_FLAGS.SATURATION_CAP_SATURATION_SUPPORTED


class TRIGGER_DEBOUNCE_MODE(_CtypesEnum):
    TRIGGER_DEBOUNCE_MODE_NONE = 0
    TRIGGER_DEBOUNCE_MODE_FALLING_EDGE = 1
    TRIGGER_DEBOUNCE_MODE_RISING_EDGE = 2
    TRIGGER_DEBOUNCE_MODE_BOTH_EDGES = 4
    TRIGGER_DEBOUNCE_MODE_AUTOMATIC = 8


TRIGGER_DEBOUNCE_MODE_NONE = TRIGGER_DEBOUNCE_MODE.TRIGGER_DEBOUNCE_MODE_NONE
TRIGGER_DEBOUNCE_MODE_FALLING_EDGE = TRIGGER_DEBOUNCE_MODE.TRIGGER_DEBOUNCE_MODE_FALLING_EDGE
TRIGGER_DEBOUNCE_MODE_RISING_EDGE = TRIGGER_DEBOUNCE_MODE.TRIGGER_DEBOUNCE_MODE_RISING_EDGE
TRIGGER_DEBOUNCE_MODE_BOTH_EDGES = TRIGGER_DEBOUNCE_MODE.TRIGGER_DEBOUNCE_MODE_BOTH_EDGES
TRIGGER_DEBOUNCE_MODE_AUTOMATIC = TRIGGER_DEBOUNCE_MODE.TRIGGER_DEBOUNCE_MODE_AUTOMATIC


class TRIGGER_DEBOUNCE_CMD(_CtypesEnum):
    TRIGGER_DEBOUNCE_CMD_SET_MODE = 0
    TRIGGER_DEBOUNCE_CMD_SET_DELAY_TIME = 1
    TRIGGER_DEBOUNCE_CMD_GET_SUPPORTED_MODES = 2
    TRIGGER_DEBOUNCE_CMD_GET_MODE = 3
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME = 4
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_MIN = 5
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_MAX = 6
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_INC = 7
    TRIGGER_DEBOUNCE_CMD_GET_MODE_DEFAULT = 8
    TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_DEFAULT = 9


TRIGGER_DEBOUNCE_CMD_SET_MODE = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_SET_MODE
TRIGGER_DEBOUNCE_CMD_SET_DELAY_TIME = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_SET_DELAY_TIME
TRIGGER_DEBOUNCE_CMD_GET_SUPPORTED_MODES = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_GET_SUPPORTED_MODES
TRIGGER_DEBOUNCE_CMD_GET_MODE = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_GET_MODE
TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME
TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_MIN = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_MIN
TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_MAX = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_MAX
TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_INC = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_INC
TRIGGER_DEBOUNCE_CMD_GET_MODE_DEFAULT = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_GET_MODE_DEFAULT
TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_DEFAULT = TRIGGER_DEBOUNCE_CMD.TRIGGER_DEBOUNCE_CMD_GET_DELAY_TIME_DEFAULT


class RGB_COLOR_MODELS(_CtypesEnum):
    RGB_COLOR_MODEL_SRGB_D50 = 1
    RGB_COLOR_MODEL_SRGB_D65 = 2
    RGB_COLOR_MODEL_CIE_RGB_E = 4
    RGB_COLOR_MODEL_ECI_RGB_D50 = 8
    RGB_COLOR_MODEL_ADOBE_RGB_D65 = 16


RGB_COLOR_MODEL_SRGB_D50 = RGB_COLOR_MODELS.RGB_COLOR_MODEL_SRGB_D50
RGB_COLOR_MODEL_SRGB_D65 = RGB_COLOR_MODELS.RGB_COLOR_MODEL_SRGB_D65
RGB_COLOR_MODEL_CIE_RGB_E = RGB_COLOR_MODELS.RGB_COLOR_MODEL_CIE_RGB_E
RGB_COLOR_MODEL_ECI_RGB_D50 = RGB_COLOR_MODELS.RGB_COLOR_MODEL_ECI_RGB_D50
RGB_COLOR_MODEL_ADOBE_RGB_D65 = RGB_COLOR_MODELS.RGB_COLOR_MODEL_ADOBE_RGB_D65


class LENS_SHADING_MODELS(_CtypesEnum):
    LSC_MODEL_AGL = 1
    LSC_MODEL_TL84 = 2
    LSC_MODEL_D50 = 4
    LSC_MODEL_D65 = 8


LSC_MODEL_AGL = LENS_SHADING_MODELS.LSC_MODEL_AGL
LSC_MODEL_TL84 = LENS_SHADING_MODELS.LSC_MODEL_TL84
LSC_MODEL_D50 = LENS_SHADING_MODELS.LSC_MODEL_D50
LSC_MODEL_D65 = LENS_SHADING_MODELS.LSC_MODEL_D65


class COLOR_TEMPERATURE_CMD(_CtypesEnum):
    COLOR_TEMPERATURE_CMD_SET_TEMPERATURE = 0
    COLOR_TEMPERATURE_CMD_SET_RGB_COLOR_MODEL = 1
    COLOR_TEMPERATURE_CMD_GET_SUPPORTED_RGB_COLOR_MODELS = 2
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE = 3
    COLOR_TEMPERATURE_CMD_GET_RGB_COLOR_MODEL = 4
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_MIN = 5
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_MAX = 6
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_INC = 7
    COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_DEFAULT = 8
    COLOR_TEMPERATURE_CMD_GET_RGB_COLOR_MODEL_DEFAULT = 9
    COLOR_TEMPERATURE_CMD_SET_LENS_SHADING_MODEL = 10
    COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL = 11
    COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL_SUPPORTED = 12
    COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL_DEFAULT = 13


COLOR_TEMPERATURE_CMD_SET_TEMPERATURE = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_SET_TEMPERATURE
COLOR_TEMPERATURE_CMD_SET_RGB_COLOR_MODEL = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_SET_RGB_COLOR_MODEL
COLOR_TEMPERATURE_CMD_GET_SUPPORTED_RGB_COLOR_MODELS = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_SUPPORTED_RGB_COLOR_MODELS
COLOR_TEMPERATURE_CMD_GET_TEMPERATURE = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_TEMPERATURE
COLOR_TEMPERATURE_CMD_GET_RGB_COLOR_MODEL = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_RGB_COLOR_MODEL
COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_MIN = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_MIN
COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_MAX = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_MAX
COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_INC = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_INC
COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_DEFAULT = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_TEMPERATURE_DEFAULT
COLOR_TEMPERATURE_CMD_GET_RGB_COLOR_MODEL_DEFAULT = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_RGB_COLOR_MODEL_DEFAULT
COLOR_TEMPERATURE_CMD_SET_LENS_SHADING_MODEL = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_SET_LENS_SHADING_MODEL
COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL
COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL_SUPPORTED = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL_SUPPORTED
COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL_DEFAULT = COLOR_TEMPERATURE_CMD.COLOR_TEMPERATURE_CMD_GET_LENS_SHADING_MODEL_DEFAULT


class TRANSFER_CAPABILITY_FLAGS(_CtypesEnum):
    TRANSFER_CAP_IMAGEDELAY = 1
    TRANSFER_CAP_PACKETINTERVAL = 32


TRANSFER_CAP_IMAGEDELAY = TRANSFER_CAPABILITY_FLAGS.TRANSFER_CAP_IMAGEDELAY
TRANSFER_CAP_PACKETINTERVAL = TRANSFER_CAPABILITY_FLAGS.TRANSFER_CAP_PACKETINTERVAL


class TRANSFER_CMD(_CtypesEnum):
    TRANSFER_CMD_QUERY_CAPABILITIES = 0
    TRANSFER_CMD_SET_IMAGEDELAY_US = 1000
    TRANSFER_CMD_SET_PACKETINTERVAL_US = 1005
    TRANSFER_CMD_GET_IMAGEDELAY_US = 2000
    TRANSFER_CMD_GET_PACKETINTERVAL_US = 2005
    TRANSFER_CMD_GETRANGE_IMAGEDELAY_US = 3000
    TRANSFER_CMD_GETRANGE_PACKETINTERVAL_US = 3005
    TRANSFER_CMD_SET_IMAGE_DESTINATION = 5000
    TRANSFER_CMD_GET_IMAGE_DESTINATION = 5001
    TRANSFER_CMD_GET_IMAGE_DESTINATION_CAPABILITIES = 5002


TRANSFER_CMD_QUERY_CAPABILITIES = TRANSFER_CMD.TRANSFER_CMD_QUERY_CAPABILITIES
TRANSFER_CMD_SET_IMAGEDELAY_US = TRANSFER_CMD.TRANSFER_CMD_SET_IMAGEDELAY_US
TRANSFER_CMD_SET_PACKETINTERVAL_US = TRANSFER_CMD.TRANSFER_CMD_SET_PACKETINTERVAL_US
TRANSFER_CMD_GET_IMAGEDELAY_US = TRANSFER_CMD.TRANSFER_CMD_GET_IMAGEDELAY_US
TRANSFER_CMD_GET_PACKETINTERVAL_US = TRANSFER_CMD.TRANSFER_CMD_GET_PACKETINTERVAL_US
TRANSFER_CMD_GETRANGE_IMAGEDELAY_US = TRANSFER_CMD.TRANSFER_CMD_GETRANGE_IMAGEDELAY_US
TRANSFER_CMD_GETRANGE_PACKETINTERVAL_US = TRANSFER_CMD.TRANSFER_CMD_GETRANGE_PACKETINTERVAL_US
TRANSFER_CMD_SET_IMAGE_DESTINATION = TRANSFER_CMD.TRANSFER_CMD_SET_IMAGE_DESTINATION
TRANSFER_CMD_GET_IMAGE_DESTINATION = TRANSFER_CMD.TRANSFER_CMD_GET_IMAGE_DESTINATION
TRANSFER_CMD_GET_IMAGE_DESTINATION_CAPABILITIES = TRANSFER_CMD.TRANSFER_CMD_GET_IMAGE_DESTINATION_CAPABILITIES


class TRANSFER_TARGET(_CtypesEnum):
    IS_TRANSFER_DESTINATION_DEVICE_MEMORY = 1
    IS_TRANSFER_DESTINATION_USER_MEMORY = 2


IS_TRANSFER_DESTINATION_DEVICE_MEMORY = TRANSFER_TARGET.IS_TRANSFER_DESTINATION_DEVICE_MEMORY
IS_TRANSFER_DESTINATION_USER_MEMORY = TRANSFER_TARGET.IS_TRANSFER_DESTINATION_USER_MEMORY


class IS_BOOTBOOST_CMD(_CtypesEnum):
    IS_BOOTBOOST_CMD_ENABLE = 65537
    IS_BOOTBOOST_CMD_ENABLE_AND_WAIT = 65793
    IS_BOOTBOOST_CMD_DISABLE = 65553
    IS_BOOTBOOST_CMD_DISABLE_AND_WAIT = 65809
    IS_BOOTBOOST_CMD_WAIT = 65792
    IS_BOOTBOOST_CMD_GET_ENABLED = 536936481
    IS_BOOTBOOST_CMD_ADD_ID = 269484033
    IS_BOOTBOOST_CMD_SET_IDLIST = 269484037
    IS_BOOTBOOST_CMD_REMOVE_ID = 269484049
    IS_BOOTBOOST_CMD_CLEAR_IDLIST = 1048597
    IS_BOOTBOOST_CMD_GET_IDLIST = 806354977
    IS_BOOTBOOST_CMD_GET_IDLIST_SIZE = 537919522


IS_BOOTBOOST_CMD_ENABLE = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_ENABLE
IS_BOOTBOOST_CMD_ENABLE_AND_WAIT = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_ENABLE_AND_WAIT
IS_BOOTBOOST_CMD_DISABLE = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_DISABLE
IS_BOOTBOOST_CMD_DISABLE_AND_WAIT = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_DISABLE_AND_WAIT
IS_BOOTBOOST_CMD_WAIT = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_WAIT
IS_BOOTBOOST_CMD_GET_ENABLED = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_GET_ENABLED
IS_BOOTBOOST_CMD_ADD_ID = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_ADD_ID
IS_BOOTBOOST_CMD_SET_IDLIST = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_SET_IDLIST
IS_BOOTBOOST_CMD_REMOVE_ID = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_REMOVE_ID
IS_BOOTBOOST_CMD_CLEAR_IDLIST = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_CLEAR_IDLIST
IS_BOOTBOOST_CMD_GET_IDLIST = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_GET_IDLIST
IS_BOOTBOOST_CMD_GET_IDLIST_SIZE = IS_BOOTBOOST_CMD.IS_BOOTBOOST_CMD_GET_IDLIST_SIZE


class DEVICE_FEATURE_CMD(_CtypesEnum):
    IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_FEATURES = 1
    IS_DEVICE_FEATURE_CMD_SET_LINESCAN_MODE = 2
    IS_DEVICE_FEATURE_CMD_GET_LINESCAN_MODE = 3
    IS_DEVICE_FEATURE_CMD_SET_LINESCAN_NUMBER = 4
    IS_DEVICE_FEATURE_CMD_GET_LINESCAN_NUMBER = 5
    IS_DEVICE_FEATURE_CMD_SET_SHUTTER_MODE = 6
    IS_DEVICE_FEATURE_CMD_GET_SHUTTER_MODE = 7
    IS_DEVICE_FEATURE_CMD_SET_PREFER_XS_HS_MODE = 8
    IS_DEVICE_FEATURE_CMD_GET_PREFER_XS_HS_MODE = 9
    IS_DEVICE_FEATURE_CMD_GET_DEFAULT_PREFER_XS_HS_MODE = 10
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_DEFAULT = 11
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE = 12
    IS_DEVICE_FEATURE_CMD_SET_LOG_MODE = 13
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE_DEFAULT = 14
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE_RANGE = 15
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE = 16
    IS_DEVICE_FEATURE_CMD_SET_LOG_MODE_MANUAL_VALUE = 17
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN_DEFAULT = 18
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN_RANGE = 19
    IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN = 20
    IS_DEVICE_FEATURE_CMD_SET_LOG_MODE_MANUAL_GAIN = 21
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE_DEFAULT = 22
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE = 23
    IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_MODE = 24
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION_DEFAULT = 25
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION_RANGE = 26
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION = 27
    IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_POSITION = 28
    IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_MODE_DEFAULT = 29
    IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_MODE = 30
    IS_DEVICE_FEATURE_CMD_SET_FPN_CORRECTION_MODE = 31
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN_RANGE = 32
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN_DEFAULT = 33
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN = 34
    IS_DEVICE_FEATURE_CMD_SET_SENSOR_SOURCE_GAIN = 35
    IS_DEVICE_FEATURE_CMD_GET_BLACK_REFERENCE_MODE_DEFAULT = 36
    IS_DEVICE_FEATURE_CMD_GET_BLACK_REFERENCE_MODE = 37
    IS_DEVICE_FEATURE_CMD_SET_BLACK_REFERENCE_MODE = 38
    IS_DEVICE_FEATURE_CMD_GET_ALLOW_RAW_WITH_LUT = 39
    IS_DEVICE_FEATURE_CMD_SET_ALLOW_RAW_WITH_LUT = 40
    IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_SENSOR_BIT_DEPTHS = 41
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_BIT_DEPTH_DEFAULT = 42
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_BIT_DEPTH = 43
    IS_DEVICE_FEATURE_CMD_SET_SENSOR_BIT_DEPTH = 44
    IS_DEVICE_FEATURE_CMD_GET_TEMPERATURE = 45
    IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION = 46
    IS_DEVICE_FEATURE_CMD_SET_JPEG_COMPRESSION = 47
    IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION_DEFAULT = 48
    IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION_RANGE = 49
    IS_DEVICE_FEATURE_CMD_GET_NOISE_REDUCTION_MODE = 50
    IS_DEVICE_FEATURE_CMD_SET_NOISE_REDUCTION_MODE = 51
    IS_DEVICE_FEATURE_CMD_GET_NOISE_REDUCTION_MODE_DEFAULT = 52
    IS_DEVICE_FEATURE_CMD_GET_TIMESTAMP_CONFIGURATION = 53
    IS_DEVICE_FEATURE_CMD_SET_TIMESTAMP_CONFIGURATION = 54
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_DEFAULT = 55
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_NUMBER = 56
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_LIST = 57
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT = 58
    IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_HEIGHT = 59
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION_DEFAULT = 60
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION_RANGE = 61
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION = 62
    IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION = 63
    IS_DEVICE_FEATURE_CMD_GET_SENSOR_TEMPERATURE_NUMERICAL_VALUE = 64
    IS_DEVICE_FEATURE_CMD_SET_IMAGE_EFFECT = 65
    IS_DEVICE_FEATURE_CMD_GET_IMAGE_EFFECT = 66
    IS_DEVICE_FEATURE_CMD_GET_IMAGE_EFFECT_DEFAULT = 67
    IS_DEVICE_FEATURE_CMD_GET_EXTENDED_PIXELCLOCK_RANGE_ENABLE_DEFAULT = 68
    IS_DEVICE_FEATURE_CMD_GET_EXTENDED_PIXELCLOCK_RANGE_ENABLE = 69
    IS_DEVICE_FEATURE_CMD_SET_EXTENDED_PIXELCLOCK_RANGE_ENABLE = 70
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_SCOPE = 71
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_PARAMS = 72
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_SET_PARAMS = 73
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_MODE_DEFAULT = 74
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_MODE = 75
    IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_SET_MODE = 76
    IS_DEVICE_FEATURE_CMD_SET_I2C_TARGET = 77
    IS_DEVICE_FEATURE_CMD_SET_WIDE_DYNAMIC_RANGE_MODE = 78
    IS_DEVICE_FEATURE_CMD_GET_WIDE_DYNAMIC_RANGE_MODE = 79
    IS_DEVICE_FEATURE_CMD_GET_WIDE_DYNAMIC_RANGE_MODE_DEFAULT = 80
    IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_BLACK_REFERENCE_MODES = 81
    IS_DEVICE_FEATURE_CMD_SET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE = 82
    IS_DEVICE_FEATURE_CMD_GET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE = 83
    IS_DEVICE_FEATURE_CMD_GET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE_DEFAULT = 84
    IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE_SUPPORTED_LINE_MODES = 85
    IS_DEVICE_FEATURE_CMD_SET_REPEATED_START_CONDITION_I2C = 86
    IS_DEVICE_FEATURE_CMD_GET_REPEATED_START_CONDITION_I2C = 87
    IS_DEVICE_FEATURE_CMD_GET_REPEATED_START_CONDITION_I2C_DEFAULT = 88
    IS_DEVICE_FEATURE_CMD_GET_TEMPERATURE_STATUS = 89
    IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE = 90
    IS_DEVICE_FEATURE_CMD_SET_MEMORY_MODE_ENABLE = 91
    IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE_DEFAULT = 92
    IS_DEVICE_FEATURE_CMD_93 = 93
    IS_DEVICE_FEATURE_CMD_94 = 94
    IS_DEVICE_FEATURE_CMD_95 = 95
    IS_DEVICE_FEATURE_CMD_96 = 96
    IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_EXTERNAL_INTERFACES = 97
    IS_DEVICE_FEATURE_CMD_GET_EXTERNAL_INTERFACE = 98
    IS_DEVICE_FEATURE_CMD_SET_EXTERNAL_INTERFACE = 99
    IS_DEVICE_FEATURE_CMD_EXTENDED_AWB_LIMITS_GET = 100
    IS_DEVICE_FEATURE_CMD_EXTENDED_AWB_LIMITS_SET = 101
    IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE_SUPPORTED = 102
    IS_DEVICE_FEATURE_CMD_SET_SPI_TARGET = 103
    IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_IS_CALIBRATED = 104
    IS_DEVICE_FEATURE_CMD_SET_FPN_CORRECTION_DATA_LOADING = 105
    IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_DATA_LOADING = 106
    IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_BUFFER_LIMIT = 107
    IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_BUFFER_LIMIT_DEFAULT = 108
    IS_DEVICE_FEATURE_CMD_SET_MEMORY_MODE_BUFFER_LIMIT = 109
    IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_DATA_LOADING_DEFAULT = 110


IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_FEATURES = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_FEATURES
IS_DEVICE_FEATURE_CMD_SET_LINESCAN_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_LINESCAN_MODE
IS_DEVICE_FEATURE_CMD_GET_LINESCAN_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LINESCAN_MODE
IS_DEVICE_FEATURE_CMD_SET_LINESCAN_NUMBER = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_LINESCAN_NUMBER
IS_DEVICE_FEATURE_CMD_GET_LINESCAN_NUMBER = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LINESCAN_NUMBER
IS_DEVICE_FEATURE_CMD_SET_SHUTTER_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_SHUTTER_MODE
IS_DEVICE_FEATURE_CMD_GET_SHUTTER_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SHUTTER_MODE
IS_DEVICE_FEATURE_CMD_SET_PREFER_XS_HS_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_PREFER_XS_HS_MODE
IS_DEVICE_FEATURE_CMD_GET_PREFER_XS_HS_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_PREFER_XS_HS_MODE
IS_DEVICE_FEATURE_CMD_GET_DEFAULT_PREFER_XS_HS_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_DEFAULT_PREFER_XS_HS_MODE
IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_LOG_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LOG_MODE
IS_DEVICE_FEATURE_CMD_SET_LOG_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_LOG_MODE
IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE_RANGE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE_RANGE
IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_VALUE
IS_DEVICE_FEATURE_CMD_SET_LOG_MODE_MANUAL_VALUE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_LOG_MODE_MANUAL_VALUE
IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN_RANGE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN_RANGE
IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LOG_MODE_MANUAL_GAIN
IS_DEVICE_FEATURE_CMD_SET_LOG_MODE_MANUAL_GAIN = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_LOG_MODE_MANUAL_GAIN
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE
IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_MODE
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION_RANGE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION_RANGE
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_POSITION
IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_POSITION = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_POSITION
IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_MODE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_MODE_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_MODE
IS_DEVICE_FEATURE_CMD_SET_FPN_CORRECTION_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_FPN_CORRECTION_MODE
IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN_RANGE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN_RANGE
IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SENSOR_SOURCE_GAIN
IS_DEVICE_FEATURE_CMD_SET_SENSOR_SOURCE_GAIN = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_SENSOR_SOURCE_GAIN
IS_DEVICE_FEATURE_CMD_GET_BLACK_REFERENCE_MODE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_BLACK_REFERENCE_MODE_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_BLACK_REFERENCE_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_BLACK_REFERENCE_MODE
IS_DEVICE_FEATURE_CMD_SET_BLACK_REFERENCE_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_BLACK_REFERENCE_MODE
IS_DEVICE_FEATURE_CMD_GET_ALLOW_RAW_WITH_LUT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_ALLOW_RAW_WITH_LUT
IS_DEVICE_FEATURE_CMD_SET_ALLOW_RAW_WITH_LUT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_ALLOW_RAW_WITH_LUT
IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_SENSOR_BIT_DEPTHS = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_SENSOR_BIT_DEPTHS
IS_DEVICE_FEATURE_CMD_GET_SENSOR_BIT_DEPTH_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SENSOR_BIT_DEPTH_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_SENSOR_BIT_DEPTH = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SENSOR_BIT_DEPTH
IS_DEVICE_FEATURE_CMD_SET_SENSOR_BIT_DEPTH = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_SENSOR_BIT_DEPTH
IS_DEVICE_FEATURE_CMD_GET_TEMPERATURE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_TEMPERATURE
IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION
IS_DEVICE_FEATURE_CMD_SET_JPEG_COMPRESSION = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_JPEG_COMPRESSION
IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION_RANGE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_JPEG_COMPRESSION_RANGE
IS_DEVICE_FEATURE_CMD_GET_NOISE_REDUCTION_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_NOISE_REDUCTION_MODE
IS_DEVICE_FEATURE_CMD_SET_NOISE_REDUCTION_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_NOISE_REDUCTION_MODE
IS_DEVICE_FEATURE_CMD_GET_NOISE_REDUCTION_MODE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_NOISE_REDUCTION_MODE_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_TIMESTAMP_CONFIGURATION = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_TIMESTAMP_CONFIGURATION
IS_DEVICE_FEATURE_CMD_SET_TIMESTAMP_CONFIGURATION = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_TIMESTAMP_CONFIGURATION
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_NUMBER = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_NUMBER
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_LIST = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT_LIST
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_HEIGHT
IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_HEIGHT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_HEIGHT
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION_RANGE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION_RANGE
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION
IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_VERTICAL_AOI_MERGE_ADDITIONAL_POSITION
IS_DEVICE_FEATURE_CMD_GET_SENSOR_TEMPERATURE_NUMERICAL_VALUE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SENSOR_TEMPERATURE_NUMERICAL_VALUE
IS_DEVICE_FEATURE_CMD_SET_IMAGE_EFFECT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_IMAGE_EFFECT
IS_DEVICE_FEATURE_CMD_GET_IMAGE_EFFECT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_IMAGE_EFFECT
IS_DEVICE_FEATURE_CMD_GET_IMAGE_EFFECT_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_IMAGE_EFFECT_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_EXTENDED_PIXELCLOCK_RANGE_ENABLE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_EXTENDED_PIXELCLOCK_RANGE_ENABLE_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_EXTENDED_PIXELCLOCK_RANGE_ENABLE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_EXTENDED_PIXELCLOCK_RANGE_ENABLE
IS_DEVICE_FEATURE_CMD_SET_EXTENDED_PIXELCLOCK_RANGE_ENABLE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_EXTENDED_PIXELCLOCK_RANGE_ENABLE
IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_SCOPE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_SCOPE
IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_PARAMS = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_PARAMS
IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_SET_PARAMS = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_SET_PARAMS
IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_MODE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_MODE_DEFAULT
IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_GET_MODE
IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_SET_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_MULTI_INTEGRATION_SET_MODE
IS_DEVICE_FEATURE_CMD_SET_I2C_TARGET = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_I2C_TARGET
IS_DEVICE_FEATURE_CMD_SET_WIDE_DYNAMIC_RANGE_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_WIDE_DYNAMIC_RANGE_MODE
IS_DEVICE_FEATURE_CMD_GET_WIDE_DYNAMIC_RANGE_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_WIDE_DYNAMIC_RANGE_MODE
IS_DEVICE_FEATURE_CMD_GET_WIDE_DYNAMIC_RANGE_MODE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_WIDE_DYNAMIC_RANGE_MODE_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_BLACK_REFERENCE_MODES = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_BLACK_REFERENCE_MODES
IS_DEVICE_FEATURE_CMD_SET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE
IS_DEVICE_FEATURE_CMD_GET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE
IS_DEVICE_FEATURE_CMD_GET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_LEVEL_CONTROLLED_TRIGGER_INPUT_MODE_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE_SUPPORTED_LINE_MODES = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_VERTICAL_AOI_MERGE_MODE_SUPPORTED_LINE_MODES
IS_DEVICE_FEATURE_CMD_SET_REPEATED_START_CONDITION_I2C = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_REPEATED_START_CONDITION_I2C
IS_DEVICE_FEATURE_CMD_GET_REPEATED_START_CONDITION_I2C = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_REPEATED_START_CONDITION_I2C
IS_DEVICE_FEATURE_CMD_GET_REPEATED_START_CONDITION_I2C_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_REPEATED_START_CONDITION_I2C_DEFAULT
IS_DEVICE_FEATURE_CMD_GET_TEMPERATURE_STATUS = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_TEMPERATURE_STATUS
IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE
IS_DEVICE_FEATURE_CMD_SET_MEMORY_MODE_ENABLE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_MEMORY_MODE_ENABLE
IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE_DEFAULT
IS_DEVICE_FEATURE_CMD_93 = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_93
IS_DEVICE_FEATURE_CMD_94 = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_94
IS_DEVICE_FEATURE_CMD_95 = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_95
IS_DEVICE_FEATURE_CMD_96 = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_96
IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_EXTERNAL_INTERFACES = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_SUPPORTED_EXTERNAL_INTERFACES
IS_DEVICE_FEATURE_CMD_GET_EXTERNAL_INTERFACE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_EXTERNAL_INTERFACE
IS_DEVICE_FEATURE_CMD_SET_EXTERNAL_INTERFACE = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_EXTERNAL_INTERFACE
IS_DEVICE_FEATURE_CMD_EXTENDED_AWB_LIMITS_GET = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_EXTENDED_AWB_LIMITS_GET
IS_DEVICE_FEATURE_CMD_EXTENDED_AWB_LIMITS_SET = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_EXTENDED_AWB_LIMITS_SET
IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE_SUPPORTED = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_ENABLE_SUPPORTED
IS_DEVICE_FEATURE_CMD_SET_SPI_TARGET = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_SPI_TARGET
IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_IS_CALIBRATED = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_IS_CALIBRATED
IS_DEVICE_FEATURE_CMD_SET_FPN_CORRECTION_DATA_LOADING = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_FPN_CORRECTION_DATA_LOADING
IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_DATA_LOADING = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_DATA_LOADING
IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_BUFFER_LIMIT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_BUFFER_LIMIT
IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_BUFFER_LIMIT_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_MEMORY_MODE_BUFFER_LIMIT_DEFAULT
IS_DEVICE_FEATURE_CMD_SET_MEMORY_MODE_BUFFER_LIMIT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_SET_MEMORY_MODE_BUFFER_LIMIT
IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_DATA_LOADING_DEFAULT = DEVICE_FEATURE_CMD.IS_DEVICE_FEATURE_CMD_GET_FPN_CORRECTION_DATA_LOADING_DEFAULT


class DEVICE_FEATURE_MODE_CAPS(_CtypesEnum):
    IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING = 1
    IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL = 2
    IS_DEVICE_FEATURE_CAP_LINESCAN_MODE_FAST = 4
    IS_DEVICE_FEATURE_CAP_LINESCAN_NUMBER = 8
    IS_DEVICE_FEATURE_CAP_PREFER_XS_HS_MODE = 16
    IS_DEVICE_FEATURE_CAP_LOG_MODE = 32
    IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING_GLOBAL_START = 64
    IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL_ALTERNATIVE_TIMING = 128
    IS_DEVICE_FEATURE_CAP_VERTICAL_AOI_MERGE = 256
    IS_DEVICE_FEATURE_CAP_FPN_CORRECTION = 512
    IS_DEVICE_FEATURE_CAP_SENSOR_SOURCE_GAIN = 1024
    IS_DEVICE_FEATURE_CAP_BLACK_REFERENCE = 2048
    IS_DEVICE_FEATURE_CAP_SENSOR_BIT_DEPTH = 4096
    IS_DEVICE_FEATURE_CAP_TEMPERATURE = 8192
    IS_DEVICE_FEATURE_CAP_JPEG_COMPRESSION = 16384
    IS_DEVICE_FEATURE_CAP_NOISE_REDUCTION = 32768
    IS_DEVICE_FEATURE_CAP_TIMESTAMP_CONFIGURATION = 65536
    IS_DEVICE_FEATURE_CAP_IMAGE_EFFECT = 131072
    IS_DEVICE_FEATURE_CAP_EXTENDED_PIXELCLOCK_RANGE = 262144
    IS_DEVICE_FEATURE_CAP_MULTI_INTEGRATION = 524288
    IS_DEVICE_FEATURE_CAP_WIDE_DYNAMIC_RANGE = 1048576
    IS_DEVICE_FEATURE_CAP_LEVEL_CONTROLLED_TRIGGER = 2097152
    IS_DEVICE_FEATURE_CAP_REPEATED_START_CONDITION_I2C = 4194304
    IS_DEVICE_FEATURE_CAP_TEMPERATURE_STATUS = 8388608
    IS_DEVICE_FEATURE_CAP_MEMORY_MODE = 16777216
    IS_DEVICE_FEATURE_CAP_SEND_EXTERNAL_INTERFACE_DATA = 33554432


IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING
IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL
IS_DEVICE_FEATURE_CAP_LINESCAN_MODE_FAST = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_LINESCAN_MODE_FAST
IS_DEVICE_FEATURE_CAP_LINESCAN_NUMBER = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_LINESCAN_NUMBER
IS_DEVICE_FEATURE_CAP_PREFER_XS_HS_MODE = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_PREFER_XS_HS_MODE
IS_DEVICE_FEATURE_CAP_LOG_MODE = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_LOG_MODE
IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING_GLOBAL_START = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING_GLOBAL_START
IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL_ALTERNATIVE_TIMING = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL_ALTERNATIVE_TIMING
IS_DEVICE_FEATURE_CAP_VERTICAL_AOI_MERGE = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_VERTICAL_AOI_MERGE
IS_DEVICE_FEATURE_CAP_FPN_CORRECTION = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_FPN_CORRECTION
IS_DEVICE_FEATURE_CAP_SENSOR_SOURCE_GAIN = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_SENSOR_SOURCE_GAIN
IS_DEVICE_FEATURE_CAP_BLACK_REFERENCE = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_BLACK_REFERENCE
IS_DEVICE_FEATURE_CAP_SENSOR_BIT_DEPTH = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_SENSOR_BIT_DEPTH
IS_DEVICE_FEATURE_CAP_TEMPERATURE = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_TEMPERATURE
IS_DEVICE_FEATURE_CAP_JPEG_COMPRESSION = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_JPEG_COMPRESSION
IS_DEVICE_FEATURE_CAP_NOISE_REDUCTION = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_NOISE_REDUCTION
IS_DEVICE_FEATURE_CAP_TIMESTAMP_CONFIGURATION = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_TIMESTAMP_CONFIGURATION
IS_DEVICE_FEATURE_CAP_IMAGE_EFFECT = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_IMAGE_EFFECT
IS_DEVICE_FEATURE_CAP_EXTENDED_PIXELCLOCK_RANGE = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_EXTENDED_PIXELCLOCK_RANGE
IS_DEVICE_FEATURE_CAP_MULTI_INTEGRATION = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_MULTI_INTEGRATION
IS_DEVICE_FEATURE_CAP_WIDE_DYNAMIC_RANGE = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_WIDE_DYNAMIC_RANGE
IS_DEVICE_FEATURE_CAP_LEVEL_CONTROLLED_TRIGGER = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_LEVEL_CONTROLLED_TRIGGER
IS_DEVICE_FEATURE_CAP_REPEATED_START_CONDITION_I2C = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_REPEATED_START_CONDITION_I2C
IS_DEVICE_FEATURE_CAP_TEMPERATURE_STATUS = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_TEMPERATURE_STATUS
IS_DEVICE_FEATURE_CAP_MEMORY_MODE = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_MEMORY_MODE
IS_DEVICE_FEATURE_CAP_SEND_EXTERNAL_INTERFACE_DATA = DEVICE_FEATURE_MODE_CAPS.IS_DEVICE_FEATURE_CAP_SEND_EXTERNAL_INTERFACE_DATA


class IS_TEMPERATURE_CONTROL_STATUS(_CtypesEnum):
    TEMPERATURE_CONTROL_STATUS_NORMAL = 0
    TEMPERATURE_CONTROL_STATUS_WARNING = 1
    TEMPERATURE_CONTROL_STATUS_CRITICAL = 2


TEMPERATURE_CONTROL_STATUS_NORMAL = IS_TEMPERATURE_CONTROL_STATUS.TEMPERATURE_CONTROL_STATUS_NORMAL
TEMPERATURE_CONTROL_STATUS_WARNING = IS_TEMPERATURE_CONTROL_STATUS.TEMPERATURE_CONTROL_STATUS_WARNING
TEMPERATURE_CONTROL_STATUS_CRITICAL = IS_TEMPERATURE_CONTROL_STATUS.TEMPERATURE_CONTROL_STATUS_CRITICAL


class NOISE_REDUCTION_MODES(_CtypesEnum):
    IS_NOISE_REDUCTION_OFF = 0
    IS_NOISE_REDUCTION_ADAPTIVE = 1


IS_NOISE_REDUCTION_OFF = NOISE_REDUCTION_MODES.IS_NOISE_REDUCTION_OFF
IS_NOISE_REDUCTION_ADAPTIVE = NOISE_REDUCTION_MODES.IS_NOISE_REDUCTION_ADAPTIVE


class LOG_MODES(_CtypesEnum):
    IS_LOG_MODE_FACTORY_DEFAULT = 0
    IS_LOG_MODE_OFF = 1
    IS_LOG_MODE_MANUAL = 2
    IS_LOG_MODE_AUTO = 3


IS_LOG_MODE_FACTORY_DEFAULT = LOG_MODES.IS_LOG_MODE_FACTORY_DEFAULT
IS_LOG_MODE_OFF = LOG_MODES.IS_LOG_MODE_OFF
IS_LOG_MODE_MANUAL = LOG_MODES.IS_LOG_MODE_MANUAL
IS_LOG_MODE_AUTO = LOG_MODES.IS_LOG_MODE_AUTO


class VERTICAL_AOI_MERGE_MODES(_CtypesEnum):
    IS_VERTICAL_AOI_MERGE_MODE_OFF = 0
    IS_VERTICAL_AOI_MERGE_MODE_FREERUN = 1
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_SOFTWARE = 2
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_FALLING_GPIO1 = 3
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_RISING_GPIO1 = 4
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_FALLING_GPIO2 = 5
    IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_RISING_GPIO2 = 6


IS_VERTICAL_AOI_MERGE_MODE_OFF = VERTICAL_AOI_MERGE_MODES.IS_VERTICAL_AOI_MERGE_MODE_OFF
IS_VERTICAL_AOI_MERGE_MODE_FREERUN = VERTICAL_AOI_MERGE_MODES.IS_VERTICAL_AOI_MERGE_MODE_FREERUN
IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_SOFTWARE = VERTICAL_AOI_MERGE_MODES.IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_SOFTWARE
IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_FALLING_GPIO1 = VERTICAL_AOI_MERGE_MODES.IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_FALLING_GPIO1
IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_RISING_GPIO1 = VERTICAL_AOI_MERGE_MODES.IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_RISING_GPIO1
IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_FALLING_GPIO2 = VERTICAL_AOI_MERGE_MODES.IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_FALLING_GPIO2
IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_RISING_GPIO2 = VERTICAL_AOI_MERGE_MODES.IS_VERTICAL_AOI_MERGE_MODE_TRIGGERED_RISING_GPIO2


class VERTICAL_AOI_MERGE_MODE_LINE_TRIGGER(_CtypesEnum):
    IS_VERTICAL_AOI_MERGE_MODE_LINE_FREERUN = 1
    IS_VERTICAL_AOI_MERGE_MODE_LINE_SOFTWARE_TRIGGER = 2
    IS_VERTICAL_AOI_MERGE_MODE_LINE_GPIO_TRIGGER = 4


IS_VERTICAL_AOI_MERGE_MODE_LINE_FREERUN = VERTICAL_AOI_MERGE_MODE_LINE_TRIGGER.IS_VERTICAL_AOI_MERGE_MODE_LINE_FREERUN
IS_VERTICAL_AOI_MERGE_MODE_LINE_SOFTWARE_TRIGGER = VERTICAL_AOI_MERGE_MODE_LINE_TRIGGER.IS_VERTICAL_AOI_MERGE_MODE_LINE_SOFTWARE_TRIGGER
IS_VERTICAL_AOI_MERGE_MODE_LINE_GPIO_TRIGGER = VERTICAL_AOI_MERGE_MODE_LINE_TRIGGER.IS_VERTICAL_AOI_MERGE_MODE_LINE_GPIO_TRIGGER


class LEVEL_CONTROLLED_TRIGGER_INPUT_MODES(_CtypesEnum):
    IS_LEVEL_CONTROLLED_TRIGGER_INPUT_OFF = 0
    IS_LEVEL_CONTROLLED_TRIGGER_INPUT_ON = 1


IS_LEVEL_CONTROLLED_TRIGGER_INPUT_OFF = LEVEL_CONTROLLED_TRIGGER_INPUT_MODES.IS_LEVEL_CONTROLLED_TRIGGER_INPUT_OFF
IS_LEVEL_CONTROLLED_TRIGGER_INPUT_ON = LEVEL_CONTROLLED_TRIGGER_INPUT_MODES.IS_LEVEL_CONTROLLED_TRIGGER_INPUT_ON


class FPN_CORRECTION_MODES(_CtypesEnum):
    IS_FPN_CORRECTION_MODE_OFF = 0
    IS_FPN_CORRECTION_MODE_HARDWARE = 1


IS_FPN_CORRECTION_MODE_OFF = FPN_CORRECTION_MODES.IS_FPN_CORRECTION_MODE_OFF
IS_FPN_CORRECTION_MODE_HARDWARE = FPN_CORRECTION_MODES.IS_FPN_CORRECTION_MODE_HARDWARE


class FPN_CORRECTION_DATA_LOADING(_CtypesEnum):
    IS_FPN_CORRECTION_DATA_LOADING_OFF = 0
    IS_FPN_CORRECTION_DATA_LOADING_ON = 1


IS_FPN_CORRECTION_DATA_LOADING_OFF = FPN_CORRECTION_DATA_LOADING.IS_FPN_CORRECTION_DATA_LOADING_OFF
IS_FPN_CORRECTION_DATA_LOADING_ON = FPN_CORRECTION_DATA_LOADING.IS_FPN_CORRECTION_DATA_LOADING_ON


class BLACK_REFERENCE_MODES(_CtypesEnum):
    IS_BLACK_REFERENCE_MODE_OFF = 0
    IS_BLACK_REFERENCE_MODE_COLUMNS_LEFT = 1
    IS_BLACK_REFERENCE_MODE_ROWS_TOP = 2


IS_BLACK_REFERENCE_MODE_OFF = BLACK_REFERENCE_MODES.IS_BLACK_REFERENCE_MODE_OFF
IS_BLACK_REFERENCE_MODE_COLUMNS_LEFT = BLACK_REFERENCE_MODES.IS_BLACK_REFERENCE_MODE_COLUMNS_LEFT
IS_BLACK_REFERENCE_MODE_ROWS_TOP = BLACK_REFERENCE_MODES.IS_BLACK_REFERENCE_MODE_ROWS_TOP


class SENSOR_BIT_DEPTH(_CtypesEnum):
    IS_SENSOR_BIT_DEPTH_AUTO = 0
    IS_SENSOR_BIT_DEPTH_8_BIT = 1
    IS_SENSOR_BIT_DEPTH_10_BIT = 2
    IS_SENSOR_BIT_DEPTH_12_BIT = 4


IS_SENSOR_BIT_DEPTH_AUTO = SENSOR_BIT_DEPTH.IS_SENSOR_BIT_DEPTH_AUTO
IS_SENSOR_BIT_DEPTH_8_BIT = SENSOR_BIT_DEPTH.IS_SENSOR_BIT_DEPTH_8_BIT
IS_SENSOR_BIT_DEPTH_10_BIT = SENSOR_BIT_DEPTH.IS_SENSOR_BIT_DEPTH_10_BIT
IS_SENSOR_BIT_DEPTH_12_BIT = SENSOR_BIT_DEPTH.IS_SENSOR_BIT_DEPTH_12_BIT


class TIMESTAMP_CONFIGURATION_MODE(_CtypesEnum):
    IS_RESET_TIMESTAMP_ONCE = 1


IS_RESET_TIMESTAMP_ONCE = TIMESTAMP_CONFIGURATION_MODE.IS_RESET_TIMESTAMP_ONCE


class TIMESTAMP_CONFIGURATION_PIN(_CtypesEnum):
    TIMESTAMP_CONFIGURATION_PIN_NONE = 0
    TIMESTAMP_CONFIGURATION_PIN_TRIGGER = 1
    TIMESTAMP_CONFIGURATION_PIN_GPIO_1 = 2
    TIMESTAMP_CONFIGURATION_PIN_GPIO_2 = 3


TIMESTAMP_CONFIGURATION_PIN_NONE = TIMESTAMP_CONFIGURATION_PIN.TIMESTAMP_CONFIGURATION_PIN_NONE
TIMESTAMP_CONFIGURATION_PIN_TRIGGER = TIMESTAMP_CONFIGURATION_PIN.TIMESTAMP_CONFIGURATION_PIN_TRIGGER
TIMESTAMP_CONFIGURATION_PIN_GPIO_1 = TIMESTAMP_CONFIGURATION_PIN.TIMESTAMP_CONFIGURATION_PIN_GPIO_1
TIMESTAMP_CONFIGURATION_PIN_GPIO_2 = TIMESTAMP_CONFIGURATION_PIN.TIMESTAMP_CONFIGURATION_PIN_GPIO_2


class TIMESTAMP_CONFIGURATION_EDGE(_CtypesEnum):
    TIMESTAMP_CONFIGURATION_EDGE_FALLING = 0
    TIMESTAMP_CONFIGURATION_EDGE_RISING = 1


TIMESTAMP_CONFIGURATION_EDGE_FALLING = TIMESTAMP_CONFIGURATION_EDGE.TIMESTAMP_CONFIGURATION_EDGE_FALLING
TIMESTAMP_CONFIGURATION_EDGE_RISING = TIMESTAMP_CONFIGURATION_EDGE.TIMESTAMP_CONFIGURATION_EDGE_RISING


class IMAGE_EFFECT_MODE(_CtypesEnum):
    IS_IMAGE_EFFECT_DISABLE = 0
    IS_IMAGE_EFFECT_SEPIA = 1
    IS_IMAGE_EFFECT_MONOCHROME = 2
    IS_IMAGE_EFFECT_NEGATIVE = 3
    IS_IMAGE_EFFECT_CROSSHAIRS = 4


IS_IMAGE_EFFECT_DISABLE = IMAGE_EFFECT_MODE.IS_IMAGE_EFFECT_DISABLE
IS_IMAGE_EFFECT_SEPIA = IMAGE_EFFECT_MODE.IS_IMAGE_EFFECT_SEPIA
IS_IMAGE_EFFECT_MONOCHROME = IMAGE_EFFECT_MODE.IS_IMAGE_EFFECT_MONOCHROME
IS_IMAGE_EFFECT_NEGATIVE = IMAGE_EFFECT_MODE.IS_IMAGE_EFFECT_NEGATIVE
IS_IMAGE_EFFECT_CROSSHAIRS = IMAGE_EFFECT_MODE.IS_IMAGE_EFFECT_CROSSHAIRS


class IS_EXTENDED_PIXELCLOCK_RANGE(_CtypesEnum):
    EXTENDED_PIXELCLOCK_RANGE_OFF = 0
    EXTENDED_PIXELCLOCK_RANGE_ON = 1


EXTENDED_PIXELCLOCK_RANGE_OFF = IS_EXTENDED_PIXELCLOCK_RANGE.EXTENDED_PIXELCLOCK_RANGE_OFF
EXTENDED_PIXELCLOCK_RANGE_ON = IS_EXTENDED_PIXELCLOCK_RANGE.EXTENDED_PIXELCLOCK_RANGE_ON


class IS_MULTI_INTEGRATION_MODE(_CtypesEnum):
    MULTI_INTEGRATION_MODE_OFF = 0
    MULTI_INTEGRATION_MODE_SOFTWARE = 1
    MULTI_INTEGRATION_MODE_GPIO1 = 2
    MULTI_INTEGRATION_MODE_GPIO2 = 3


MULTI_INTEGRATION_MODE_OFF = IS_MULTI_INTEGRATION_MODE.MULTI_INTEGRATION_MODE_OFF
MULTI_INTEGRATION_MODE_SOFTWARE = IS_MULTI_INTEGRATION_MODE.MULTI_INTEGRATION_MODE_SOFTWARE
MULTI_INTEGRATION_MODE_GPIO1 = IS_MULTI_INTEGRATION_MODE.MULTI_INTEGRATION_MODE_GPIO1
MULTI_INTEGRATION_MODE_GPIO2 = IS_MULTI_INTEGRATION_MODE.MULTI_INTEGRATION_MODE_GPIO2


class IS_I2C_TARGET(_CtypesEnum):
    I2C_TARGET_DEFAULT = 0
    I2C_TARGET_SENSOR_1 = 1
    I2C_TARGET_SENSOR_2 = 2
    I2C_TARGET_LOGIC_BOARD = 4


I2C_TARGET_DEFAULT = IS_I2C_TARGET.I2C_TARGET_DEFAULT
I2C_TARGET_SENSOR_1 = IS_I2C_TARGET.I2C_TARGET_SENSOR_1
I2C_TARGET_SENSOR_2 = IS_I2C_TARGET.I2C_TARGET_SENSOR_2
I2C_TARGET_LOGIC_BOARD = IS_I2C_TARGET.I2C_TARGET_LOGIC_BOARD


class IS_SPI_TARGET(_CtypesEnum):
    SPI_TARGET_DEFAULT = 0
    SPI_TARGET_SENSOR_1 = 1
    SPI_TARGET_SENSOR_2 = 2


SPI_TARGET_DEFAULT = IS_SPI_TARGET.SPI_TARGET_DEFAULT
SPI_TARGET_SENSOR_1 = IS_SPI_TARGET.SPI_TARGET_SENSOR_1
SPI_TARGET_SENSOR_2 = IS_SPI_TARGET.SPI_TARGET_SENSOR_2


class IS_MEMORY_MODE(_CtypesEnum):
    IS_MEMORY_MODE_OFF = 0
    IS_MEMORY_MODE_ON = 1


IS_MEMORY_MODE_OFF = IS_MEMORY_MODE.IS_MEMORY_MODE_OFF
IS_MEMORY_MODE_ON = IS_MEMORY_MODE.IS_MEMORY_MODE_ON


class IS_EXTERNAL_INTERFACE_TYPE(_CtypesEnum):
    IS_EXTERNAL_INTERFACE_TYPE_NONE = 0
    IS_EXTERNAL_INTERFACE_TYPE_I2C = 1


IS_EXTERNAL_INTERFACE_TYPE_NONE = IS_EXTERNAL_INTERFACE_TYPE.IS_EXTERNAL_INTERFACE_TYPE_NONE
IS_EXTERNAL_INTERFACE_TYPE_I2C = IS_EXTERNAL_INTERFACE_TYPE.IS_EXTERNAL_INTERFACE_TYPE_I2C


class IS_EXTERNAL_INTERFACE_REGISTER_TYPE(_CtypesEnum):
    IS_EXTERNAL_INTERFACE_REGISTER_TYPE_8BIT = 0
    IS_EXTERNAL_INTERFACE_REGISTER_TYPE_16BIT = 1
    IS_EXTERNAL_INTERFACE_REGISTER_TYPE_NONE = 2


IS_EXTERNAL_INTERFACE_REGISTER_TYPE_8BIT = IS_EXTERNAL_INTERFACE_REGISTER_TYPE.IS_EXTERNAL_INTERFACE_REGISTER_TYPE_8BIT
IS_EXTERNAL_INTERFACE_REGISTER_TYPE_16BIT = IS_EXTERNAL_INTERFACE_REGISTER_TYPE.IS_EXTERNAL_INTERFACE_REGISTER_TYPE_16BIT
IS_EXTERNAL_INTERFACE_REGISTER_TYPE_NONE = IS_EXTERNAL_INTERFACE_REGISTER_TYPE.IS_EXTERNAL_INTERFACE_REGISTER_TYPE_NONE


class IS_EXTERNAL_INTERFACE_EVENT(_CtypesEnum):
    IS_EXTERNAL_INTERFACE_EVENT_RISING_VSYNC = 0
    IS_EXTERNAL_INTERFACE_EVENT_FALLING_VSYNC = 1


IS_EXTERNAL_INTERFACE_EVENT_RISING_VSYNC = IS_EXTERNAL_INTERFACE_EVENT.IS_EXTERNAL_INTERFACE_EVENT_RISING_VSYNC
IS_EXTERNAL_INTERFACE_EVENT_FALLING_VSYNC = IS_EXTERNAL_INTERFACE_EVENT.IS_EXTERNAL_INTERFACE_EVENT_FALLING_VSYNC


class IS_EXTERNAL_INTERFACE_DATA(_CtypesEnum):
    IS_EXTERNAL_INTERFACE_DATA_USER = 0
    IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_FULL = 1
    IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_LOWBYTE = 2
    IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_HIGHBYTE = 3


IS_EXTERNAL_INTERFACE_DATA_USER = IS_EXTERNAL_INTERFACE_DATA.IS_EXTERNAL_INTERFACE_DATA_USER
IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_FULL = IS_EXTERNAL_INTERFACE_DATA.IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_FULL
IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_LOWBYTE = IS_EXTERNAL_INTERFACE_DATA.IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_LOWBYTE
IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_HIGHBYTE = IS_EXTERNAL_INTERFACE_DATA.IS_EXTERNAL_INTERFACE_DATA_TIMESTAMP_HIGHBYTE


class EXPOSURE_CMD(_CtypesEnum):
    IS_EXPOSURE_CMD_GET_CAPS = 1
    IS_EXPOSURE_CMD_GET_EXPOSURE_DEFAULT = 2
    IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN = 3
    IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX = 4
    IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_INC = 5
    IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE = 6
    IS_EXPOSURE_CMD_GET_EXPOSURE = 7
    IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MIN = 8
    IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MAX = 9
    IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_INC = 10
    IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE = 11
    IS_EXPOSURE_CMD_SET_EXPOSURE = 12
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MIN = 13
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MAX = 14
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_INC = 15
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE = 16
    IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_ENABLE = 17
    IS_EXPOSURE_CMD_SET_LONG_EXPOSURE_ENABLE = 18
    IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_DEFAULT = 19
    IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_RANGE = 20
    IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO = 21
    IS_EXPOSURE_CMD_SET_DUAL_EXPOSURE_RATIO = 22


IS_EXPOSURE_CMD_GET_CAPS = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_CAPS
IS_EXPOSURE_CMD_GET_EXPOSURE_DEFAULT = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_EXPOSURE_DEFAULT
IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN
IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX
IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_INC = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_INC
IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE
IS_EXPOSURE_CMD_GET_EXPOSURE = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_EXPOSURE
IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MIN = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MIN
IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MAX = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_MAX
IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_INC = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE_INC
IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_FINE_INCREMENT_RANGE
IS_EXPOSURE_CMD_SET_EXPOSURE = EXPOSURE_CMD.IS_EXPOSURE_CMD_SET_EXPOSURE
IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MIN = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MIN
IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MAX = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_MAX
IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_INC = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE_INC
IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE
IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_ENABLE = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_ENABLE
IS_EXPOSURE_CMD_SET_LONG_EXPOSURE_ENABLE = EXPOSURE_CMD.IS_EXPOSURE_CMD_SET_LONG_EXPOSURE_ENABLE
IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_DEFAULT = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_DEFAULT
IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_RANGE = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO_RANGE
IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO = EXPOSURE_CMD.IS_EXPOSURE_CMD_GET_DUAL_EXPOSURE_RATIO
IS_EXPOSURE_CMD_SET_DUAL_EXPOSURE_RATIO = EXPOSURE_CMD.IS_EXPOSURE_CMD_SET_DUAL_EXPOSURE_RATIO


class EXPOSURE_CAPS(_CtypesEnum):
    IS_EXPOSURE_CAP_EXPOSURE = 1
    IS_EXPOSURE_CAP_FINE_INCREMENT = 2
    IS_EXPOSURE_CAP_LONG_EXPOSURE = 4
    IS_EXPOSURE_CAP_DUAL_EXPOSURE = 8


IS_EXPOSURE_CAP_EXPOSURE = EXPOSURE_CAPS.IS_EXPOSURE_CAP_EXPOSURE
IS_EXPOSURE_CAP_FINE_INCREMENT = EXPOSURE_CAPS.IS_EXPOSURE_CAP_FINE_INCREMENT
IS_EXPOSURE_CAP_LONG_EXPOSURE = EXPOSURE_CAPS.IS_EXPOSURE_CAP_LONG_EXPOSURE
IS_EXPOSURE_CAP_DUAL_EXPOSURE = EXPOSURE_CAPS.IS_EXPOSURE_CAP_DUAL_EXPOSURE


class TRIGGER_CMD(_CtypesEnum):
    IS_TRIGGER_CMD_GET_BURST_SIZE_SUPPORTED = 1
    IS_TRIGGER_CMD_GET_BURST_SIZE_RANGE = 2
    IS_TRIGGER_CMD_GET_BURST_SIZE = 3
    IS_TRIGGER_CMD_SET_BURST_SIZE = 4
    IS_TRIGGER_CMD_GET_FRAME_PRESCALER_SUPPORTED = 5
    IS_TRIGGER_CMD_GET_FRAME_PRESCALER_RANGE = 6
    IS_TRIGGER_CMD_GET_FRAME_PRESCALER = 7
    IS_TRIGGER_CMD_SET_FRAME_PRESCALER = 8
    IS_TRIGGER_CMD_GET_LINE_PRESCALER_SUPPORTED = 9
    IS_TRIGGER_CMD_GET_LINE_PRESCALER_RANGE = 10
    IS_TRIGGER_CMD_GET_LINE_PRESCALER = 11
    IS_TRIGGER_CMD_SET_LINE_PRESCALER = 12


IS_TRIGGER_CMD_GET_BURST_SIZE_SUPPORTED = TRIGGER_CMD.IS_TRIGGER_CMD_GET_BURST_SIZE_SUPPORTED
IS_TRIGGER_CMD_GET_BURST_SIZE_RANGE = TRIGGER_CMD.IS_TRIGGER_CMD_GET_BURST_SIZE_RANGE
IS_TRIGGER_CMD_GET_BURST_SIZE = TRIGGER_CMD.IS_TRIGGER_CMD_GET_BURST_SIZE
IS_TRIGGER_CMD_SET_BURST_SIZE = TRIGGER_CMD.IS_TRIGGER_CMD_SET_BURST_SIZE
IS_TRIGGER_CMD_GET_FRAME_PRESCALER_SUPPORTED = TRIGGER_CMD.IS_TRIGGER_CMD_GET_FRAME_PRESCALER_SUPPORTED
IS_TRIGGER_CMD_GET_FRAME_PRESCALER_RANGE = TRIGGER_CMD.IS_TRIGGER_CMD_GET_FRAME_PRESCALER_RANGE
IS_TRIGGER_CMD_GET_FRAME_PRESCALER = TRIGGER_CMD.IS_TRIGGER_CMD_GET_FRAME_PRESCALER
IS_TRIGGER_CMD_SET_FRAME_PRESCALER = TRIGGER_CMD.IS_TRIGGER_CMD_SET_FRAME_PRESCALER
IS_TRIGGER_CMD_GET_LINE_PRESCALER_SUPPORTED = TRIGGER_CMD.IS_TRIGGER_CMD_GET_LINE_PRESCALER_SUPPORTED
IS_TRIGGER_CMD_GET_LINE_PRESCALER_RANGE = TRIGGER_CMD.IS_TRIGGER_CMD_GET_LINE_PRESCALER_RANGE
IS_TRIGGER_CMD_GET_LINE_PRESCALER = TRIGGER_CMD.IS_TRIGGER_CMD_GET_LINE_PRESCALER
IS_TRIGGER_CMD_SET_LINE_PRESCALER = TRIGGER_CMD.IS_TRIGGER_CMD_SET_LINE_PRESCALER


class IS_DEVICE_INFO_CMD(_CtypesEnum):
    IS_DEVICE_INFO_CMD_GET_DEVICE_INFO = 33619969


IS_DEVICE_INFO_CMD_GET_DEVICE_INFO = IS_DEVICE_INFO_CMD.IS_DEVICE_INFO_CMD_GET_DEVICE_INFO


class IS_OPTIMAL_CAMERA_TIMING_CMD(_CtypesEnum):
    IS_OPTIMAL_CAMERA_TIMING_CMD_GET_PIXELCLOCK = 1
    IS_OPTIMAL_CAMERA_TIMING_CMD_GET_FRAMERATE = 2


IS_OPTIMAL_CAMERA_TIMING_CMD_GET_PIXELCLOCK = IS_OPTIMAL_CAMERA_TIMING_CMD.IS_OPTIMAL_CAMERA_TIMING_CMD_GET_PIXELCLOCK
IS_OPTIMAL_CAMERA_TIMING_CMD_GET_FRAMERATE = IS_OPTIMAL_CAMERA_TIMING_CMD.IS_OPTIMAL_CAMERA_TIMING_CMD_GET_FRAMERATE


class UEYE_ETH_DEVICESTATUS(_CtypesEnum):
    IS_ETH_DEVSTATUS_READY_TO_OPERATE = 1
    IS_ETH_DEVSTATUS_TESTING_IP_CURRENT = 2
    IS_ETH_DEVSTATUS_TESTING_IP_PERSISTENT = 4
    IS_ETH_DEVSTATUS_TESTING_IP_RANGE = 8
    IS_ETH_DEVSTATUS_INAPPLICABLE_IP_CURRENT = 16
    IS_ETH_DEVSTATUS_INAPPLICABLE_IP_PERSISTENT = 32
    IS_ETH_DEVSTATUS_INAPPLICABLE_IP_RANGE = 64
    IS_ETH_DEVSTATUS_UNPAIRED = 256
    IS_ETH_DEVSTATUS_PAIRING_IN_PROGRESS = 512
    IS_ETH_DEVSTATUS_PAIRED = 1024
    IS_ETH_DEVSTATUS_FORCE_100MBPS = 4096
    IS_ETH_DEVSTATUS_NO_COMPORT = 8192
    IS_ETH_DEVSTATUS_RECEIVING_FW_STARTER = 65536
    IS_ETH_DEVSTATUS_RECEIVING_FW_RUNTIME = 131072
    IS_ETH_DEVSTATUS_INAPPLICABLE_FW_RUNTIME = 262144
    IS_ETH_DEVSTATUS_INAPPLICABLE_FW_STARTER = 524288
    IS_ETH_DEVSTATUS_REBOOTING_FW_RUNTIME = 1048576
    IS_ETH_DEVSTATUS_REBOOTING_FW_STARTER = 2097152
    IS_ETH_DEVSTATUS_REBOOTING_FW_FAILSAFE = 4194304
    IS_ETH_DEVSTATUS_RUNTIME_FW_ERR0 = 2147483648


IS_ETH_DEVSTATUS_READY_TO_OPERATE = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_READY_TO_OPERATE
IS_ETH_DEVSTATUS_TESTING_IP_CURRENT = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_TESTING_IP_CURRENT
IS_ETH_DEVSTATUS_TESTING_IP_PERSISTENT = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_TESTING_IP_PERSISTENT
IS_ETH_DEVSTATUS_TESTING_IP_RANGE = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_TESTING_IP_RANGE
IS_ETH_DEVSTATUS_INAPPLICABLE_IP_CURRENT = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_INAPPLICABLE_IP_CURRENT
IS_ETH_DEVSTATUS_INAPPLICABLE_IP_PERSISTENT = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_INAPPLICABLE_IP_PERSISTENT
IS_ETH_DEVSTATUS_INAPPLICABLE_IP_RANGE = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_INAPPLICABLE_IP_RANGE
IS_ETH_DEVSTATUS_UNPAIRED = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_UNPAIRED
IS_ETH_DEVSTATUS_PAIRING_IN_PROGRESS = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_PAIRING_IN_PROGRESS
IS_ETH_DEVSTATUS_PAIRED = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_PAIRED
IS_ETH_DEVSTATUS_FORCE_100MBPS = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_FORCE_100MBPS
IS_ETH_DEVSTATUS_NO_COMPORT = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_NO_COMPORT
IS_ETH_DEVSTATUS_RECEIVING_FW_STARTER = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_RECEIVING_FW_STARTER
IS_ETH_DEVSTATUS_RECEIVING_FW_RUNTIME = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_RECEIVING_FW_RUNTIME
IS_ETH_DEVSTATUS_INAPPLICABLE_FW_RUNTIME = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_INAPPLICABLE_FW_RUNTIME
IS_ETH_DEVSTATUS_INAPPLICABLE_FW_STARTER = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_INAPPLICABLE_FW_STARTER
IS_ETH_DEVSTATUS_REBOOTING_FW_RUNTIME = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_REBOOTING_FW_RUNTIME
IS_ETH_DEVSTATUS_REBOOTING_FW_STARTER = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_REBOOTING_FW_STARTER
IS_ETH_DEVSTATUS_REBOOTING_FW_FAILSAFE = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_REBOOTING_FW_FAILSAFE
IS_ETH_DEVSTATUS_RUNTIME_FW_ERR0 = UEYE_ETH_DEVICESTATUS.IS_ETH_DEVSTATUS_RUNTIME_FW_ERR0


class UEYE_ETH_CONTROLSTATUS(_CtypesEnum):
    IS_ETH_CTRLSTATUS_AVAILABLE = 1
    IS_ETH_CTRLSTATUS_ACCESSIBLE1 = 2
    IS_ETH_CTRLSTATUS_ACCESSIBLE2 = 4
    IS_ETH_CTRLSTATUS_PERSISTENT_IP_USED = 16
    IS_ETH_CTRLSTATUS_COMPATIBLE = 32
    IS_ETH_CTRLSTATUS_ADAPTER_ON_DHCP = 64
    IS_ETH_CTRLSTATUS_ADAPTER_SETUP_OK = 128
    IS_ETH_CTRLSTATUS_UNPAIRING_IN_PROGRESS = 256
    IS_ETH_CTRLSTATUS_PAIRING_IN_PROGRESS = 512
    IS_ETH_CTRLSTATUS_PAIRED = 4096
    IS_ETH_CTRLSTATUS_OPENED = 16384
    IS_ETH_CTRLSTATUS_FW_UPLOAD_STARTER = 65536
    IS_ETH_CTRLSTATUS_FW_UPLOAD_RUNTIME = 131072
    IS_ETH_CTRLSTATUS_REBOOTING = 1048576
    IS_ETH_CTRLSTATUS_BOOTBOOST_ENABLED = 16777216
    IS_ETH_CTRLSTATUS_BOOTBOOST_ACTIVE = 33554432
    IS_ETH_CTRLSTATUS_INITIALIZED = 134217728
    IS_ETH_CTRLSTATUS_TO_BE_DELETED = 1073741824
    IS_ETH_CTRLSTATUS_TO_BE_REMOVED = 2147483648


IS_ETH_CTRLSTATUS_AVAILABLE = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_AVAILABLE
IS_ETH_CTRLSTATUS_ACCESSIBLE1 = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_ACCESSIBLE1
IS_ETH_CTRLSTATUS_ACCESSIBLE2 = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_ACCESSIBLE2
IS_ETH_CTRLSTATUS_PERSISTENT_IP_USED = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_PERSISTENT_IP_USED
IS_ETH_CTRLSTATUS_COMPATIBLE = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_COMPATIBLE
IS_ETH_CTRLSTATUS_ADAPTER_ON_DHCP = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_ADAPTER_ON_DHCP
IS_ETH_CTRLSTATUS_ADAPTER_SETUP_OK = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_ADAPTER_SETUP_OK
IS_ETH_CTRLSTATUS_UNPAIRING_IN_PROGRESS = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_UNPAIRING_IN_PROGRESS
IS_ETH_CTRLSTATUS_PAIRING_IN_PROGRESS = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_PAIRING_IN_PROGRESS
IS_ETH_CTRLSTATUS_PAIRED = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_PAIRED
IS_ETH_CTRLSTATUS_OPENED = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_OPENED
IS_ETH_CTRLSTATUS_FW_UPLOAD_STARTER = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_FW_UPLOAD_STARTER
IS_ETH_CTRLSTATUS_FW_UPLOAD_RUNTIME = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_FW_UPLOAD_RUNTIME
IS_ETH_CTRLSTATUS_REBOOTING = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_REBOOTING
IS_ETH_CTRLSTATUS_BOOTBOOST_ENABLED = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_BOOTBOOST_ENABLED
IS_ETH_CTRLSTATUS_BOOTBOOST_ACTIVE = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_BOOTBOOST_ACTIVE
IS_ETH_CTRLSTATUS_INITIALIZED = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_INITIALIZED
IS_ETH_CTRLSTATUS_TO_BE_DELETED = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_TO_BE_DELETED
IS_ETH_CTRLSTATUS_TO_BE_REMOVED = UEYE_ETH_CONTROLSTATUS.IS_ETH_CTRLSTATUS_TO_BE_REMOVED


class UEYE_ETH_PACKETFILTER_SETUP(_CtypesEnum):
    IS_ETH_PCKTFLT_PASSALL = 0
    IS_ETH_PCKTFLT_BLOCKUEGET = 1
    IS_ETH_PCKTFLT_BLOCKALL = 2


IS_ETH_PCKTFLT_PASSALL = UEYE_ETH_PACKETFILTER_SETUP.IS_ETH_PCKTFLT_PASSALL
IS_ETH_PCKTFLT_BLOCKUEGET = UEYE_ETH_PACKETFILTER_SETUP.IS_ETH_PCKTFLT_BLOCKUEGET
IS_ETH_PCKTFLT_BLOCKALL = UEYE_ETH_PACKETFILTER_SETUP.IS_ETH_PCKTFLT_BLOCKALL


class UEYE_ETH_LINKSPEED_SETUP(_CtypesEnum):
    IS_ETH_LINKSPEED_100MB = 100
    IS_ETH_LINKSPEED_1000MB = 1000


IS_ETH_LINKSPEED_100MB = UEYE_ETH_LINKSPEED_SETUP.IS_ETH_LINKSPEED_100MB
IS_ETH_LINKSPEED_1000MB = UEYE_ETH_LINKSPEED_SETUP.IS_ETH_LINKSPEED_1000MB


class IPCONFIG_CAPABILITY_FLAGS(_CtypesEnum):
    IPCONFIG_CAP_PERSISTENT_IP_SUPPORTED = 1
    IPCONFIG_CAP_AUTOCONFIG_IP_SUPPORTED = 4


IPCONFIG_CAP_PERSISTENT_IP_SUPPORTED = IPCONFIG_CAPABILITY_FLAGS.IPCONFIG_CAP_PERSISTENT_IP_SUPPORTED
IPCONFIG_CAP_AUTOCONFIG_IP_SUPPORTED = IPCONFIG_CAPABILITY_FLAGS.IPCONFIG_CAP_AUTOCONFIG_IP_SUPPORTED


class IPCONFIG_CMD(_CtypesEnum):
    IPCONFIG_CMD_QUERY_CAPABILITIES = 0
    IPCONFIG_CMD_SET_PERSISTENT_IP = 16842752
    IPCONFIG_CMD_SET_AUTOCONFIG_IP = 17039360
    IPCONFIG_CMD_SET_AUTOCONFIG_IP_BYDEVICE = 17039616
    IPCONFIG_CMD_RESERVED1 = 17301504
    IPCONFIG_CMD_GET_PERSISTENT_IP = 33619968
    IPCONFIG_CMD_GET_AUTOCONFIG_IP = 33816576
    IPCONFIG_CMD_GET_AUTOCONFIG_IP_BYDEVICE = 33816832


IPCONFIG_CMD_QUERY_CAPABILITIES = IPCONFIG_CMD.IPCONFIG_CMD_QUERY_CAPABILITIES
IPCONFIG_CMD_SET_PERSISTENT_IP = IPCONFIG_CMD.IPCONFIG_CMD_SET_PERSISTENT_IP
IPCONFIG_CMD_SET_AUTOCONFIG_IP = IPCONFIG_CMD.IPCONFIG_CMD_SET_AUTOCONFIG_IP
IPCONFIG_CMD_SET_AUTOCONFIG_IP_BYDEVICE = IPCONFIG_CMD.IPCONFIG_CMD_SET_AUTOCONFIG_IP_BYDEVICE
IPCONFIG_CMD_RESERVED1 = IPCONFIG_CMD.IPCONFIG_CMD_RESERVED1
IPCONFIG_CMD_GET_PERSISTENT_IP = IPCONFIG_CMD.IPCONFIG_CMD_GET_PERSISTENT_IP
IPCONFIG_CMD_GET_AUTOCONFIG_IP = IPCONFIG_CMD.IPCONFIG_CMD_GET_AUTOCONFIG_IP
IPCONFIG_CMD_GET_AUTOCONFIG_IP_BYDEVICE = IPCONFIG_CMD.IPCONFIG_CMD_GET_AUTOCONFIG_IP_BYDEVICE


class CONFIGURATION_SEL(_CtypesEnum):
    IS_CONFIG_CPU_IDLE_STATES_BIT_AC_VALUE = 1
    IS_CONFIG_CPU_IDLE_STATES_BIT_DC_VALUE = 2
    IS_CONFIG_IPO_NOT_ALLOWED = 0
    IS_CONFIG_IPO_ALLOWED = 1
    IS_CONFIG_OPEN_MP_DISABLE = 0
    IS_CONFIG_OPEN_MP_ENABLE = 1
    IS_CONFIG_INITIAL_PARAMETERSET_NONE = 0
    IS_CONFIG_INITIAL_PARAMETERSET_1 = 1
    IS_CONFIG_INITIAL_PARAMETERSET_2 = 2
    IS_CONFIG_ETH_CONFIGURATION_MODE_OFF = 0
    IS_CONFIG_ETH_CONFIGURATION_MODE_ON = 1
    IS_CONFIG_TRUSTED_PAIRING_OFF = 0
    IS_CONFIG_TRUSTED_PAIRING_ON = 1
    IS_CONFIG_IMAGE_MEMORY_COMPATIBILITY_MODE_OFF = 0
    IS_CONFIG_IMAGE_MEMORY_COMPATIBILITY_MODE_ON = 1


IS_CONFIG_CPU_IDLE_STATES_BIT_AC_VALUE = CONFIGURATION_SEL.IS_CONFIG_CPU_IDLE_STATES_BIT_AC_VALUE
IS_CONFIG_CPU_IDLE_STATES_BIT_DC_VALUE = CONFIGURATION_SEL.IS_CONFIG_CPU_IDLE_STATES_BIT_DC_VALUE
IS_CONFIG_IPO_NOT_ALLOWED = CONFIGURATION_SEL.IS_CONFIG_IPO_NOT_ALLOWED
IS_CONFIG_IPO_ALLOWED = CONFIGURATION_SEL.IS_CONFIG_IPO_ALLOWED
IS_CONFIG_OPEN_MP_DISABLE = CONFIGURATION_SEL.IS_CONFIG_OPEN_MP_DISABLE
IS_CONFIG_OPEN_MP_ENABLE = CONFIGURATION_SEL.IS_CONFIG_OPEN_MP_ENABLE
IS_CONFIG_INITIAL_PARAMETERSET_NONE = CONFIGURATION_SEL.IS_CONFIG_INITIAL_PARAMETERSET_NONE
IS_CONFIG_INITIAL_PARAMETERSET_1 = CONFIGURATION_SEL.IS_CONFIG_INITIAL_PARAMETERSET_1
IS_CONFIG_INITIAL_PARAMETERSET_2 = CONFIGURATION_SEL.IS_CONFIG_INITIAL_PARAMETERSET_2
IS_CONFIG_ETH_CONFIGURATION_MODE_OFF = CONFIGURATION_SEL.IS_CONFIG_ETH_CONFIGURATION_MODE_OFF
IS_CONFIG_ETH_CONFIGURATION_MODE_ON = CONFIGURATION_SEL.IS_CONFIG_ETH_CONFIGURATION_MODE_ON
IS_CONFIG_TRUSTED_PAIRING_OFF = CONFIGURATION_SEL.IS_CONFIG_TRUSTED_PAIRING_OFF
IS_CONFIG_TRUSTED_PAIRING_ON = CONFIGURATION_SEL.IS_CONFIG_TRUSTED_PAIRING_ON
IS_CONFIG_IMAGE_MEMORY_COMPATIBILITY_MODE_OFF = CONFIGURATION_SEL.IS_CONFIG_IMAGE_MEMORY_COMPATIBILITY_MODE_OFF
IS_CONFIG_IMAGE_MEMORY_COMPATIBILITY_MODE_ON = CONFIGURATION_SEL.IS_CONFIG_IMAGE_MEMORY_COMPATIBILITY_MODE_ON


class CONFIGURATION_CMD(_CtypesEnum):
    IS_CONFIG_CMD_GET_CAPABILITIES = 1
    IS_CONFIG_CPU_IDLE_STATES_CMD_GET_ENABLE = 2
    IS_CONFIG_CPU_IDLE_STATES_CMD_SET_DISABLE_ON_OPEN = 4
    IS_CONFIG_CPU_IDLE_STATES_CMD_GET_DISABLE_ON_OPEN = 5
    IS_CONFIG_OPEN_MP_CMD_GET_ENABLE = 6
    IS_CONFIG_OPEN_MP_CMD_SET_ENABLE = 7
    IS_CONFIG_OPEN_MP_CMD_GET_ENABLE_DEFAULT = 8
    IS_CONFIG_INITIAL_PARAMETERSET_CMD_SET = 9
    IS_CONFIG_INITIAL_PARAMETERSET_CMD_GET = 10
    IS_CONFIG_ETH_CONFIGURATION_MODE_CMD_SET_ENABLE = 11
    IS_CONFIG_ETH_CONFIGURATION_MODE_CMD_GET_ENABLE = 12
    IS_CONFIG_IPO_CMD_GET_ALLOWED = 13
    IS_CONFIG_IPO_CMD_SET_ALLOWED = 14
    IS_CONFIG_CMD_TRUSTED_PAIRING_SET = 15
    IS_CONFIG_CMD_TRUSTED_PAIRING_GET = 16
    IS_CONFIG_CMD_TRUSTED_PAIRING_GET_DEFAULT = 17
    IS_CONFIG_CMD_RESERVED_1 = 18
    IS_CONFIG_CMD_SET_IMAGE_MEMORY_COMPATIBILIY_MODE = 19
    IS_CONFIG_CMD_GET_IMAGE_MEMORY_COMPATIBILIY_MODE = 20
    IS_CONFIG_CMD_GET_IMAGE_MEMORY_COMPATIBILIY_MODE_DEFAULT = 21


IS_CONFIG_CMD_GET_CAPABILITIES = CONFIGURATION_CMD.IS_CONFIG_CMD_GET_CAPABILITIES
IS_CONFIG_CPU_IDLE_STATES_CMD_GET_ENABLE = CONFIGURATION_CMD.IS_CONFIG_CPU_IDLE_STATES_CMD_GET_ENABLE
IS_CONFIG_CPU_IDLE_STATES_CMD_SET_DISABLE_ON_OPEN = CONFIGURATION_CMD.IS_CONFIG_CPU_IDLE_STATES_CMD_SET_DISABLE_ON_OPEN
IS_CONFIG_CPU_IDLE_STATES_CMD_GET_DISABLE_ON_OPEN = CONFIGURATION_CMD.IS_CONFIG_CPU_IDLE_STATES_CMD_GET_DISABLE_ON_OPEN
IS_CONFIG_OPEN_MP_CMD_GET_ENABLE = CONFIGURATION_CMD.IS_CONFIG_OPEN_MP_CMD_GET_ENABLE
IS_CONFIG_OPEN_MP_CMD_SET_ENABLE = CONFIGURATION_CMD.IS_CONFIG_OPEN_MP_CMD_SET_ENABLE
IS_CONFIG_OPEN_MP_CMD_GET_ENABLE_DEFAULT = CONFIGURATION_CMD.IS_CONFIG_OPEN_MP_CMD_GET_ENABLE_DEFAULT
IS_CONFIG_INITIAL_PARAMETERSET_CMD_SET = CONFIGURATION_CMD.IS_CONFIG_INITIAL_PARAMETERSET_CMD_SET
IS_CONFIG_INITIAL_PARAMETERSET_CMD_GET = CONFIGURATION_CMD.IS_CONFIG_INITIAL_PARAMETERSET_CMD_GET
IS_CONFIG_ETH_CONFIGURATION_MODE_CMD_SET_ENABLE = CONFIGURATION_CMD.IS_CONFIG_ETH_CONFIGURATION_MODE_CMD_SET_ENABLE
IS_CONFIG_ETH_CONFIGURATION_MODE_CMD_GET_ENABLE = CONFIGURATION_CMD.IS_CONFIG_ETH_CONFIGURATION_MODE_CMD_GET_ENABLE
IS_CONFIG_IPO_CMD_GET_ALLOWED = CONFIGURATION_CMD.IS_CONFIG_IPO_CMD_GET_ALLOWED
IS_CONFIG_IPO_CMD_SET_ALLOWED = CONFIGURATION_CMD.IS_CONFIG_IPO_CMD_SET_ALLOWED
IS_CONFIG_CMD_TRUSTED_PAIRING_SET = CONFIGURATION_CMD.IS_CONFIG_CMD_TRUSTED_PAIRING_SET
IS_CONFIG_CMD_TRUSTED_PAIRING_GET = CONFIGURATION_CMD.IS_CONFIG_CMD_TRUSTED_PAIRING_GET
IS_CONFIG_CMD_TRUSTED_PAIRING_GET_DEFAULT = CONFIGURATION_CMD.IS_CONFIG_CMD_TRUSTED_PAIRING_GET_DEFAULT
IS_CONFIG_CMD_RESERVED_1 = CONFIGURATION_CMD.IS_CONFIG_CMD_RESERVED_1
IS_CONFIG_CMD_SET_IMAGE_MEMORY_COMPATIBILIY_MODE = CONFIGURATION_CMD.IS_CONFIG_CMD_SET_IMAGE_MEMORY_COMPATIBILIY_MODE
IS_CONFIG_CMD_GET_IMAGE_MEMORY_COMPATIBILIY_MODE = CONFIGURATION_CMD.IS_CONFIG_CMD_GET_IMAGE_MEMORY_COMPATIBILIY_MODE
IS_CONFIG_CMD_GET_IMAGE_MEMORY_COMPATIBILIY_MODE_DEFAULT = CONFIGURATION_CMD.IS_CONFIG_CMD_GET_IMAGE_MEMORY_COMPATIBILIY_MODE_DEFAULT


class CONFIGURATION_CAPS(_CtypesEnum):
    IS_CONFIG_CPU_IDLE_STATES_CAP_SUPPORTED = 1
    IS_CONFIG_OPEN_MP_CAP_SUPPORTED = 2
    IS_CONFIG_INITIAL_PARAMETERSET_CAP_SUPPORTED = 4
    IS_CONFIG_IPO_CAP_SUPPORTED = 8
    IS_CONFIG_TRUSTED_PAIRING_CAP_SUPPORTED = 16


IS_CONFIG_CPU_IDLE_STATES_CAP_SUPPORTED = CONFIGURATION_CAPS.IS_CONFIG_CPU_IDLE_STATES_CAP_SUPPORTED
IS_CONFIG_OPEN_MP_CAP_SUPPORTED = CONFIGURATION_CAPS.IS_CONFIG_OPEN_MP_CAP_SUPPORTED
IS_CONFIG_INITIAL_PARAMETERSET_CAP_SUPPORTED = CONFIGURATION_CAPS.IS_CONFIG_INITIAL_PARAMETERSET_CAP_SUPPORTED
IS_CONFIG_IPO_CAP_SUPPORTED = CONFIGURATION_CAPS.IS_CONFIG_IPO_CAP_SUPPORTED
IS_CONFIG_TRUSTED_PAIRING_CAP_SUPPORTED = CONFIGURATION_CAPS.IS_CONFIG_TRUSTED_PAIRING_CAP_SUPPORTED


class IO_CMD(_CtypesEnum):
    IS_IO_CMD_GPIOS_GET_SUPPORTED = 1
    IS_IO_CMD_GPIOS_GET_SUPPORTED_INPUTS = 2
    IS_IO_CMD_GPIOS_GET_SUPPORTED_OUTPUTS = 3
    IS_IO_CMD_GPIOS_GET_DIRECTION = 4
    IS_IO_CMD_GPIOS_SET_DIRECTION = 5
    IS_IO_CMD_GPIOS_GET_STATE = 6
    IS_IO_CMD_GPIOS_SET_STATE = 7
    IS_IO_CMD_LED_GET_STATE = 8
    IS_IO_CMD_LED_SET_STATE = 9
    IS_IO_CMD_LED_TOGGLE_STATE = 10
    IS_IO_CMD_FLASH_GET_GLOBAL_PARAMS = 11
    IS_IO_CMD_FLASH_APPLY_GLOBAL_PARAMS = 12
    IS_IO_CMD_FLASH_GET_SUPPORTED_GPIOS = 13
    IS_IO_CMD_FLASH_GET_PARAMS_MIN = 14
    IS_IO_CMD_FLASH_GET_PARAMS_MAX = 15
    IS_IO_CMD_FLASH_GET_PARAMS_INC = 16
    IS_IO_CMD_FLASH_GET_PARAMS = 17
    IS_IO_CMD_FLASH_SET_PARAMS = 18
    IS_IO_CMD_FLASH_GET_MODE = 19
    IS_IO_CMD_FLASH_SET_MODE = 20
    IS_IO_CMD_PWM_GET_SUPPORTED_GPIOS = 21
    IS_IO_CMD_PWM_GET_PARAMS_MIN = 22
    IS_IO_CMD_PWM_GET_PARAMS_MAX = 23
    IS_IO_CMD_PWM_GET_PARAMS_INC = 24
    IS_IO_CMD_PWM_GET_PARAMS = 25
    IS_IO_CMD_PWM_SET_PARAMS = 26
    IS_IO_CMD_PWM_GET_MODE = 27
    IS_IO_CMD_PWM_SET_MODE = 28
    IS_IO_CMD_GPIOS_GET_CONFIGURATION = 29
    IS_IO_CMD_GPIOS_SET_CONFIGURATION = 30
    IS_IO_CMD_FLASH_GET_GPIO_PARAMS_MIN = 31
    IS_IO_CMD_FLASH_SET_GPIO_PARAMS = 32
    IS_IO_CMD_FLASH_GET_AUTO_FREERUN_DEFAULT = 33
    IS_IO_CMD_FLASH_GET_AUTO_FREERUN = 34
    IS_IO_CMD_FLASH_SET_AUTO_FREERUN = 35


IS_IO_CMD_GPIOS_GET_SUPPORTED = IO_CMD.IS_IO_CMD_GPIOS_GET_SUPPORTED
IS_IO_CMD_GPIOS_GET_SUPPORTED_INPUTS = IO_CMD.IS_IO_CMD_GPIOS_GET_SUPPORTED_INPUTS
IS_IO_CMD_GPIOS_GET_SUPPORTED_OUTPUTS = IO_CMD.IS_IO_CMD_GPIOS_GET_SUPPORTED_OUTPUTS
IS_IO_CMD_GPIOS_GET_DIRECTION = IO_CMD.IS_IO_CMD_GPIOS_GET_DIRECTION
IS_IO_CMD_GPIOS_SET_DIRECTION = IO_CMD.IS_IO_CMD_GPIOS_SET_DIRECTION
IS_IO_CMD_GPIOS_GET_STATE = IO_CMD.IS_IO_CMD_GPIOS_GET_STATE
IS_IO_CMD_GPIOS_SET_STATE = IO_CMD.IS_IO_CMD_GPIOS_SET_STATE
IS_IO_CMD_LED_GET_STATE = IO_CMD.IS_IO_CMD_LED_GET_STATE
IS_IO_CMD_LED_SET_STATE = IO_CMD.IS_IO_CMD_LED_SET_STATE
IS_IO_CMD_LED_TOGGLE_STATE = IO_CMD.IS_IO_CMD_LED_TOGGLE_STATE
IS_IO_CMD_FLASH_GET_GLOBAL_PARAMS = IO_CMD.IS_IO_CMD_FLASH_GET_GLOBAL_PARAMS
IS_IO_CMD_FLASH_APPLY_GLOBAL_PARAMS = IO_CMD.IS_IO_CMD_FLASH_APPLY_GLOBAL_PARAMS
IS_IO_CMD_FLASH_GET_SUPPORTED_GPIOS = IO_CMD.IS_IO_CMD_FLASH_GET_SUPPORTED_GPIOS
IS_IO_CMD_FLASH_GET_PARAMS_MIN = IO_CMD.IS_IO_CMD_FLASH_GET_PARAMS_MIN
IS_IO_CMD_FLASH_GET_PARAMS_MAX = IO_CMD.IS_IO_CMD_FLASH_GET_PARAMS_MAX
IS_IO_CMD_FLASH_GET_PARAMS_INC = IO_CMD.IS_IO_CMD_FLASH_GET_PARAMS_INC
IS_IO_CMD_FLASH_GET_PARAMS = IO_CMD.IS_IO_CMD_FLASH_GET_PARAMS
IS_IO_CMD_FLASH_SET_PARAMS = IO_CMD.IS_IO_CMD_FLASH_SET_PARAMS
IS_IO_CMD_FLASH_GET_MODE = IO_CMD.IS_IO_CMD_FLASH_GET_MODE
IS_IO_CMD_FLASH_SET_MODE = IO_CMD.IS_IO_CMD_FLASH_SET_MODE
IS_IO_CMD_PWM_GET_SUPPORTED_GPIOS = IO_CMD.IS_IO_CMD_PWM_GET_SUPPORTED_GPIOS
IS_IO_CMD_PWM_GET_PARAMS_MIN = IO_CMD.IS_IO_CMD_PWM_GET_PARAMS_MIN
IS_IO_CMD_PWM_GET_PARAMS_MAX = IO_CMD.IS_IO_CMD_PWM_GET_PARAMS_MAX
IS_IO_CMD_PWM_GET_PARAMS_INC = IO_CMD.IS_IO_CMD_PWM_GET_PARAMS_INC
IS_IO_CMD_PWM_GET_PARAMS = IO_CMD.IS_IO_CMD_PWM_GET_PARAMS
IS_IO_CMD_PWM_SET_PARAMS = IO_CMD.IS_IO_CMD_PWM_SET_PARAMS
IS_IO_CMD_PWM_GET_MODE = IO_CMD.IS_IO_CMD_PWM_GET_MODE
IS_IO_CMD_PWM_SET_MODE = IO_CMD.IS_IO_CMD_PWM_SET_MODE
IS_IO_CMD_GPIOS_GET_CONFIGURATION = IO_CMD.IS_IO_CMD_GPIOS_GET_CONFIGURATION
IS_IO_CMD_GPIOS_SET_CONFIGURATION = IO_CMD.IS_IO_CMD_GPIOS_SET_CONFIGURATION
IS_IO_CMD_FLASH_GET_GPIO_PARAMS_MIN = IO_CMD.IS_IO_CMD_FLASH_GET_GPIO_PARAMS_MIN
IS_IO_CMD_FLASH_SET_GPIO_PARAMS = IO_CMD.IS_IO_CMD_FLASH_SET_GPIO_PARAMS
IS_IO_CMD_FLASH_GET_AUTO_FREERUN_DEFAULT = IO_CMD.IS_IO_CMD_FLASH_GET_AUTO_FREERUN_DEFAULT
IS_IO_CMD_FLASH_GET_AUTO_FREERUN = IO_CMD.IS_IO_CMD_FLASH_GET_AUTO_FREERUN
IS_IO_CMD_FLASH_SET_AUTO_FREERUN = IO_CMD.IS_IO_CMD_FLASH_SET_AUTO_FREERUN


class AUTOPARAMETER_CMD(_CtypesEnum):
    IS_AWB_CMD_GET_SUPPORTED_TYPES = 1
    IS_AWB_CMD_GET_TYPE = 2
    IS_AWB_CMD_SET_TYPE = 3
    IS_AWB_CMD_GET_ENABLE = 4
    IS_AWB_CMD_SET_ENABLE = 5
    IS_AWB_CMD_GET_SUPPORTED_RGB_COLOR_MODELS = 6
    IS_AWB_CMD_GET_RGB_COLOR_MODEL = 7
    IS_AWB_CMD_SET_RGB_COLOR_MODEL = 8
    IS_AES_CMD_GET_SUPPORTED_TYPES = 9
    IS_AES_CMD_SET_ENABLE = 10
    IS_AES_CMD_GET_ENABLE = 11
    IS_AES_CMD_SET_TYPE = 12
    IS_AES_CMD_GET_TYPE = 13
    IS_AES_CMD_SET_CONFIGURATION = 14
    IS_AES_CMD_GET_CONFIGURATION = 15
    IS_AES_CMD_GET_CONFIGURATION_DEFAULT = 16
    IS_AES_CMD_GET_CONFIGURATION_RANGE = 17


IS_AWB_CMD_GET_SUPPORTED_TYPES = AUTOPARAMETER_CMD.IS_AWB_CMD_GET_SUPPORTED_TYPES
IS_AWB_CMD_GET_TYPE = AUTOPARAMETER_CMD.IS_AWB_CMD_GET_TYPE
IS_AWB_CMD_SET_TYPE = AUTOPARAMETER_CMD.IS_AWB_CMD_SET_TYPE
IS_AWB_CMD_GET_ENABLE = AUTOPARAMETER_CMD.IS_AWB_CMD_GET_ENABLE
IS_AWB_CMD_SET_ENABLE = AUTOPARAMETER_CMD.IS_AWB_CMD_SET_ENABLE
IS_AWB_CMD_GET_SUPPORTED_RGB_COLOR_MODELS = AUTOPARAMETER_CMD.IS_AWB_CMD_GET_SUPPORTED_RGB_COLOR_MODELS
IS_AWB_CMD_GET_RGB_COLOR_MODEL = AUTOPARAMETER_CMD.IS_AWB_CMD_GET_RGB_COLOR_MODEL
IS_AWB_CMD_SET_RGB_COLOR_MODEL = AUTOPARAMETER_CMD.IS_AWB_CMD_SET_RGB_COLOR_MODEL
IS_AES_CMD_GET_SUPPORTED_TYPES = AUTOPARAMETER_CMD.IS_AES_CMD_GET_SUPPORTED_TYPES
IS_AES_CMD_SET_ENABLE = AUTOPARAMETER_CMD.IS_AES_CMD_SET_ENABLE
IS_AES_CMD_GET_ENABLE = AUTOPARAMETER_CMD.IS_AES_CMD_GET_ENABLE
IS_AES_CMD_SET_TYPE = AUTOPARAMETER_CMD.IS_AES_CMD_SET_TYPE
IS_AES_CMD_GET_TYPE = AUTOPARAMETER_CMD.IS_AES_CMD_GET_TYPE
IS_AES_CMD_SET_CONFIGURATION = AUTOPARAMETER_CMD.IS_AES_CMD_SET_CONFIGURATION
IS_AES_CMD_GET_CONFIGURATION = AUTOPARAMETER_CMD.IS_AES_CMD_GET_CONFIGURATION
IS_AES_CMD_GET_CONFIGURATION_DEFAULT = AUTOPARAMETER_CMD.IS_AES_CMD_GET_CONFIGURATION_DEFAULT
IS_AES_CMD_GET_CONFIGURATION_RANGE = AUTOPARAMETER_CMD.IS_AES_CMD_GET_CONFIGURATION_RANGE


class AES_MODE(_CtypesEnum):
    IS_AES_MODE_PEAK = 1
    IS_AES_MODE_MEAN = 2


IS_AES_MODE_PEAK = AES_MODE.IS_AES_MODE_PEAK
IS_AES_MODE_MEAN = AES_MODE.IS_AES_MODE_MEAN


class AES_CHANNEL(_CtypesEnum):
    IS_AES_CHANNEL_MONO = 1
    IS_AES_CHANNEL_RED = 1
    IS_AES_CHANNEL_GREEN = 2
    IS_AES_CHANNEL_BLUE = 4


IS_AES_CHANNEL_MONO = AES_CHANNEL.IS_AES_CHANNEL_MONO
IS_AES_CHANNEL_RED = AES_CHANNEL.IS_AES_CHANNEL_RED
IS_AES_CHANNEL_GREEN = AES_CHANNEL.IS_AES_CHANNEL_GREEN
IS_AES_CHANNEL_BLUE = AES_CHANNEL.IS_AES_CHANNEL_BLUE


class AES_PEAK_MODE(_CtypesEnum):
    IS_AES_PEAK_MODE_SELECTED_CHANNELS = 0
    IS_AES_PEAK_MODE_LEADING_CHANNEL = 1
    IS_AES_PEAK_MODE_ACCUMULATED_CHANNELS = 2


IS_AES_PEAK_MODE_SELECTED_CHANNELS = AES_PEAK_MODE.IS_AES_PEAK_MODE_SELECTED_CHANNELS
IS_AES_PEAK_MODE_LEADING_CHANNEL = AES_PEAK_MODE.IS_AES_PEAK_MODE_LEADING_CHANNEL
IS_AES_PEAK_MODE_ACCUMULATED_CHANNELS = AES_PEAK_MODE.IS_AES_PEAK_MODE_ACCUMULATED_CHANNELS


class AES_GRANULARITY(_CtypesEnum):
    IS_AES_GRANULARITY_PER_100 = 0
    IS_AES_GRANULARITY_PER_1000 = 1
    IS_AES_GRANULARITY_PER_10000 = 2


IS_AES_GRANULARITY_PER_100 = AES_GRANULARITY.IS_AES_GRANULARITY_PER_100
IS_AES_GRANULARITY_PER_1000 = AES_GRANULARITY.IS_AES_GRANULARITY_PER_1000
IS_AES_GRANULARITY_PER_10000 = AES_GRANULARITY.IS_AES_GRANULARITY_PER_10000


class CONVERT_CMD(_CtypesEnum):
    IS_CONVERT_CMD_APPLY_PARAMS_AND_CONVERT_BUFFER = 1


IS_CONVERT_CMD_APPLY_PARAMS_AND_CONVERT_BUFFER = CONVERT_CMD.IS_CONVERT_CMD_APPLY_PARAMS_AND_CONVERT_BUFFER


class PARAMETERSET_CMD(_CtypesEnum):
    IS_PARAMETERSET_CMD_LOAD_EEPROM = 1
    IS_PARAMETERSET_CMD_LOAD_FILE = 2
    IS_PARAMETERSET_CMD_SAVE_EEPROM = 3
    IS_PARAMETERSET_CMD_SAVE_FILE = 4
    IS_PARAMETERSET_CMD_GET_NUMBER_SUPPORTED = 5
    IS_PARAMETERSET_CMD_GET_HW_PARAMETERSET_AVAILABLE = 6
    IS_PARAMETERSET_CMD_ERASE_HW_PARAMETERSET = 7


IS_PARAMETERSET_CMD_LOAD_EEPROM = PARAMETERSET_CMD.IS_PARAMETERSET_CMD_LOAD_EEPROM
IS_PARAMETERSET_CMD_LOAD_FILE = PARAMETERSET_CMD.IS_PARAMETERSET_CMD_LOAD_FILE
IS_PARAMETERSET_CMD_SAVE_EEPROM = PARAMETERSET_CMD.IS_PARAMETERSET_CMD_SAVE_EEPROM
IS_PARAMETERSET_CMD_SAVE_FILE = PARAMETERSET_CMD.IS_PARAMETERSET_CMD_SAVE_FILE
IS_PARAMETERSET_CMD_GET_NUMBER_SUPPORTED = PARAMETERSET_CMD.IS_PARAMETERSET_CMD_GET_NUMBER_SUPPORTED
IS_PARAMETERSET_CMD_GET_HW_PARAMETERSET_AVAILABLE = PARAMETERSET_CMD.IS_PARAMETERSET_CMD_GET_HW_PARAMETERSET_AVAILABLE
IS_PARAMETERSET_CMD_ERASE_HW_PARAMETERSET = PARAMETERSET_CMD.IS_PARAMETERSET_CMD_ERASE_HW_PARAMETERSET


class EDGE_ENHANCEMENT_CMD(_CtypesEnum):
    IS_EDGE_ENHANCEMENT_CMD_GET_RANGE = 1
    IS_EDGE_ENHANCEMENT_CMD_GET_DEFAULT = 2
    IS_EDGE_ENHANCEMENT_CMD_GET = 3
    IS_EDGE_ENHANCEMENT_CMD_SET = 4


IS_EDGE_ENHANCEMENT_CMD_GET_RANGE = EDGE_ENHANCEMENT_CMD.IS_EDGE_ENHANCEMENT_CMD_GET_RANGE
IS_EDGE_ENHANCEMENT_CMD_GET_DEFAULT = EDGE_ENHANCEMENT_CMD.IS_EDGE_ENHANCEMENT_CMD_GET_DEFAULT
IS_EDGE_ENHANCEMENT_CMD_GET = EDGE_ENHANCEMENT_CMD.IS_EDGE_ENHANCEMENT_CMD_GET
IS_EDGE_ENHANCEMENT_CMD_SET = EDGE_ENHANCEMENT_CMD.IS_EDGE_ENHANCEMENT_CMD_SET


class PIXELCLOCK_CMD(_CtypesEnum):
    IS_PIXELCLOCK_CMD_GET_NUMBER = 1
    IS_PIXELCLOCK_CMD_GET_LIST = 2
    IS_PIXELCLOCK_CMD_GET_RANGE = 3
    IS_PIXELCLOCK_CMD_GET_DEFAULT = 4
    IS_PIXELCLOCK_CMD_GET = 5
    IS_PIXELCLOCK_CMD_SET = 6


IS_PIXELCLOCK_CMD_GET_NUMBER = PIXELCLOCK_CMD.IS_PIXELCLOCK_CMD_GET_NUMBER
IS_PIXELCLOCK_CMD_GET_LIST = PIXELCLOCK_CMD.IS_PIXELCLOCK_CMD_GET_LIST
IS_PIXELCLOCK_CMD_GET_RANGE = PIXELCLOCK_CMD.IS_PIXELCLOCK_CMD_GET_RANGE
IS_PIXELCLOCK_CMD_GET_DEFAULT = PIXELCLOCK_CMD.IS_PIXELCLOCK_CMD_GET_DEFAULT
IS_PIXELCLOCK_CMD_GET = PIXELCLOCK_CMD.IS_PIXELCLOCK_CMD_GET
IS_PIXELCLOCK_CMD_SET = PIXELCLOCK_CMD.IS_PIXELCLOCK_CMD_SET


class IMAGE_FILE_CMD(_CtypesEnum):
    IS_IMAGE_FILE_CMD_LOAD = 1
    IS_IMAGE_FILE_CMD_SAVE = 2


IS_IMAGE_FILE_CMD_LOAD = IMAGE_FILE_CMD.IS_IMAGE_FILE_CMD_LOAD
IS_IMAGE_FILE_CMD_SAVE = IMAGE_FILE_CMD.IS_IMAGE_FILE_CMD_SAVE


class BLACKLEVEL_MODES(_CtypesEnum):
    IS_AUTO_BLACKLEVEL_OFF = 0
    IS_AUTO_BLACKLEVEL_ON = 1


IS_AUTO_BLACKLEVEL_OFF = BLACKLEVEL_MODES.IS_AUTO_BLACKLEVEL_OFF
IS_AUTO_BLACKLEVEL_ON = BLACKLEVEL_MODES.IS_AUTO_BLACKLEVEL_ON


class BLACKLEVEL_CAPS(_CtypesEnum):
    IS_BLACKLEVEL_CAP_SET_AUTO_BLACKLEVEL = 1
    IS_BLACKLEVEL_CAP_SET_OFFSET = 2


IS_BLACKLEVEL_CAP_SET_AUTO_BLACKLEVEL = BLACKLEVEL_CAPS.IS_BLACKLEVEL_CAP_SET_AUTO_BLACKLEVEL
IS_BLACKLEVEL_CAP_SET_OFFSET = BLACKLEVEL_CAPS.IS_BLACKLEVEL_CAP_SET_OFFSET


class BLACKLEVEL_CMD(_CtypesEnum):
    IS_BLACKLEVEL_CMD_GET_CAPS = 1
    IS_BLACKLEVEL_CMD_GET_MODE_DEFAULT = 2
    IS_BLACKLEVEL_CMD_GET_MODE = 3
    IS_BLACKLEVEL_CMD_SET_MODE = 4
    IS_BLACKLEVEL_CMD_GET_OFFSET_DEFAULT = 5
    IS_BLACKLEVEL_CMD_GET_OFFSET_RANGE = 6
    IS_BLACKLEVEL_CMD_GET_OFFSET = 7
    IS_BLACKLEVEL_CMD_SET_OFFSET = 8


IS_BLACKLEVEL_CMD_GET_CAPS = BLACKLEVEL_CMD.IS_BLACKLEVEL_CMD_GET_CAPS
IS_BLACKLEVEL_CMD_GET_MODE_DEFAULT = BLACKLEVEL_CMD.IS_BLACKLEVEL_CMD_GET_MODE_DEFAULT
IS_BLACKLEVEL_CMD_GET_MODE = BLACKLEVEL_CMD.IS_BLACKLEVEL_CMD_GET_MODE
IS_BLACKLEVEL_CMD_SET_MODE = BLACKLEVEL_CMD.IS_BLACKLEVEL_CMD_SET_MODE
IS_BLACKLEVEL_CMD_GET_OFFSET_DEFAULT = BLACKLEVEL_CMD.IS_BLACKLEVEL_CMD_GET_OFFSET_DEFAULT
IS_BLACKLEVEL_CMD_GET_OFFSET_RANGE = BLACKLEVEL_CMD.IS_BLACKLEVEL_CMD_GET_OFFSET_RANGE
IS_BLACKLEVEL_CMD_GET_OFFSET = BLACKLEVEL_CMD.IS_BLACKLEVEL_CMD_GET_OFFSET
IS_BLACKLEVEL_CMD_SET_OFFSET = BLACKLEVEL_CMD.IS_BLACKLEVEL_CMD_SET_OFFSET


class IMGBUF_CMD(_CtypesEnum):
    IS_IMGBUF_DEVMEM_CMD_GET_AVAILABLE_ITERATIONS = 1
    IS_IMGBUF_DEVMEM_CMD_GET_ITERATION_INFO = 2
    IS_IMGBUF_DEVMEM_CMD_TRANSFER_IMAGE = 3
    IS_IMGBUF_DEVMEM_CMD_RELEASE_ITERATIONS = 4


IS_IMGBUF_DEVMEM_CMD_GET_AVAILABLE_ITERATIONS = IMGBUF_CMD.IS_IMGBUF_DEVMEM_CMD_GET_AVAILABLE_ITERATIONS
IS_IMGBUF_DEVMEM_CMD_GET_ITERATION_INFO = IMGBUF_CMD.IS_IMGBUF_DEVMEM_CMD_GET_ITERATION_INFO
IS_IMGBUF_DEVMEM_CMD_TRANSFER_IMAGE = IMGBUF_CMD.IS_IMGBUF_DEVMEM_CMD_TRANSFER_IMAGE
IS_IMGBUF_DEVMEM_CMD_RELEASE_ITERATIONS = IMGBUF_CMD.IS_IMGBUF_DEVMEM_CMD_RELEASE_ITERATIONS


class MEASURE_CMD(_CtypesEnum):
    IS_MEASURE_CMD_SHARPNESS_AOI_SET = 1
    IS_MEASURE_CMD_SHARPNESS_AOI_INQUIRE = 2
    IS_MEASURE_CMD_SHARPNESS_AOI_SET_PRESET = 3


IS_MEASURE_CMD_SHARPNESS_AOI_SET = MEASURE_CMD.IS_MEASURE_CMD_SHARPNESS_AOI_SET
IS_MEASURE_CMD_SHARPNESS_AOI_INQUIRE = MEASURE_CMD.IS_MEASURE_CMD_SHARPNESS_AOI_INQUIRE
IS_MEASURE_CMD_SHARPNESS_AOI_SET_PRESET = MEASURE_CMD.IS_MEASURE_CMD_SHARPNESS_AOI_SET_PRESET


class MEASURE_SHARPNESS_AOI_PRESETS(_CtypesEnum):
    IS_MEASURE_SHARPNESS_AOI_PRESET_1 = 1


IS_MEASURE_SHARPNESS_AOI_PRESET_1 = MEASURE_SHARPNESS_AOI_PRESETS.IS_MEASURE_SHARPNESS_AOI_PRESET_1


class IS_MEMORY_CMD(_CtypesEnum):
    IS_MEMORY_GET_SIZE = 1
    IS_MEMORY_READ = 2
    IS_MEMORY_WRITE = 3


IS_MEMORY_GET_SIZE = IS_MEMORY_CMD.IS_MEMORY_GET_SIZE
IS_MEMORY_READ = IS_MEMORY_CMD.IS_MEMORY_READ
IS_MEMORY_WRITE = IS_MEMORY_CMD.IS_MEMORY_WRITE


class IS_MEMORY_DESCRIPTION(_CtypesEnum):
    IS_MEMORY_USER_1 = 1
    IS_MEMORY_USER_2 = 2


IS_MEMORY_USER_1 = IS_MEMORY_DESCRIPTION.IS_MEMORY_USER_1
IS_MEMORY_USER_2 = IS_MEMORY_DESCRIPTION.IS_MEMORY_USER_2


class IS_SEQUENCER_CMD(_CtypesEnum):
    IS_SEQUENCER_MODE_ENABLED_SET = 1
    IS_SEQUENCER_MODE_ENABLED_GET = 2
    IS_SEQUENCER_CONFIGURATION_ENABLED_SET = 3
    IS_SEQUENCER_CONFIGURATION_ENABLED_GET = 4
    IS_SEQUENCER_MODE_SUPPORTED_GET = 5
    IS_SEQUENCER_RESET = 6
    IS_SEQUENCER_CONFIGURATION_LOAD = 7
    IS_SEQUENCER_CONFIGURATION_SAVE = 8
    IS_SEQUENCER_SET_SAVE = 10
    IS_SEQUENCER_SET_START_SET = 11
    IS_SEQUENCER_SET_START_GET = 12
    IS_SEQUENCER_SET_SELECTED_SET = 13
    IS_SEQUENCER_SET_SELECTED_GET = 14
    IS_SEQUENCER_SET_PATH_SET = 15
    IS_SEQUENCER_SET_PATH_GET = 16
    IS_SEQUENCER_SET_MAX_COUNT_GET = 17
    IS_SEQUENCER_FEATURE_SELECTED_SET = 20
    IS_SEQUENCER_FEATURE_SELECTED_GET = 21
    IS_SEQUENCER_FEATURE_ENABLED_SET = 22
    IS_SEQUENCER_FEATURE_ENABLED_GET = 23
    IS_SEQUENCER_FEATURE_SUPPORTED_GET = 24
    IS_SEQUENCER_FEATURE_VALUE_GET = 25
    IS_SEQUENCER_PATH_MAX_COUNT_GET = 30
    IS_SEQUENCER_TRIGGER_SOURCE_SUPPORTED_GET = 31


IS_SEQUENCER_MODE_ENABLED_SET = IS_SEQUENCER_CMD.IS_SEQUENCER_MODE_ENABLED_SET
IS_SEQUENCER_MODE_ENABLED_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_MODE_ENABLED_GET
IS_SEQUENCER_CONFIGURATION_ENABLED_SET = IS_SEQUENCER_CMD.IS_SEQUENCER_CONFIGURATION_ENABLED_SET
IS_SEQUENCER_CONFIGURATION_ENABLED_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_CONFIGURATION_ENABLED_GET
IS_SEQUENCER_MODE_SUPPORTED_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_MODE_SUPPORTED_GET
IS_SEQUENCER_RESET = IS_SEQUENCER_CMD.IS_SEQUENCER_RESET
IS_SEQUENCER_CONFIGURATION_LOAD = IS_SEQUENCER_CMD.IS_SEQUENCER_CONFIGURATION_LOAD
IS_SEQUENCER_CONFIGURATION_SAVE = IS_SEQUENCER_CMD.IS_SEQUENCER_CONFIGURATION_SAVE
IS_SEQUENCER_SET_SAVE = IS_SEQUENCER_CMD.IS_SEQUENCER_SET_SAVE
IS_SEQUENCER_SET_START_SET = IS_SEQUENCER_CMD.IS_SEQUENCER_SET_START_SET
IS_SEQUENCER_SET_START_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_SET_START_GET
IS_SEQUENCER_SET_SELECTED_SET = IS_SEQUENCER_CMD.IS_SEQUENCER_SET_SELECTED_SET
IS_SEQUENCER_SET_SELECTED_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_SET_SELECTED_GET
IS_SEQUENCER_SET_PATH_SET = IS_SEQUENCER_CMD.IS_SEQUENCER_SET_PATH_SET
IS_SEQUENCER_SET_PATH_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_SET_PATH_GET
IS_SEQUENCER_SET_MAX_COUNT_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_SET_MAX_COUNT_GET
IS_SEQUENCER_FEATURE_SELECTED_SET = IS_SEQUENCER_CMD.IS_SEQUENCER_FEATURE_SELECTED_SET
IS_SEQUENCER_FEATURE_SELECTED_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_FEATURE_SELECTED_GET
IS_SEQUENCER_FEATURE_ENABLED_SET = IS_SEQUENCER_CMD.IS_SEQUENCER_FEATURE_ENABLED_SET
IS_SEQUENCER_FEATURE_ENABLED_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_FEATURE_ENABLED_GET
IS_SEQUENCER_FEATURE_SUPPORTED_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_FEATURE_SUPPORTED_GET
IS_SEQUENCER_FEATURE_VALUE_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_FEATURE_VALUE_GET
IS_SEQUENCER_PATH_MAX_COUNT_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_PATH_MAX_COUNT_GET
IS_SEQUENCER_TRIGGER_SOURCE_SUPPORTED_GET = IS_SEQUENCER_CMD.IS_SEQUENCER_TRIGGER_SOURCE_SUPPORTED_GET


class IS_SEQUENCER_FEATURE(_CtypesEnum):
    IS_FEATURE_EXPOSURE = 1
    IS_FEATURE_GAIN = 2
    IS_FEATURE_AOI_OFFSET_X = 4
    IS_FEATURE_AOI_OFFSET_Y = 8
    IS_FEATURE_FLASH = 16


IS_FEATURE_EXPOSURE = IS_SEQUENCER_FEATURE.IS_FEATURE_EXPOSURE
IS_FEATURE_GAIN = IS_SEQUENCER_FEATURE.IS_FEATURE_GAIN
IS_FEATURE_AOI_OFFSET_X = IS_SEQUENCER_FEATURE.IS_FEATURE_AOI_OFFSET_X
IS_FEATURE_AOI_OFFSET_Y = IS_SEQUENCER_FEATURE.IS_FEATURE_AOI_OFFSET_Y
IS_FEATURE_FLASH = IS_SEQUENCER_FEATURE.IS_FEATURE_FLASH


class E_IS_SEQUENCER_TRIGGER_SOURCE(_CtypesEnum):
    IS_TRIGGER_SOURCE_OFF = 0
    IS_TRIGGER_SOURCE_FRAME_END = 1
    IS_TRIGGER_SOURCE_FRAME_START = 2
    IS_TRIGGER_SOURCE_EXPOSURE_END = 4


IS_TRIGGER_SOURCE_OFF = E_IS_SEQUENCER_TRIGGER_SOURCE.IS_TRIGGER_SOURCE_OFF
IS_TRIGGER_SOURCE_FRAME_END = E_IS_SEQUENCER_TRIGGER_SOURCE.IS_TRIGGER_SOURCE_FRAME_END
IS_TRIGGER_SOURCE_FRAME_START = E_IS_SEQUENCER_TRIGGER_SOURCE.IS_TRIGGER_SOURCE_FRAME_START
IS_TRIGGER_SOURCE_EXPOSURE_END = E_IS_SEQUENCER_TRIGGER_SOURCE.IS_TRIGGER_SOURCE_EXPOSURE_END


class IS_PERSISTENT_MEMORY_CMD(_CtypesEnum):
    IS_PERSISTENT_MEMORY_READ_USER_EXTENDED = 1
    IS_PERSISTENT_MEMORY_WRITE_USER_EXTENDED = 2
    IS_PERSISTENT_MEMORY_GET_SIZE_USER_EXTENDED = 3
    IS_PERSISTENT_MEMORY_READ_USER = 4
    IS_PERSISTENT_MEMORY_WRITE_USER = 5
    IS_PERSISTENT_MEMORY_GET_SIZE_USER = 6
    IS_PERSISTENT_MEMORY_READ_USER_PROTECTED = 7
    IS_PERSISTENT_MEMORY_WRITE_USER_PROTECTED = 8
    IS_PERSISTENT_MEMORY_GET_SIZE_USER_PROTECTED = 9


IS_PERSISTENT_MEMORY_READ_USER_EXTENDED = IS_PERSISTENT_MEMORY_CMD.IS_PERSISTENT_MEMORY_READ_USER_EXTENDED
IS_PERSISTENT_MEMORY_WRITE_USER_EXTENDED = IS_PERSISTENT_MEMORY_CMD.IS_PERSISTENT_MEMORY_WRITE_USER_EXTENDED
IS_PERSISTENT_MEMORY_GET_SIZE_USER_EXTENDED = IS_PERSISTENT_MEMORY_CMD.IS_PERSISTENT_MEMORY_GET_SIZE_USER_EXTENDED
IS_PERSISTENT_MEMORY_READ_USER = IS_PERSISTENT_MEMORY_CMD.IS_PERSISTENT_MEMORY_READ_USER
IS_PERSISTENT_MEMORY_WRITE_USER = IS_PERSISTENT_MEMORY_CMD.IS_PERSISTENT_MEMORY_WRITE_USER
IS_PERSISTENT_MEMORY_GET_SIZE_USER = IS_PERSISTENT_MEMORY_CMD.IS_PERSISTENT_MEMORY_GET_SIZE_USER
IS_PERSISTENT_MEMORY_READ_USER_PROTECTED = IS_PERSISTENT_MEMORY_CMD.IS_PERSISTENT_MEMORY_READ_USER_PROTECTED
IS_PERSISTENT_MEMORY_WRITE_USER_PROTECTED = IS_PERSISTENT_MEMORY_CMD.IS_PERSISTENT_MEMORY_WRITE_USER_PROTECTED
IS_PERSISTENT_MEMORY_GET_SIZE_USER_PROTECTED = IS_PERSISTENT_MEMORY_CMD.IS_PERSISTENT_MEMORY_GET_SIZE_USER_PROTECTED


class POWER_DELIVERY_CMD(_CtypesEnum):
    IS_POWER_DELIVERY_CMD_GET_SUPPORTED = 1
    IS_POWER_DELIVERY_CMD_GET_PROFILE = 2
    IS_POWER_DELIVERY_CMD_GET_SUPPORTED_PROFILES = 3
    IS_POWER_DELIVERY_CMD_SET_PROFILE = 4


IS_POWER_DELIVERY_CMD_GET_SUPPORTED = POWER_DELIVERY_CMD.IS_POWER_DELIVERY_CMD_GET_SUPPORTED
IS_POWER_DELIVERY_CMD_GET_PROFILE = POWER_DELIVERY_CMD.IS_POWER_DELIVERY_CMD_GET_PROFILE
IS_POWER_DELIVERY_CMD_GET_SUPPORTED_PROFILES = POWER_DELIVERY_CMD.IS_POWER_DELIVERY_CMD_GET_SUPPORTED_PROFILES
IS_POWER_DELIVERY_CMD_SET_PROFILE = POWER_DELIVERY_CMD.IS_POWER_DELIVERY_CMD_SET_PROFILE


class POWER_DELIVERY_PROFILES(_CtypesEnum):
    IS_POWER_DELIVERY_PROFILE_INVALID = 0
    IS_POWER_DELIVERY_PROFILE_5V_LOW_POWER = 1
    IS_POWER_DELIVERY_PROFILE_5V_HIGH_POWER = 2
    IS_POWER_DELIVERY_PROFILE_9V = 4
    IS_POWER_DELIVERY_PROFILE_12V = 8
    IS_POWER_DELIVERY_PROFILE_14V8 = 16
    IS_POWER_DELIVERY_PROFILE_15V = 32


IS_POWER_DELIVERY_PROFILE_INVALID = POWER_DELIVERY_PROFILES.IS_POWER_DELIVERY_PROFILE_INVALID
IS_POWER_DELIVERY_PROFILE_5V_LOW_POWER = POWER_DELIVERY_PROFILES.IS_POWER_DELIVERY_PROFILE_5V_LOW_POWER
IS_POWER_DELIVERY_PROFILE_5V_HIGH_POWER = POWER_DELIVERY_PROFILES.IS_POWER_DELIVERY_PROFILE_5V_HIGH_POWER
IS_POWER_DELIVERY_PROFILE_9V = POWER_DELIVERY_PROFILES.IS_POWER_DELIVERY_PROFILE_9V
IS_POWER_DELIVERY_PROFILE_12V = POWER_DELIVERY_PROFILES.IS_POWER_DELIVERY_PROFILE_12V
IS_POWER_DELIVERY_PROFILE_14V8 = POWER_DELIVERY_PROFILES.IS_POWER_DELIVERY_PROFILE_14V8
IS_POWER_DELIVERY_PROFILE_15V = POWER_DELIVERY_PROFILES.IS_POWER_DELIVERY_PROFILE_15V



class IS_RANGE_S32(_Structure):
    _pack_ = 8
    _fields_ = [
        ("s32Min", c_int),
        ("s32Max", c_int),
        ("s32Inc", c_int),
    ]


class IS_RANGE_F64(_Structure):
    _pack_ = 8
    _fields_ = [
        ("f64Min", c_double),
        ("f64Max", c_double),
        ("f64Inc", c_double),
    ]


class BOARDINFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("SerNo", (c_char * 12)),
        ("ID", (c_char * 20)),
        ("Version", (c_char * 10)),
        ("Date", (c_char * 12)),
        ("Select", c_ubyte),
        ("Type", c_ubyte),
        ("Reserved", (c_char * 8)),
    ]


class SENSORINFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("SensorID", c_ushort),
        ("strSensorName", (c_char * 32)),
        ("nColorMode", c_char),
        ("nMaxWidth", c_uint),
        ("nMaxHeight", c_uint),
        ("bMasterGain", c_int),
        ("bRGain", c_int),
        ("bGGain", c_int),
        ("bBGain", c_int),
        ("bGlobShutter", c_int),
        ("wPixelSize", c_ushort),
        ("nUpperLeftBayerPixel", c_char),
        ("Reserved", (c_char * 13)),
    ]


class REVISIONINFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("size", c_ushort),
        ("Sensor", c_ushort),
        ("Cypress", c_ushort),
        ("Blackfin", c_uint),
        ("DspFirmware", c_ushort),
        ("USB_Board", c_ushort),
        ("Sensor_Board", c_ushort),
        ("Processing_Board", c_ushort),
        ("Memory_Board", c_ushort),
        ("Housing", c_ushort),
        ("Filter", c_ushort),
        ("Timing_Board", c_ushort),
        ("Product", c_ushort),
        ("Power_Board", c_ushort),
        ("Logic_Board", c_ushort),
        ("FX3", c_ushort),
        ("FPGA", c_ushort),
        ("reserved", (c_ubyte * 92)),
    ]


class UEYE_CAPTURE_STATUS_INFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("dwCapStatusCnt_Total", c_uint),
        ("reserved", (c_ubyte * 60)),
        ("adwCapStatusCnt_Detail", (c_uint * 256)),
    ]


class UEYE_CAMERA_INFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("dwCameraID", c_uint),
        ("dwDeviceID", c_uint),
        ("dwSensorID", c_uint),
        ("dwInUse", c_uint),
        ("SerNo", (c_char * 16)),
        ("Model", (c_char * 16)),
        ("dwStatus", c_uint),
        ("dwReserved", (c_uint * 2)),
        ("FullModelName", (c_char * 32)),
        ("dwReserved2", (c_uint * 5)),
    ]


class _UEYE_CAMERA_LIST(_Structure):
    _pack_ = 8
    _fields_ = [
        ("dwCount", c_uint),
        ("uci", (UEYE_CAMERA_INFO * 1)),
    ]


def UEYE_CAMERA_LIST(uci=(UEYE_CAMERA_INFO * 1)):
    _uci = uci if isinstance(uci, type) else type(uci)

    class UEYE_CAMERA_LIST(_Structure):
        _pack_ = 8
        _fields_ = [
            ("dwCount", c_uint),
            ("uci", _uci),
        ]

    ueye_camera_list = UEYE_CAMERA_LIST()

    return ueye_camera_list


class AUTO_BRIGHT_STATUS(_Structure):
    _pack_ = 8
    _fields_ = [
        ("curValue", c_uint),
        ("curError", c_long),
        ("curController", c_uint),
        ("curCtrlStatus", c_uint),
    ]


class AUTO_WB_CHANNNEL_STATUS(_Structure):
    _pack_ = 8
    _fields_ = [
        ("curValue", c_uint),
        ("curError", c_long),
        ("curCtrlStatus", c_uint),
    ]


class AUTO_WB_STATUS(_Structure):
    _pack_ = 8
    _fields_ = [
        ("RedChannel", AUTO_WB_CHANNNEL_STATUS),
        ("GreenChannel", AUTO_WB_CHANNNEL_STATUS),
        ("BlueChannel", AUTO_WB_CHANNNEL_STATUS),
        ("curController", c_uint),
    ]


class UEYE_AUTO_INFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("AutoAbility", c_uint),
        ("sBrightCtrlStatus", AUTO_BRIGHT_STATUS),
        ("sWBCtrlStatus", AUTO_WB_STATUS),
        ("AShutterPhotomCaps", c_uint),
        ("AGainPhotomCaps", c_uint),
        ("AAntiFlickerCaps", c_uint),
        ("SensorWBModeCaps", c_uint),
        ("reserved", (c_uint * 8)),
    ]


class DC_INFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("nSize", c_uint),
        ("hDC", c_void_p),
        ("nCx", c_uint),
        ("nCy", c_uint),
    ]


class KNEEPOINT(_Structure):
    _pack_ = 8
    _fields_ = [
        ("x", c_double),
        ("y", c_double),
    ]


class KNEEPOINTARRAY(_Structure):
    _pack_ = 8
    _fields_ = [
        ("NumberOfUsedKneepoints", c_int),
        ("Kneepoint", (KNEEPOINT * 10)),
    ]


class KNEEPOINTINFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("NumberOfSupportedKneepoints", c_int),
        ("NumberOfUsedKneepoints", c_int),
        ("MinValueX", c_double),
        ("MaxValueX", c_double),
        ("MinValueY", c_double),
        ("MaxValueY", c_double),
        ("DefaultKneepoint", (KNEEPOINT * 10)),
        ("Reserved", (c_int * 10)),
    ]


class SENSORSCALERINFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("nCurrMode", c_int),
        ("nNumberOfSteps", c_int),
        ("dblFactorIncrement", c_double),
        ("dblMinFactor", c_double),
        ("dblMaxFactor", c_double),
        ("dblCurrFactor", c_double),
        ("nSupportedModes", c_int),
        ("bReserved", (c_ubyte * 84)),
    ]


class UEYETIME(_Structure):
    _pack_ = 8
    _fields_ = [
        ("wYear", c_ushort),
        ("wMonth", c_ushort),
        ("wDay", c_ushort),
        ("wHour", c_ushort),
        ("wMinute", c_ushort),
        ("wSecond", c_ushort),
        ("wMilliseconds", c_ushort),
        ("byReserved", (c_ubyte * 10)),
    ]


class UEYEIMAGEINFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("dwFlags", c_uint),
        ("byReserved1", (c_ubyte * 4)),
        ("u64TimestampDevice", c_longlong),
        ("TimestampSystem", UEYETIME),
        ("dwIoStatus", c_uint),
        ("wAOIIndex", c_ushort),
        ("wAOICycle", c_ushort),
        ("u64FrameNumber", c_longlong),
        ("dwImageBuffers", c_uint),
        ("dwImageBuffersInUse", c_uint),
        ("dwReserved3", c_uint),
        ("dwImageHeight", c_uint),
        ("dwImageWidth", c_uint),
        ("dwHostProcessTime", c_uint),
        ("bySequencerIndex", c_ubyte),
    ]


class IMAGE_FORMAT_INFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("nFormatID", c_int),
        ("nWidth", c_uint),
        ("nHeight", c_uint),
        ("nX0", c_int),
        ("nY0", c_int),
        ("nSupportedCaptureModes", c_uint),
        ("nBinningMode", c_uint),
        ("nSubsamplingMode", c_uint),
        ("strFormatName", (c_char * 64)),
        ("dSensorScalerFactor", c_double),
        ("nReserved", (c_uint * 22)),
    ]


class _IMAGE_FORMAT_LIST(_Structure):
    _pack_ = 8
    _fields_ = [
        ("nSizeOfListEntry", c_uint),
        ("nNumListElements", c_uint),
        ("nReserved", (c_uint * 4)),
        ("FormatInfo", (IMAGE_FORMAT_INFO * 1)),
    ]


def IMAGE_FORMAT_LIST(FormatInfo=(IMAGE_FORMAT_INFO * 1)):
    _FormatInfo = FormatInfo if isinstance(FormatInfo, type) else type(FormatInfo)

    class IMAGE_FORMAT_LIST(_Structure):
        _pack_ = 8
        _fields_ = [
            ("nSizeOfListEntry", c_uint),
            ("nNumListElements", c_uint),
            ("nReserved", (c_uint * 4)),
            ("FormatInfo", _FormatInfo),
        ]

    image_format_list = IMAGE_FORMAT_LIST()

    return image_format_list


class FDT_INFO_EL(_Structure):
    _pack_ = 8
    _fields_ = [
        ("nFacePosX", c_int),
        ("nFacePosY", c_int),
        ("nFaceWidth", c_int),
        ("nFaceHeight", c_int),
        ("nAngle", c_int),
        ("nPosture", c_uint),
        ("TimestampSystem", UEYETIME),
        ("nReserved", c_longlong),
        ("nReserved2", (c_uint * 4)),
    ]


class _FDT_INFO_LIST(_Structure):
    _pack_ = 8
    _fields_ = [
        ("nSizeOfListEntry", c_uint),
        ("nNumDetectedFaces", c_uint),
        ("nNumListElements", c_uint),
        ("nReserved", (c_uint * 4)),
        ("FaceEntry", (FDT_INFO_EL * 1)),
    ]


def FDT_INFO_LIST(FaceEntry=(FDT_INFO_EL * 1)):
    _FaceEntry = FaceEntry if isinstance(FaceEntry, type) else type(FaceEntry)

    class FDT_INFO_LIST(_Structure):
        _pack_ = 8
        _fields_ = [
            ("nSizeOfListEntry", c_uint),
            ("nNumDetectedFaces", c_uint),
            ("nNumListElements", c_uint),
            ("nReserved", (c_uint * 4)),
            ("FaceEntry", _FaceEntry),
        ]

    fdt_info_list = FDT_INFO_LIST()

    return fdt_info_list


class OPENGL_DISPLAY(_Structure):
    _pack_ = 8
    _fields_ = [
        ("nWindowID", c_int),
        ("pDisplay", c_void_p),
    ]


class IS_POINT_2D(_Structure):
    _pack_ = 8
    _fields_ = [
        ("s32X", c_int),
        ("s32Y", c_int),
    ]


class IS_SIZE_2D(_Structure):
    _pack_ = 8
    _fields_ = [
        ("s32Width", c_int),
        ("s32Height", c_int),
    ]


class IS_RECT(_Structure):
    _pack_ = 8
    _fields_ = [
        ("s32X", c_int),
        ("s32Y", c_int),
        ("s32Width", c_int),
        ("s32Height", c_int),
    ]


class AOI_SEQUENCE_PARAMS(_Structure):
    _pack_ = 8
    _fields_ = [
        ("s32AOIIndex", c_int),
        ("s32NumberOfCycleRepetitions", c_int),
        ("s32X", c_int),
        ("s32Y", c_int),
        ("dblExposure", c_double),
        ("s32Gain", c_int),
        ("s32BinningMode", c_int),
        ("s32SubsamplingMode", c_int),
        ("s32DetachImageParameters", c_int),
        ("dblScalerFactor", c_double),
        ("s32InUse", c_int),
        ("byReserved", (c_ubyte * 60)),
    ]


class RANGE_OF_VALUES_U32(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32Minimum", c_uint),
        ("u32Maximum", c_uint),
        ("u32Increment", c_uint),
        ("u32Default", c_uint),
        ("u32Infinite", c_uint),
    ]


class _IS_BOOTBOOST_IDLIST(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32NumberOfEntries", c_uint),
        ("aList", (c_ubyte * 1)),
    ]


def IS_BOOTBOOST_IDLIST(aList=(c_ubyte * 1)):
    _aList = aList if isinstance(aList, type) else type(aList)

    class IS_BOOTBOOST_IDLIST(_Structure):
        _pack_ = 8
        _fields_ = [
            ("u32NumberOfEntries", c_uint),
            ("aList", _aList),
        ]

    is_bootboost_idlist = IS_BOOTBOOST_IDLIST()

    return is_bootboost_idlist


class IS_TIMESTAMP_CONFIGURATION(_Structure):
    _pack_ = 8
    _fields_ = [
        ("s32Mode", c_int),
        ("s32Pin", c_int),
        ("s32Edge", c_int),
    ]


class IS_MULTI_INTEGRATION_CYCLES(_Structure):
    _pack_ = 8
    _fields_ = [
        ("dblIntegration_ms", c_double),
        ("dblPause_ms", c_double),
    ]


class IS_MULTI_INTEGRATION_SCOPE(_Structure):
    _pack_ = 8
    _fields_ = [
        ("dblMinIntegration_ms", c_double),
        ("dblMaxIntegration_ms", c_double),
        ("dblIntegrationGranularity_ms", c_double),
        ("dblMinPause_ms", c_double),
        ("dblMaxPause_ms", c_double),
        ("dblPauseGranularity_ms", c_double),
        ("dblMinCycle_ms", c_double),
        ("dblMaxCycle_ms", c_double),
        ("dblCycleGranularity_ms", c_double),
        ("dblMinTriggerCycle_ms", c_double),
        ("dblMinTriggerDuration_ms", c_double),
        ("nMinNumberOfCycles", c_uint),
        ("nMaxNumberOfCycles", c_uint),
        ("m_bReserved", (c_ubyte * 32)),
    ]


class IS_EXTERNAL_INTERFACE_I2C_CONFIGURATION(_Structure):
    _pack_ = 1
    _fields_ = [
        ("bySlaveAddress", c_ubyte),
        ("wRegisterAddress", c_ushort),
        ("byRegisterAddressType", c_ubyte),
        ("byAckPolling", c_ubyte),
        ("byReserved", (c_ubyte * 11)),
    ]


class IS_EXTERNAL_INTERFACE_CONFIGURATION(_Structure):
    _pack_ = 1
    _fields_ = [
        ("wInterfaceType", c_ushort),
        ("sInterfaceConfiguration", (c_ubyte * 16)),
        ("wSendEvent", c_ushort),
        ("wDataSelection", c_ushort),
    ]


class IS_DEVICE_INFO_HEARTBEAT(_Structure):
    _pack_ = 1
    _fields_ = [
        ("reserved_1", (c_ubyte * 24)),
        ("dwRuntimeFirmwareVersion", c_uint),
        ("reserved_2", (c_ubyte * 8)),
        ("wTemperature", c_ushort),
        ("wLinkSpeed_Mb", c_ushort),
        ("reserved_3", (c_ubyte * 6)),
        ("wComportOffset", c_ushort),
        ("reserved", (c_ubyte * 200)),
    ]


class IS_DEVICE_INFO_CONTROL(_Structure):
    _pack_ = 1
    _fields_ = [
        ("dwDeviceId", c_uint),
        ("reserved", (c_ubyte * 148)),
    ]


class IS_DEVICE_INFO(_Structure):
    _pack_ = 1
    _fields_ = [
        ("infoDevHeartbeat", IS_DEVICE_INFO_HEARTBEAT),
        ("infoDevControl", IS_DEVICE_INFO_CONTROL),
        ("reserved", (c_ubyte * 240)),
    ]


class _IS_OPTIMAL_CAMERA_TIMING(_Structure):
    _pack_ = 8
    _fields_ = [
        ("s32Mode", c_int),
        ("s32TimeoutFineTuning", c_int),
        ("ps32PixelClock", ctypes.POINTER(c_int)),
        ("pdFramerate", ctypes.POINTER(c_double)),
    ]


def IS_OPTIMAL_CAMERA_TIMING(ps32PixelClock=None, pdFramerate=None):
    _ps32PixelClock = ps32PixelClock if ps32PixelClock is None else ctypes.cast(ctypes.pointer(ps32PixelClock), ctypes.POINTER(c_int))
    _pdFramerate = pdFramerate if pdFramerate is None else ctypes.cast(ctypes.pointer(pdFramerate), ctypes.POINTER(c_double))

    is_optimal_camera_timing = _IS_OPTIMAL_CAMERA_TIMING()

    is_optimal_camera_timing.ps32PixelClock = _ps32PixelClock
    is_optimal_camera_timing.pdFramerate = _pdFramerate

    return is_optimal_camera_timing


class sby(_Structure):
    _pack_ = 1
    _fields_ = [
        ("by1", c_ubyte),
        ("by2", c_ubyte),
        ("by3", c_ubyte),
        ("by4", c_ubyte),
    ]


class UEYE_ETH_ADDR_IPV4(_Union):
    _pack_ = 1
    _fields_ = [
        ("by", sby),
        ("dwAddr", c_uint),
    ]


class UEYE_ETH_ADDR_MAC(_Structure):
    _pack_ = 1
    _fields_ = [
        ("abyOctet", (c_ubyte * 6)),
    ]


class UEYE_ETH_IP_CONFIGURATION(_Structure):
    _pack_ = 1
    _fields_ = [
        ("ipAddress", UEYE_ETH_ADDR_IPV4),
        ("ipSubnetmask", UEYE_ETH_ADDR_IPV4),
        ("reserved", (c_ubyte * 4)),
    ]


class UEYE_ETH_DEVICE_INFO_HEARTBEAT(_Structure):
    _pack_ = 1
    _fields_ = [
        ("abySerialNumber", (c_ubyte * 12)),
        ("byDeviceType", c_ubyte),
        ("byCameraID", c_ubyte),
        ("wSensorID", c_ushort),
        ("wSizeImgMem_MB", c_ushort),
        ("reserved_1", (c_ubyte * 2)),
        ("dwVerStarterFirmware", c_uint),
        ("dwVerRuntimeFirmware", c_uint),
        ("dwStatus", c_uint),
        ("reserved_2", (c_ubyte * 4)),
        ("wTemperature", c_ushort),
        ("wLinkSpeed_Mb", c_ushort),
        ("macDevice", UEYE_ETH_ADDR_MAC),
        ("wComportOffset", c_ushort),
        ("ipcfgPersistentIpCfg", UEYE_ETH_IP_CONFIGURATION),
        ("ipcfgCurrentIpCfg", UEYE_ETH_IP_CONFIGURATION),
        ("macPairedHost", UEYE_ETH_ADDR_MAC),
        ("reserved_4", (c_ubyte * 2)),
        ("ipPairedHostIp", UEYE_ETH_ADDR_IPV4),
        ("ipAutoCfgIpRangeBegin", UEYE_ETH_ADDR_IPV4),
        ("ipAutoCfgIpRangeEnd", UEYE_ETH_ADDR_IPV4),
        ("abyUserSpace", (c_ubyte * 8)),
        ("reserved_5", (c_ubyte * 84)),
        ("reserved_6", (c_ubyte * 64)),
    ]


class UEYE_ETH_DEVICE_INFO_CONTROL(_Structure):
    _pack_ = 1
    _fields_ = [
        ("dwDeviceID", c_uint),
        ("dwControlStatus", c_uint),
        ("reserved_1", (c_ubyte * 80)),
        ("reserved_2", (c_ubyte * 64)),
    ]


class UEYE_ETH_ETHERNET_CONFIGURATION(_Structure):
    _pack_ = 1
    _fields_ = [
        ("ipcfg", UEYE_ETH_IP_CONFIGURATION),
        ("mac", UEYE_ETH_ADDR_MAC),
    ]


class UEYE_ETH_AUTOCFG_IP_SETUP(_Structure):
    _pack_ = 1
    _fields_ = [
        ("ipAutoCfgIpRangeBegin", UEYE_ETH_ADDR_IPV4),
        ("ipAutoCfgIpRangeEnd", UEYE_ETH_ADDR_IPV4),
        ("reserved", (c_ubyte * 4)),
    ]


class UEYE_ETH_ADAPTER_INFO(_Structure):
    _pack_ = 1
    _fields_ = [
        ("dwAdapterID", c_uint),
        ("dwDeviceLinkspeed", c_uint),
        ("ethcfg", UEYE_ETH_ETHERNET_CONFIGURATION),
        ("reserved_2", (c_ubyte * 2)),
        ("bIsEnabledDHCP", c_int),
        ("autoCfgIp", UEYE_ETH_AUTOCFG_IP_SETUP),
        ("bIsValidAutoCfgIpRange", c_int),
        ("dwCntDevicesKnown", c_uint),
        ("dwCntDevicesPaired", c_uint),
        ("wPacketFilter", c_ushort),
        ("reserved_3", (c_ubyte * 38)),
        ("reserved_4", (c_ubyte * 64)),
    ]


class UEYE_ETH_DRIVER_INFO(_Structure):
    _pack_ = 1
    _fields_ = [
        ("dwMinVerStarterFirmware", c_uint),
        ("dwMaxVerStarterFirmware", c_uint),
        ("reserved_1", (c_ubyte * 8)),
        ("reserved_2", (c_ubyte * 64)),
    ]


class UEYE_ETH_DEVICE_INFO(_Structure):
    _pack_ = 1
    _fields_ = [
        ("infoDevHeartbeat", UEYE_ETH_DEVICE_INFO_HEARTBEAT),
        ("infoDevControl", UEYE_ETH_DEVICE_INFO_CONTROL),
        ("infoAdapter", UEYE_ETH_ADAPTER_INFO),
        ("infoDriver", UEYE_ETH_DRIVER_INFO),
    ]


class UEYE_COMPORT_CONFIGURATION(_Structure):
    _pack_ = 1
    _fields_ = [
        ("wComportNumber", c_ushort),
    ]


class IO_FLASH_PARAMS(_Structure):
    _pack_ = 8
    _fields_ = [
        ("s32Delay", c_int),
        ("u32Duration", c_uint),
    ]


class IO_PWM_PARAMS(_Structure):
    _pack_ = 8
    _fields_ = [
        ("dblFrequency_Hz", c_double),
        ("dblDutyCycle", c_double),
    ]


class IO_GPIO_CONFIGURATION(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32Gpio", c_uint),
        ("u32Caps", c_uint),
        ("u32Configuration", c_uint),
        ("u32State", c_uint),
        ("u32Reserved", (c_uint * 12)),
    ]


class _AES_CONFIGURATION(_Structure):
    _pack_ = 4
    _fields_ = [
        ("nMode", c_int),
        ("pConfiguration", (c_char * 1)),
    ]


def AES_CONFIGURATION(pConfiguration=(c_char * 1)):
    _pConfiguration = pConfiguration if isinstance(pConfiguration, type) else type(pConfiguration)

    class AES_CONFIGURATION(_Structure):
        _pack_ = 4
        _fields_ = [
            ("nMode", c_int),
            ("pConfiguration", _pConfiguration),
        ]

    aes_configuration = AES_CONFIGURATION()

    return aes_configuration


class AES_PEAK_WHITE_CONFIGURATION(_Structure):
    _pack_ = 8
    _fields_ = [
        ("rectUserAOI", IS_RECT),
        ("nFrameSkip", c_uint),
        ("nHysteresis", c_uint),
        ("nReference", c_uint),
        ("nChannel", c_uint),
        ("f64Maximum", c_double),
        ("f64Minimum", c_double),
        ("reserved", (c_char * 32)),
    ]


class AES_PEAK_CONFIGURATION(_Structure):
    _pack_ = 8
    _fields_ = [
        ("rectUserAOI", IS_RECT),
        ("nFrameSkip", c_uint),
        ("nHysteresis", c_uint),
        ("nReference", c_uint),
        ("nChannel", c_uint),
        ("f64Maximum", c_double),
        ("f64Minimum", c_double),
        ("nMode", c_uint),
        ("nGranularity", c_uint),
    ]


class AES_PEAK_WHITE_CONFIGURATION_RANGE(_Structure):
    _pack_ = 8
    _fields_ = [
        ("rangeFrameSkip", IS_RANGE_S32),
        ("rangeHysteresis", IS_RANGE_S32),
        ("rangeReference", IS_RANGE_S32),
        ("reserved", (c_char * 32)),
    ]


class AES_PEAK_CONFIGURATION_RANGE(_Structure):
    _pack_ = 8
    _fields_ = [
        ("rangeFrameSkip", IS_RANGE_S32),
        ("rangeHysteresis", IS_RANGE_S32),
        ("rangeReference", IS_RANGE_S32),
    ]


class BUFFER_CONVERSION_PARAMS(_Structure):
    _pack_ = 8
    _fields_ = [
        ("pSourceBuffer", c_mem_p),
        ("pDestBuffer", c_mem_p),
        ("nDestPixelFormat", c_int),
        ("nDestPixelConverter", c_int),
        ("nDestGamma", c_int),
        ("nDestEdgeEnhancement", c_int),
        ("nDestColorCorrectionMode", c_int),
        ("nDestSaturationU", c_int),
        ("nDestSaturationV", c_int),
        ("reserved", (c_ubyte * 32)),
    ]


class _IMAGE_FILE_PARAMS(_Structure):
    _pack_ = 8
    _fields_ = [
        ("pwchFileName", c_wchar_p),
        ("nFileType", c_uint),
        ("nQuality", c_uint),
        ("ppcImageMem", ctypes.POINTER(c_mem_p)),
        ("pnImageID", ctypes.POINTER(c_uint)),
        ("reserved", (c_ubyte * 32)),
    ]


def IMAGE_FILE_PARAMS(ppcImageMem=None, pnImageID=None):
    _ppcImageMem = ppcImageMem if ppcImageMem is None else ctypes.cast(ctypes.pointer(ppcImageMem), ctypes.POINTER(c_mem_p))
    _pnImageID = pnImageID if pnImageID is None else ctypes.cast(ctypes.pointer(pnImageID), ctypes.POINTER(c_uint))

    image_file_params = _IMAGE_FILE_PARAMS()

    image_file_params.ppcImageMem = _ppcImageMem
    image_file_params.pnImageID = _pnImageID

    return image_file_params


class ID_RANGE(_Structure):
    _pack_ = 8
    _fields_ = [
        ("s32First", c_int),
        ("s32Last", c_int),
    ]


class IMGBUF_ITERATION_INFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32IterationID", c_uint),
        ("rangeImageID", ID_RANGE),
        ("bReserved", (c_ubyte * 52)),
    ]


class IMGBUF_ITEM(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32IterationID", c_uint),
        ("s32ImageID", c_int),
    ]


class MEASURE_SHARPNESS_AOI_INFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32NumberAOI", c_uint),
        ("u32SharpnessValue", c_uint),
        ("rcAOI", IS_RECT),
    ]


class IS_LUT_CONFIGURATION_64(_Structure):
    _pack_ = 8
    _fields_ = [
        ("dblValues", ((c_double * 64) * 3)),
        ("bAllChannelsAreEqual", c_int),
    ]


class IS_LUT_CONFIGURATION_PRESET_64(_Structure):
    _pack_ = 8
    _fields_ = [
        ("predefinedLutID", c_int),
        ("lutConfiguration", IS_LUT_CONFIGURATION_64),
    ]


class IS_LUT_STATE(_Structure):
    _pack_ = 8
    _fields_ = [
        ("bLUTEnabled", c_int),
        ("nLUTStateID", c_int),
        ("nLUTModeID", c_int),
        ("nLUTBits", c_int),
    ]


class IS_LUT_SUPPORT_INFO(_Structure):
    _pack_ = 8
    _fields_ = [
        ("bSupportLUTHardware", c_int),
        ("bSupportLUTSoftware", c_int),
        ("nBitsHardware", c_int),
        ("nBitsSoftware", c_int),
        ("nChannelsHardware", c_int),
        ("nChannelsSoftware", c_int),
    ]


class IS_MEMORY_ACCESS(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32Description", c_uint),
        ("u32Offset", c_uint),
        ("pu8Data", c_mem_p),
        ("u32SizeOfData", c_uint),
    ]


class IS_MEMORY_SIZE(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32Description", c_uint),
        ("u32SizeBytes", c_uint),
    ]


class IS_MULTI_AOI_DESCRIPTOR(_Structure):
    _pack_ = 8
    _fields_ = [
        ("nPosX", c_uint),
        ("nPosY", c_uint),
        ("nWidth", c_uint),
        ("nHeight", c_uint),
        ("nStatus", c_uint),
    ]


class _IS_MULTI_AOI_CONTAINER(_Structure):
    _pack_ = 8
    _fields_ = [
        ("nNumberOfAOIs", c_uint),
        ("pMultiAOIList", ctypes.POINTER(IS_MULTI_AOI_DESCRIPTOR)),
    ]


def IS_MULTI_AOI_CONTAINER(pMultiAOIList=(IS_MULTI_AOI_DESCRIPTOR * 1)):
    _pMultiAOIList = pMultiAOIList if isinstance(pMultiAOIList, type) else type(pMultiAOIList)

    is_multi_aoi_container = _IS_MULTI_AOI_CONTAINER()

    is_multi_aoi_container.pMultiAOIList = ctypes.cast(ctypes.create_string_buffer(ctypes.sizeof(_pMultiAOIList)), ctypes.POINTER(IS_MULTI_AOI_DESCRIPTOR))

    return is_multi_aoi_container


class IS_PMC_READONLYDEVICEDESCRIPTOR(_Structure):
    _pack_ = 8
    _fields_ = [
        ("ipCamera", UEYE_ETH_ADDR_IPV4),
        ("ipMulticast", UEYE_ETH_ADDR_IPV4),
        ("u32CameraId", c_uint),
        ("u32ErrorHandlingMode", c_uint),
    ]


class IS_SEQUENCER_PATH(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32PathIndex", c_uint),
        ("u32NextIndex", c_uint),
        ("u32TriggerSource", c_uint),
        ("u32TriggerActivation", c_uint),
    ]


class IS_SEQUENCER_GAIN_CONFIGURATION(_Structure):
    _pack_ = 8
    _fields_ = [
        ("Master", c_uint),
        ("Red", c_uint),
        ("Green", c_uint),
        ("Blue", c_uint),
    ]


class IS_SEQUENCER_FLASH_CONFIGURATION(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32Mode", c_uint),
        ("u32Duration", c_uint),
        ("u32Delay", c_uint),
    ]


class IS_PERSISTENT_MEMORY(_Structure):
    _pack_ = 8
    _fields_ = [
        ("u32Offset", c_uint),
        ("u32Count", c_uint),
        ("s32Option", c_int),
        ("pu8Memory", c_mem_p),
    ]


IS_COLORMODE_INVALID = 0
IS_COLORMODE_MONOCHROME = 1
IS_COLORMODE_BAYER = 2
IS_COLORMODE_CBYCRY = 4
IS_COLORMODE_JPEG = 8
IS_SENSOR_INVALID = 0x0000
IS_SENSOR_UI141X_M = 0x0001
IS_SENSOR_UI141X_C = 0x0002
IS_SENSOR_UI144X_M = 0x0003
IS_SENSOR_UI144X_C = 0x0004
IS_SENSOR_UI154X_M = 0x0030
IS_SENSOR_UI154X_C = 0x0031
IS_SENSOR_UI145X_C = 0x0008
IS_SENSOR_UI146X_C = 0x000a
IS_SENSOR_UI148X_M = 0x000b
IS_SENSOR_UI148X_C = 0x000c
IS_SENSOR_UI121X_M = 0x0010
IS_SENSOR_UI121X_C = 0x0011
IS_SENSOR_UI122X_M = 0x0012
IS_SENSOR_UI122X_C = 0x0013
IS_SENSOR_UI164X_C = 0x0015
IS_SENSOR_UI155X_C = 0x0017
IS_SENSOR_UI1223_M = 0x0018
IS_SENSOR_UI1223_C = 0x0019
IS_SENSOR_UI149X_M = 0x003E
IS_SENSOR_UI149X_C = 0x003F
IS_SENSOR_UI1225_M = 0x0022
IS_SENSOR_UI1225_C = 0x0023
IS_SENSOR_UI1645_C = 0x0025
IS_SENSOR_UI1555_C = 0x0027
IS_SENSOR_UI1545_M = 0x0028
IS_SENSOR_UI1545_C = 0x0029
IS_SENSOR_UI1455_C = 0x002B
IS_SENSOR_UI1465_C = 0x002D
IS_SENSOR_UI1485_M = 0x002E
IS_SENSOR_UI1485_C = 0x002F
IS_SENSOR_UI1495_M = 0x0040
IS_SENSOR_UI1495_C = 0x0041
IS_SENSOR_UI112X_M = 0x004A
IS_SENSOR_UI112X_C = 0x004B
IS_SENSOR_UI1008_M = 0x004C
IS_SENSOR_UI1008_C = 0x004D
IS_SENSOR_UI1005_M = 0x020A
IS_SENSOR_UI1005_C = 0x020B
IS_SENSOR_UI1240_M = 0x0050
IS_SENSOR_UI1240_C = 0x0051
IS_SENSOR_UI1240_NIR = 0x0062
IS_SENSOR_UI1240LE_M = 0x0054
IS_SENSOR_UI1240LE_C = 0x0055
IS_SENSOR_UI1240LE_NIR = 0x0064
IS_SENSOR_UI1240ML_M = 0x0066
IS_SENSOR_UI1240ML_C = 0x0067
IS_SENSOR_UI1240ML_NIR = 0x0200
IS_SENSOR_UI1243_M_SMI = 0x0078
IS_SENSOR_UI1243_C_SMI = 0x0079
IS_SENSOR_UI1543_M = 0x0032
IS_SENSOR_UI1543_C = 0x0033
IS_SENSOR_UI1544_M = 0x003A
IS_SENSOR_UI1544_C = 0x003B
IS_SENSOR_UI1543_M_WO = 0x003C
IS_SENSOR_UI1543_C_WO = 0x003D
IS_SENSOR_UI1453_C = 0x0035
IS_SENSOR_UI1463_C = 0x0037
IS_SENSOR_UI1483_M = 0x0038
IS_SENSOR_UI1483_C = 0x0039
IS_SENSOR_UI1493_M = 0x004E
IS_SENSOR_UI1493_C = 0x004F
IS_SENSOR_UI1463_M_WO = 0x0044
IS_SENSOR_UI1463_C_WO = 0x0045
IS_SENSOR_UI1553_C_WN = 0x0047
IS_SENSOR_UI1483_M_WO = 0x0048
IS_SENSOR_UI1483_C_WO = 0x0049
IS_SENSOR_UI1580_M = 0x005A
IS_SENSOR_UI1580_C = 0x005B
IS_SENSOR_UI1580LE_M = 0x0060
IS_SENSOR_UI1580LE_C = 0x0061
IS_SENSOR_UI1360M = 0x0068
IS_SENSOR_UI1360C = 0x0069
IS_SENSOR_UI1360NIR = 0x0212
IS_SENSOR_UI1370M = 0x006A
IS_SENSOR_UI1370C = 0x006B
IS_SENSOR_UI1370NIR = 0x0214
IS_SENSOR_UI1250_M = 0x006C
IS_SENSOR_UI1250_C = 0x006D
IS_SENSOR_UI1250_NIR = 0x006E
IS_SENSOR_UI1250LE_M = 0x0070
IS_SENSOR_UI1250LE_C = 0x0071
IS_SENSOR_UI1250LE_NIR = 0x0072
IS_SENSOR_UI1250ML_M = 0x0074
IS_SENSOR_UI1250ML_C = 0x0075
IS_SENSOR_UI1250ML_NIR = 0x0202
IS_SENSOR_XS = 0x020B
IS_SENSOR_UI1493_M_AR = 0x0204
IS_SENSOR_UI1493_C_AR = 0x0205
IS_SENSOR_UI1060_M = 0x021A
IS_SENSOR_UI1060_C = 0x021B
IS_SENSOR_UI1013XC = 0x021D
IS_SENSOR_UI1140M = 0x021E
IS_SENSOR_UI1140C = 0x021F
IS_SENSOR_UI1140NIR = 0x0220
IS_SENSOR_UI1590M = 0x0222
IS_SENSOR_UI1590C = 0x0223
IS_SENSOR_UI1260_M = 0x0226
IS_SENSOR_UI1260_C = 0x0227
IS_SENSOR_UI1130_M = 0x022A
IS_SENSOR_UI1130_C = 0x022B
IS_SENSOR_UI1160_M = 0x022C
IS_SENSOR_UI1160_C = 0x022D
IS_SENSOR_UI1180_M = 0x022E
IS_SENSOR_UI1180_C = 0x022F
IS_SENSOR_UI1080_M = 0x0230
IS_SENSOR_UI1080_C = 0x0231
IS_SENSOR_UI1280_M = 0x0232
IS_SENSOR_UI1280_C = 0x0233
IS_SENSOR_UI1860_M = 0x0234
IS_SENSOR_UI1860_C = 0x0235
IS_SENSOR_UI1880_M = 0x0236
IS_SENSOR_UI1880_C = 0x0237
IS_SENSOR_UI1270_M = 0x0238
IS_SENSOR_UI1270_C = 0x0239
IS_SENSOR_UI1070_M = 0x023A
IS_SENSOR_UI1070_C = 0x023B
IS_SENSOR_UI1130LE_M = 0x023C
IS_SENSOR_UI1130LE_C = 0x023D
IS_SENSOR_UI1290_M = 0x023E
IS_SENSOR_UI1290_C = 0x023F
IS_SENSOR_UI1090_M = 0x0240
IS_SENSOR_UI1090_C = 0x0241
IS_SENSOR_UI1000_M = 0x0242
IS_SENSOR_UI1000_C = 0x0243
IS_SENSOR_UI1200_M = 0x0244
IS_SENSOR_UI1200_C = 0x0245
IS_SENSOR_UI223X_M = 0x0080
IS_SENSOR_UI223X_C = 0x0081
IS_SENSOR_UI241X_M = 0x0082
IS_SENSOR_UI241X_C = 0x0083
IS_SENSOR_UI234X_M = 0x0084
IS_SENSOR_UI234X_C = 0x0085
IS_SENSOR_UI221X_M = 0x0088
IS_SENSOR_UI221X_C = 0x0089
IS_SENSOR_UI231X_M = 0x0090
IS_SENSOR_UI231X_C = 0x0091
IS_SENSOR_UI222X_M = 0x0092
IS_SENSOR_UI222X_C = 0x0093
IS_SENSOR_UI224X_M = 0x0096
IS_SENSOR_UI224X_C = 0x0097
IS_SENSOR_UI225X_M = 0x0098
IS_SENSOR_UI225X_C = 0x0099
IS_SENSOR_UI214X_M = 0x009A
IS_SENSOR_UI214X_C = 0x009B
IS_SENSOR_UI228X_M = 0x009C
IS_SENSOR_UI228X_C = 0x009D
IS_SENSOR_UI223X_M_R3 = 0x0180
IS_SENSOR_UI223X_C_R3 = 0x0181
IS_SENSOR_UI241X_M_R2 = 0x0182
IS_SENSOR_UI251X_M = 0x0182
IS_SENSOR_UI241X_C_R2 = 0x0183
IS_SENSOR_UI251X_C = 0x0183
IS_SENSOR_UI234X_M_R3 = 0x0184
IS_SENSOR_UI234X_C_R3 = 0x0185
IS_SENSOR_UI221X_M_R3 = 0x0188
IS_SENSOR_UI221X_C_R3 = 0x0189
IS_SENSOR_UI222X_M_R3 = 0x0192
IS_SENSOR_UI222X_C_R3 = 0x0193
IS_SENSOR_UI224X_M_R3 = 0x0196
IS_SENSOR_UI224X_C_R3 = 0x0197
IS_SENSOR_UI225X_M_R3 = 0x0198
IS_SENSOR_UI225X_C_R3 = 0x0199
IS_SENSOR_UI2130_M = 0x019E
IS_SENSOR_UI2130_C = 0x019F
IS_SENSOR_PASSIVE_MULTICAST = 0x0F00
IS_NO_SUCCESS = -1
IS_SUCCESS = 0
IS_INVALID_CAMERA_HANDLE = 1
IS_INVALID_HANDLE = 1
IS_IO_REQUEST_FAILED = 2
IS_CANT_OPEN_DEVICE = 3
IS_CANT_CLOSE_DEVICE = 4
IS_CANT_SETUP_MEMORY = 5
IS_NO_HWND_FOR_ERROR_REPORT = 6
IS_ERROR_MESSAGE_NOT_CREATED = 7
IS_ERROR_STRING_NOT_FOUND = 8
IS_HOOK_NOT_CREATED = 9
IS_TIMER_NOT_CREATED = 10
IS_CANT_OPEN_REGISTRY = 11
IS_CANT_READ_REGISTRY = 12
IS_CANT_VALIDATE_BOARD = 13
IS_CANT_GIVE_BOARD_ACCESS = 14
IS_NO_IMAGE_MEM_ALLOCATED = 15
IS_CANT_CLEANUP_MEMORY = 16
IS_CANT_COMMUNICATE_WITH_DRIVER = 17
IS_FUNCTION_NOT_SUPPORTED_YET = 18
IS_OPERATING_SYSTEM_NOT_SUPPORTED = 19
IS_INVALID_VIDEO_IN = 20
IS_INVALID_IMG_SIZE = 21
IS_INVALID_ADDRESS = 22
IS_INVALID_VIDEO_MODE = 23
IS_INVALID_AGC_MODE = 24
IS_INVALID_GAMMA_MODE = 25
IS_INVALID_SYNC_LEVEL = 26
IS_INVALID_CBARS_MODE = 27
IS_INVALID_COLOR_MODE = 28
IS_INVALID_SCALE_FACTOR = 29
IS_INVALID_IMAGE_SIZE = 30
IS_INVALID_IMAGE_POS = 31
IS_INVALID_CAPTURE_MODE = 32
IS_INVALID_RISC_PROGRAM = 33
IS_INVALID_BRIGHTNESS = 34
IS_INVALID_CONTRAST = 35
IS_INVALID_SATURATION_U = 36
IS_INVALID_SATURATION_V = 37
IS_INVALID_HUE = 38
IS_INVALID_HOR_FILTER_STEP = 39
IS_INVALID_VERT_FILTER_STEP = 40
IS_INVALID_EEPROM_READ_ADDRESS = 41
IS_INVALID_EEPROM_WRITE_ADDRESS = 42
IS_INVALID_EEPROM_READ_LENGTH = 43
IS_INVALID_EEPROM_WRITE_LENGTH = 44
IS_INVALID_BOARD_INFO_POINTER = 45
IS_INVALID_DISPLAY_MODE = 46
IS_INVALID_ERR_REP_MODE = 47
IS_INVALID_BITS_PIXEL = 48
IS_INVALID_MEMORY_POINTER = 49
IS_FILE_WRITE_OPEN_ERROR = 50
IS_FILE_READ_OPEN_ERROR = 51
IS_FILE_READ_INVALID_BMP_ID = 52
IS_FILE_READ_INVALID_BMP_SIZE = 53
IS_FILE_READ_INVALID_BIT_COUNT = 54
IS_WRONG_KERNEL_VERSION = 55
IS_RISC_INVALID_XLENGTH = 60
IS_RISC_INVALID_YLENGTH = 61
IS_RISC_EXCEED_IMG_SIZE = 62
IS_DD_MAIN_FAILED = 70
IS_DD_PRIMSURFACE_FAILED = 71
IS_DD_SCRN_SIZE_NOT_SUPPORTED = 72
IS_DD_CLIPPER_FAILED = 73
IS_DD_CLIPPER_HWND_FAILED = 74
IS_DD_CLIPPER_CONNECT_FAILED = 75
IS_DD_BACKSURFACE_FAILED = 76
IS_DD_BACKSURFACE_IN_SYSMEM = 77
IS_DD_MDL_MALLOC_ERR = 78
IS_DD_MDL_SIZE_ERR = 79
IS_DD_CLIP_NO_CHANGE = 80
IS_DD_PRIMMEM_NULL = 81
IS_DD_BACKMEM_NULL = 82
IS_DD_BACKOVLMEM_NULL = 83
IS_DD_OVERLAYSURFACE_FAILED = 84
IS_DD_OVERLAYSURFACE_IN_SYSMEM = 85
IS_DD_OVERLAY_NOT_ALLOWED = 86
IS_DD_OVERLAY_COLKEY_ERR = 87
IS_DD_OVERLAY_NOT_ENABLED = 88
IS_DD_GET_DC_ERROR = 89
IS_DD_DDRAW_DLL_NOT_LOADED = 90
IS_DD_THREAD_NOT_CREATED = 91
IS_DD_CANT_GET_CAPS = 92
IS_DD_NO_OVERLAYSURFACE = 93
IS_DD_NO_OVERLAYSTRETCH = 94
IS_DD_CANT_CREATE_OVERLAYSURFACE = 95
IS_DD_CANT_UPDATE_OVERLAYSURFACE = 96
IS_DD_INVALID_STRETCH = 97
IS_EV_INVALID_EVENT_NUMBER = 100
IS_INVALID_MODE = 101
IS_CANT_FIND_FALCHOOK = 102
IS_CANT_FIND_HOOK = 102
IS_CANT_GET_HOOK_PROC_ADDR = 103
IS_CANT_CHAIN_HOOK_PROC = 104
IS_CANT_SETUP_WND_PROC = 105
IS_HWND_NULL = 106
IS_INVALID_UPDATE_MODE = 107
IS_NO_ACTIVE_IMG_MEM = 108
IS_CANT_INIT_EVENT = 109
IS_FUNC_NOT_AVAIL_IN_OS = 110
IS_CAMERA_NOT_CONNECTED = 111
IS_SEQUENCE_LIST_EMPTY = 112
IS_CANT_ADD_TO_SEQUENCE = 113
IS_LOW_OF_SEQUENCE_RISC_MEM = 114
IS_IMGMEM2FREE_USED_IN_SEQ = 115
IS_IMGMEM_NOT_IN_SEQUENCE_LIST = 116
IS_SEQUENCE_BUF_ALREADY_LOCKED = 117
IS_INVALID_DEVICE_ID = 118
IS_INVALID_BOARD_ID = 119
IS_ALL_DEVICES_BUSY = 120
IS_HOOK_BUSY = 121
IS_TIMED_OUT = 122
IS_NULL_POINTER = 123
IS_WRONG_HOOK_VERSION = 124
IS_INVALID_PARAMETER = 125
IS_NOT_ALLOWED = 126
IS_OUT_OF_MEMORY = 127
IS_INVALID_WHILE_LIVE = 128
IS_ACCESS_VIOLATION = 129
IS_UNKNOWN_ROP_EFFECT = 130
IS_INVALID_RENDER_MODE = 131
IS_INVALID_THREAD_CONTEXT = 132
IS_NO_HARDWARE_INSTALLED = 133
IS_INVALID_WATCHDOG_TIME = 134
IS_INVALID_WATCHDOG_MODE = 135
IS_INVALID_PASSTHROUGH_IN = 136
IS_ERROR_SETTING_PASSTHROUGH_IN = 137
IS_FAILURE_ON_SETTING_WATCHDOG = 138
IS_NO_USB20 = 139
IS_CAPTURE_RUNNING = 140
IS_MEMORY_BOARD_ACTIVATED = 141
IS_MEMORY_BOARD_DEACTIVATED = 142
IS_NO_MEMORY_BOARD_CONNECTED = 143
IS_TOO_LESS_MEMORY = 144
IS_IMAGE_NOT_PRESENT = 145
IS_MEMORY_MODE_RUNNING = 146
IS_MEMORYBOARD_DISABLED = 147
IS_TRIGGER_ACTIVATED = 148
IS_WRONG_KEY = 150
IS_CRC_ERROR = 151
IS_NOT_YET_RELEASED = 152
IS_NOT_CALIBRATED = 153
IS_WAITING_FOR_KERNEL = 154
IS_NOT_SUPPORTED = 155
IS_TRIGGER_NOT_ACTIVATED = 156
IS_OPERATION_ABORTED = 157
IS_BAD_STRUCTURE_SIZE = 158
IS_INVALID_BUFFER_SIZE = 159
IS_INVALID_PIXEL_CLOCK = 160
IS_INVALID_EXPOSURE_TIME = 161
IS_AUTO_EXPOSURE_RUNNING = 162
IS_CANNOT_CREATE_BB_SURF = 163
IS_CANNOT_CREATE_BB_MIX = 164
IS_BB_OVLMEM_NULL = 165
IS_CANNOT_CREATE_BB_OVL = 166
IS_NOT_SUPP_IN_OVL_SURF_MODE = 167
IS_INVALID_SURFACE = 168
IS_SURFACE_LOST = 169
IS_RELEASE_BB_OVL_DC = 170
IS_BB_TIMER_NOT_CREATED = 171
IS_BB_OVL_NOT_EN = 172
IS_ONLY_IN_BB_MODE = 173
IS_INVALID_COLOR_FORMAT = 174
IS_INVALID_WB_BINNING_MODE = 175
IS_INVALID_I2C_DEVICE_ADDRESS = 176
IS_COULD_NOT_CONVERT = 177
IS_TRANSFER_ERROR = 178
IS_PARAMETER_SET_NOT_PRESENT = 179
IS_INVALID_CAMERA_TYPE = 180
IS_INVALID_HOST_IP_HIBYTE = 181
IS_CM_NOT_SUPP_IN_CURR_DISPLAYMODE = 182
IS_NO_IR_FILTER = 183
IS_STARTER_FW_UPLOAD_NEEDED = 184
IS_DR_LIBRARY_NOT_FOUND = 185
IS_DR_DEVICE_OUT_OF_MEMORY = 186
IS_DR_CANNOT_CREATE_SURFACE = 187
IS_DR_CANNOT_CREATE_VERTEX_BUFFER = 188
IS_DR_CANNOT_CREATE_TEXTURE = 189
IS_DR_CANNOT_LOCK_OVERLAY_SURFACE = 190
IS_DR_CANNOT_UNLOCK_OVERLAY_SURFACE = 191
IS_DR_CANNOT_GET_OVERLAY_DC = 192
IS_DR_CANNOT_RELEASE_OVERLAY_DC = 193
IS_DR_DEVICE_CAPS_INSUFFICIENT = 194
IS_INCOMPATIBLE_SETTING = 195
IS_DR_NOT_ALLOWED_WHILE_DC_IS_ACTIVE = 196
IS_DEVICE_ALREADY_PAIRED = 197
IS_SUBNETMASK_MISMATCH = 198
IS_SUBNET_MISMATCH = 199
IS_INVALID_IP_CONFIGURATION = 200
IS_DEVICE_NOT_COMPATIBLE = 201
IS_NETWORK_FRAME_SIZE_INCOMPATIBLE = 202
IS_NETWORK_CONFIGURATION_INVALID = 203
IS_ERROR_CPU_IDLE_STATES_CONFIGURATION = 204
IS_DEVICE_BUSY = 205
IS_SENSOR_INITIALIZATION_FAILED = 206
IS_IMAGE_BUFFER_NOT_DWORD_ALIGNED = 207
IS_OFF = 0
IS_ON = 1
IS_IGNORE_PARAMETER = -1
IS_USE_DEVICE_ID = 0x8000
IS_ALLOW_STARTER_FW_UPLOAD = 0x10000
IS_GET_AUTO_EXIT_ENABLED = 0x8000
IS_DISABLE_AUTO_EXIT = 0
IS_ENABLE_AUTO_EXIT = 1
IS_GET_LIVE = 0x8000
IS_WAIT = 0x0001
IS_DONT_WAIT = 0x0000
IS_FORCE_VIDEO_STOP = 0x4000
IS_FORCE_VIDEO_START = 0x4000
IS_USE_NEXT_MEM = 0x8000
IS_VIDEO_NOT_FINISH = 0
IS_VIDEO_FINISH = 1
IS_GET_RENDER_MODE = 0x8000
IS_RENDER_DISABLED = 0x0000
IS_RENDER_NORMAL = 0x0001
IS_RENDER_FIT_TO_WINDOW = 0x0002
IS_RENDER_DOWNSCALE_1_2 = 0x0004
IS_RENDER_MIRROR_UPDOWN = 0x0010
IS_RENDER_PLANAR_COLOR_RED = 0x0080
IS_RENDER_PLANAR_COLOR_GREEN = 0x0100
IS_RENDER_PLANAR_COLOR_BLUE = 0x0200
IS_RENDER_PLANAR_MONO_RED = 0x0400
IS_RENDER_PLANAR_MONO_GREEN = 0x0800
IS_RENDER_PLANAR_MONO_BLUE = 0x1000
IS_RENDER_ROTATE_90 = 0x0020
IS_RENDER_ROTATE_180 = 0x0040
IS_RENDER_ROTATE_270 = 0x2000
IS_USE_AS_DC_STRUCTURE = 0x4000
IS_USE_AS_DC_HANDLE = 0x8000
IS_GET_EXTERNALTRIGGER = 0x8000
IS_GET_TRIGGER_STATUS = 0x8001
IS_GET_TRIGGER_MASK = 0x8002
IS_GET_TRIGGER_INPUTS = 0x8003
IS_GET_SUPPORTED_TRIGGER_MODE = 0x8004
IS_GET_TRIGGER_COUNTER = 0x8000
IS_SET_TRIGGER_MASK = 0x0100
IS_SET_TRIGGER_CONTINUOUS = 0x1000
IS_SET_TRIGGER_OFF = 0x0000
IS_SET_TRIGGER_HI_LO = (IS_SET_TRIGGER_CONTINUOUS|0x0001)
IS_SET_TRIGGER_LO_HI = (IS_SET_TRIGGER_CONTINUOUS|0x0002)
IS_SET_TRIGGER_SOFTWARE = (IS_SET_TRIGGER_CONTINUOUS|0x0008)
IS_SET_TRIGGER_HI_LO_SYNC = 0x0010
IS_SET_TRIGGER_LO_HI_SYNC = 0x0020
IS_SET_TRIGGER_PRE_HI_LO = (IS_SET_TRIGGER_CONTINUOUS|0x0040)
IS_SET_TRIGGER_PRE_LO_HI = (IS_SET_TRIGGER_CONTINUOUS|0x0080)
IS_GET_TRIGGER_DELAY = 0x8000
IS_GET_MIN_TRIGGER_DELAY = 0x8001
IS_GET_MAX_TRIGGER_DELAY = 0x8002
IS_GET_TRIGGER_DELAY_GRANULARITY = 0x8003
IS_GET_PIXEL_CLOCK = 0x8000
IS_GET_DEFAULT_PIXEL_CLK = 0x8001
IS_GET_PIXEL_CLOCK_INC = 0x8005
IS_GET_FRAMERATE = 0x8000
IS_GET_DEFAULT_FRAMERATE = 0x8001
IS_GET_MASTER_GAIN = 0x8000
IS_GET_RED_GAIN = 0x8001
IS_GET_GREEN_GAIN = 0x8002
IS_GET_BLUE_GAIN = 0x8003
IS_GET_DEFAULT_MASTER = 0x8004
IS_GET_DEFAULT_RED = 0x8005
IS_GET_DEFAULT_GREEN = 0x8006
IS_GET_DEFAULT_BLUE = 0x8007
IS_GET_GAINBOOST = 0x8008
IS_SET_GAINBOOST_ON = 0x0001
IS_SET_GAINBOOST_OFF = 0x0000
IS_GET_SUPPORTED_GAINBOOST = 0x0002
IS_MIN_GAIN = 0
IS_MAX_GAIN = 100
IS_GET_MASTER_GAIN_FACTOR = 0x8000
IS_GET_RED_GAIN_FACTOR = 0x8001
IS_GET_GREEN_GAIN_FACTOR = 0x8002
IS_GET_BLUE_GAIN_FACTOR = 0x8003
IS_SET_MASTER_GAIN_FACTOR = 0x8004
IS_SET_RED_GAIN_FACTOR = 0x8005
IS_SET_GREEN_GAIN_FACTOR = 0x8006
IS_SET_BLUE_GAIN_FACTOR = 0x8007
IS_GET_DEFAULT_MASTER_GAIN_FACTOR = 0x8008
IS_GET_DEFAULT_RED_GAIN_FACTOR = 0x8009
IS_GET_DEFAULT_GREEN_GAIN_FACTOR = 0x800a
IS_GET_DEFAULT_BLUE_GAIN_FACTOR = 0x800b
IS_INQUIRE_MASTER_GAIN_FACTOR = 0x800c
IS_INQUIRE_RED_GAIN_FACTOR = 0x800d
IS_INQUIRE_GREEN_GAIN_FACTOR = 0x800e
IS_INQUIRE_BLUE_GAIN_FACTOR = 0x800f
IS_SET_GLOBAL_SHUTTER_ON = 0x0001
IS_SET_GLOBAL_SHUTTER_OFF = 0x0000
IS_GET_GLOBAL_SHUTTER = 0x0010
IS_GET_SUPPORTED_GLOBAL_SHUTTER = 0x0020
IS_GET_BL_COMPENSATION = 0x8000
IS_GET_BL_OFFSET = 0x8001
IS_GET_BL_DEFAULT_MODE = 0x8002
IS_GET_BL_DEFAULT_OFFSET = 0x8003
IS_GET_BL_SUPPORTED_MODE = 0x8004
IS_BL_COMPENSATION_DISABLE = 0
IS_BL_COMPENSATION_ENABLE = 1
IS_BL_COMPENSATION_OFFSET = 32
IS_MIN_BL_OFFSET = 0
IS_MAX_BL_OFFSET = 255
IS_GET_HW_GAMMA = 0x8000
IS_GET_HW_SUPPORTED_GAMMA = 0x8001
IS_SET_HW_GAMMA_OFF = 0x0000
IS_SET_HW_GAMMA_ON = 0x0001
IS_GET_SATURATION_U = 0x8000
IS_MIN_SATURATION_U = 0
IS_MAX_SATURATION_U = 200
IS_DEFAULT_SATURATION_U = 100
IS_GET_SATURATION_V = 0x8001
IS_MIN_SATURATION_V = 0
IS_MAX_SATURATION_V = 200
IS_DEFAULT_SATURATION_V = 100
IS_AOI_IMAGE_SET_AOI = 0x0001
IS_AOI_IMAGE_GET_AOI = 0x0002
IS_AOI_IMAGE_SET_POS = 0x0003
IS_AOI_IMAGE_GET_POS = 0x0004
IS_AOI_IMAGE_SET_SIZE = 0x0005
IS_AOI_IMAGE_GET_SIZE = 0x0006
IS_AOI_IMAGE_GET_POS_MIN = 0x0007
IS_AOI_IMAGE_GET_SIZE_MIN = 0x0008
IS_AOI_IMAGE_GET_POS_MAX = 0x0009
IS_AOI_IMAGE_GET_SIZE_MAX = 0x0010
IS_AOI_IMAGE_GET_POS_INC = 0x0011
IS_AOI_IMAGE_GET_SIZE_INC = 0x0012
IS_AOI_IMAGE_GET_POS_X_ABS = 0x0013
IS_AOI_IMAGE_GET_POS_Y_ABS = 0x0014
IS_AOI_IMAGE_GET_ORIGINAL_AOI = 0x0015
IS_AOI_IMAGE_POS_ABSOLUTE = 0x10000000
IS_AOI_IMAGE_SET_POS_FAST = 0x0020
IS_AOI_IMAGE_GET_POS_FAST_SUPPORTED = 0x0021
IS_AOI_AUTO_BRIGHTNESS_SET_AOI = 0x0030
IS_AOI_AUTO_BRIGHTNESS_GET_AOI = 0x0031
IS_AOI_AUTO_WHITEBALANCE_SET_AOI = 0x0032
IS_AOI_AUTO_WHITEBALANCE_GET_AOI = 0x0033
IS_AOI_MULTI_GET_SUPPORTED_MODES = 0x0100
IS_AOI_MULTI_SET_AOI = 0x0200
IS_AOI_MULTI_GET_AOI = 0x0400
IS_AOI_MULTI_DISABLE_AOI = 0x0800
IS_AOI_MULTI_MODE_X_Y_AXES = 0x0001
IS_AOI_MULTI_MODE_Y_AXES = 0x0002
IS_AOI_MULTI_MODE_GET_MAX_NUMBER = 0x0003
IS_AOI_MULTI_MODE_GET_DEFAULT = 0x0004
IS_AOI_MULTI_MODE_ONLY_VERIFY_AOIS = 0x0005
IS_AOI_MULTI_MODE_GET_MINIMUM_SIZE = 0x0006
IS_AOI_MULTI_MODE_GET_ENABLED = 0x0007
IS_AOI_MULTI_STATUS_SETBYUSER = 0x00000001
IS_AOI_MULTI_STATUS_COMPLEMENT = 0x00000002
IS_AOI_MULTI_STATUS_VALID = 0x00000004
IS_AOI_MULTI_STATUS_CONFLICT = 0x00000008
IS_AOI_MULTI_STATUS_ERROR = 0x00000010
IS_AOI_MULTI_STATUS_UNUSED = 0x00000020
IS_AOI_SEQUENCE_GET_SUPPORTED = 0x0050
IS_AOI_SEQUENCE_SET_PARAMS = 0x0051
IS_AOI_SEQUENCE_GET_PARAMS = 0x0052
IS_AOI_SEQUENCE_SET_ENABLE = 0x0053
IS_AOI_SEQUENCE_GET_ENABLE = 0x0054
IS_AOI_SEQUENCE_INDEX_AOI_1 = 0
IS_AOI_SEQUENCE_INDEX_AOI_2 = 1
IS_AOI_SEQUENCE_INDEX_AOI_3 = 2
IS_AOI_SEQUENCE_INDEX_AOI_4 = 4
IS_GET_ROP_EFFECT = 0x8000
IS_GET_SUPPORTED_ROP_EFFECT = 0x8001
IS_SET_ROP_NONE = 0
IS_SET_ROP_MIRROR_UPDOWN = 8
IS_SET_ROP_MIRROR_UPDOWN_ODD = 16
IS_SET_ROP_MIRROR_UPDOWN_EVEN = 32
IS_SET_ROP_MIRROR_LEFTRIGHT = 64
IS_GET_SUBSAMPLING = 0x8000
IS_GET_SUPPORTED_SUBSAMPLING = 0x8001
IS_GET_SUBSAMPLING_TYPE = 0x8002
IS_GET_SUBSAMPLING_FACTOR_HORIZONTAL = 0x8004
IS_GET_SUBSAMPLING_FACTOR_VERTICAL = 0x8008
IS_SUBSAMPLING_DISABLE = 0x00
IS_SUBSAMPLING_2X_VERTICAL = 0x0001
IS_SUBSAMPLING_2X_HORIZONTAL = 0x0002
IS_SUBSAMPLING_4X_VERTICAL = 0x0004
IS_SUBSAMPLING_4X_HORIZONTAL = 0x0008
IS_SUBSAMPLING_3X_VERTICAL = 0x0010
IS_SUBSAMPLING_3X_HORIZONTAL = 0x0020
IS_SUBSAMPLING_5X_VERTICAL = 0x0040
IS_SUBSAMPLING_5X_HORIZONTAL = 0x0080
IS_SUBSAMPLING_6X_VERTICAL = 0x0100
IS_SUBSAMPLING_6X_HORIZONTAL = 0x0200
IS_SUBSAMPLING_8X_VERTICAL = 0x0400
IS_SUBSAMPLING_8X_HORIZONTAL = 0x0800
IS_SUBSAMPLING_16X_VERTICAL = 0x1000
IS_SUBSAMPLING_16X_HORIZONTAL = 0x2000
IS_SUBSAMPLING_COLOR = 0x01
IS_SUBSAMPLING_MONO = 0x02
IS_SUBSAMPLING_MASK_VERTICAL = (IS_SUBSAMPLING_2X_VERTICAL|IS_SUBSAMPLING_4X_VERTICAL|IS_SUBSAMPLING_3X_VERTICAL|IS_SUBSAMPLING_5X_VERTICAL|IS_SUBSAMPLING_6X_VERTICAL|IS_SUBSAMPLING_8X_VERTICAL|IS_SUBSAMPLING_16X_VERTICAL)
IS_SUBSAMPLING_MASK_HORIZONTAL = (IS_SUBSAMPLING_2X_HORIZONTAL|IS_SUBSAMPLING_4X_HORIZONTAL|IS_SUBSAMPLING_3X_HORIZONTAL|IS_SUBSAMPLING_5X_HORIZONTAL|IS_SUBSAMPLING_6X_HORIZONTAL|IS_SUBSAMPLING_8X_HORIZONTAL|IS_SUBSAMPLING_16X_HORIZONTAL)
IS_GET_BINNING = 0x8000
IS_GET_SUPPORTED_BINNING = 0x8001
IS_GET_BINNING_TYPE = 0x8002
IS_GET_BINNING_FACTOR_HORIZONTAL = 0x8004
IS_GET_BINNING_FACTOR_VERTICAL = 0x8008
IS_BINNING_DISABLE = 0x00
IS_BINNING_2X_VERTICAL = 0x0001
IS_BINNING_2X_HORIZONTAL = 0x0002
IS_BINNING_4X_VERTICAL = 0x0004
IS_BINNING_4X_HORIZONTAL = 0x0008
IS_BINNING_3X_VERTICAL = 0x0010
IS_BINNING_3X_HORIZONTAL = 0x0020
IS_BINNING_5X_VERTICAL = 0x0040
IS_BINNING_5X_HORIZONTAL = 0x0080
IS_BINNING_6X_VERTICAL = 0x0100
IS_BINNING_6X_HORIZONTAL = 0x0200
IS_BINNING_8X_VERTICAL = 0x0400
IS_BINNING_8X_HORIZONTAL = 0x0800
IS_BINNING_16X_VERTICAL = 0x1000
IS_BINNING_16X_HORIZONTAL = 0x2000
IS_BINNING_COLOR = 0x01
IS_BINNING_MONO = 0x02
IS_BINNING_MASK_VERTICAL = (IS_BINNING_2X_VERTICAL|IS_BINNING_3X_VERTICAL|IS_BINNING_4X_VERTICAL|IS_BINNING_5X_VERTICAL|IS_BINNING_6X_VERTICAL|IS_BINNING_8X_VERTICAL|IS_BINNING_16X_VERTICAL)
IS_BINNING_MASK_HORIZONTAL = (IS_BINNING_2X_HORIZONTAL|IS_BINNING_3X_HORIZONTAL|IS_BINNING_4X_HORIZONTAL|IS_BINNING_5X_HORIZONTAL|IS_BINNING_6X_HORIZONTAL|IS_BINNING_8X_HORIZONTAL|IS_BINNING_16X_HORIZONTAL)
IS_SET_ENABLE_AUTO_GAIN = 0x8800
IS_GET_ENABLE_AUTO_GAIN = 0x8801
IS_SET_ENABLE_AUTO_SHUTTER = 0x8802
IS_GET_ENABLE_AUTO_SHUTTER = 0x8803
IS_SET_ENABLE_AUTO_WHITEBALANCE = 0x8804
IS_GET_ENABLE_AUTO_WHITEBALANCE = 0x8805
IS_SET_ENABLE_AUTO_FRAMERATE = 0x8806
IS_GET_ENABLE_AUTO_FRAMERATE = 0x8807
IS_SET_ENABLE_AUTO_SENSOR_GAIN = 0x8808
IS_GET_ENABLE_AUTO_SENSOR_GAIN = 0x8809
IS_SET_ENABLE_AUTO_SENSOR_SHUTTER = 0x8810
IS_GET_ENABLE_AUTO_SENSOR_SHUTTER = 0x8811
IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER = 0x8812
IS_GET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER = 0x8813
IS_SET_ENABLE_AUTO_SENSOR_FRAMERATE = 0x8814
IS_GET_ENABLE_AUTO_SENSOR_FRAMERATE = 0x8815
IS_SET_ENABLE_AUTO_SENSOR_WHITEBALANCE = 0x8816
IS_GET_ENABLE_AUTO_SENSOR_WHITEBALANCE = 0x8817
IS_SET_AUTO_REFERENCE = 0x8000
IS_GET_AUTO_REFERENCE = 0x8001
IS_SET_AUTO_GAIN_MAX = 0x8002
IS_GET_AUTO_GAIN_MAX = 0x8003
IS_SET_AUTO_SHUTTER_MAX = 0x8004
IS_GET_AUTO_SHUTTER_MAX = 0x8005
IS_SET_AUTO_SPEED = 0x8006
IS_GET_AUTO_SPEED = 0x8007
IS_SET_AUTO_WB_OFFSET = 0x8008
IS_GET_AUTO_WB_OFFSET = 0x8009
IS_SET_AUTO_WB_GAIN_RANGE = 0x800A
IS_GET_AUTO_WB_GAIN_RANGE = 0x800B
IS_SET_AUTO_WB_SPEED = 0x800C
IS_GET_AUTO_WB_SPEED = 0x800D
IS_SET_AUTO_WB_ONCE = 0x800E
IS_GET_AUTO_WB_ONCE = 0x800F
IS_SET_AUTO_BRIGHTNESS_ONCE = 0x8010
IS_GET_AUTO_BRIGHTNESS_ONCE = 0x8011
IS_SET_AUTO_HYSTERESIS = 0x8012
IS_GET_AUTO_HYSTERESIS = 0x8013
IS_GET_AUTO_HYSTERESIS_RANGE = 0x8014
IS_SET_AUTO_WB_HYSTERESIS = 0x8015
IS_GET_AUTO_WB_HYSTERESIS = 0x8016
IS_GET_AUTO_WB_HYSTERESIS_RANGE = 0x8017
IS_SET_AUTO_SKIPFRAMES = 0x8018
IS_GET_AUTO_SKIPFRAMES = 0x8019
IS_GET_AUTO_SKIPFRAMES_RANGE = 0x801A
IS_SET_AUTO_WB_SKIPFRAMES = 0x801B
IS_GET_AUTO_WB_SKIPFRAMES = 0x801C
IS_GET_AUTO_WB_SKIPFRAMES_RANGE = 0x801D
IS_SET_SENS_AUTO_SHUTTER_PHOTOM = 0x801E
IS_SET_SENS_AUTO_GAIN_PHOTOM = 0x801F
IS_GET_SENS_AUTO_SHUTTER_PHOTOM = 0x8020
IS_GET_SENS_AUTO_GAIN_PHOTOM = 0x8021
IS_GET_SENS_AUTO_SHUTTER_PHOTOM_DEF = 0x8022
IS_GET_SENS_AUTO_GAIN_PHOTOM_DEF = 0x8023
IS_SET_SENS_AUTO_CONTRAST_CORRECTION = 0x8024
IS_GET_SENS_AUTO_CONTRAST_CORRECTION = 0x8025
IS_GET_SENS_AUTO_CONTRAST_CORRECTION_RANGE = 0x8026
IS_GET_SENS_AUTO_CONTRAST_CORRECTION_INC = 0x8027
IS_GET_SENS_AUTO_CONTRAST_CORRECTION_DEF = 0x8028
IS_SET_SENS_AUTO_CONTRAST_FDT_AOI_ENABLE = 0x8029
IS_GET_SENS_AUTO_CONTRAST_FDT_AOI_ENABLE = 0x8030
IS_SET_SENS_AUTO_BACKLIGHT_COMP = 0x8031
IS_GET_SENS_AUTO_BACKLIGHT_COMP = 0x8032
IS_GET_SENS_AUTO_BACKLIGHT_COMP_RANGE = 0x8033
IS_GET_SENS_AUTO_BACKLIGHT_COMP_INC = 0x8034
IS_GET_SENS_AUTO_BACKLIGHT_COMP_DEF = 0x8035
IS_SET_ANTI_FLICKER_MODE = 0x8036
IS_GET_ANTI_FLICKER_MODE = 0x8037
IS_GET_ANTI_FLICKER_MODE_DEF = 0x8038
IS_GET_AUTO_REFERENCE_DEF = 0x8039
IS_GET_AUTO_WB_OFFSET_DEF = 0x803A
IS_GET_AUTO_WB_OFFSET_MIN = 0x803B
IS_GET_AUTO_WB_OFFSET_MAX = 0x803C
IS_MIN_AUTO_BRIGHT_REFERENCE = 0
IS_MAX_AUTO_BRIGHT_REFERENCE = 255
IS_DEFAULT_AUTO_BRIGHT_REFERENCE = 128
IS_MIN_AUTO_SPEED = 0
IS_MAX_AUTO_SPEED = 100
IS_DEFAULT_AUTO_SPEED = 50
IS_DEFAULT_AUTO_WB_OFFSET = 0
IS_MIN_AUTO_WB_OFFSET = -50
IS_MAX_AUTO_WB_OFFSET = 50
IS_DEFAULT_AUTO_WB_SPEED = 50
IS_MIN_AUTO_WB_SPEED = 0
IS_MAX_AUTO_WB_SPEED = 100
IS_MIN_AUTO_WB_REFERENCE = 0
IS_MAX_AUTO_WB_REFERENCE = 255
IS_SET_AUTO_BRIGHT_AOI = 0x8000
IS_GET_AUTO_BRIGHT_AOI = 0x8001
IS_SET_IMAGE_AOI = 0x8002
IS_GET_IMAGE_AOI = 0x8003
IS_SET_AUTO_WB_AOI = 0x8004
IS_GET_AUTO_WB_AOI = 0x8005
IS_GET_COLOR_MODE = 0x8000
IS_CM_FORMAT_PLANAR = 0x2000
IS_CM_FORMAT_MASK = 0x2000
IS_CM_ORDER_BGR = 0x0000
IS_CM_ORDER_RGB = 0x0080
IS_CM_ORDER_MASK = 0x0080
IS_CM_PREFER_PACKED_SOURCE_FORMAT = 0x4000
IS_CM_SENSOR_RAW8 = 11
IS_CM_SENSOR_RAW10 = 33
IS_CM_SENSOR_RAW12 = 27
IS_CM_SENSOR_RAW16 = 29
IS_CM_MONO8 = 6
IS_CM_MONO10 = 34
IS_CM_MONO12 = 26
IS_CM_MONO16 = 28
IS_CM_BGR5_PACKED = (3|IS_CM_ORDER_BGR)
IS_CM_BGR565_PACKED = (2|IS_CM_ORDER_BGR)
IS_CM_RGB8_PACKED = (1|IS_CM_ORDER_RGB)
IS_CM_BGR8_PACKED = (1|IS_CM_ORDER_BGR)
IS_CM_RGBA8_PACKED = (0|IS_CM_ORDER_RGB)
IS_CM_BGRA8_PACKED = (0|IS_CM_ORDER_BGR)
IS_CM_RGBY8_PACKED = (24|IS_CM_ORDER_RGB)
IS_CM_BGRY8_PACKED = (24|IS_CM_ORDER_BGR)
IS_CM_RGB10_PACKED = (25|IS_CM_ORDER_RGB)
IS_CM_BGR10_PACKED = (25|IS_CM_ORDER_BGR)
IS_CM_RGB10_UNPACKED = (35|IS_CM_ORDER_RGB)
IS_CM_BGR10_UNPACKED = (35|IS_CM_ORDER_BGR)
IS_CM_RGB12_UNPACKED = (30|IS_CM_ORDER_RGB)
IS_CM_BGR12_UNPACKED = (30|IS_CM_ORDER_BGR)
IS_CM_RGBA12_UNPACKED = (31|IS_CM_ORDER_RGB)
IS_CM_BGRA12_UNPACKED = (31|IS_CM_ORDER_BGR)
IS_CM_JPEG = 32
IS_CM_UYVY_PACKED = 12
IS_CM_UYVY_MONO_PACKED = 13
IS_CM_UYVY_BAYER_PACKED = 14
IS_CM_CBYCRY_PACKED = 23
IS_CM_RGB8_PLANAR = (1|IS_CM_ORDER_RGB|IS_CM_FORMAT_PLANAR)
IS_CM_ALL_POSSIBLE = 0xFFFF
IS_CM_MODE_MASK = 0x007F
IS_HOTPIXEL_DISABLE_CORRECTION = 0x0000
IS_HOTPIXEL_ENABLE_SENSOR_CORRECTION = 0x0001
IS_HOTPIXEL_ENABLE_CAMERA_CORRECTION = 0x0002
IS_HOTPIXEL_ENABLE_SOFTWARE_USER_CORRECTION = 0x0004
IS_HOTPIXEL_DISABLE_SENSOR_CORRECTION = 0x0008
IS_HOTPIXEL_GET_CORRECTION_MODE = 0x8000
IS_HOTPIXEL_GET_SUPPORTED_CORRECTION_MODES = 0x8001
IS_HOTPIXEL_GET_SOFTWARE_USER_LIST_EXISTS = 0x8100
IS_HOTPIXEL_GET_SOFTWARE_USER_LIST_NUMBER = 0x8101
IS_HOTPIXEL_GET_SOFTWARE_USER_LIST = 0x8102
IS_HOTPIXEL_SET_SOFTWARE_USER_LIST = 0x8103
IS_HOTPIXEL_SAVE_SOFTWARE_USER_LIST = 0x8104
IS_HOTPIXEL_LOAD_SOFTWARE_USER_LIST = 0x8105
IS_HOTPIXEL_GET_CAMERA_FACTORY_LIST_EXISTS = 0x8106
IS_HOTPIXEL_GET_CAMERA_FACTORY_LIST_NUMBER = 0x8107
IS_HOTPIXEL_GET_CAMERA_FACTORY_LIST = 0x8108
IS_HOTPIXEL_GET_CAMERA_USER_LIST_EXISTS = 0x8109
IS_HOTPIXEL_GET_CAMERA_USER_LIST_NUMBER = 0x810A
IS_HOTPIXEL_GET_CAMERA_USER_LIST = 0x810B
IS_HOTPIXEL_SET_CAMERA_USER_LIST = 0x810C
IS_HOTPIXEL_GET_CAMERA_USER_LIST_MAX_NUMBER = 0x810D
IS_HOTPIXEL_DELETE_CAMERA_USER_LIST = 0x810E
IS_HOTPIXEL_GET_MERGED_CAMERA_LIST_NUMBER = 0x810F
IS_HOTPIXEL_GET_MERGED_CAMERA_LIST = 0x8110
IS_HOTPIXEL_SAVE_SOFTWARE_USER_LIST_UNICODE = 0x8111
IS_HOTPIXEL_LOAD_SOFTWARE_USER_LIST_UNICODE = 0x8112
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_ENABLE = 0x8113
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_ENABLE_DEFAULT = 0x8114
IS_HOTPIXEL_ADAPTIVE_CORRECTION_SET_ENABLE = 0x8115
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_MODE = 0x8116
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_MODE_DEFAULT = 0x8117
IS_HOTPIXEL_ADAPTIVE_CORRECTION_SET_MODE = 0x8118
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_SENSITIVITY = 0x8119
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_SENSITIVITY_DEFAULT = 0x8120
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_SENSITIVITY_MIN = 0x8121
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_SENSITIVITY_MAX = 0x8122
IS_HOTPIXEL_ADAPTIVE_CORRECTION_SET_SENSITIVITY = 0x8123
IS_HOTPIXEL_ADAPTIVE_CORRECTION_RESET_DETECTION = 0x8124
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_NUMBER_DETECTED = 0x8125
IS_HOTPIXEL_ADAPTIVE_CORRECTION_RESET_DETECTION_CLUSTER = 0x8126
IS_HOTPIXEL_ADAPTIVE_CORRECTION_GET_NUMBER_DETECTED_CLUSTER = 0x8127
IS_HOTPIXEL_ADAPTIVE_CORRECTION_DISABLE = 0
IS_HOTPIXEL_ADAPTIVE_CORRECTION_ENABLE = 1
IS_HOTPIXEL_ADAPTIVE_CORRECTION_DETECT_ONCE = 0x0000
IS_HOTPIXEL_ADAPTIVE_CORRECTION_DETECT_DYNAMIC = 0x0001
IS_HOTPIXEL_ADAPTIVE_CORRECTION_DETECT_ONCE_CLUSTER = 0x0002
IS_HOTPIXEL_ADAPTIVE_CORRECTION_DETECT_DYNAMIC_CLUSTER = 0x0004
IS_GET_CCOR_MODE = 0x8000
IS_GET_SUPPORTED_CCOR_MODE = 0x8001
IS_GET_DEFAULT_CCOR_MODE = 0x8002
IS_GET_CCOR_FACTOR = 0x8003
IS_GET_CCOR_FACTOR_MIN = 0x8004
IS_GET_CCOR_FACTOR_MAX = 0x8005
IS_GET_CCOR_FACTOR_DEFAULT = 0x8006
IS_CCOR_DISABLE = 0x0000
IS_CCOR_ENABLE = 0x0001
IS_CCOR_ENABLE_NORMAL = IS_CCOR_ENABLE
IS_CCOR_ENABLE_BG40_ENHANCED = 0x0002
IS_CCOR_ENABLE_HQ_ENHANCED = 0x0004
IS_CCOR_SET_IR_AUTOMATIC = 0x0080
IS_CCOR_FACTOR = 0x0100
IS_CCOR_ENABLE_MASK = (IS_CCOR_ENABLE_NORMAL|IS_CCOR_ENABLE_BG40_ENHANCED|IS_CCOR_ENABLE_HQ_ENHANCED)
IS_GET_BAYER_CV_MODE = 0x8000
IS_SET_BAYER_CV_NORMAL = 0x0000
IS_SET_BAYER_CV_BETTER = 0x0001
IS_SET_BAYER_CV_BEST = 0x0002
IS_CONV_MODE_NONE = 0x0000
IS_CONV_MODE_SOFTWARE = 0x0001
IS_CONV_MODE_SOFTWARE_3X3 = 0x0002
IS_CONV_MODE_SOFTWARE_5X5 = 0x0004
IS_CONV_MODE_HARDWARE_3X3 = 0x0008
IS_CONV_MODE_OPENCL_3X3 = 0x0020
IS_CONV_MODE_OPENCL_5X5 = 0x0040
IS_CONV_MODE_JPEG = 0x0100
IS_GET_EDGE_ENHANCEMENT = 0x8000
IS_EDGE_EN_DISABLE = 0
IS_EDGE_EN_STRONG = 1
IS_EDGE_EN_WEAK = 2
IS_GET_WB_MODE = 0x8000
IS_SET_WB_DISABLE = 0x0000
IS_SET_WB_USER = 0x0001
IS_SET_WB_AUTO_ENABLE = 0x0002
IS_SET_WB_AUTO_ENABLE_ONCE = 0x0004
IS_SET_WB_DAYLIGHT_65 = 0x0101
IS_SET_WB_COOL_WHITE = 0x0102
IS_SET_WB_U30 = 0x0103
IS_SET_WB_ILLUMINANT_A = 0x0104
IS_SET_WB_HORIZON = 0x0105
IS_EEPROM_MIN_USER_ADDRESS = 0
IS_EEPROM_MAX_USER_ADDRESS = 63
IS_EEPROM_MAX_USER_SPACE = 64
IS_GET_ERR_REP_MODE = 0x8000
IS_ENABLE_ERR_REP = 1
IS_DISABLE_ERR_REP = 0
IS_GET_DISPLAY_MODE = 0x8000
IS_SET_DM_DIB = 1
IS_SET_DM_DIRECT3D = 4
IS_SET_DM_OPENGL = 8
IS_SET_DM_MONO = 0x800
IS_SET_DM_BAYER = 0x1000
IS_SET_DM_YCBCR = 0x4000
DR_GET_OVERLAY_DC = 1
DR_GET_MAX_OVERLAY_SIZE = 2
DR_GET_OVERLAY_KEY_COLOR = 3
DR_RELEASE_OVERLAY_DC = 4
DR_SHOW_OVERLAY = 5
DR_HIDE_OVERLAY = 6
DR_SET_OVERLAY_SIZE = 7
DR_SET_OVERLAY_POSITION = 8
DR_SET_OVERLAY_KEY_COLOR = 9
DR_SET_HWND = 10
DR_ENABLE_SCALING = 11
DR_DISABLE_SCALING = 12
DR_CLEAR_OVERLAY = 13
DR_ENABLE_SEMI_TRANSPARENT_OVERLAY = 14
DR_DISABLE_SEMI_TRANSPARENT_OVERLAY = 15
DR_CHECK_COMPATIBILITY = 16
DR_SET_VSYNC_OFF = 17
DR_SET_VSYNC_AUTO = 18
DR_SET_USER_SYNC = 19
DR_GET_USER_SYNC_POSITION_RANGE = 20
DR_LOAD_OVERLAY_FROM_FILE = 21
DR_STEAL_NEXT_FRAME = 22
DR_SET_STEAL_FORMAT = 23
DR_GET_STEAL_FORMAT = 24
DR_ENABLE_IMAGE_SCALING = 25
DR_GET_OVERLAY_SIZE = 26
DR_CHECK_COLOR_MODE_SUPPORT = 27
DR_GET_OVERLAY_DATA = 28
DR_UPDATE_OVERLAY_DATA = 29
DR_GET_SUPPORTED = 30
IS_SAVE_USE_ACTUAL_IMAGE_SIZE = 0x00010000
IS_RENUM_BY_CAMERA = 0
IS_RENUM_BY_HOST = 1
IS_SET_EVENT_ODD = 0
IS_SET_EVENT_EVEN = 1
IS_SET_EVENT_FRAME = 2
IS_SET_EVENT_EXTTRIG = 3
IS_SET_EVENT_VSYNC = 4
IS_SET_EVENT_SEQ = 5
IS_SET_EVENT_STEAL = 6
IS_SET_EVENT_VPRES = 7
IS_SET_EVENT_CAPTURE_STATUS = 8
IS_SET_EVENT_TRANSFER_FAILED = IS_SET_EVENT_CAPTURE_STATUS
IS_SET_EVENT_DEVICE_RECONNECTED = 9
IS_SET_EVENT_MEMORY_MODE_FINISH = 10
IS_SET_EVENT_FRAME_RECEIVED = 11
IS_SET_EVENT_WB_FINISHED = 12
IS_SET_EVENT_AUTOBRIGHTNESS_FINISHED = 13
IS_SET_EVENT_OVERLAY_DATA_LOST = 16
IS_SET_EVENT_CAMERA_MEMORY = 17
IS_SET_EVENT_CONNECTIONSPEED_CHANGED = 18
IS_SET_EVENT_AUTOFOCUS_FINISHED = 19
IS_SET_EVENT_FIRST_PACKET_RECEIVED = 20
IS_SET_EVENT_PMC_IMAGE_PARAMS_CHANGED = 21
IS_SET_EVENT_DEVICE_PLUGGED_IN = 22
IS_SET_EVENT_DEVICE_UNPLUGGED = 23
IS_SET_EVENT_TEMPERATURE_STATUS = 24
IS_SET_EVENT_REMOVE = 128
IS_SET_EVENT_REMOVAL = 129
IS_SET_EVENT_NEW_DEVICE = 130
IS_SET_EVENT_STATUS_CHANGED = 131
IS_UEYE_MESSAGE = (0x400+0x0100)
IS_FRAME = 0x0000
IS_SEQUENCE = 0x0001
IS_TRIGGER = 0x0002
IS_CAPTURE_STATUS = 0x0003
IS_TRANSFER_FAILED = IS_CAPTURE_STATUS
IS_DEVICE_RECONNECTED = 0x0004
IS_MEMORY_MODE_FINISH = 0x0005
IS_FRAME_RECEIVED = 0x0006
IS_GENERIC_ERROR = 0x0007
IS_STEAL_VIDEO = 0x0008
IS_WB_FINISHED = 0x0009
IS_AUTOBRIGHTNESS_FINISHED = 0x000A
IS_OVERLAY_DATA_LOST = 0x000B
IS_CAMERA_MEMORY = 0x000C
IS_CONNECTIONSPEED_CHANGED = 0x000D
IS_AUTOFOCUS_FINISHED = 0x000E
IS_FIRST_PACKET_RECEIVED = 0x000F
IS_PMC_IMAGE_PARAMS_CHANGED = 0x0010
IS_DEVICE_PLUGGED_IN = 0x0011
IS_DEVICE_UNPLUGGED = 0x0012
IS_TEMPERATURE_STATUS = 0x0013
IS_DEVICE_REMOVED = 0x1000
IS_DEVICE_REMOVAL = 0x1001
IS_NEW_DEVICE = 0x1002
IS_DEVICE_STATUS_CHANGED = 0x1003
IS_GET_CAMERA_ID = 0x8000
IS_GET_STATUS = 0x8000
IS_EXT_TRIGGER_EVENT_CNT = 0
IS_FIFO_OVR_CNT = 1
IS_SEQUENCE_CNT = 2
IS_LAST_FRAME_FIFO_OVR = 3
IS_SEQUENCE_SIZE = 4
IS_VIDEO_PRESENT = 5
IS_STEAL_FINISHED = 6
IS_STORE_FILE_PATH = 7
IS_LUMA_BANDWIDTH_FILTER = 8
IS_BOARD_REVISION = 9
IS_MIRROR_BITMAP_UPDOWN = 10
IS_BUS_OVR_CNT = 11
IS_STEAL_ERROR_CNT = 12
IS_LOW_COLOR_REMOVAL = 13
IS_CHROMA_COMB_FILTER = 14
IS_CHROMA_AGC = 15
IS_WATCHDOG_ON_BOARD = 16
IS_PASSTHROUGH_ON_BOARD = 17
IS_EXTERNAL_VREF_MODE = 18
IS_WAIT_TIMEOUT = 19
IS_TRIGGER_MISSED = 20
IS_LAST_CAPTURE_ERROR = 21
IS_PARAMETER_SET_1 = 22
IS_PARAMETER_SET_2 = 23
IS_STANDBY = 24
IS_STANDBY_SUPPORTED = 25
IS_QUEUED_IMAGE_EVENT_CNT = 26
IS_PARAMETER_EXT = 27
IS_INTERFACE_TYPE_USB = 0x40
IS_INTERFACE_TYPE_USB3 = 0x60
IS_INTERFACE_TYPE_ETH = 0x80
IS_INTERFACE_TYPE_PMC = 0xf0
IS_BOARD_TYPE_UEYE_USB = (IS_INTERFACE_TYPE_USB+0)
IS_BOARD_TYPE_UEYE_USB_SE = IS_BOARD_TYPE_UEYE_USB
IS_BOARD_TYPE_UEYE_USB_RE = IS_BOARD_TYPE_UEYE_USB
IS_BOARD_TYPE_UEYE_USB_ME = (IS_INTERFACE_TYPE_USB+0x01)
IS_BOARD_TYPE_UEYE_USB_LE = (IS_INTERFACE_TYPE_USB+0x02)
IS_BOARD_TYPE_UEYE_USB_XS = (IS_INTERFACE_TYPE_USB+0x03)
IS_BOARD_TYPE_UEYE_USB_ML = (IS_INTERFACE_TYPE_USB+0x05)
IS_BOARD_TYPE_UEYE_USB3_SE = IS_INTERFACE_TYPE_USB3
IS_BOARD_TYPE_UEYE_USB3_LE = (IS_INTERFACE_TYPE_USB3+0x02)
IS_BOARD_TYPE_UEYE_USB3_XC = (IS_INTERFACE_TYPE_USB3+0x03)
IS_BOARD_TYPE_UEYE_USB3_CP = (IS_INTERFACE_TYPE_USB3+0x04)
IS_BOARD_TYPE_UEYE_USB3_ML = (IS_INTERFACE_TYPE_USB3+0x05)
IS_BOARD_TYPE_UEYE_ETH = IS_INTERFACE_TYPE_ETH
IS_BOARD_TYPE_UEYE_ETH_HE = IS_BOARD_TYPE_UEYE_ETH
IS_BOARD_TYPE_UEYE_ETH_SE = (IS_INTERFACE_TYPE_ETH+0x01)
IS_BOARD_TYPE_UEYE_ETH_RE = IS_BOARD_TYPE_UEYE_ETH_SE
IS_BOARD_TYPE_UEYE_ETH_LE = (IS_INTERFACE_TYPE_ETH+0x02)
IS_BOARD_TYPE_UEYE_ETH_CP = (IS_INTERFACE_TYPE_ETH+0x04)
IS_BOARD_TYPE_UEYE_ETH_SEP = (IS_INTERFACE_TYPE_ETH+0x06)
IS_BOARD_TYPE_UEYE_ETH_REP = IS_BOARD_TYPE_UEYE_ETH_SEP
IS_BOARD_TYPE_UEYE_ETH_LEET = (IS_INTERFACE_TYPE_ETH+0x07)
IS_BOARD_TYPE_UEYE_ETH_TE = (IS_INTERFACE_TYPE_ETH+0x08)
IS_BOARD_TYPE_UEYE_ETH_FA = (IS_INTERFACE_TYPE_ETH+0x0A)
IS_BOARD_TYPE_UEYE_ETH_SE_R4 = (IS_INTERFACE_TYPE_ETH+0x0B)
IS_BOARD_TYPE_UEYE_ETH_CP_R2 = (IS_INTERFACE_TYPE_ETH+0x0C)
IS_CAMERA_TYPE_UEYE_USB = IS_BOARD_TYPE_UEYE_USB_SE
IS_CAMERA_TYPE_UEYE_USB_SE = IS_BOARD_TYPE_UEYE_USB_SE
IS_CAMERA_TYPE_UEYE_USB_RE = IS_BOARD_TYPE_UEYE_USB_RE
IS_CAMERA_TYPE_UEYE_USB_ME = IS_BOARD_TYPE_UEYE_USB_ME
IS_CAMERA_TYPE_UEYE_USB_LE = IS_BOARD_TYPE_UEYE_USB_LE
IS_CAMERA_TYPE_UEYE_USB_ML = IS_BOARD_TYPE_UEYE_USB_ML
IS_CAMERA_TYPE_UEYE_USB3_LE = IS_BOARD_TYPE_UEYE_USB3_LE
IS_CAMERA_TYPE_UEYE_USB3_XC = IS_BOARD_TYPE_UEYE_USB3_XC
IS_CAMERA_TYPE_UEYE_USB3_CP = IS_BOARD_TYPE_UEYE_USB3_CP
IS_CAMERA_TYPE_UEYE_USB3_ML = IS_BOARD_TYPE_UEYE_USB3_ML
IS_CAMERA_TYPE_UEYE_ETH = IS_BOARD_TYPE_UEYE_ETH_HE
IS_CAMERA_TYPE_UEYE_ETH_HE = IS_BOARD_TYPE_UEYE_ETH_HE
IS_CAMERA_TYPE_UEYE_ETH_SE = IS_BOARD_TYPE_UEYE_ETH_SE
IS_CAMERA_TYPE_UEYE_ETH_RE = IS_BOARD_TYPE_UEYE_ETH_RE
IS_CAMERA_TYPE_UEYE_ETH_LE = IS_BOARD_TYPE_UEYE_ETH_LE
IS_CAMERA_TYPE_UEYE_ETH_CP = IS_BOARD_TYPE_UEYE_ETH_CP
IS_CAMERA_TYPE_UEYE_ETH_SEP = IS_BOARD_TYPE_UEYE_ETH_SEP
IS_CAMERA_TYPE_UEYE_ETH_REP = IS_BOARD_TYPE_UEYE_ETH_REP
IS_CAMERA_TYPE_UEYE_ETH_LEET = IS_BOARD_TYPE_UEYE_ETH_LEET
IS_CAMERA_TYPE_UEYE_ETH_TE = IS_BOARD_TYPE_UEYE_ETH_TE
IS_CAMERA_TYPE_UEYE_ETH_CP_R2 = IS_BOARD_TYPE_UEYE_ETH_CP_R2
IS_CAMERA_TYPE_UEYE_ETH_FA = IS_BOARD_TYPE_UEYE_ETH_FA
IS_CAMERA_TYPE_UEYE_ETH_SE_R4 = IS_BOARD_TYPE_UEYE_ETH_SE_R4
IS_CAMERA_TYPE_UEYE_PMC = (IS_INTERFACE_TYPE_PMC+0x01)
IS_OS_UNDETERMINED = 0
IS_OS_WIN95 = 1
IS_OS_WINNT40 = 2
IS_OS_WIN98 = 3
IS_OS_WIN2000 = 4
IS_OS_WINXP = 5
IS_OS_WINME = 6
IS_OS_WINNET = 7
IS_OS_WINSERVER2003 = 8
IS_OS_WINVISTA = 9
IS_OS_LINUX24 = 10
IS_OS_LINUX26 = 11
IS_OS_WIN7 = 12
IS_OS_WIN8 = 13
IS_OS_WIN8SERVER = 14
IS_OS_GREATER_THAN_WIN8 = 15
IS_USB_10 = 0x0001
IS_USB_11 = 0x0002
IS_USB_20 = 0x0004
IS_USB_30 = 0x0008
IS_ETHERNET_10 = 0x0080
IS_ETHERNET_100 = 0x0100
IS_ETHERNET_1000 = 0x0200
IS_ETHERNET_10000 = 0x0400
IS_USB_LOW_SPEED = 1
IS_USB_FULL_SPEED = 12
IS_USB_HIGH_SPEED = 480
IS_USB_SUPER_SPEED = 4000
IS_ETHERNET_10Base = 10
IS_ETHERNET_100Base = 100
IS_ETHERNET_1000Base = 1000
IS_ETHERNET_10GBase = 10000
IS_HDR_NOT_SUPPORTED = 0
IS_HDR_KNEEPOINTS = 1
IS_DISABLE_HDR = 0
IS_ENABLE_HDR = 1
IS_TEST_IMAGE_NONE = 0x00000000
IS_TEST_IMAGE_WHITE = 0x00000001
IS_TEST_IMAGE_BLACK = 0x00000002
IS_TEST_IMAGE_HORIZONTAL_GREYSCALE = 0x00000004
IS_TEST_IMAGE_VERTICAL_GREYSCALE = 0x00000008
IS_TEST_IMAGE_DIAGONAL_GREYSCALE = 0x00000010
IS_TEST_IMAGE_WEDGE_GRAY = 0x00000020
IS_TEST_IMAGE_WEDGE_COLOR = 0x00000040
IS_TEST_IMAGE_ANIMATED_WEDGE_GRAY = 0x00000080
IS_TEST_IMAGE_ANIMATED_WEDGE_COLOR = 0x00000100
IS_TEST_IMAGE_MONO_BARS = 0x00000200
IS_TEST_IMAGE_COLOR_BARS1 = 0x00000400
IS_TEST_IMAGE_COLOR_BARS2 = 0x00000800
IS_TEST_IMAGE_GREYSCALE1 = 0x00001000
IS_TEST_IMAGE_GREY_AND_COLOR_BARS = 0x00002000
IS_TEST_IMAGE_MOVING_GREY_AND_COLOR_BARS = 0x00004000
IS_TEST_IMAGE_ANIMATED_LINE = 0x00008000
IS_TEST_IMAGE_ALTERNATE_PATTERN = 0x00010000
IS_TEST_IMAGE_VARIABLE_GREY = 0x00020000
IS_TEST_IMAGE_MONOCHROME_HORIZONTAL_BARS = 0x00040000
IS_TEST_IMAGE_MONOCHROME_VERTICAL_BARS = 0x00080000
IS_TEST_IMAGE_CURSOR_H = 0x00100000
IS_TEST_IMAGE_CURSOR_V = 0x00200000
IS_TEST_IMAGE_COLDPIXEL_GRID = 0x00400000
IS_TEST_IMAGE_HOTPIXEL_GRID = 0x00800000
IS_TEST_IMAGE_VARIABLE_RED_PART = 0x01000000
IS_TEST_IMAGE_VARIABLE_GREEN_PART = 0x02000000
IS_TEST_IMAGE_VARIABLE_BLUE_PART = 0x04000000
IS_TEST_IMAGE_SHADING_IMAGE = 0x08000000
IS_TEST_IMAGE_WEDGE_GRAY_SENSOR = 0x10000000
IS_TEST_IMAGE_ANIMATED_WEDGE_GRAY_SENSOR = 0x20000000
IS_TEST_IMAGE_RAMPING_PATTERN = 0x40000000
IS_TEST_IMAGE_CHESS_PATTERN = 0x80000000
IS_DISABLE_SENSOR_SCALER = 0
IS_ENABLE_SENSOR_SCALER = 1
IS_ENABLE_ANTI_ALIASING = 2
IS_TRIGGER_TIMEOUT = 0
IS_BEST_PCLK_RUN_ONCE = 0
IS_LOCK_LAST_BUFFER = 0x8002
IS_GET_ALLOC_ID_OF_THIS_BUF = 0x8004
IS_GET_ALLOC_ID_OF_LAST_BUF = 0x8008
IS_USE_ALLOC_ID = 0x8000
IS_USE_CURRENT_IMG_SIZE = 0xC000
IS_GET_D3D_MEM = 0x8000
IS_IMG_BMP = 0
IS_IMG_JPG = 1
IS_IMG_PNG = 2
IS_IMG_RAW = 4
IS_IMG_TIF = 8
IS_I2C_16_BIT_REGISTER = 0x10000000
IS_I2C_0_BIT_REGISTER = 0x20000000
IS_I2C_DONT_WAIT = 0x00800000
IS_GET_GAMMA_MODE = 0x8000
IS_SET_GAMMA_OFF = 0
IS_SET_GAMMA_ON = 1
IS_GET_CAPTURE_MODE = 0x8000
IS_SET_CM_ODD = 0x0001
IS_SET_CM_EVEN = 0x0002
IS_SET_CM_FRAME = 0x0004
IS_SET_CM_NONINTERLACED = 0x0008
IS_SET_CM_NEXT_FRAME = 0x0010
IS_SET_CM_NEXT_FIELD = 0x0020
IS_SET_CM_BOTHFIELDS = (IS_SET_CM_ODD|IS_SET_CM_EVEN|IS_SET_CM_NONINTERLACED)
IS_SET_CM_FRAME_STEREO = 0x2004
WM_USER = 0x400
INFINITE = -1
IS_INVALID_HIDS = 0
IS_INVALID_HCAM = 0
IS_INVALID_HFALC = 0
CAMINFO = BOARDINFO
FIRMWARE_DOWNLOAD_NOT_SUPPORTED = 0x00000001
INTERFACE_SPEED_NOT_SUPPORTED = 0x00000002
INVALID_SENSOR_DETECTED = 0x00000004
AUTHORIZATION_FAILED = 0x00000008
DEVSTS_INCLUDED_STARTER_FIRMWARE_INCOMPATIBLE = 0x00000010
AC_SHUTTER = 0x00000001
AC_GAIN = 0x00000002
AC_WHITEBAL = 0x00000004
AC_WB_RED_CHANNEL = 0x00000008
AC_WB_GREEN_CHANNEL = 0x00000010
AC_WB_BLUE_CHANNEL = 0x00000020
AC_FRAMERATE = 0x00000040
AC_SENSOR_SHUTTER = 0x00000080
AC_SENSOR_GAIN = 0x00000100
AC_SENSOR_GAIN_SHUTTER = 0x00000200
AC_SENSOR_FRAMERATE = 0x00000400
AC_SENSOR_WB = 0x00000800
AC_SENSOR_AUTO_REFERENCE = 0x00001000
AC_SENSOR_AUTO_SPEED = 0x00002000
AC_SENSOR_AUTO_HYSTERESIS = 0x00004000
AC_SENSOR_AUTO_SKIPFRAMES = 0x00008000
AC_SENSOR_AUTO_CONTRAST_CORRECTION = 0x00010000
AC_SENSOR_AUTO_CONTRAST_FDT_AOI = 0x00020000
AC_SENSOR_AUTO_BACKLIGHT_COMP = 0x00040000
ACS_ADJUSTING = 0x00000001
ACS_FINISHED = 0x00000002
ACS_DISABLED = 0x00000004
IS_BOOTBOOST_ID_MIN = 1
IS_BOOTBOOST_ID_MAX = 254
IS_BOOTBOOST_ID_NONE = 0
IS_BOOTBOOST_ID_ALL = 255
IS_BOOTBOOST_DEFAULT_WAIT_TIMEOUT_SEC = 60
IO_LED_STATE_1 = 0
IO_LED_STATE_2 = 1
IO_LED_ENABLE = 2
IO_LED_DISABLE = 3
IO_LED_BLINK_ENABLE = 4
IO_LED_BLINK_DISABLE = 5
IO_LED_BLINK_5_TIMES = 6
IO_FLASH_MODE_OFF = 0
IO_FLASH_MODE_TRIGGER_LO_ACTIVE = 1
IO_FLASH_MODE_TRIGGER_HI_ACTIVE = 2
IO_FLASH_MODE_CONSTANT_HIGH = 3
IO_FLASH_MODE_CONSTANT_LOW = 4
IO_FLASH_MODE_FREERUN_LO_ACTIVE = 5
IO_FLASH_MODE_FREERUN_HI_ACTIVE = 6
IS_FLASH_MODE_PWM = 0x8000
IO_FLASH_MODE_GPIO_1 = 0x0010
IO_FLASH_MODE_GPIO_2 = 0x0020
IO_FLASH_MODE_GPIO_3 = 0x0040
IO_FLASH_MODE_GPIO_4 = 0x0080
IO_FLASH_MODE_GPIO_5 = 0x0100
IO_FLASH_MODE_GPIO_6 = 0x0200
IO_FLASH_GPIO_PORT_MASK = (IO_FLASH_MODE_GPIO_1|IO_FLASH_MODE_GPIO_2|IO_FLASH_MODE_GPIO_3|IO_FLASH_MODE_GPIO_4|IO_FLASH_MODE_GPIO_5|IO_FLASH_MODE_GPIO_6)
IO_GPIO_1 = 0x0001
IO_GPIO_2 = 0x0002
IO_GPIO_3 = 0x0004
IO_GPIO_4 = 0x0008
IO_GPIO_5 = 0x0010
IO_GPIO_6 = 0x0020
IS_GPIO_INPUT = 0x0001
IS_GPIO_OUTPUT = 0x0002
IS_GPIO_FLASH = 0x0004
IS_GPIO_PWM = 0x0008
IS_GPIO_COMPORT_RX = 0x0010
IS_GPIO_COMPORT_TX = 0x0020
IS_GPIO_MULTI_INTEGRATION_MODE = 0x0040
IS_GPIO_TRIGGER = 0x0080
IS_GPIO_I2C = 0x0100
IS_GPIO_TWI = IS_GPIO_I2C
IS_FLASH_AUTO_FREERUN_OFF = 0
IS_FLASH_AUTO_FREERUN_ON = 1
IS_AWB_GREYWORLD = 0x0001
IS_AWB_COLOR_TEMPERATURE = 0x0002
IS_AUTOPARAMETER_DISABLE = 0
IS_AUTOPARAMETER_ENABLE = 1
IS_AUTOPARAMETER_ENABLE_RUNONCE = 2
IS_LUT_64 = 64
IS_LUT_128 = 128
IS_LUT_PRESET_ID_IDENTITY = 0
IS_LUT_PRESET_ID_NEGATIVE = 1
IS_LUT_PRESET_ID_GLOW1 = 2
IS_LUT_PRESET_ID_GLOW2 = 3
IS_LUT_PRESET_ID_ASTRO1 = 4
IS_LUT_PRESET_ID_RAINBOW1 = 5
IS_LUT_PRESET_ID_MAP1 = 6
IS_LUT_PRESET_ID_HOT = 7
IS_LUT_PRESET_ID_SEPIC = 8
IS_LUT_PRESET_ID_ONLY_RED = 9
IS_LUT_PRESET_ID_ONLY_GREEN = 10
IS_LUT_PRESET_ID_ONLY_BLUE = 11
IS_LUT_PRESET_ID_DIGITAL_GAIN_2X = 12
IS_LUT_PRESET_ID_DIGITAL_GAIN_4X = 13
IS_LUT_PRESET_ID_DIGITAL_GAIN_8X = 14
IS_LUT_CMD_SET_ENABLED = 0x0001
IS_LUT_CMD_SET_MODE = 0x0002
IS_LUT_CMD_GET_STATE = 0x0005
IS_LUT_CMD_GET_SUPPORT_INFO = 0x0006
IS_LUT_CMD_SET_USER_LUT = 0x0010
IS_LUT_CMD_GET_USER_LUT = 0x0011
IS_LUT_CMD_GET_COMPLETE_LUT = 0x0012
IS_LUT_CMD_GET_PRESET_LUT = 0x0013
IS_LUT_CMD_LOAD_FILE = 0x0100
IS_LUT_CMD_SAVE_FILE = 0x0101
IS_LUT_STATE_ID_FLAG_HARDWARE = 0x0010
IS_LUT_STATE_ID_FLAG_SOFTWARE = 0x0020
IS_LUT_STATE_ID_FLAG_GAMMA = 0x0100
IS_LUT_STATE_ID_FLAG_LUT = 0x0200
IS_LUT_STATE_ID_INACTIVE = 0x0000
IS_LUT_STATE_ID_NOT_SUPPORTED = 0x0001
IS_LUT_STATE_ID_HARDWARE_LUT = (IS_LUT_STATE_ID_FLAG_HARDWARE|IS_LUT_STATE_ID_FLAG_LUT)
IS_LUT_STATE_ID_HARDWARE_GAMMA = (IS_LUT_STATE_ID_FLAG_HARDWARE|IS_LUT_STATE_ID_FLAG_GAMMA)
IS_LUT_STATE_ID_HARDWARE_LUTANDGAMMA = (IS_LUT_STATE_ID_FLAG_HARDWARE|IS_LUT_STATE_ID_FLAG_LUT|IS_LUT_STATE_ID_FLAG_GAMMA)
IS_LUT_STATE_ID_SOFTWARE_LUT = (IS_LUT_STATE_ID_FLAG_SOFTWARE|IS_LUT_STATE_ID_FLAG_LUT)
IS_LUT_STATE_ID_SOFTWARE_GAMMA = (IS_LUT_STATE_ID_FLAG_SOFTWARE|IS_LUT_STATE_ID_FLAG_GAMMA)
IS_LUT_STATE_ID_SOFTWARE_LUTANDGAMMA = (IS_LUT_STATE_ID_FLAG_SOFTWARE|IS_LUT_STATE_ID_FLAG_LUT|IS_LUT_STATE_ID_FLAG_GAMMA)
IS_LUT_MODE_ID_DEFAULT = 0
IS_LUT_MODE_ID_FORCE_HARDWARE = 1
IS_LUT_MODE_ID_FORCE_SOFTWARE = 2
IS_LUT_DISABLED = 0
IS_LUT_ENABLED = 1
IS_GAMMA_CMD_SET = 0x0001
IS_GAMMA_CMD_GET_DEFAULT = 0x0002
IS_GAMMA_CMD_GET = 0x0003
IS_GAMMA_VALUE_MIN = 1
IS_GAMMA_VALUE_MAX = 1000
IS_MC_CMD_FLAG_ACTIVE = 0x1000
IS_MC_CMD_FLAG_PASSIVE = 0x2000
IS_PMC_CMD_INITIALIZE = (0x0001|IS_MC_CMD_FLAG_PASSIVE)
IS_PMC_CMD_DEINITIALIZE = (0x0002|IS_MC_CMD_FLAG_PASSIVE)
IS_PMC_CMD_ADDMCDEVICE = (0x0003|IS_MC_CMD_FLAG_PASSIVE)
IS_PMC_CMD_REMOVEMCDEVICE = (0x0004|IS_MC_CMD_FLAG_PASSIVE)
IS_PMC_CMD_STOREDEVICES = (0x0005|IS_MC_CMD_FLAG_PASSIVE)
IS_PMC_CMD_LOADDEVICES = (0x0006|IS_MC_CMD_FLAG_PASSIVE)
IS_PMC_CMD_SYSTEM_SET_ENABLE = (0x0007|IS_MC_CMD_FLAG_PASSIVE)
IS_PMC_CMD_SYSTEM_GET_ENABLE = (0x0008|IS_MC_CMD_FLAG_PASSIVE)
IS_PMC_CMD_REMOVEALLMCDEVICES = (0x0009|IS_MC_CMD_FLAG_PASSIVE)
IS_AMC_CMD_SET_MC_IP = (0x0010|IS_MC_CMD_FLAG_ACTIVE)
IS_AMC_CMD_GET_MC_IP = (0x0011|IS_MC_CMD_FLAG_ACTIVE)
IS_AMC_CMD_SET_MC_ENABLED = (0x0012|IS_MC_CMD_FLAG_ACTIVE)
IS_AMC_CMD_GET_MC_ENABLED = (0x0013|IS_MC_CMD_FLAG_ACTIVE)
IS_AMC_CMD_GET_MC_SUPPORTED = (0x0014|IS_MC_CMD_FLAG_ACTIVE)
IS_AMC_SUPPORTED_FLAG_DEVICE = (0x0001)
IS_AMC_SUPPORTED_FLAG_FIRMWARE = (0x0002)
IS_PMC_ERRORHANDLING_REJECT_IMAGES = 0x01
IS_PMC_ERRORHANDLING_IGNORE_MISSING_PARTS = 0x02
IS_PMC_ERRORHANDLING_MERGE_IMAGES_RELEASE_ON_COMPLETE = 0x03
IS_PMC_ERRORHANDLING_MERGE_IMAGES_RELEASE_ON_RECEIVED_IMGLEN = 0x04


_is_CaptureStatus = _bind("is_CaptureStatus", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_CaptureStatus(hCam, nCommand, pParam, nSizeOfParam):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nCommand: c_uint (aka c-type: UINT)
    :param pParam: c_void_p (aka c-type: void \*)
    :param nSizeOfParam: c_uint (aka c-type: UINT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_CaptureStatus is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_CaptureStatus(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_WaitEvent = _bind("is_WaitEvent", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)


def is_WaitEvent(hCam, which, nTimeout):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param which: c_int (aka c-type: INT)
    :param nTimeout: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_WaitEvent is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _which = _value_cast(which, ctypes.c_int)
    _nTimeout = _value_cast(nTimeout, ctypes.c_int)

    ret = _is_WaitEvent(_hCam, _which, _nTimeout)

    return ret


_is_SetSaturation = _bind("is_SetSaturation", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)


def is_SetSaturation(hCam, ChromU, ChromV):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param ChromU: c_int (aka c-type: INT)
    :param ChromV: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetSaturation is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _ChromU = _value_cast(ChromU, ctypes.c_int)
    _ChromV = _value_cast(ChromV, ctypes.c_int)

    ret = _is_SetSaturation(_hCam, _ChromU, _ChromV)

    return ret


_is_PrepareStealVideo = _bind("is_PrepareStealVideo", [ctypes.c_uint, ctypes.c_int, ctypes.c_uint], ctypes.c_int)


def is_PrepareStealVideo(hCam, Mode, StealColorMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Mode: c_int (aka c-type: int)
    :param StealColorMode: c_uint (aka c-type: ULONG)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_PrepareStealVideo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Mode = _value_cast(Mode, ctypes.c_int)
    _StealColorMode = _value_cast(StealColorMode, ctypes.c_uint)

    ret = _is_PrepareStealVideo(_hCam, _Mode, _StealColorMode)

    return ret


_is_GetNumberOfDevices = _bind("is_GetNumberOfDevices", None, ctypes.c_int)


def is_GetNumberOfDevices():
    """
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetNumberOfDevices is None:
        raise NotImplementedError()

    ret = _is_GetNumberOfDevices()

    return ret


_is_StopLiveVideo = _bind("is_StopLiveVideo", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_StopLiveVideo(hCam, Wait):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Wait: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_StopLiveVideo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Wait = _value_cast(Wait, ctypes.c_int)

    ret = _is_StopLiveVideo(_hCam, _Wait)

    return ret


_is_FreezeVideo = _bind("is_FreezeVideo", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_FreezeVideo(hCam, Wait):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Wait: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_FreezeVideo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Wait = _value_cast(Wait, ctypes.c_int)

    ret = _is_FreezeVideo(_hCam, _Wait)

    return ret


_is_CaptureVideo = _bind("is_CaptureVideo", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_CaptureVideo(hCam, Wait):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Wait: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_CaptureVideo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Wait = _value_cast(Wait, ctypes.c_int)

    ret = _is_CaptureVideo(_hCam, _Wait)

    return ret


_is_IsVideoFinish = _bind("is_IsVideoFinish", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_IsVideoFinish(hCam, pValue):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pValue: c_int (aka c-type: INT \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_IsVideoFinish is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_IsVideoFinish(_hCam, ctypes.byref(pValue))

    return ret


_is_HasVideoStarted = _bind("is_HasVideoStarted", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_HasVideoStarted(hCam, pbo):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pbo: c_int (aka c-type: BOOL \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_HasVideoStarted is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_HasVideoStarted(_hCam, ctypes.byref(pbo))

    return ret


_is_AllocImageMem = _bind("is_AllocImageMem", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(c_mem_p), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_AllocImageMem(hCam, width, height, bitspixel, ppcImgMem, pid):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _width = _value_cast(width, ctypes.c_int)
    _height = _value_cast(height, ctypes.c_int)
    _bitspixel = _value_cast(bitspixel, ctypes.c_int)

    ret = _is_AllocImageMem(_hCam, _width, _height, _bitspixel, ctypes.byref(ppcImgMem), ctypes.byref(pid))

    return ret


_is_SetImageMem = _bind("is_SetImageMem", [ctypes.c_uint, c_mem_p, ctypes.c_int], ctypes.c_int)


def is_SetImageMem(hCam, pcMem, id):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pcMem: c_mem_p (aka c-type: char \*)
    :param id: c_int (aka c-type: int)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetImageMem is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _id = _value_cast(id, ctypes.c_int)

    ret = _is_SetImageMem(_hCam, pcMem, _id)

    return ret


_is_FreeImageMem = _bind("is_FreeImageMem", [ctypes.c_uint, c_mem_p, ctypes.c_int], ctypes.c_int)


def is_FreeImageMem(hCam, pcMem, id):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pcMem: c_mem_p (aka c-type: char \*)
    :param id: c_int (aka c-type: int)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_FreeImageMem is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _id = _value_cast(id, ctypes.c_int)

    ret = _is_FreeImageMem(_hCam, pcMem, _id)

    return ret


_is_GetImageMem = _bind("is_GetImageMem", [ctypes.c_uint, ctypes.POINTER(c_mem_p)], ctypes.c_int)


def is_GetImageMem(hCam, pMem):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pMem: c_mem_p (aka c-type: VOID \* \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetImageMem is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetImageMem(_hCam, ctypes.byref(pMem))

    return ret


_is_GetActiveImageMem = _bind("is_GetActiveImageMem", [ctypes.c_uint, ctypes.POINTER(c_mem_p), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_GetActiveImageMem(hCam, ppcMem, pnID):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param ppcMem: c_mem_p (aka c-type: char \* \*)
    :param pnID: c_int (aka c-type: int \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetActiveImageMem is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetActiveImageMem(_hCam, ctypes.byref(ppcMem), ctypes.byref(pnID))

    return ret


_is_InquireImageMem = _bind("is_InquireImageMem", [ctypes.c_uint, c_mem_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_InquireImageMem(hCam, pcMem, nID, pnX, pnY, pnBits, pnPitch):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nID = _value_cast(nID, ctypes.c_int)

    ret = _is_InquireImageMem(_hCam, pcMem, _nID, ctypes.byref(pnX) if pnX is not None else None, ctypes.byref(pnY) if pnY is not None else None, ctypes.byref(pnBits) if pnBits is not None else None, ctypes.byref(pnPitch) if pnPitch is not None else None)

    return ret


_is_GetImageMemPitch = _bind("is_GetImageMemPitch", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_GetImageMemPitch(hCam, pPitch):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pPitch: c_int (aka c-type: INT \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetImageMemPitch is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetImageMemPitch(_hCam, ctypes.byref(pPitch))

    return ret


_is_SetAllocatedImageMem = _bind("is_SetAllocatedImageMem", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, c_mem_p, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_SetAllocatedImageMem(hCam, width, height, bitspixel, pcImgMem, pid):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _width = _value_cast(width, ctypes.c_int)
    _height = _value_cast(height, ctypes.c_int)
    _bitspixel = _value_cast(bitspixel, ctypes.c_int)

    ret = _is_SetAllocatedImageMem(_hCam, _width, _height, _bitspixel, pcImgMem, ctypes.byref(pid))

    return ret


_is_CopyImageMem = _bind("is_CopyImageMem", [ctypes.c_uint, c_mem_p, ctypes.c_int, c_mem_p], ctypes.c_int)


def is_CopyImageMem(hCam, pcSource, nID, pcDest):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nID = _value_cast(nID, ctypes.c_int)

    ret = _is_CopyImageMem(_hCam, pcSource, _nID, pcDest)

    return ret


_is_CopyImageMemLines = _bind("is_CopyImageMemLines", [ctypes.c_uint, c_mem_p, ctypes.c_int, ctypes.c_int, c_mem_p], ctypes.c_int)


def is_CopyImageMemLines(hCam, pcSource, nID, nLines, pcDest):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nID = _value_cast(nID, ctypes.c_int)
    _nLines = _value_cast(nLines, ctypes.c_int)

    ret = _is_CopyImageMemLines(_hCam, pcSource, _nID, _nLines, pcDest)

    return ret


_is_AddToSequence = _bind("is_AddToSequence", [ctypes.c_uint, c_mem_p, ctypes.c_int], ctypes.c_int)


def is_AddToSequence(hCam, pcMem, nID):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pcMem: c_mem_p (aka c-type: char \*)
    :param nID: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_AddToSequence is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nID = _value_cast(nID, ctypes.c_int)

    ret = _is_AddToSequence(_hCam, pcMem, _nID)

    return ret


_is_ClearSequence = _bind("is_ClearSequence", [ctypes.c_uint], ctypes.c_int)


def is_ClearSequence(hCam):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_ClearSequence is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_ClearSequence(_hCam)

    return ret


_is_GetActSeqBuf = _bind("is_GetActSeqBuf", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(c_mem_p), ctypes.POINTER(c_mem_p)], ctypes.c_int)


def is_GetActSeqBuf(hCam, pnNum, ppcMem, ppcMemLast):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetActSeqBuf(_hCam, ctypes.byref(pnNum) if pnNum is not None else None, ctypes.byref(ppcMem) if ppcMem is not None else None, ctypes.byref(ppcMemLast) if ppcMemLast is not None else None)

    return ret


_is_LockSeqBuf = _bind("is_LockSeqBuf", [ctypes.c_uint, ctypes.c_int, c_mem_p], ctypes.c_int)


def is_LockSeqBuf(hCam, nNum, pcMem):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nNum: c_int (aka c-type: INT)
    :param pcMem: c_mem_p (aka c-type: char \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_LockSeqBuf is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nNum = _value_cast(nNum, ctypes.c_int)

    ret = _is_LockSeqBuf(_hCam, _nNum, pcMem)

    return ret


_is_UnlockSeqBuf = _bind("is_UnlockSeqBuf", [ctypes.c_uint, ctypes.c_int, c_mem_p], ctypes.c_int)


def is_UnlockSeqBuf(hCam, nNum, pcMem):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nNum: c_int (aka c-type: INT)
    :param pcMem: c_mem_p (aka c-type: char \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_UnlockSeqBuf is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nNum = _value_cast(nNum, ctypes.c_int)

    ret = _is_UnlockSeqBuf(_hCam, _nNum, pcMem)

    return ret


_is_GetError = _bind("is_GetError", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_char_p)], ctypes.c_int)


def is_GetError(hCam, pErr, ppcErr):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pErr: c_int (aka c-type: INT \*)
    :param ppcErr: c_char_p (aka c-type: IS_CHAR \* \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetError is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetError(_hCam, ctypes.byref(pErr), ctypes.byref(ppcErr))

    return ret


_is_SetErrorReport = _bind("is_SetErrorReport", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetErrorReport(hCam, Mode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Mode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetErrorReport is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Mode = _value_cast(Mode, ctypes.c_int)

    ret = _is_SetErrorReport(_hCam, _Mode)

    return ret


_is_SetColorMode = _bind("is_SetColorMode", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetColorMode(hCam, Mode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Mode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetColorMode is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Mode = _value_cast(Mode, ctypes.c_int)

    ret = _is_SetColorMode(_hCam, _Mode)

    return ret


_is_GetColorDepth = _bind("is_GetColorDepth", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_GetColorDepth(hCam, pnCol, pnColMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pnCol: c_int (aka c-type: INT \*)
    :param pnColMode: c_int (aka c-type: INT \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetColorDepth is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetColorDepth(_hCam, ctypes.byref(pnCol), ctypes.byref(pnColMode))

    return ret


_is_RenderBitmap = _bind("is_RenderBitmap", [ctypes.c_uint, ctypes.c_int, ctypes.c_void_p, ctypes.c_int], ctypes.c_int)


def is_RenderBitmap(hCam, nMemID, hwnd, nMode):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMemID = _value_cast(nMemID, ctypes.c_int)
    _hwnd = _pointer_cast(hwnd, ctypes.c_void_p)
    _nMode = _value_cast(nMode, ctypes.c_int)

    ret = _is_RenderBitmap(_hCam, _nMemID, _hwnd, _nMode)

    return ret


_is_SetDisplayMode = _bind("is_SetDisplayMode", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetDisplayMode(hCam, Mode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Mode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetDisplayMode is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Mode = _value_cast(Mode, ctypes.c_int)

    ret = _is_SetDisplayMode(_hCam, _Mode)

    return ret


_is_SetDisplayPos = _bind("is_SetDisplayPos", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)


def is_SetDisplayPos(hCam, x, y):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param x: c_int (aka c-type: INT)
    :param y: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetDisplayPos is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _x = _value_cast(x, ctypes.c_int)
    _y = _value_cast(y, ctypes.c_int)

    ret = _is_SetDisplayPos(_hCam, _x, _y)

    return ret


_is_SetHwnd = _bind("is_SetHwnd", [ctypes.c_uint, ctypes.c_void_p], ctypes.c_int)


def is_SetHwnd(hCam, hwnd):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param hwnd: c_void_p (aka c-type: HWND)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetHwnd is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _hwnd = _pointer_cast(hwnd, ctypes.c_void_p)

    ret = _is_SetHwnd(_hCam, _hwnd)

    return ret


_is_GetVsyncCount = _bind("is_GetVsyncCount", [ctypes.c_uint, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long)], ctypes.c_int)


def is_GetVsyncCount(hCam, pIntr, pActIntr):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pIntr: c_long (aka c-type: long \*)
    :param pActIntr: c_long (aka c-type: long \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetVsyncCount is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

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


def is_InitEvent(hCam, hEv, which):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param hEv: c_void_p (aka c-type: HANDLE)
    :param which: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_InitEvent is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _hEv = _pointer_cast(hEv, ctypes.c_void_p)
    _which = _value_cast(which, ctypes.c_int)

    ret = _is_InitEvent(_hCam, _hEv, _which)

    return ret


_is_ExitEvent = _bind("is_ExitEvent", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_ExitEvent(hCam, which):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param which: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_ExitEvent is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _which = _value_cast(which, ctypes.c_int)

    ret = _is_ExitEvent(_hCam, _which)

    return ret


_is_EnableEvent = _bind("is_EnableEvent", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_EnableEvent(hCam, which):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param which: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_EnableEvent is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _which = _value_cast(which, ctypes.c_int)

    ret = _is_EnableEvent(_hCam, _which)

    return ret


_is_DisableEvent = _bind("is_DisableEvent", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_DisableEvent(hCam, which):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param which: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_DisableEvent is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _which = _value_cast(which, ctypes.c_int)

    ret = _is_DisableEvent(_hCam, _which)

    return ret


_is_SetExternalTrigger = _bind("is_SetExternalTrigger", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetExternalTrigger(hCam, nTriggerMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nTriggerMode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetExternalTrigger is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nTriggerMode = _value_cast(nTriggerMode, ctypes.c_int)

    ret = _is_SetExternalTrigger(_hCam, _nTriggerMode)

    return ret


_is_SetTriggerCounter = _bind("is_SetTriggerCounter", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetTriggerCounter(hCam, nValue):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nValue: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetTriggerCounter is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nValue = _value_cast(nValue, ctypes.c_int)

    ret = _is_SetTriggerCounter(_hCam, _nValue)

    return ret


_is_SetRopEffect = _bind("is_SetRopEffect", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], ctypes.c_int)


def is_SetRopEffect(hCam, effect, param, reserved):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
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


def is_ExitCamera(hCam):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_ExitCamera is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_ExitCamera(_hCam)

    return ret


_is_GetCameraInfo = _bind("is_GetCameraInfo", [ctypes.c_uint, ctypes.POINTER(CAMINFO)], ctypes.c_int)


def is_GetCameraInfo(hCam, pInfo):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pInfo: CAMINFO (aka c-type: PCAMINFO)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetCameraInfo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetCameraInfo(_hCam, ctypes.byref(pInfo))

    return ret


_is_CameraStatus = _bind("is_CameraStatus", [ctypes.c_uint, ctypes.c_int, ctypes.c_uint], ctypes.c_int)


def is_CameraStatus(hCam, nInfo, ulValue):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nInfo: c_int (aka c-type: INT)
    :param ulValue: c_uint (aka c-type: ULONG)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_CameraStatus is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nInfo = _value_cast(nInfo, ctypes.c_int)
    _ulValue = _value_cast(ulValue, ctypes.c_uint)

    ret = _is_CameraStatus(_hCam, _nInfo, _ulValue)

    return ret


_is_GetCameraType = _bind("is_GetCameraType", [ctypes.c_uint], ctypes.c_int)


def is_GetCameraType(hCam):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetCameraType is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

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


def is_GetUsedBandwidth(hCam):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetUsedBandwidth is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetUsedBandwidth(_hCam)

    return ret


_is_GetFrameTimeRange = _bind("is_GetFrameTimeRange", [ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)], ctypes.c_int)


def is_GetFrameTimeRange(hCam, min, max, intervall):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetFrameTimeRange(_hCam, ctypes.byref(min), ctypes.byref(max), ctypes.byref(intervall))

    return ret


_is_SetFrameRate = _bind("is_SetFrameRate", [ctypes.c_uint, ctypes.c_double, ctypes.POINTER(ctypes.c_double)], ctypes.c_int)


def is_SetFrameRate(hCam, FPS, newFPS):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param FPS: c_double (aka c-type: double)
    :param newFPS: c_double (aka c-type: double \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetFrameRate is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _FPS = _value_cast(FPS, ctypes.c_double)

    ret = _is_SetFrameRate(_hCam, _FPS, ctypes.byref(newFPS))

    return ret


_is_GetFramesPerSecond = _bind("is_GetFramesPerSecond", [ctypes.c_uint, ctypes.POINTER(ctypes.c_double)], ctypes.c_int)


def is_GetFramesPerSecond(hCam, dblFPS):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param dblFPS: c_double (aka c-type: double \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetFramesPerSecond is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetFramesPerSecond(_hCam, ctypes.byref(dblFPS))

    return ret


_is_GetSensorInfo = _bind("is_GetSensorInfo", [ctypes.c_uint, ctypes.POINTER(SENSORINFO)], ctypes.c_int)


def is_GetSensorInfo(hCam, pInfo):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pInfo: SENSORINFO (aka c-type: PSENSORINFO)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetSensorInfo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetSensorInfo(_hCam, ctypes.byref(pInfo))

    return ret


_is_GetRevisionInfo = _bind("is_GetRevisionInfo", [ctypes.c_uint, ctypes.POINTER(REVISIONINFO)], ctypes.c_int)


def is_GetRevisionInfo(hCam, prevInfo):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param prevInfo: REVISIONINFO (aka c-type: PREVISIONINFO)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetRevisionInfo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetRevisionInfo(_hCam, ctypes.byref(prevInfo))

    return ret


_is_EnableAutoExit = _bind("is_EnableAutoExit", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_EnableAutoExit(hCam, nMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_EnableAutoExit is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_int)

    ret = _is_EnableAutoExit(_hCam, _nMode)

    return ret


_is_EnableMessage = _bind("is_EnableMessage", [ctypes.c_uint, ctypes.c_int, ctypes.c_void_p], ctypes.c_int)


def is_EnableMessage(hCam, which, hWnd):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param which: c_int (aka c-type: INT)
    :param hWnd: c_void_p (aka c-type: HWND)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_EnableMessage is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _which = _value_cast(which, ctypes.c_int)
    _hWnd = _pointer_cast(hWnd, ctypes.c_void_p)

    ret = _is_EnableMessage(_hCam, _which, _hWnd)

    return ret


_is_SetHardwareGain = _bind("is_SetHardwareGain", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int], ctypes.c_int)


def is_SetHardwareGain(hCam, nMaster, nRed, nGreen, nBlue):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMaster = _value_cast(nMaster, ctypes.c_int)
    _nRed = _value_cast(nRed, ctypes.c_int)
    _nGreen = _value_cast(nGreen, ctypes.c_int)
    _nBlue = _value_cast(nBlue, ctypes.c_int)

    ret = _is_SetHardwareGain(_hCam, _nMaster, _nRed, _nGreen, _nBlue)

    return ret


_is_SetWhiteBalance = _bind("is_SetWhiteBalance", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetWhiteBalance(hCam, nMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetWhiteBalance is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_int)

    ret = _is_SetWhiteBalance(_hCam, _nMode)

    return ret


_is_SetWhiteBalanceMultipliers = _bind("is_SetWhiteBalanceMultipliers", [ctypes.c_uint, ctypes.c_double, ctypes.c_double, ctypes.c_double], ctypes.c_int)


def is_SetWhiteBalanceMultipliers(hCam, dblRed, dblGreen, dblBlue):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _dblRed = _value_cast(dblRed, ctypes.c_double)
    _dblGreen = _value_cast(dblGreen, ctypes.c_double)
    _dblBlue = _value_cast(dblBlue, ctypes.c_double)

    ret = _is_SetWhiteBalanceMultipliers(_hCam, _dblRed, _dblGreen, _dblBlue)

    return ret


_is_GetWhiteBalanceMultipliers = _bind("is_GetWhiteBalanceMultipliers", [ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)], ctypes.c_int)


def is_GetWhiteBalanceMultipliers(hCam, pdblRed, pdblGreen, pdblBlue):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetWhiteBalanceMultipliers(_hCam, ctypes.byref(pdblRed), ctypes.byref(pdblGreen), ctypes.byref(pdblBlue))

    return ret


_is_SetColorCorrection = _bind("is_SetColorCorrection", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_double)], ctypes.c_int)


def is_SetColorCorrection(hCam, nEnable, factors):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nEnable: c_int (aka c-type: INT)
    :param factors: c_double (aka c-type: double \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetColorCorrection is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nEnable = _value_cast(nEnable, ctypes.c_int)

    ret = _is_SetColorCorrection(_hCam, _nEnable, ctypes.byref(factors))

    return ret


_is_SetSubSampling = _bind("is_SetSubSampling", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetSubSampling(hCam, mode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param mode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetSubSampling is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _mode = _value_cast(mode, ctypes.c_int)

    ret = _is_SetSubSampling(_hCam, _mode)

    return ret


_is_ForceTrigger = _bind("is_ForceTrigger", [ctypes.c_uint], ctypes.c_int)


def is_ForceTrigger(hCam):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_ForceTrigger is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_ForceTrigger(_hCam)

    return ret


_is_GetBusSpeed = _bind("is_GetBusSpeed", [ctypes.c_uint], ctypes.c_int)


def is_GetBusSpeed(hCam):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetBusSpeed is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetBusSpeed(_hCam)

    return ret


_is_SetBinning = _bind("is_SetBinning", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetBinning(hCam, mode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param mode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetBinning is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _mode = _value_cast(mode, ctypes.c_int)

    ret = _is_SetBinning(_hCam, _mode)

    return ret


_is_ResetToDefault = _bind("is_ResetToDefault", [ctypes.c_uint], ctypes.c_int)


def is_ResetToDefault(hCam):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_ResetToDefault is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_ResetToDefault(_hCam)

    return ret


_is_SetCameraID = _bind("is_SetCameraID", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetCameraID(hCam, nID):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nID: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetCameraID is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nID = _value_cast(nID, ctypes.c_int)

    ret = _is_SetCameraID(_hCam, _nID)

    return ret


_is_SetBayerConversion = _bind("is_SetBayerConversion", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetBayerConversion(hCam, nMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetBayerConversion is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_int)

    ret = _is_SetBayerConversion(_hCam, _nMode)

    return ret


_is_SetHardwareGamma = _bind("is_SetHardwareGamma", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetHardwareGamma(hCam, nMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetHardwareGamma is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
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


def is_SetAutoParameter(hCam, param, pval1, pval2):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _param = _value_cast(param, ctypes.c_int)

    ret = _is_SetAutoParameter(_hCam, _param, ctypes.byref(pval1), ctypes.byref(pval2))

    return ret


_is_GetAutoInfo = _bind("is_GetAutoInfo", [ctypes.c_uint, ctypes.POINTER(UEYE_AUTO_INFO)], ctypes.c_int)


def is_GetAutoInfo(hCam, pInfo):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pInfo: UEYE_AUTO_INFO (aka c-type: UEYE_AUTO_INFO \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetAutoInfo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetAutoInfo(_hCam, ctypes.byref(pInfo))

    return ret


_is_GetImageHistogram = _bind("is_GetImageHistogram", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_uint)], ctypes.c_int)


def is_GetImageHistogram(hCam, nID, ColorMode, pHistoMem):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nID = _value_cast(nID, ctypes.c_int)
    _ColorMode = _value_cast(ColorMode, ctypes.c_int)

    ret = _is_GetImageHistogram(_hCam, _nID, _ColorMode, ctypes.cast(pHistoMem, ctypes.POINTER(ctypes.c_uint)))

    return ret


_is_SetTriggerDelay = _bind("is_SetTriggerDelay", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetTriggerDelay(hCam, nTriggerDelay):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nTriggerDelay: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetTriggerDelay is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nTriggerDelay = _value_cast(nTriggerDelay, ctypes.c_int)

    ret = _is_SetTriggerDelay(_hCam, _nTriggerDelay)

    return ret


_is_SetGainBoost = _bind("is_SetGainBoost", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetGainBoost(hCam, mode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param mode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetGainBoost is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _mode = _value_cast(mode, ctypes.c_int)

    ret = _is_SetGainBoost(_hCam, _mode)

    return ret


_is_SetGlobalShutter = _bind("is_SetGlobalShutter", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_SetGlobalShutter(hCam, mode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param mode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetGlobalShutter is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _mode = _value_cast(mode, ctypes.c_int)

    ret = _is_SetGlobalShutter(_hCam, _mode)

    return ret


_is_SetExtendedRegister = _bind("is_SetExtendedRegister", [ctypes.c_uint, ctypes.c_int, ctypes.c_ushort], ctypes.c_int)


def is_SetExtendedRegister(hCam, index, value):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param index: c_int (aka c-type: INT)
    :param value: c_ushort (aka c-type: WORD)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetExtendedRegister is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _index = _value_cast(index, ctypes.c_int)
    _value = _value_cast(value, ctypes.c_ushort)

    ret = _is_SetExtendedRegister(_hCam, _index, _value)

    return ret


_is_GetExtendedRegister = _bind("is_GetExtendedRegister", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_ushort)], ctypes.c_int)


def is_GetExtendedRegister(hCam, index, pwValue):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param index: c_int (aka c-type: INT)
    :param pwValue: c_ushort (aka c-type: WORD \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetExtendedRegister is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _index = _value_cast(index, ctypes.c_int)

    ret = _is_GetExtendedRegister(_hCam, _index, ctypes.byref(pwValue))

    return ret


_is_SetHWGainFactor = _bind("is_SetHWGainFactor", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)


def is_SetHWGainFactor(hCam, nMode, nFactor):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_int (aka c-type: INT)
    :param nFactor: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetHWGainFactor is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_int)
    _nFactor = _value_cast(nFactor, ctypes.c_int)

    ret = _is_SetHWGainFactor(_hCam, _nMode, _nFactor)

    return ret


_is_Renumerate = _bind("is_Renumerate", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_Renumerate(hCam, nMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_Renumerate is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_int)

    ret = _is_Renumerate(_hCam, _nMode)

    return ret


_is_WriteI2C = _bind("is_WriteI2C", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int], ctypes.c_int)


def is_WriteI2C(hCam, nDeviceAddr, nRegisterAddr, pbData, nLen):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nDeviceAddr = _value_cast(nDeviceAddr, ctypes.c_int)
    _nRegisterAddr = _value_cast(nRegisterAddr, ctypes.c_int)
    _nLen = _value_cast(nLen, ctypes.c_int)

    ret = _is_WriteI2C(_hCam, _nDeviceAddr, _nRegisterAddr, ctypes.cast(pbData, ctypes.POINTER(ctypes.c_ubyte)), _nLen)

    return ret


_is_ReadI2C = _bind("is_ReadI2C", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int], ctypes.c_int)


def is_ReadI2C(hCam, nDeviceAddr, nRegisterAddr, pbData, nLen):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nDeviceAddr = _value_cast(nDeviceAddr, ctypes.c_int)
    _nRegisterAddr = _value_cast(nRegisterAddr, ctypes.c_int)
    _nLen = _value_cast(nLen, ctypes.c_int)

    ret = _is_ReadI2C(_hCam, _nDeviceAddr, _nRegisterAddr, ctypes.cast(pbData, ctypes.POINTER(ctypes.c_ubyte)), _nLen)

    return ret


_is_GetHdrMode = _bind("is_GetHdrMode", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_GetHdrMode(hCam, Mode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Mode: c_int (aka c-type: INT \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetHdrMode is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetHdrMode(_hCam, ctypes.byref(Mode))

    return ret


_is_EnableHdr = _bind("is_EnableHdr", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_EnableHdr(hCam, Enable):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Enable: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_EnableHdr is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Enable = _value_cast(Enable, ctypes.c_int)

    ret = _is_EnableHdr(_hCam, _Enable)

    return ret


_is_SetHdrKneepoints = _bind("is_SetHdrKneepoints", [ctypes.c_uint, ctypes.POINTER(KNEEPOINTARRAY), ctypes.c_int], ctypes.c_int)


def is_SetHdrKneepoints(hCam, KneepointArray, KneepointArraySize):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param KneepointArray: KNEEPOINTARRAY (aka c-type: KNEEPOINTARRAY \*)
    :param KneepointArraySize: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetHdrKneepoints is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _KneepointArraySize = _value_cast(KneepointArraySize, ctypes.c_int)

    ret = _is_SetHdrKneepoints(_hCam, ctypes.byref(KneepointArray), _KneepointArraySize)

    return ret


_is_GetHdrKneepoints = _bind("is_GetHdrKneepoints", [ctypes.c_uint, ctypes.POINTER(KNEEPOINTARRAY), ctypes.c_int], ctypes.c_int)


def is_GetHdrKneepoints(hCam, KneepointArray, KneepointArraySize):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param KneepointArray: KNEEPOINTARRAY (aka c-type: KNEEPOINTARRAY \*)
    :param KneepointArraySize: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetHdrKneepoints is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _KneepointArraySize = _value_cast(KneepointArraySize, ctypes.c_int)

    ret = _is_GetHdrKneepoints(_hCam, ctypes.byref(KneepointArray), _KneepointArraySize)

    return ret


_is_GetHdrKneepointInfo = _bind("is_GetHdrKneepointInfo", [ctypes.c_uint, ctypes.POINTER(KNEEPOINTINFO), ctypes.c_int], ctypes.c_int)


def is_GetHdrKneepointInfo(hCam, KneepointInfo, KneepointInfoSize):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param KneepointInfo: KNEEPOINTINFO (aka c-type: KNEEPOINTINFO \*)
    :param KneepointInfoSize: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetHdrKneepointInfo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _KneepointInfoSize = _value_cast(KneepointInfoSize, ctypes.c_int)

    ret = _is_GetHdrKneepointInfo(_hCam, ctypes.byref(KneepointInfo), _KneepointInfoSize)

    return ret


_is_SetOptimalCameraTiming = _bind("is_SetOptimalCameraTiming", [ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)], ctypes.c_int)


def is_SetOptimalCameraTiming(hCam, Mode, Timeout, pMaxPxlClk, pMaxFrameRate):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Mode = _value_cast(Mode, ctypes.c_int)
    _Timeout = _value_cast(Timeout, ctypes.c_int)

    ret = _is_SetOptimalCameraTiming(_hCam, _Mode, _Timeout, ctypes.byref(pMaxPxlClk), ctypes.byref(pMaxFrameRate))

    return ret


_is_GetSupportedTestImages = _bind("is_GetSupportedTestImages", [ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_GetSupportedTestImages(hCam, SupportedTestImages):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param SupportedTestImages: c_int (aka c-type: INT \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetSupportedTestImages is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_GetSupportedTestImages(_hCam, ctypes.byref(SupportedTestImages))

    return ret


_is_GetTestImageValueRange = _bind("is_GetTestImageValueRange", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_GetTestImageValueRange(hCam, TestImage, TestImageValueMin, TestImageValueMax):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _TestImage = _value_cast(TestImage, ctypes.c_int)

    ret = _is_GetTestImageValueRange(_hCam, _TestImage, ctypes.byref(TestImageValueMin), ctypes.byref(TestImageValueMax))

    return ret


_is_SetSensorTestImage = _bind("is_SetSensorTestImage", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)


def is_SetSensorTestImage(hCam, Param1, Param2):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param Param1: c_int (aka c-type: INT)
    :param Param2: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetSensorTestImage is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _Param1 = _value_cast(Param1, ctypes.c_int)
    _Param2 = _value_cast(Param2, ctypes.c_int)

    ret = _is_SetSensorTestImage(_hCam, _Param1, _Param2)

    return ret


_is_GetColorConverter = _bind("is_GetColorConverter", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_GetColorConverter(hCam, ColorMode, pCurrentConvertMode, pDefaultConvertMode, pSupportedConvertModes):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _ColorMode = _value_cast(ColorMode, ctypes.c_int)

    ret = _is_GetColorConverter(_hCam, _ColorMode, ctypes.byref(pCurrentConvertMode), ctypes.byref(pDefaultConvertMode), ctypes.byref(pSupportedConvertModes))

    return ret


_is_SetColorConverter = _bind("is_SetColorConverter", [ctypes.c_uint, ctypes.c_int, ctypes.c_int], ctypes.c_int)


def is_SetColorConverter(hCam, ColorMode, ConvertMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param ColorMode: c_int (aka c-type: INT)
    :param ConvertMode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetColorConverter is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _ColorMode = _value_cast(ColorMode, ctypes.c_int)
    _ConvertMode = _value_cast(ConvertMode, ctypes.c_int)

    ret = _is_SetColorConverter(_hCam, _ColorMode, _ConvertMode)

    return ret


_is_WaitForNextImage = _bind("is_WaitForNextImage", [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(c_mem_p), ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_WaitForNextImage(hCam, timeout, ppcMem, imageID):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _timeout = _value_cast(timeout, ctypes.c_uint)

    ret = _is_WaitForNextImage(_hCam, _timeout, ctypes.byref(ppcMem), ctypes.byref(imageID))

    return ret


_is_InitImageQueue = _bind("is_InitImageQueue", [ctypes.c_uint, ctypes.c_int], ctypes.c_int)


def is_InitImageQueue(hCam, nMode):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_InitImageQueue is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_int)

    ret = _is_InitImageQueue(_hCam, _nMode)

    return ret


_is_ExitImageQueue = _bind("is_ExitImageQueue", [ctypes.c_uint], ctypes.c_int)


def is_ExitImageQueue(hCam):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_ExitImageQueue is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

    ret = _is_ExitImageQueue(_hCam)

    return ret


_is_SetTimeout = _bind("is_SetTimeout", [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], ctypes.c_int)


def is_SetTimeout(hCam, nMode, Timeout):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_uint (aka c-type: UINT)
    :param Timeout: c_uint (aka c-type: UINT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetTimeout is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_uint)
    _Timeout = _value_cast(Timeout, ctypes.c_uint)

    ret = _is_SetTimeout(_hCam, _nMode, _Timeout)

    return ret


_is_GetTimeout = _bind("is_GetTimeout", [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)], ctypes.c_int)


def is_GetTimeout(hCam, nMode, pTimeout):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_uint (aka c-type: UINT)
    :param pTimeout: c_uint (aka c-type: UINT \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetTimeout is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_uint)

    ret = _is_GetTimeout(_hCam, _nMode, ctypes.byref(pTimeout))

    return ret


_is_GetDuration = _bind("is_GetDuration", [ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)], ctypes.c_int)


def is_GetDuration(hCam, nMode, pnTime):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_uint (aka c-type: UINT)
    :param pnTime: c_int (aka c-type: INT \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetDuration is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_uint)

    ret = _is_GetDuration(_hCam, _nMode, ctypes.byref(pnTime))

    return ret


_is_GetSensorScalerInfo = _bind("is_GetSensorScalerInfo", [ctypes.c_uint, ctypes.POINTER(SENSORSCALERINFO), ctypes.c_int], ctypes.c_int)


def is_GetSensorScalerInfo(hCam, pSensorScalerInfo, nSensorScalerInfoSize):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pSensorScalerInfo: SENSORSCALERINFO (aka c-type: SENSORSCALERINFO \*)
    :param nSensorScalerInfoSize: c_int (aka c-type: INT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetSensorScalerInfo is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nSensorScalerInfoSize = _value_cast(nSensorScalerInfoSize, ctypes.c_int)

    ret = _is_GetSensorScalerInfo(_hCam, ctypes.byref(pSensorScalerInfo), _nSensorScalerInfoSize)

    return ret


_is_SetSensorScaler = _bind("is_SetSensorScaler", [ctypes.c_uint, ctypes.c_uint, ctypes.c_double], ctypes.c_int)


def is_SetSensorScaler(hCam, nMode, dblFactor):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param nMode: c_uint (aka c-type: UINT)
    :param dblFactor: c_double (aka c-type: double)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetSensorScaler is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_uint)
    _dblFactor = _value_cast(dblFactor, ctypes.c_double)

    ret = _is_SetSensorScaler(_hCam, _nMode, _dblFactor)

    return ret


_is_GetImageInfo = _bind("is_GetImageInfo", [ctypes.c_uint, ctypes.c_int, ctypes.POINTER(UEYEIMAGEINFO), ctypes.c_int], ctypes.c_int)


def is_GetImageInfo(hCam, nImageBufferID, pImageInfo, nImageInfoSize):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nImageBufferID = _value_cast(nImageBufferID, ctypes.c_int)
    _nImageInfoSize = _value_cast(nImageInfoSize, ctypes.c_int)

    ret = _is_GetImageInfo(_hCam, _nImageBufferID, ctypes.byref(pImageInfo), _nImageInfoSize)

    return ret


_is_ImageFormat = _bind("is_ImageFormat", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_ImageFormat(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_ImageFormat(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_FaceDetection = _bind("is_FaceDetection", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_FaceDetection(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_FaceDetection(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_Focus = _bind("is_Focus", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Focus(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_Focus(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_ImageStabilization = _bind("is_ImageStabilization", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_ImageStabilization(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_ImageStabilization(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_ScenePreset = _bind("is_ScenePreset", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_ScenePreset(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_ScenePreset(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_Zoom = _bind("is_Zoom", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Zoom(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_Zoom(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_Sharpness = _bind("is_Sharpness", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Sharpness(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_Sharpness(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_Saturation = _bind("is_Saturation", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Saturation(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_Saturation(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_TriggerDebounce = _bind("is_TriggerDebounce", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_TriggerDebounce(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_TriggerDebounce(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_ColorTemperature = _bind("is_ColorTemperature", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_ColorTemperature(hCam, nCommand, pParam, nSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _nSizeOfParam = _value_cast(nSizeOfParam, ctypes.c_uint)

    ret = _is_ColorTemperature(_hCam, _nCommand, _pParam, _nSizeOfParam)

    return ret


_is_DirectRenderer = _bind("is_DirectRenderer", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_DirectRenderer(hCam, nMode, pParam, SizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _SizeOfParam = _value_cast(SizeOfParam, ctypes.c_uint)

    ret = _is_DirectRenderer(_hCam, _nMode, _pParam, _SizeOfParam)

    return ret


_is_HotPixel = _bind("is_HotPixel", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_HotPixel(hCam, nMode, pParam, SizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nMode = _value_cast(nMode, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _SizeOfParam = _value_cast(SizeOfParam, ctypes.c_uint)

    ret = _is_HotPixel(_hCam, _nMode, _pParam, _SizeOfParam)

    return ret


_is_AOI = _bind("is_AOI", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_AOI(hCam, nCommand, pParam, SizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _SizeOfParam = _value_cast(SizeOfParam, ctypes.c_uint)

    ret = _is_AOI(_hCam, _nCommand, _pParam, _SizeOfParam)

    return ret


_is_Transfer = _bind("is_Transfer", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Transfer(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_Transfer(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_BootBoost = _bind("is_BootBoost", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_BootBoost(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_BootBoost(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_DeviceFeature = _bind("is_DeviceFeature", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_DeviceFeature(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_DeviceFeature(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_Exposure = _bind("is_Exposure", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Exposure(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_Exposure(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_Trigger = _bind("is_Trigger", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Trigger(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_Trigger(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_DeviceInfo = _bind("is_DeviceInfo", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_DeviceInfo(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_DeviceInfo(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_OptimalCameraTiming = _bind("is_OptimalCameraTiming", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_OptimalCameraTiming(hCam, u32Command, pParam, u32SizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _u32Command = _value_cast(u32Command, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _u32SizeOfParam = _value_cast(u32SizeOfParam, ctypes.c_uint)

    ret = _is_OptimalCameraTiming(_hCam, _u32Command, _pParam, _u32SizeOfParam)

    return ret


_is_SetStarterFirmware = _bind("is_SetStarterFirmware", [ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint], ctypes.c_int)


def is_SetStarterFirmware(hCam, pcFilepath, uFilepathLen):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pcFilepath: c_char_p (aka c-type: const CHAR \*)
    :param uFilepathLen: c_uint (aka c-type: UINT)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_SetStarterFirmware is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)
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


def is_GetComportNumber(hCam, pComportNumber):
    """
    :param hCam: c_uint (aka c-type: HIDS)
    :param pComportNumber: c_uint (aka c-type: UINT \*)
    :returns: success, or no success, that is the answer
    :raises NotImplementedError: if function could not be loaded
    """
    if _is_GetComportNumber is None:
        raise NotImplementedError()

    _hCam = _value_cast(hCam, ctypes.c_uint)

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


def is_IO(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_IO(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_AutoParameter = _bind("is_AutoParameter", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_AutoParameter(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_AutoParameter(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_Convert = _bind("is_Convert", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Convert(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_Convert(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_ParameterSet = _bind("is_ParameterSet", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_ParameterSet(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_ParameterSet(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_EdgeEnhancement = _bind("is_EdgeEnhancement", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_EdgeEnhancement(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_EdgeEnhancement(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_PixelClock = _bind("is_PixelClock", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_PixelClock(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_PixelClock(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_ImageFile = _bind("is_ImageFile", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_ImageFile(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_ImageFile(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_Blacklevel = _bind("is_Blacklevel", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Blacklevel(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_Blacklevel(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_ImageBuffer = _bind("is_ImageBuffer", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_ImageBuffer(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_ImageBuffer(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_Measure = _bind("is_Measure", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Measure(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_Measure(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_LUT = _bind("is_LUT", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_LUT(hCam, nCommand, pParam, cbSizeOfParams):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParams = _value_cast(cbSizeOfParams, ctypes.c_uint)

    ret = _is_LUT(_hCam, _nCommand, _pParam, _cbSizeOfParams)

    return ret


_is_Gamma = _bind("is_Gamma", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Gamma(hCam, nCommand, pParam, cbSizeOfParams):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
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


def is_Multicast(hCam, nCommand, pParam, cbSizeOfParams):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParams = _value_cast(cbSizeOfParams, ctypes.c_uint)

    ret = _is_Multicast(_hCam, _nCommand, _pParam, _cbSizeOfParams)

    return ret


_is_Sequencer = _bind("is_Sequencer", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_Sequencer(hCam, nCommand, pParam, cbSizeOfParams):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParams = _value_cast(cbSizeOfParams, ctypes.c_uint)

    ret = _is_Sequencer(_hCam, _nCommand, _pParam, _cbSizeOfParams)

    return ret


_is_PersistentMemory = _bind("is_PersistentMemory", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_PersistentMemory(hCam, nCommand, pParam, cbSizeOfParam):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParam = _value_cast(cbSizeOfParam, ctypes.c_uint)

    ret = _is_PersistentMemory(_hCam, _nCommand, _pParam, _cbSizeOfParam)

    return ret


_is_PowerDelivery = _bind("is_PowerDelivery", [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint], ctypes.c_int)


def is_PowerDelivery(hCam, nCommand, pParam, cbSizeOfParams):
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

    _hCam = _value_cast(hCam, ctypes.c_uint)
    _nCommand = _value_cast(nCommand, ctypes.c_uint)
    _pParam = _pointer_cast(pParam, ctypes.c_void_p)
    _cbSizeOfParams = _value_cast(cbSizeOfParams, ctypes.c_uint)

    ret = _is_PowerDelivery(_hCam, _nCommand, _pParam, _cbSizeOfParams)

    return ret




