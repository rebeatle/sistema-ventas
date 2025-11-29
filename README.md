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
- [Contribución](#-contribución)
- [Roadmap](#-roadmap)
- [Licencia](#-licencia)
- [Contacto](#-contacto)

---

## ✨ Características

### 🛒 **Gestión de Ventas**
- ✅ Registro rápido de ventas con búsqueda inteligente de productos
- ✅ Múltiples métodos de pago (Efectivo, Yape, Plin, Otros)
- ✅ Cálculo automático de totales por método de pago
- ✅ Productos de precio variable (copias, impresiones, etc.)
- ✅ Historial completo de ventas con fecha y hora
- ✅ Interfaz intuitiva con scroll para muchos productos

### 📦 **Control de Inventario**
- ✅ Gestión completa de productos (Agregar, Editar, Eliminar)
- ✅ Control de stock opcional (activable/desactivable)
- ✅ Alertas automáticas de stock bajo
- ✅ Categorización de productos
- ✅ Importación/exportación CSV
- ✅ Actualización automática de stock al vender

### 📊 **Reportes y Análisis**
- ✅ **Inventario Vendido**: Filtrado por fecha, categoría o producto
- ✅ **Top 10 Productos**: Por cantidad vendida y por ingresos
- ✅ **Análisis de Métodos de Pago**: Distribución y porcentajes
- ✅ **Gráficos Visuales**: 
  - Ventas por categoría (gráficos de pastel)
  - Tendencia de ventas diarias (línea)
  - Top productos (barras horizontales)
- ✅ **Exportación de Reportes**: Formato CSV compatible con Excel

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
│ Archivo  Productos  Ventas  Reportes  Configuración            │
├─────────────────────────────────────────────────────────────────┤
│ Producto: [Coca Cola 500ml - S/ 3.50 ▼] Cant:[1] Pago:[EYPO]   │
│                                              [Agregar]  [Otro]   │
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

### Reportes con Gráficos
Los gráficos se generan con matplotlib y muestran análisis visuales de las ventas.

---

## 🔧 Requisitos

### Requisitos del Sistema
- **Sistema Operativo**: Windows 7+, Linux, macOS
- **Python**: 3.8 o superior
- **Espacio en Disco**: ~50 MB
- **RAM**: 256 MB mínimo

### Dependencias de Python
```
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

1. **Primera Ejecución**: El sistema creará automáticamente:
   - `productos.csv` con productos de ejemplo
   - Carpeta `ventas/` para almacenar historial
   - `config_stock.txt` para configuración

2. **Agregar Productos**:
   - Menú → Productos → Agregar Producto
   - Completa: Código, Nombre, Precio, Categoría, Stock (opcional)

3. **Registrar Venta**:
   - Selecciona producto del desplegable
   - Define cantidad
   - Elige método de pago (E/Y/P/O)
   - Click en "Agregar"
   - Al finalizar: Menú → Ventas → Guardar Ventas

4. **Ver Reportes**:
   - Menú → Reportes → Selecciona tipo de reporte
   - Define rango de fechas
   - Click en "Analizar"

### Producto de Precio Variable
Para productos con precio variable (copias, impresiones):
1. Click en botón "Otro"
2. Ingresa descripción, cantidad y precio
3. Selecciona método de pago
4. Click en "Agregar a Venta"

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
├── config_stock.txt       # Configuración de stock
│
├── ventas/               # Carpeta de historial
│   ├── ventas_2024-11-29.csv
│   ├── ventas_2024-11-30.csv
│   └── ...
│
├── requirements.txt      # Dependencias del proyecto
├── README.md            # Este archivo
└── LICENSE              # Licencia del proyecto
```

---

## 🎯 Funcionalidades Detalladas

### 📦 Gestión de Productos

#### Agregar Producto
- Código único
- Nombre descriptivo
- Precio (soles peruanos)
- Categoría
- Stock inicial (si está activado)

#### Editar Producto
- Modificar cualquier campo excepto código
- Actualización en tiempo real

#### Eliminar Producto
- Confirmación antes de eliminar
- No afecta historial de ventas

### 💰 Métodos de Pago

| Código | Método | Descripción |
|--------|--------|-------------|
| **E** | Efectivo | Pago en efectivo |
| **Y** | Yape | Billetera virtual Yape |
| **P** | Plin | Billetera virtual Plin |
| **O** | Otros | Tarjetas, transferencias, etc. |

### 📊 Tipos de Reportes

#### 1. Inventario Vendido
- Filtros: Fecha, Categoría, Producto
- Muestra: Cantidad vendida e ingresos generados
- Exportable a CSV

#### 2. Top Productos
- Top 10 por cantidad vendida
- Top 10 por ingresos
- Gráficos de barras horizontales

#### 3. Análisis de Pagos
- Distribución por método de pago
- Porcentajes y totales
- Gráfico de barras

#### 4. Gráficos
- Ventas por categoría (doble pastel)
- Tendencia de ventas diarias (línea)
- Top productos (barras)

#### 5. Reporte Completo
- Resumen general
- Todos los análisis en un CSV
- Compatible con Excel

---

## ⚙️ Configuración

### Control de Stock

El sistema permite activar/desactivar el control de inventario:

**Activar Stock:**
- Menú → Configuración → Gestión de Stock → Activar
- Descuenta automáticamente al vender
- Alerta cuando stock ≤ 5 unidades
- No permite vender sin stock

**Desactivar Stock:**
- Menú → Configuración → Gestión de Stock → Desactivar
- Permite ventas ilimitadas
- No controla inventario

### Formato de Archivos

#### productos.csv
```csv
codigo,nombre,precio,categoria,stock
001,Coca Cola 500ml,3.50,Bebidas,50
002,Galletas Oreo,4.50,Snacks,30
```

#### ventas/ventas_2024-11-29.csv
```csv
fecha,hora,codigo,nombre,cantidad,precio_unitario,subtotal,metodo_pago,categoria
2024-11-29,14:30:15,001,Coca Cola 500ml,2,3.50,7.00,E,Bebidas
2024-11-29,14:31:20,VAR,Copias A4,10,0.10,1.00,E,Varios
```

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución
- Mantén el código en español (comentarios y variables)
- Sigue el estilo PEP 8
- Documenta nuevas funciones
- Prueba antes de enviar PR

---

## 🗺️ Roadmap

### Versión 1.1 (Próximamente)
- [ ] Impresión de tickets de venta
- [ ] Backup automático de datos
- [ ] Modo oscuro
- [ ] Multi-usuario con permisos

### Versión 1.2 (Planificado)
- [ ] Integración con facturación electrónica (SUNAT)
- [ ] App móvil complementaria
- [ ] Sincronización en la nube
- [ ] Lector de código de barras

### Versión 2.0 (Futuro)
- [ ] Base de datos SQLite
- [ ] Gestión de proveedores
- [ ] Cuentas por cobrar
- [ ] Dashboard web

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 [Tu Nombre]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📞 Contacto

**Desarrollador**: [Tu Nombre]

- 📧 Email: tu-email@ejemplo.com
- 🐙 GitHub: [@tu-usuario](https://github.com/tu-usuario)
- 💼 LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

**Link del Proyecto**: [https://github.com/tu-usuario/sistema-bazar](https://github.com/tu-usuario/sistema-bazar)

---

## 🙏 Agradecimientos

- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Framework GUI
- [Matplotlib](https://matplotlib.org/) - Gráficos y visualizaciones
- Comunidad de desarrolladores Python en Perú
- Todos los que han probado y dado feedback

---

## ⭐ ¿Te gustó el proyecto?

Si este proyecto te fue útil, considera:
- ⭐ Darle una estrella en GitHub
- 🐛 Reportar bugs o sugerir mejoras
- 🤝 Contribuir con código
- 📢 Compartirlo con otros bazares

---

**Hecho con ❤️ en Perú** 🇵🇪