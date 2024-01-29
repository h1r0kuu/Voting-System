from typing import Union, List

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont   
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
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import Voting, Vote
from django.http import HttpResponse
from django.contrib.staticfiles import finders
from django.db.models import QuerySet

TOP_MARGIN = 10

class RaportPDF:
    def __init__(self, voting):
        self.voting: Voting = voting
        self.response = HttpResponse(content_type='application/pdf; charset=utf-8')
        self.response['Content-Disposition'] = f'attachment; filename="report_{voting.title}.pdf"'
        self.canvas = canvas.Canvas(self.response, pagesize=letter)
        self.step = 0
        self.votes: Union[QuerySet, List[Vote]] = voting.vote_set.all()
        self.sorted_votes = self.voting.get_votes_percentages()

        pdfmetrics.registerFont(TTFont('DejaVuSans', finders.find("fonts/DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', finders.find("fonts/DejaVuSans-Bold.ttf")))
        self.canvas.setFont("DejaVuSans", 8)

    def sort_votes(self):
        list_of_votes = self.votes
        votes_count = self.votes.count()
        if len(list_of_votes) > 0:
            if self.voting.voting_type == 'U':
                list_of_votes = [
                    (
                        round((list_of_votes.filter(vote_option_for_usual=vote_choice[0]).count() * 100) / votes_count),
                        vote_choice[1]
                    )
                        for vote_choice in Vote.VOTE_CHOICES
                ]
            elif self.voting.voting_type == 'O':
                options = self.voting.votingoption_set.all()
                list_of_votes = [
                    (
                        round((list_of_votes.filter(option=option).count() * 100) / votes_count), 
                        option.option_value
                    )
                    for option in options
                ]
            list_of_votes.sort(reverse=True, key=lambda x: x[0])
        return list_of_votes

    def generate_title(self):
        title_style = ParagraphStyle('Title', parent=getSampleStyleSheet()['Title'], fontSize=24, spaceAfter=12, textColor='white', fontName='DejaVuSans')
        title_paragraph = Paragraph(self.voting.title, title_style)

        _, th = title_paragraph.wrap(8.5 * inch, 10 * inch)
        self.step = (th + 3 * TOP_MARGIN)
        rect_height, rect_width = self.step, letter[0]
        rect_x_position, rect_y_position = 0, letter[1] - rect_height

        title_x_position, title_y_position = 0, letter[1] - (TOP_MARGIN + th)

        self.canvas.setFillColor(colors.red)
        self.canvas.rect(rect_x_position, rect_y_position, rect_width, rect_height, fill=True)

        title_paragraph.drawOn(self.canvas, title_x_position, title_y_position)

    def generate_table(self):
        description_style = getSampleStyleSheet()['BodyText']
        description_style.fontName='DejaVuSans'
        description = Paragraph(self.voting.description, description_style)
        dw, dh = description.wrap(8.5 * inch, 10 * inch)
    
        current_quorum = self.voting.current_quorum
        voting_result = self.voting.get_result()['winner']

        data = [
            ["Opis", description],
            ["Typ głosowania", self.voting.get_voting_type_display()],
            ["Wymagany kworum", f"{self.voting.quorum} %"],
            ["Bieżący kworum", f"{current_quorum} %"],
            ["Twórca", f'{self.voting.creator.username} ({self.voting.creator.get_full_name()})' ],
            ["Czas rozpoczęcia", self.voting.start_time.strftime('%Y-%m-%d %H:%M:%S')],
            ["Czas zakończenia", self.voting.end_time.strftime('%Y-%m-%d %H:%M:%S')],
            ["Czas utworzenia", self.voting.created_at.strftime('%Y-%m-%d %H:%M:%S')],
            ["Wygrana opcja", str(voting_result)],
        ]

        if self.voting.voting_type == 'U':
            data.append(["Większość bezwzględna", self.voting.relative_majority])

        table = Table(data, colWidths=[3 * inch, 5.5 * inch])
        table.setStyle(TableStyle([
            ('TEXTFONT', (0, 0), (-1, -1), 'DejaVuSans'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),

            ('BACKGROUND', (0, 0), (-1, 0), Color(255, 0, 0, 0.1)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), Color(255, 0, 0, 0.1)),
            ('GRID', (0,0), (-1,-1), 1, colors.red),

            # row - Wygrana opcja
            ('FONTNAME', (0, 8), (1, 8), "DejaVuSans-Bold"),
        ]))
        _, th = table.wrapOn(self.canvas, 0, 0)
        self.step += th
        table.drawOn(self.canvas, 0, letter[1] - self.step)
    
    def generate_chart(self):
        CHART_WIDTH = CHART_HEIGHT = 200
        self.step += CHART_HEIGHT
        drawing = Drawing(CHART_WIDTH, CHART_HEIGHT)
        if self.voting.voting_type == 'U':
            votes_data, votes_labels = zip(*self.sorted_votes)
            print(votes_data)
            print(votes_labels)
            pie = Pie()
            pie.x = 20
            pie.y = 70
            pie.width = 100
            pie.height = 100
            pie.data = votes_data
            pie.labels = votes_labels
            pie.slices.fontName='DejaVuSans'
            pie.slices.popout = 3
            drawing.add(pie)

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
            legend.fontName='DejaVuSans'
            drawing.add(legend)

        elif self.voting.voting_type == 'O':
            votes_data, votes_labels = zip(*self.sorted_votes)

            pie = Pie()
            pie.x = 20
            pie.y = 70
            pie.width = 100
            pie.height = 100
            pie.data = votes_data
            pie.labels = votes_labels
            pie.slices.popout = 3
            pie.slices.fontName='DejaVuSans'
            winner_index = votes_data.index(max(votes_data))
            pie.slices[winner_index].popout = 4
            drawing.add(pie)

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
            legend.fontName='DejaVuSans'
            drawing.add(legend)

        renderPDF.draw(drawing, self.canvas, 2 * inch, letter[1] - self.step)

    def generate_pdf(self):
        self.generate_title()
        self.generate_table()
        if(self.votes.count() > 0):
            self.generate_chart()
        self.canvas.save()

        return self.response
