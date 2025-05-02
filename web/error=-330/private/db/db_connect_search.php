<?php
// connect.php
$servername = "db";
$username   = "search_user";
$password   = "passwordidk";
$dbname     = "sqli_challenge";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
