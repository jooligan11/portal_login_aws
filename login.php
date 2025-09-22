<?php
// Parámetros de conexión
$host = "localhost";
$usuario_db = "root";
$contrasena_db = "";
$nombre_db = "mi_base_de_datos";

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
$sql = "SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?";
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
