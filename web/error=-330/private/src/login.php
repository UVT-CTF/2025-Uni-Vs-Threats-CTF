<?php
session_start();
require_once __DIR__ . '/private/db/db_connect_reset.php';

$ip = $_SERVER['REMOTE_ADDR'];
$time = time();
$time10 = floor($time / 10);  // Group timestamps in 10s
$time60 = floor($time / 60);  // Group timestamps in 60s

// Initialize counters
if (!isset($_SESSION['rate_limit_10s'][$ip])) {
    $_SESSION['rate_limit_10s'][$ip] = [];
}
if (!isset($_SESSION['rate_limit_60s'][$ip])) {
    $_SESSION['rate_limit_60s'][$ip] = [];
}

// Track hits
$_SESSION['rate_limit_10s'][$ip][$time10] = ($_SESSION['rate_limit_10s'][$ip][$time10] ?? 0) + 1;
$_SESSION['rate_limit_60s'][$ip][$time60] = ($_SESSION['rate_limit_60s'][$ip][$time60] ?? 0) + 1;

// Limits
$burst_limit = 10;      // Max 10 requests per 10 seconds
$minute_limit = 50;     // Max 50 requests per 60 seconds

// Check limits
if ($_SESSION['rate_limit_10s'][$ip][$time10] > $burst_limit || $_SESSION['rate_limit_60s'][$ip][$time60] > $minute_limit) {
    header('HTTP/1.1 429 Too Many Requests');
    echo "Rate limit exceeded.";
    exit;
}

// Detect sqlmap User-Agent
$user_agent = $_SERVER['HTTP_USER_AGENT'] ?? '';
if (stripos($user_agent, 'sqlmap') !== false) {
    header('HTTP/1.1 403 Forbidden');
    echo "Access Denied.";
    exit;
}


// Set error reporting to hide sensitive errors (only for production/CTF)
error_reporting(0);
ini_set('display_errors', 0);

$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    // Intentionally vulnerable query for CTF
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    
    try {
        $result = $conn->query($query);
        
        if ($result && $result->num_rows > 0) {
            $user = $result->fetch_assoc();
            $_SESSION['user'] = $user['username'];
            $_SESSION['is_admin'] = $user['is_admin'];
            header('Location: search.php');
            exit;
        } else {
            $error = 'Invalid credentials';
        }
    } catch (Exception $e) {
        // Log the actual error for your reference
        error_log("SQL Error: " . $e->getMessage());
        // Show generic message to user
        $error = 'SQL error - try to exploit this!';
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login Challenge</title>
    <link rel="stylesheet" href="style.css">
    <script>
        // Prevent right-click
        document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        });

        // Prevent F12, Ctrl+Shift+I, Ctrl+U
        document.onkeydown = function(e) {
        if (e.key === 'F12' || 
        (e.ctrlKey && e.shiftKey && e.key === 'I') || 
        (e.ctrlKey && e.key === 'u')) {
        e.preventDefault();
        alert('Inspection disabled for this challenge');
        return false;
        }
};
</script>
</head>
<body>
    <div class="container">
        <h1>Login</h1>        
        <?php if ($error): ?>
            <p class="error"><?= htmlspecialchars($error) ?></p>
        <?php endif; ?>
        
        <form method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            
            <button type="submit">Login</button>
            <a href="password_reset.php">Forgot password?</a>
        </div>

        </form>
    </div>
</body>
</html>