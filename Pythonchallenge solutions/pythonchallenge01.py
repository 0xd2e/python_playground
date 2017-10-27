#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/map.html


from string import ascii_lowercase


secret_message = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."

# Each letter in ascii_lowercase is replaced by a letter shifted by 2 positions
key = "".maketrans(ascii_lowercase, ascii_lowercase[2:] + ascii_lowercase[:2])

print("Secret message:", secret_message.translate(key))
print("Magic word:", "map".translate(key))
