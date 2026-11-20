<?php
// Tep dienthoai_get.php
header("Access-Control-Allow-Origin: *");

// Cau hinh ket noi CSDL dienthoai_db
$host = 'localhost';
$dbname = 'dienthoai_db';
$username = 'root'; 
$password = '';     

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("{RESULT: FAILED}");
}

$action = isset($_GET['action']) ? $_GET['action'] : '';

switch ($action) {
    case 'login':
        $email = isset($_GET['email']) ? $_GET['email'] : '';
        $maxacthuc = isset($_GET['maxacthuc']) ? $_GET['maxacthuc'] : '';
        
        $stmt = $pdo->prepare("SELECT * FROM nguoidung WHERE email = ? AND maxacthuc = ?");
        $stmt->execute([$email, $maxacthuc]);
        
        if ($stmt->rowCount() > 0) {
            echo "{RESULT: SUCCESS}";
        } else {
            echo "{RESULT: FAILED}";
        }
        break;

    case 'getall':
        $stmt = $pdo->query("SELECT * FROM dienthoai");
        $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode($data);
        break;

    case 'add':
        $tendienthoai = isset($_GET['tendienthoai']) ? $_GET['tendienthoai'] : '';
        $hangsanxuat = isset($_GET['hangsanxuat']) ? $_GET['hangsanxuat'] : '';
        $ram = isset($_GET['ram']) ? (int)$_GET['ram'] : 0;
        $giaban = isset($_GET['giaban']) ? $_GET['giaban'] : 0;
        $manhinh_gap = isset($_GET['manhinh_gap']) ? (int)$_GET['manhinh_gap'] : 0; 

        $stmt = $pdo->prepare("INSERT INTO dienthoai (tendienthoai, hangsanxuat, ram, giaban, manhinh_gap) VALUES (?, ?, ?, ?, ?)");
        if ($stmt->execute([$tendienthoai, $hangsanxuat, $ram, $giaban, $manhinh_gap])) {
            echo "{RESULT: SUCCESS}";
        } else {
            echo "{RESULT: FAILED}";
        }
        break;

    case 'update':
        $id = isset($_GET['id']) ? $_GET['id'] : '';
        $tendienthoai = isset($_GET['tendienthoai']) ? $_GET['tendienthoai'] : '';
        $hangsanxuat = isset($_GET['hangsanxuat']) ? $_GET['hangsanxuat'] : '';
        $ram = isset($_GET['ram']) ? (int)$_GET['ram'] : 0;
        $giaban = isset($_GET['giaban']) ? $_GET['giaban'] : 0;
        $manhinh_gap = isset($_GET['manhinh_gap']) ? (int)$_GET['manhinh_gap'] : 0;

        $stmt = $pdo->prepare("UPDATE dienthoai SET tendienthoai=?, hangsanxuat=?, ram=?, giaban=?, manhinh_gap=? WHERE id=?");
        if ($stmt->execute([$tendienthoai, $hangsanxuat, $ram, $giaban, $manhinh_gap, $id])) {
            echo "{RESULT: SUCCESS}";
        } else {
            echo "{RESULT: FAILED}";
        }
        break;

    case 'delete':
        $id = isset($_GET['id']) ? $_GET['id'] : '';
        $stmt = $pdo->prepare("DELETE FROM dienthoai WHERE id=?");
        if ($stmt->execute([$id])) {
            echo "{RESULT: SUCCESS}";
        } else {
            echo "{RESULT: FAILED}";
        }
        break;

    default:
        echo "{RESULT: FAILED}";
        break;
}
?>