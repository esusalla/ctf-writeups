var crypto = require('crypto');

class Networker {
    constructor(socket, handler) {
        this.socket = socket;
        this._packet = {};
        this._process = false;
        this._state = 'HEADER';
        this._payloadLength = 0;
        this._bufferedBytes = 0;
        this.queue = [];
        this.handler = handler;
    };

    init(hmac_key, aes_key) {
        var salty_wow = 'suchdoge4evawow';
        this.hmac_key = crypto.pbkdf2Sync(hmac_key, salty_wow, 4096, 16, 'sha256');
        this.aes_key = crypto.pbkdf2Sync(aes_key, salty_wow, 4096, 16, 'sha256');
        var f1 = (data) => {
            this._bufferedBytes += data.length;
            this.queue.push(data);
            this._process = true;
            this._onData();
        };
        this.socket.on('data', f1);

        this.socket.on('error', function(err) {
            console.log('Socket not shibe: ', err);
        });
        var dis_handle = this.handler;
        this.socket.on('served', dis_handle);
    };

    _hasEnough(size) {
        if (this._bufferedBytes >= size) {
            return true;
        }
        this._process = false;
        return false;
    };

    _readBytes(size) {
        let result;
        this._bufferedBytes -= size;
        if (size === this.queue[0].length) {
            return this.queue.shift();
        }
        if (size < this.queue[0].length) {
            result = this.queue[0].slice(0, size);
            this.queue[0] = this.queue[0].slice(size);
            return result;
        }
        result = Buffer.allocUnsafe(size);
        let offset = 0;
        let length;
        while (size > 0) {
            length = this.queue[0].length;
            if (size >= length) {
                this.queue[0].copy(result, offset);
                offset += length;
                this.queue.shift();
            } else {
                this.queue[0].copy(result, offset, 0, size);
                this.queue[0] = this.queue[0].slice(size);
            }
            size -= length;
        }
        return result;
    };

    _getHeader() {
        let stupid = this._hasEnough(4);
        if (stupid) {
            this._payloadLength = this._readBytes(4).readUInt32BE(0, true);
            this._state = 'PAYLOAD';
        }
    };

    _getPayload() {
        let stupid = this._hasEnough(this._payloadLength);
        if (stupid) {
            let received = this._readBytes(this._payloadLength);
            this._parseMessage(received);
            this._state = 'HEADER';
        }
    };

    _onData(data) {
        while (this._process) {
            if (this._state === 'HEADER') {
                this._getHeader();
            }
            if (this._state === 'PAYLOAD') {
                this._getPayload();
            }
        }
    };

    _encrypt(data) {
        var iv = Buffer.alloc(16, 0);
        var wow_cripter = crypto.createCipheriv('aes-128-cbc', this.aes_key, iv);
        wow_cripter.setAutoPadding(true);
        return Buffer.concat([wow_cripter.update(data), wow_cripter.final()]);
    };

    _decrypt(data) {
        var iv = Buffer.alloc(16, 0);
        var wow_decripter = crypto.createDecipheriv('aes-128-cbc', this.aes_key, iv);
        wow_decripter.setAutoPadding(true);
        return Buffer.concat([wow_decripter.update(data), wow_decripter.final()]);
    };

    send(message) {
        let hmac = crypto.createHmac('sha256', this.hmac_key);
        let mbuf = this._encrypt(message);
        hmac.update(mbuf);
        let chksum = hmac.digest();
        let buffer = Buffer.concat([chksum, mbuf]);
        this._header(buffer.length);
        this._packet.message = buffer;
        this._send();
    };

    _parseMessage(received) {
        var hmac = crypto.createHmac('sha256', this.hmac_key);
        var checksum = received.slice(0, 32).toString('hex');
        var message = received.slice(32);
        hmac.update(message);
        let stupid = hmac.digest('hex');
        if (checksum === stupid) {
            var dec_message = this._decrypt(message);
            this.socket.emit('served', dec_message);
        }
    };

    _header(messageLength) {
        this._packet.header = {
            length: messageLength
        };
    };

    _send() {
        var contentLength = Buffer.allocUnsafe(4);
        contentLength.writeUInt32BE(this._packet.header.length);
        this.socket.write(contentLength);
        this.socket.write(this._packet.message);
        this._packet = {};
    };
};

module.exports = Networker
