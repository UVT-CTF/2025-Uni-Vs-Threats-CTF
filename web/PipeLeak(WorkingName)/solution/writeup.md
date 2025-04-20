# PipeLeak Writeup

## Step 1: XSS

The /posts/:id endpoint is vulnerable through the "location" field (which is not directly editable through the site UI).
By reporting a certain post, the admin bot will execute the XSS code.

## Step 2: Bruteforcing chrome CDP port

See solution.js and attacker.js

- Some endpoint is required to delay page loading (e.g. https://httpbin.org/delay/5)
- Some endpoint is required for data exfiltration (e.g. https://webhook.site/)
- You will need to enable wildcard CORS if using webhook.site

## Step 3: Polluting the log file

- First, send a request to localhost:8080/<title> and then to localhost:8080/</title>
- This will ensure that the flag is leaked through the log.htm page.

## Step 4: Interact with CDP

- Open log.htm in a new tab with the json/new endpoint
- Fetch the tab list, which contains the titles of all tabs and exfiltrate it.
- You will need to use the admin/doHttpReq SSRF endpoint to bypass CDP CORS.

## Bypassing doHttpReq endpoint restrictions

- To successfully call doHttpReq you need a null Origin, which can be achieved through a Location header redirect
- e.g. use https://httpbin.org/redirect-to
