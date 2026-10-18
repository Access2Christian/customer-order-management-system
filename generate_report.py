"""
Automated Academic Report Document Builder for SEN 306.
Compiles professional structural layout and embeds local image figures into a PDF.
Author: Christian Chijioke Nnaji
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_report():
    pdf_filename = "SEN306_TMA_Report.pdf"
    
    # Initialize document parameters with safe printable margins
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                            rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Academic Typography & Style Palettes
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1A365D'),
        alignment=1, # Centered
        spaceAfter=12
    )
    
    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontSize=10,
        leading=15,
        spaceAfter=8
    )

    caption_style = ParagraphStyle(
        'ImgCaption',
        parent=styles['Italic'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#4A5568'),
        alignment=1, # Centered
        spaceAfter=14
    )

    # Header Panel Representation
    story.append(Paragraph("<b>MIVA OPEN UNIVERSITY</b>", title_style))
    story.append(Paragraph("<b>Department of Software Engineering</b>", ParagraphStyle('Sub', alignment=1, fontSize=11, textColor=colors.HexColor('#4A5568'), spaceAfter=12)))
    
    meta_box = """
    <b>Course Code:</b> SEN 306 — Software Construction<br/>
    <b>Assessment Type:</b> Tutor-Marked Assessment (Individual Work)<br/>
    <b>Student Name:</b> Christian Chijioke Nnaji | <b>Reg No:</b> 2024/B/SENG/0246 | <b>ID:</b> 30037606<br/>
    <b>Date:</b> October 18, 2026
    """
    story.append(Paragraph(meta_box, body_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>PROJECT REPORT: CUSTOMER ORDER & SUPPORT MANAGEMENT SYSTEM</b>", ParagraphStyle('SubT', alignment=1, fontSize=12, textColor=colors.HexColor('#1A365D'), spaceAfter=10)))
    story.append(Spacer(1, 5))

    # Internal helper function to embed local assets safely
    def add_screenshot_figure(filename, caption_text):
        if os.path.exists(filename):
            try:
                img = Image(filename, width=340, height=190)
                story.append(img)
                story.append(Paragraph(caption_text, caption_style))
                story.append(Spacer(1, 5))
            except Exception:
                story.append(Paragraph(f"<i>[Error: Processing failed for graphic template asset '{filename}']</i>", caption_style))
        else:
            story.append(Paragraph(f"<i>[Missing Visual Verification: Place '{filename}' in folder to embed screenshot]</i>", caption_style))

    # Section 1
    story.append(Paragraph("1. Executive Summary & Task Overview", h2_style))
    exec_p = """
    The goal of this project was to design and construct a modular, real-life Customer Order Processing and Support 
    Management application demonstrating the practical integration of three core data structures: a <b>Queue</b>, a 
    <b>Singly Linked List</b>, and a <b>Stack</b>. To adhere to strict software construction standards, no built-in Python 
    collection array helper methods (such as native list extensions) were used for data storage or tracking configurations. 
    Every single layer was written from scratch using a node-based pointer connection structure.<br/><br/>
    The codebase is split into clean modules (<code>queue_module.py</code>, <code>linkedlist.py</code>, <code>stack.py</code>, 
    and <code>main.py</code>) to fulfill professional design abstractions, decouple software logic, and enforce high maintainability.<br/><br/>
    <b>Remote Assignment Delivery Links:</b><br/>
    • GitHub Source Code Link: <u>https://github.com/Access2Christian/customer-order-management-system.git</u><br/>
    • Google Drive Institutional Cloud Share: <u>https://drive.google.com/drive/folders/1pSo8X8BwN5-3MMcPNWQij9KXC6ssh8vG?usp=sharing</u>
    """
    story.append(Paragraph(exec_p, body_style))
    add_screenshot_figure("fig1.png", "Figure 1: Version control deployment pipeline verification sync (Git Push to Remote Main Branch)")

    # Section 2
    story.append(Paragraph("2. Functional Mapping of Data Structures", h2_style))
    ds_p = """
    • <b>Queue (FIFO):</b> Serves as the <i>Inbound Order Intake Pipeline</i>. Checkout events are appended using <code>enqueue()</code> at the rear boundary and extracted via <code>dequeue()</code> from the front, ensuring customer orders are processed in strict chronological arrival sequence.<br/>
    • <b>Singly Linked List:</b> Serves as the persistent <i>Active Orders Catalog Database</i>. It navigates reference pointer structures linearly, allowing custom runtime logic to look up records or handle target link extractions securely without fragmenting data chains.<br/>
    • <b>Stack (LIFO):</b> Serves as the atomic <i>Undo Transaction Ledger</i>. Every mutation operation (insertions, flag updates, deletions) pushes state snapshots onto the top-level pointer. Popping an item from the stack rolls back variations safely.
    """
    story.append(Paragraph(ds_p, body_style))
    add_screenshot_figure("fig2.png", "Figure 2: Inbound order intake pipeline processing simulation (Option 1: Enqueue)")
    add_screenshot_figure("fig3.png", "Figure 3: Pipeline verification tracking routine (Option 2: Dequeue to Database Catalog)")

    # Section 3
    story.append(Paragraph("3. Application of Software Construction Principles", h2_style))
    principles_p = """
    • <b>Modular Design:</b> Architecture decouples data containment components cleanly away from runtime presentation logic.<br/>
    • <b>High Cohesion:</b> Classes implement single-purpose operational tracking methods (e.g., node reference shuffling rules).<br/>
    • <b>Low Coupling:</b> Submodules use native Python parameter models with no interdependencies or internal cross-imports.<br/>
    • <b>Defensive Validation:</b> Robust evaluation loops intercept non-numeric amounts, missing fields, or duplicate identifiers.
    """
    story.append(Paragraph(principles_p, body_style))
    add_screenshot_figure("fig4.png", "Figure 4: Data field entry adjustment tracking initialization (Option 4: Update order status flags)")
    add_screenshot_figure("fig4_b.png", "Figure 4b: Data mutation confirmation — Order status changed successfully to Delivered")
    add_screenshot_figure("fig5.png", "Figure 5: Active memory list database evaluation layer (Option 8: Active orders catalog look)")

    # Section 4
    story.append(Paragraph("4. Operational Test Execution Evidence", h2_style))
    story.append(Paragraph("Empirical terminal screenshots documenting state removal mutations and stack recovery transformations:", body_style))
    
    add_screenshot_figure("fig6.png", "Figure 6: Destructive catalog removal tracking operation (Option 5: Remove order)")
    add_screenshot_figure("fig7.png", "Figure 7: System rollback execution state analysis (Option 6: Undo last action)")
    add_screenshot_figure("fig8.png", "Figure 8: Quantitative operational metrics administrative overview dashboard (Option 10)")

    # Generate document layout structure
    doc.build(story)
    print("\n" + "="*60)
    print("🎉 Success! Beautifully formatted report compiled locally as 'SEN306_TMA_Report.pdf'.")
    print("="*60 + "\n")

if __name__ == "__main__":
    create_report()
