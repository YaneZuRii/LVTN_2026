<?php
// Tep dienthoai_post.php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");

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

// Kiem tra phuong thuc POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    die("{RESULT: FAILED}");
}

$action = isset($_POST['action']) ? $_POST['action'] : '';

switch ($action) {
    case 'login':
        $email = isset($_POST['email']) ? $_POST['email'] : '';
        $maxacthuc = isset($_POST['maxacthuc']) ? $_POST['maxacthuc'] : '';
        
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
        $tendienthoai = isset($_POST['tendienthoai']) ? $_POST['tendienthoai'] : '';
        $hangsanxuat = isset($_POST['hangsanxuat']) ? $_POST['hangsanxuat'] : '';
        $ram = isset($_POST['ram']) ? (int)$_POST['ram'] : 0;
        $giaban = isset($_POST['giaban']) ? $_POST['giaban'] : 0;
        $manhinh_gap = isset($_POST['manhinh_gap']) ? (int)$_POST['manhinh_gap'] : 0;

        $stmt = $pdo->prepare("INSERT INTO dienthoai (tendienthoai, hangsanxuat, ram, giaban, manhinh_gap) VALUES (?, ?, ?, ?, ?)");
        if ($stmt->execute([$tendienthoai, $hangsanxuat, $ram, $giaban, $manhinh_gap])) {
            echo "{RESULT: SUCCESS}";
        } else {
            echo "{RESULT: FAILED}";
        }
        break;

    case 'update':
        $id = isset($_POST['id']) ? $_POST['id'] : '';
        $tendienthoai = isset($_POST['tendienthoai']) ? $_POST['tendienthoai'] : '';
        $hangsanxuat = isset($_POST['hangsanxuat']) ? $_POST['hangsanxuat'] : '';
        $ram = isset($_POST['ram']) ? (int)$_POST['ram'] : 0;
        $giaban = isset($_POST['giaban']) ? $_POST['giaban'] : 0;
        $manhinh_gap = isset($_POST['manhinh_gap']) ? (int)$_POST['manhinh_gap'] : 0;

        $stmt = $pdo->prepare("UPDATE dienthoai SET tendienthoai=?, hangsanxuat=?, ram=?, giaban=?, manhinh_gap=? WHERE id=?");
        if ($stmt->execute([$tendienthoai, $hangsanxuat, $ram, $giaban, $manhinh_gap, $id])) {
            echo "{RESULT: SUCCESS}";
        } else {
            echo "{RESULT: FAILED}";
        }
        break;

    case 'delete':
        $id = isset($_POST['id']) ? $_POST['id'] : '';
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