const vm = require('./vm.js');
const fs = require('fs');
const { execSync } = require('child_process');

/* Base64 decoding stuff */
const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';

// Use a lookup table to find the index.
const lookup = typeof Uint8Array === 'undefined' ? [] : new Uint8Array(256);
for (let i = 0; i < chars.length; i++) {
    lookup[chars.charCodeAt(i)] = i;
}

const decode = (base64) => {
    let bufferLength = base64.length * 0.75,
        len = base64.length,
        i,
        p = 0,
        encoded1,
        encoded2,
        encoded3,
        encoded4;

    if (base64[base64.length - 1] === '=') {
        bufferLength--;
        if (base64[base64.length - 2] === '=') {
            bufferLength--;
        }
    }

    const arraybuffer = new ArrayBuffer(bufferLength),
        bytes = new Uint8Array(arraybuffer);

    for (i = 0; i < len; i += 4) {
        encoded1 = lookup[base64.charCodeAt(i)];
        encoded2 = lookup[base64.charCodeAt(i + 1)];
        encoded3 = lookup[base64.charCodeAt(i + 2)];
        encoded4 = lookup[base64.charCodeAt(i + 3)];

        bytes[p++] = (encoded1 << 2) | (encoded2 >> 4);
        bytes[p++] = ((encoded2 & 15) << 4) | (encoded3 >> 2);
        bytes[p++] = ((encoded3 & 3) << 6) | (encoded4 & 63);
    }

    return arraybuffer;
};

const byteCode = decode(fs.readFileSync('encrypt.txt').toString());

const FLAG = fs.readFileSync('flag.txt').toString().trim();

// external
let flagBytes = FLAG.split('').map(char => char.charCodeAt(0));

let result = vm.executeVMCode(byteCode, [flagBytes]);

console.log(result.map(char => String.fromCharCode(char)).join(''));
console.log(FLAG + ' -> ' + result);

const vmTemplateCode = fs.readFileSync('vm.js').toString().split('/*%ENDTEMPLATE%*/')[0];

let encryptTemplate = fs.readFileSync('encryptTemplate.asm').toString();

/* Create dynamic length flag check */
let flagCheck = '';
for (let i = 0; i < FLAG.length; i++) {
    flagCheck += `
LOADNUM check ${result[i]}
LOADNUM idx ${i}
LOADFROMARRAY value flag idx
CMPEQ result value check
JUMPIFNOT result failed`;
}

encryptTemplate = encryptTemplate.replace('%FLAGCHECK%', flagCheck);

try { fs.mkdirSync('temp'); } catch (e) { }
fs.writeFileSync('temp/encrypt.asm', encryptTemplate);

try {
    const output = execSync('node compiler temp/encrypt.asm temp/encrypt', { encoding: 'utf-8' }); // change command as needed
    console.log(output);
} catch (err) {
    console.error('Error:', err.message);
}

const encryptByteCode = Buffer.from(fs.readFileSync('temp/encrypt.txt').toString(), 'base64').toJSON().data;

let jsTemplate = fs.readFileSync('jsTemplate.js').toString();
jsTemplate = jsTemplate.replace('/*%VMCODE%*/', vmTemplateCode);
jsTemplate = jsTemplate.replace('/*%BYTECODE%*/', encryptByteCode.toString());

/* Obfuscate js code */
// TODO: cat de obfuscat ar trebui sa fie?
const JavaScriptObfuscator = require('javascript-obfuscator');
let obfuscationResult = JavaScriptObfuscator.obfuscate(jsTemplate, {
    compact: true,
    controlFlowFlattening: true,
    deadCodeInjection: true,
    controlFlowFlatteningThreshold: 1,
    numbersToExpressions: true,
    simplify: true,
    stringArrayShuffle: true,
    splitStrings: true,
    stringArrayThreshold: 1,
    debugProtection: false,
    selfDefending: false,
    stringArrayCallsTransform: true,
    stringArrayRotate: true,
    renameProperties: true,
    renameGlobals: true,
    renamePropertiesMode: 'unsafe'
});

fs.writeFileSync('output/main.js', obfuscationResult.getObfuscatedCode());

console.log('Challenge has been created !!');
