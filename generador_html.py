import os
import subprocess


def generar_html(resultados):
    """
    Genera un archivo HTML con los resultados procesados.
    """
    html_path = "reporte_resistencia.html"
    with open(html_path, "w") as html_file:
        html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Reporte de Genes de Resistencia</title>\n")
        html_file.write("<style>\n")
        html_file.write("table { width: 100%; border-collapse: collapse; }\n")
        html_file.write("th, td { border: 1px solid black; padding: 8px; text-align: left; }\n")
        html_file.write("th { background-color: #f2f2f2; }\n")
        html_file.write("</style>\n</head>\n<body>\n")
        html_file.write("<h1>Reporte de Genes de Resistencia</h1>\n")
        html_file.write("<table>\n<tr><th>Paciente</th><th>Identificador</th><th>Genes</th><th>Longitud</th><th>Localización</th></tr>\n")

        for clave, data in resultados.items():
            qseqid, identificador, length, localizacion = clave
            genes = ", ".join(sorted(data["genes"]))

            html_file.write(f"<tr><td>{qseqid}</td><td>{identificador}</td><td>{genes}</td>")
            html_file.write(f"<td>{length} bp</td><td>{localizacion}</td></tr>\n")

        html_file.write("</table>\n</body>\n</html>")

    # Abrir el HTML generado
    if os.name == "nt":  # Windows
        os.startfile(html_path)
    elif os.name == "posix":  # Linux/Mac
        subprocess.run(["xdg-open", html_path])
