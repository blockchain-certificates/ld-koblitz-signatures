import base64
import json

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def get_hash(json_ld):
    """
    Normalize and hash the json-ld document
    """
    options = {'algorithm': 'URDNA2015', 'format': 'application/nquads',
               'documentLoader': cached_document_loader}
    normalized = jsonld.normalize(to_sign, options=options)
    normalized_hash = SHA256.new(data=normalized.encode()).digest()
    return normalized_hash


def prepare_payload(payload, header=None):
    """
    Prepare the payload to sign including the protected header as per
    RFC 7797
    """
    if not header:
        header = {'alg': 'RS256', 'b64': False, 'crit': ['b64']}

    header_str = json.dumps(header, separators=(',', ':'), sort_keys=True).encode('utf-8')
    encoded_header = base64.urlsafe_b64encode(header_str).replace(b'=', b'')
    return b'.'.join([encoded_header, payload])


def sign_rs256(payload, private_key):
    """
    Produce a RS256 signature of the payload
    """
    key = RSA.importKey(private_key)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA256.new(payload))
    return signature


def sign(payload, private_key):
    """
    Produce a RS256 jws signature with unencoded payload as per RFC 7797
    """
    prepared_payload = prepare_payload(payload)
    print(prepared_payload)
    print(private_key)
    signature = sign_rs256(prepared_payload, private_key)
    return base64.urlsafe_b64encode(signature).replace(b'=', b'')


def verify_jws(signed_json, public_key, options=None):
    "Verify a jws signature"

    # 1. normalize
    # 2. sha256 hash
    # 3. RS256 verify


