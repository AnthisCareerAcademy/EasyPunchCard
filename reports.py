from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


class Report():
    def __init__(self):
        """Placeholder. Need help to put stuff here"""

    def calculate_pages(self):
        """
        Simulated for loop counter (for total page count)
        """
        fake_y_pos = 615
        total_pages = 1
        for i in range(len(data['names'])):
            if fake_y_pos < 40:
                total_pages += 1
                fake_y_pos = 730
            fake_y_pos -= 16
        return total_pages

    def create_basic_pdf(self, file_name, company_name, title, start_date, end_date, data):
        # Initialize necessary variables
        current_time = datetime.now()
        current_time = current_time.strftime("%m/%d/%Y %I:%M:%S %p")
        page_num = 1
        y_pos = 625

        # Set up the canvas
        c = canvas.Canvas(file_name, pagesize=letter)

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(306, 750, company_name)
        c.setFont("Helvetica-Oblique", 20)
        c.drawCentredString(306, 720, title)

        # Date
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, 690, f"{start_date} - {end_date}")

        # Header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(75, 650, 'Employee')
        c.drawString(320, 650, 'Hours:Minutes')

        # Draw the horizontal line below the header
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(2)
        c.line(65, 645, 525, 645)

        total_pages = self.calculate_pages()

        # First page set up
        c.setFont("Helvetica", 10)
        c.drawString(520, 30, f"Page {page_num} of {total_pages}")
        c.drawString(30, 30, current_time)

        # Loop through all names and total minutes
        for i, (name, time) in enumerate(zip(data['names'], data['times'])):
            if y_pos < 70:
                # Create new page and add page number at the bottom
                c.showPage()
                page_num += 1
                c.setFont("Helvetica", 10)
                # Page number
                c.drawString(520, 30, f"Page {page_num} of {total_pages}")
                # Date/time
                c.drawString(30, 30, current_time)
                # Reset y position to top of next page
                y_pos = 730
            # Name and total hours:minutes
            c.setFont("Helvetica", 12)
            c.drawString(80, y_pos, name)
            c.drawString(370, y_pos, time)
            y_pos -= 16

        # Save the PDF
        c.save()

    def create_detailed_pdf(self, file_name, company_name, title, username, start_date, end_date, data):
        # Initialize necessary variables
        current_time = datetime.now()
        current_time = current_time.strftime("%m/%d/%Y %I:%M:%S %p")
        page_num = 1
        y_pos = 625

        # Set up the canvas
        c = canvas.Canvas(file_name, pagesize=letter)

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(306, 750, company_name)
        c.setFont("Helvetica-Oblique", 20)
        c.drawCentredString(306, 720, title)

        # Date
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, 690, f"{start_date} - {end_date}")

        # Username
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, 670, username)

        # Header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(75, 650, 'Employee')
        c.drawString(320, 650, 'Hours:Minutes')

        # Draw the horizontal line below the header
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(2)
        c.line(65, 645, 525, 645)

        total_pages = self.calculate_pages()

        # First page set up
        c.setFont("Helvetica", 10)
        c.drawString(520, 30, f"Page {page_num} of {total_pages}")
        c.drawString(30, 30, current_time)

        # Loop through all names and total minutes
        for i, (name, time) in enumerate(zip(data['names'], data['times'])):
            if y_pos < 70:
                # Create new page and add page number at the bottom
                c.showPage()
                page_num += 1
                c.setFont("Helvetica", 10)
                # Page number
                c.drawString(520, 30, f"Page {page_num} of {total_pages}")
                # Date/time
                c.drawString(30, 30, current_time)
                # Reset y position to top of next page
                y_pos = 730
            # Name and total hours:minutes
            c.setFont("Helvetica", 12)
            c.drawString(80, y_pos, name)
            c.drawString(370, y_pos, time)
            y_pos -= 16

        # Save the PDF
        c.save()

# Hardcode info for now
company = "Anthis Cosmetology"
title = "Time Clock Total Report"
start_date = "05/15/2024"
end_date = "06/20/2024"
data = {
    'names': ['Alice', 'Bob', 'Charlie', 'Logan sucks', 'Alice', 'Bob', 'Charlie', 'Logan sucks', 'Alice', 'Bob',
              'Charlie', 'Logan sucks', 'Alice', 'Bob', 'Charlie', 'Logan sucks', 'Alice', 'Bob', 'Charlie',
              'Logan sucks', 'Alice', 'Bob', 'Charlie', 'Logan sucks', 'Alice', 'Bob', 'Charlie', 'Logan sucks',
              'Alice', 'Bob', 'Charlie', 'Logan sucks', 'Alice', 'Bob', 'Charlie', 'Logan sucks', 'Alice', 'Bob',
              'Charlie', 'Logan sucks', 'Alice', 'Bob', 'Charlie', 'Logan sucks', 'Alice', 'Bob', 'Charlie',
              'Logan sucks', 'Alice', 'Bob', 'Charlie', 'Logan sucks', 'Alice', 'Bob', 'Charlie', 'Logan sucks',
              'Alice', 'Bob', 'Charlie', 'Logan sucks', 'Alice', 'Bob', 'Charlie', 'Logan sucks'],
    'times': ['11:23', '08:52', '00:03', '-50:90', '11:23', '08:52', '00:03', '-50:90', '11:23', '08:52', '00:03',
              '-50:90', '11:23', '08:52', '00:03', '-50:90', '11:23', '08:52', '00:03', '-50:90', '11:23', '08:52',
              '00:03', '-50:90', '11:23', '08:52', '00:03', '-50:90', '11:23', '08:52', '00:03', '-50:90', '11:23',
              '08:52', '00:03', '-50:90', '11:23', '08:52', '00:03', '-50:90', '11:23', '08:52', '00:03', '-50:90',
              '11:23', '08:52', '00:03', '-50:90', '11:23', '08:52', '00:03', '-50:90', '11:23', '08:52', '00:03',
              '-50:90', '11:23', '08:52', '00:03', '-50:90', '11:23', '08:52', '00:03', '-50:90']
}
# Create the PDF
report = Report()
report.create_detailed_pdf("simple_reportlab_pdf.pdf", company, title, "ya mama", start_date, end_date, data)

print("PDF created successfully!")