from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from database import SqlAccess


class Report():
    def __init__(self, unique_id):
        self.access = SqlAccess(unique_id)
        self.directory = "Reports"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    @staticmethod
    def calculate_number_of_pages(data):
        """
        Calculating number of pages the report will have
        """
        items_per_page = (615 - 40) // 16
        total_pages = (len(data) + items_per_page - 1) // items_per_page
        return total_pages + 1

    def create_class_pdf(self, file_name, company_name, title, start_date, end_date):
        # Initialize necessary variables
        current_time = datetime.now()
        current_time = current_time.strftime("%m/%d/%Y %I:%M:%S %p")
        page_num = 1
        y_pos = 625
        data = self.access.admin_read_all_users()
        print(data)

        # Set up the canvas
        c = canvas.Canvas(f"{self.directory}/{file_name}.pdf", pagesize=letter)

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

        total_pages = self.calculate_number_of_pages(data)

        # First page set up
        c.setFont("Helvetica", 10)
        c.drawString(520, 30, f"Page {page_num} of {total_pages}")
        c.drawString(30, 30, current_time)

        # Loop through all names and total minutes
        for row in data:
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
            c.drawString(80, y_pos, row[1])
            c.drawString(370, y_pos, str(row[-1]))
            y_pos -= 16

        # Save the PDF
        c.save()

    def create_user_specific_pdf(self, file_name, company_name, title,
                                 start_date, end_date, name, student_id):
        # Initialize necessary variables
        current_time = datetime.now()
        current_time = current_time.strftime("%m/%d/%Y %I:%M:%S %p")
        page_num = 1
        y_pos = 605
        data = self.access.admin_read_self_table(student_id)

        # Set up the canvas
        c = canvas.Canvas(f"{self.directory}/{file_name}.pdf", pagesize=letter)

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
        c.drawString(30, 662, name)

        # Header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(75, 630, 'Date')
        c.drawString(200, 630, 'Time(in)')
        c.drawString(325, 630, 'Time(out)')
        c.drawString(430, 630, 'Hours:Minutes')

        # Draw the horizontal line below the header
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(2)
        c.line(65, 622, 525, 622)

        total_pages = self.calculate_number_of_pages(data)

        # First page set up
        c.setFont("Helvetica", 10)
        c.drawString(520, 30, f"Page {page_num} of {total_pages}")
        c.drawString(30, 30, current_time)

        # Loop through all names and total minutes
        for row in data:
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
            # Date, clock in time, clock out time, and total minutes
            c.setFont("Helvetica", 12)
            c.drawString(75, y_pos, row[1])
            c.drawRightString(245, y_pos, row[2])
            c.drawRightString(375, y_pos, row[3])
            c.drawString(460, y_pos, row[4])
            y_pos -= 16

        # Save the PDF
        c.save()

    def download_pdf(self, path):
        if os.name == "nt":
            os.startfile(path)