from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from database import SqlAccess
import subprocess


class Report():
    def __init__(self, unique_id):
        self.access = SqlAccess(unique_id)
        documents_path = os.path.expanduser("~/Documents")
        self.directory = os.path.join(documents_path, "Reports")
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    @staticmethod
    def calculate_number_of_pages(data):
        """
        Calculating number of pages the report will have
        """
        items_per_page = (615 - 40) // 16
        total_pages = (len(data) + items_per_page - 1) // items_per_page
        return total_pages

    def create_class_pdf(self, file_name, company_name, title):
        # Initialize necessary variables
        current_time = datetime.now()
        current_time = current_time.strftime("%m/%d/%Y %I:%M:%S %p")
        page_num = 1
        y_pos = 625
        data = self.access.admin_read_all_users()

        # Set up the canvas
        c = canvas.Canvas(f"{self.directory}/{file_name}.pdf", pagesize=letter)

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(306, 750, company_name)
        c.setFont("Helvetica-Oblique", 20)
        c.drawCentredString(306, 720, title)

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
            username = row["first_name"] + " " + row["last_name"]
            c.drawString(80, y_pos, username)
            hours = row["total_minutes"] // 60
            minutes = row["total_minutes"] % 60
            c.drawCentredString(360, y_pos, f"{hours}:{minutes}")
            y_pos -= 16

        # Save the PDF
        c.save()

    def create_user_specific_pdf(self, file_name, company_name, title,
                                 start_date, end_date, name, student_id):
        # Initialize necessary variables
        current_time = datetime.now()
        current_time = current_time.strftime("%m/%d/%Y %I:%M:%S %p")
        clock_format = "%b %d %Y %I:%M%p"
        date_format = '%m/%d/%Y'
        string_start_date = start_date
        string_end_date = end_date
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
        page_num = 1
        y_pos = 605
        data = self.access.admin_read_user_history(student_id)
        print(data)
        filtered_data = []
    
        for session in data:
            try:
                # Convert the string to a datetime object
                session_start_time = datetime.strptime(session['start_time'], clock_format)
            except ValueError:
                continue
            
            # Check if the start_time is within the given range
            if start_date <= session_start_time <= end_date:
                filtered_data.append(session)
        
        # sort data by start_time
        filtered_data.sort(key=lambda x: datetime.strptime(x['start_time'], clock_format))

        print(filtered_data)

        # Set up the canvas
        c = canvas.Canvas(f"{self.directory}/{file_name}.pdf", pagesize=letter)

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(306, 750, company_name)
        c.setFont("Helvetica-Oblique", 20)
        c.drawCentredString(306, 720, title)

        # Date
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, 690, f"{string_start_date} - {string_end_date}")

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
        for row in filtered_data:
            # Goes to the next item if the start time is empty
            if not row['start_time']:
                continue
            # Create new page and add page number at the bottom
            if y_pos < 70:
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
            
            row_date = datetime.strptime(row['start_time'], clock_format)
            if start_date <= row_date <= end_date:
                c.drawString(75, y_pos, str(row_date.strftime("%m/%d/%Y")))
                # Convert clock in string to datetime
                time_in = datetime.strptime(row['start_time'], clock_format)
                c.drawRightString(245, y_pos, f"{datetime.strftime(time_in, "%H:%M")}")
                if row['end_time'] == None:
                    c.drawRightString(375, y_pos, "N/A")
                else:
                    # Get the time out string and convert it to datetime
                    time_out = datetime.strptime(row['end_time'], clock_format)
                    c.drawRightString(375, y_pos, f"{datetime.strftime(time_out, "%H:%M")}")
                hours = row['total_minutes'] // 60
                minutes = row['total_minutes'] % 60
                c.drawCentredString(468, y_pos, f"{hours}:{minutes}")
                y_pos -= 16
            else:
                continue

        # Save the PDF
        c.save()

    def download_pdf(self, path):
        subprocess.Popen(f'explorer /select,"{path}"')