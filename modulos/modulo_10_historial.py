# 10- HISTORIAL DEL SISTEMA

# 1- IMPORTACION DE MODULOS NECESARIOS
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import csv
import os
import tempfile
import getpass
import platform
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# 2- FUNCION PRINCIPAL DEL MODULO
# linea 1 def
def ejecutar_modulo(app):
    # CREAR VENTANA CENTRADA
    ventana = tk.Toplevel()
    ventana.title("Historial del Sistema")

    ancho_ventana = 1000
    alto_ventana = 600
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x_pos = int((ancho_pantalla - ancho_ventana) / 2)
    y_pos = int((alto_pantalla - alto_ventana) / 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    ventana.transient(app)
    ventana.lift()
    ventana.grab_set()

    # COLORES
    color_fondo = "#f8e38c"
    color_validado = "#c9f7c3"
    color_error = "#ffc9c9"

    # FRAMES
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_botones = tk.Frame(ventana, bg="#dddddd")
    frame_botones.pack(side=tk.RIGHT, fill=tk.Y)

    # TITULO
    tk.Label(frame_tabla, text="Historial del Sistema", font=("Arial", 16, "bold")).pack(pady=10)

    # TABLA
    columnas = ("Fecha", "Hora", "Usuario", "Accion")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=25)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=200)
    tabla.pack(fill=tk.BOTH, expand=True)

    # 3- FUNCION PARA ACTUALIZAR
    # linea 2 def
    def actualizar():
        for i in tabla.get_children():
            tabla.delete(i)
        datos = obtener_historial_ficticio()
        for fila in datos:
            tabla.insert("", tk.END, values=fila)

    # 4- FUNCION PARA EXPORTAR A EXCEL
    # linea 2 def
    def exportar_excel():
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
        if archivo:
            with open(archivo, "w", newline="") as f:
                escritor = csv.writer(f)
                escritor.writerow(columnas)
                for fila_id in tabla.get_children():
                    fila = tabla.item(fila_id)['values']
                    escritor.writerow(fila)
            messagebox.showinfo("Exportado", "Archivo CSV guardado correctamente.")

    # 5- FUNCION PARA EXPORTAR A PDF
    # linea 2 def
    def exportar_pdf():
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(temp_file.name, pagesize=A4)
        c.setFont("Helvetica", 12)
        c.drawString(50, 800, "Historial del Sistema - MP Systems")

        y = 770
        for col in columnas:
            c.drawString(50 + columnas.index(col)*150, y, col)

        y -= 20
        for fila_id in tabla.get_children():
            fila = tabla.item(fila_id)['values']
            for i, valor in enumerate(fila):
                c.drawString(50 + i*150, y, str(valor))
            y -= 20
            if y < 50:
                c.showPage()
                y = 800

        c.save()

        # ABRIR ARCHIVO TEMPORAL
        if platform.system() == "Windows":
            os.startfile(temp_file.name)
        elif platform.system() == "Darwin":
            os.system(f"open '{temp_file.name}'")
        else:
            os.system(f"xdg-open '{temp_file.name}'")

        # PREGUNTAR SI DESEA GUARDAR
        respuesta = messagebox.askyesno("Guardar PDF", "¿Desea guardar este archivo?")
        if respuesta:
            archivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
            if archivo:
                with open(temp_file.name, "rb") as src, open(archivo, "wb") as dst:
                    dst.write(src.read())
                messagebox.showinfo("Guardado", "Archivo PDF guardado correctamente.")
        os.remove(temp_file.name)

    # 6- FUNCION FICTICIA PARA CARGAR HISTORIAL
    # linea 1 def
    def obtener_historial_ficticio():
        usuario = getpass.getuser()
        ahora = datetime.now()
        return [
            [ahora.strftime("%d/%m/%Y"), ahora.strftime("%H:%M:%S"), usuario, "Inicio del sistema"],
            [ahora.strftime("%d/%m/%Y"), ahora.strftime("%H:%M:%S"), usuario, "Ingreso al modulo Libro Diario"],
            [ahora.strftime("%d/%m/%Y"), ahora.strftime("%H:%M:%S"), usuario, "Validacion de asiento contable"],
        ]

    # 7- BOTONES
    botones = [
        ("Actualizar", actualizar),
        ("Exportar a Excel", exportar_excel),
        ("Exportar a PDF", exportar_pdf)
    ]

    for texto, accion in botones:
        tk.Button(frame_botones, text=texto, width=18, command=accion).pack(pady=10, padx=10)

    actualizar()
