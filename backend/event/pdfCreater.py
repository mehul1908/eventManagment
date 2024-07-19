from reportlab.pdfgen import canvas

from reportlab.lib import colors


from models import Event


def createPdf():
	fileName = 'sample.pdf'
	documentTitle = 'sample document title'
	title = 'sample title'
	subTitle = 'sample sub title'
	textLines =[
		'line 1 ... .... ... ... ...',
		'line 2 .... .... .... ....'
	]
	pdf = canvas.Canvas(fileName)
	pdf.setTitle(documentTitle)
	pdf.setFont("Courier-Bold" , 36)
	pdf.drawCentredString(300,770 , title)
	pdf.setFillColorRGB(0, 0, 255) 
	pdf.setFont("Courier-Bold", 24) 
	pdf.drawCentredString(290, 720, subTitle)
	pdf.line(30, 710, 550, 710) 
	text = pdf.beginText(40, 680) 
	text.setFont("Courier", 18) 
	text.setFillColor(colors.red) 
	for line in textLines: 
		text.textLine(line) 
	pdf.drawText(text) 
	pdf.save()

def pdfWelcome(eventId=None , attendeeId=None):
	fileName = 'welcome.pdf'
	documentTitle = 'Congratulation , You have enrolled in the Event'
	title = eventId.eventName
	# title = "abcdefghijklmnopqrstuvwxyzabcdefghikjlmo"
	subTitle = "Congratulation , You have enrolled in the Event"
	pdf = canvas.Canvas(fileName)
	pdf.setTitle(documentTitle)
	pdf.setFont("Courier-Bold" ,24)
	pdf.drawCentredString(300,770 , title)
	pdf.setFillColorRGB(0, 0, 255) 
	pdf.setFont("Courier-Bold", 18) 
	pdf.drawCentredString(290, 720, subTitle)
	pdf.line(30, 710, 550, 710)
	
	pdf.drawCentredString(290 , 700 , "Event Detail")
	text = pdf.beginText(40, 680) 
	text.setFont("Courier", 18) 
	text.setFillColor(colors.black) 

	
	text.textLine(f'Date and Time : {eventId.time.strftime("%B %d, %Y  %H:%M:%S")}')
	text.textLine(f'Venue : {eventId.venue}')
	pdf.drawText(text) 

	pdf.line(30 , 650 , 550 , 650)

	
	pdf.save()

pdfWelcome(Event.objects.get(pk=1))
