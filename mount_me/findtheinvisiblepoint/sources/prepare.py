from os import urandom

from Crypto.PublicKey import RSA


if __name__ == "__main__":
    with open("jwt_secret.bin", "wb") as f:
        f.write(urandom(48))

    key = RSA.generate(1024)
    with open("key.pub", "wb") as f:
        f.write(key.publickey().exportKey())
    with open("key.pem", "wb") as f:
        f.write(key.exportKey())
