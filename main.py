"""
Sistema de Gestión de Bazar
Punto de entrada principal
"""
import tkinter as tk
from interfaz import VentanaPrincipal


def main():
    """Función principal del programa"""
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()


if __name__ == "__main__":
    main()