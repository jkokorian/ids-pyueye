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

import os
import sys
import warnings
from ctypes import CDLL
from ctypes.util import find_library

__all__ = ["DLL"]


def _findlib(libnames, path=None):
    """
    """
    platform = sys.platform

    if platform in ("win32", "cli"):
        pattern = "{}.dll"
    elif platform == "darwin":
        pattern = "lib{}.dylib"
    else:
        pattern = "lib{}.so"

    searchfor = libnames
    if type(libnames) is dict:
        if platform not in libnames:
            platform = "DEFAULT"
            
        searchfor = libnames[platform]

    results = []
    if path:
        for libname in searchfor:
            for subpath in str.split(path, os.pathsep):
                dllfile = os.path.join(subpath, pattern.format(libname))
                
                if os.path.exists(dllfile):
                    results.append(dllfile)

    for libname in searchfor:
        dllfile = find_library(libname)
        
        if dllfile:
            results.append(dllfile)

    return results


class DLL(object):
    """
    Function wrapper around the different DLL functions. Do not use or
    instantiate this one directly from your user code.
    """
    def __init__(self, libinfo, libnames, path=None):
        self._dll = None
        foundlibs = _findlib(libnames, path)
        dllmsg = "DLL_PATH: {}".format(path or "unset")
        if not foundlibs:
            raise RuntimeError("could not find any library for {} ({})".format(libinfo, dllmsg))

        for libfile in foundlibs:
            try:
                self._dll = CDLL(libfile)
                self._libfile = libfile
                break
            except Exception as exc:
                warnings.warn(repr(exc), ImportWarning)

        if self._dll is None:
            raise RuntimeError("found {}, but it's not usable for the library {}".format(foundlibs, libinfo))

        if path is not None and sys.platform in ("win32", "cli") and \
            path in self._libfile:
            os.environ["PATH"] = "{};{}".format(path, os.environ["PATH"])

    def bind_function(self, funcname, args=None, returns=None, optfunc=None):
        """
        Binds the passed argument and return value types to the specified
        function.
        """
        func = getattr(self._dll, funcname, None)

        if not func:
            if optfunc:
                warnings.warn("function '{}' not found in {!r}, using replacement".format(funcname, self._dll), ImportWarning)
                func = _nonexistent(funcname, optfunc)

        if func:
            func.argtypes = args
            func.restype = returns
        else:
            warnings.warn("function '{}' not found in {!r}".format(funcname, self._dll), ImportWarning)

        return func

    @property
    def libfile(self):
        """
        Gets the filename of the loaded library.
        """
        return self._libfile


def _nonexistent(funcname, func):
    """
    A simple wrapper to mark functions and methods as nonexistent.
    """
    def wrapper(*fargs, **kw):
        warnings.warn("{} does not exist".format(funcname), category=RuntimeWarning, stacklevel=2)

        return func(*fargs, **kw)

    wrapper.__name__ = func.__name__

    return wrapper


def load_dll(libinfo, libnames, envname=None):
    """
    DDL loadfunction.
    :param libinfo: DLL name
    :param libnames: DLL names
    :param envname: used environment variable
    :returns: libfile and bind function
    :raises ImportError: if DLL was not found
    """
    try:
        dll = DLL(libinfo, libnames, os.getenv(envname))
    except RuntimeError as exc:
        raise ImportError(exc)
        
    return dll.libfile, dll.bind_function
    
