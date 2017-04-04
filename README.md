
[![PyPI version](https://badge.fury.io/py/cert-core.svg)](https://badge.fury.io/py/cert-core)


# ld-koblitz-signatures

A minimal implementation of the EcdsaKoblitzSignature2016 JSON-LD signature, signing and verification. This is used by Blockcerts cert-verifier and cert-issuer for signing and verification. 

Keep in mind that, in contrast to the [jsonld-signatures javascript library](https://github.com/digitalbazaar/jsonld-signatures) implementation, this minimal implementation currently lacks additional checks that should be performed (issuer keys, dates, etc). Therefore this library should not be used as a standalone verifier in the current state. The Blockcerts project uses this library COMBINED with cert-verifier to ensure the additional checks are performed.



## Contact

Contact [info@blockcerts.org](mailto:info@blockcerts.org) with questions
