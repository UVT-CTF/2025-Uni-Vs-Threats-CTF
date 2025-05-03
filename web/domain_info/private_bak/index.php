<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>UVT-CTF - Whois Challenge</title>
    <style>
        body {
            background-color: #0d0d0d;
            font-family: monospace;
            color: #00ffea;
            padding: 20px;
        }
        input, button {
            padding: 10px;
            margin-top: 10px;
            width: 100%;
            background: #1a1a1a;
            color: #f8f8f8;
            border: 1px solid #333;
        }
        button {
            background-color: #00ffea;
            color: #000;
            font-weight: bold;
            cursor: pointer;
        }
        pre {
            background: #1a1a1a;
            padding: 20px;
            margin-top: 20px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>

<h1>🔍 Whois Execution</h1>

<form method="POST">
    <label>Target Host:</label>
    <input type="text" name="host" placeholder="127.0.0.1" required>

    <label>Target Port:</label>
    <input type="number" name="port" placeholder="43" required>

    <label>Query Object:</label>
    <input type="text" name="query" placeholder="example.com" required>

    <label>Save As Filename (Optional):</label>
    <input type="text" name="savefile" placeholder="file.txt">

    <button type="submit">Execute</button>
</form>

<?php
function cleanUploads($path, $minutes = 2) {
    foreach (glob($path . "/*") as $file) {
        if (is_file($file) && (time() - filemtime($file)) > ($minutes * 60)) {
            unlink($file);
        }
    }
}

function randomString($length = 6) {
    return substr(str_shuffle("abcdefghijklmnopqrstuvwxyz0123456789"), 0, $length);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $host = $_POST['host'];
    $port = $_POST['port'];
    $query = $_POST['query'];
    $savefile = $_POST['savefile'];

    // Basic anti-command injection filters
    foreach ([$host, $port, $query, $savefile] as $input) {
        if (preg_match('/[;&|`$()<>]/', $input)) {
            die("<p style='color:red;'>❌ Command Injection Detected!</p>");
        }
    }

    // Extra simple validation
    if (!filter_var($host, FILTER_VALIDATE_IP) && !filter_var($host, FILTER_VALIDATE_DOMAIN)) {
        die("<p style='color:red;'>❌ Invalid Hostname</p>");
    }

    // Safe escaping
    $host = escapeshellarg($host);
    $port = escapeshellarg($port);
    $query = escapeshellarg($query);

    // Create uploads folder if not exists
    $uploadDir = __DIR__ . '/uploads';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }

    // Cleanup old files
    cleanUploads($uploadDir, 2); // Delete files older than 2 minutes

    // Randomize file name
    if (empty($savefile)) {
        $savefile = "output.txt";
    }
    $randomPrefix = randomString();
    $finalName = $randomPrefix . "_" . basename($savefile);
    $savepath = $uploadDir . '/' . $finalName;

    // Execute
    $command = "whois -h " . $host . " -p " . $port . " " . $query  . " >  " . escapeshellarg($savepath);
    system($command);
    echo "Command: <pre>" . htmlspecialchars($command) . "</pre>";
    echo "<h2>✅ Whois Executed. Saved in:</h2>";
    echo "<pre>/uploads/" . htmlspecialchars($finalName) . "</pre>";
    echo "<p><a style='color:#00ffea;' href='/uploads/" . htmlspecialchars($finalName) . "' target='_blank'>Click here to view your file</a></p>";
}
?>

</body>
</html>
