const crypto = require('crypto');
const fs = require('fs');
const stream = require('stream');
const tls = require('tls');

const dson = require('dogeon');

const salty_wow = 'suchdoge4evawow';
const hmac_key = crypto.pbkdf2Sync('such doge is yes wow', salty_wow, 4096, 16, 'sha256');
const aes_key = crypto.pbkdf2Sync('such doge is shibe wow', salty_wow, 4096, 16, 'sha256');

function encrypt(data) {
    let iv = Buffer.alloc(16, 0);
    let wow_cripter = crypto.createCipheriv('aes-128-cbc', aes_key, iv);
    wow_cripter.setAutoPadding(true);
    return Buffer.concat([wow_cripter.update(data), wow_cripter.final()]);
}

function decrypt(data) {
    let iv = Buffer.alloc(16, 0);
    let wow_decripter = crypto.createDecipheriv('aes-128-cbc', aes_key, iv);
    wow_decripter.setAutoPadding(true);
    return Buffer.concat([wow_decripter.update(data), wow_decripter.final()]);
}

function encode(message) {
    let json = JSON.parse(message.toString());
    let dsonBuf = Buffer.from(dson.stringify(json));
    let mbuf = encrypt(dsonBuf);
    let hmac = crypto.createHmac('sha256', hmac_key);
    hmac.update(mbuf);

    let chksum = hmac.digest();
    let buffer = Buffer.concat([chksum, mbuf]);

    let contentLength = Buffer.allocUnsafe(4);
    contentLength.writeUInt32BE(buffer.length);

    return Buffer.concat([contentLength, buffer]);
}

let encodeMessage = new stream.Transform();
encodeMessage._transform = function(chunk, encoding, done) {
    done(null, encode(chunk));
};


function parseMessage(received) {
    let hmac = crypto.createHmac('sha256', hmac_key);
    let checksum = received.slice(0, 32).toString('hex');
    let message = received.slice(32);
    hmac.update(message);

    let stupid = hmac.digest('hex');
    if (checksum === stupid) {
        let decrypted = decrypt(message).toString();
        return dson.parse(decrypted);
    }
}

const options = {
    ca: [fs.readFileSync('./auth/doge-ca.pem')],
    cert: fs.readFileSync('./auth/server-cert.pem'),
    key: fs.readFileSync('./auth/server-key.pem'),
    checkServerIdentity: () => undefined,
};

// const url = 'localhost';
const url = 'veryprotocol.challenges.adversary.zone';
var socket = tls.connect(41414, url, options, () => {
    console.log('client connected', socket.authorized ? 'authorized' : 'unauthorized');

    // stdin: {"dogesez":"do me a favor", "ohmaze":"cript(secrit_key, cript_key)"}
    process.stdin.pipe(encodeMessage).pipe(socket);
    process.stdin.resume();
});

socket.on('data', (data) => {
    let msg = parseMessage(data);
    if (msg) {
        console.log(msg);
    }
});

socket.on('end', () => {
    console.log('Ended')
    process.exit();
});
