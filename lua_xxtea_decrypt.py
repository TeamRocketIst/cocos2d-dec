import ctypes, argparse, os
from ctypes import c_char_p, c_ulong


def decrypt_file(file_path, signature, xxtea_key, xxtea_decrypt):
    sign_size = len(signature)
    with open(file_path, 'rb') as f:
        data = f.read()
    
    if data and data.startswith(signature):
        if len(data) == len(signature):
            with open(file_path, 'wb'= as f:
                f.write(b"")
            print("\033[1;32m %s \033[0m" % file_path, end="\n")
            return
        data = data[sign_size:]
        data_len = len(data)
        key = xxtea_key
        key_len = len(key)
        ret_len = ctypes.c_ulong()
        print("\033[93m %s \033[0m" % ("Decrypting "+file_path), end="\n")
        result = xxtea_decrypt(data, data_len, key, key_len, ctypes.byref(ret_len))
        decrypted_data = ctypes.string_at(result, ret_len.value)
        if (ret_len.value != 0):
            with open(file_path, 'wb') as f:
                f.write(decrypted_data)
            print("\033[1;32m %s \033[0m" % file_path, end="\n")
        else:
            print("\033[1;31m %s \033[0m" % ("something went wrong decryption the file "+file_path), end="\n")

def decrypt_folder(path, signature, xxtea_key, xxtea_decrypt):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                decrypt_file(file_path, signature, xxtea_key, xxtea_decrypt)
    else:
        decrypt_file(path, signature, xxtea_key, xxtea_decrypt)
def main():
    parser = argparse.ArgumentParser(description='Decrypt files or folder using XXTEA.')
    parser.add_argument("path", metavar="path", type=str, help="Path to the file or folder")
    parser.add_argument("-k", '--key',metavar='key', type=str, required=True, help="XXTEA Key")
    parser.add_argument("-s", '--signature', metavar='signature', type=str, required=True, help="Signature")
    args = parser.parse_args()
    my_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib/libext_xxtea.dylib'))
    xxtea_decrypt = my_lib.xxtea_decrypt
    xxtea_decrypt.argtypes = [c_char_p, c_ulong, c_char_p, c_ulong, ctypes.POINTER(c_ulong)]
    xxtea_decrypt.restype = ctypes.POINTER(ctypes.c_ubyte)
    decrypt_folder(args.path, args.signature.encode(), args.key.encode(), xxtea_decrypt)

if __name__ == '__main__':
    main()
