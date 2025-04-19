const express = require('express');
const app = express();

const PORT = process.env.PORT || 2999;

function disableCors(res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET');
    res.setHeader('Access-Control-Allow-Headers', '');
}

// /delay?t=5 will delay for 5 seconds
app.get('/delay', async (req, res) => {
    const t = parseFloat(req.query.t);

    if (isNaN(t) || t < 0) {
        return res.status(400).send('Invalid or missing ?t= query param (must be a non-negative number)');
    }

    console.log(`Delaying response for ${t} seconds...`);

    // Delay using setTimeout wrapped in a Promise
    await new Promise(resolve => setTimeout(resolve, t * 1000));

    res.send(`Responded after ${t} seconds`);
});

app.get('/send', async (req, res) => {
    console.log(req.query.data);
    res.status(200).send('');
});

// For bypassing origin checks
app.get('/redir', async(req, res) => {
    disableCors(res);
    res.redirect(decodeURIComponent(req.query.url));
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
