#!/usr/bin/python3

# http://www.pythonchallenge.com/pc/def/integrity.html


import bz2


username = bz2.decompress(b'BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084')  # pylint: disable=C0301
password = bz2.decompress(b'BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08')  # pylint: disable=C0301

print('Hidden link:', 'http://www.pythonchallenge.com/pc/return/good.html')
print('Username:', username.decode('utf-8'))
print('Password:', password.decode('utf-8'))
