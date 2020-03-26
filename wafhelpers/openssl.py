import ctypes


def check_SSL_version(ctx):
    lib = ctypes.CDLL("libcrypto.so")
    version_int = lib.OpenSSL_version_num()
    # version = struct.unpack('cccc', version_int)
    lib.OpenSSL_version.restype = ctypes.c_char_p
    version_string = '%d.%d.%d%s' % (
                     (version_int >> 28) & 0xff,
                     (version_int >> 20) & 0xff,
                     (version_int >> 12) & 0xff,
                     (version_int >> 4) & 0xff and chr(
                      ord('a') - 1 + ((version_int >> 4) & 0xf)) or '')
    valid = (version_int > 0x1010101f)
    color = 'GREEN' if valid else 'YELLOW'
    ctx.msg("Checking for openssl %s > 1.1.1a" %
            version_string, 'yes' if valid else 'no', color=color)
    if not valid:
        ctx.fatal('openssl %s too old' % version_string)
