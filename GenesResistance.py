import os
import subprocess
from tkinter import Tk, filedialog, messagebox, Button, Label, StringVar
from generador_html import generar_html  # Importar la función desde el archivo separado

def seleccionar_archivo():
    """
    Función para seleccionar un archivo FASTA mediante un diálogo de archivo.
    """
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo FASTA",
        filetypes=(("Archivos FASTA", "*.fasta"), ("Todos los archivos", "*.*"))
    )
    if archivo:
        ruta_var.set(f"Archivo seleccionado:\n{archivo}")
        global archivo_seleccionado
        archivo_seleccionado = archivo

def generar_reporte():
    """
    Función para ejecutar BLAST, procesar los resultados y generar un reporte HTML.
    """
    if not archivo_seleccionado:
        messagebox.showerror("Error", "Selecciona un archivo FASTA antes de continuar.")
        return

    # BLAST search (ajusta los parámetros según tu configuración)
    base_datos = "genes_resistencia_db"  # Cambia esto al nombre de tu base BLAST
    salida_blast = "resultado_blast.txt"
    comando_blast = f"blastn -query {archivo_seleccionado} -db {base_datos} -out {salida_blast} -outfmt '6 qseqid sseqid pident length qstart qend'"

    try:
        subprocess.run(comando_blast, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"No se pudo ejecutar BLAST:\n{e}")
        return

    # Procesar resultados de BLAST
    resultados = {}
    with open(salida_blast, "r") as f:
        for linea in f:
            campos = linea.strip().split("\t")
            if len(campos) < 6:
                continue

            qseqid, sseqid, pident, length, qstart, qend = campos
            pident = float(pident)

            # Solo incluir coincidencias con 100% de identidad
            if pident != 100.00:
                continue

            # Extraer identificador y nombre de la bacteria
            identificador = sseqid.split("|")[1] if "|" in sseqid else sseqid
            gene_name = sseqid.split("|")[-1].split("[")[0].strip()

            # Clave única basada en identidad, longitud y localización
            clave = (qseqid, identificador, length, f"{qstart}-{qend}")

            if clave not in resultados:
                resultados[clave] = {"genes": set()}

            resultados[clave]["genes"].add(gene_name)

    # Generar HTML usando el archivo separado
    generar_html(resultados)

    messagebox.showinfo("Éxito", "Reporte HTML generado correctamente.")

# Interfaz gráfica con Tkinter
app = Tk()
app.title("Análisis de Genes de Resistencia")
app.geometry("500x200")

archivo_seleccionado = None
ruta_var = StringVar()
ruta_var.set("No se ha seleccionado ningún archivo")

ruta_label = Label(app, textvariable=ruta_var, wraplength=400, justify="center")
ruta_label.pack(pady=10)

btn_seleccionar = Button(app, text="Seleccionar archivo FASTA", command=seleccionar_archivo)
btn_seleccionar.pack(pady=5)

btn_generar = Button(app, text="Generar reporte", command=generar_reporte)
btn_generar.pack(pady=10)

app.mainloop()
