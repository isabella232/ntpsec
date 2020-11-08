#! /usr/bin/env python

"""tlscheck - Helper for checking SSL library bits."""
import ctypes
import ctypes.util
import sys
ver, vers = 0, []
try:
    tls = ctypes.CDLL(ctypes.util.find_library('ssl'))
except OSError:
    sys.stderr.write('Could not find SSL library.\n')
    sys.exit(1)

tls.OpenSSL_version_num.restype = ctypes.c_ulong
tls.OpenSSL_version.argtypes = [ctypes.c_int]
tls.OpenSSL_version.restype = ctypes.c_char_p

ver = tls.OpenSSL_version_num()  # unsigned long OpenSSL_version_num();

_ = '%08x' % ver
# OPENSSL_VERSION_NUMBER is a numeric release version identifier:
# MNNFFPPS: major minor fix patch status
for a, b in ((0, 1), (1, 3), (3, 5), (5, 7), (7, 8)):
    vers.append(int(_[a:b], 16))

polystr = str
if str is not bytes:
    def polystr(string):
        """Convert bytes into a string."""
        return str(string, encoding='latin-1')


def ver_to_int(*va):
    """Split the version number into parts."""
    return int('%x%02x%02x%02x%x' % va, 16)


def verstr():
    """Return SSL library version string."""
    return polystr(tls.OpenSSL_version(0))


def check_openssl_functions(ctx):
    """Check if several functions are in TLS library."""
    # (currently unused) intended to check for
    # OpenSSL functions not just the version
    funclist = [  # could be made long/short-er
        'SSL_CTX_set_alpn_protos',
        'SSL_CTX_set_alpn_select_cb',
        'SSL_export_keying_material',
        'SSL_get0_alpn_selected',
    ]
    output = True
    step = None
    for func in funclist:
        step = hasattr(tls, func)
        ctx.msg('Checking ssl for %s' % func,
                ('no', 'yes')[step])
        output &= step
    if not output:
        ctx.fatal('missing critical functionality')


def check_libssl_tls13(ctx):  # Does not catch non-OpenSSL implentation
    """Check badly if TLS1.3 is supported."""
    # (currently unused) intended to replace
    # check_libssl_tls13 from OpenSSL wafhelper
    _ = ver > ver_to_int(1, 1, 1, 0, 0)
    t = verstr()
    _ &= 'OpenSSL' in t
    ctx.msg('Checking for OpenSSL with TLSv1.3 support',
            ' '.join(t.split()[:2]))
    if not _:
        ctx.fatal('TLS library too old need 1.1.1b got %s' % verstr())
    return _


def check_openssl_bad_version(ctx):  # TODO: tighten bad version numbers
    """Check if version is not 1.1.1b prerelease or any 1.1.1a."""
    # (currently unused) intended to replace
    # check_openssl_bad_version from OpenSSL wafhelper
    if ver > ver_to_int(1, 1, 1, 2, 15):
        _ = True
    else:
        _ = ver < ver_to_int(1, 1, 1, 0, 0)
    ctx.msg('Checking for OpenSSL != 1.1.1a',
            ('no', 'yes')[_])
    if not _:
        ctx.fatal('')
    return _


def configure(ctx):
    """Pull in modules checks."""
    check_openssl_functions(ctx)


if __name__ == '__main__':
    if vers[0] > 2:  # If notionally OpenSSL 3
        sys.exit(0)
    elif vers[0] == 2:  # If notionally OpenSSL 2
        sys.exit(1)
    # OPENSSL_VERSION_NUMBER is a numeric release version identifier:
    # major minor fix patch status
    # Check if version is earlier than 1.1.1b
    if ver <= ver_to_int(1, 1, 1, 2, 15):
        sys.exit(1)
    sys.exit(0)
