# Operaciones: Backups, Restauración y Monitoreo

Este documento define los procedimientos operativos recomendados para la administración, recuperación y observabilidad de ProfeOnline en el entorno de producción.

## 💾 1. Estrategia de Backups y Restauración (PEND-004)

### SQLite (Entorno de pruebas / simple)
Si el sitio opera temporalmente con SQLite:
*   **Frecuencia:** Diaria.
*   **Método:** Copia del archivo `db.sqlite3` mediante snapshot en caliente.
*   **Comando de Respaldo:**
    ```bash
    sqlite3 db.sqlite3 ".backup 'backups/db_backup_$(date +%F).sqlite3'"
    ```
*   **Comando de Restauración:**
    ```bash
    cp backups/db_backup_[FECHA].sqlite3 db.sqlite3
    ```

### PostgreSQL / Supabase (Entorno de Producción)
Cuando el sitio esté enlazado a la base de datos PostgreSQL/Supabase en producción via `DATABASE_URL`:
*   **Frecuencia:** Automatizada diariamente (retención de 30 días) mediante la consola de Supabase o pg_dump.
*   **Comando de Respaldo Manual (pg_dump):**
    ```bash
    pg_dump -d "$DATABASE_URL" -F c -b -v -f "backups/db_backup_$(date +%F).dump"
    ```
*   **Comando de Restauración (pg_restore):**
    ```bash
    pg_restore -d "$DATABASE_URL" -v "backups/db_backup_[FECHA].dump"
    ```

### Plan de Rollback Operativo
En caso de que un deploy falle o corrompa datos:
1.  **Revertir el código:** Hacer checkout del último commit estable (`git checkout <hash_commit>`) o hacer redeploy de la versión anterior en el proveedor de hosting.
2.  **Revertir base de datos:** Si se realizaron migraciones irreversibles o destructivas, restaurar el último dump de base de datos antes del deploy.

---

## 📈 2. Monitoreo, Alertas y Logs (PEND-005)

### Registro de Logs (Logging)
El sistema utiliza el framework de logging nativo de Django configurado para volcar salidas a consola (stdout), capturadas automáticamente por el hosting (ej. Render, Heroku, Supabase logs).
*   Se registran con severidad `WARNING` o `ERROR` todos los intentos de autenticación rechazados en el webhook (`api_video.py`), así como excepciones de deserialización o bloqueos de rate limit.

### Checklist de Alertas en Producción
Se recomienda configurar integraciones con herramientas de monitoreo APM (ej. Sentry, Logtail, o alertas de la plataforma de hosting) para vigilar las siguientes métricas:
1.  **Errores 500 (Fatal Application Error):** Configurar alerta inmediata si se detectan más de 2 errores 500 en un rango de 5 minutos.
2.  **Errores 401/403 repetidos en API / Webhook:** Indica posibles ataques de fuerza bruta o tokens desactualizados. Configurar alerta si la tasa excede el rate limit usual.
3.  **Respuestas 429 (Too Many Requests):** Monitorear la activación de rate limiting en el webhook para detectar abusos en la red.
4.  **CPU / Memoria:** Alerta si el uso de memoria excede el 85% de la capacidad de la instancia por más de 10 minutos.
