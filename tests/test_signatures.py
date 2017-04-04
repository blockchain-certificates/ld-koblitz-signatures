import json
import unittest

from ld_koblitz_signatures import signatures
from ld_koblitz_signatures.signatures import SignatureOptions

private_key = 'L4mEi7eEdTNNFQEWaa7JhUKAbtHdVvByGAqvpJKC53mfiqunjBjw'
created = '2017-03-24T21:48:24Z'
creator = 'ecdsa-koblitz-pubkey:1LGpGhGK8whX23ZNdxrgtjKrek9rP4xWER'


class TestSignatures(unittest.TestCase):
    def test_sign(self):
        with open('data/sample.json') as f:
            to_sign = json.load(f)
            options = SignatureOptions(created, creator)
            result = signatures.sign(to_sign, private_key, options)
            verify_result = signatures.verify(result, options)
            self.assertTrue(verify_result)

    def test_verify(self):
        with open('data/sample_signed.json') as f:
            to_verify = json.load(f)
            options = SignatureOptions(created, creator)
            result = signatures.verify(to_verify, options)
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
