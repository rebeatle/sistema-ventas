# 🏪 Sistema de Gestión de Bazar

Sistema completo de punto de venta (POS) diseñado específicamente para bazares y tiendas de conveniencia en Perú. Desarrollado con Python y Tkinter, ofrece una interfaz intuitiva y funcionalidades completas para gestionar ventas, inventario y generar reportes detallados.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [Configuración](#-configuración)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## ✨ Características

### 🛒 **Gestión de Ventas**
- ✅ Registro rápido de ventas con búsqueda inteligente de productos
- ✅ Múltiples métodos de pago (Efectivo, Yape, Plin, Otros)
- ✅ Cálculo automático de totales por método de pago
- ✅ Productos de precio variable (copias, impresiones, servicios)
- ✅ Historial completo de ventas con fecha y hora
- ✅ Interfaz intuitiva con scroll para muchos productos

### 📦 **Control de Inventario**
- ✅ Gestión completa de productos (Agregar, Editar, Eliminar)
- ✅ Control de stock opcional (activable/desactivable)
- ✅ Stock siempre visible en lista de productos
- ✅ Alertas automáticas de stock bajo (≤ 5 unidades)
- ✅ Categorización de productos
- ✅ Actualización automática de stock al vender

### 📊 **Reportes y Análisis**
- ✅ **Reporte del Día**: Vista rápida de ventas diarias con:
  - Productos agrupados por nombre
  - Cantidad total vendida de cada producto
  - Desglose por método de pago por producto
  - Totales y porcentajes por método de pago
  - Exportación a CSV para compartir
- ✅ **Inventario Vendido**: Filtrado por fecha, categoría o producto
- ✅ **Top 10 Productos**: Por cantidad vendida y por ingresos
- ✅ **Análisis de Métodos de Pago**: Distribución y porcentajes
- ✅ **Gráficos Visuales**: 
  - Ventas por categoría (gráficos de pastel)
  - Tendencia de ventas diarias (línea)
  - Top productos (barras horizontales)
- ✅ **Exportación de Reportes Completos**: Formato CSV con rango de fechas personalizable

### 💼 **Características Adicionales**
- ✅ Interfaz completamente en español
- ✅ Diseño adaptado al mercado peruano
- ✅ Soporte para soles peruanos (S/)
- ✅ Sistema de archivos CSV para fácil edición
- ✅ Sin necesidad de base de datos
- ✅ Portable y ligero

---

## 📸 Capturas de Pantalla

### Pantalla Principal de Ventas
```
┌─────────────────────────────────────────────────────────────────┐
│ Archivo  Productos  Reportes  Configuración                    │
├─────────────────────────────────────────────────────────────────┤
│ Producto: [Coca Cola 500ml - S/ 3.50 [STOCK: 50] ▼]           │
│           Cant:[1] Pago:[E Y P O]  [Agregar]  [Otro]           │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Producto               Cant  P.Unit  Subtotal  Pago  Acciones│ │
│ │ Coca Cola 500ml         2    S/3.50  S/7.00    E    [Eliminar]│ │
│ │ Galletas Oreo           1    S/4.50  S/4.50    Y    [Eliminar]│ │
│ └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ TOTAL GENERAL: S/ 11.50  |  Efectivo: S/ 7.00  |  Virtual: S/ 4.50│
└─────────────────────────────────────────────────────────────────┘
```

### Reporte del Día
```
┌─────────────────────────────────────────────────────────────────┐
│                    📊 REPORTE DEL DÍA                           │
│                   Fecha: Sábado 29/11/2024                      │
├─────────────────────────────────────────────────────────────────┤
│ Producto          │ Cant Total │ P.Unit  │ Subtotal │ Métodos  │
│ Coca Cola 500ml   │     5      │ S/ 3.50 │ S/ 17.50 │ E(3),Y(2)│
│ Galletas Oreo     │     3      │ S/ 4.50 │ S/ 13.50 │ Yape (3) │
├─────────────────────────────────────────────────────────────────┤
│ 💰 RESUMEN DE PAGOS:                                            │
│   Efectivo:  S/ 10.50  (33.9%)                                 │
│   Yape:      S/ 20.50  (66.1%)                                 │
│   Plin:      S/  0.00  ( 0.0%)                                 │
│   Otros:     S/  0.00  ( 0.0%)                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━                                    │
│   TOTAL GENERAL: S/ 31.00                                      │
│   (2 productos diferentes | 2 transacciones)                   │
└─────────────────────────────────────────────────────────────────┘
```

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
matplotlib>=3.5.0
```

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

### 3. Instalar Dependencias
```bash
pip install matplotlib
```

### 4. Ejecutar el Sistema
```bash
python main.py
```

---

## 🚀 Uso

### Inicio Rápido

#### **Primera Ejecución**
El sistema creará automáticamente:
- `productos.csv` con productos de ejemplo
- Carpeta `ventas/` para almacenar historial
- `config_stock.txt` para configuración de inventario

#### **Agregar Productos**
1. Menú → **Productos** → **Agregar Producto**
2. Completa los campos:
   - **Código**: Identificador único (ej: 001, ABC123)
   - **Nombre**: Nombre descriptivo del producto
   - **Precio**: Precio en soles (ej: 3.50)
   - **Categoría**: Bebidas, Snacks, Dulces, etc.
   - **Stock Inicial**: Cantidad disponible (si stock está activado)
3. Click en **Guardar**

#### **Registrar Venta**
1. Selecciona producto del desplegable (muestra nombre, precio y stock)
2. Define cantidad con el control numérico
3. Elige método de pago:
   - **E**: Efectivo
   - **Y**: Yape
   - **P**: Plin
   - **O**: Otros (tarjetas, transferencias)
4. Click en **Agregar**
5. Repite para más productos
6. Al finalizar: Menú → **Reportes** → **Guardar ventas**

#### **Producto de Precio Variable**
Para productos sin precio fijo (copias, impresiones, servicios):
1. Click en botón **Otro**
2. Ingresa:
   - **Descripción**: Ej. "Copias A4 color"
   - **Cantidad**: Número de unidades
   - **Precio Unitario**: Precio por unidad
3. Selecciona método de pago
4. Click en **Agregar a Venta**

#### **Ver Reporte del Día** ⭐ NUEVO
Para revisar caja al final del día:
1. Menú → **Reportes** → **📊 Reporte del Día**
2. Verás:
   - **Productos agrupados**: Cada producto aparece una sola vez con su cantidad total
   - **Métodos de pago por producto**: "Efectivo (3), Yape (2)" muestra cómo se vendió
   - **Totales por método**: Cuánto dinero hay en efectivo, Yape, Plin, etc.
   - **Total general**: Suma de todos los métodos
3. Click en **📄 Exportar CSV** para guardar o compartir
4. Click en **🔄 Actualizar** para refrescar datos

#### **Ver Reportes Avanzados**
1. Menú → **Reportes** → Selecciona tipo:
   - **Inventario Vendido**: Productos vendidos con filtros
   - **Top Productos**: Los 10 más vendidos
   - **Análisis de Pagos**: Distribución de métodos
   - **Gráficos**: Visualizaciones con matplotlib
   - **Exportar Reporte Completo**: CSV con análisis completo personalizable

---

## 📁 Estructura del Proyecto

```
sistema-bazar/
│
├── main.py                 # Punto de entrada principal
├── interfaz.py            # Interfaz gráfica (GUI)
├── logica.py              # Lógica de negocio
├── config.py              # Configuración del sistema
├── reportes.py            # Módulo de análisis y reportes
├── ventana_reportes.py    # Interfaces de reportes
│
├── productos.csv          # Base de datos de productos
├── config_stock.txt       # Configuración de stock (True/False)
│
├── ventas/               # Carpeta de historial
│   ├── ventas_2024-11-29.csv
│   ├── ventas_2024-11-30.csv
│   └── ...
│
├── requirements.txt      # Dependencias del proyecto
├── README.md            # Este archivo
└── LICENSE              # Licencia MIT
```

---

## 🎯 Funcionalidades Detalladas

### 📦 Gestión de Productos

#### **Agregar Producto**
- Código único obligatorio
- Validación de precios (solo números positivos)
- Stock inicial configurable
- Categorización para reportes

#### **Editar Producto**
- Modificar cualquier campo excepto código
- Actualización en tiempo real en interfaz
- Preserva historial de ventas previas

#### **Eliminar Producto**
- Confirmación obligatoria antes de eliminar
- No afecta historial de ventas anteriores
- Elimina de `productos.csv`

### 💰 Métodos de Pago

| Código | Método | Descripción | Uso Común |
|--------|--------|-------------|-----------|
| **E** | Efectivo | Pago en efectivo | Billetes y monedas |
| **Y** | Yape | Billetera virtual BCP | Transferencia móvil |
| **P** | Plin | Billetera virtual múltiple | Transferencia móvil |
| **O** | Otros | Tarjetas, transferencias, etc. | Cualquier otro método |

### 📊 Sistema de Reportes

#### **1. Reporte del Día** ⭐ DESTACADO
**Propósito:** Revisión rápida de caja al final del día

**Características:**
- **Agrupación inteligente**: Si vendes el mismo producto varias veces, aparece una sola vez
- **Desglose de métodos**: Muestra cómo se vendió cada producto
  - Ejemplo: "Efectivo (3), Yape (2)" = 3 unidades en efectivo, 2 en Yape
- **Totales por método**: Cuánto dinero físico vs virtual tienes
- **Porcentajes**: % de cada método sobre el total
- **Exportación**: Guarda como CSV para compartir con gerencia

**Casos de uso:**
- Cerrar caja al final del día
- Verificar que el dinero físico coincida con ventas en efectivo
- Enviar resumen diario al dueño
- Auditoría rápida de ventas

#### **2. Inventario Vendido**
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

#### **3. Top 10 Productos**
**Dos vistas:**
- **Por cantidad**: Los más vendidos en unidades
- **Por ingresos**: Los que generaron más dinero

**Incluye:**
- Gráficos de barras horizontales (opcional)
- Código, nombre, categoría
- Cantidad o ingreso según vista

#### **4. Análisis de Métodos de Pago**
**Muestra:**
- Total por método (Efectivo, Yape, Plin, Otros)
- Porcentaje de cada método
- Gráfico de barras comparativo

**Útil para:**
- Saber cuánto efectivo esperar en caja
- Planificar cambio necesario
- Entender preferencias de pago de clientes

#### **5. Gráficos Visuales**
Requiere matplotlib instalado

**Tipos de gráficos:**
- **Ventas por categoría**: Gráfico de pastel doble (cantidad e ingresos)
- **Tendencia diaria**: Línea temporal de ventas
- **Top productos**: Barras horizontales con colores

#### **6. Reporte Completo Exportable**
**Contenido:**
- Resumen general (totales, promedios, fechas)
- Top 10 productos por cantidad
- Ventas por categoría
- Análisis de métodos de pago

**Formato:** CSV estructurado por secciones

**Uso:** Informes mensuales, análisis de tendencias

---

## ⚙️ Configuración

### Control de Stock

El sistema permite activar/desactivar el control de inventario:

#### **Activar Stock**
1. Menú → **Configuración** → **Gestión de Stock** → **✅ Activar Stock**
2. Efectos:
   - Stock se muestra en lista de productos: `[STOCK: 50]`
   - Descuenta automáticamente al vender
   - Alerta cuando stock ≤ 5 unidades: **"ADVERTENCIA: Stock bajo para X: N unidades"**
   - No permite vender sin stock suficiente
   - Botón **"Ver Productos con Stock Bajo"** disponible

#### **Desactivar Stock**
1. Menú → **Configuración** → **Gestión de Stock** → **❌ Desactivar Stock**
2. Efectos:
   - No controla inventario
   - Permite ventas ilimitadas
   - Stock en CSV se mantiene pero no se usa

#### **Recargar Productos**
Si editas `productos.csv` manualmente:
1. Menú → **Archivo** → **Recargar Productos**
2. Los cambios se reflejan inmediatamente

### Formato de Archivos

#### **productos.csv**
```csv
codigo,nombre,precio,categoria,stock
001,Coca Cola 500ml,3.50,Bebidas,50
002,Galletas Oreo,4.50,Snacks,30
003,Copias A4,0.10,Servicios,0
```

**Notas:**
- Código debe ser único
- Precio con punto decimal (3.50, no 3,50)
- Stock: 0 si está desactivado o para productos variables

#### **ventas/ventas_YYYY-MM-DD.csv**
```csv
fecha,hora,codigo,nombre,cantidad,precio_unitario,subtotal,metodo_pago,categoria
2024-11-29,14:30:15,001,Coca Cola 500ml,2,3.50,7.00,E,Bebidas
2024-11-29,14:31:20,VAR,Copias A4,10,0.10,1.00,E,Varios
```

**Notas:**
- Un archivo por día
- Código `VAR` para productos de precio variable
- Hora en formato 24h

#### **config_stock.txt**
```
True
```
o
```
False
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

### **Problema: Gráficos no se muestran**
**Causa:** matplotlib no instalado

**Solución:**
```bash
pip install matplotlib
```

### **Problema: Stock no se actualiza al vender**
**Verificar:**
1. Menú → Configuración → Gestión de Stock
2. Debe estar **Activado**
3. Si aparece desactivado, hacer click en **✅ Activar Stock**

### **Problema: "No hay ventas para guardar"**
**Causa:** Intentaste guardar sin agregar productos

**Solución:**
1. Agrega al menos un producto a la venta
2. Luego: Menú → Reportes → Guardar ventas

### **Problema: Reporte del Día está vacío**
**Causa:** No hay ventas guardadas para hoy

**Solución:**
1. Registra y **guarda** al menos una venta
2. Menú → Reportes → Guardar ventas
3. Luego: Menú → Reportes → Reporte del Día

### **Problema: CSV con caracteres raros al abrir en Excel**
**Causa:** Codificación UTF-8

**Solución:**
1. Abrir Excel
2. Datos → **Obtener datos** → **Desde archivo** → **Desde texto/CSV**
3. Seleccionar archivo
4. Cambiar **Origen del archivo** a **UTF-8**
5. Click en **Cargar**

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature:
   ```bash
   git checkout -b feature/NuevaCaracteristica
   ```
3. Commit tus cambios:
   ```bash
   git commit -m 'Add: nueva característica increíble'
   ```
4. Push a la rama:
   ```bash
   git push origin feature/NuevaCaracteristica
   ```
5. Abre un Pull Request

### Guías de Contribución
- Mantén el código en español (comentarios y variables)
- Sigue el estilo PEP 8
- Documenta nuevas funciones con docstrings
- Prueba antes de enviar PR
- Actualiza README si agregas funcionalidades

---

## 📝 Changelog

### **v1.2.0** - 2024-11-29
#### Agregado
- ⭐ **Reporte del Día**: Vista rápida con productos agrupados
- 📊 Desglose de métodos de pago por producto
- 📄 Exportación de Reporte del Día a CSV
- 📦 Stock siempre visible en lista de productos

#### Mejorado
- ✅ Ventana "Otro" ahora tiene scroll
- ✅ Exportar Reporte Completo con selector de fechas funcional
- 🔧 Código duplicado eliminado

#### Corregido
- 🐛 Productos duplicados en reportes (ahora agrupados correctamente)
- 🐛 VentanaExportarReporte sin interfaz funcional

### **v1.1.0** - 2024-11-15
#### Agregado
- Control de stock opcional
- Alertas de stock bajo
- Productos de precio variable
- Gráficos con matplotlib

### **v1.0.0** - 2024-11-01
#### Lanzamiento inicial
- Sistema de ventas básico
- Gestión de productos
- Reportes simples

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 rebe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Contacto

**Desarrollador**: rebe

**Repositorio**: [https://github.com/rebeatle/sistema-ventas](https://github.com/rebeatle/sistema-ventas)

**Issues**: Para reportar bugs o sugerir mejoras, usa la sección [Issues](https://github.com/rebeatle/sistema-ventas/issues) en GitHub

---

## 🙏 Agradecimientos

- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Framework GUI
- [Matplotlib](https://matplotlib.org/) - Gráficos y visualizaciones
- Comunidad de desarrolladores Python en Perú
- Todos los que han probado y dado feedback
- Usuarios del sistema que sugirieron mejoras

---

## ⭐ ¿Te gustó el proyecto?

Si este proyecto te fue útil, considera:
- ⭐ Darle una estrella en GitHub
- 🐛 Reportar bugs o sugerir mejoras en [Issues](https://github.com/rebeatle/sistema-ventas/issues)
- 🤝 Contribuir con código mediante Pull Requests
- 📢 Compartirlo con otros bazares y negocios
- 💬 Dejar feedback sobre tu experiencia

---

## 🎯 Roadmap Futuro

### **En consideración:**
- [ ] Impresión de tickets de venta
- [ ] Backup automático de datos
- [ ] Modo oscuro para la interfaz
- [ ] Soporte para múltiples usuarios
- [ ] Integración con impresoras térmicas
- [ ] App móvil complementaria
- [ ] Sincronización en la nube (opcional)
- [ ] Sistema de clientes frecuentes
- [ ] Generación de códigos de barras

**¿Tienes una sugerencia?** Abre un [Issue](https://github.com/rebeatle/sistema-ventas/issues) en GitHub

---

**Hecho con ❤️ en Perú** 🇵🇪

---

## 📚 Documentación Adicional

### **Para Desarrolladores**
Si quieres modificar o extender el sistema, consulta:
- `config.py`: Colores, fuentes, rutas configurables
- `logica.py`: Lógica de negocio y validaciones
- `reportes.py`: Motor de análisis y generación de reportes

### **Para Usuarios Finales**
- Guía rápida de uso incluida en el menú Ayuda (próximamente)
- Tutoriales en video: [pendiente]

---

**Última actualización:** 29 de noviembre de 2024  
**Versión:** 1.2.0