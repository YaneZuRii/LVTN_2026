<?php
// Tep sach_get.php
header("Access-Control-Allow-Origin: *");

// Cau hinh ket noi CSDL thuvien_db
$host = 'localhost';
$dbname = 'thuvien_db';
$username = 'root'; 
$password = '';     

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("{STATUS: NO}");
}

$action = isset($_GET['action']) ? $_GET['action'] : '';

switch ($action) {
    case 'login':
        $mathe = isset($_GET['mathe']) ? $_GET['mathe'] : '';
        $mapin = isset($_GET['mapin']) ? $_GET['mapin'] : '';
        
        $stmt = $pdo->prepare("SELECT * FROM dangnhap WHERE mathe = ? AND mapin = ?");
        $stmt->execute([$mathe, $mapin]);
        
        if ($stmt->rowCount() > 0) {
            echo "{STATUS: YES}";
        } else {
            echo "{STATUS: NO}";
        }
        break;

    case 'getall':
        $stmt = $pdo->query("SELECT * FROM sach");
        $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode($data);
        break;

    case 'add':
        $tensach = isset($_GET['tensach']) ? $_GET['tensach'] : '';
        $tacgia = isset($_GET['tacgia']) ? $_GET['tacgia'] : '';
        $giatien = isset($_GET['giatien']) ? $_GET['giatien'] : 0;
        // Ep kieu ve so nguyen de luu vao BOOLEAN (1 hoac 0)
        $conhang = isset($_GET['conhang']) ? (int)$_GET['conhang'] : 1; 

        $stmt = $pdo->prepare("INSERT INTO sach (tensach, tacgia, giatien, conhang) VALUES (?, ?, ?, ?)");
        if ($stmt->execute([$tensach, $tacgia, $giatien, $conhang])) {
            echo "{STATUS: YES}";
        } else {
            echo "{STATUS: NO}";
        }
        break;

    case 'update':
        $id = isset($_GET['id']) ? $_GET['id'] : '';
        $tensach = isset($_GET['tensach']) ? $_GET['tensach'] : '';
        $tacgia = isset($_GET['tacgia']) ? $_GET['tacgia'] : '';
        $giatien = isset($_GET['giatien']) ? $_GET['giatien'] : 0;
        $conhang = isset($_GET['conhang']) ? (int)$_GET['conhang'] : 1;

        $stmt = $pdo->prepare("UPDATE sach SET tensach=?, tacgia=?, giatien=?, conhang=? WHERE id=?");
        if ($stmt->execute([$tensach, $tacgia, $giatien, $conhang, $id])) {
            echo "{STATUS: YES}";
        } else {
            echo "{STATUS: NO}";
        }
        break;

    case 'delete':
        $id = isset($_GET['id']) ? $_GET['id'] : '';
        $stmt = $pdo->prepare("DELETE FROM sach WHERE id=?");
        if ($stmt->execute([$id])) {
            echo "{STATUS: YES}";
        } else {
            echo "{STATUS: NO}";
        }
        break;

    default:
        echo "{STATUS: NO}";
        break;
}
?>