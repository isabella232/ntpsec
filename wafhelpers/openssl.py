#! /usr/bin/env python

"""openssl - Helper for checking SSL library bits."""
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

SNIP_LIBSSL_TLS13_CHECK = """
#include <openssl/tls1.h>

#ifndef TLS1_3_VERSION
#error OpenSSL must have support for TLSv1.3
#endif

int main(void) {
    return 0;
}
"""

if str is bytes:
    polystr = str
else:
    def polystr(string):
        """Convert bytes into a string."""
        return str(string, encoding='latin-1')


def yesno(it):
    """Return a string depending on a (maybe) boolean."""
    if not it:
        return 'not found'
    if it is True:
        return 'yes'
    return it


def check_libssl_tls13(ctx):
    """Check if the OpenSSL define for TLS1.3 exists.."""
    ctx.check_cc(
        fragment=SNIP_LIBSSL_TLS13_CHECK,
        use="SSL CRYPTO",
        msg="Checking for OpenSSL with TLSv1.3 support",
    )


def configure(cfg):
    """Pull in modules checks."""
    check_libssl_tls13(cfg)
    eventual = bool(ver > 0x1010101f)
    checks = [['Checking for OpenSSL > 1.1.1a',
                polystr(tls.OpenSSL_version(0)).split()[1]]]
    funcs = [
        'SSL_CTX_set_alpn_protos',
        'SSL_CTX_set_alpn_select_cb',
        'SSL_export_keying_material',
        'SSL_get0_alpn_selected',
    ]
    interim = None
    for func in funcs:
        interim = hasattr(tls, func)
        eventual &= interim
        checks.append(['Checking ssl for %s' % func, yesno(interim)])
    for check in checks:
        cfg.msg(*check)
    if not eventual:
        print(vars(tls))
        cfg.fatal('missing NTS critical functionality')


if __name__ == '__main__':
    # import os
    import subprocess
    import tempfile

    class fake_context():
        """Fake having a waf install so all this can run inside waf or out."""
        right_shift = 0

        def msg(self, left, right):
            """Print out useful text messages."""
            dent = len(left)
            if dent > self.right_shift:
                self.right_shift = dent
            print('{1:{0}s} : {2:s}'.format(self.right_shift, left, right))

        def fatal(self, error):
            """Die in a fire."""
            print(error)
            sys.exit(1)

        def check_cc(self, fragment=None, use=None, msg=None):
            """compiler C code fragment with uses libraries printing msg.."""
            # if not (fragment and use and message):
                # self.fatal('Too dumb to live.')
            dent = len(msg)
            if dent > self.right_shift:
                self.right_shift = dent
            sys.stdout.write('{1:{0}s} : '.format(self.right_shift, msg))
            Popen = subprocess.Popen
            cflags = []
            for lib in use:
                p = Popen(['pkg-config', '--cflags-only-I', lib],
                          universal_newlines=True,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
                if p.returncode:
                    print('no pkg-config %s\n' % lib)
                    sys.exit(1)
                stdout, _ = p.communicate()
                cflags.append(stdout.strip())
            with tempfile.NamedTemporaryFile() as fp:
                fp.write(bytes(fragment, encoding='latin-1'))
                p = Popen(['cc', '-c'] + cflags + [fp.name],
                          universal_newlines=True,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
                if p.returncode:
                    print('no compile %d\n' % p.returncode)
                    sys.exit(1)
            print('yes')
            return 0

    context = fake_context()
    configure(context)
