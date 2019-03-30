import hashlib
import ecdsa


def generate_citizen_pub_priv_key():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    print(sk, vk)
    return {"citizen_public_id": vk, "citizen_private_id": sk}


def sign_vote(sk, vote):
    message = bytes(str(vote),  'utf-8')
    signed_vote = sk.sign(message)
    return signed_vote


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


if __name__ == "__main__":
    generate_citizen_pub_priv_key()

