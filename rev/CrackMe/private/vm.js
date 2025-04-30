/**
     * The main utility for reading network data. This doesn't use a global buffer and instead needs to be initialized with an ArrayBuffer.
     * @exports
     * @param {ArrayBuffer} buffer Readable arraybuffer
     * @property {DataView} data Main readable view of the buffer data
     * @property {number} len Byte length of data
     * @property {number} offset Local reading offset of data
     */
function NetReader(buffer) {
    this.data = new DataView(buffer);
    this.len = this.data.byteLength;
    this.offset = 0;
    this.strState = 0x17;
}

NetReader.prototype.reachedEnd = function() {
    return this.offset >= this.data.byteLength;
}

/**
 * Reads a uint8
 * @returns {number}
 */
NetReader.prototype.readUInt8 = function() {
    if (this.len - this.offset < 1) return;
    let value = this.data.getUint8(this.offset);
    this.offset++;
    return value;
};

/**
 * Reads a uint16
 * @returns {number}
 */
NetReader.prototype.readUInt16 = function() {
    if (this.len - this.offset < 2) return;
    let value = this.data.getUint16(this.offset, false);
    this.offset += 2;
    return value;
};

/**
 * Reads a float32
 * @returns {number}
 */
NetReader.prototype.readFloat32 = function() {
    if (this.len - this.offset < 4) return;
    let value = this.data.getFloat32(this.offset, false);
    this.offset += 4;
    return value;
};

/**
 * Reads a int16
 * @returns {number}
 */
NetReader.prototype.readInt16 = function() {
    if (this.len - this.offset < 2) return;
    let value = this.data.getInt16(this.offset, false);
    this.offset += 2;
    return value;
};

/**
 * Reads a uint32
 * @returns {number}
 */
NetReader.prototype.readUInt32 = function() {
    if (this.len - this.offset < 4) return;
    let value = this.data.getUint32(this.offset, false);
    this.offset += 4;
    return value;
};

NetReader.prototype.readInt32 = function() {
    if (this.len - this.offset < 4) return;
    let value = this.data.getInt32(this.offset, false);
    this.offset += 4;
    return value;
};

/**
 * Reads a string (Internally a list of Uint16 characters)
 * @returns {string}
 */
NetReader.prototype.readString = function() {
    let final = '';
    let amount = this.readUInt16() ^ 15821;
    let lastChar = 0;
    for (let i = 0; i < amount; i++) {
        let relChar = this.readInt16() ^ this.strState;
        final += String.fromCharCode(relChar + lastChar);
        this.strState ^= 0x19;
        lastChar = relChar + lastChar;
    }
    return final;
};

NetReader.prototype.alignStream = function(alignment) {
    while (this.offset % alignment !== 0)
        this.readUInt8();
};

function executeVMCode(codeBuffer, args = []) {
    let variableMap = {};
    let extId = 0;

    for (let arg of args)
        variableMap[++extId] = arg;

    let reader = new NetReader(codeBuffer);

    function readNumber() {
        let type = reader.readUInt8();
        switch (type) {
            case 1:
                return reader.readInt32();
            case 2:
                return reader.readFloat32();
        }
    }

    while (!reader.reachedEnd()) {
        let instrId = reader.readUInt8() ^ 174;

        let varId;

        switch (instrId) {
            case 1: // LOADNUM
                varId = reader.readUInt16();
                variableMap[varId] = readNumber();
                break;
            case 2: // ADDNUM
                varId = reader.readUInt16();
                variableMap[varId] += readNumber();
                break;
            case 3: // XORSHIFT
                varId = reader.readUInt16();
                variableMap[varId] ^= variableMap[varId] >>> readNumber();
                break;
            case 4: // IMUL
                varId = reader.readUInt16();
                variableMap[varId] = Math.imul(variableMap[varId], readNumber());
                break;
            case 5: // ABS
                varId = reader.readUInt16();
                if (variableMap[varId] < 0)
                    variableMap[varId] = -variableMap[varId];
                break;
            case 6: // LOADATTRIB
                varId = reader.readUInt16();
                let attributeOwner = variableMap[reader.readUInt16()];
                variableMap[varId] = undefined;

                let chainCount = reader.readUInt8();
                for (let i = 0; i < chainCount; i++) {
                    let attr = reader.readString();
                    variableMap[varId] = (variableMap[varId] || attributeOwner)[attr];
                }
                break;
            case 7: // CMPGREATER
                varId = reader.readUInt16();
                variableMap[varId] = variableMap[reader.readUInt16()] > variableMap[reader.readUInt16()];
                break;
            case 8: // CMPEQ
                varId = reader.readUInt16();
                variableMap[varId] = variableMap[reader.readUInt16()] === variableMap[reader.readUInt16()];
                break;
            case 9: // CMPGREATEREQ
                varId = reader.readUInt16();
                variableMap[varId] = variableMap[reader.readUInt16()] >= variableMap[reader.readUInt16()];
                break;
            case 10: // JUMPIFNOT
                varId = reader.readUInt16();
                if (!variableMap[varId])
                    reader.offset = reader.readUInt32();
                break;
            case 11: // JUMPIF
                varId = reader.readUInt16();
                if (variableMap[varId])
                    reader.offset = reader.readUInt32();
                break;
            case 12: // CP
                varId = reader.readUInt16();
                variableMap[varId] = variableMap[reader.readUInt16()];
                break;
            case 13: // MOD
                varId = reader.readUInt16();
                variableMap[varId] %= variableMap[reader.readUInt16()];
                break;
            case 14: // SWAP ARR
                let array = variableMap[reader.readUInt16()];
                let idx1 = variableMap[reader.readUInt16()];
                let idx2 = variableMap[reader.readUInt16()];

                let temp = array[idx1];
                array[idx1] = array[idx2];
                array[idx2] = temp;
                break;
            case 15: // ret
                return variableMap[reader.readUInt16()];
            case 16: // dbg
                let varCount = reader.readUInt8();
                let str = '';
                for (let i = 0; i < varCount; i++)
                    str += variableMap[reader.readUInt16()] + ' ';
                console.log(str);
                break;
            case 18: // add
                varId = reader.readUInt16();
                variableMap[varId] += variableMap[reader.readUInt16()];
                break;
            case 20: // CREATEARRAY
                varId = reader.readUInt16();
                variableMap[varId] = [];
                break;
            case 21: // PUSH
                varId = reader.readUInt16();
                variableMap[varId].push(variableMap[reader.readUInt16()]);
                break;
            case 22: // LOADFROMARRAY
                varId = reader.readUInt16();
                variableMap[varId] = variableMap[reader.readUInt16()][variableMap[reader.readUInt16()]];
                break;
            case 23: // not
                varId = reader.readUInt16();
                variableMap[varId] = !variableMap[varId];
                break;
            case 24: // load str
                varId = reader.readUInt16();
                variableMap[varId] = reader.readString();
                break;
            case 25: // call
                varId = reader.readUInt16();

                let argCnt = reader.readUInt8();
                let args = [];
                for (let i = 0; i < argCnt; i++)
                    args.push(variableMap[reader.readUInt16()]);
                variableMap[varId].apply(null, args);
                break;
            case 26: // call with ret
                varId = reader.readUInt16();
                let ret = reader.readUInt16();
                let argCnt2 = reader.readUInt8();
                let args2 = [];
                for (let i = 0; i < argCnt2; i++)
                    args2.push(variableMap[reader.readUInt16()]);
                variableMap[ret] = variableMap[varId].apply(null, args2);
                break;
            case 27: // call with attrib
                varId = reader.readUInt16();
                let attrib = reader.readString();
                let owner = variableMap[varId];
                let ret2 = reader.readUInt16();
                let argCnt3 = reader.readUInt8();
                let args3 = [];
                for (let i = 0; i < argCnt3; i++)
                    args3.push(variableMap[reader.readUInt16()]);
                variableMap[ret2] = owner[attrib].apply(owner, args3);
                break;
            case 28: // set attrib
                varId = reader.readUInt16();
                variableMap[varId][reader.readString()] = variableMap[reader.readUInt16()];
                break;
            case 29: // and
                varId = reader.readUInt16();
                variableMap[varId] &= readNumber();
                break;
            case 30: // xor
                varId = reader.readUInt16();
                variableMap[varId] ^= variableMap[reader.readUInt16()];
                break;
            case 31: // LSR with variable
                varId = reader.readUInt16();
                variableMap[varId] >>>= variableMap[reader.readUInt16()];
                break;
            case 32: // STORETOARRAY
                varId = reader.readUInt16();
                variableMap[varId][variableMap[reader.readUInt16()]] = variableMap[reader.readUInt16()];
                break;
            default:
                throw new Error('invalid: ' + instrId + ' ' + reader.offset);
        }

        reader.alignStream(8);
    }
}

/*%ENDTEMPLATE%*/

module.exports = {
    executeVMCode
};
