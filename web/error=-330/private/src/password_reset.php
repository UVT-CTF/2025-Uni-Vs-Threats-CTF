<?php
session_start();
require_once __DIR__ . '/private/db/db_connect_reset.php';

// Hide PHP errors
error_reporting(0);
ini_set('display_errors', 0);

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';

    // VULNERABLE: Still inserting user input directly into SQL
    $query = "SELECT username FROM users WHERE email = '$email' AND LENGTH(email) < 70 LIMIT 1";

    $result = $conn->query($query);

    if ($result) {
        if ($result->num_rows > 0) {
            // Email exists (maybe!)
            $message = "If the email exists, a reset link has been sent.";
        } else {
            // Email does not exist
            $message = "If the email exists, a reset link has been sent.";
        }
    } else {
        // Even if SQL fails, show same message
        $message = "If the email exists, a reset link has been sent.";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Password Reset</title>
    <link rel="stylesheet" href="style.css">
    <script>
        // Disable inspection tools
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        });
        document.onkeydown = function(e) {
            if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I') || (e.ctrlKey && e.key === 'u')) {
                e.preventDefault();
                alert('Inspection disabled.');
                return false;
            }
        };
    </script>
</head>
<body>
    <div class="container">
        <h1>Password Reset</h1>

        <?php if ($message): ?>
            <p class="info"><?= htmlspecialchars($message) ?></p>
        <?php endif; ?>

        <form method="POST">
            <label for="email">Email:</label>
            <input type="text" id="text" name="email" required>

            <button type="submit">Reset Password</button>
        </form>
    </div>
</body>
</html>
