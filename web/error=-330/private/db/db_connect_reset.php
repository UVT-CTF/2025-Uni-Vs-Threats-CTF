<?php
$servername = "db"; // The service name for MySQL container in docker-compose
$username = "root";  // MySQL username
$password = "rootpass";  // MySQL password
$dbname = "password_reset"; // MySQL database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
