
from reportlab.pdfgen import canvas

lyrics = ['well she hit Net Solutions', \
'and she registered her own .com site now', \
'and filled it up with yahoo profile pics', \
'she snarfed in one night now', \
'and she made 50 million when Hugh Hefner', \
'bought up the rights now', \
'and she\'ll have fun fun fun', \
'til her Daddy takes the keyboard away']

def textsize(canvas):
    from reportlab.lib.units import inch
    from reportlab.lib.colors import magenta, red
    canvas.setFont("Times-Roman", 20)
    canvas.setFillColor(red)
    canvas.drawCentredString(2.75*inch, 2.5*inch, "Font size examples")
    canvas.setFillColor(magenta)
    size = 7
    y = 2.3*inch
    x = 1.3*inch
    for line in lyrics:
        canvas.setFont("Helvetica", size)
        canvas.drawRightString(x,y,"%s points: " % size)
        canvas.drawString(x,y, line)
        y = y-size*1.2
        size = size+1.5


c = canvas.Canvas("hello.pdf")
textsize(c)
c.showPage()
c.save()

