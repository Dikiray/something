from os import urandom
import json
import base64
from random import randint

import flask
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import jwt


with open("jwt_secret.bin", "rb") as f:
    jwt_secret = f.read()
with open("key.pub", "rb") as f:
    pubkey = RSA.importKey(f.read())
with open("key.pem", "rb") as f:
    privkey = RSA.importKey(f.read())


encryptor = PKCS1_OAEP.new(pubkey)
decryptor = PKCS1_OAEP.new(privkey)


def encrypt_data(data):
    return base64.b85encode(encryptor.encrypt(data))

def decrypt_data(data):
    return decryptor.decrypt(base64.b85decode(data))


def pack_jwt(payload, do_encryption=True):
    encoded = json.dumps(payload).encode('utf-8')
    if do_encryption:
        encoded = encrypt_data(encoded)
    b64ed = base64.b64encode(encoded).decode('utf-8')
    return jwt.encode({'encrypted_data': b64ed}, jwt_secret)

def unpack_jwt(data, is_encrypted=True):
    if is_encrypted:
        b64ed = jwt.decode(data, jwt_secret)['encrypted_data']
    else:
        b64ed = jwt.decode(data, jwt_secret)['unencrypted_data']
    encrypted = base64.b64decode(b64ed.encode('utf-8')).decode('utf-8')
    return json.loads(decrypt_data(encrypted).decode('utf-8'))


app = flask.Flask(__name__)


default_jwt = pack_jwt({'x': 0, 'y': 0, 'score': 0})


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/trial')
def trial():
    return flask.render_template('trial.html')

@app.route('/game')
def game():
    data = flask.request.cookies.get('gamedata')
    if data is None:
        data = default_jwt
    data = unpack_jwt(data)

    resp = flask.make_response(flask.render_template('game.html', score=data['score']))

    if 'gamedata' not in flask.request.cookies.keys():
        resp.set_cookie('gamedata', pack_jwt(data).decode('utf-8'))

    return resp

@app.route('/send', methods=['POST'])
def send():
    sent_json = flask.request.get_json()

    # sent x, sent y
    sx, sy = sent_json['x'], sent_json['y']

    gamedata = unpack_jwt(flask.request.cookies['gamedata'])
    # actual x, actual y
    ax, ay = gamedata['x'], gamedata['y']

    if sx == ax and sy == ay:
        gamedata['x'] = randint(0, sent_json['winx']-1)
        gamedata['y'] = randint(0, sent_json['winy']-1)
        gamedata['score'] = gamedata['score'] + 1

        if gamedata['score'] >= 10**4:
            resp = flask.jsonify({'ok': True, 'bingo': True,
                'next_url': '/lets_finally_get_flag'})
        else:
            resp = flask.jsonify({'ok': True, 'bingo': True})

        resp.set_cookie('gamedata', pack_jwt(gamedata))
    else:
        resp = flask.jsonify({'ok': True, 'bingo': False})

    return resp

@app.route('/lets_finally_get_flag')
def lets_finally_get_flag():
    return 'Ну пипец)<br><br>PB{u_r_a_cr33py_st41k3r}'


if __name__ == "__main__":
    app.run('0.0.0.0', debug=False)
