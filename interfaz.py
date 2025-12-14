"""
Interfaz Gráfica del Sistema de Bazar - VERSIÓN LIMPIA
Usando tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from logica import GestorProductos, GestorVentas, validar_numero
from ventana_reportes import VentanaInventarioVendido, VentanaReporteDia
import config
from config import COLORES, FUENTES, METODOS_PAGO

class VentanaPrincipal:
    """Ventana principal del sistema"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Bazar")
        self.root.geometry("850x600")  # Compacto inicial
        self.root.minsize(800, 550)    # Mínimo funcional
        self.root.resizable(True, True) # Redimensionable
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
        
        # Actualizar
        self.actualizar_productos_dict()
        # Recuperar ventas temporales si existen
        self.recuperar_ventas_temporales()
        # Manejar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.al_cerrar)

    def recuperar_ventas_temporales(self):
        """Recupera ventas de sesión anterior si existen"""
        exito, datos = self.gestor_ventas.cargar_temporal()
        
        if exito and datos:
            # Actualizar interfaz con las ventas recuperadas
            self.actualizar_lista()
            self.actualizar_totales()
            
            # Mensaje informativo discreto
            timestamp = datos.get('timestamp', 'desconocida')
            total = datos.get('total', 0)
            cantidad = datos.get('cantidad_productos', 0)
            
            mensaje = (
                f"✅ Ventas Recuperadas\n\n"
                f"Se recuperaron {cantidad} producto(s) de la sesión anterior\n"
                f"Fecha: {timestamp}\n"
                f"Total: S/ {total:.2f}\n\n"
                f"Puede continuar agregando ventas o cerrar caja."
            )
            
            messagebox.showinfo("Recuperación Automática", mensaje)


    def al_cerrar(self):
        """Maneja el cierre de la ventana"""
        if self.gestor_ventas.ventas_actuales:
            respuesta = messagebox.askyesnocancel(
                "Cerrar Sistema",
                "Hay ventas sin guardar.\n\n"
                "• SÍ: Cerrar caja y salir\n"
                "• NO: Salir sin guardar\n"
                "• CANCELAR: No cerrar",
                icon='warning'
            )
            
            if respuesta is None:  # Cancelar
                return
            elif respuesta:  # Sí - Cerrar caja
                exito, resultado = self.gestor_ventas.guardar_ventas()
                if exito:
                    self.mostrar_resumen_cierre(resultado)
                    self.root.destroy()
                else:
                    messagebox.showerror("Error", resultado)
                    return
            else:  # No - Solo cerrar
                # ✅ MODIFICADO: Limpiar temporal al salir sin guardar
                self.gestor_ventas.limpiar_temporal()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def mostrar_resumen_cierre(self, resultado):
        """Muestra resumen al cerrar caja"""
        mensaje = (
            f"✅ Caja Cerrada - Resumen:\n\n"
            f"• Total del día: S/ {resultado['total']:.2f}\n"
            f"• Efectivo: S/ {resultado['efectivo']:.2f}\n"
            f"• Virtual: S/ {resultado['virtual']:.2f}\n"
            f"• Productos vendidos: {resultado['productos']}\n\n"
            f"Archivo guardado en:\n{resultado['archivo']}"
        )
        messagebox.showinfo("Caja Cerrada", mensaje)
    
    def crear_menu(self):
        """Crea el menú superior"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Recargar Productos", command=self.recargar_productos)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.al_cerrar)
        
        # Menú Productos
        menu_productos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Productos", menu=menu_productos)
        menu_productos.add_command(label="Agregar Producto", command=self.ventana_agregar_producto)
        menu_productos.add_command(label="Editar Producto", command=self.ventana_editar_producto)
        menu_productos.add_command(label="Eliminar Producto", command=self.ventana_eliminar_producto)
        
        # Menú Reportes (SIMPLIFICADO)
        menu_reportes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reportes", menu=menu_reportes)
        menu_reportes.add_command(label="📦 Cerrar Caja del Día", command=self.cerrar_caja)
        menu_reportes.add_command(label="📊 Consultar Ventas Diarias", command=self.abrir_reporte_dia)
        menu_reportes.add_separator()
        menu_reportes.add_command(label="📋 Inventario Vendido", command=self.abrir_inventario_vendido)
        menu_reportes.add_separator()
        menu_reportes.add_command(label="🗑️ Limpiar Caja (Emergencia)", command=self.limpiar_caja_emergencia)
        
        # Menú Configuración
        menu_config = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Configuración", menu=menu_config)
        menu_config.add_command(label="Gestión de Stock", command=self.configurar_stock)
    
    def crear_seccion_busqueda(self):
        """Crea la sección de búsqueda de productos CON AUTOCOMPLETADO"""
        frame_busqueda = tk.Frame(self.root, bg=COLORES['fondo'], pady=10)
        frame_busqueda.pack(fill=tk.X, padx=10)
        
        # Label
        tk.Label(frame_busqueda, text="Producto:", font=FUENTES['normal'], 
                bg=COLORES['fondo']).pack(side=tk.LEFT, padx=5)
        
        # Frame para Entry + Listbox
        self.frame_autocompletado = tk.Frame(frame_busqueda, bg=COLORES['fondo'])
        self.frame_autocompletado.pack(side=tk.LEFT, padx=5)
        
        # Entry para búsqueda
        self.entry_busqueda = tk.Entry(self.frame_autocompletado, font=FUENTES['normal'], width=40)
        self.entry_busqueda.pack()
        self.entry_busqueda.bind('<KeyRelease>', self.filtrar_productos)
        self.entry_busqueda.bind('<Down>', self.mover_seleccion_abajo)
        
        # Listbox flotante (inicialmente oculto)
        self.listbox_productos = tk.Listbox(self.frame_autocompletado, font=FUENTES['normal'], 
                                            height=6, width=40)
        self.listbox_productos.bind('<<ListboxSelect>>', self.seleccionar_de_listbox)
        self.listbox_productos.bind('<Return>', self.seleccionar_de_listbox)
        
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

        # Botón Otro
        btn_otro = tk.Button(frame_busqueda, text="Otro", command=self.agregar_producto_variable,
                            bg=COLORES['primario'], fg='white', font=FUENTES['normal'],
                            cursor='hand2', padx=15)
        btn_otro.pack(side=tk.LEFT, padx=5)
        
        # Variable para productos completos
        self.productos_dict = {}

    def filtrar_productos(self, event):
        """Filtra productos mientras se escribe"""
        texto = self.entry_busqueda.get().lower()
        
        if not texto:
            self.listbox_productos.pack_forget()
            return
        
        # Limpiar listbox
        self.listbox_productos.delete(0, tk.END)
        
        # Filtrar productos
        coincidencias = []
        for producto in self.gestor_productos.productos:
            nombre_completo = f"{producto['nombre']} - S/ {producto['precio']:.2f}"
            if config.STOCK_ACTIVADO:
                nombre_completo += f" [STOCK: {producto['stock']}]"
            
            if texto in producto['nombre'].lower() or texto in producto['codigo'].lower():
                coincidencias.append((nombre_completo, producto))
        
        # Mostrar coincidencias
        if coincidencias:
            for nombre_completo, producto in coincidencias[:10]:  # Limitar a 10
                self.listbox_productos.insert(tk.END, nombre_completo)
                self.productos_dict[nombre_completo] = producto
            
            self.listbox_productos.pack()
            self.listbox_productos.config(height=min(len(coincidencias), 6))
        else:
            self.listbox_productos.pack_forget()

    def mover_seleccion_abajo(self, event):
        """Permite navegar con flecha abajo al listbox"""
        if self.listbox_productos.winfo_ismapped():
            self.listbox_productos.focus_set()
            self.listbox_productos.selection_set(0)

    def seleccionar_de_listbox(self, event):
        """Selecciona un producto del listbox"""
        if not self.listbox_productos.curselection():
            return
        
        seleccion = self.listbox_productos.get(self.listbox_productos.curselection())
        self.entry_busqueda.delete(0, tk.END)
        self.entry_busqueda.insert(0, seleccion)
        self.producto_seleccionado = self.productos_dict[seleccion]
        self.listbox_productos.pack_forget()
        self.spin_cantidad.focus_set()
    
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
        
        # Control de stock
        if config.STOCK_ACTIVADO:
            exito, mensaje_stock = self.gestor_productos.actualizar_stock(
                self.producto_seleccionado['codigo'], cantidad)
            if not exito:
                messagebox.showerror("Error de Stock", mensaje_stock)
                self.gestor_ventas.eliminar_venta(len(self.gestor_ventas.ventas_actuales) - 1)
                return
            elif "ADVERTENCIA" in mensaje_stock:
                messagebox.showwarning("Advertencia", mensaje_stock)
        
        # Actualizar interfaz
        self.agregar_item_lista(venta, len(self.gestor_ventas.ventas_actuales) - 1)
        self.actualizar_totales()
        self.actualizar_productos_dict()
        
        # ✅ NUEVO: Autoguardar en segundo plano
        self.gestor_ventas.autoguardar_temporal()

        # Limpiar selección
        self.entry_busqueda.delete(0, tk.END)
        self.spin_cantidad.delete(0, tk.END)
        self.spin_cantidad.insert(0, '1')
        self.producto_seleccionado = None
        self.entry_busqueda.focus_set()

    def actualizar_productos_dict(self):
        """Actualiza el diccionario de productos después de cambios en stock"""
        self.productos_dict = {}
        for producto in self.gestor_productos.productos:
            nombre_completo = f"{producto['nombre']} - S/ {producto['precio']:.2f}"
            if config.STOCK_ACTIVADO:
                nombre_completo += f" [STOCK: {producto['stock']}]"
            self.productos_dict[nombre_completo] = producto
    
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
        if config.STOCK_ACTIVADO and indice < len(self.gestor_ventas.ventas_actuales):
            venta = self.gestor_ventas.ventas_actuales[indice]
            for producto in self.gestor_productos.productos:
                if producto['codigo'] == venta['codigo']:
                    producto['stock'] += venta['cantidad']
                    self.gestor_productos.guardar_productos()
                    break
        
        if self.gestor_ventas.eliminar_venta(indice):
            self.actualizar_lista()
            self.actualizar_totales()
            self.actualizar_productos_dict()
    
            # ✅ NUEVO: Autoguardar después de eliminar
            self.gestor_ventas.autoguardar_temporal()

    def actualizar_lista(self):
        """Actualiza la lista visual de ventas"""
        for widget in self.frame_productos.winfo_children():
            widget.destroy()
        
        self.crear_encabezado_lista()
        
        for i, venta in enumerate(self.gestor_ventas.obtener_ventas()):
            self.agregar_item_lista(venta, i)
    
    def actualizar_totales(self):
        """Actualiza los totales mostrados"""
        totales = self.gestor_ventas.calcular_totales()
        self.label_total_general.config(text=f"S/ {totales['general']:.2f}")
        self.label_total_efectivo.config(text=f"S/ {totales['efectivo']:.2f}")
        self.label_total_virtual.config(text=f"S/ {totales['virtual']:.2f}")
    
    def cerrar_caja(self):
        """Cierra la caja del día (guarda ventas y limpia lista)"""
        if not self.gestor_ventas.ventas_actuales:
            messagebox.showwarning("Advertencia", "No hay ventas para guardar")
            return
        
        # Confirmación
        respuesta = messagebox.askyesno(
            "Cerrar Caja del Día",
            "¿Desea cerrar la caja del día?\n\n"
            "Esto guardará todas las ventas actuales\n"
            "y limpiará la lista para comenzar una nueva caja.",
            icon='question'
        )
        
        if not respuesta:
            return
        
        exito, resultado = self.gestor_ventas.guardar_ventas()
        if exito:
            self.mostrar_resumen_cierre(resultado)
            self.actualizar_lista()
            self.actualizar_totales()
        else:
            messagebox.showerror("Error", resultado)
    
    def limpiar_caja_emergencia(self):
        """Limpia la caja actual sin guardar (EMERGENCIA)"""
        if not self.gestor_ventas.ventas_actuales:
            messagebox.showinfo("Información", "No hay ventas en la caja actual")
            return
        
        # Doble confirmación
        respuesta1 = messagebox.askyesno(
            "⚠️ Limpiar Caja (Emergencia)",
            "ADVERTENCIA: Esta acción eliminará todas las ventas\n"
            "actuales SIN GUARDAR.\n\n"
            "¿Está seguro de continuar?",
            icon='warning'
        )
        
        if not respuesta1:
            return
        
        respuesta2 = messagebox.askyesno(
            "⚠️ Confirmación Final",
            "Esta es su última oportunidad.\n\n"
            "Las ventas actuales se perderán PERMANENTEMENTE.\n\n"
            "¿Confirma la limpieza de caja?",
            icon='error'
        )
        
        if respuesta2:
            # Devolver stock si está activado
            if config.STOCK_ACTIVADO:
                for venta in self.gestor_ventas.ventas_actuales:
                    for producto in self.gestor_productos.productos:
                        if producto['codigo'] == venta['codigo']:
                            producto['stock'] += venta['cantidad']
                self.gestor_productos.guardar_productos()
            
            self.gestor_ventas.limpiar_ventas()
            self.actualizar_lista()
            self.actualizar_totales()
            self.actualizar_productos_dict()
            messagebox.showinfo("Caja Limpiada", "La caja ha sido limpiada exitosamente")
    
    def recargar_productos(self):
        """Recarga los productos del CSV"""
        if self.gestor_productos.cargar_productos():
            self.actualizar_productos_dict()
            messagebox.showinfo("Éxito", "Productos recargados correctamente")
        else:
            messagebox.showerror("Error", "No se pudieron recargar los productos")
    
    def agregar_producto_variable(self):
        """Abre ventana para agregar producto de precio variable Y guardarlo en productos.csv"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Producto Variable")
        ventana.geometry("400x300")
        ventana.geometry("380x280")
        ventana.minsize(350, 250)
        ventana.resizable(True, True)
        ventana.configure(bg=COLORES['fondo'])

        
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Frame principal con scroll
        main_frame = tk.Frame(ventana, bg=COLORES['fondo'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame, bg=COLORES['fondo'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORES['fondo'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        tk.Label(scrollable_frame, text="Producto de Precio Variable", 
                font=FUENTES['titulo'], bg=COLORES['fondo']).pack(pady=15)
        
        tk.Label(scrollable_frame, 
                text="El producto se agregará automáticamente\nal catálogo para uso futuro.",
                font=FUENTES['pequeña'], bg=COLORES['fondo'], 
                fg='gray', justify=tk.CENTER).pack(pady=5)
        
        # Frame para campos
        frame_campos = tk.Frame(scrollable_frame, bg=COLORES['fondo'])
        frame_campos.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Nombre del producto
        tk.Label(frame_campos, text="Nombre del Producto:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        entry_nombre = tk.Entry(frame_campos, font=FUENTES['normal'], width=25)
        entry_nombre.insert(0, "otros")
        entry_nombre.select_range(0, tk.END)
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.focus()
        
        # Precio Base
        tk.Label(frame_campos, text="Precio Base Unitario:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        entry_precio = tk.Entry(frame_campos, font=FUENTES['normal'], width=25)
        entry_precio.grid(row=1, column=1, padx=10, pady=10)
        
        # Cantidad
        tk.Label(frame_campos, text="Cantidad:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        spin_cantidad_var = tk.Spinbox(frame_campos, from_=1, to=1000, width=23,
                                    font=FUENTES['normal'])
        spin_cantidad_var.grid(row=2, column=1, padx=10, pady=10)
        
        # Categoría (opcional)
        tk.Label(frame_campos, text="Categoría:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=3, column=0, padx=10, pady=10, sticky='e')
        combo_categoria = ttk.Combobox(frame_campos, font=FUENTES['normal'], width=23)
        combo_categoria['values'] = ['Varios'] + self.gestor_productos.obtener_categorias()
        combo_categoria.set('Varios')
        combo_categoria.grid(row=3, column=1, padx=10, pady=10)
        
        # Método de pago
        tk.Label(frame_campos, text="Método de Pago:", font=FUENTES['normal'],
                bg=COLORES['fondo']).grid(row=4, column=0, padx=10, pady=10, sticky='e')
        
        frame_metodos_var = tk.Frame(frame_campos, bg=COLORES['fondo'])
        frame_metodos_var.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        
        metodo_pago_var = tk.StringVar(value='E')
        for codigo, nombre in METODOS_PAGO.items():
            rb = tk.Radiobutton(frame_metodos_var, text=f"{codigo} ({nombre})", 
                            variable=metodo_pago_var, value=codigo,
                            font=FUENTES['pequeña'], bg=COLORES['fondo'])
            rb.pack(anchor='w')
        
        # Función para agregar
        def agregar_variable():
            nombre = entry_nombre.get().strip()
            precio_str = entry_precio.get().strip()
            cantidad_str = spin_cantidad_var.get()
            categoria = combo_categoria.get().strip()
            metodo = metodo_pago_var.get()
            
            if not nombre:
                messagebox.showerror("Error", "Ingrese el nombre del producto")
                entry_nombre.focus()
                return
            
            if not validar_numero(precio_str, 'float'):
                messagebox.showerror("Error", "El precio debe ser un número válido")
                entry_precio.focus()
                return
            
            if not validar_numero(cantidad_str, 'int'):
                messagebox.showerror("Error", "La cantidad debe ser un número válido")
                spin_cantidad_var.focus()
                return
            
            cantidad = int(cantidad_str)
            precio = float(precio_str)
            
            # Generar código automático
            codigo = self.gestor_productos.obtener_siguiente_codigo_variable()
            
            # Guardar producto en productos.csv
            exito, mensaje = self.gestor_productos.agregar_producto(
                codigo, nombre, precio, categoria, stock=0
            )
            
            if not exito:
                messagebox.showerror("Error", f"No se pudo agregar el producto:\n{mensaje}")
                return
            
            # Recargar productos
            self.gestor_productos.cargar_productos()
            self.actualizar_productos_dict()
            
            # Buscar el producto recién agregado
            producto_nuevo = None
            for p in self.gestor_productos.productos:
                if p['codigo'] == codigo:
                    producto_nuevo = p
                    break
            
            if not producto_nuevo:
                messagebox.showerror("Error", "Producto agregado pero no encontrado")
                return
            
            # Agregar a la venta actual
            venta = self.gestor_ventas.agregar_venta(producto_nuevo, cantidad, metodo)
            self.agregar_item_lista(venta, len(self.gestor_ventas.ventas_actuales) - 1)
            self.actualizar_totales()
            
            # ✅ NUEVO: Autoguardar en segundo plano
            self.gestor_ventas.autoguardar_temporal()

            ventana.destroy()
            messagebox.showinfo("Éxito", 
                              f"✅ Producto '{nombre}' agregado al catálogo\n"
                              f"Código: {codigo}\n"
                              f"Precio base: S/ {precio:.2f}\n\n"
                              f"También se agregó a la venta actual.")
        
        # Botón Agregar
        btn_agregar_var = tk.Button(scrollable_frame, text="Agregar a Venta y Catálogo", 
                                    command=agregar_variable,
                                    bg=COLORES['secundario'], fg='white', 
                                    font=FUENTES['normal'], cursor='hand2',
                                    padx=30, pady=10)
        btn_agregar_var.pack(pady=15)
        
        # Botón Cancelar
        btn_cancelar = tk.Button(scrollable_frame, text="Cancelar", 
                                command=ventana.destroy,
                                bg=COLORES['borde'], fg='white', 
                                font=FUENTES['pequeña'], cursor='hand2',
                                padx=20, pady=5)
        btn_cancelar.pack(pady=5)
        
        # Pack canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Permitir Enter
        entry_precio.bind('<Return>', lambda e: agregar_variable())
        
        # Habilitar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # === MÉTODOS DE GESTIÓN DE PRODUCTOS ===
    
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
                self.actualizar_productos_dict()
                ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        btn_guardar = tk.Button(ventana, text="Guardar", command=guardar,
                               bg=COLORES['secundario'], fg='white', font=FUENTES['normal'],
                               cursor='hand2', padx=20)
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)
    
    def ventana_editar_producto(self):
        """Abre ventana para editar un producto existente"""
        ventana_seleccion = tk.Toplevel(self.root)
        ventana_seleccion.title("Seleccionar Producto")
        ventana_seleccion.geometry("450x400")
        ventana_seleccion.configure(bg=COLORES['fondo'])
        
        tk.Label(ventana_seleccion, text="Seleccione el producto a editar:", 
                font=FUENTES['titulo'], bg=COLORES['fondo']).pack(pady=10)
        
        frame_lista = tk.Frame(ventana_seleccion, bg='white')
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame_lista, font=FUENTES['normal'], 
                            yscrollcommand=scrollbar.set, height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for producto in self.gestor_productos.productos:
            listbox.insert(tk.END, f"{producto['codigo']} - {producto['nombre']} - S/ {producto['precio']:.2f}")
        
        def abrir_editor():
            seleccion = listbox.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            
            producto = self.gestor_productos.productos[seleccion[0]]
            ventana_seleccion.destroy()
            
            ventana = tk.Toplevel(self.root)
            ventana.title("Editar Producto")
            ventana.geometry("400x300")
            ventana.configure(bg=COLORES['fondo'])
            
            tk.Label(ventana, text="Código:", font=FUENTES['normal'], 
                    bg=COLORES['fondo']).grid(row=0, column=0, padx=10, pady=10, sticky='e')
            entry_codigo = tk.Entry(ventana, font=FUENTES['normal'], width=25)
            entry_codigo.insert(0, producto['codigo'])
            entry_codigo.config(state='disabled')
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
                    self.actualizar_productos_dict()
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
        
        frame_lista = tk.Frame(ventana, bg='white')
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame_lista, font=FUENTES['normal'], 
                            yscrollcommand=scrollbar.set, height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for producto in self.gestor_productos.productos:
            listbox.insert(tk.END, f"{producto['codigo']} - {producto['nombre']} - S/ {producto['precio']:.2f}")
        
        def eliminar():
            seleccion = listbox.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return
            
            producto = self.gestor_productos.productos[seleccion[0]]
            
            respuesta = messagebox.askyesno("Confirmar Eliminación", 
                                           f"¿Está seguro de eliminar el producto?\n\n"
                                           f"Código: {producto['codigo']}\n"
                                           f"Nombre: {producto['nombre']}\n"
                                           f"Precio: S/ {producto['precio']:.2f}\n\n"
                                           f"Esta acción no se puede deshacer.")
            if respuesta:
                if self.gestor_productos.eliminar_producto(producto['codigo']):
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                    self.actualizar_productos_dict()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el producto")
        
        btn_eliminar = tk.Button(ventana, text="Eliminar Seleccionado", 
                                command=eliminar,
                                bg=COLORES['error'], fg='white', font=FUENTES['normal'],
                                cursor='hand2', padx=20)
        btn_eliminar.pack(pady=10)
    
    # === MÉTODOS DE REPORTES ===
    
    def abrir_inventario_vendido(self):
        """Abre ventana de inventario vendido"""
        ventana = VentanaInventarioVendido(self.root)
        ventana.set_gestor_productos(self.gestor_productos)
    
    def abrir_reporte_dia(self):
        """Abre ventana de reporte del día"""
        VentanaReporteDia(self.root)
    
    def configurar_stock(self):
        """Abre ventana de configuración de stock"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Configuración de Stock")
        ventana.geometry("500x500")
        ventana.configure(bg=COLORES['fondo'])
        
        tk.Label(ventana, text="Gestión de Inventario (Stock)", 
                font=FUENTES['titulo'], bg=COLORES['fondo']).pack(pady=20)
        
        estado_actual = "ACTIVADO" if config.STOCK_ACTIVADO else "DESACTIVADO"
        tk.Label(ventana, text=f"Estado actual: {estado_actual}",
                font=FUENTES['normal'], bg=COLORES['fondo'], 
                fg=COLORES['secundario'] if config.STOCK_ACTIVADO else COLORES['error']).pack(pady=10)
        
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
        
        frame_botones = tk.Frame(ventana, bg=COLORES['fondo'])
        frame_botones.pack(pady=20)
        
        def activar_stock():
            config.guardar_config_stock(True)
            config.STOCK_ACTIVADO = True
            self.gestor_productos.cargar_productos()
            self.actualizar_productos_dict()
            messagebox.showinfo("Éxito", "Control de stock ACTIVADO\n\n"
                                        "Los productos han sido recargados.")
            ventana.destroy()
        
        def desactivar_stock():
            respuesta = messagebox.askyesno("Confirmar", 
                                        "¿Desea DESACTIVAR el control de stock?\n\n"
                                        "Los valores de stock se mantendrán en el CSV\n"
                                        "pero no se controlarán las ventas.")
            if respuesta:
                config.guardar_config_stock(False)
                config.STOCK_ACTIVADO = False
                self.gestor_productos.cargar_productos()
                self.actualizar_productos_dict()
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