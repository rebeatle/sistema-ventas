"""
Módulo de Reportes y Análisis del Sistema de Bazar
Genera estadísticas, análisis y gráficos de ventas
"""
import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from config import *


class AnalizadorVentas:
    """Analiza las ventas y genera reportes"""
    
    def __init__(self):
        self.ventas = []
    
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
    
    def top_productos_cantidad(self, limite=10):
        """Retorna los productos más vendidos por cantidad"""
        contador = Counter()
        info_productos = {}
        
        for venta in self.ventas:
            codigo = venta['codigo']
            contador[codigo] += venta['cantidad']
            info_productos[codigo] = {
                'nombre': venta['nombre'],
                'categoria': venta['categoria']
            }
        
        top = []
        for codigo, cantidad in contador.most_common(limite):
            top.append({
                'codigo': codigo,
                'nombre': info_productos[codigo]['nombre'],
                'categoria': info_productos[codigo]['categoria'],
                'cantidad': cantidad
            })
        
        return top
    
    def top_productos_ingresos(self, limite=10):
        """Retorna los productos que más ingresos generaron"""
        ingresos = defaultdict(float)
        info_productos = {}
        
        for venta in self.ventas:
            codigo = venta['codigo']
            ingresos[codigo] += venta['subtotal']
            info_productos[codigo] = {
                'nombre': venta['nombre'],
                'categoria': venta['categoria']
            }
        
        # Ordenar por ingresos
        top = sorted(ingresos.items(), key=lambda x: x[1], reverse=True)[:limite]
        
        resultado = []
        for codigo, ingreso in top:
            resultado.append({
                'codigo': codigo,
                'nombre': info_productos[codigo]['nombre'],
                'categoria': info_productos[codigo]['categoria'],
                'ingresos': ingreso
            })
        
        return resultado
    
    def analisis_metodos_pago(self):
        """Analiza ventas por método de pago"""
        metodos = defaultdict(lambda: {'cantidad': 0, 'total': 0.0})
        
        for venta in self.ventas:
            metodo = venta['metodo_pago']
            metodos[metodo]['cantidad'] += venta['cantidad']
            metodos[metodo]['total'] += venta['subtotal']
        
        # Calcular totales
        total_general = sum(m['total'] for m in metodos.values())
        
        resultado = []
        for metodo_cod, datos in metodos.items():
            porcentaje = (datos['total'] / total_general * 100) if total_general > 0 else 0
            resultado.append({
                'metodo_codigo': metodo_cod,
                'metodo_nombre': METODOS_PAGO.get(metodo_cod, 'Desconocido'),
                'cantidad_items': datos['cantidad'],
                'total': datos['total'],
                'porcentaje': porcentaje
            })
        
        # Ordenar por total
        resultado.sort(key=lambda x: x['total'], reverse=True)
        return resultado
    
    def ventas_por_categoria(self):
        """Retorna ventas agrupadas por categoría"""
        categorias = defaultdict(lambda: {'cantidad': 0, 'ingresos': 0.0})
        
        for venta in self.ventas:
            cat = venta['categoria']
            categorias[cat]['cantidad'] += venta['cantidad']
            categorias[cat]['ingresos'] += venta['subtotal']
        
        resultado = []
        for categoria, datos in categorias.items():
            resultado.append({
                'categoria': categoria,
                'cantidad': datos['cantidad'],
                'ingresos': datos['ingresos']
            })
        
        # Ordenar por ingresos
        resultado.sort(key=lambda x: x['ingresos'], reverse=True)
        return resultado
    
    def ventas_diarias(self):
        """Retorna ventas totales por día"""
        por_dia = defaultdict(float)
        
        for venta in self.ventas:
            fecha = venta['fecha']
            por_dia[fecha] += venta['subtotal']
        
        # Convertir a lista ordenada por fecha
        resultado = [{'fecha': fecha, 'total': total} 
                    for fecha, total in sorted(por_dia.items())]
        return resultado
    
    def resumen_general(self):
        """Genera un resumen general de las ventas"""
        if not self.ventas:
            return None
        
        total_ventas = sum(v['subtotal'] for v in self.ventas)
        total_items = sum(v['cantidad'] for v in self.ventas)
        productos_unicos = len(set(v['codigo'] for v in self.ventas))
        
        # Fechas
        fechas = [v['fecha'] for v in self.ventas]
        fecha_inicio = min(fechas)
        fecha_fin = max(fechas)
        
        # Producto más vendido
        contador = Counter(v['nombre'] for v in self.ventas)
        producto_top = contador.most_common(1)[0] if contador else ('N/A', 0)
        
        return {
            'total_ventas': total_ventas,
            'total_items': total_items,
            'productos_unicos': productos_unicos,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'producto_mas_vendido': producto_top[0],
            'cantidad_producto_top': producto_top[1],
            'promedio_venta_diaria': total_ventas / len(set(fechas)) if fechas else 0
        }
    def reporte_dia(self):
        """
        Genera reporte del día actual con desglose por producto y método de pago
        Returns: dict con productos, totales por método y total general
        """
        from datetime import datetime
        
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        
        # Cargar solo ventas de hoy
        if not self.cargar_ventas_rango(fecha_hoy, fecha_hoy):
            return None
        
        # Agrupar ventas por producto
        productos_vendidos = []
        for venta in self.ventas:
            productos_vendidos.append({
                'nombre': venta['nombre'],
                'cantidad': venta['cantidad'],
                'precio_unitario': venta['precio_unitario'],
                'subtotal': venta['subtotal'],
                'metodo_pago': METODOS_PAGO.get(venta['metodo_pago'], 'Desconocido'),
                'metodo_codigo': venta['metodo_pago']
            })
        
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
            'fecha': fecha_hoy,
            'productos': productos_vendidos,
            'totales_metodos': totales_metodos,
            'porcentajes': porcentajes,
            'total_general': total_general,
            'cantidad_ventas': len(productos_vendidos)
        }

class GeneradorGraficos:
    """Genera gráficos usando matplotlib"""
    
    @staticmethod
    def preparar_matplotlib():
        """Importa matplotlib con backend apropiado"""
        try:
            import matplotlib
            matplotlib.use('TkAgg')
            import matplotlib.pyplot as plt
            return plt
        except ImportError:
            return None
    
    @staticmethod
    def grafico_top_productos(datos, por_cantidad=True):
        """Genera gráfico de barras de top productos"""
        plt = GeneradorGraficos.preparar_matplotlib()
        if not plt or not datos:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        nombres = [d['nombre'][:20] for d in datos]  # Truncar nombres largos
        valores = [d['cantidad'] if por_cantidad else d['ingresos'] for d in datos]
        
        colores = plt.cm.Set3(range(len(nombres)))
        barras = ax.barh(nombres, valores, color=colores)
        
        # Etiquetas
        titulo = 'Top Productos por Cantidad Vendida' if por_cantidad else 'Top Productos por Ingresos'
        ax.set_xlabel('Cantidad' if por_cantidad else 'Ingresos (S/)')
        ax.set_ylabel('Productos')
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        
        # Agregar valores en las barras
        for i, (barra, valor) in enumerate(zip(barras, valores)):
            width = barra.get_width()
            texto = f'{int(valor)}' if por_cantidad else f'S/ {valor:.2f}'
            ax.text(width, barra.get_y() + barra.get_height()/2, 
                   texto, ha='left', va='center', fontsize=9)
        
        ax.invert_yaxis()  # Invertir para que el mayor esté arriba
        plt.tight_layout()
        return fig
    
    @staticmethod
    def grafico_categorias(datos):
        """Genera gráfico de pastel por categorías"""
        plt = GeneradorGraficos.preparar_matplotlib()
        if not plt or not datos:
            return None
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        categorias = [d['categoria'] for d in datos]
        cantidades = [d['cantidad'] for d in datos]
        ingresos = [d['ingresos'] for d in datos]
        
        # Gráfico por cantidad
        colores = plt.cm.Set3(range(len(categorias)))
        ax1.pie(cantidades, labels=categorias, autopct='%1.1f%%', 
               colors=colores, startangle=90)
        ax1.set_title('Distribución por Cantidad', fontsize=12, fontweight='bold')
        
        # Gráfico por ingresos
        ax2.pie(ingresos, labels=categorias, autopct='%1.1f%%',
               colors=colores, startangle=90)
        ax2.set_title('Distribución por Ingresos', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def grafico_metodos_pago(datos):
        """Genera gráfico de métodos de pago"""
        plt = GeneradorGraficos.preparar_matplotlib()
        if not plt or not datos:
            return None
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        metodos = [d['metodo_nombre'] for d in datos]
        totales = [d['total'] for d in datos]
        
        colores = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'][:len(metodos)]
        barras = ax.bar(metodos, totales, color=colores)
        
        ax.set_ylabel('Total (S/)', fontsize=11)
        ax.set_title('Ventas por Método de Pago', fontsize=14, fontweight='bold')
        
        # Agregar valores sobre las barras
        for barra in barras:
            height = barra.get_height()
            ax.text(barra.get_x() + barra.get_width()/2, height,
                   f'S/ {height:.2f}', ha='center', va='bottom', fontsize=10)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def grafico_ventas_diarias(datos):
        """Genera gráfico de línea de ventas diarias"""
        plt = GeneradorGraficos.preparar_matplotlib()
        if not plt or not datos:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        fechas = [d['fecha'] for d in datos]
        totales = [d['total'] for d in datos]
        
        ax.plot(fechas, totales, marker='o', linewidth=2, 
               markersize=6, color='#2196F3')
        ax.fill_between(range(len(fechas)), totales, alpha=0.3, color='#2196F3')
        
        ax.set_xlabel('Fecha', fontsize=11)
        ax.set_ylabel('Ventas (S/)', fontsize=11)
        ax.set_title('Tendencia de Ventas Diarias', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig


class ExportadorReportes:
    """Exporta reportes a diferentes formatos"""
    
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
    
    @staticmethod
    def generar_reporte_completo(analizador, fecha_inicio, fecha_fin):
        """Genera un reporte completo en CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre = f'reporte_completo_{timestamp}.csv'
        
        # Obtener todos los datos
        inventario = analizador.inventario_vendido()
        top_cantidad = analizador.top_productos_cantidad(10)
        top_ingresos = analizador.top_productos_ingresos(10)
        metodos = analizador.analisis_metodos_pago()
        categorias = analizador.ventas_por_categoria()
        resumen = analizador.resumen_general()
        
        # Crear estructura del reporte
        datos_reporte = []
        
        # Encabezado
        datos_reporte.append({
            'Sección': 'REPORTE DE VENTAS',
            'Dato': f'Del {fecha_inicio} al {fecha_fin}',
            'Valor': ''
        })
        datos_reporte.append({'Sección': '', 'Dato': '', 'Valor': ''})
        
        # Resumen general
        datos_reporte.append({'Sección': 'RESUMEN GENERAL', 'Dato': '', 'Valor': ''})
        datos_reporte.append({'Sección': '', 'Dato': 'Total Ventas', 
                            'Valor': f"S/ {resumen['total_ventas']:.2f}"})
        datos_reporte.append({'Sección': '', 'Dato': 'Total Items Vendidos', 
                            'Valor': resumen['total_items']})
        datos_reporte.append({'Sección': '', 'Dato': 'Productos Únicos', 
                            'Valor': resumen['productos_unicos']})
        datos_reporte.append({'Sección': '', 'Dato': 'Promedio Venta Diaria', 
                            'Valor': f"S/ {resumen['promedio_venta_diaria']:.2f}"})
        datos_reporte.append({'Sección': '', 'Dato': '', 'Valor': ''})
        
        # Top productos
        datos_reporte.append({'Sección': 'TOP 10 PRODUCTOS (Cantidad)', 'Dato': '', 'Valor': ''})
        for i, p in enumerate(top_cantidad, 1):
            datos_reporte.append({'Sección': '', 'Dato': f"{i}. {p['nombre']}", 
                                'Valor': p['cantidad']})
        datos_reporte.append({'Sección': '', 'Dato': '', 'Valor': ''})
        
        # Ventas por categoría
        datos_reporte.append({'Sección': 'VENTAS POR CATEGORÍA', 'Dato': '', 'Valor': ''})
        for cat in categorias:
            datos_reporte.append({'Sección': '', 'Dato': cat['categoria'], 
                                'Valor': f"S/ {cat['ingresos']:.2f}"})
        datos_reporte.append({'Sección': '', 'Dato': '', 'Valor': ''})
        
        # Métodos de pago
        datos_reporte.append({'Sección': 'MÉTODOS DE PAGO', 'Dato': '', 'Valor': ''})
        for m in metodos:
            datos_reporte.append({'Sección': '', 'Dato': m['metodo_nombre'], 
                                'Valor': f"S/ {m['total']:.2f} ({m['porcentaje']:.1f}%)"})
        
        return ExportadorReportes.exportar_csv(
            datos_reporte, nombre, ['Sección', 'Dato', 'Valor']
        )