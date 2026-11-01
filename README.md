# TasaFácil: Calculadora de Tasas de Cambio y Presupuestos para Emprendedores

Aplicación web para emprendedores y pequeños negocios venezolanos que permite
consultar las tasas del día (BCV, Euro, Binance), convertir montos USD↔Bs y
calcular presupuestos de compra-venta considerando el diferencial cambiario real.

---

## Metodología de Desarrollo en V — Rama Descendente

### 1. Análisis de Requisitos (Requirement Gathering)

**Necesidad del usuario:** En Venezuela, los proveedores venden en dólares a
distintas tasas (BCV, Euro, Binance), pero el vendedor final suele estar obligado
a vender a tasa BCV. Esto genera un diferencial cambiario que el emprendedor debe
considerar para no vender a pérdida. No existe una herramienta accesible que
combine tasas del día + cálculo de presupuestos con tasas de compra y venta
diferenciadas.

**Requisitos funcionales clave:**
- Consulta pública de las tres tasas del día con variación y spread.
- Conversor USD↔Bs en las tres tasas.
- Calculadora de presupuestos multi-ítem con tasa de compra por ítem y tasa de venta global.
- Dos modos de cálculo: precio→% ganancia y % ganancia→precio.
- Ganancia expresada en Bs y en las tres tasas USD.
- Alerta de venta a pérdida.
- Registro de usuarios para guardar presupuestos, productos e historial.
- Exportación a PDF (cotización) y Excel (listado).
- Administrador que gestiona usuarios y corrige tasas manualmente.

**Roles:** Visitante, Usuario y Administrador.

### 2. Análisis del Sistema (System Analysis)

**Comportamiento general:** La aplicación tiene dos grandes áreas:

- **Área pública (Visitante):** tasas del día, conversor y calculadora en modo
  efímero (sin guardar). No requiere autenticación.
- **Área privada (Usuario):** gestión de productos, creación/edición de
  presupuestos, historial, exportación y perfil de negocio.
- **Área administrativa (Administrador):** gestión de usuarios y tasas desde
  Django Admin.

**Arquitectura funcional:** Aplicación Django monolítica con renderizado de
plantillas (SSR). El flujo es: request → vista Django → modelo → template →
respuesta. Vite se usa exclusivamente para compilar assets (CSS/JS) del frontend.

**Módulos funcionales:**
1. Tasas (consulta, historial, spread, actualización automática).
2. Conversión (USD↔Bs).
3. Autenticación (registro, login, perfil de negocio).
4. Productos (CRUD del catálogo del usuario).
5. Presupuestos (cálculo, guardado, historial, edición).
6. Exportación (PDF y Excel).
7. Administración (Django Admin).

**Justificación del login:** La autenticación no es un requisito artificial; es
la puerta de entrada al historial y la reutilización de presupuestos y catálogos.
El Visitante puede probar la calculadora sin registrarse, pero guardar requiere
cuenta, asociando los datos a un emprendedor concreto.

### 3. Diseño de Software / Arquitectura (Software Design)

**Stack tecnológico:**
- **Backend:** Python 3.12 + Django 5.x.
- **Base de datos:** PostgreSQL 16 (vía Docker, fase final).
- **Frontend:** Django Templates + Vite.js para assets (CSS/JS).
- **Gráficos:** Chart.js.
- **Exportación:** ReportLab (PDF) + openpyxl (Excel).
- **Tasas automáticas:** librería `pyDolarVenezuela` / API pública de Binance.
- **Contenedores:** Docker + docker-compose (fase final).

**Componentes principales:**
- `config/` — configuración del proyecto Django.
- `tasas/` — modelo Tasa, servicio de actualización, vistas públicas.
- `cuentas/` — autenticación + perfil de negocio.
- `productos/` — catálogo de productos del usuario.
- `presupuestos/` — cálculo, guardado, historial, exportación.
- `templates/` — plantillas base, públicas y privadas.

**Interfaces:**
- Pública: `/` (home), `/tasas/`, `/conversor/`, `/presupuesto/probar/`.
- Privada: `/cuenta/panel/`, `/productos/`, `/presupuestos/`.
- Admin: `/admin/`.

**Seguridad:** Uso de `django.contrib.auth`, vistas protegidas con
`@login_required`, permisos por grupo, CSRF en formularios, contraseñas
hasheadas, y snapshots de tasas en presupuestos para integridad histórica.

### 4. Diseño de Módulos (Module Design)

**Módulo Tasas:**
- Modelo `Tasa` con `fuente` (BCV/Euro/Binance), `valor_bs_por_usd`, `fecha`,
  `origen` (auto/manual). Restricción única en `(fuente, fecha)`.
- Servicio `actualizar_tasas()` invocado por comando de gestión (cron diario).
- Fallback: si la API falla, se reutiliza la última tasa guardada con flag
  `desactualizada=True` en la vista.

**Módulo Conversión:**
- Función pura `convertir(monto, tasa_origen, tasa_destino)` reutilizada por
  el conversor y por el cálculo de presupuestos.

**Módulo Autenticación:**
- `User` de Django + `PerfilNegocio` (OneToOne) con nombre, RIF, teléfono, logo.
- Registro por email (`USERNAME_FIELD='email'`), sin verificación.

**Módulo Productos:**
- CRUD estándar. Cada producto pertenece a un usuario. Costo en USD.

**Módulo Presupuestos:**
- Modelos `Presupuesto` e `ItemPresupuesto`.
- Cada ítem guarda snapshot de `tasa_compra_fuente` y `tasa_compra_valor`.
- El presupuesto guarda snapshot de `tasa_venta_fuente` y `tasa_venta_valor`.
- Lógica de cálculo (pseudocódigo):

```
total_costo_bs = Σ (costo_usd_unitario × cantidad × tasa_compra_valor_ítem)
total_venta_bs = total_venta_usd × tasa_venta_valor

# Modo A (precio conocido)
porcentaje_ganancia = (total_venta_bs - total_costo_bs) / total_costo_bs × 100

# Modo B (ganancia objetivo)
total_venta_bs = total_costo_bs × (1 + porcentaje_objetivo / 100)
total_venta_usd = total_venta_bs / tasa_venta_valor

ganancia_bs = total_venta_bs - total_costo_bs
ganancia_usd_bcv    = ganancia_bs / tasa_bcv
ganancia_usd_euro   = ganancia_bs / tasa_euro
ganancia_usd_binance= ganancia_bs / tasa_binance
```

- Alerta `venta_a_perdida=True` si `ganancia_bs <= 0`.

**Módulo Exportación:**
- Vista `export_pdf(presupuesto_id)` → genera PDF con ReportLab, incluye datos
  del `PerfilNegocio`.
- Vista `export_xlsx()` → genera Excel con openpyxl, listado del historial.

**Módulo Administración:**
- `admin.site.register(Tasa, TasaAdmin)` con edición de valor y origen.
- Admin de usuarios estándar de Django.

### Punto de Inflexión: Codificación (Coding)

A partir de este punto inicia la construcción del código siguiendo la fase
ascendente de verificación (pruebas unitarias por módulo, pruebas de integración
de cálculo de presupuestos, y pruebas de aceptación con usuarios reales).

# Levantar todo
docker compose up --build

# Realizar migraciones
docker compose exec web python manage.py migrate 

# Crear superusuario
docker compose exec web python manage.py createsuperuser 

# Acceder a la app
# http://localhost:8000

# Detener
docker compose down
