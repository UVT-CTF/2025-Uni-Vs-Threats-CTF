# PipeLeak Writeup

## Step 1: XSS

The /posts/:id endpoint is vulnerable through the "location" field (which is not directly editable through the site UI).
By reporting a certain post, the admin bot will execute the XSS code.

## Step 2: Bruteforcing chrome CDP port

See solution.js and payload.html

- Some endpoint is required to delay page loading (e.g. https://httpbin.org/delay/5)
- Some endpoint is required for data exfiltration (e.g. https://webhook.site/)

## Step 3: Polluting the log file

- First, send a request to localhost:8080/<title> and then to localhost:8080/</title>
- Note that the Cookie value has to be passed to go to the right log.htm
- This will ensure that the flag is leaked through the log.htm page.

## Step 4: Interact with CDP

- Open log.htm in a new tab with the json/new endpoint
- Fetch the tab list, which contains the titles of all tabs and exfiltrate it.
- You will need to use the admin/doHttpReq SSRF endpoint to bypass CDP CORS.

## Bypassing doHttpReq endpoint restrictions

- To successfully call doHttpReq you need a null Origin, which can be achieved through a Location header redirect
- e.g. use https://httpbin.org/redirect-to

## Responses:

```json
{
   "description": "",
   "devtoolsFrontendUrl": "https://chrome-devtools-frontend.appspot.com/serve_rev/@9ba7e609d28c509a8ce9265c2247065d8d251173/inspector.html?ws=127.0.0.1:38781/devtools/page/F54BD62C85568D141017C763423584CD",
   "id": "F54BD62C85568D141017C763423584CD",
   "title": "",
   "type": "page",
   "url": "file:///app/log.htm",
   "webSocketDebuggerUrl": "ws://127.0.0.1:38781/devtools/page/F54BD62C85568D141017C763423584CD"
}
```

```json
[ {
   "description": "",
   "devtoolsFrontendUrl": "https://chrome-devtools-frontend.appspot.com/serve_rev/@9ba7e609d28c509a8ce9265c2247065d8d251173/inspector.html?ws=127.0.0.1:38781/devtools/page/F54BD62C85568D141017C763423584CD",
   "id": "F54BD62C85568D141017C763423584CD",
   "title": "&lt;br&gt;Flag: &quot;UVT{n0w_y0ur3_th1nk1ng_w1th_p0rt4ls}&quot;&lt;br&gt;GET /",
   "type": "page",
   "url": "file:///app/log.htm",
   "webSocketDebuggerUrl": "ws://127.0.0.1:38781/devtools/page/F54BD62C85568D141017C763423584CD"
}, {
   "description": "",
   "devtoolsFrontendUrl": "https://chrome-devtools-frontend.appspot.com/serve_rev/@9ba7e609d28c509a8ce9265c2247065d8d251173/inspector.html?ws=127.0.0.1:38781/devtools/page/5640129E7D63D9E5A1B43D6425B7BA81",
   "id": "5640129E7D63D9E5A1B43D6425B7BA81",
   "title": "My Blog",
   "type": "page",
   "url": "http://localhost:8080/posts/1",
   "webSocketDebuggerUrl": "ws://127.0.0.1:38781/devtools/page/5640129E7D63D9E5A1B43D6425B7BA81"
}, {
   "description": "",
   "devtoolsFrontendUrl": "https://chrome-devtools-frontend.appspot.com/serve_rev/@9ba7e609d28c509a8ce9265c2247065d8d251173/inspector.html?ws=127.0.0.1:38781/devtools/page/913F425DE3310684855CC5C1306E7203",
   "id": "913F425DE3310684855CC5C1306E7203",
   "title": "about:blank",
   "type": "page",
   "url": "about:blank",
   "webSocketDebuggerUrl": "ws://127.0.0.1:38781/devtools/page/913F425DE3310684855CC5C1306E7203"
} ]
```
