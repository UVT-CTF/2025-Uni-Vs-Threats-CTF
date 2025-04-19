import express from 'express';
import path from 'path';
import puppeteer from 'puppeteer';
import fs from 'fs';

const app = express();
const PORT = process.env.PORT || 8080;

const FLAG = fs.readFileSync('../flag.txt');

// TODO: Boss wants logs to have that oomph
let LOG_DATA = '<h1>Server logs</h1><br>'

let posts = [
    {
        from: 'admin',
        content: 'Welcome to my blog!',
        location: 'Earth'
    }
]

app.set('view engine', 'ejs');
app.set('views', 'views');

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

app.use((req, res, next) => {
    logger(`${req.method} ${decodeURIComponent(req.url)}`);
    next();
});

app.get('/', (req, res) => {
    res.render('index', { title: 'Welcome', message: 'Hello, EJS + Express!', posts: posts.toReversed() });
});

app.get('/post', (req, res) => {
    res.status(200).render('create', { title: 'Post' });
});

app.get('/posts/:id', (req, res) => {
    const id = parseInt(req.params.id);

    if (isNaN(id) || id < 0 || id >= posts.length || !posts[id]) {
        console.log('Not found: ' + req.params.id);
        res.status(404).render('404');
        return;
    }

    console.log('Post found: ' + posts[id]);
    res.status(200).render('post', { title: 'Post', post: posts[id] });
});

app.get('/report/:id', (req, res) => {
    const id = parseInt(req.params.id);

    if (isNaN(id) || id < 0 || id >= posts.length || !posts[id]) {
        res.status(404).render('404');
        return;
    }

    res.status(200).send('Post has been reported, admin will take a look!');

    verifyReportWithAI('http://localhost:8080/posts/' + id);
});

app.post('/post', (req, res) => {
    const content = req.body.content;
    const location = req.body.location;
    posts.push({
        from: 'user',
        content: content,
        location: location || 'Earth'
    })
    res.redirect('/');
});

let allowedMethods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'];

function disableCors(res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET');
    res.setHeader('Access-Control-Allow-Headers', '');
}

app.get('/doHttpReq', (req, res) => {
    try {
        disableCors(res);
        if ((`${req.headers.origin}` != 'null'
            && `${req.headers.origin}` != 'undefined')
            || req.headers['sec-fetch-mode'] === 'no-cors'
            || req.headers['sec-fetch-site'] === 'same-site'
            || req.headers['sec-fetch-site'] === 'same-origin'
        )
            throw new Error('Request is not secure- cannot call this endpoint from the browser');

        let url = req.query.url ?? '';
        let method = req.query.method ?? 'GET';

        if (method !== 'GET' && req.headers['sec-fetch-mode'] === 'navigate') {
            throw new Error('What?')
        }

        if (!allowedMethods.includes(method))
            throw new Error('Method not allowed');

        if (url.length > 100)
            throw new Error('URL is too long');

        logger(method + ' ' + url + ' ' + FLAG);

        fetch(url, {
            method: method
        }).then(async (rsp) => {
            let data = await rsp.text()
            res.send(data)
        }).catch(e => {
            console.error(e);
            res.sendStatus(500);
        });
    } catch (e) {
        console.error(e);
        res.sendStatus(500);
    }
});

app.use((req, res) => {
    res.status(404).render('404', {});
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// Gotta stay safe out here..
const allowedProtocols = ['http://', 'https://', 'about:blank'];

export const verifyReportWithAI = async (url) => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });

    const page = await browser.newPage();

    page.on('console', msg => {
        console.log(`PAGE LOG: ${msg.text()}`);
    });

    await guardPage(page);

    browser.on('targetcreated', async (target) => {
        await guardPage(await target.page());
    });

    try {
        await page.goto(url, {
            waitUntil: "networkidle0",
        });

        console.log('Page load finished!');
    } catch (err) {
        console.error(err);
    } finally {
        await browser.close();
    }
};

async function guardPage(page) {
    let ok = false;
    let url = page.url();

    for (let allowedProtocol of allowedProtocols) {
        if (url.startsWith(allowedProtocol)) {
            ok = true;
            break;
        }
    }

    if (!ok) {
        await page.setJavaScriptEnabled(false);
        await page.setRequestInterception(true);

        page.on('request', (request) => {
            request.abort();
        });

        page.on('dialog', async (dialog) => {
            await dialog.dismiss();
        });

        page.on('framenavigated', async () => {
            await page.close();
        });
    }
}

function logger(data) {
    // TODO: format nicely
    LOG_DATA += data + '<br>' + 'Flag: ' + FLAG + '<br>';

    fs.writeFileSync('./log.htm', LOG_DATA);
}
