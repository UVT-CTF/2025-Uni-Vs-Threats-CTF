/*%VMCODE%*/

const BYTECODE = new Uint8Array([/*%BYTECODE%*/]).buffer;

function check(flagStr) {
    let bytes = flagStr.split('').map(char => char.charCodeAt(0));
    let result = executeVMCode(BYTECODE, [bytes]);
    return result === 1;
}

let result = document.getElementById('result');
let pwInput = document.getElementById('pw');
let submit = document.getElementById('submit');

submit.onclick = function() {
    if (pwInput.value && check(pwInput.value)) {
        result.innerText = 'Correct!';
    } else {
        result.innerText = 'Incorrect!';
    }
}