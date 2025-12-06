"""
Ventanas de Reportes del Sistema de Bazar - VERSIÓN LIMPIA
Solo: Reporte del Día e Inventario Vendido
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from config import *
from reportes import AnalizadorVentas, ExportadorReportes


class VentanaReporteDia:
    """Ventana para consultar ventas de días específicos"""
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("📊 Consultar Ventas Diarias")
        self.ventana.geometry("950x750")
        self.ventana.configure(bg=COLORES['fondo'])
        
        self.analizador = AnalizadorVentas()
        self.datos = None
        self.fecha_seleccionada = datetime.now().strftime('%Y-%m-%d')
        
        self.crear_interfaz()
        self.cargar_datos()
    
    def crear_interfaz(self):
        """Crea la interfaz"""
        # Encabezado con selector de fecha
        frame_header = tk.Frame(self.ventana, bg=COLORES['primario'])
        frame_header.pack(fill=tk.X)
        
        tk.Label(frame_header, text="📊 CONSULTAR VENTAS DIARIAS", 
                font=('Arial', 16, 'bold'), bg=COLORES['primario'], 
                fg='white').pack(pady=10)
        
        # Frame de selección de fecha
        frame_fecha = tk.Frame(frame_header, bg=COLORES['primario'])
        frame_fecha.pack(pady=10)
        
        tk.Label(frame_fecha, text="Seleccionar Fecha:", 
                font=FUENTES['normal'], bg=COLORES['primario'], 
                fg='white').pack(side=tk.LEFT, padx=5)
        
        self.entry_fecha = tk.Entry(frame_fecha, font=FUENTES['normal'], width=12)
        self.entry_fecha.insert(0, self.fecha_seleccionada)
        self.entry_fecha.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_fecha, text="(YYYY-MM-DD)", 
                font=FUENTES['pequeña'], bg=COLORES['primario'], 
                fg='lightgray').pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_fecha, text="Buscar", command=self.cambiar_fecha,
                 bg='white', fg=COLORES['primario'], font=FUENTES['normal'],
                 cursor='hand2', padx=15).pack(side=tk.LEFT, padx=5)
        
        # Botones rápidos
        frame_rapidos = tk.Frame(frame_header, bg=COLORES['primario'])
        frame_rapidos.pack(pady=5)
        
        botones = [
            ("Hoy", 0),
            ("Ayer", -1),
            ("Hace 7 días", -7),
            ("Hace 30 días", -30)
        ]
        
        for texto, dias in botones:
            fecha = (datetime.now() + timedelta(days=dias)).strftime('%Y-%m-%d')
            tk.Button(frame_rapidos, text=texto, 
                     command=lambda f=fecha: self.ir_a_fecha(f),
                     bg='#1976D2', fg='white', font=FUENTES['pequeña'],
                     cursor='hand2', padx=10).pack(side=tk.LEFT, padx=3)
        
        # Label de fecha actual
        self.label_fecha = tk.Label(self.ventana, text="", 
                                   font=FUENTES['titulo'], bg=COLORES['fondo'])
        self.label_fecha.pack(pady=10)
        
        # Tabla de productos
        tk.Label(self.ventana, text="Productos Vendidos:", 
                font=FUENTES['titulo'], bg=COLORES['fondo']).pack(pady=5, anchor='w', padx=20)
        
        frame_tabla = tk.Frame(self.ventana, bg='white')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scroll_y = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
        
        columnas = ('producto', 'cantidad', 'precio_unit', 'subtotal', 'metodos')
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings',
                                yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set,
                                height=12)
        
        self.tree.heading('producto', text='Producto')
        self.tree.heading('cantidad', text='Cantidad Total')
        self.tree.heading('precio_unit', text='Precio Unitario')
        self.tree.heading('subtotal', text='Subtotal')
        self.tree.heading('metodos', text='Métodos de Pago')
        
        self.tree.column('producto', width=250)
        self.tree.column('cantidad', width=100, anchor='center')
        self.tree.column('precio_unit', width=120, anchor='center')
        self.tree.column('subtotal', width=120, anchor='center')
        self.tree.column('metodos', width=200, anchor='center')
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame de resumen
        frame_resumen = tk.Frame(self.ventana, bg='#e8f5e9', relief=tk.RAISED, bd=2)
        frame_resumen.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_resumen, text="💰 RESUMEN DE PAGOS", 
                font=FUENTES['titulo'], bg='#e8f5e9').pack(pady=10)
        
        self.frame_totales = tk.Frame(frame_resumen, bg='#e8f5e9')
        self.frame_totales.pack(pady=10)
        
        self.label_total_general = tk.Label(frame_resumen, text="", 
                                           font=('Arial', 16, 'bold'), 
                                           fg=COLORES['secundario'], bg='#e8f5e9')
        self.label_total_general.pack(pady=15)
        
        # Botones de acción
        frame_botones = tk.Frame(self.ventana, bg=COLORES['fondo'])
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="📄 Exportar CSV", 
                 command=self.exportar_csv,
                 bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(frame_botones, text="🔄 Actualizar", 
                 command=self.cargar_datos,
                 bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(frame_botones, text="Cerrar", 
                 command=self.ventana.destroy,
                 bg=COLORES['borde'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT, padx=10)
    
    def ir_a_fecha(self, fecha):
        """Navega a una fecha específica"""
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, fecha)
        self.cambiar_fecha()
    
    def cambiar_fecha(self):
        """Cambia la fecha seleccionada y recarga datos"""
        fecha = self.entry_fecha.get().strip()
        
        # Validar formato
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", 
                               "Formato de fecha inválido.\n"
                               "Use el formato: YYYY-MM-DD\n"
                               "Ejemplo: 2024-12-06")
            return
        
        self.fecha_seleccionada = fecha
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga los datos de la fecha seleccionada"""
        self.datos = self.analizador.reporte_dia(self.fecha_seleccionada)
        
        if not self.datos:
            # Mostrar mensaje de no hay ventas
            self.label_fecha.config(
                text=f"📅 {self.fecha_seleccionada} - Sin ventas registradas",
                fg=COLORES['error']
            )
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Limpiar totales
            for widget in self.frame_totales.winfo_children():
                widget.destroy()
            
            self.label_total_general.config(text="No hay ventas para esta fecha")
            
            messagebox.showinfo("Sin ventas", 
                              f"No hay ventas registradas para el {self.fecha_seleccionada}")
            return
        
        # Actualizar label de fecha
        try:
            fecha_obj = datetime.strptime(self.fecha_seleccionada, '%Y-%m-%d')
            dia_semana = fecha_obj.strftime('%A')
            fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            self.label_fecha.config(
                text=f"📅 {dia_semana} {fecha_formateada}",
                fg=COLORES['texto']
            )
        except:
            self.label_fecha.config(text=f"📅 {self.fecha_seleccionada}")
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Llenar tabla con productos AGRUPADOS
        for producto in self.datos['productos']:
            self.tree.insert('', tk.END, values=(
                producto['nombre'],
                producto['cantidad'],
                f"S/ {producto['precio_unitario']:.2f}",
                f"S/ {producto['subtotal']:.2f}",
                producto['metodos_pago']
            ))
        
        # Limpiar frame de totales
        for widget in self.frame_totales.winfo_children():
            widget.destroy()
        
        # Mostrar totales por método
        metodos_orden = ['Efectivo', 'Yape', 'Plin', 'Otros']
        for i, metodo in enumerate(metodos_orden):
            total = self.datos['totales_metodos'][metodo]
            porcentaje = self.datos['porcentajes'][metodo]
            
            frame_metodo = tk.Frame(self.frame_totales, bg='#e8f5e9')
            frame_metodo.grid(row=i//2, column=i%2, padx=20, pady=5, sticky='w')
            
            tk.Label(frame_metodo, text=f"{metodo}:", 
                    font=FUENTES['normal'], bg='#e8f5e9', width=10, 
                    anchor='w').pack(side=tk.LEFT)
            tk.Label(frame_metodo, text=f"S/ {total:.2f}", 
                    font=FUENTES['normal'], bg='#e8f5e9', width=12,
                    anchor='e', fg=COLORES['secundario'] if total > 0 else 'gray').pack(side=tk.LEFT)
            tk.Label(frame_metodo, text=f"({porcentaje:.1f}%)", 
                    font=FUENTES['pequeña'], bg='#e8f5e9', 
                    fg='gray').pack(side=tk.LEFT, padx=5)
        
        # Total general
        total_productos = len(self.datos['productos'])
        self.label_total_general.config(
            text=f"━━━━━━━━━━━━━━━━━━━\n"
                 f"TOTAL GENERAL: S/ {self.datos['total_general']:.2f}\n"
                 f"({total_productos} productos diferentes | {self.datos['cantidad_ventas']} transacciones)"
        )
    
    def exportar_csv(self):
        """Exporta el reporte a CSV"""
        if not self.datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre = f'reporte_dia_{self.datos["fecha"]}_{timestamp}.csv'
        
        # Preparar datos para CSV
        datos_csv = []
        
        # Encabezado
        datos_csv.append({
            'Sección': 'REPORTE DEL DÍA',
            'Dato': self.datos['fecha'],
            'Valor': ''
        })
        datos_csv.append({'Sección': '', 'Dato': '', 'Valor': ''})
        
        # Productos vendidos
        datos_csv.append({'Sección': 'PRODUCTOS VENDIDOS', 'Dato': '', 'Valor': ''})
        for producto in self.datos['productos']:
            datos_csv.append({
                'Sección': producto['nombre'],
                'Dato': f"Cantidad: {producto['cantidad']} | Precio Unit: S/ {producto['precio_unitario']:.2f}",
                'Valor': f"S/ {producto['subtotal']:.2f} | {producto['metodos_pago']}"
            })
        
        datos_csv.append({'Sección': '', 'Dato': '', 'Valor': ''})
        
        # Totales por método
        datos_csv.append({'Sección': 'TOTALES POR MÉTODO DE PAGO', 'Dato': '', 'Valor': ''})
        for metodo, total in self.datos['totales_metodos'].items():
            porcentaje = self.datos['porcentajes'][metodo]
            datos_csv.append({
                'Sección': metodo,
                'Dato': f"S/ {total:.2f}",
                'Valor': f"{porcentaje:.1f}%"
            })
        
        datos_csv.append({'Sección': '', 'Dato': '', 'Valor': ''})
        datos_csv.append({
            'Sección': 'TOTAL GENERAL',
            'Dato': f"S/ {self.datos['total_general']:.2f}",
            'Valor': f"{self.datos['cantidad_ventas']} transacciones"
        })
        
        # Exportar
        exito, ruta = ExportadorReportes.exportar_csv(
            datos_csv, nombre, ['Sección', 'Dato', 'Valor']
        )
        
        if exito:
            messagebox.showinfo("✅ Éxito", 
                              f"Reporte exportado exitosamente:\n\n{ruta}")
        else:
            messagebox.showerror("❌ Error", f"No se pudo exportar: {ruta}")


class VentanaInventarioVendido:
    """Ventana para ver inventario vendido con filtros"""
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("📋 Inventario Vendido")
        self.ventana.geometry("1000x700")
        self.ventana.configure(bg=COLORES['fondo'])
        
        self.analizador = AnalizadorVentas()
        self.gestor_productos = None
        
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