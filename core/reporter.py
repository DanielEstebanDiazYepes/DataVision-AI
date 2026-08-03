from fpdf import FPDF
import plotly.io as pio

class PDFReporter:
    def __init__(self, title="Reporte DataVision AI"):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.title = title
        
    def add_summary(self, stats, graphs_paths):
        self.pdf.cell(200, 10, txt=self.title, ln=True, align='C')
        self.pdf.ln(10)
        # Añadir estadísticas en tabla simple
        for key, val in stats.items():
            self.pdf.cell(0, 10, txt=f"{key}: {val}", ln=True)
        # Insertar imágenes de gráficos
        for path in graphs_paths:
            self.pdf.image(path, x=10, w=190)
        return self.pdf.output(dest='S').encode('latin1')