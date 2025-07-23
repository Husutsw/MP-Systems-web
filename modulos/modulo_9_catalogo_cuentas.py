# 9- CATALOGO DE CUENTAS (ESTILO AJUSTADO AL MODULO 6)

# 1- IMPORTACION DE MODULOS NECESARIOS
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import os
import platform
import csv  # IMPORTANTE PARA EXCEL

# 2- FUNCION PRINCIPAL DEL MODULO
#linea 1 def
def ejecutar_modulo(app):
    # CREACION DE VENTANA SECUNDARIA
    ventana = tk.Toplevel()
    ventana.title("Catalogo de Cuentas")

    # CONFIGURACION DE TAMAÑO Y POSICION
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

    # DEFINICION DE COLORES
    color_fondo = "#f8e38c"
    color_validado = "#c9f7c3"
    color_error = "#ffc9c9"

    # CREACION DE FRAMES
    frame_tabla = tk.Frame(ventana)
    frame_tabla.grid_rowconfigure(0, weight=1)
    frame_tabla.grid_columnconfigure(0, weight=1)

    contenedor = tk.Frame(frame_tabla)
    contenedor.pack(pady=20)

    frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_botones = tk.Frame(ventana, bg="#dddddd")
    frame_botones.pack(side=tk.RIGHT, fill=tk.Y)

    # TITULO Y ENCABEZADOS (ACTUALIZADO CON EMPRESA)
    tk.Label(contenedor, text=f"Catalogo de Cuentas - {app.empresa_actual}", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
    headers = ["Codigo", "Nombre de Cuenta", "Tipo"]
    for idx, header in enumerate(headers):
        tk.Label(contenedor, text=header, font=("Arial", 12, "bold")).grid(row=1, column=idx)

    barra_resultado = tk.Label(contenedor, text="", font=("Arial", 11, "bold"))
    barra_resultado.grid(row=1000, column=0, columnspan=3, pady=10)

    filas = []

    # 3- FUNCION PARA AGREGAR FILAS
    #linea 2 def
    def agregar_fila():
        row = len(filas) + 2
        codigo = tk.Entry(contenedor, width=20, bg=color_fondo)
        codigo.grid(row=row, column=0, padx=2)
        nombre = tk.Entry(contenedor, width=40, bg=color_fondo)
        nombre.grid(row=row, column=1, padx=2)
        tipo = ttk.Combobox(contenedor, values=["Activo", "Pasivo", "Patrimonio", "Ingreso", "Egreso"], state="readonly", width=20)
        tipo.set("Activo")
        tipo.grid(row=row, column=2, padx=2)
        filas.append((codigo, nombre, tipo))

    # 4- FUNCION PARA ELIMINAR FILAS
    #linea 2 def
    def eliminar_fila():
        if not filas:
            messagebox.showwarning("Aviso", "No hay filas para eliminar.")
            return
        codigo, nombre, tipo = filas.pop()
        codigo.destroy()
        nombre.destroy()
        tipo.destroy()

    # 5- FUNCION PARA VALIDAR CATALOGO
    #linea 2 def
    def validar_catalogo():
        valido = True
        for fila in filas:
            codigo, nombre, tipo = fila

            codigo_valido = bool(codigo.get().strip())
            nombre_valido = bool(nombre.get().strip())

            if codigo_valido:
                codigo.config(bg=color_validado)
            else:
                codigo.config(bg=color_error)
                valido = False

            if nombre_valido:
                nombre.config(bg=color_validado)
            else:
                nombre.config(bg=color_error)
                valido = False

        if not valido:
            messagebox.showerror("Error", "Por favor complete todos los campos del catalogo.")
        return valido

    # 6- FUNCION PARA EXPORTAR A PDF
    #linea 2 def
    def exportar_pdf():
        validar_catalogo()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(temp_file.name, pagesize=A4)
        c.setFont("Helvetica", 12)
        c.drawString(50, 800, f"Catalogo de Cuentas - {app.empresa_actual}")
        y = 770
        c.drawString(50, y, "Codigo")
        c.drawString(200, y, "Nombre de Cuenta")
        c.drawString(400, y, "Tipo")
        y -= 20
        for codigo, nombre, tipo in filas:
            c.drawString(50, y, codigo.get())
            c.drawString(200, y, nombre.get())
            c.drawString(400, y, tipo.get())
            y -= 20
            if y < 50:
                c.showPage()
                y = 800
        c.save()

        if platform.system() == "Windows":
            os.startfile(temp_file.name)
        elif platform.system() == "Darwin":
            os.system(f"open '{temp_file.name}'")
        else:
            os.system(f"xdg-open '{temp_file.name}'")

        respuesta = messagebox.askyesno("Guardar PDF", "¿Desea guardar este archivo?")
        if respuesta:
            archivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
            if archivo:
                with open(temp_file.name, "rb") as src, open(archivo, "wb") as dst:
                    dst.write(src.read())
                messagebox.showinfo("Guardado", "Archivo guardado correctamente.")
        os.remove(temp_file.name)

    # 7- FUNCION PARA EXPORTAR A EXCEL
    #linea 2 def
    def exportar_excel():
        if not validar_catalogo():
            return
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivo CSV", "*.csv")])
        if archivo:
            with open(archivo, mode="w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Codigo", "Nombre de Cuenta", "Tipo"])
                for codigo, nombre, tipo in filas:
                    writer.writerow([codigo.get(), nombre.get(), tipo.get()])
            messagebox.showinfo("Exportado", "Archivo exportado correctamente.")

    # 8- FUNCION PARA VOLVER AL MENU
    #linea 2 def
    def volver_menu():
        ventana.destroy()

    # 9- CREACION DE BOTONES Y ASOCIACION DE FUNCIONES
    botones = [
        ("Agregar Fila", agregar_fila),
        ("Eliminar Fila", eliminar_fila),
        ("Validar Catalogo", validar_catalogo),
        ("Exportar PDF", exportar_pdf),
        ("Exportar Excel", exportar_excel),
        ("Menu", volver_menu)
    ]

    for texto, accion in botones:
        tk.Button(frame_botones, text=texto, width=18, command=accion).pack(pady=10, padx=10)

    # 10- AGREGAR UNA FILA POR DEFECTO AL INICIAR
    agregar_fila()
