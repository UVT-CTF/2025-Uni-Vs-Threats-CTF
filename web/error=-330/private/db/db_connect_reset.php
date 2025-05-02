<?php
// ./private/db/db_connect_reset.php
$servername = "db";
$username   = "search_user";
$password   = "passwordidk";
$dbname     = "password_reset";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
