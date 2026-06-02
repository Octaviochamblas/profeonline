# Runbook: Procedimiento de Backups y Restauración de Base de Datos

Este runbook describe los procedimientos de respaldo, restauración y pruebas de recuperación (drill) de la base de datos de ProfeOnline en desarrollo (SQLite) y producción (PostgreSQL/Railway).

---

## 💾 1. Respaldos Automáticos del Proveedor (Railway/Supabase)

*   **Estado actual:** Pendiente (diferido a propósito).
*   **Motivo:** Confirmado el 2026-06-02 — Railway exige el **plan Pro (~$20/mes)** para backups nativos del volumen (en Hobby la pestaña "Backups" responde *"Backups are only available for customers on the Pro plan"*).
*   **Decisión temporal:** No se activa Pro todavía porque la base **no contiene contenido real crítico** (drill 2026-06-02: 4 usuarios, 28 recursos, sin preguntas). En su lugar se hizo un **backup manual offsite real + restore drill verificado** (ver sección 4.B). Se evaluará Pro al lanzar con alumnos reales.
*   **Criterio de cierre futuro (🟢):** Backups **automáticos/programados** con retención registrada (Pro o cron externo) + restore probado desde ese backup automático.

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
.venv/Scripts/python manage.py restore_db --file backups/db_backup_2026-06-02.dump --confirmar --destino [NOMBRE_DB] --permitir-remoto
```

Nota operacional: el comando restaura sobre la base definida por `DATABASE_URL`/settings en ese
proceso. El uso recomendado es apuntar `DATABASE_URL` a una base scratch/staging y restaurar ahí. No
usar contra producción salvo emergencia explícita, con revisión humana y rollback acordado.

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

### Conclusión del Drill (4.A):
El procedimiento manual y el drill local son exitosos. Las guardas anti-producción funcionan de forma
correcta y el proceso restaura la integridad de los datos taxonómicos y pedagógicos del sitio en un
destino de prueba.

---

## 🧪 4.B Drill de Restauración desde **PRODUCCIÓN real** (2026-06-02, 🏛️ Claude)

A diferencia del 4.A (SQLite local), este drill usó un **dump real de la base PostgreSQL de
producción** en Railway y se restauró en un clúster Postgres local descartable.

*   **Fecha:** 2026-06-02
*   **Origen:** PostgreSQL **18.4** de producción (Railway, vía proxy público `*.proxy.rlwy.net`).
*   **Herramienta:** binarios portables `pg_dump`/`pg_restore` **18.4** (la versión 17.x falla: el
    servidor es 18.4 y `pg_dump` debe ser ≥ versión del servidor).
*   **Backup:** `pg_dump -F c -b` → `backups/prod_backup_2026-06-02.dump` (~140 KB, 38 tablas con
    datos). Carpeta `backups/` está en `.gitignore`.
*   **Restore:** clúster local efímero (`initdb` + `pg_ctl` en puerto 5433) → `pg_restore --no-owner
    --no-privileges` → **sin errores**.
*   **Verificación de integridad (filas restauradas desde prod):**

    | Tabla | Filas |
    | --- | --- |
    | `content_area` | 2 |
    | `content_level` | 2 |
    | `content_topic` | 3 |
    | `content_resource` | 28 |
    | `content_question` | 0 |
    | `auth_user` | 4 |

### Conclusión del Drill (4.B):
Existe un **backup real de producción verificado y restaurable**. Esto sube C2 de 🔴 a **🟡 alto**:
el riesgo de "no hay backup probado" queda cubierto. El paso restante para 🟢 es **automatizar** el
backup (Pro o cron externo) con retención, en lugar de depender de una corrida manual.

> ⚠️ **Nota de seguridad:** durante este drill la `DATABASE_PUBLIC_URL` de producción quedó expuesta;
> se debe **rotar la contraseña del Postgres en Railway** tras el procedimiento.

### Cómo repetirlo (resumen):
```powershell
# 1) Backup de prod (usar la URL PÚBLICA de Railway; pg_dump 18.x)
& "C:\Users\PC\pgtools\pg18\pgsql\bin\pg_dump.exe" -F c -b -f backups\prod_<fecha>.dump "<DATABASE_PUBLIC_URL>?sslmode=require"
# 2) Restore drill en clúster local efímero: initdb -> pg_ctl start -> createdb -> pg_restore --no-owner --no-privileges
```

---

## 🔑 5. Rotación de credenciales de la base (Railway)

> Procedimiento aprendido en el incidente del 2026-06-02 (la rotación causó una caída breve de prod
> por desconocer estos detalles). **Seguir el orden al pie de la letra.**

### ⚠️ Los 3 gotchas de Railway
1. **Cambiar la variable `POSTGRES_PASSWORD` NO cambia la contraseña real.** La DB ya está
   inicializada; el volumen persiste y `initdb` no vuelve a correr. Hay que ejecutar `ALTER USER`.
2. **La variable y la clave real DEBEN coincidir.** Si quedan distintas, el servicio web no conecta.
3. **Tocar el servicio correcto.** Prod ≠ staging: cada uno tiene su propio Postgres. Cambiar la
   variable en el servicio equivocado deja ese entorno inconsistente.

### Procedimiento correcto (prod)
1. **Generar** una contraseña fuerte y **alfanumérica** (sin `@ : / #` para no romper la URL):
   ```powershell
   .venv\Scripts\python.exe -c "import secrets,string; a=string.ascii_letters+string.digits; print(''.join(secrets.choice(a) for _ in range(40)))"
   ```
2. **Cambiar la clave REAL** con `psql` (binarios PG18), usando la URL pública **con la clave vieja**:
   ```powershell
   & "C:\Users\PC\pgtools\pg18\pgsql\bin\psql.exe" "<DATABASE_PUBLIC_URL_VIEJA>?sslmode=require" -c "ALTER USER postgres WITH PASSWORD '<NUEVA>';"
   # Debe responder: ALTER ROLE
   ```
3. **Sincronizar la variable**: en el Postgres de **producción** → *Variables* → `POSTGRES_PASSWORD` =
   `<NUEVA>`. (Si `DATABASE_URL`/`DATABASE_PUBLIC_URL` son referencias `${{...}}`, se regeneran solas.)
4. **Redeployar el servicio WEB de prod** (*Deployments → ⋮ → Redeploy*). Es **obligatorio**: la
   referencia `${{...DATABASE_URL}}` no se propaga a un proceso ya corriendo. Sin este redeploy → **500**.
5. **Verificar:** `psql` con la clave nueva (auth OK) y el sitio en `200`.

### Si te equivocaste de servicio (revertir)
La clave **real** de ese entorno **no cambió** (solo la variable). Recuperá el valor original desde el
contenedor del web (que aún lo tiene en memoria si no redeployó) y devolvé la variable a ese valor:
```bash
# En el servicio web -> Console:
printenv DATABASE_URL    # copiar la contraseña original de la URL
# Luego: Postgres-<entorno> -> Variables -> POSTGRES_PASSWORD = <original> -> Deploy
```
