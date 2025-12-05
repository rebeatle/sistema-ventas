"""
Lógica de Negocio del Sistema de Bazar - ACTUALIZADO CON STOCK
Manejo de CSV, validaciones y cálculos
"""
import csv
import os
from datetime import datetime
from config import *
import json

class GestorProductos:
    """Maneja la carga, guardado y manipulación de productos"""
    
    def __init__(self):
        self.productos = []
        self.cargar_productos()
    
    def cargar_productos(self):
        """Carga los productos desde el CSV"""
        if not os.path.exists(RUTA_PRODUCTOS):
            self.crear_csv_ejemplo()
        
        try:
            with open(RUTA_PRODUCTOS, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                self.productos = list(lector)
                # Convertir precios y stock a numéricos
                for producto in self.productos:
                    producto['precio'] = float(producto['precio'])
                    # Si no existe la columna stock, agregarla con valor 0
                    if 'stock' not in producto:
                        producto['stock'] = 0
                    else:
                        try:
                            producto['stock'] = int(producto['stock'])
                        except:
                            producto['stock'] = 0
            return True
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            return False
    
    def crear_csv_ejemplo(self):
        """Crea un CSV de ejemplo con productos iniciales"""
        productos_ejemplo = [
            {'codigo': '001', 'nombre': 'Coca Cola 500ml', 'precio': '3.50', 'categoria': 'Bebidas', 'stock': '50'},
            {'codigo': '002', 'nombre': 'Inca Kola 500ml', 'precio': '3.50', 'categoria': 'Bebidas', 'stock': '40'},
            {'codigo': '003', 'nombre': 'Agua San Luis 625ml', 'precio': '2.00', 'categoria': 'Bebidas', 'stock': '60'},
            {'codigo': '004', 'nombre': 'Galletas Oreo', 'precio': '4.50', 'categoria': 'Snacks', 'stock': '30'},
            {'codigo': '005', 'nombre': 'Papas Lays', 'precio': '5.00', 'categoria': 'Snacks', 'stock': '25'},
            {'codigo': '006', 'nombre': 'Chocolate Sublime', 'precio': '2.50', 'categoria': 'Dulces', 'stock': '45'},
            {'codigo': '007', 'nombre': 'Chicles Trident', 'precio': '1.50', 'categoria': 'Dulces', 'stock': '100'},
            {'codigo': '008', 'nombre': 'Pan Integral', 'precio': '6.00', 'categoria': 'Panadería', 'stock': '15'},
        ]
        
        with open(RUTA_PRODUCTOS, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_PRODUCTOS)
            escritor.writeheader()
            escritor.writerows(productos_ejemplo)
    
    def guardar_productos(self):
        """Guarda los productos en el CSV"""
        try:
            with open(RUTA_PRODUCTOS, 'w', newline='', encoding='utf-8') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_PRODUCTOS)
                escritor.writeheader()
                escritor.writerows(self.productos)
            return True
        except Exception as e:
            print(f"Error al guardar productos: {e}")
            return False
    
    def agregar_producto(self, codigo, nombre, precio, categoria, stock=0):
        """Agrega un nuevo producto"""
        # Verificar si el código ya existe
        if any(p['codigo'] == codigo for p in self.productos):
            return False, "El código ya existe"
        
        nuevo_producto = {
            'codigo': codigo,
            'nombre': nombre,
            'precio': float(precio),
            'categoria': categoria,
            'stock': int(stock)
        }
        self.productos.append(nuevo_producto)
        return self.guardar_productos(), "Producto agregado exitosamente"
    
    def editar_producto(self, codigo, nombre, precio, categoria, stock=None):
        """Edita un producto existente"""
        for producto in self.productos:
            if producto['codigo'] == codigo:
                producto['nombre'] = nombre
                producto['precio'] = float(precio)
                producto['categoria'] = categoria
                if stock is not None:
                    producto['stock'] = int(stock)
                return self.guardar_productos(), "Producto editado exitosamente"
        return False, "Producto no encontrado"
    
    def eliminar_producto(self, codigo):
        """Elimina un producto"""
        self.productos = [p for p in self.productos if p['codigo'] != codigo]
        return self.guardar_productos()
    
    def buscar_producto(self, codigo):
        """Busca un producto por código"""
        for producto in self.productos:
            if producto['codigo'] == codigo:
                return producto
        return None
    
    def obtener_nombres_productos(self):
        """Retorna lista de nombres con precio para el combobox"""
        resultado = []
        for p in self.productos:
            texto = f"{p['nombre']} - S/ {p['precio']:.2f}"
            # Si el stock está activado y es bajo, agregar advertencia
            if STOCK_ACTIVADO:
                texto += f" [STOCK: {p['stock']}]"
            resultado.append(texto)
        return resultado
    
    def obtener_categorias(self):
        """Retorna lista de categorías únicas"""
        categorias = set(p['categoria'] for p in self.productos)
        return sorted(list(categorias))
    
    def actualizar_stock(self, codigo, cantidad_vendida):
        """Actualiza el stock de un producto después de una venta"""
        if not STOCK_ACTIVADO:
            return True, "Stock desactivado"
        
        for producto in self.productos:
            if producto['codigo'] == codigo:
                nuevo_stock = producto['stock'] - cantidad_vendida
                if nuevo_stock < 0:
                    return False, f"Stock insuficiente. Disponible: {producto['stock']}"
                producto['stock'] = nuevo_stock
                self.guardar_productos()
                
                # Advertencia si el stock es bajo
                if nuevo_stock <= 5:
                    return True, f"ADVERTENCIA: Stock bajo para '{producto['nombre']}': {nuevo_stock} unidades"
                return True, "Stock actualizado"
        return False, "Producto no encontrado"
    
    def productos_stock_bajo(self, umbral=10):
        """Retorna productos con stock bajo"""
        if not STOCK_ACTIVADO:
            return []
        
        return [p for p in self.productos if p['stock'] <= umbral]


class GestorVentas:
    """Maneja el registro de ventas y cálculos"""
    
    def __init__(self):
        self.ventas_actuales = []
        self.ventas_guardadas_hoy = []  # ✅ NUEVO: rastrea ventas ya guardadas
        self.ruta_temporal = os.path.join(RUTA_BASE, 'ventas_temp.json')
    
    def agregar_venta(self, producto, cantidad, metodo_pago):
        """Agrega una venta a la lista actual"""
        venta = {
            'codigo': producto['codigo'],
            'nombre': producto['nombre'],
            'cantidad': cantidad,
            'precio_unitario': producto['precio'],
            'subtotal': producto['precio'] * cantidad,
            'metodo_pago': metodo_pago,
            'categoria': producto['categoria']
        }
        self.ventas_actuales.append(venta)
        return venta
    
    def eliminar_venta(self, indice):
        """Elimina una venta de la lista actual"""
        if 0 <= indice < len(self.ventas_actuales):
            self.ventas_actuales.pop(indice)
            return True
        return False
    
    def calcular_totales(self):
        """Calcula los totales de las ventas actuales"""
        total_general = sum(v['subtotal'] for v in self.ventas_actuales)
        total_efectivo = sum(v['subtotal'] for v in self.ventas_actuales if v['metodo_pago'] == 'E')
        total_virtual = sum(v['subtotal'] for v in self.ventas_actuales 
                           if v['metodo_pago'] in METODOS_VIRTUALES)
        
        return {
            'general': total_general,
            'efectivo': total_efectivo,
            'virtual': total_virtual
        }
    def guardar_temporal(self):
        """Guarda las ventas actuales en archivo temporal (BACKUP AUTOMÁTICO)"""
        try:
            datos_temp = {
                'fecha': datetime.now().strftime('%Y-%m-%d'),
                'hora_ultimo_guardado': datetime.now().strftime('%H:%M:%S'),
                'ventas': self.ventas_actuales
            }
            with open(self.ruta_temporal, 'w', encoding='utf-8') as f:
                json.dump(datos_temp, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar temporal: {e}")
            return False
    
    def cargar_temporal(self):
        """Carga las ventas temporales si existen y son del día actual"""
        if not os.path.exists(self.ruta_temporal):
            return False, "No hay sesión anterior"
        
        try:
            with open(self.ruta_temporal, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            fecha_temp = datos.get('fecha', '')
            fecha_hoy = datetime.now().strftime('%Y-%m-%d')
            
            if fecha_temp != fecha_hoy:
                return False, "La sesión anterior es de otro día"
            
            self.ventas_actuales = datos.get('ventas', [])
            return True, f"Sesión recuperada ({len(self.ventas_actuales)} productos)"
        except Exception as e:
            return False, f"Error al cargar sesión: {e}"
    
    def limpiar_temporal(self):
        """Elimina el archivo temporal"""
        try:
            if os.path.exists(self.ruta_temporal):
                os.remove(self.ruta_temporal)
            return True
        except:
            return False
    def guardar_ventas(self):
        """Guarda las ventas actuales EN EL ARCHIVO DEFINITIVO"""
        if not self.ventas_actuales:
            return False, "No hay ventas para guardar"
        
        fecha_actual = datetime.now()
        fecha_str = fecha_actual.strftime('%Y-%m-%d')
        hora_str = fecha_actual.strftime('%H:%M:%S')
        
        nombre_archivo = os.path.join(RUTA_VENTAS, f'ventas_{fecha_str}.csv')
        archivo_existe = os.path.exists(nombre_archivo)
        
        try:
            with open(nombre_archivo, 'a', newline='', encoding='utf-8') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_VENTAS)
                
                if not archivo_existe:
                    escritor.writeheader()
                
                # Agregar fecha y hora a cada venta
                for venta in self.ventas_actuales:
                    venta['fecha'] = fecha_str
                    venta['hora'] = hora_str
                    escritor.writerow(venta)
            
            # ✅ NUEVO: Limpiar lista automáticamente después de guardar
            self.ventas_guardadas_hoy.extend(self.ventas_actuales)
            self.ventas_actuales = []
            self.limpiar_temporal()
            
            return True, f"✅ Ventas guardadas exitosamente\n\nArchivo: {nombre_archivo}\n\nLa lista de ventas ha sido limpiada."
        except Exception as e:
            return False, f"Error al guardar ventas: {e}"
    
    def limpiar_ventas(self):
        """Limpia la lista de ventas actuales"""
        self.ventas_actuales = []
    
    def obtener_ventas(self):
        """Retorna la lista de ventas actuales"""
        return self.ventas_actuales
    
    def obtener_historial(self, fecha=None):
        """Lee el historial de ventas de una fecha específica o todas"""
        import os
        historial = []
        
        if fecha:
            # Leer archivo específico
            nombre_archivo = os.path.join(RUTA_VENTAS, f'ventas_{fecha}.csv')
            if os.path.exists(nombre_archivo):
                try:
                    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                        lector = csv.DictReader(archivo)
                        historial = list(lector)
                except Exception as e:
                    print(f"Error al leer historial: {e}")
        else:
            # Leer todos los archivos de ventas
            if os.path.exists(RUTA_VENTAS):
                for archivo in sorted(os.listdir(RUTA_VENTAS)):
                    if archivo.startswith('ventas_') and archivo.endswith('.csv'):
                        ruta_completa = os.path.join(RUTA_VENTAS, archivo)
                        try:
                            with open(ruta_completa, 'r', encoding='utf-8') as f:
                                lector = csv.DictReader(f)
                                historial.extend(list(lector))
                        except Exception as e:
                            print(f"Error al leer {archivo}: {e}")
        
        return historial


def validar_numero(valor, tipo='int'):
    """Valida que un valor sea numérico"""
    try:
        if tipo == 'int':
            return int(valor) > 0
        elif tipo == 'float':
            return float(valor) > 0
    except ValueError:
        return False
    return False