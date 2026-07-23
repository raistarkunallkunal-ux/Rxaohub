const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 3000;

const FIREBASE_DB_URL = "https://myscript-6a096-default-rtdb.asia-southeast1.firebasedatabase.app/";

// Change this to any secret password you want
const SECRET_KEY = "MySecretAuthKey123";

const FAKE_404_HTML = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Page Not Found</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { min-height: 100vh; display: flex; justify-content: center; align-items: center; background: #0d0e15; font-family: -apple-system, sans-serif; color: #fff; padding: 20px; }
        .container { text-align: center; width: 100%; max-width: 480px; padding: 30px 20px; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; backdrop-filter: blur(12px); }
        h1 { font-size: clamp(4rem, 15vw, 7rem); font-weight: 900; background: linear-gradient(45deg, #ff4b2b, #ff416c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; }
        p { font-size: clamp(0.95rem, 3.5vw, 1.15rem); color: #a0a5b5; margin-bottom: 24px; }
        .btn { display: inline-block; width: 100%; max-width: 220px; text-decoration: none; color: #fff; background: #ff416c; padding: 12px 24px; border-radius: 8px; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <h1>404</h1>
        <p>The page or resource you are looking for does not exist.</p>
        <a href="/" class="btn">Return Home</a>
    </div>
</body>
</html>
`;

app.get('/get-script', async (req, res) => {
    // Check if the secret header matches
    const clientKey = req.headers['x-auth-key'];

    // If a browser opens it OR the key is wrong -> Show 404
    if (clientKey !== SECRET_KEY) {
        res.setHeader('Content-Type', 'text/html');
        return res.status(404).send(FAKE_404_HTML);
    }

    try {
        const response = await axios.get(`${FIREBASE_DB_URL}scripts.json`);
        const scriptsData = response.data;

        if (!scriptsData) {
            return res.status(404).send("-- Error: No keys available.");
        }

        const keys = Object.keys(scriptsData);
        const randomKey = keys[Math.floor(Math.random() * keys.length)];
        const scriptPayload = scriptsData[randomKey];

        await axios.delete(`${FIREBASE_DB_URL}scripts/${randomKey}.json`);

        res.setHeader('Content-Type', 'text/plain');
        return res.status(200).send(scriptPayload);
    } catch (error) {
        return res.status(500).send("-- Internal Server Error");
    }
});

// Any other URL shows 404
app.use((req, res) => {
    res.setHeader('Content-Type', 'text/html');
    res.status(404).send(FAKE_404_HTML);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
