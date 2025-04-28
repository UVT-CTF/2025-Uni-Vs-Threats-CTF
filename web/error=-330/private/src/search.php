<?php
session_start();
require_once __DIR__ . '/private/db/db_connect_search.php';

$ip = $_SERVER['REMOTE_ADDR'];
$session_id = session_id();
$time = time();
$time10 = floor($time / 10);
$time60 = floor($time / 60);

// Use session + IP combined as identifier
$identifier = md5($session_id . $ip);

// Initialize rate limit tracking arrays
if (!isset($_SESSION['rate_limit_10s'][$identifier])) {
    $_SESSION['rate_limit_10s'][$identifier] = [];
}
if (!isset($_SESSION['rate_limit_60s'][$identifier])) {
    $_SESSION['rate_limit_60s'][$identifier] = [];
}

// Increment counters
$_SESSION['rate_limit_10s'][$identifier][$time10] = ($_SESSION['rate_limit_10s'][$identifier][$time10] ?? 0) + 1;
$_SESSION['rate_limit_60s'][$identifier][$time60] = ($_SESSION['rate_limit_60s'][$identifier][$time60] ?? 0) + 1;

// Set burst and minute limits
$burst_limit = 20;      
$minute_limit = 60;     

// Rate limit check
if ($_SESSION['rate_limit_10s'][$identifier][$time10] > $burst_limit || $_SESSION['rate_limit_60s'][$identifier][$time60] > $minute_limit) {
    header('HTTP/1.1 429 Too Many Requests');
    echo "Rate limit exceeded.";
    exit;
}

// Clean up old rate limit data
foreach ($_SESSION['rate_limit_10s'][$identifier] as $timestamp => $count) {
    if ($timestamp < floor(($time - 300) / 10)) {
        unset($_SESSION['rate_limit_10s'][$identifier][$timestamp]);
    }
}
foreach ($_SESSION['rate_limit_60s'][$identifier] as $timestamp => $count) {
    if ($timestamp < floor(($time - 300) / 60)) {
        unset($_SESSION['rate_limit_60s'][$identifier][$timestamp]);
    }
}

// User-Agent detection (block sqlmap)
$user_agent = $_SERVER['HTTP_USER_AGENT'] ?? '';
if (stripos($user_agent, 'sqlmap') !== false) {
    header('HTTP/1.1 403 Forbidden');
    echo "Access Denied.";
    exit;
}

// --- VULNERABLE SEARCH --- (keep for SQLi challenge)

$search = rawurldecode($_GET['search'] ?? '');
$results = [];
$error = '';

if (!empty($search)) {
    $query = "SELECT id, name, price, description FROM products WHERE name LIKE '$search'"; // <-- vulnerable on purpose

    try {
        $result = $conn->query($query);
        
        if ($result) {
            while ($row = $result->fetch_assoc()) {
                $results[] = $row;
            }

            $upperSearch = strtoupper($search);
            if (strpos($upperSearch, '@@VERSION') !== false || 
                strpos($upperSearch, 'VERSION()') !== false) {
                $results[] = [
                    'id' => 'DB Version',
                    'name' => $conn->server_info,
                    'price' => '',
                    'description' => 'Database version information'
                ];
            }
        }
    } catch (mysqli_sql_exception $e) {
        error_log("Search error: " . $e->getMessage());
        
        if (strpos($e->getMessage(), 'UNION') !== false) {
            $error = "UNION error";
        } else {
            $error = "Database error";
        }
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Product Search</title>
    <link rel="stylesheet" href="style.css">
    <script>
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        });
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
        <h1>Product Search</h1>
        
        <form method="GET">
            <input type="text" name="search" placeholder="Search products..." 
                   value="<?= htmlspecialchars($search) ?>">
            <button type="submit">Search</button>
        </form>

        <?php if ($error): ?>
            <div class="error">
                <?= htmlspecialchars($error) ?>
            </div>
        <?php endif; ?>

        <?php if (!empty($search)): ?>
            <h3>Results for "<?= htmlspecialchars($search) ?>"</h3>
            
            <?php if (!empty($results)): ?>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Description</th>
                    </tr>
                    <?php foreach ($results as $product): ?>
                        <tr>
                            <td><?= htmlspecialchars($product['id'] ?? 'NULL') ?></td>
                            <td><?= htmlspecialchars($product['name'] ?? 'NULL') ?></td>
                            <td><?= htmlspecialchars($product['price'] ?? 'NULL') ?></td>
                            <td><?= htmlspecialchars($product['description'] ?? 'NULL') ?></td>
                        </tr>
                    <?php endforeach; ?>
                </table>
            <?php else: ?>
                <p>No products found</p>
            <?php endif; ?>
        <?php endif; ?>
    </div>
</body>
</html>