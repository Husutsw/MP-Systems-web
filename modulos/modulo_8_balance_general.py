# 8- BALANCE GENERAL (DERIVADO DEL MODULO 7 AJUSTADO)
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import os
import platform
import csv

def ejecutar_modulo(app):
    ventana = tk.Toplevel()
    ventana.title("Balance General")
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

    color_fondo = "#f8e38c"
    color_validado = "#c9f7c3"
    color_error = "#ffc9c9"

    frame_tabla = tk.Frame(ventana)
    frame_tabla.grid_rowconfigure(0, weight=1)
    frame_tabla.grid_columnconfigure(0, weight=1)

    contenedor = tk.Frame(frame_tabla)
    contenedor.pack(pady=10)

    frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_botones = tk.Frame(ventana, bg="#dddddd")
    frame_botones.pack(side=tk.RIGHT, fill=tk.Y)

    # TITULO CON NOMBRE DEL MODULO Y EMPRESA
    tk.Label(
        contenedor,
        text=f"Balance General - {app.empresa_actual}",
        font=("Arial", 16, "bold")
    ).grid(row=0, column=0, columnspan=3, pady=10)

    headers = ["Categoria", "Descripcion", "Monto"]
    for idx, header in enumerate(headers):
        tk.Label(contenedor, text=header, font=("Arial", 12, "bold")).grid(row=1, column=idx)

    barra_resultado = tk.Label(contenedor, text="", font=("Arial", 11, "bold"))
    barra_resultado.grid(row=1000, column=0, columnspan=3, pady=10)

    filas = []

    def agregar_fila():
        row = len(filas) + 2
        tipo = ttk.Combobox(contenedor, values=["Activo", "Pasivo", "Patrimonio"], state="readonly", width=17)
        tipo.set("Activo")
        tipo.grid(row=row, column=0, padx=2)
        desc = tk.Entry(contenedor, width=30, bg=color_fondo)
        desc.grid(row=row, column=1, padx=2)
        monto = tk.Entry(contenedor, width=17, bg=color_fondo)
        monto.grid(row=row, column=2, padx=2)
        filas.append((tipo, desc, monto))

    def eliminar_fila():
        if not filas:
            messagebox.showwarning("Aviso", "No hay filas para eliminar.")
            return
        tipo, desc, monto = filas.pop()
        tipo.destroy()
        desc.destroy()
        monto.destroy()

    def calcular():
        activo = 0
        pasivo = 0
        patrimonio = 0
        for f in filas:
            descripcion_valida = bool(f[1].get().strip())
            try:
                monto = float(f[2].get())
                f[2].delete(0, tk.END)
                f[2].insert(0, f"{app.simbolo_moneda} {monto:,.2f}")
                f[2].config(bg=color_validado)
                f[1].config(bg=color_validado if descripcion_valida else color_error)
                if f[0].get() == "Activo":
                    activo += monto
                elif f[0].get() == "Pasivo":
                    pasivo += monto
                elif f[0].get() == "Patrimonio":
                    patrimonio += monto
            except:
                f[2].delete(0, tk.END)
                f[2].insert(0, f"{app.simbolo_moneda} 0.00")
                f[2].config(bg=color_error)
                f[1].config(bg=color_error)

        resultado = activo - (pasivo + patrimonio)
        msg = f"Activo: {app.simbolo_moneda} {activo:,.2f} | Pasivo: {app.simbolo_moneda} {pasivo:,.2f} | Patrimonio: {app.simbolo_moneda} {patrimonio:,.2f}\n"
        msg += f"{'BALANCE CUADRADO' if resultado == 0 else 'DESCUADRE'} - Diferencia: {app.simbolo_moneda} {abs(resultado):,.2f}"
        barra_resultado.config(text=msg, bg="#f8d2d2" if resultado != 0 else "#d2f8d2")
        messagebox.showinfo("Resultado", msg)

    def exportar_pdf():
        calcular()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(temp_file.name, pagesize=A4)
        c.setFont("Helvetica", 12)
        c.drawString(50, 800, f"Balance General - {app.empresa_actual}")
        y = 770
        c.drawString(50, y, "Categoria")
        c.drawString(200, y, "Descripcion")
        c.drawString(400, y, "Monto")
        y -= 20
        for tipo, desc, monto in filas:
            c.drawString(50, y, tipo.get())
            c.drawString(200, y, desc.get())
            c.drawString(400, y, monto.get())
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

    def exportar_excel():
        calcular()
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivo CSV", "*.csv")])
        if archivo:
            with open(archivo, mode="w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Categoria", "Descripcion", "Monto"])
                for tipo, desc, monto in filas:
                    writer.writerow([tipo.get(), desc.get(), monto.get()])
            messagebox.showinfo("Exportado", "Archivo exportado correctamente.")

    def volver_menu():
        ventana.destroy()

    botones = [
        ("Agregar Fila", agregar_fila),
        ("Eliminar Fila", eliminar_fila),
        ("Calcular", calcular),
        ("Exportar PDF", exportar_pdf),
        ("Exportar Excel", exportar_excel),
        ("Menu", volver_menu)
    ]

    for texto, accion in botones:
        tk.Button(frame_botones, text=texto, width=18, command=accion).pack(pady=10, padx=10)

    agregar_fila()
