"""
Configuración del Sistema de Bazar - VERSIÓN LIMPIA
"""
import os
import sys

# ============================================
# CORRECCIÓN PARA EJECUTABLES PyInstaller
# ============================================
def obtener_ruta_base():
    """
    Obtiene la ruta base del programa.
    Funciona tanto para .py como para .exe
    """
    if getattr(sys, 'frozen', False):
        # Corriendo como ejecutable (.exe)
        # sys.executable es la ruta del .exe
        ruta = os.path.dirname(sys.executable)
    else:
        # Corriendo como script (.py)
        ruta = os.path.dirname(os.path.abspath(__file__))
    
    return ruta

# Rutas de archivos
RUTA_BASE = obtener_ruta_base()
RUTA_PRODUCTOS = os.path.join(RUTA_BASE, "productos.csv")
RUTA_VENTAS = os.path.join(RUTA_BASE, "ventas_diarias")  # ✅ CAMBIO: Nueva carpeta
RUTA_CONFIG_STOCK = os.path.join(RUTA_BASE, "config_stock.txt")

# Crear carpeta de ventas si no existe
if not os.path.exists(RUTA_VENTAS):
    os.makedirs(RUTA_VENTAS)

# Métodos de pago
METODOS_PAGO = {
    'E': 'Efectivo',
    'Y': 'Yape',
    'P': 'Plin',
    'O': 'Otros'
}

# Métodos virtuales (para calcular total virtual)
METODOS_VIRTUALES = ['Y', 'P', 'O']

# Colores de la interfaz
COLORES = {
    'fondo': '#f0f0f0',
    'fondo_productos': 'white',
    'texto': '#333333',
    'primario': '#2196F3',
    'secundario': '#4CAF50',
    'error': '#f44336',
    'borde': '#cccccc',
    'advertencia': '#FF9800'
}

# Fuentes
FUENTES = {
    'titulo': ('Arial', 12, 'bold'),
    'normal': ('Arial', 10),
    'pequeña': ('Arial', 9),
    'total': ('Arial', 14, 'bold')
}

# Estructura del CSV de productos (CON STOCK OPCIONAL)
COLUMNAS_PRODUCTOS = ['codigo', 'nombre', 'precio', 'categoria', 'stock']

# Estructura del CSV de ventas
COLUMNAS_VENTAS = ['fecha', 'hora', 'codigo', 'nombre', 'cantidad', 'precio_unitario', 
                   'subtotal', 'metodo_pago', 'categoria']

# Configuración de stock
def cargar_config_stock():
    """Carga la configuración de si el stock está activado"""
    if os.path.exists(RUTA_CONFIG_STOCK):
        try:
            with open(RUTA_CONFIG_STOCK, 'r') as f:
                return f.read().strip() == 'True'
        except:
            return False
    return False

def guardar_config_stock(activado):
    """Guarda la configuración de stock"""
    try:
        with open(RUTA_CONFIG_STOCK, 'w') as f:
            f.write('True' if activado else 'False')
        return True
    except:
        return False

# Variable global para control de stock
STOCK_ACTIVADO = cargar_config_stock()