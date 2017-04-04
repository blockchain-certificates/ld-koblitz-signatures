import json

import bitcoin
from bitcoin.signmessage import BitcoinMessage, SignMessage, VerifyMessage
from bitcoin.wallet import CBitcoinSecret
from pyld import jsonld
from pyld.jsonld import JsonLdProcessor
from werkzeug.contrib.cache import SimpleCache

from .document_loader import jsonld_document_loader

cache = SimpleCache()

SECURITY_CONTEXT_URL = 'https://w3id.org/security/v1'
algorithm = 'EcdsaKoblitzSignature2016'
PUBKEY_PREFIX = 'ecdsa-koblitz-pubkey:'


class SignatureOptions:
    def __init__(self, created, creator, domain=None, nonce=None):
        self.created = created
        self.creator = creator
        self.domain = domain
        self.nonce = nonce


def cached_document_loader(url, override_cache=False):
    if not override_cache:
        result = cache.get(url)
        if result:
            return result
    doc = jsonld_document_loader(url)
    cache.set(url, doc)
    return doc


def _getDataToHash(input, options):
    toHash = ''
    headers = {
        'http://purl.org/dc/elements/1.1/created': options.created,
        'https://w3id.org/security#domain': options.domain,
        'https://w3id.org/security#nonce': options.nonce
    }
    # add headers in lexicographical order
    import collections
    keys = collections.OrderedDict(sorted(headers.items()))
    for k, v in keys.items():
        if v:
            toHash += k + ': ' + v + '\n'
    toHash += input
    return toHash


def normalize_jsonld(json_ld_to_normalize):
    """
    Normalize the JSON-LD certificate
    :param certificate_json:
    :return:
    """
    options = {'algorithm': 'URDNA2015', 'format': 'application/nquads', 'documentLoader': cached_document_loader}
    normalized = jsonld.normalize(json_ld_to_normalize, options=options)
    return normalized


def verify(signed_json, options, chain_name='mainnet'):
    # options['expandContext': {'@vocab': 'https://fallback.org/'}]

    # compact to security context
    res = jsonld.compact(signed_json, SECURITY_CONTEXT_URL,
                         options={'documentLoader': cached_document_loader})
    signature = res['signature']['signatureValue']
    del res['signature']
    normalized = normalize_jsonld(res)
    to_hash = _getDataToHash(normalized, options=options)

    message = BitcoinMessage(to_hash)

    signing_key = options.creator[len(PUBKEY_PREFIX):]

    # TODO: obtain lock while modifying global state
    bitcoin.SelectParams(chain_name)
    return VerifyMessage(signing_key, message, signature)


def sign(to_sign, private_key, options, chain_name='mainnet'):
    import copy
    copy = copy.deepcopy(to_sign)
    if 'signature' in copy:
        del copy['signature']

    # normalize and get data to hash
    normalized = normalize_jsonld(to_sign)
    to_hash = _getDataToHash(normalized, options=options)

    # TODO: obtain lock while modifying global state
    bitcoin.SelectParams(chain_name)
    message = BitcoinMessage(to_hash)
    secret_key = CBitcoinSecret(private_key)
    signature = SignMessage(secret_key, message)

    # compact just signature part against all contexts
    signature_payload = {
        '@context': SECURITY_CONTEXT_URL,
        'type': algorithm,
        'creator': options.creator,
        'created': options.created,
        'signatureValue': signature.decode('utf-8')
    }

    tmp = {
        'https://w3id.org/security#signature': signature_payload
    }

    prev_contexts = JsonLdProcessor.get_values(to_sign, '@context')
    if not SECURITY_CONTEXT_URL in prev_contexts:
        prev_contexts.append(SECURITY_CONTEXT_URL)
    c = {'@context': prev_contexts}
    res = jsonld.compact(tmp, c, options={'documentLoader': cached_document_loader})
    copy['@context'] = prev_contexts
    copy['signature'] = res['signature']
    return copy


def main(args=None):
    with open('../tests/data/sample.json') as f:
        to_sign = json.load(f)
        result = sign(to_sign)
        print(result)

    with open('../tests/data/sample_signed.json') as f:
        to_verify = json.load(f)
        result = verify(to_verify)
        print(result)


if __name__ == '__main__':
    main()
