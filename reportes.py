"""
Módulo de Reportes del Sistema de Bazar - VERSIÓN LIMPIA
Solo funcionalidades esenciales: Reporte del Día e Inventario Vendido
"""
import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict
from config import *


class AnalizadorVentas:
    """Analiza las ventas y genera reportes"""
    
    def __init__(self):
        self.ventas = []
    
    def cargar_ventas_fecha(self, fecha):
        """Carga ventas de una fecha específica (YYYY-MM-DD)"""
        self.ventas = []
        
        nombre_archivo = os.path.join(RUTA_VENTAS, f'ventas_{fecha}.csv')
        
        if not os.path.exists(nombre_archivo):
            return False
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                lector = csv.DictReader(f)
                for venta in lector:
                    # Convertir valores numéricos
                    venta['cantidad'] = int(venta['cantidad'])
                    venta['precio_unitario'] = float(venta['precio_unitario'])
                    venta['subtotal'] = float(venta['subtotal'])
                    self.ventas.append(venta)
        except Exception as e:
            print(f"Error al leer archivo: {e}")
            return False
        
        return len(self.ventas) > 0
    
    def cargar_ventas_rango(self, fecha_inicio, fecha_fin):
        """Carga todas las ventas dentro de un rango de fechas"""
        self.ventas = []
        
        if not os.path.exists(RUTA_VENTAS):
            return False
        
        # Convertir strings a datetime
        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            return False
        
        # Recorrer cada día en el rango
        fecha_actual = inicio
        while fecha_actual <= fin:
            fecha_str = fecha_actual.strftime('%Y-%m-%d')
            archivo = os.path.join(RUTA_VENTAS, f'ventas_{fecha_str}.csv')
            
            if os.path.exists(archivo):
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        lector = csv.DictReader(f)
                        for venta in lector:
                            # Convertir valores numéricos
                            venta['cantidad'] = int(venta['cantidad'])
                            venta['precio_unitario'] = float(venta['precio_unitario'])
                            venta['subtotal'] = float(venta['subtotal'])
                            self.ventas.append(venta)
                except Exception as e:
                    print(f"Error al leer {archivo}: {e}")
            
            fecha_actual += timedelta(days=1)
        
        return len(self.ventas) > 0
    
    def inventario_vendido(self, categoria=None, codigo_producto=None):
        """
        Retorna inventario vendido con opciones de filtrado
        Returns: dict con productos y sus cantidades vendidas
        """
        inventario = defaultdict(lambda: {
            'nombre': '',
            'categoria': '',
            'cantidad_total': 0,
            'ingresos_totales': 0.0,
            'codigo': ''
        })
        
        for venta in self.ventas:
            codigo = venta['codigo']
            
            # Aplicar filtros
            if categoria and venta['categoria'] != categoria:
                continue
            if codigo_producto and codigo != codigo_producto:
                continue
            
            inventario[codigo]['nombre'] = venta['nombre']
            inventario[codigo]['categoria'] = venta['categoria']
            inventario[codigo]['codigo'] = codigo
            inventario[codigo]['cantidad_total'] += venta['cantidad']
            inventario[codigo]['ingresos_totales'] += venta['subtotal']
        
        # Convertir a lista ordenada por cantidad
        resultado = sorted(inventario.values(), 
                          key=lambda x: x['cantidad_total'], 
                          reverse=True)
        return resultado
    
    def reporte_dia(self, fecha=None):
        """
        Genera reporte de un día específico con desglose por producto y método de pago
        Si fecha es None, usa el día actual
        Returns: dict con productos AGRUPADOS, totales por método y total general
        """
        if fecha is None:
            fecha = datetime.now().strftime('%Y-%m-%d')
        
        # Cargar solo ventas de la fecha especificada
        if not self.cargar_ventas_fecha(fecha):
            return None
        
        # Agrupar ventas por producto y método de pago
        productos_agrupados = defaultdict(lambda: {
            'cantidad_total': 0,
            'precio_unitario': 0.0,
            'subtotal_total': 0.0,
            'desglose_metodos': defaultdict(lambda: {'cantidad': 0, 'subtotal': 0.0})
        })
        
        for venta in self.ventas:
            codigo = venta['codigo']
            nombre = venta['nombre']
            metodo = venta['metodo_pago']
            key = f"{codigo}|{nombre}"  # Clave única por producto
            
            # Acumular totales por producto
            productos_agrupados[key]['cantidad_total'] += venta['cantidad']
            productos_agrupados[key]['precio_unitario'] = venta['precio_unitario']
            productos_agrupados[key]['subtotal_total'] += venta['subtotal']
            
            # Acumular por método de pago
            productos_agrupados[key]['desglose_metodos'][metodo]['cantidad'] += venta['cantidad']
            productos_agrupados[key]['desglose_metodos'][metodo]['subtotal'] += venta['subtotal']
        
        # Convertir a lista para la interfaz
        productos_vendidos = []
        for key, datos in productos_agrupados.items():
            codigo, nombre = key.split('|', 1)
            
            # Crear string de métodos de pago
            metodos_str = []
            for metodo_cod, metodo_datos in datos['desglose_metodos'].items():
                metodo_nombre = METODOS_PAGO.get(metodo_cod, 'Desconocido')
                metodos_str.append(f"{metodo_nombre} ({metodo_datos['cantidad']})")
            
            productos_vendidos.append({
                'codigo': codigo,
                'nombre': nombre,
                'cantidad': datos['cantidad_total'],
                'precio_unitario': datos['precio_unitario'],
                'subtotal': datos['subtotal_total'],
                'metodos_pago': ', '.join(metodos_str)
            })
        
        # Ordenar por nombre
        productos_vendidos.sort(key=lambda x: x['nombre'])
        
        # Calcular totales por método de pago
        totales_metodos = {
            'Efectivo': 0.0,
            'Yape': 0.0,
            'Plin': 0.0,
            'Otros': 0.0
        }
        
        for venta in self.ventas:
            metodo_nombre = METODOS_PAGO.get(venta['metodo_pago'], 'Otros')
            totales_metodos[metodo_nombre] += venta['subtotal']
        
        # Total general
        total_general = sum(totales_metodos.values())
        
        # Calcular porcentajes
        porcentajes = {}
        for metodo, total in totales_metodos.items():
            porcentaje = (total / total_general * 100) if total_general > 0 else 0
            porcentajes[metodo] = porcentaje
        
        return {
            'fecha': fecha,
            'productos': productos_vendidos,
            'totales_metodos': totales_metodos,
            'porcentajes': porcentajes,
            'total_general': total_general,
            'cantidad_ventas': len(self.ventas)
        }


class ExportadorReportes:
    """Exporta reportes a CSV"""
    
    @staticmethod
    def exportar_csv(datos, nombre_archivo, columnas):
        """Exporta datos a CSV"""
        try:
            ruta = os.path.join(RUTA_BASE, nombre_archivo)
            with open(ruta, 'w', newline='', encoding='utf-8') as f:
                if datos:
                    escritor = csv.DictWriter(f, fieldnames=columnas)
                    escritor.writeheader()
                    escritor.writerows(datos)
            return True, ruta
        except Exception as e:
            return False, str(e)