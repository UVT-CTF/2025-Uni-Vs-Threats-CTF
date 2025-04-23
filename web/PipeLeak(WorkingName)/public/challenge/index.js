import express from 'express';
import puppeteer from 'puppeteer';
import fs from 'fs';
import { randomBytes } from 'crypto';
import cookieParser from 'cookie-parser';

const app = express();
const PORT = process.env.PORT || 8080;

const FLAG = process.env.FLAG || 'UVT{a_flag_goes_here}';

// TODO: Boss wants logs to have that oomph
let LOG_DATA = '<h1>Server logs</h1><br>'

const defaultPosts = [
    {
        from: 'admin',
        content: '{´◕ ◡ ◕｀} Hello world!',
        location: 'Earth'
    }
]

let userData = {};

function createNewUser() {
    let id = randomBytes(16).toString('hex');

    userData[id] = JSON.parse(JSON.stringify(defaultPosts));
    return id;
}

app.set('view engine', 'ejs');
app.set('views', 'views');

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

app.use((req, res, next) => {
    let userId = req.cookies['user'];
    console.log(userId, req.url);
    if (userId && userData[userId])
        logger(userId, `${req.method} ${decodeURIComponent(req.url)}`);
    next();
});

app.get('/', (req, res) => {
    let userId = req.cookies['user'];

    if (!userId || !userData[userId]) {
        userId = createNewUser();
        res.cookie('user', userId, {
            maxAge: 24 * 60 * 60 * 1000
        });
    }

    res.render('index', { posts: userData[userId].toReversed() });
});

app.get('/post', (req, res) => {
    res.status(200).render('create', {});
});

app.get('/posts/:user/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const user = req.params.user;

    if (!userData[user] || isNaN(id) || id < 0 || id >= userData[user].length || !userData[user][id]) {
        res.status(404).render('404');
        return;
    }

    res.status(200).render('post', { post: userData[user][id] });
});

app.get('/share/:id', (req, res) => {
    let userId = req.cookies['user'];

    if (!userId || !userData[userId]) {
        res.status(400).send('(╯°□°)╯︵ ┻━┻ You are not authenticated');
        return;
    }

    const id = parseInt(req.params.id);

    if (isNaN(id) || id < 0 || id >= userData[userId].length || !userData[userId][id]) {
        res.status(404).render('404');
        return;
    }

    res.status(200).send('◕ ◡ ◕ Note has been shared, admin will take a look!');

    checkNoteWithAI(`http://localhost:${PORT}/posts/${userId}/${id}`);
});

app.post('/post', (req, res) => {
    let userId = req.cookies['user'];

    if (!userId || !userData[userId]) {
        res.status(400).send('(╯°□°)╯︵ ┻━┻ You are not authenticated');
        return;
    }

    const content = req.body.content;
    const location = req.body.location;
    userData[userId].push({
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

// TODO: remove next sprint
app.get('/admin/doHttpReq', (req, res) => {
    try {
        disableCors(res);
        if ((`${req.headers.origin}` != 'null'
            && `${req.headers.origin}` != 'undefined')
            || req.headers['sec-fetch-mode'] === 'no-cors'
            || req.headers['sec-fetch-site'] === 'same-site'
            || req.headers['sec-fetch-site'] === 'same-origin'
        )
            throw new Error('(ノಠ ∩ಠ)ノ彡( \\o°o)\\ Request is not secure- cannot call this endpoint from the browser');

        let url = req.query.url ?? '';
        let method = req.query.method ?? 'GET';

        if (method !== 'GET' && req.headers['sec-fetch-mode'] === 'navigate') {
            throw new Error('(゜-゜) What?')
        }

        if (!allowedMethods.includes(method))
            throw new Error('(」゜ロ゜)」Method not allowed');

        if (url.length > 128)
            throw new Error('(」゜ロ゜)」URL is too long');

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
    console.log(`Notes App is up and running on port ${PORT}!`);
});

// Gotta stay safe out here..
const allowedProtocols = ['http://', 'https://', 'about:blank'];

export const checkNoteWithAI = async (url) => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });

    const page = await browser.newPage();

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

function logger(userId, data) {
    // TODO: format nicely
    LOG_DATA += data + '<br>' + 'Flag: ' + FLAG + '<br>';

    try { fs.mkdirSync('./logs'); } catch (e) { };
    fs.writeFileSync(`./logs/log-${userId}.htm`, LOG_DATA);
}
