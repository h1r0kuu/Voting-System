from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont   
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import Color 
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import User, Vote
from django.http import HttpResponse

def generate_pdf_report(voting):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{voting.title}_report.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont('Verdana', 24)
    # Draw a red rectangle for the title
    # c.setFillColor(colors.red)
    # c.rect(0, 10 * inch, 8.5 * inch, 1 * inch, fill=True)

    # c.setFillColor(colors.white)
    # c.setFont("Helvetica-Bold", 24)
    # c.drawCentredString(4.25 * inch, 10.35 * inch, voting.title.upper())

     # Define a style for the title and description
    title_style = ParagraphStyle('Title', parent=getSampleStyleSheet()['Title'], fontSize=24, spaceAfter=12)
    description_style = getSampleStyleSheet()['BodyText']

    # Create Paragraph objects for the title and description
    title_lines = voting.title
    title = Paragraph(voting.title, title_style)
    description = Paragraph(voting.description, description_style)

    # Calculate the required height for the title and description
    title_height = title.wrap(8.5 * inch, 10 * inch)[1]
    description_height = description.wrap(8.5 * inch, 10 * inch)[1]
    title_lines = len(title.blPara.lines)

    # Draw a red rectangle for the title and description
    c.setFillColor(colors.red)
    c.rect(0, (10 - title_lines / 3.5) * inch, 8.5 * inch, (title_lines / 0.5) * inch, fill=True)

    # Draw the title and description text
    title.drawOn(c, 0, 10 * inch)
    # description.drawOn(c, 0, 10 * inch)

    # ...


    styles = getSampleStyleSheet()
    styles['Normal'].alignment = TA_CENTER
    description = Paragraph(voting.description, styles['Normal'])

    total_users = User.objects.count()
    voted_users = voting.vote_set.count()
    gained_quorum = int((voted_users / total_users) * 100)
    success = f'Yes {gained_quorum}%' if gained_quorum >= voting.quorum else f'No {gained_quorum}%'

    data = [
        ["Description", description],
        ["Voting Type", voting.get_voting_type_display()],
        ["Quorum", f"{voting.quorum}%"],
        ["Creator", voting.creator.username],
        ["Voting successful", success],
        ["Start Time", voting.start_time.strftime('%Y-%m-%d %H:%M:%S')],
        ["End Time", voting.end_time.strftime('%Y-%m-%d %H:%M:%S')],
        ["Created At", voting.created_at.strftime('%Y-%m-%d %H:%M:%S')],
    ]

    if voting.voting_type == 'U':
        data.append(["Relative Majority", voting.usualvoting.relative_majority])

    table = Table(data, colWidths=[3 * inch, 5.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), Color(255, 0, 0, 0.1)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), Color(255, 0, 0, 0.1)),
        ('GRID', (0,0), (-1,-1), 1, colors.red)
    ]))

    # Draw the table on the canvas
    table.wrapOn(c, 0, 0)
    table.drawOn(c, 0, (7.68 - title_lines / 1.5) * inch)

    if voting.voting_type == 'U':
        usual_voting = voting.usualvoting
        # c.drawString(1 * inch, 7.5 * inch, f"Relative Majority: {usual_voting.relative_majority}")

        votes = [(Vote.objects.filter(voting=voting, vote_option_for_usual=vote_choice[0]).count(), vote_choice[1]) for vote_choice in Vote.VOTE_CHOICES]

        # Sort this list in descending order based on the vote count
        votes.sort(reverse=True, key=lambda x: x[0])

        # # Split this sorted list back into two lists: one for the vote counts and one for the labels
        votes_data, votes_labels = zip(*votes)

        d = Drawing(200, 200)
        pie = Pie()
        pie.x = 20
        pie.y = 70
        pie.width = 100
        pie.height = 100
        pie.data = votes_data
        pie.labels = ['Tak', 'Nie', 'Wstrzymuje się']
        pie.slices.popout = 3
        d.add(pie)

        legend = Legend()
        legend.x = 220
        legend.y = 145
        legend.colorNamePairs = [(pie.slices[i].fillColor, f"{pie.labels[i]}: {pie.data[i]}%") for i in range(len(pie.data))]
        legend.dx = 8
        legend.dy = 8
        legend.yGap = 0
        legend.strokeWidth = 0
        legend.columnMaximum = len(pie.data)
        legend.alignment ='right'
        d.add(legend)


        renderPDF.draw(d, c, 2 * inch, (5 - title_lines) * inch)
    elif voting.voting_type == 'O':
        optional_voting = voting.get_specific_vote()
        options = optional_voting.voting_options.all()

         # Create a list of tuples where each tuple contains the vote count and the corresponding label
        votes = [(Vote.objects.filter(voting=voting, option=option).count(), option.option_value) for option in options]

        # Sort this list in descending order based on the vote count
        votes.sort(reverse=True, key=lambda x: x[0])

        # Split this sorted list back into two lists: one for the vote counts and one for the labels
        votes_data, votes_labels = zip(*votes)

        d = Drawing(200, 200)
        pie = Pie()
        pie.x = 20
        pie.y = 70
        pie.width = 100
        pie.height = 100
        pie.data = votes_data
        pie.labels = votes_labels
        pie.slices.popout = 3  # Make all slices pop out
        winner_index = votes_data.index(max(votes_data))
        pie.slices[winner_index].popout = 4
        d.add(pie)

         # Add a legend
        legend = Legend()
        legend.x = 220
        legend.y = 165
        legend.colorNamePairs = [(pie.slices[i].fillColor, f"{pie.labels[i]}: {pie.data[i]}%") for i in range(len(pie.data))]
        legend.dx = 8
        legend.dy = 8
        legend.yGap = 0
        legend.strokeWidth = 0
        legend.columnMaximum = len(pie.data)
        legend.alignment ='right'
        d.add(legend)

        renderPDF.draw(d, c, 2 * inch, (5 - title_lines) * inch)

    c.save()

    return response