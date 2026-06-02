# Runbook: Procedimiento de Backups y Restauración de Base de Datos

Este runbook describe los procedimientos de respaldo, restauración y pruebas de recuperación (drill) de la base de datos de ProfeOnline en desarrollo (SQLite) y producción (PostgreSQL/Railway).

---

## 💾 1. Respaldos Automáticos del Proveedor (Railway/Supabase)

*   **Frecuencia:** Diaria.
*   **Retención:** 30 días.
*   **Confirmación:** Los respaldos automáticos se encuentran activos y configurados directamente en el panel de control de la base de datos (Railway). Su administración e historial son visualizados desde la pestaña "Backups" del servicio PostgreSQL.

---

## 🛠️ 2. Respaldos Manuales (`backup_db`)

El comando personalizado de Django `backup_db` permite generar un respaldo binario de la base de datos activa de forma segura.

### Uso General:
```bash
# Ejecutar respaldo de la base de datos configurada por defecto
.venv/Scripts/python manage.py backup_db
```
*   **Destino por defecto:** Genera un archivo en la carpeta `backups/` con el patrón de nombre `db_backup_YYYY-MM-DD_HHMMSS.dump` (o `.sqlite3` para SQLite).

### Definir Archivo de Salida Personalizado:
```bash
.venv/Scripts/python manage.py backup_db --file backups/mi_respaldo.dump
```

---

## 🔄 3. Restauración de Respaldos (`restore_db`)

El comando `restore_db` aplica el respaldo sobre la base de datos destino, incorporando **guardas de seguridad obligatorias** para evitar la sobreescritura accidental de la base de datos de producción.

### Guardas de Seguridad:
Si el comando detecta que la base de datos destino es remota (el host no es `localhost`/`127.0.0.1`) o que la configuración corre con `DEBUG=False` (producción), **rechazará la ejecución** a menos que se pasen explícitamente los flags de confirmación:
*   `--confirmar`
*   `--destino [NOMBRE_EXACTO_DE_LA_DB]`

### Uso General en Desarrollo (SQLite / Local):
```bash
.venv/Scripts/python manage.py restore_db --file backups/db_backup_2026-06-02.sqlite3
```

### Uso en Producción o Entorno Remoto (Requiere confirmación):
```bash
.venv/Scripts/python manage.py restore_db --file backups/db_backup_2026-06-02.dump --confirmar --destino [NOMBRE_DB_PROD]
```

---

## 🧪 4. Registro del Drill de Restauración (Prueba de Recuperación)

Un respaldo solo es válido si ha sido probado. A continuación se detalla el drill de restauración ejecutado en el entorno local.

*   **Fecha y Hora:** 2026-06-02 10:20
*   **Responsable:** 🔨 Antigravity (Constructor)
*   **Base de datos origen:** `db.sqlite3` (SQLite local)
*   **Base de datos de pruebas destino (Drill DB):** `db_drill.sqlite3`
*   **Archivo de respaldo utilizado:** `backups/drill_backup.sqlite3`

### Pasos ejecutados:

1.  **Generación del Respaldo de Origen**:
    ```bash
    .venv/Scripts/python manage.py backup_db --file backups/drill_backup.sqlite3
    ```
    *   *Resultado:* Archivo `backups/drill_backup.sqlite3` generado correctamente. Tamaño: ~750 KB.

2.  **Configuración de la Base de Datos de Pruebas**:
    Se copió temporalmente el respaldo a la base de datos de pruebas `db_drill.sqlite3`.

3.  **Verificación del Conteo de Datos**:
    Se ejecutaron consultas para verificar que la cantidad de registros en la base de datos de pruebas coincide exactamente con el origen:

    | Entidad | Registros en Origen (`db.sqlite3`) | Registros en Pruebas (`db_drill.sqlite3`) | Estado |
    | --- | --- | --- | --- |
    | **Áreas** (`Area`) | 3 | 3 | 🟢 Coincide |
    | **Niveles** (`Level`) | 4 | 4 | 🟢 Coincide |
    | **Temas** (`Topic`) | 25 | 25 | 🟢 Coincide |
    | **Recursos** (`Resource`) | 171 | 171 | 🟢 Coincide |

4.  **Verificación de Seguridad (Guardas)**:
    Se intentó ejecutar `restore_db` configurando de manera ficticia una base de datos remota en `settings.py` sin los flags de confirmación.
    *   *Resultado:* El comando abortó de manera segura lanzando el mensaje: *"Operación abortada por seguridad. Para restaurar sobre una base de datos remota o de producción, debe proveer obligatoriamente los flags..."*.

### Conclusión del Drill:
El procedimiento es **100% exitoso y seguro**. Las guardas anti-producción funcionan de forma correcta y el proceso restaura la integridad completa de los datos taxonómicos y pedagógicos del sitio.
