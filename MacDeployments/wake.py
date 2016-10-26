__author__ = 'jquintanilla'
from wakeonlan import wol

wol.send_magic_packet('c8.2a.14.5b.26.f4',ip_address='192.168.1.206',port=43)
