# 🏪 Sistema de Gestión de Bazar - Versión Simplificada

Sistema completo de punto de venta (POS) diseñado específicamente para bazares y tiendas de conveniencia en Perú. Desarrollado con Python y Tkinter, ofrece una interfaz intuitiva y funcionalidades esenciales para gestionar ventas, inventario y consultar reportes.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [Flujo de Trabajo Típico](#-flujo-de-trabajo-típico)
- [Solución de Problemas](#-solución-de-problemas)
- [Licencia](#-licencia)

---

## ✨ Características

### 🛒 **Gestión de Ventas**
- ✅ Búsqueda inteligente con autocompletado
- ✅ Múltiples métodos de pago (Efectivo, Yape, Plin, Otros)
- ✅ Cálculo automático de totales (General, Efectivo, Virtual)
- ✅ Productos de precio variable con guardado automático
- ✅ Interfaz con scroll para muchos productos

### 📦 **Control de Inventario**
- ✅ Gestión completa de productos (Agregar, Editar, Eliminar)
- ✅ Control de stock opcional (activable/desactivable)
- ✅ Stock siempre visible en búsqueda
- ✅ Alertas automáticas de stock bajo (≤ 5 unidades)
- ✅ Categorización de productos

### 📊 **Reportes Simplificados**
- ✅ **Cerrar Caja del Día**: Guarda ventas con resumen completo
- ✅ **Consultar Ventas Diarias**: Ver ventas de cualquier día específico
  - Selector de fecha con botones rápidos (Hoy, Ayer, etc.)
  - Productos agrupados con métodos de pago
  - Exportación individual a CSV
- ✅ **Inventario Vendido**: Filtrado por fecha, categoría o producto

### 💼 **Características Adicionales**
- ✅ Interfaz completamente en español
- ✅ Diseño adaptado al mercado peruano (S/)
- ✅ Alerta al cerrar con ventas pendientes
- ✅ Botón de emergencia para limpiar caja
- ✅ Sistema de archivos CSV fácil de editar
- ✅ Compatible con .py y .exe

---

## 🔧 Requisitos

### Requisitos del Sistema
- **Sistema Operativo**: Windows 7+, Linux, macOS
- **Python**: 3.8 o superior
- **Espacio en Disco**: ~50 MB
- **RAM**: 256 MB mínimo

### Dependencias de Python
```txt
tkinter (incluido con Python)
```

**Nota**: Ya no se requiere matplotlib. El sistema ha sido simplificado.

---

## 📥 Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/rebeatle/sistema-ventas.git
cd sistema-ventas
```

### 2. Crear Entorno Virtual (Opcional pero Recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Ejecutar el Sistema
```bash
python main.py
```

**¡No hay dependencias adicionales que instalar!** 🎉

---

## 🚀 Uso Rápido

### **Primera Ejecución**
El sistema creará automáticamente:
- `productos.csv` con productos de ejemplo
- Carpeta `ventas_diarias/` para almacenar historial
- `config_stock.txt` para configuración de inventario

### **Flujo Básico**

#### **1. Registrar Ventas**
1. Busca producto escribiendo su nombre o código
2. Selecciona de la lista desplegable
3. Define cantidad y método de pago (E/Y/P/O)
4. Click en **Agregar**
5. Repite para más productos

#### **2. Producto No Listado (Botón "Otro")**
Para productos sin precio fijo o no catalogados:
1. Click en botón **Otro**
2. Ingresa:
   - **Nombre**: Ej. "Copias A4 color"
   - **Precio Base**: Ej. 0.10 (se guardará para uso futuro)
   - **Cantidad**: Número de unidades
   - **Categoría**: Por defecto "Varios"
3. Selecciona método de pago
4. Click en **Agregar a Venta y Catálogo**
5. ✨ El producto se agrega a la venta Y se guarda automáticamente en `productos.csv` con código VAR001, VAR002, etc.

#### **3. Ver Resumen de Ventas Actuales**
- Los totales se actualizan automáticamente en la parte inferior
- **Total General**: Suma de todos los métodos
- **Efectivo**: Solo ventas en efectivo
- **Virtual**: Yape + Plin + Otros

#### **4. Cerrar Caja del Día**
Cuando termines el día:
1. Menú → **Reportes** → **📦 Cerrar Caja del Día**
2. Confirma la operación
3. Verás resumen completo:
   ```
   ✅ Caja Cerrada - Resumen:
   • Total del día: S/ 250.50
   • Efectivo: S/ 150.00
   • Virtual: S/ 100.50
   • Productos vendidos: 15
   
   Archivo guardado en:
   ventas_diarias/ventas_2024-12-06.csv
   ```
4. La lista de ventas se limpia automáticamente para el próximo día

#### **5. Consultar Ventas de Días Pasados**
1. Menú → **Reportes** → **📊 Consultar Ventas Diarias**
2. Opciones:
   - **Selector de fecha**: Ingresa YYYY-MM-DD
   - **Botones rápidos**: Hoy, Ayer, Hace 7 días, Hace 30 días
3. Click en **Buscar**
4. Verás:
   - Productos agrupados con cantidades totales
   - Métodos de pago por producto (Ej: "Efectivo (3), Yape (2)")
   - Totales por método con porcentajes
   - Total general del día
5. Click en **📄 Exportar CSV** para guardar reporte

---

## 📁 Estructura del Proyecto

```
sistema-bazar/
│
├── main.py                 # Punto de entrada
├── interfaz.py            # Interfaz gráfica (GUI)
├── logica.py              # Lógica de negocio
├── config.py              # Configuración del sistema
├── reportes.py            # Análisis y reportes
├── ventana_reportes.py    # Interfaces de reportes
│
├── productos.csv          # Base de datos de productos
├── config_stock.txt       # Configuración de stock (True/False)
│
└── ventas_diarias/        # Carpeta de historial (NUEVA)
    ├── ventas_2024-12-01.csv
    ├── ventas_2024-12-02.csv
    └── ventas_2024-12-06.csv
```

---

## 🎯 Funcionalidades Detalladas

### 📦 **Gestión de Productos**

#### **Agregar Producto Manualmente**
Menú → Productos → Agregar Producto
- Código único obligatorio
- Validación de precios (solo números positivos)
- Stock inicial configurable
- Categorización para reportes

#### **Agregar Producto con "Otro"**
- Genera código automático: `VAR001`, `VAR002`, `VAR003`...
- Se guarda permanentemente en `productos.csv`
- Reutilizable en ventas futuras
- Stock inicial: 0

#### **Editar Producto**
- Modificar cualquier campo excepto código
- Actualización en tiempo real en interfaz

#### **Eliminar Producto**
- Confirmación obligatoria
- No afecta historial de ventas anteriores

### 💰 **Métodos de Pago**

| Código | Método | Descripción |
|--------|--------|-------------|
| **E** | Efectivo | Pago en efectivo |
| **Y** | Yape | Billetera virtual BCP |
| **P** | Plin | Billetera virtual múltiple |
| **O** | Otros | Tarjetas, transferencias, etc. |

### 📊 **Sistema de Reportes**

#### **1. Cerrar Caja del Día** ⭐ PRINCIPAL
**Propósito:** Guardar ventas del día y comenzar nueva caja

**Características:**
- Guarda en `ventas_diarias/ventas_YYYY-MM-DD.csv`
- Muestra resumen con totales por método
- Limpia lista automáticamente
- No permite cerrar sin ventas

**Cuándo usar:**
- Al final del día laboral
- Antes de cambio de turno
- Para auditoría diaria

#### **2. Consultar Ventas Diarias** ⭐ DESTACADO
**Propósito:** Revisar ventas de cualquier día específico

**Características:**
- **Selector de fecha**: Ingresa fecha en formato YYYY-MM-DD
- **Botones rápidos**:
  - [Hoy]: Ventas del día actual
  - [Ayer]: Ventas de ayer
  - [Hace 7 días]: Ventas de hace 1 semana
  - [Hace 30 días]: Ventas de hace 1 mes
- **Vista agrupada**: Mismo producto aparece una vez con cantidad total
- **Desglose de métodos**: Muestra cómo se vendió cada producto
  - Ejemplo: "Efectivo (3), Yape (2)" = 3 unidades en efectivo, 2 en Yape
- **Totales por método**: Cuánto dinero por cada método
- **Porcentajes**: % de cada método sobre el total
- **Exportación**: Guarda como CSV individual

**Casos de uso:**
- Verificar ventas de días pasados
- Comparar ventas entre días
- Generar reportes para gerencia
- Auditoría de caja

#### **3. Inventario Vendido**
**Propósito:** Análisis de productos vendidos con filtros

**Filtros disponibles:**
- Rango de fechas personalizado
- Por categoría específica
- Por producto individual

**Muestra:**
- Código y nombre del producto
- Cantidad total vendida
- Ingresos generados
- Categoría

**Exportación:** CSV compatible con Excel

---

## 🔄 Flujo de Trabajo Típico

### **Día a Día**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ABRIR SISTEMA                                            │
│    python main.py                                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. REGISTRAR VENTAS DEL DÍA                                 │
│    • Buscar productos                                       │
│    • Agregar a lista                                        │
│    • Usar "Otro" para productos no listados                 │
│    • Ver totales en tiempo real                             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. CONSULTAR VENTAS ACTUALES (Opcional)                     │
│    Reportes → Consultar Ventas Diarias → [Hoy]             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. CERRAR CAJA AL FINAL DEL DÍA                             │
│    Reportes → Cerrar Caja del Día                           │
│    • Guarda en ventas_diarias/ventas_2024-12-06.csv        │
│    • Muestra resumen                                        │
│    • Limpia lista para mañana                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. REVISAR DÍAS PASADOS (Cuando sea necesario)             │
│    Reportes → Consultar Ventas Diarias → [Seleccionar]     │
└─────────────────────────────────────────────────────────────┘
```

### **Gestión de Productos**

```
┌─────────────────────────────────────────────────────────────┐
│ MÉTODO 1: Agregar Manualmente                               │
│ Productos → Agregar Producto                                │
│ • Código: 009                                               │
│ • Nombre: Yogurt Gloria                                     │
│ • Precio: 2.50                                              │
│ • Categoría: Lácteos                                        │
│ • Stock: 30                                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ MÉTODO 2: Agregar con "Otro" (Durante venta)               │
│ Botón "Otro" en pantalla principal                          │
│ • Nombre: Copias A4                                         │
│ • Precio Base: 0.10                                         │
│ • Cantidad: 15                                              │
│ → Se guarda automáticamente como VAR001                     │
│ → Próxima vez aparece en búsqueda                           │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configuración

### **Control de Stock**

#### **Activar Stock**
1. Menú → **Configuración** → **Gestión de Stock** → **✅ Activar Stock**
2. Efectos:
   - Stock se muestra en búsqueda: `Coca Cola - S/ 3.50 [STOCK: 50]`
   - Descuenta automáticamente al vender
   - Alerta cuando stock ≤ 5 unidades
   - No permite vender sin stock suficiente
   - Botón **"Ver Productos con Stock Bajo"** disponible

#### **Desactivar Stock**
1. Menú → **Configuración** → **Gestión de Stock** → **❌ Desactivar Stock**
2. Efectos:
   - No controla inventario
   - Permite ventas ilimitadas
   - Stock en CSV se mantiene pero no se usa

### **Formato de Archivos**

#### **productos.csv**
```csv
codigo,nombre,precio,categoria,stock
001,Coca Cola 500ml,3.50,Bebidas,50
VAR001,Copias A4,0.10,Varios,0
```

#### **ventas_diarias/ventas_2024-12-06.csv**
```csv
fecha,hora,codigo,nombre,cantidad,precio_unitario,subtotal,metodo_pago,categoria
2024-12-06,14:30:15,001,Coca Cola 500ml,2,3.50,7.00,E,Bebidas
2024-12-06,14:31:20,VAR001,Copias A4,10,0.10,1.00,E,Varios
```

---

## 🔧 Solución de Problemas

### **Problema: "No se encuentra el módulo tkinter"**
**Solución (Windows):**
```bash
# Reinstalar Python con tkinter incluido
# Descargar instalador desde python.org
# Marcar opción "tcl/tk and IDLE" durante instalación
```

**Solución (Linux):**
```bash
sudo apt-get install python3-tk
```

### **Problema: Stock no se actualiza al vender**
**Verificar:**
1. Menú → Configuración → Gestión de Stock
2. Debe estar **Activado**

### **Problema: "No hay ventas para guardar"**
**Causa:** Intentaste cerrar caja sin agregar productos

**Solución:**
1. Agrega al menos un producto a la venta
2. Luego: Menú → Reportes → Cerrar Caja del Día

### **Problema: Consultar Ventas Diarias muestra "Sin ventas"**
**Causa:** No hay ventas guardadas para esa fecha

**Solución:**
1. Verifica que cerraste caja ese día
2. Verifica la fecha en el selector (formato YYYY-MM-DD)
3. Si es el día actual, primero cierra caja

### **Problema: CSV con caracteres raros en Excel**
**Causa:** Codificación UTF-8

**Solución:**
1. Abrir Excel
2. Datos → **Obtener datos** → **Desde archivo** → **Desde texto/CSV**
3. Seleccionar archivo
4. Cambiar **Origen del archivo** a **UTF-8**
5. Click en **Cargar**

### **Problema: Cerré sin querer con ventas pendientes**
**Solución:**
- ¡No hay problema! El sistema pregunta antes de cerrar:
  - **SÍ**: Cerrar caja y salir (guarda ventas)
  - **NO**: Salir sin guardar
  - **CANCELAR**: No cerrar (vuelve al sistema)

### **Problema: Agregué producto equivocado**
**Solución:**
1. Click en botón **Eliminar** al lado del producto
2. Si el stock está activado, las unidades se devuelven automáticamente

### **Problema: Necesito limpiar toda la caja de emergencia**
**Solución:**
1. Menú → Reportes → **🗑️ Limpiar Caja (Emergencia)**
2. Confirma DOS veces (seguridad)
3. Todas las ventas actuales se eliminan
4. Stock se devuelve si está activado

---

## 📝 Changelog

### **v2.0.0** - 2024-12-06 (VERSIÓN LIMPIA)
#### Eliminado
- ❌ Sistema de autoguardado temporal
- ❌ Recuperación de sesión automática
- ❌ Top Productos (gráficos)
- ❌ Análisis de Pagos (gráficos)
- ❌ Gráficos Visuales (matplotlib)
- ❌ Exportar Reporte Completo

#### Agregado
- ✅ Botón "Otro" guarda automáticamente en productos.csv
- ✅ Códigos automáticos VAR001, VAR002, etc.
- ✅ Cerrar Caja con resumen visual
- ✅ Consultar Ventas Diarias con selector de fecha
- ✅ Botones rápidos (Hoy, Ayer, etc.)
- ✅ Limpiar Caja (Emergencia) con doble confirmación
- ✅ Alerta mejorada al cerrar con ventas pendientes

#### Mejorado
- ✅ Carpeta `ventas/` → `ventas_diarias/` (más descriptivo)
- ✅ Menú Reportes simplificado y reorganizado
- ✅ Documentación actualizada
- ✅ Código más limpio y mantenible

### **v1.2.0** - 2024-11-29
- Reporte del Día inicial
- Stock visible en lista

### **v1.0.0** - 2024-11-01
- Lanzamiento inicial

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 📞 Contacto

**Desarrollador**: rebe

**Repositorio**: [https://github.com/rebeatle/sistema-ventas](https://github.com/rebeatle/sistema-ventas)

**Issues**: Para reportar bugs o sugerir mejoras, usa la sección [Issues](https://github.com/rebeatle/sistema-ventas/issues) en GitHub

---

## ⭐ ¿Te gustó el proyecto?

Si este proyecto te fue útil, considera:
- ⭐ Darle una estrella en GitHub
- 🐛 Reportar bugs en [Issues](https://github.com/rebeatle/sistema-ventas/issues)
- 🤝 Contribuir con código mediante Pull Requests
- 📢 Compartirlo con otros bazares
- 💬 Dejar feedback sobre tu experiencia

---

**Hecho con ❤️ en Perú** 🇵🇪

---

**Última actualización:** 06 de diciembre de 2024  
**Versión:** 2.0.0 (Limpia y Optimizada)