from fpdf import FPDF
import os
from analytics.stats import calculate_student_stats, calculate_class_stats

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'reports')

def generate_student_report(student_id):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    stats = calculate_student_stats(student_id)
    if not stats:
        return {"error": "No data found for this student"}
    
    class_stats = calculate_class_stats()
    
    student_rank = None
    for s in class_stats['leaderboard']:
        if s['student_id'] == student_id:
            student_rank = s['rank']
            student_percentile = s['percentile']
            break
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_fill_color(41, 128, 185)
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_xy(0, 8)
    pdf.cell(210, 10, 'Student Analytics System', align='C')
    pdf.set_font('Helvetica', '', 12)
    pdf.set_xy(0, 20)
    pdf.cell(210, 10, 'Academic Performance Report', align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(15, 45)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 8, 'Student Information')
    pdf.ln(1)
    pdf.set_draw_color(41, 128, 185)
    pdf.set_line_width(0.5)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font('Helvetica', '', 11)
    info_data = [
        ('Name', stats['name']),
        ('Roll Number', stats['roll_number']),
        ('Student ID', str(student_id)),
    ]
    
    for label, value in info_data:
        pdf.set_x(15)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(50, 7, f'{label}:')
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 7, value)
        pdf.ln()
    
    pdf.ln(5)
    pdf.set_x(15)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 8, 'Performance Summary')
    pdf.ln(1)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(6)
    
    def draw_summary_box(x, y, w, h, label, value, color):
        pdf.set_fill_color(*color)
        pdf.set_xy(x, y)
        pdf.rect(x, y, w, h, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_xy(x, y + 4)
        pdf.cell(w, 8, value, align='C')
        pdf.set_font('Helvetica', '', 9)
        pdf.set_xy(x, y + 13)
        pdf.cell(w, 6, label, align='C')
        pdf.set_text_color(0, 0, 0)
    
    box_y = pdf.get_y()
    draw_summary_box(15, box_y, 42, 24, 'Overall %', f"{stats['percentage']}%", (41, 128, 185))
    draw_summary_box(62, box_y, 42, 24, 'Grade', stats['grade'], (39, 174, 96))
    draw_summary_box(109, box_y, 42, 24, 'Class Rank', f"#{student_rank}", (142, 68, 173))
    draw_summary_box(156, box_y, 42, 24, 'Percentile', f"{student_percentile}%", (230, 126, 34))
    
    pdf.set_xy(15, box_y + 30)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 8, 'Subject-wise Performance')
    pdf.ln(1)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_fill_color(41, 128, 185)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_x(15)
    pdf.cell(70, 8, 'Subject', border=0, fill=True)
    pdf.cell(30, 8, 'Marks', align='C', border=0, fill=True)
    pdf.cell(30, 8, 'Max Marks', align='C', border=0, fill=True)
    pdf.cell(30, 8, 'Percentage', align='C', border=0, fill=True)
    pdf.cell(20, 8, 'Grade', align='C', border=0, fill=True)
    pdf.ln()
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 11)
    
    fill = False
    for subject, data in stats['subject_wise'].items():
        if fill:
            pdf.set_fill_color(235, 245, 255)
        else:
            pdf.set_fill_color(255, 255, 255)
        
        pdf.set_x(15)
        pdf.cell(70, 7, subject, border=0, fill=True)
        pdf.cell(30, 7, str(data['marks']), align='C', border=0, fill=True)
        pdf.cell(30, 7, str(data['max_marks']), align='C', border=0, fill=True)
        pdf.cell(30, 7, f"{data['percentage']}%", align='C', border=0, fill=True)
        pdf.cell(20, 7, data['grade'], align='C', border=0, fill=True)
        pdf.ln()
        fill = not fill
    
    pdf.ln(6)
    pdf.set_x(15)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 8, 'Insights')
    pdf.ln(1)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)
    
    insights = [
        f"Strongest Subject: {stats['strongest_subject']} ({stats['subject_wise'][stats['strongest_subject']]['percentage']}%)",
        f"Weakest Subject: {stats['weakest_subject']} ({stats['subject_wise'][stats['weakest_subject']]['percentage']}%)",
        f"Total Marks Scored: {stats['total_marks']} out of {stats['total_max_marks']}",
        f"Class Average: {class_stats['class_average']}% | Your Score: {stats['percentage']}%"
    ]
    
    pdf.set_font('Helvetica', '', 11)
    for insight in insights:
        pdf.set_x(15)
        pdf.set_fill_color(235, 245, 255)
        pdf.cell(180, 7, f"  {insight}", border=0, fill=True)
        pdf.ln(8)
    
    pdf.set_y(-20)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, 'Generated by Student Analytics System', align='C')
    
    filename = f"report_{stats['roll_number']}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)
    pdf.output(filepath)
    
    return {"success": True, "file": filepath, "filename": filename}