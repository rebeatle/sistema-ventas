"""
Interfaz Gráfica del Sistema de Bazar - VERSIÓN COMPLETA ACTUALIZADA
Usando tkinter
"""
import tkinter as tk
from config import COLORES, FUENTES, METODOS_PAGO  
from tkinter import ttk, messagebox, simpledialog
from logica import GestorProductos, GestorVentas, validar_numero
from ventana_reportes import (VentanaInventarioVendido, VentanaTopProductos,
                              VentanaAnalisisPagos, VentanaGraficos, 
                              VentanaExportarReporte)
import config


class VentanaPrincipal:
    """Ventana principal del sistema"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Bazar")
        self.root.geometry("900x700")
        self.root.configure(bg=COLORES['fondo'])
        
        # Inicializar gestores
        self.gestor_productos = GestorProductos()
        self.gestor_ventas = GestorVentas()
        
        # Variables
        self.producto_seleccionado = None
        
        # Crear interfaz
        self.crear_menu()
        self.crear_seccion_busqueda()
        self.crear_lista_ventas()
        self.crear_totales()
        
        # Actualizar lista de productos
        self.actualizar_combobox()
    
    def crear_menu(self):
        """Crea el menú superior"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Recargar Productos", command=self.recargar_productos)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        # Menú Productos
        menu_productos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Productos", menu=menu_productos)
        menu_productos.add_command(label="Agregar Producto", command=self.ventana_agregar_producto)
        menu_productos.add_command(label="Editar Producto", command=self.ventana_editar_producto)
        menu_productos.add_command(label="Eliminar Producto", command=self.ventana_eliminar_producto)
        
        # Menú Ventas
        menu_ventas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ventas", menu=menu_ventas)
        menu_ventas.add_command(label="Guardar Ventas", command=self.guardar_ventas)
        menu_ventas.add_command(label="Nueva Venta", command=self.nueva_venta)
        menu_ventas.add_command(label="Ver Historial", command=self.ver_historial)
        
        # Menú Reportes
        menu_reportes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reportes", menu=menu_reportes)
        menu_reportes.add_command(label="Inventario Vendido", command=self.abrir_inventario_vendido)
        menu_reportes.add_command(label="Top Productos", command=self.abrir_top_productos)
        menu_reportes.add_command(label="Análisis de Pagos", command=self.abrir_analisis_pagos)
        menu_reportes.add_command(label="Gráficos", command=self.abrir_graficos)
        menu_reportes.add_separator()
        menu_reportes.add_command(label="Exportar Reporte Completo", command=self.abrir_exportar_reporte)
        
        # Menú Configuración
        menu_config = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Configuración", menu=menu_config)
        menu_config.add_command(label="Gestión de Stock", command=self.configurar_stock)
    
    def crear_seccion_busqueda(self):
        """Crea la sección de búsqueda de productos"""
        frame_busqueda = tk.Frame(self.root, bg=COLORES['fondo'], pady=10)
        frame_busqueda.pack(fill=tk.X, padx=10)
        
        # Label
        tk.Label(frame_busqueda, text="Producto:", font=FUENTES['normal'], 
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        # Combobox con búsqueda
        self.combo_productos = ttk.Combobox(frame_busqueda, width=40, font=FUENTES['normal'])
        self.combo_productos.pack(side=tk.LEFT, padx=5)
        self.combo_productos.bind('<<ComboboxSelected>>', self.seleccionar_producto)
        
        # Cantidad
        tk.Label(frame_busqueda, text="Cant:", font=FUENTES['normal'], 
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        self.spin_cantidad = tk.Spinbox(frame_busqueda, from_=1, to=100, width=5, 
                                       font=FUENTES['normal'])
        self.spin_cantidad.pack(side=tk.LEFT, padx=5)
        
        # Métodos de pago
        tk.Label(frame_busqueda, text="Pago:", font=FUENTES['normal'], 
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=10)
        
        self.metodo_pago = tk.StringVar(value='E')
        frame_metodos = tk.Frame(frame_busqueda, bg=COLORES['fondo'])
        frame_metodos.pack(side=tk.LEFT, padx=5)
        
        for codigo, nombre in METODOS_PAGO.items():
            rb = tk.Radiobutton(frame_metodos, text=codigo, variable=self.metodo_pago, 
                               value=codigo, font=FUENTES['pequeña'], bg=COLORES['fondo'])
            rb.pack(side=tk.LEFT, padx=2)
        
        # Botón Agregar
        btn_agregar = tk.Button(frame_busqueda, text="Agregar", command=self.agregar_producto,
                            bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                            cursor='hand2', padx=15)
        btn_agregar.pack(side=tk.LEFT, padx=5)

        # Botón Otro (producto variable)
        btn_otro = tk.Button(frame_busqueda, text="Otro", command=self.agregar_producto_variable,
                            bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                            cursor='hand2', padx=15)
        btn_otro.pack(side=tk.LEFT, padx=5)
    
    def crear_lista_ventas(self):
        """Crea la lista de productos vendidos con scroll"""
        frame_lista = tk.Frame(self.root, bg=COLORES['fondo'])
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame con scroll
        frame_scroll = tk.Frame(frame_lista, bg='white', relief=tk.SUNKEN, bd=1)
        frame_scroll.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(frame_scroll, bg='white', yscrollcommand=scrollbar.set,
                               highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)
        
        # Frame interno para los productos
        self.frame_productos = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window((0, 0), window=self.frame_productos, anchor='nw')
        
        # Configurar scroll
        self.frame_productos.bind('<Configure>', 
                                 lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        
        # Encabezado
        self.crear_encabezado_lista()
    
    def crear_encabezado_lista(self):
        """Crea el encabezado de la lista de ventas"""
        frame_encabezado = tk.Frame(self.frame_productos, bg='#e0e0e0', relief=tk.RAISED, bd=1)
        frame_encabezado.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(frame_encabezado, text="Producto", font=FUENTES['titulo'], 
                bg='#e0e0e0', width=30, anchor='w').pack(side=tk.LEFT, padx=5, pady=5)
        tk.Label(frame_encabezado, text="Cant", font=FUENTES['titulo'], 
                bg='#e0e0e0', width=5).pack(side=tk.LEFT, padx=5)
        tk.Label(frame_encabezado, text="P. Unit", font=FUENTES['titulo'], 
                bg='#e0e0e0', width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(frame_encabezado, text="Subtotal", font=FUENTES['titulo'], 
                bg='#e0e0e0', width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(frame_encabezado, text="Pago", font=FUENTES['titulo'], 
                bg='#e0e0e0', width=6).pack(side=tk.LEFT, padx=5)
        tk.Label(frame_encabezado, text="", font=FUENTES['titulo'], 
                bg='#e0e0e0', width=8).pack(side=tk.LEFT, padx=5)
    
    def crear_totales(self):
        """Crea la sección de totales"""
        frame_totales = tk.Frame(self.root, bg='#e8f5e9', relief=tk.RAISED, bd=2)
        frame_totales.pack(fill=tk.X, padx=10, pady=10)
        
        # Total General
        frame_general = tk.Frame(frame_totales, bg='#e8f5e9')
        frame_general.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(frame_general, text="TOTAL GENERAL:", font=FUENTES['total'], 
                bg='#e8f5e9').pack(anchor='w')
        self.label_total_general = tk.Label(frame_general, text="S/ 0.00", 
                                           font=FUENTES['total'], fg=COLORES['secundario'],
                                           bg='#e8f5e9')
        self.label_total_general.pack(anchor='w')
        
        # Total Efectivo
        frame_efectivo = tk.Frame(frame_totales, bg='#e8f5e9')
        frame_efectivo.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(frame_efectivo, text="Efectivo:", font=FUENTES['normal'], 
                bg='#e8f5e9').pack(anchor='w')
        self.label_total_efectivo = tk.Label(frame_efectivo, text="S/ 0.00", 
                                            font=FUENTES['normal'], bg='#e8f5e9')
        self.label_total_efectivo.pack(anchor='w')
        
        # Total Virtual
        frame_virtual = tk.Frame(frame_totales, bg='#e8f5e9')
        frame_virtual.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(frame_virtual, text="Virtual (Y/P/O):", font=FUENTES['normal'], 
                bg='#e8f5e9').pack(anchor='w')
        self.label_total_virtual = tk.Label(frame_virtual, text="S/ 0.00", 
                                           font=FUENTES['normal'], bg='#e8f5e9')
        self.label_total_virtual.pack(anchor='w')
    
    def actualizar_combobox(self):
        """Actualiza el combobox con la lista de productos"""
        nombres = self.gestor_productos.obtener_nombres_productos()
        self.combo_productos['values'] = nombres
    
    def seleccionar_producto(self, event):
        """Maneja la selección de un producto del combobox"""
        seleccion = self.combo_productos.get()
        if seleccion:
            # Extraer el nombre del producto (antes del " - S/")
            nombre = seleccion.split(' - S/')[0]
            # Buscar el producto
            for producto in self.gestor_productos.productos:
                if producto['nombre'] == nombre:
                    self.producto_seleccionado = producto
                    break
    
    def agregar_producto(self):
        """Agrega un producto a la lista de ventas"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        cantidad = self.spin_cantidad.get()
        if not validar_numero(cantidad, 'int'):
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return
        
        cantidad = int(cantidad)
        metodo = self.metodo_pago.get()
        
        # Agregar venta
        venta = self.gestor_ventas.agregar_venta(self.producto_seleccionado, cantidad, metodo)
        
        # Si el stock está activado, actualizarlo
        import config
        if config.STOCK_ACTIVADO:
            exito, mensaje_stock = self.gestor_productos.actualizar_stock(
                self.producto_seleccionado['codigo'], cantidad)
            if not exito:
                messagebox.showerror("Error de Stock", mensaje_stock)
                # Eliminar la venta que acabamos de agregar
                self.gestor_ventas.eliminar_venta(len(self.gestor_ventas.ventas_actuales) - 1)
                return
            elif "ADVERTENCIA" in mensaje_stock:
                messagebox.showwarning("Advertencia", mensaje_stock)
        
        # Actualizar interfaz
        self.agregar_item_lista(venta, len(self.gestor_ventas.ventas_actuales) - 1)
        self.actualizar_totales()
        
        # Actualizar combobox para reflejar cambios de stock
        self.actualizar_combobox()
        
        # Limpiar selección
        self.combo_productos.set('')
        self.spin_cantidad.delete(0, tk.END)
        self.spin_cantidad.insert(0, '1')
        self.producto_seleccionado = None
    
    def agregar_item_lista(self, venta, indice):
        """Agrega un item visual a la lista"""
        frame_item = tk.Frame(self.frame_productos, bg='white', relief=tk.GROOVE, bd=1)
        frame_item.pack(fill=tk.X, pady=2)
        
        tk.Label(frame_item, text=venta['nombre'], font=FUENTES['normal'], 
                bg='white', width=30, anchor='w').pack(side=tk.LEFT, padx=5, pady=5)
        tk.Label(frame_item, text=str(venta['cantidad']), font=FUENTES['normal'], 
                bg='white', width=5).pack(side=tk.LEFT, padx=5)
        tk.Label(frame_item, text=f"S/ {venta['precio_unitario']:.2f}", font=FUENTES['normal'], 
                bg='white', width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(frame_item, text=f"S/ {venta['subtotal']:.2f}", font=FUENTES['normal'], 
                bg='white', width=10, fg=COLORES['secundario']).pack(side=tk.LEFT, padx=5)
        tk.Label(frame_item, text=venta['metodo_pago'], font=FUENTES['normal'], 
                bg='white', width=6).pack(side=tk.LEFT, padx=5)
        
        btn_eliminar = tk.Button(frame_item, text="Eliminar", 
                                command=lambda: self.eliminar_item(indice),
                                bg=COLORES['error'], fg='white', font=FUENTES['pequeña'],
                                cursor='hand2')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
    
    def eliminar_item(self, indice):
        """Elimina un item de la lista"""

        # Si el stock está activado, devolver las unidades
        import config
        if config.STOCK_ACTIVADO and indice < len(self.gestor_ventas.ventas_actuales):
            venta = self.gestor_ventas.ventas_actuales[indice]
            # Devolver stock (sumar cantidad)
            for producto in self.gestor_productos.productos:
                if producto['codigo'] == venta['codigo']:
                    producto['stock'] += venta['cantidad']
                    self.gestor_productos.guardar_productos()
                    break
        
        if self.gestor_ventas.eliminar_venta(indice):
            self.actualizar_lista()
            self.actualizar_totales()
            self.actualizar_combobox()
    
    def actualizar_lista(self):
        """Actualiza la lista visual de ventas"""
        # Limpiar frame
        for widget in self.frame_productos.winfo_children():
            widget.destroy()
        
        # Recrear encabezado
        self.crear_encabezado_lista()
        
        # Agregar items
        for i, venta in enumerate(self.gestor_ventas.obtener_ventas()):
            self.agregar_item_lista(venta, i)
    
    def actualizar_totales(self):
        """Actualiza los totales mostrados"""
        totales = self.gestor_ventas.calcular_totales()
        self.label_total_general.config(text=f"S/ {totales['general']:.2f}")
        self.label_total_efectivo.config(text=f"S/ {totales['efectivo']:.2f}")
        self.label_total_virtual.config(text=f"S/ {totales['virtual']:.2f}")
    
    def guardar_ventas(self):
        """Guarda las ventas actuales"""
        if not self.gestor_ventas.ventas_actuales:
            messagebox.showwarning("Advertencia", "No hay ventas para guardar")
            return
        
        exito, mensaje = self.gestor_ventas.guardar_ventas()
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.nueva_venta()
        else:
            messagebox.showerror("Error", mensaje)
    
    def nueva_venta(self):
        """Limpia todo para comenzar una nueva venta"""
        if self.gestor_ventas.ventas_actuales:
            respuesta = messagebox.askyesno("Confirmar", 
                                           "¿Desea iniciar una nueva venta? Se perderán los datos actuales si no los guardó.")
            if not respuesta:
                return
        
        self.gestor_ventas.limpiar_ventas()
        self.actualizar_lista()
        self.actualizar_totales()
    
    def recargar_productos(self):
        """Recarga los productos del CSV"""
        if self.gestor_productos.cargar_productos():
            self.actualizar_combobox()
            messagebox.showinfo("Éxito", "Productos recargados correctamente")
        else:
            messagebox.showerror("Error", "No se pudieron recargar los productos")
    
    def ventana_agregar_producto(self):
        """Abre ventana para agregar un nuevo producto"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Producto")
        ventana.geometry("400x300")
        ventana.configure(bg=COLORES['fondo'])
        
        # Campos
        tk.Label(ventana, text="Código:", font=FUENTES['normal'], 
                bg=COLORES['fondo']).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        entry_codigo = tk.Entry(ventana, font=FUENTES['normal'], width=25)
        entry_codigo.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(ventana, text="Nombre:", font=FUENTES['normal'], 
                bg=COLORES['fondo']).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        entry_nombre = tk.Entry(ventana, font=FUENTES['normal'], width=25)
        entry_nombre.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(ventana, text="Precio:", font=FUENTES['normal'], 
                bg=COLORES['fondo']).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        entry_precio = tk.Entry(ventana, font=FUENTES['normal'], width=25)
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(ventana, text="Categoría:", font=FUENTES['normal'], 
                bg=COLORES['fondo']).grid(row=3, column=0, padx=10, pady=10, sticky='e')
        combo_categoria = ttk.Combobox(ventana, font=FUENTES['normal'], width=23)
        combo_categoria['values'] = self.gestor_productos.obtener_categorias()
        combo_categoria.grid(row=3, column=1, padx=10, pady=10)
        
        # Campo de stock
        tk.Label(ventana, text="Stock Inicial:", font=FUENTES['normal'], 
                bg=COLORES['fondo']).grid(row=4, column=0, padx=10, pady=10, sticky='e')
        entry_stock = tk.Entry(ventana, font=FUENTES['normal'], width=25)
        entry_stock.insert(0, '0')
        entry_stock.grid(row=4, column=1, padx=10, pady=10)
        
        import config
        if not config.STOCK_ACTIVADO:
            entry_stock.config(state='disabled')
            tk.Label(ventana, text="(Stock desactivado)", font=FUENTES['pequeña'],
                    bg=COLORES['fondo'], fg='gray').grid(row=4, column=2, padx=5)
        
        def guardar():
            codigo = entry_codigo.get().strip()
            nombre = entry_nombre.get().strip()
            precio = entry_precio.get().strip()
            categoria = combo_categoria.get().strip()
            
            if not all([codigo, nombre, precio, categoria]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if not validar_numero(precio, 'float'):
                messagebox.showerror("Error", "El precio debe ser un número válido")
                return
            
            stock = entry_stock.get().strip() if config.STOCK_ACTIVADO else 0
            if config.STOCK_ACTIVADO and not validar_numero(stock, 'int'):
                messagebox.showerror("Error", "El stock debe ser un número válido")
                return
            
            exito, mensaje = self.gestor_productos.agregar_producto(codigo, nombre, precio, categoria, stock)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_combobox()
                ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        btn_guardar = tk.Button(ventana, text="Guardar", command=guardar,
                               bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                               cursor='hand2', padx=20)
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)
    
    def ventana_editar_producto(self):
        """Abre ventana para editar un producto existente"""
        # Primero seleccionar el producto
        ventana_seleccion = tk.Toplevel(self.root)
        ventana_seleccion.title("Seleccionar Producto")
        ventana_seleccion.geometry("450x400")
        ventana_seleccion.configure(bg=COLORES['fondo'])
        
        tk.Label(ventana_seleccion, text="Seleccione el producto a editar:", 
                font=FUENTES['titulo'], bg=COLORES['fondo']).pack(pady=10)
        
        # Listbox con productos
        frame_lista = tk.Frame(ventana_seleccion, bg='white')
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame_lista, font=FUENTES['normal'], 
                            yscrollcommand=scrollbar.set, height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Llenar listbox
        for producto in self.gestor_productos.productos:
            listbox.insert(tk.END, f"{producto['codigo']} - {producto['nombre']} - S/ {producto['precio']:.2f}")
        
        def abrir_editor():
            seleccion = listbox.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            
            producto = self.gestor_productos.productos[seleccion[0]]
            ventana_seleccion.destroy()
            
            # Ventana de edición
            ventana = tk.Toplevel(self.root)
            ventana.title("Editar Producto")
            ventana.geometry("400x300")
            ventana.configure(bg=COLORES['fondo'])
            
            # Campos pre-llenados
            tk.Label(ventana, text="Código:", font=FUENTES['normal'], 
                    bg=COLORES['fondo']).grid(row=0, column=0, padx=10, pady=10, sticky='e')
            entry_codigo = tk.Entry(ventana, font=FUENTES['normal'], width=25)
            entry_codigo.insert(0, producto['codigo'])
            entry_codigo.config(state='disabled')  # Código no editable
            entry_codigo.grid(row=0, column=1, padx=10, pady=10)
            
            tk.Label(ventana, text="Nombre:", font=FUENTES['normal'], 
                    bg=COLORES['fondo']).grid(row=1, column=0, padx=10, pady=10, sticky='e')
            entry_nombre = tk.Entry(ventana, font=FUENTES['normal'], width=25)
            entry_nombre.insert(0, producto['nombre'])
            entry_nombre.grid(row=1, column=1, padx=10, pady=10)
            
            tk.Label(ventana, text="Precio:", font=FUENTES['normal'], 
                    bg=COLORES['fondo']).grid(row=2, column=0, padx=10, pady=10, sticky='e')
            entry_precio = tk.Entry(ventana, font=FUENTES['normal'], width=25)
            entry_precio.insert(0, str(producto['precio']))
            entry_precio.grid(row=2, column=1, padx=10, pady=10)
            
            tk.Label(ventana, text="Categoría:", font=FUENTES['normal'], 
                    bg=COLORES['fondo']).grid(row=3, column=0, padx=10, pady=10, sticky='e')
            combo_categoria = ttk.Combobox(ventana, font=FUENTES['normal'], width=23)
            combo_categoria['values'] = self.gestor_productos.obtener_categorias()
            combo_categoria.set(producto['categoria'])
            combo_categoria.grid(row=3, column=1, padx=10, pady=10)
            
            # Campo de stock
            tk.Label(ventana, text="Stock:", font=FUENTES['normal'], 
                    bg=COLORES['fondo']).grid(row=4, column=0, padx=10, pady=10, sticky='e')
            entry_stock = tk.Entry(ventana, font=FUENTES['normal'], width=25)
            entry_stock.insert(0, str(producto.get('stock', 0)))
            entry_stock.grid(row=4, column=1, padx=10, pady=10)
            
            if not config.STOCK_ACTIVADO:
                entry_stock.config(state='disabled')
                tk.Label(ventana, text="(Stock desactivado)", font=FUENTES['pequeña'],
                        bg=COLORES['fondo'], fg='gray').grid(row=4, column=2, padx=5)
            
            def guardar():
                nombre = entry_nombre.get().strip()
                precio = entry_precio.get().strip()
                categoria = combo_categoria.get().strip()
                
                if not all([nombre, precio, categoria]):
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
                    return
                
                if not validar_numero(precio, 'float'):
                    messagebox.showerror("Error", "El precio debe ser un número válido")
                    return
                
                stock = None
                if config.STOCK_ACTIVADO:
                    stock = entry_stock.get().strip()
                    if not validar_numero(stock, 'int'):
                        messagebox.showerror("Error", "El stock debe ser un número válido")
                        return
                    stock = int(stock)
                
                exito, mensaje = self.gestor_productos.editar_producto(
                    producto['codigo'], nombre, precio, categoria, stock)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.actualizar_combobox()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", mensaje)
            
            btn_guardar = tk.Button(ventana, text="Guardar Cambios", command=guardar,
                                   bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                                   cursor='hand2', padx=20)
            btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)
        
        btn_editar = tk.Button(ventana_seleccion, text="Editar Seleccionado", 
                              command=abrir_editor,
                              bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                              cursor='hand2', padx=20)
        btn_editar.pack(pady=10)
    
    def ventana_eliminar_producto(self):
        """Abre ventana para eliminar un producto"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Eliminar Producto")
        ventana.geometry("450x400")
        ventana.configure(bg=COLORES['fondo'])
        
        tk.Label(ventana, text="Seleccione el producto a eliminar:", 
                font=FUENTES['titulo'], bg=COLORES['fondo'], fg=COLORES['error']).pack(pady=10)
        
        # Listbox con productos
        frame_lista = tk.Frame(ventana, bg='white')
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame_lista, font=FUENTES['normal'], 
                            yscrollcommand=scrollbar.set, height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Llenar listbox
        for producto in self.gestor_productos.productos:
            listbox.insert(tk.END, f"{producto['codigo']} - {producto['nombre']} - S/ {producto['precio']:.2f}")
        
        def eliminar():
            seleccion = listbox.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            
            producto = self.gestor_productos.productos[seleccion[0]]
            
            # Confirmación
            respuesta = messagebox.askyesno("Confirmar Eliminación", 
                                           f"¿Está seguro de eliminar el producto?\n\n"
                                           f"Código: {producto['codigo']}\n"
                                           f"Nombre: {producto['nombre']}\n"
                                           f"Precio: S/ {producto['precio']:.2f}\n\n"
                                           f"Esta acción no se puede deshacer.")
            if respuesta:
                if self.gestor_productos.eliminar_producto(producto['codigo']):
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                    self.actualizar_combobox()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el producto")
        
        btn_eliminar = tk.Button(ventana, text="Eliminar Seleccionado", 
                                command=eliminar,
                                bg=COLORES['error'], fg='white', font=FUENTES['normal'],
                                cursor='hand2', padx=20)
        btn_eliminar.pack(pady=10)
    
    def ver_historial(self):
        """Muestra el historial de ventas en una ventana"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Historial de Ventas")
        ventana.geometry("900x600")
        ventana.configure(bg=COLORES['fondo'])
        
        # Frame superior con filtros
        frame_filtros = tk.Frame(ventana, bg=COLORES['fondo'])
        frame_filtros.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_filtros, text="Filtrar por fecha:", font=FUENTES['normal'],
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        from datetime import datetime
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        
        entry_fecha = tk.Entry(frame_filtros, font=FUENTES['normal'], width=15)
        entry_fecha.insert(0, fecha_hoy)
        entry_fecha.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_filtros, text="(YYYY-MM-DD)", font=FUENTES['pequeña'],
                bg=COLORES['fondo'], fg='gray').pack(side=tk.LEFT)
        
        # Frame para la tabla
        frame_tabla = tk.Frame(ventana, bg='white')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        scroll_y = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
        
        # Treeview para mostrar datos
        columnas = ('fecha', 'hora', 'producto', 'cantidad', 'precio', 'subtotal', 
                   'pago', 'categoria')
        tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings',
                           yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Configurar columnas
        tree.heading('fecha', text='Fecha')
        tree.heading('hora', text='Hora')
        tree.heading('producto', text='Producto')
        tree.heading('cantidad', text='Cant.')
        tree.heading('precio', text='P. Unit.')
        tree.heading('subtotal', text='Subtotal')
        tree.heading('pago', text='Pago')
        tree.heading('categoria', text='Categoría')
        
        tree.column('fecha', width=100)
        tree.column('hora', width=80)
        tree.column('producto', width=200)
        tree.column('cantidad', width=60)
        tree.column('precio', width=80)
        tree.column('subtotal', width=90)
        tree.column('pago', width=60)
        tree.column('categoria', width=100)
        
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame para totales
        frame_totales_hist = tk.Frame(ventana, bg='#e3f2fd', relief=tk.RAISED, bd=2)
        frame_totales_hist.pack(fill=tk.X, padx=10, pady=10)
        
        label_total_hist = tk.Label(frame_totales_hist, text="Total: S/ 0.00", 
                                    font=FUENTES['total'], bg='#e3f2fd')
        label_total_hist.pack(pady=10)
        
        def cargar_historial():
            # Limpiar tabla
            for item in tree.get_children():
                tree.delete(item)
            
            fecha = entry_fecha.get().strip()
            historial = self.gestor_ventas.obtener_historial(fecha if fecha else None)
            
            if not historial:
                messagebox.showinfo("Información", "No hay ventas registradas para esta fecha")
                return
            
            total = 0
            for venta in historial:
                subtotal = float(venta.get('subtotal', 0))
                total += subtotal
                tree.insert('', tk.END, values=(
                    venta.get('fecha', ''),
                    venta.get('hora', ''),
                    venta.get('nombre', ''),
                    venta.get('cantidad', ''),
                    f"S/ {float(venta.get('precio_unitario', 0)):.2f}",
                    f"S/ {subtotal:.2f}",
                    venta.get('metodo_pago', ''),
                    venta.get('categoria', '')
                ))
            
            label_total_hist.config(text=f"Total: S/ {total:.2f}")
        
        btn_buscar = tk.Button(frame_filtros, text="Buscar", command=cargar_historial,
                              bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                              cursor='hand2', padx=15)
        btn_buscar.pack(side=tk.LEFT, padx=10)
        
        btn_todo = tk.Button(frame_filtros, text="Ver Todo", 
                            command=lambda: [entry_fecha.delete(0, tk.END), cargar_historial()],
                            bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                            cursor='hand2', padx=15)
        btn_todo.pack(side=tk.LEFT, padx=5)
        
        # Cargar historial inicial
        cargar_historial()
    def agregar_producto_variable(self):
        """Abre ventana para agregar producto de precio variable"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Producto Variable")
        ventana.geometry("400x300")
        ventana.configure(bg=COLORES['fondo'])
        ventana.resizable(False, False)
        
        # Centrar ventana
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Título
        tk.Label(ventana, text="Producto de Precio Variable", 
                font=FUENTES['titulo'], bg=COLORES['fondo']).pack(pady=15)
        
        # Frame para campos
        frame_campos = tk.Frame(ventana, bg=COLORES['fondo'])
        frame_campos.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Descripción
        tk.Label(frame_campos, text="Descripción:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        entry_descripcion = tk.Entry(frame_campos, font=FUENTES['normal'], width=25)
        entry_descripcion.grid(row=0, column=1, padx=10, pady=10)
        entry_descripcion.focus()  # Foco inicial
        
        # Cantidad
        tk.Label(frame_campos, text="Cantidad:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        spin_cantidad_var = tk.Spinbox(frame_campos, from_=1, to=100, width=23,
                                    font=FUENTES['normal'])
        spin_cantidad_var.grid(row=1, column=1, padx=10, pady=10)
        
        # Precio Unitario
        tk.Label(frame_campos, text="Precio Unitario:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        entry_precio = tk.Entry(frame_campos, font=FUENTES['normal'], width=25)
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        
        # Método de pago
        tk.Label(frame_campos, text="Método de Pago:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=3, column=0, padx=10, pady=10, sticky='e')
        
        frame_metodos_var = tk.Frame(frame_campos, bg=COLORES['fondo'])
        frame_metodos_var.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        metodo_pago_var = tk.StringVar(value='E')
        for codigo, nombre in METODOS_PAGO.items():
            rb = tk.Radiobutton(frame_metodos_var, text=f"{codigo} ({nombre})", 
                            variable=metodo_pago_var, value=codigo,
                            font=FUENTES['pequeña'], bg=COLORES['fondo'])
            rb.pack(anchor='w')
        
        # Función para agregar
        def agregar_variable():
            descripcion = entry_descripcion.get().strip()
            cantidad_str = spin_cantidad_var.get()
            precio_str = entry_precio.get().strip()
            metodo = metodo_pago_var.get()
            
            # Validaciones
            if not descripcion:
                messagebox.showerror("Error", "Ingrese una descripción")
                entry_descripcion.focus()
                return
            
            if not validar_numero(cantidad_str, 'int'):
                messagebox.showerror("Error", "La cantidad debe ser un número válido")
                spin_cantidad_var.focus()
                return
            
            if not validar_numero(precio_str, 'float'):
                messagebox.showerror("Error", "El precio debe ser un número válido")
                entry_precio.focus()
                return
            
            cantidad = int(cantidad_str)
            precio = float(precio_str)
            
            # Crear producto temporal (no se guarda en CSV)
            producto_temporal = {
                'codigo': 'VAR',  # Código especial para productos variables
                'nombre': descripcion,
                'precio': precio,
                'categoria': 'Varios'
            }
            
            # Agregar venta
            venta = self.gestor_ventas.agregar_venta(producto_temporal, cantidad, metodo)
            
            # Actualizar interfaz
            self.agregar_item_lista(venta, len(self.gestor_ventas.ventas_actuales) - 1)
            self.actualizar_totales()
            
            # Cerrar ventana
            ventana.destroy()
            
            # Mensaje de confirmación
            messagebox.showinfo("Éxito", f"'{descripcion}' agregado a la venta")
        
        # Botón Agregar
        btn_agregar_var = tk.Button(ventana, text="Agregar a Venta", command=agregar_variable,
                                    bg=COLORES['secundario'], fg='white', 
                                    font=FUENTES['normal'], cursor='hand2',
                                    padx=30, pady=10)
        btn_agregar_var.pack(pady=15)
        
        # Permitir Enter para agregar
        entry_precio.bind('<Return>', lambda e: agregar_variable())
        
        # Botón Cancelar
        btn_cancelar = tk.Button(ventana, text="Cancelar", command=ventana.destroy,
                                bg=COLORES['borde'], fg='white', 
                                font=FUENTES['pequeña'], cursor='hand2',
                                padx=20, pady=5)
        btn_cancelar.pack(pady=5)

    
    # === MÉTODOS DE REPORTES ===
    
    def abrir_inventario_vendido(self):
        """Abre ventana de inventario vendido"""
        ventana = VentanaInventarioVendido(self.root)
        ventana.set_gestor_productos(self.gestor_productos)
    
    def abrir_top_productos(self):
        """Abre ventana de top productos"""
        VentanaTopProductos(self.root)
    
    def abrir_analisis_pagos(self):
        """Abre ventana de análisis de pagos"""
        VentanaAnalisisPagos(self.root)
    
    def abrir_graficos(self):
        """Abre ventana de gráficos"""
        VentanaGraficos(self.root)
    
    def abrir_exportar_reporte(self):
        """Abre ventana para exportar reporte"""
        VentanaExportarReporte(self.root)
    
    def configurar_stock(self):
        """Abre ventana de configuración de stock"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Configuración de Stock")
        ventana.geometry("500x500")
        ventana.configure(bg=COLORES['fondo'])
        
        tk.Label(ventana, text="Gestión de Inventario (Stock)", 
                font=FUENTES['titulo'], bg=COLORES['fondo']).pack(pady=20)
        
        # Estado actual
        estado_actual = "ACTIVADO" if config.STOCK_ACTIVADO else "DESACTIVADO"
        tk.Label(ventana, text=f"Estado actual: {estado_actual}",
                font=FUENTES['normal'], bg=COLORES['fondo'], 
                fg=COLORES['secundario'] if config.STOCK_ACTIVADO else COLORES['error']).pack(pady=10)      
        # Explicación
        texto_info = (
            "Cuando el control de stock está ACTIVADO:\n\n"
            "• Cada producto tendrá una columna de stock en el CSV\n"
            "• Al vender, el stock se reduce automáticamente\n"
            "• Recibirá alertas cuando el stock sea bajo\n"
            "• No podrá vender si no hay stock suficiente\n\n"
            "Cuando está DESACTIVADO:\n\n"
            "• No se controla el inventario\n"
            "• Puede vender sin límites\n"
            "• No hay alertas de stock bajo"
        )
        
        tk.Label(ventana, text=texto_info, font=FUENTES['pequeña'],
                bg=COLORES['fondo'], justify=tk.LEFT).pack(pady=20, padx=20)
        
        # Botones
        frame_botones = tk.Frame(ventana, bg=COLORES['fondo'])
        frame_botones.pack(pady=20)
        
        def activar_stock():
            from config import guardar_config_stock, STOCK_ACTIVADO as stock_actual
            guardar_config_stock(True)
            
            # Actualizar la variable global EN EL MÓDULO config
            import config
            config.STOCK_ACTIVADO = True
            
            # Recargar productos automáticamente
            self.gestor_productos.cargar_productos()
            self.actualizar_combobox()
            
            messagebox.showinfo("Éxito", "Control de stock ACTIVADO\n\n"
                                        "Los productos han sido recargados.\n"
                                        "Los productos tendrán stock inicial en 0 si no lo tenían.")
            ventana.destroy()
        def desactivar_stock():
            from config import guardar_config_stock
            respuesta = messagebox.askyesno("Confirmar", 
                                        "¿Desea DESACTIVAR el control de stock?\n\n"
                                        "Los valores de stock se mantendrán en el CSV\n"
                                        "pero no se controlarán las ventas.")
            if respuesta:
                guardar_config_stock(False)
                
                # Actualizar la variable global EN EL MÓDULO config
                import config
                config.STOCK_ACTIVADO = False
                
                # Recargar productos automáticamente
                self.gestor_productos.cargar_productos()
                self.actualizar_combobox()
                
                messagebox.showinfo("Éxito", "Control de stock DESACTIVADO")
                ventana.destroy()
        def ver_stock_bajo():
            productos_bajo = self.gestor_productos.productos_stock_bajo(10)
            if not productos_bajo:
                messagebox.showinfo("Stock", "No hay productos con stock bajo (≤ 10 unidades)")
                return
            
            mensaje = "Productos con stock bajo (≤ 10 unidades):\n\n"
            for p in productos_bajo:
                mensaje += f"• {p['nombre']}: {p['stock']} unidades\n"
            
            messagebox.showwarning("Advertencia de Stock", mensaje)
        
        tk.Button(frame_botones, text="✅ Activar Stock", command=activar_stock,
                 bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones, text="❌ Desactivar Stock", command=desactivar_stock,
                 bg=COLORES['error'], fg='white', font=FUENTES['normal'],
                 cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        if config.STOCK_ACTIVADO:
            tk.Button(ventana, text="📦 Ver Productos con Stock Bajo", 
                     command=ver_stock_bajo,
                     bg=COLORES['advertencia'], fg='white', font=FUENTES['normal'],
                     cursor='hand2', padx=20, pady=10).pack(pady=10)