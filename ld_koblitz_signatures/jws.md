# Python Implementation of JSON-LD JSON Web Signatures

The goal was to provide and implementation of JSON-LD signatures in which the
`SignatureValue` field is replaced with a JSON Web Signature as described in
the [RSA Signature Suite 2017](https://w3c-dvcg.github.io/lds-rsa2017/) spec.

More specifically we implement a subset of the [JSON Web Signature Unencoded Payload
Option RFC 7797](https://datatracker.ietf.org/doc/html/rfc7797). The only
supported algorithm is __RS256__.

## Implementation

This implementation is currently python3 only.

We only found one _JOSE_ [implementation](https://github.com/Spomky-Labs/jose)
that implemented the RFC 7797 spec and used it to test this implementation.

A modified version of an [unencoded unit test] was used:
```php

```
This tests uses the `{"alg":"RS256","b64":false,"crit":["b64"]}` header and
`$.02` as the unencoded payload.

The input of the signing function should match `eyJhbGciOiJSUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19.$.02`
and the resulting signature should match `eyJhbGciOiJSUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..fZRkjTTrcXdUovHjghM6JvlMhJuR1s8X1F4Uy_F4oMhZ9KtF2Zp78lYSOI7OxB5uoTu8FpQHvy-dz3N4nLhoSWAi2_HrxZG_2DyctUUB_8pRKYBmIdIgpOlEMjIreOvXyM6A32gR-PdbzoQq14yQbbfxk12jyZSwcaNu29gXnW_uO7ku1GSV_juWE5E_yIstvEB1GG8ApUGIuzRJDrAAa8KBkHN7Rdfhc8rJMOeSZI0dc_A-Y7t0M0RtrgvV_FhzM40K1pwr1YUZ5y1N4QV13M5u5qJ_lBK40WtWYL5MbJ58Qqk_-Q8l1dp6OCmoMvwdc7FmMsPigmyklqo46uyjjw`

Currently the code is able to construct the correct unencoded payload from the
headers and the json-ld document and produce a correct signature.

## Problems encountered

#### JSON Normalization

The biggest we encountered was how do I normalize a json document in a
consistent/deterministic way so that I can hash or sign and make sure that any
implementation in any language is able to produce the same signature or verify
a that a signature.

In fact 70% percent of time in this code was spent debugging why this code was
not able to produce the same signature that was being generated with both the
php implementation and the javascript implementation from @kimdhamilton.

Example:
```python
import json

header = {'alg': 'RS256', 'b64': False, 'crit': ['b64']}

# stringigy json
# there are no guarantees about the ordering of the keys and the separators use
# a whitespace between the keys
json.dumps(header)
'{"crit": ["b64"], "alg": "RS256", "b64": false}'

# we can specify the separators. In this case we say we don't want whitespaces
json.dumps(header, separators=(',', ':'))
'{"crit":["b64"],"alg":"RS256","b64":false}'

# and we can specify the ordering of the keys
json.dumps(header, separators=(',', ':'), sort_keys=True)
'{"alg":"RS256","b64":false,"crit":["b64"]}'

# ultimately we can specify the encoding to use and return a bytestring that
can then be used to base64 encode / sign / hash
json.dumps(header, separators=(',', ':'), sort_keys=True).encode('utf-8')
b'{"alg":"RS256","b64":false,"crit":["b64"]}'
```

Specifying the sorting of the keys, the separators and the encoding should be
enough for any implementation to be able to produce the same signature. Note
that this is not critical since the encoded header is included in the signature
but this also means that the same payload can produce different signatures.
JSON-LD signatures don't have this problem but by replacing its signature with
a JWS this is introduced because we need to deal with the JWS json header.

To my knowledge the _JOSE_ specs to not specify how you should normalize json
(maybe I am wrong @msporny).


JSON-LD does not suffer from this problem since the [normalization spec](http://json-ld.github.io/normalization/spec/)
provides deterministic way of normalizing JSON-LD so its easy for any
implementation to generate the same hash of a normalized JSON-LD document.


### TODO:
- Better scope out what we want to provide in terms of code.
    - This relates to both json-ld and jws
    - Json-ld is already [implemented in python](https://github.com/digitalbazaar/pyld)
    - JWS implementations are lacking and to my knowledge there are no RFC 7797
      python implementations.
    - Should we just provide a RFC 7797 implementation (with a least RS256) and
      use it with `PyLD` to provide jws ld-signatures?
- Finalize the code and host the repo under the rebooting web of trust
  organization
- Document the library
- Provide input for the RSA Signature Suite Spec, specially to the sections
  about the modifications to the signature and verification algorithms.
