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
usage: js_xxtea_decrypt.py [-h] -k key [-xs xor-signature] [-xk xor-key] [-bs] path
 
Decrypt files or folder using XXTEA.
 
positional arguments:
  path                  Path to the file or folder
 
optional arguments:
  -h, --help            show this help message and exit
  -k key, --key key     XXTEA Key
  -xs xor-signature, --xor-signature xor-signature
                        Signature in hex
  -xk xor-key, --xor-key xor-key
                        Xor-Key
  -bs, --beautify       Enables beautifying!

# for xxtea decryption only
$ python js_xxtea_decrypt.py apktool_out -k c79f28ea-34c1-42

# for xor or xor+xxtea (signature must be in hex to support unprintable bytes)
$ python js_xxtea_decrypt.py -k Za810xwef83lsa0A -xs "$(echo -en 'netease\x01\x01\x01\xef' | xxd -p)" -xk Wa810xwef83lsa0A enshtak_apktool/assets

# without using echo or xxd (signature must be in hex to support unprintable bytes)
$ python js_xxtea_decrypt.py -k Za810xwef83lsa0A -xs 6e657465617365010101ef -xk Wa810xwef83lsa0A enshtak_apktool/assets

```
