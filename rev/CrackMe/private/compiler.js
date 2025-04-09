const fs = require('fs');
const { netWriter } = require('./network_io');

const CUR_VERSION = 180;

const file = fs.readFileSync(process.argv[2]).toString();

let lines = file.split('\n');

let variableMap = {};
let incrementingVarId = 0;
let labels = {};

let labelWrites = [];

function writeNumber(numStr) {
    if (numStr.includes('.')) {
        let val = parseFloat(numStr);
        netWriter.writeUInt8(2);
        netWriter.writeFloat32(val);
        return;
    } else if (numStr.includes('0x')) {
        let val = parseInt(numStr, 16);
        netWriter.writeUInt8(1);
        netWriter.writeInt32(val);
        return;
    }

    let val = parseInt(numStr);
    netWriter.writeUInt8(1);
    netWriter.writeInt32(val);
}

function getOrAssignVariableId(name) {
    if (variableMap[name])
        return variableMap[name];

    variableMap[name] = 100 + ((++incrementingVarId) ^ 1587);
    return variableMap[name];
}

const CMD_MAP = {
    'LOADNUM': 1,
    'ADDNUM': 2,
    'XORSHIFT': 3,
    'IMUL': 4,
    'ABS': 5,
    'EXTERNALS': -1,
    'LOADATTRIB': 6,
    'LABEL': -1,
    'CMPGREATER': 7,
    'CMPEQ': 8,
    'CMPGREATEREQ': 9,
    'JUMPIFNOT': 10,
    'JUMPIF': 11,
    'CP': 12,
    'MOD': 13,
    'SWAPARR': 14,
    'RET': 15,
    'DEBUG': 16,
    'LOADGLOBALATTRHASH': 17,
    'ADD': 18,
    'LOADGLOBALOBJECT': 19,
    'CREATEARRAY': 20,
    'PUSH': 21,
    'LOADFROMARRAY': 22,
    'NOT': 23,
    'LOADSTR': 24,
    'CALL': 25,
    'CALLWITHRET': 26,
    'CALLATTRIB': 27,
    'SETATTRIB': 28,
    'AND': 29,
    'XOR': 30,
    'LSRVAR': 31,
    'STORETOARRAY': 32
}

netWriter.writeUInt16(CUR_VERSION);
netWriter.alignStream(8);

for (let line of lines) {
    let cmd = line.trim();
    if (cmd === '')
        continue;
    if (cmd.startsWith('#'))
        continue;
    let tokens = cmd.split(' ');
    let cmdType = tokens[0];

    let varId = null;

    if (!CMD_MAP[cmdType])
        throw new Error('missing cmd: ' + cmdType);

    if (CMD_MAP[cmdType] > 0)
        netWriter.writeUInt8(CMD_MAP[cmdType] ^ 174);

    switch (cmdType) {
        case 'LOADNUM':
        case 'ADDNUM':
        case 'XORSHIFT':
        case 'AND':
        case 'IMUL':
            varId = getOrAssignVariableId(tokens[1]);

            netWriter.writeUInt16(varId);
            writeNumber(tokens[2]);
            break;
        case 'ABS':
            varId = getOrAssignVariableId(tokens[1]);
            netWriter.writeUInt16(varId);
            break;
        case 'EXTERNALS':
            for (let i = 1; i < tokens.length; i++)
                variableMap[tokens[i]] = i;
            break;
        case 'LOADATTRIB':
            varId = getOrAssignVariableId(tokens[1]);

            netWriter.writeUInt16(varId);

            let attributeChain = tokens[2].split('.');

            let mainObject = getOrAssignVariableId(attributeChain[0]);
            netWriter.writeUInt16(mainObject);

            netWriter.writeUInt8(attributeChain.length - 1);
            for (let i = 1; i < attributeChain.length; i++)
                netWriter.writeString(attributeChain[i]);
            break;
        case 'LOADGLOBALATTRHASH':
            varId = getOrAssignVariableId(tokens[1]);

            netWriter.writeUInt16(varId);

            let attributeChain2 = tokens[2].split('.');

            netWriter.writeUInt8(attributeChain2.length);
            for (let i = 0; i < attributeChain2.length; i++)
                netWriter.writeString(attributeChain2[i]);
            break;
        case 'LABEL':
            labels[tokens[1]] = netWriter.getWriteOffset();
            break;
        case 'CMPGREATER':
        case 'CMPGREATEREQ':
        case 'CMPEQ':
            let resultVarId = getOrAssignVariableId(tokens[1]);
            netWriter.writeUInt16(resultVarId);
            let cmpVarId = getOrAssignVariableId(tokens[2]);
            netWriter.writeUInt16(cmpVarId);
            let cmpVarId2 = getOrAssignVariableId(tokens[3]);
            netWriter.writeUInt16(cmpVarId2);
            break;
        case 'JUMPIF':
        case 'JUMPIFNOT':
            varId = getOrAssignVariableId(tokens[1]);
            netWriter.writeUInt16(varId);

            //let label = labels[tokens[2]];
            labelWrites.push({
                name: tokens[2],
                offset: netWriter.getWriteOffset()
            });
            netWriter.writeUInt32(0); // rewrite later
            break;
        case 'CP':
        case 'ADD':
        case 'MOD':
        case 'XOR':
        case 'LSRVAR':
            varId = getOrAssignVariableId(tokens[1]);
            let secondVarId = getOrAssignVariableId(tokens[2]);

            netWriter.writeUInt16(varId);
            netWriter.writeUInt16(secondVarId);
            break;
        case 'LOADFROMARRAY':
        case 'SWAPARR':
            varId = getOrAssignVariableId(tokens[1]);
            let swapIdx1 = getOrAssignVariableId(tokens[2]);
            let swapIdx2 = getOrAssignVariableId(tokens[3]);

            netWriter.writeUInt16(varId);
            netWriter.writeUInt16(swapIdx1);
            netWriter.writeUInt16(swapIdx2);
            break;
        case 'RET':
            varId = tokens.length > 1 ? getOrAssignVariableId(tokens[1]) : 0;
            netWriter.writeUInt16(varId);
            break;
        case 'DEBUG':
            netWriter.writeUInt8(tokens.length - 1);
            for (let i = 1; i < tokens.length; i++)
                netWriter.writeUInt16(getOrAssignVariableId(tokens[i]));
            break;
        case 'CREATEARRAY':
        case 'LOADGLOBALOBJECT':
            varId = getOrAssignVariableId(tokens[1]);
            netWriter.writeUInt16(varId);
            break;
        case 'PUSH':
            varId = getOrAssignVariableId(tokens[1]);
            netWriter.writeUInt16(varId);

            let toPushId = getOrAssignVariableId(tokens[2]);
            netWriter.writeUInt16(toPushId);
            break;
        case 'NOT':
            varId = getOrAssignVariableId(tokens[1]);
            netWriter.writeUInt16(varId);
            break;
        case 'LOADSTR':
            varId = getOrAssignVariableId(tokens[1]);
            netWriter.writeUInt16(varId);

            let str = tokens.slice(2).join(" ");
            netWriter.writeString(str);
            break;
        case 'CALL':
            varId = getOrAssignVariableId(tokens[1]);
            netWriter.writeUInt16(varId);

            netWriter.writeUInt8(tokens.length - 2);
            for (let i = 2; i < tokens.length; i++)
                netWriter.writeUInt16(getOrAssignVariableId(tokens[i]));
            break;
        case 'CALLWITHRET':
            varId = getOrAssignVariableId(tokens[1]);
            netWriter.writeUInt16(varId);

            netWriter.writeUInt16(getOrAssignVariableId(tokens[2])); //ret

            netWriter.writeUInt8(tokens.length - 3);
            for (let i = 3; i < tokens.length; i++)
                netWriter.writeUInt16(getOrAssignVariableId(tokens[i]));
            break;
        case 'CALLATTRIB':
            let splitData = tokens[1].split('.');
            netWriter.writeUInt16(getOrAssignVariableId(splitData[0]));
            netWriter.writeString(splitData[1]);

            netWriter.writeUInt16(getOrAssignVariableId(tokens[2])); //ret

            netWriter.writeUInt8(tokens.length - 3);
            for (let i = 3; i < tokens.length; i++)
                netWriter.writeUInt16(getOrAssignVariableId(tokens[i]));
            break;
        case 'SETATTRIB':
            let splitData2 = tokens[1].split('.');
            netWriter.writeUInt16(getOrAssignVariableId(splitData2[0]));
            netWriter.writeString(splitData2[1]);

            netWriter.writeUInt16(getOrAssignVariableId(tokens[2]));
            break;
        case 'STORETOARRAY':
            varId = getOrAssignVariableId(tokens[1]);
            let idx = getOrAssignVariableId(tokens[2]);
            let val = getOrAssignVariableId(tokens[3]);

            netWriter.writeUInt16(varId);
            netWriter.writeUInt16(idx);
            netWriter.writeUInt16(val);
            break;
    }

    netWriter.alignStream(8);
}

let originalOffset = netWriter.getWriteOffset();
for (let label of labelWrites) {
    netWriter.setWriteOffset(label.offset);
    let labelOff = labels[label.name];
    if (typeof labelOff === 'undefined')
        throw new Error('missing label: ' + label.name);
    //console.log(labels, labelOff, label);
    netWriter.writeUInt32(labelOff);
}
netWriter.setWriteOffset(originalOffset);

let buffer = Buffer.from(netWriter.writeOut());
fs.writeFileSync(process.argv[3] + '.txt', buffer.toString('base64'));
