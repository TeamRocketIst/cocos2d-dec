### Linux:
```bash
$ apt update && apt install cmake
```

### Mac-os:
```bash
$ brew install cmake
```

### Compile xxtea lib
```
$ cmake .
$ make
```

Create a virtualenv and install python dependencies:
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Unpack apk with `unzip` or `apktool`:
```bash
$ apktool d -r -s -f base.apk -o apktool_out 
```

For cocos2d-lua:
```bash
$ python lua_xxtea_decrypt.py -h
usage: lua_xxtea_decrypt.py [-h] -k key -s signature path

Decrypt files or folder using XXTEA.

positional arguments:
  path                  Path to the file or folder

optional arguments:
  -h, --help            show this help message and exit
  -k key, --key key     XXTEA Key
  -s signature, --signature signature
                        Signature
$ python lua_xxtea_decrypt.py apktool_out -k cocos2d_lua_ks -s LJ
 Decrypting apktool_out/assets/base/src/config.luac
 apktool_out/assets/base/src/config.luac
 Decrypting apktool_out/assets/base/src/main.luac
 apktool_out/assets/base/src/main.luac
 Decrypting apktool_out/assets/base/src/app/MyApp.luac
 apktool_out/assets/base/src/app/MyApp.luac
```

For cocos2d-js run:
```bash
$ python js_xxtea_decrypt.py -h
usage: js_xxtea_decrypt.py [-h] -k key path

Decrypt files or folder using XXTEA.

positional arguments:
  path               Path to the file or folder

optional arguments:
  -h, --help         show this help message and exit
  -k key, --key key  XXTEA Key
$ python js_xxtea_decrypt.py apktool_out -k c79f28ea-34c1-42
 Decrypting apktool_out/assets/assets/internal/index.jsc
 Beautifying
 apktool_out/assets/assets/internal/index.js
 Decrypting apktool_out/assets/assets/main/index.jsc
 Beautifying
 apktool_out/assets/assets/main/index.js
 Decrypting apktool_out/assets/src/settings.jsc
 Beautifying
 apktool_out/assets/src/settings.js
 Decrypting apktool_out/assets/src/cocos2d-jsb.jsc
 Beautifying
 apktool_out/assets/src/cocos2d-jsb.js
```
