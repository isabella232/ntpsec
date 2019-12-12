#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
"""Python wrapper for selected libntp C library routines."""
import ctypes
import errno
import os
import sys
import ntp.poly

TYPE_SYS = 1
TYPE_PEER = 2
TYPE_CLOCK = 3

# Add raw interface to libNTP.
_ntpc = None
_cwd = os.getcwd()
if 'ntpsec' in _cwd.split('/'):
    _paths = [
        'main/ntpd/',
        'build/main/ntpd/',
        '../../ntpd/',
        ]
else:
    _paths = ['@LIBDIR@/']

_loaded = False
for _path in _paths:
    try:
        if not _loaded:
            _ntpc = ctypes.CDLL('%slibntpc.so' % _path, use_errno=True)
            _loaded = True
            break
    except OSError:
        continue
if not _loaded:
    sys.stderr.write('Could not open libntpc.so\nExiting\n')
    exit(1)


def setprogname(in_string):
    """Set program name for logging purposes."""
    mid_bytes = ntp.poly.polybytes(in_string)
    _setprogname(mid_bytes)


def _lfp_wrap(callback, in_string):
    """NTP l_fp to other Python-style format."""
    mid_bytes = ntp.poly.polybytes(in_string)
    out_value = callback(mid_bytes)
    err = ctypes.get_errno()
    if err == errno.EINVAL:
        raise ValueError('ill-formed hex date')
    return out_value


def statustoa(i_type, i_st):
    """Convert a time stamp to something readable."""
    mid_str = _statustoa(i_type, i_st)
    return ntp.poly.polystr(mid_str)


def prettydate(in_string):
    """Convert a time stamp to something readable."""
    mid_str = _lfp_wrap(_prettydate, in_string)
    return ntp.poly.polystr(mid_str)


def lfptofloat(in_string):
    """NTP l_fp to Python-style float time."""
    return _lfp_wrap(_lfptofloat, in_string)


def msyslog(level, in_string):
    """Either send a message to the terminal or print it on the standard output."""
    mid_bytes = ntp.poly.polybytes(in_string)
    _msyslog(level, mid_bytes)


# Set return type and argument types of hidden ffi handlers
_msyslog = _ntpc.msyslog
_msyslog.restype = None
_msyslog.argtypes = [ctypes.c_int, ctypes.c_char_p]

_setprogname = _ntpc.ntpc_setprogname
_setprogname.restype = None
_setprogname.argtypes = [ctypes.c_char_p]

_prettydate = _ntpc.ntpc_prettydate
_prettydate.restype = ctypes.c_char_p
_prettydate.argtypes = [ctypes.c_char_p]

_lfptofloat = _ntpc.ntpc_lfptofloat
_lfptofloat.restype = ctypes.c_double
_lfptofloat.argtypes = [ctypes.c_char_p]

# Status string display from peer status word.
_statustoa = _ntpc.statustoa
_statustoa.restype = ctypes.c_char_p
_statustoa.argtypes = [ctypes.c_int, ctypes.c_int]


# Set time to nanosecond precision.
set_tod = _ntpc.ntpc_set_tod
set_tod.restype = ctypes.c_int
set_tod.argtypes = [ctypes.c_int, ctypes.c_int]

# Adjust system time by slewing.
adj_systime = _ntpc.ntpc_adj_systime
adj_systime.restype = ctypes.c_bool
adj_systime.argtypes = [ctypes.c_double]

# Adjust system time by stepping.
step_systime = _ntpc.ntpc_step_systime
step_systime.restype = ctypes.c_bool
step_systime.argtypes = [ctypes.c_double]
