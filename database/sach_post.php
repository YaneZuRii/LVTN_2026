<?php
// Tep sach_post.php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");

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

// Kiem tra phuong thuc POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    die("{STATUS: NO}");
}

$action = isset($_POST['action']) ? $_POST['action'] : '';

switch ($action) {
    case 'login':
        $mathe = isset($_POST['mathe']) ? $_POST['mathe'] : '';
        $mapin = isset($_POST['mapin']) ? $_POST['mapin'] : '';
        
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
        $tensach = isset($_POST['tensach']) ? $_POST['tensach'] : '';
        $tacgia = isset($_POST['tacgia']) ? $_POST['tacgia'] : '';
        $giatien = isset($_POST['giatien']) ? $_POST['giatien'] : 0;
        $conhang = isset($_POST['conhang']) ? (int)$_POST['conhang'] : 1;

        $stmt = $pdo->prepare("INSERT INTO sach (tensach, tacgia, giatien, conhang) VALUES (?, ?, ?, ?)");
        if ($stmt->execute([$tensach, $tacgia, $giatien, $conhang])) {
            echo "{STATUS: YES}";
        } else {
            echo "{STATUS: NO}";
        }
        break;

    case 'update':
        $id = isset($_POST['id']) ? $_POST['id'] : '';
        $tensach = isset($_POST['tensach']) ? $_POST['tensach'] : '';
        $tacgia = isset($_POST['tacgia']) ? $_POST['tacgia'] : '';
        $giatien = isset($_POST['giatien']) ? $_POST['giatien'] : 0;
        $conhang = isset($_POST['conhang']) ? (int)$_POST['conhang'] : 1;

        $stmt = $pdo->prepare("UPDATE sach SET tensach=?, tacgia=?, giatien=?, conhang=? WHERE id=?");
        if ($stmt->execute([$tensach, $tacgia, $giatien, $conhang, $id])) {
            echo "{STATUS: YES}";
        } else {
            echo "{STATUS: NO}";
        }
        break;

    case 'delete':
        $id = isset($_POST['id']) ? $_POST['id'] : '';
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