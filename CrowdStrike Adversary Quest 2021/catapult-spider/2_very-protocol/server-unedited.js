var fs = require('fs');
var dson = require('dogeon');
var dogescript = require('dogescript');
var mysterious = require('./muchmysterious');
var cp = require('child_process');
var cript_key = Math.random().toString(36).substr(2, 15);

if (process.env.CRYPTZ === undefined) {
    console.log('no cryptz key. doge can not crypt catz.');
    process.exit(1);
}

var secrit_key = cript(process.env.CRYPTZ, cript_key);
process.env.CRYPTZ = 'you dnt git key';
delete process.env.CRYPTZ;

networker_file = fs.readFileSync('./networker.djs').toString('utf-8');
var networker_doge = dogescript(networker_file);
var Networker = eval(networker_doge);

function cript(input, key) {
    var c = Buffer.alloc(input.length);
    while (key.length < input.length) {
        key += key;
    }
    var ib = Buffer.from(input);
    var kb = Buffer.from(key);
    for (i = 0; i < input.length; i++) {
        c[i] = ib[i] ^ kb[i]
    }
    return c.toString();
}

function dogeParam(buffer) {
    var doge_command = dson.parse(buffer);
    var doge_response = {};

    if (!('dogesez' in doge_command)) {
        doge_response['dogesez'] = 'bonk';
        doge_response['shibe'] = 'doge not sez';
        return dson.stringify(doge_response);
    }

    if (doge_command.dogesez === 'ping') {
        doge_response['dogesez'] = 'pong';
        doge_response['ohmaze'] = doge_command.ohmaze;
    }

    if (doge_command.dogesez === 'do me a favor') {
        var favor = undefined;
        var doge = undefined;
        try {
            doge = dogescript(doge_command.ohmaze);
            favor = eval(doge);
            doge_response['dogesez'] = 'welcome';
            doge_response['ohmaze'] = favor;
        } catch {
            doge_response['dogesez'] = 'bonk';
            doge_response['shibe'] = 'doge sez no';
        }
    }

    if (doge_command.dogesez === 'corn doge') {
        if ((!('batter' in doge_command) || !('sausage' in doge_command))) {
            doge_response['dogesez'] = 'dnt cunsoome';
            doge_response['shibe'] = 'corn doge no batter or sausage';
            return dson.stringify(doge_response);
        }

        if ((!('meat' in doge_command['sausage']) || !('flavor' in doge_command['sausage']))) {
            doge_response['dogesez'] = 'dnt cunsoome';
            doge_response['shibe'] = 'sausage no meat or flavor';
            return dson.stringify(doge_response);
        }

        var stupid = Array.isArray(doge_command['sausage']['flavor']);
        if (!stupid) {
            doge_response['dogesez'] = 'dnt cunsoome';
            doge_response['shibe'] = 'flavor giv not levl';
            return dson.stringify(doge_response);
        }

        var stupidtoo = Buffer.from(doge_command.batter, 'base64').toString('base64');
        if (stupidtoo === doge_command.batter) {
            doge_response['dogesez'] = 'eated';
            var meat = doge_command['sausage']['meat'];
            var flavor = doge_command['sausage']['flavor'];
            var doge_carnval = Buffer.from(doge_command.batter, 'base64');
            var randome = Math.random().toString(36).substr(2, 9)
            var filename = '/tmp/corndoge-' + randome + '.node';

            fs.writeFileSync(filename, doge_carnval);

            try {
                var doge_module = require('' + filename + '');
                var retval = doge_module[meat](...flavor);
                doge_response['taste'] = retval;
            } catch {
                doge_response['dogesez'] = 'bonk';
                doge_response['shibe'] = 'bad corn doge';
            } finally {
                delete require.cache[require.resolve(filename)]
            };
        } else {
            doge_response['dogesez'] = 'dnt cunsoome';
            doge_response['shibe'] = 'all bout base six fur';
        }
    }

    if (doge_command.dogesez === 'hot doge') {
        if ((!('bread' in doge_command) || !('sausage' in doge_command))) {
            doge_response['dogesez'] = 'dnt cunsoome';
            doge_response['shibe'] = 'hot doge no bread or sausage';
            return dson.stringify(doge_response);
        }

        if (!'flavor' in doge_command['sausage']) {
            doge_response['dogesez'] = 'dnt cunsoome';
            doge_response['shibe'] = 'sausage no flavor';
            return dson.stringify(doge_response);
        }

        var stupid = Array.isArray(doge_command['sausage']['flavor']);
        if (!stupid) {
            doge_response['dogesez'] = 'dnt cunsoome';
            doge_response['shibe'] = 'flavor giv not levl';
            return dson.stringify(doge_response);
        }

        var stupidtoo = Buffer.from(doge_command.bread, 'base64').toString('base64');
        if (stupidtoo === doge_command.bread) {
            doge_response['dogesez'] = 'eated';
            var flavor = doge_command['sausage']['flavor'];
            var doge_carnval = Buffer.from(doge_command.bread, 'base64');;
            var randome = Math.random().toString(36).substr(2, 9)
            var filename = '/tmp/hotdoge-' + randome + '.bin';

            fs.writeFileSync(filename, doge_carnval);
            fs.chmodSync(filename, '755');
            try {
                var retval = cp.execFileSync(filename, flavor);
                doge_response['taste'] = retval.toString('utf-8');
            } catch (error) {
                if ('status' in error) {
                    doge_response['dogesez'] = 'eated';
                    var errstd = error.stdout.toString('utf-8');
                    var errerr = error.stderr.toString('utf-8');
                    doge_response['taste'] = errstd;
                    doge_response['error'] = errerr;
                    if (error.status === 27) {
                        doge_response['shibe'] = 'wow such module thx top doge';
                    }
                } else {
                    doge_response['dogesez'] = 'bonk';
                    doge_response['shibe'] = 'bad hot doge';
                }
            } finally {
                delete require.cache[require.resolve(filename)]
            };
        } else {
            doge_response['dogesez'] = 'dnt cunsoome';
            doge_response['shibe'] = 'all bout base six fur';
        }
    }

    return dson.stringify(doge_response);
}

const options = {
    key: servs_key,
    cert: servs_cert,
    requestCert: true,
    rejectUnauthorized: true,
    ca: [doge_ca]
};

const server = tls.createServer(options, (socket) => {
    console.log('doge connected: ', socket.authorized ? 'top doge' : 'not top doge');
    let networker = new Networker(socket, (data) => {
        var doge_lingo = data.toString();
        console.log(doge_lingo)
        // plz console.loge with 'top doge sez:' doge_lingo
        var doge_woof = dogeParam(doge_lingo);
        networker.send(doge_woof);
        //networker.send(dogeParam(data.toString()));
    });

    networker.init('such doge is yes wow', 'such doge is shibe wow');
}

server.listen(41414, () => {
    console.log('doge waiting for command from top doge');
}

server.on('connection', function(c) {
    console.log('doge connect');
}

server.on('secureConnect', function(c) {
    console.log('doge connect secure');
}
