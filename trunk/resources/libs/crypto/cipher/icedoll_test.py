#! /usr/bin/env python
""" crypto.cipher.icedoll_test

    Tests for icedoll encryption algorithm

    Copyright (c) (c) 2002 by Paul A. Lambert
    Read LICENSE.txt for license information.
"""
from crypto.cipher.icedoll  import Icedoll
from crypto.cipher.base     import noPadding
from binascii               import a2b_hex
from binascii_plus          import b2a_p, a2b_p
import unittest

class Icedoll_Basic_Tests(unittest.TestCase):
    """ Test Icedoll algorithm """

    def testDctEqPt(self):
        """ test of plaintext = decrypt(encrypt(plaintext)) """
        alg = Icedoll( 16*chr(0), padding=noPadding())
        pt  = 16*4*'a'             # block aligned
        ct  = alg.encrypt(pt)
        print 'ct  = ',b2a_p(ct)
        dct = alg.decrypt(ct)
        print 'dct = ',b2a_p(dct)
        assert(pt == dct), 'pt != dct'

        alg = Icedoll( 16*chr(0))  # autoPad
        pt  = 17*4*'a'             # non-block aligned
        ct  = alg.encrypt(pt)
        print 'ct  = ',b2a_p(ct)
        dct = alg.decrypt(ct)
        print 'dct = ',b2a_p(dct)
        assert(pt == dct), 'pt != dct'

    def xxxtestGladman_dev_vec(self):
        """ All 25 combinations of block and key size.
            These test vectors were generated by Dr Brian Gladman
            using the program aes_vec.cpp  <brg@gladman.uk.net> 24th May 2001.
            vectors in file: dev_vec.txt
            http://fp.gladman.plus.com/cryptography_technology/rijndael/index.htm
            note -> ket, pt the same .. ct different
        """
        def IcedollTestVec(i, key, pt, ct):
            """ Run single AES test vector with any legal blockSize
                and any legal key size. """
            bkey, plainText, cipherText = a2b_hex(key), a2b_hex(pt), a2b_hex(ct)
            kSize = len(bkey)
            bSize = len(cipherText) # set block size to length of block
            alg = Icedoll(bkey, keySize=kSize, blockSize=bSize, padding=noPadding())
            cct = alg.encrypt(plainText)
            print 'pt    =',b2a_p(plainText)
            print 'ct    =',b2a_p(cct)
            dcct = alg.decrypt(cct)
            #print '_dcct',b2a_p(dcct)
            self.assertEqual( dcct, plainText )
            self.assertEqual( alg.encrypt(plainText),  cipherText )
            self.assertEqual( alg.decrypt(cipherText), plainText )


        IcedollTestVec( i   = 'dev_vec.txt 16 byte block, 16 byte key',
                         key = '2b7e151628aed2a6abf7158809cf4f3c',
                         pt  = '3243f6a8885a308d313198a2e0370734',
                         ct  = '3925841d02dc09fbdc118597196a0b32')

        IcedollTestVec( i   = 'dev_vec.txt 16 byte block, 20 byte key',
                         key = '2b7e151628aed2a6abf7158809cf4f3c762e7160',
                         pt  = '3243f6a8885a308d313198a2e0370734',
                         ct  = '231d844639b31b412211cfe93712b880')

        IcedollTestVec( i   = 'dev_vec.txt 16 byte block, 24 byte key',
                         key = '2b7e151628aed2a6abf7158809cf4f3c762e7160f38b4da5',
                         pt  = '3243f6a8885a308d313198a2e0370734',
                         ct  = 'f9fb29aefc384a250340d833b87ebc00')

        IcedollTestVec( i   = 'dev_vec.txt 16 byte block, 28 byte key',
                         key = '2b7e151628aed2a6abf7158809cf4f3c762e7160f38b4da56a784d90',
                         pt  = '3243f6a8885a308d313198a2e0370734',
                         ct  = '8faa8fe4dee9eb17caa4797502fc9d3f')

        IcedollTestVec( i   = 'dev_vec.txt 16 byte block, 32 byte key',
                         key = '2b7e151628aed2a6abf7158809cf4f3c762e7160f38b4da56a784d9045190cfe',
                         pt  = '3243f6a8885a308d313198a2e0370734',
                         ct  = '1a6e6c2c662e7da6501ffb62bc9e93f3')


# Make this test module runnable from the command prompt
if __name__ == "__main__":
    unittest.main()


