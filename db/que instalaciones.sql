USE spidernet_web;
CREATE TABLE instalaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    coordenadas VARCHAR(50),  -- Para geolocalización (latitud, longitud)
    tipo_instalacion ENUM('Residencial', 'Empresarial', 'Otro') NOT NULL,
    equipo_instalado TEXT,  -- Detalles del equipo (router, antena, ONT, etc.)
    tecnico_asignado VARCHAR(100) NOT NULL,
    estado ENUM('Pendiente', 'En Proceso', 'Completada', 'Cancelada') DEFAULT 'Pendiente',
    fecha_programada DATETIME,
    fecha_realizacion DATETIME NULL,  
    observaciones TEXT,
    fotos JSON,  -- Para guardar evidencias de instalación (URLs o base64)
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE
);
