var ptr_WSAStartup = Module.getExportByName(null, "WSAStartup");
var isDumped = false;
var PROTECTION = 'wr-';
var TARGET_STRING = '"targets":[';

function stringToByteArray(str) {
    var byteArray = [];
    for (var i = 0; i < str.length; i++) {
        var charCode = str.charCodeAt(i);
        byteArray.push(charCode);
    }
    return byteArray;
}

function indexOfBuffer(buf, search) {
    let searchBytes = stringToByteArray(search);
    let searchLen = searchBytes.length;
    let max = buf.byteLength - searchLen;
    outer: for (let i = 0; i <= max; i++) {
        for (let j = 0; j < searchLen; j++) {
            if (buf[i + j] !== searchBytes[j])
                continue outer;
        }
        return i;
    }
    return -1;
}

Interceptor.attach(ptr_WSAStartup, {
    onEnter: function (args) {
        if (!isDumped) {
            isDumped = true;
            setTimeout(function() {
                let ranges = Process.enumerateRanges(PROTECTION);
                console.log('[BEGIN] Memory ranges located: ' + ranges.length);
                ranges.forEach(function (range) {
                    let buffer = null;
                    try {
                        buffer = new Uint8Array(range.base.readByteArray(range.size));
                        if (indexOfBuffer(buffer, TARGET_STRING) !== -1) {
                            let destFileName = `dumps/${range.base}_dump`;
                            let file = new File(destFileName, 'wb');
                            file.write(buffer);
                            file.flush();
                            file.close();
                            console.log('[DUMP] Memory dumped: ' + destFileName);
                        }
                    } catch (e) {
                        console.log('[ERROR] Failed to dump memory at: ' + range.base + ' Error: ' + e.message);
                    }
                });
                console.log('[END] Memory dump process completed');
                let ExitProcess = new NativeFunction(Module.getExportByName(null, 'ExitProcess'), 'void', ['uint']);
                ExitProcess(0);
            }, 15000); // Espera de 15 segundos
        }
    },

    onLeave: function (retval) {
        //TODO: Limpieza
    }
});
