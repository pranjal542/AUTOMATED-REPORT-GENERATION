import csv
from fpdf import FPDF
import pandas as pd


def read_data(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Skipping header if present
        next(reader, None)
        for row in reader:
            data.append(row)
    return data


def analyze_data(data):
    df = pd.DataFrame(data, columns=["ID", "Name", "Score"])
    
    df["Score"] = pd.to_numeric(df["Score"], errors='coerce')

    
    avg_score = df["Score"].mean()
    total_students = len(df)
    passed_students = len(df[df["Score"] >= 50])
    failed_students = len(df[df["Score"] < 50])

    return avg_score, total_students, passed_students, failed_students


def generate_pdf_report(file_path, avg_score, total_students, passed_students, failed_students):
    pdf = FPDF()

    
    pdf.add_page()

    
    pdf.set_font("Arial", size=12)

    
    pdf.cell(200, 10, txt="Student Performance Report", ln=True, align="C")

    
    pdf.ln(10)  # Line break
    pdf.cell(200, 10, txt=f"Data Source: {file_path}", ln=True)
    pdf.cell(200, 10, txt=f"Total Students: {total_students}", ln=True)
    pdf.cell(200, 10, txt=f"Students Passed: {passed_students}", ln=True)
    pdf.cell(200, 10, txt=f"Students Failed: {failed_students}", ln=True)
    pdf.cell(200, 10, txt=f"Average Score: {avg_score:.2f}", ln=True)

    
    pdf.ln(10)  # Line break
    pdf.cell(200, 10, txt="Detailed Data Analysis:", ln=True)
    
    
    pdf.ln(5)  # Line break
    pdf.cell(200, 10, txt="Top 5 Students based on Score:", ln=True)

    # Add top 5 students
    data = pd.read_csv(file_path)
    data["Score"] = pd.to_numeric(data["Score"], errors="coerce")
    top_students = data.sort_values(by="Score", ascending=False).head(5)

    
    for index, row in top_students.iterrows():
        pdf.cell(200, 10, txt=f"{row['Name']} - {row['Score']}", ln=True)

    
    pdf_output = "student_performance_report.pdf"
    pdf.output(pdf_output)

    print(f"PDF report generated: {pdf_output}")

# Example Usage
if __name__ == "__main__":
    
    file_path = "student_scores.csv"

    
    data = read_data(file_path)

   
    avg_score, total_students, passed_students, failed_students = analyze_data(data)

    
    generate_pdf_report(file_path, avg_score, total_students, passed_students, failed_students)
