"""
Ventanas de Reportes del Sistema de Bazar
Interfaces gráficas para análisis y reportes
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from config import *
from reportes import AnalizadorVentas, GeneradorGraficos, ExportadorReportes


class VentanaInventarioVendido:
    """Ventana para ver inventario vendido con filtros"""
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Inventario Vendido")
        self.ventana.geometry("1000x700")
        self.ventana.configure(bg=COLORES['fondo'])
        
        self.analizador = AnalizadorVentas()
        self.gestor_productos = None  # Se asignará desde fuera
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de inventario"""
        # Frame de filtros
        frame_filtros = tk.LabelFrame(self.ventana, text="Filtros", 
                                      font=FUENTES['titulo'], bg=COLORES['fondo'])
        frame_filtros.pack(fill=tk.X, padx=10, pady=10)
        
        # Fechas
        frame_fechas = tk.Frame(frame_filtros, bg=COLORES['fondo'])
        frame_fechas.pack(pady=10)
        
        tk.Label(frame_fechas, text="Desde:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=0, column=0, padx=5, pady=5)
        
        # Fecha por defecto: hace 30 días
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=30)
        
        self.entry_fecha_inicio = tk.Entry(frame_fechas, font=FUENTES['normal'], width=12)
        self.entry_fecha_inicio.insert(0, fecha_inicio.strftime('%Y-%m-%d'))
        self.entry_fecha_inicio.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_fechas, text="Hasta:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=0, column=2, padx=5)
        
        self.entry_fecha_fin = tk.Entry(frame_fechas, font=FUENTES['normal'], width=12)
        self.entry_fecha_fin.insert(0, fecha_fin.strftime('%Y-%m-%d'))
        self.entry_fecha_fin.grid(row=0, column=3, padx=5)
        
        tk.Button(self.ventana, text="Generar y Exportar Reporte", 
                 command=self.generar_reporte,
                 bg=COLORES['secundario'], fg='white', font=FUENTES['titulo'],
                 cursor='hand2', padx=30, pady=15).pack(pady=30)
    
    def generar_reporte(self):
        """Genera y exporta el reporte completo"""
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()
        
        if not self.analizador.cargar_ventas_rango(fecha_inicio, fecha_fin):
            messagebox.showwarning("Sin datos", 
                                  "No hay ventas registradas en el rango seleccionado")
            return
        
        exito, ruta = ExportadorReportes.generar_reporte_completo(
            self.analizador, fecha_inicio, fecha_fin
        )
        
        if exito:
            messagebox.showinfo("Éxito", 
                              f"Reporte generado exitosamente:\n\n{ruta}\n\n"
                              f"Puede abrirlo con Excel o cualquier editor de CSV")
        else:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {ruta}")
        self.entry_fecha_inicio = tk.Entry(frame_fechas, font=FUENTES['normal'], width=12)
        self.entry_fecha_inicio.insert(0, fecha_inicio.strftime('%Y-%m-%d'))
        self.entry_fecha_inicio.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_fechas, text="Hasta:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=0, column=2, padx=5, pady=5)
        
        self.entry_fecha_fin = tk.Entry(frame_fechas, font=FUENTES['normal'], width=12)
        self.entry_fecha_fin.insert(0, fecha_fin.strftime('%Y-%m-%d'))
        self.entry_fecha_fin.grid(row=0, column=3, padx=5, pady=5)
        
        # Filtros adicionales
        frame_filtros_extra = tk.Frame(frame_filtros, bg=COLORES['fondo'])
        frame_filtros_extra.pack(pady=5)
        
        tk.Label(frame_filtros_extra, text="Categoría:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=0, column=0, padx=5, pady=5)
        
        self.combo_categoria = ttk.Combobox(frame_filtros_extra, font=FUENTES['normal'], 
                                            width=15, state='readonly')
        self.combo_categoria.set('Todas')
        self.combo_categoria.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_filtros_extra, text="Producto:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=0, column=2, padx=5, pady=5)
        
        self.combo_producto = ttk.Combobox(frame_filtros_extra, font=FUENTES['normal'], 
                                           width=25, state='readonly')
        self.combo_producto.set('Todos')
        self.combo_producto.grid(row=0, column=3, padx=5, pady=5)
        
        # Botones
        frame_botones = tk.Frame(frame_filtros, bg=COLORES['fondo'])
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="Analizar", command=self.analizar,
                 bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones, text="Exportar CSV", command=self.exportar,
                 bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20).pack(side=tk.LEFT, padx=5)
        
        # Tabla de resultados
        frame_tabla = tk.Frame(self.ventana, bg='white')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scroll_y = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
        
        columnas = ('codigo', 'nombre', 'categoria', 'cantidad', 'ingresos')
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings',
                                yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree.heading('codigo', text='Código')
        self.tree.heading('nombre', text='Producto')
        self.tree.heading('categoria', text='Categoría')
        self.tree.heading('cantidad', text='Cantidad Vendida')
        self.tree.heading('ingresos', text='Ingresos Generados')
        
        self.tree.column('codigo', width=80)
        self.tree.column('nombre', width=250)
        self.tree.column('categoria', width=120)
        self.tree.column('cantidad', width=120)
        self.tree.column('ingresos', width=150)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame de resumen
        self.frame_resumen = tk.Frame(self.ventana, bg='#e8f5e9', relief=tk.RAISED, bd=2)
        self.frame_resumen.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_resumen = tk.Label(self.frame_resumen, text="Seleccione rango de fechas y presione Analizar",
                                      font=FUENTES['normal'], bg='#e8f5e9')
        self.label_resumen.pack(pady=10)
    
    def set_gestor_productos(self, gestor):
        """Asigna el gestor de productos para llenar combos"""
        self.gestor_productos = gestor
        if gestor:
            # Llenar combo de categorías
            categorias = ['Todas'] + gestor.obtener_categorias()
            self.combo_categoria['values'] = categorias
            
            # Llenar combo de productos
            productos = ['Todos'] + [f"{p['codigo']} - {p['nombre']}" 
                                    for p in gestor.productos]
            self.combo_producto['values'] = productos
    
    def analizar(self):
        """Realiza el análisis con los filtros seleccionados"""
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()
        
        # Cargar ventas
        if not self.analizador.cargar_ventas_rango(fecha_inicio, fecha_fin):
            messagebox.showwarning("Sin datos", 
                                  "No hay ventas registradas en el rango seleccionado")
            return
        
        # Aplicar filtros
        categoria = self.combo_categoria.get()
        categoria = None if categoria == 'Todas' else categoria
        
        producto_sel = self.combo_producto.get()
        codigo_producto = None
        if producto_sel != 'Todos':
            codigo_producto = producto_sel.split(' - ')[0]
        
        # Obtener inventario
        inventario = self.analizador.inventario_vendido(categoria, codigo_producto)
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Llenar tabla
        total_cantidad = 0
        total_ingresos = 0.0
        
        for item in inventario:
            self.tree.insert('', tk.END, values=(
                item['codigo'],
                item['nombre'],
                item['categoria'],
                item['cantidad_total'],
                f"S/ {item['ingresos_totales']:.2f}"
            ))
            total_cantidad += item['cantidad_total']
            total_ingresos += item['ingresos_totales']
        
        # Actualizar resumen
        self.label_resumen.config(
            text=f"Total: {len(inventario)} productos | "
                 f"Cantidad vendida: {total_cantidad} unidades | "
                 f"Ingresos: S/ {total_ingresos:.2f}"
        )
    
    def exportar(self):
        """Exporta el inventario actual a CSV"""
        items = []
        for item_id in self.tree.get_children():
            valores = self.tree.item(item_id)['values']
            items.append({
                'Código': valores[0],
                'Producto': valores[1],
                'Categoría': valores[2],
                'Cantidad Vendida': valores[3],
                'Ingresos': valores[4]
            })
        
        if not items:
            messagebox.showwarning("Sin datos", "No hay datos para exportar")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre = f'inventario_vendido_{timestamp}.csv'
        
        exito, ruta = ExportadorReportes.exportar_csv(
            items, nombre, ['Código', 'Producto', 'Categoría', 'Cantidad Vendida', 'Ingresos']
        )
        
        if exito:
            messagebox.showinfo("Éxito", f"Reporte exportado en:\n{ruta}")
        else:
            messagebox.showerror("Error", f"No se pudo exportar: {ruta}")


class VentanaTopProductos:
    """Ventana para ver top productos y gráficos"""
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Top Productos")
        self.ventana.geometry("900x700")
        self.ventana.configure(bg=COLORES['fondo'])
        
        self.analizador = AnalizadorVentas()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz"""
        # Filtros de fecha
        frame_filtros = tk.Frame(self.ventana, bg=COLORES['fondo'])
        frame_filtros.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_filtros, text="Desde:", font=FUENTES['normal'],
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=30)
        
        self.entry_fecha_inicio = tk.Entry(frame_filtros, font=FUENTES['normal'], width=12)
        self.entry_fecha_inicio.insert(0, fecha_inicio.strftime('%Y-%m-%d'))
        self.entry_fecha_inicio.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtros, text="Hasta:", font=FUENTES['normal'],
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        self.entry_fecha_fin = tk.Entry(frame_filtros, font=FUENTES['normal'], width=12)
        self.entry_fecha_fin.insert(0, fecha_fin.strftime('%Y-%m-%d'))
        self.entry_fecha_fin.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_filtros, text="Analizar", command=self.analizar,
                 bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20).pack(side=tk.LEFT, padx=10)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña: Top por Cantidad
        self.frame_cantidad = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.frame_cantidad, text='Top por Cantidad')
        self.crear_tabla_top(self.frame_cantidad, por_cantidad=True)
        
        # Pestaña: Top por Ingresos
        self.frame_ingresos = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.frame_ingresos, text='Top por Ingresos')
        self.crear_tabla_top(self.frame_ingresos, por_cantidad=False)
        
        # Botones de gráficos
        frame_botones = tk.Frame(self.ventana, bg=COLORES['fondo'])
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(frame_botones, text="📊 Ver Gráfico Cantidad", 
                 command=lambda: self.mostrar_grafico(True),
                 bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones, text="📊 Ver Gráfico Ingresos", 
                 command=lambda: self.mostrar_grafico(False),
                 bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=15).pack(side=tk.LEFT, padx=5)
    
    def crear_tabla_top(self, parent, por_cantidad):
        """Crea una tabla para top productos"""
        scroll = tk.Scrollbar(parent, orient=tk.VERTICAL)
        
        if por_cantidad:
            columnas = ('posicion', 'codigo', 'nombre', 'categoria', 'cantidad')
            tree = ttk.Treeview(parent, columns=columnas, show='headings',
                              yscrollcommand=scroll.set)
            tree.heading('cantidad', text='Cantidad Vendida')
            tree.column('cantidad', width=120)
            setattr(self, 'tree_cantidad', tree)
        else:
            columnas = ('posicion', 'codigo', 'nombre', 'categoria', 'ingresos')
            tree = ttk.Treeview(parent, columns=columnas, show='headings',
                              yscrollcommand=scroll.set)
            tree.heading('ingresos', text='Ingresos Generados')
            tree.column('ingresos', width=150)
            setattr(self, 'tree_ingresos', tree)
        
        tree.heading('posicion', text='#')
        tree.heading('codigo', text='Código')
        tree.heading('nombre', text='Producto')
        tree.heading('categoria', text='Categoría')
        
        tree.column('posicion', width=50)
        tree.column('codigo', width=80)
        tree.column('nombre', width=250)
        tree.column('categoria', width=120)
        
        scroll.config(command=tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def analizar(self):
        """Analiza y muestra los top productos"""
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()
        
        if not self.analizador.cargar_ventas_rango(fecha_inicio, fecha_fin):
            messagebox.showwarning("Sin datos", 
                                  "No hay ventas registradas en el rango seleccionado")
            return
        
        # Top por cantidad
        top_cantidad = self.analizador.top_productos_cantidad(10)
        self.tree_cantidad.delete(*self.tree_cantidad.get_children())
        for i, item in enumerate(top_cantidad, 1):
            self.tree_cantidad.insert('', tk.END, values=(
                i, item['codigo'], item['nombre'], 
                item['categoria'], item['cantidad']
            ))
        
        # Top por ingresos
        top_ingresos = self.analizador.top_productos_ingresos(10)
        self.tree_ingresos.delete(*self.tree_ingresos.get_children())
        for i, item in enumerate(top_ingresos, 1):
            self.tree_ingresos.insert('', tk.END, values=(
                i, item['codigo'], item['nombre'], 
                item['categoria'], f"S/ {item['ingresos']:.2f}"
            ))
    
    def mostrar_grafico(self, por_cantidad):
        """Muestra gráfico de top productos"""
        if por_cantidad:
            datos = self.analizador.top_productos_cantidad(10)
        else:
            datos = self.analizador.top_productos_ingresos(10)
        
        if not datos:
            messagebox.showwarning("Sin datos", "Primero debe realizar el análisis")
            return
        
        fig = GeneradorGraficos.grafico_top_productos(datos, por_cantidad)
        if fig:
            fig.show()
        else:
            messagebox.showerror("Error", "No se pudo generar el gráfico.\n"
                                         "Asegúrese de tener matplotlib instalado.")


class VentanaAnalisisPagos:
    """Ventana para análisis de métodos de pago"""
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Análisis de Métodos de Pago")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg=COLORES['fondo'])
        
        self.analizador = AnalizadorVentas()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz"""
        # Filtros de fecha
        frame_filtros = tk.Frame(self.ventana, bg=COLORES['fondo'])
        frame_filtros.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_filtros, text="Desde:", font=FUENTES['normal'],
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=30)
        
        self.entry_fecha_inicio = tk.Entry(frame_filtros, font=FUENTES['normal'], width=12)
        self.entry_fecha_inicio.insert(0, fecha_inicio.strftime('%Y-%m-%d'))
        self.entry_fecha_inicio.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtros, text="Hasta:", font=FUENTES['normal'],
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        self.entry_fecha_fin = tk.Entry(frame_filtros, font=FUENTES['normal'], width=12)
        self.entry_fecha_fin.insert(0, fecha_fin.strftime('%Y-%m-%d'))
        self.entry_fecha_fin.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_filtros, text="Analizar", command=self.analizar,
                 bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20).pack(side=tk.LEFT, padx=10)
        
        tk.Button(frame_filtros, text="📊 Ver Gráfico", command=self.mostrar_grafico,
                 bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20).pack(side=tk.LEFT, padx=5)
        
        # Tabla
        frame_tabla = tk.Frame(self.ventana, bg='white')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scroll = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
        
        columnas = ('metodo', 'items', 'total', 'porcentaje')
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings',
                                yscrollcommand=scroll.set)
        
        self.tree.heading('metodo', text='Método de Pago')
        self.tree.heading('items', text='Items Vendidos')
        self.tree.heading('total', text='Total')
        self.tree.heading('porcentaje', text='Porcentaje')
        
        self.tree.column('metodo', width=200)
        self.tree.column('items', width=120)
        self.tree.column('total', width=150)
        self.tree.column('porcentaje', width=100)
        
        scroll.config(command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def analizar(self):
        """Realiza el análisis"""
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()
        
        if not self.analizador.cargar_ventas_rango(fecha_inicio, fecha_fin):
            messagebox.showwarning("Sin datos", 
                                  "No hay ventas registradas en el rango seleccionado")
            return
        
        metodos = self.analizador.analisis_metodos_pago()
        
        self.tree.delete(*self.tree.get_children())
        for m in metodos:
            self.tree.insert('', tk.END, values=(
                m['metodo_nombre'],
                m['cantidad_items'],
                f"S/ {m['total']:.2f}",
                f"{m['porcentaje']:.1f}%"
            ))
    
    def mostrar_grafico(self):
        """Muestra gráfico de métodos de pago"""
        metodos = self.analizador.analisis_metodos_pago()
        if not metodos:
            messagebox.showwarning("Sin datos", "Primero debe realizar el análisis")
            return
        
        fig = GeneradorGraficos.grafico_metodos_pago(metodos)
        if fig:
            fig.show()
        else:
            messagebox.showerror("Error", "No se pudo generar el gráfico")


class VentanaGraficos:
    """Ventana con múltiples gráficos"""
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gráficos de Ventas")
        self.ventana.geometry("500x400")
        self.ventana.configure(bg=COLORES['fondo'])
        
        self.analizador = AnalizadorVentas()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de selección de gráficos"""
        # Filtros
        frame_filtros = tk.Frame(self.ventana, bg=COLORES['fondo'])
        frame_filtros.pack(fill=tk.X, padx=10, pady=20)
        
        tk.Label(frame_filtros, text="Desde:", font=FUENTES['normal'],
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=30)
        
        self.entry_fecha_inicio = tk.Entry(frame_filtros, font=FUENTES['normal'], width=12)
        self.entry_fecha_inicio.insert(0, fecha_inicio.strftime('%Y-%m-%d'))
        self.entry_fecha_inicio.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtros, text="Hasta:", font=FUENTES['normal'],
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        self.entry_fecha_fin = tk.Entry(frame_filtros, font=FUENTES['normal'], width=12)
        self.entry_fecha_fin.insert(0, fecha_fin.strftime('%Y-%m-%d'))
        self.entry_fecha_fin.pack(side=tk.LEFT, padx=5)
        
        # Botones de gráficos
        tk.Label(self.ventana, text="Seleccione el gráfico a visualizar:",
                font=FUENTES['titulo'], bg=COLORES['fondo']).pack(pady=20)
        
        frame_botones = tk.Frame(self.ventana, bg=COLORES['fondo'])
        frame_botones.pack(expand=True)
        
        botones = [
            ("📊 Ventas por Categoría", self.grafico_categorias),
            ("📈 Tendencia de Ventas Diarias", self.grafico_ventas_diarias),
            ("🏆 Top Productos (Cantidad)", lambda: self.grafico_top(True)),
            ("💰 Top Productos (Ingresos)", lambda: self.grafico_top(False)),
        ]
        
        for texto, comando in botones:
            tk.Button(frame_botones, text=texto, command=comando,
                     bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                     cursor='hand2', width=30, pady=10).pack(pady=5)
    
    def cargar_datos(self):
        """Carga los datos del rango seleccionado"""
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()
        
        if not self.analizador.cargar_ventas_rango(fecha_inicio, fecha_fin):
            messagebox.showwarning("Sin datos", 
                                  "No hay ventas registradas en el rango seleccionado")
            return False
        return True
    
    def grafico_categorias(self):
        """Muestra gráfico de categorías"""
        if not self.cargar_datos():
            return
        
        datos = self.analizador.ventas_por_categoria()
        fig = GeneradorGraficos.grafico_categorias(datos)
        if fig:
            fig.show()
        else:
            messagebox.showerror("Error", "No se pudo generar el gráfico")
    
    def grafico_ventas_diarias(self):
        """Muestra gráfico de ventas diarias"""
        if not self.cargar_datos():
            return
        
        datos = self.analizador.ventas_diarias()
        fig = GeneradorGraficos.grafico_ventas_diarias(datos)
        if fig:
            fig.show()
        else:
            messagebox.showerror("Error", "No se pudo generar el gráfico")
    
    def grafico_top(self, por_cantidad):
        """Muestra gráfico de top productos"""
        if not self.cargar_datos():
            return
        
        if por_cantidad:
            datos = self.analizador.top_productos_cantidad(10)
        else:
            datos = self.analizador.top_productos_ingresos(10)
        
        fig = GeneradorGraficos.grafico_top_productos(datos, por_cantidad)
        if fig:
            fig.show()
        else:
            messagebox.showerror("Error", "No se pudo generar el gráfico")


class VentanaExportarReporte:
    """Ventana para exportar reporte completo"""
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Exportar Reporte Completo")
        self.ventana.geometry("500x300")
        self.ventana.configure(bg=COLORES['fondo'])
        
        self.analizador = AnalizadorVentas()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz"""
        tk.Label(self.ventana, text="Generar Reporte Completo",
                font=FUENTES['titulo'], bg=COLORES['fondo']).pack(pady=20)
        
        tk.Label(self.ventana, 
                text="El reporte incluirá:\n\n"
                     "• Resumen general de ventas\n"
                     "• Top 10 productos más vendidos\n"
                     "• Ventas por categoría\n"
                     "• Análisis de métodos de pago\n\n"
                     "Seleccione el rango de fechas:",
                font=FUENTES['normal'], bg=COLORES['fondo'], justify=tk.LEFT).pack(pady=10)
        
        frame_fechas = tk.Frame(self.ventana, bg=COLORES['fondo'])
        frame_fechas.pack(pady=20)
        
        tk.Label(frame_fechas, text="Desde:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=0, column=0, padx=5)
        
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=30)