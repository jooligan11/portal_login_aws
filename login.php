<?php
// Parámetros de conexión
$host = "localhost";
$usuario_db = "admin";
$contrasena_db = "123456";
$nombre_db = "login";

// Crear conexión
$conn = new mysqli($host, $usuario_db, $contrasena_db, $nombre_db);

// Verificar conexión
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

// Obtener datos del formulario
$usuario = $_POST['usuario'];
$contrasena = $_POST['contrasena'];

// Preparar consulta segura
$sql = "SELECT * FROM users WHERE user = ? AND password = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $usuario, $contrasena);
$stmt->execute();
$resultado = $stmt->get_result();

if ($resultado->num_rows === 1) {
    echo "✅ Acceso concedido. Bienvenido, $usuario.";
} else {
    echo "❌ Usuario o contraseña incorrectos.";
}

$stmt->close();
$conn->close();
?>
