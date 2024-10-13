import ctypes, argparse, os, gzip, jsbeautifier, zlib, binascii, platform
from ctypes import c_char_p, c_ulong
from io import BytesIO
import zipfile 

def beautify_js(data):
    options = jsbeautifier.default_options()
    options.indent_size = 2
    options.indent_char = " "
    options.preserve_newlines = True
    options.jslint_happy = False
    options.keep_array_indentation = False
    options.brace_style = "collapse"
    options.indent_level = 0
    options.indent_with_tabs = 0
    options.keep_function_indentation = 1
    return jsbeautifier.beautify(data.decode(), options).encode()

def xor_decrypt(data):
    data_out = bytearray()
    sign = args.xor_signature if args.xor_signature else ""
    sign = binascii.unhexlify(sign)#bytes([ord(char) for char in sign])
    #print(bytes(sign))
    # ignoring for now the versions that don't have signature
    if sign != "" and (data.startswith(sign) or data.endswith(sign)):
        data = data[len(sign):] if data.startswith(sign) else data[:-len(sign)]
        for i,c in enumerate(data):
            data_out.append(c ^ ord(args.xor_key[i% len(args.xor_key)]))
    else:
        data_out = data
    return bytes(data_out)

def write_file(file_path, data):
    with open(file_path, 'wb') as f:
        if (file_path.endswith('.js') or file_path.endswith('.js') or file_path.endswith('.json')) and args.beautify:
            print("\033[96m %s \033[0m" % ("Beautifying "), end="\n")
            beautified = beautify_js(data)
        else:
            beautified = data
        f.write(bytes(beautified))
        #if args.xor_key:
        print("\033[1;32m %s \033[0m" % file_path, end="\n")


def decrypt_file(file_path, xxtea_key, xxtea_decrypt):
    with open(file_path, 'rb') as f:
        if args.xor_key:
            print("\033[93m %s \033[0m" % ("Decrypting "+file_path), end="\n")
            data = xor_decrypt(f.read())
        else:
            data = f.read()
    if data and file_path.endswith('.jsc'):
        data_len = len(data)
        key = xxtea_key
        key_len = len(key)
        ret_len = ctypes.c_ulong()
        print("\033[93m %s \033[0m" % ("Decrypting "+file_path), end="\n")
        result = xxtea_decrypt(data, data_len, key, key_len, ctypes.byref(ret_len))
        #print(ret_len.value)
        decrypted_data = ctypes.string_at(result, ret_len.value)
        if ret_len.value > 0:
            if decrypted_data[:2] == b"PK":
                fio = BytesIO(decrypted_data)
                fzip = zipfile.ZipFile(file=fio)
                decrypted_data = fzip.read(fzip.namelist()[0])
                write_file(file_path.replace('.jsc','.js'), decrypted_data)
            elif decrypted_data[:2] == b"\x1f\x8b":
                write_file(file_path.replace('.jsc','.js'), zlib.decompress(decrypted_data, 16 + zlib.MAX_WBITS))
            else:
                try:
                    write_file(file_path.replace('.jsc','.js'), decrypted_data)
                except UnicodeDecodeError:
                    print("\033[1;31m %s \033[0m" % ("Wrong key maybe ?? "+file_path), end="\n")
        else:
            print("\033[1;31m %s \033[0m" % ("something went wrong decryption the file "+file_path), end="\n")
    elif data:
        write_file(file_path, data)


def decrypt_folder(path, xxtea_key, xxtea_decrypt):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if args.xor_key or file_path.endswith('jsc'):
                    decrypt_file(file_path, xxtea_key, xxtea_decrypt)
    else:
        if args.xor_key or file_path.endswith('jsc'):
            decrypt_file(path, xxtea_key, xxtea_decrypt)

def main():
    global args
    parser = argparse.ArgumentParser(description='Decrypt files or folder using XXTEA.')
    parser.add_argument("path", metavar="path", type=str, help="Path to the file or folder")
    parser.add_argument("-k", '--key',metavar='key', type=str, required=True, help="XXTEA Key")
    parser.add_argument("-xs", '--xor-signature', metavar='xor-signature', type=str, required=False, help="Signature in hex")
    parser.add_argument("-xk", '--xor-key', metavar='xor-key', type=str, required=False, help="Xor-Key")
    parser.add_argument("-bs", '--beautify', action="store_true", required=False, help="Enables beautifying!")

    args = parser.parse_args()
    my_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib/libext_xxtea'\
        +".so" if platform.system() == "Linux" else ".dynlib" if platform.system()== 'Darwin' else ".so")) 
    xxtea_decrypt = my_lib.xxtea_decrypt
    xxtea_decrypt.argtypes = [c_char_p, c_ulong, c_char_p, c_ulong, ctypes.POINTER(c_ulong)]
    xxtea_decrypt.restype = ctypes.POINTER(ctypes.c_ubyte)
    
    decrypt_folder(args.path, args.key.encode(), xxtea_decrypt)

if __name__ == '__main__':
    args = None
    main()
