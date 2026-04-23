from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(report_text, charts):
    doc = SimpleDocTemplate("market_report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Daily Market Intelligence Report", styles["Title"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(report_text, styles["Normal"]))
    content.append(Spacer(1, 20))

    for chart in charts:
        content.append(Image(chart, width=400, height=200))
        content.append(Spacer(1, 10))

    doc.build(content)
