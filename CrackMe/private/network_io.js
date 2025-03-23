
/**
 * Since all network write IO is single threaded and linear, a single write buffer can be reused across all operations
 * @type {DataView}
 */
let writeBuffer = new DataView(new ArrayBuffer(100000));

/**
 * The offset at which to write in the writeBuffer. Resets by sending with the client's send()
 * @type {number}
 */
let writeOffset = 0;
let strState = 0x17;

/**
 * The main network writer utility. All data is written in big endian format
 * @exports
 */
let netWriter = {

    /**
     * Writes a value as a uint8
     * @param {number} value
     */
    writeUInt8: function (value) {
        writeBuffer.setUint8(writeOffset, value);
        writeOffset++;
    },

    /**
     * Write a boolean as a byte
     * @param {boolean} value
     */
    writeBool: function (value) {
        this.writeUInt8(value ? 1 : 0);
    },

    /**
     * Write a uint16 value
     * @param {number} value
     */
    writeUInt16: function (value) {
        writeBuffer.setUint16(writeOffset, value);
        writeOffset += 2;
    },

    writeInt16: function (value) {
        writeBuffer.setInt16(writeOffset, value);
        writeOffset += 2;
    },

    /**
     * Write a int32 value
     * @param {number} value
     */
    writeInt32: function (value) {
        writeBuffer.setInt32(writeOffset, value);
        writeOffset += 4;
    },

    writeInt64: function (value) {
        writeBuffer.setBigInt64(writeOffset, value);
        writeOffset += 4;
    },

    /**
     * Write a float32 value
     * @param {number} value
     */
    writeFloat32: function (value) {
        writeBuffer.setFloat32(writeOffset, value);
        writeOffset += 4;
    },

    /**
     * Write a uint16 value
     * @param {number} value
     */
    writeUInt32: function (value) {
        writeBuffer.setUint32(writeOffset, value);
        writeOffset += 4;
    },

    /**
     * Write a float64 value
     * @param {number} value
     */
    writeFloat64: function (value) {
        writeBuffer.setFloat64(writeOffset, value);
        writeOffset += 8;
    },

    alignStream: function (alignment) {
        while (writeOffset % alignment !== 0)
            this.writeUInt8(Math.floor(Math.random() * 255));
    },

    /**
     * Write a string (Internally a list of Uint16 encoded characters)
     * @param {string} value
     */
    writeString: function (value) {
        this.writeUInt16(value.length ^ 15821);
        let lastChar = 0;
        for (let i = 0; i < value.length; i++) {
            let newChar = value.charCodeAt(i);
            this.writeInt16((newChar - lastChar) ^ strState);
            strState ^= 0x19;
            lastChar = newChar;
        }
    },

    /**
     * Return sliced buffer and reset offset
     * @returns {ArrayBuffer} buffer sliced
     */
    writeOut: function () {
        let buffer = writeBuffer.buffer.slice(0, writeOffset);
        writeOffset = 0;
        strState = 0;
        return buffer;
    },

    getWriteOffset: function () {
        return writeOffset;
    },

    setWriteOffset: function(offset) {
        writeOffset = offset;
    }
};

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

NetReader.prototype.reachedEnd = function () {
    return this.offset >= this.data.byteLength;
}

/**
 * Reads a uint8
 * @returns {number}
 */
NetReader.prototype.readUInt8 = function () {
    if (this.len - this.offset < 1) return;
    let value = this.data.getUint8(this.offset);
    this.offset++;
    return value;
};

/**
 * Reads a uint16
 * @returns {number}
 */
NetReader.prototype.readUInt16 = function () {
    if (this.len - this.offset < 2) return;
    let value = this.data.getUint16(this.offset, false);
    this.offset += 2;
    return value;
};

/**
 * Reads a float32
 * @returns {number}
 */
NetReader.prototype.readFloat32 = function () {
    if (this.len - this.offset < 4) return;
    let value = this.data.getFloat32(this.offset, false);
    this.offset += 4;
    return value;
};

/**
 * Reads a int16
 * @returns {number}
 */
NetReader.prototype.readInt16 = function () {
    if (this.len - this.offset < 2) return;
    let value = this.data.getInt16(this.offset, false);
    this.offset += 2;
    return value;
};

/**
 * Reads a uint32
 * @returns {number}
 */
NetReader.prototype.readUInt32 = function () {
    if (this.len - this.offset < 4) return;
    let value = this.data.getUint32(this.offset, false);
    this.offset += 4;
    return value;
};

NetReader.prototype.readInt32 = function () {
    if (this.len - this.offset < 4) return;
    let value = this.data.getInt32(this.offset, false);
    this.offset += 4;
    return value;
};

/**
 * Reads a float64
 * @returns {number}
 */
NetReader.prototype.readFloat64 = function () {
    if (this.len - this.offset < 8) return;
    let value = this.data.getFloat64(this.offset, false);
    this.offset += 8;
    return value;
};

/**
 * Reads a bool
 * @returns {boolean}
 */
NetReader.prototype.readBool = function () {
    return this.readUInt8() === 0 ? false : true;
};

/**
 * Reads a string (Internally a list of Uint16 characters)
 * @returns {string}
 */
NetReader.prototype.readString = function () {
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

/**
 * Reads a string with a U32 length
 * @returns {string}
 */
NetReader.prototype.readDataString = function () {
    let final = '';
    let size = this.readUInt32();
    for (let i = 0; i < size; i++) {
        final += String.fromCharCode(this.readUInt16() ^ 0x42);
    }
    return final;
};

/**
 * Reads a base64 encoded string (Internally a list of Uint8 characters)
 * @returns {string} Decoded string
 */
NetReader.prototype.readBase64String = function () {
    let final = '';
    let amount = this.readUInt16();
    for (let i = 0; i < amount; i++) {
        final += String.fromCharCode(this.readUInt8() ^ 0x42);
    }

    return window.atob(final);
};

NetReader.prototype.alignStream = function (alignment) {
    while (this.offset % alignment !== 0)
        this.readUInt8();
};

module.exports = {
    netWriter,
    NetReader
}