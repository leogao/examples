from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle as PS
from reportlab.platypus import PageBreak, flowables, Spacer, Table
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents, SimpleIndex
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import fonts,colors
from string import split, strip, join, whitespace, find

def HeaderFooter(canvas, doc):
    canvas.saveState()
    styleN = PS('nomal', fontName='Times-Roman', leading=9, fontSize=9)
    P = Paragraph("This is a multi-line footer or header", styleN)
    w, h = P.wrap(doc.width, doc.bottomMargin)
    #print doc.width, doc.bottomMargin
    print w, h
    #print dir(doc)
    #print dir(canvas)
    if doc.page == 1:
        footerMsg = []
        footerMsg.append(Paragraph("Lei Yang", styleN))
        footerMsg.append(Paragraph("Wei Gao", styleN))
        footerMsg.append(Paragraph("XiangYu Dong", styleN))
        footerMsg.append(Paragraph("Liang Chi", styleN))
        footerMsg.append(Paragraph("Beijing ChaoYang, China", styleN))
        canvas.line(2.5*cm, h+50, w+2.5*cm, h+50)
        f = Frame(70, 2, 16*cm, 2.1*cm, showBoundary=0)
        f.addFromList(footerMsg,canvas)
    else:
        #if flowable.__class__.__name__ == 'Paragraph':
        #    text = flowable.getPlainText()
        #    style = flowable.style.name
        P = Paragraph("User Guide", styleN)
        w, h = P.wrap(doc.width, doc.bottomMargin)
        P.drawOn(canvas, doc.leftMargin, h+789)
        canvas.line(2.5*cm, h+780, w+2.5*cm, h+780)
    canvas.restoreState()

# do First Page
def doFirstPage():
    import datetime
    format = "%Y/%m/%d %H:%M:%S"
    today = datetime.datetime.today()
    stime = today.strftime(format)
    story.append(Paragraph('Wind River Linux BSP Testing', PS('title', fontName='Times-Bold', alignment=1, leading=50, fontSize= 24)))
    story.append(Paragraph('User Guide', PS('title', fontName='Times-Bold', alignment=1, leading=60, fontSize= 24)))
    story.append(Paragraph('Version 0.1', PS('title', fontName='Times-Roman', alignment=1, leading=20, fontSize= 12)))
    story.append(Paragraph('Wei.Gao@windriver.com', PS('title', fontName='Times-Roman', alignment=1, leading=20, fontSize= 12)))
    story.append(Paragraph('Document generated on %s' % stime, PS('title', fontName='Times-Roman', alignment=1, leading=20, fontSize= 12)))
    story.append(PageBreak())

# Table of contents
def doTableOfContents():
    toc = TableOfContents()
    toc.levelStyles = [
        PS(fontName='Times-Bold', fontSize=14, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, leading=14),
        PS(fontSize=12, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, leading=12),
    ]

    story.append(Paragraph('<b>Table of contents</b>', centered))
    story.append(toc)
    story.append(PageBreak())

def doSimpleIndex():
    global index
    index = SimpleIndex(dot=' . ', headers=True)
    story.append(index)

# This function makes our headings
def doHeading(text,sty):
    from hashlib import sha1
    #create bookmarkname
    bn=sha1(text+sty.name).hexdigest()
    #modify paragraph text to include an anchor point with name bn
    h=Paragraph(text+'<a name="%s"/>' % bn,sty)
    #store the bookmark name on the flowable so afterFlowable can see this
    h._bookmarkName=bn
    story.append(h)

# Do Doc contents story
def doDocStorys():
    doHeading('Chapter 1 BootCheck', h1)
    #story.append(Spacer(1,6))
    #story.append(Paragraph('For boot testing and bootcheck', bd))
    story.append(Spacer(1,6))
    doHeading('1.1 bootcheck_pcimatch', h2)
    story.append(Spacer(1,6))
    story.append(Paragraph('Description', h3))
    story.append(Spacer(1,6))
    story.append(Paragraph('For bootcheck_pcimatch description', bd))
    story.append(Spacer(1,6))
    story.append(Paragraph('Preconditions', h3))
    story.append(Spacer(1,6))
    story.append(Paragraph('For bootcheck_pcimatch Preconditions', bd))
    story.append(Spacer(1,6))
    story.append(Paragraph('Test Step', h3))
    stylesheet=getSampleStyleSheet()
    story.append(Spacer(1,6))
    data = []
    data.append(['Test Steps','Expect Result'])
    #story.append(Spacer(1,12))
    #ts=[('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),('BOX', (0,0), (-1,-1), 0.5, colors.black),('FONT', (0,0), (-1,-1), 'Times-Bold')]
    ts=[('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BOX', (0,0), (-1,-1), 0.5, colors.green),
        ('FONT', (0,0), (-1,-1), 'Times-Bold'),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black)]

    table = Table(data, 220, 18, ts)
    story.append(table)

    data = []
    data.append(['xxxxxxxxxxxxx','Successfully'])
    #ts=[('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),('BOX', (0,0), (-1,-1), 0.5, colors.green),('FONT', (0,0), (-1,-1), 'Times-Roman')]
    ts=[('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BOX', (0,0), (-1,-1), 0.5, colors.green),
        ('FONT', (0,0), (-1,-1), 'Times-Bold'),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black)]
    table = Table(data, 220, 180, ts)
    story.append(table)
    story.append(Spacer(1,6))
    story.append(Paragraph('NOTE', h3))
    story.append(Spacer(1,6))
    story.append(Paragraph('For bootcheck_pcimatch NOTE', bd))
    story.append(Spacer(1,20))

# Body contents

class DocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        frame1 = Frame(2.5*cm, 2.5*cm, 16*cm, 25*cm, id='F1')
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('nomal', [frame1], onPageEnd=HeaderFooter)
        #template = PageTemplate('nomal', [Frame(2.5*cm, 2.5*cm, 16*cm, 25*cm, id='F1')], onPageEnd=HeaderFooter)
        #template = PageTemplate('nomal', [Frame(2.5*cm, 2.5*cm, 16*cm, 25*cm, id='F1', showBoundary=1)], onPageEnd=HeaderFooter)
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                level = 0
            elif style == 'Heading2':
                level = 1
            else:
                return
            E = [level, text, self.page]
            #if we have a bookmark name append that to our notify data
            bn = getattr(flowable,'_bookmarkName',None)
            if bn is not None: E.append(bn)
            self.notify('TOCEntry', tuple(E))

            # Add PDF outline entries (not really needed/tested here).
            key = str(hash(flowable))
            c = self.canv
            c.bookmarkPage(key)
            c.addOutlineEntry(text, key, level=level, closed=0)

            # index a bunch of pythonic buzzwords.  In real life this
            # would be driven by markup.
            for phrase in ['uniform','depraved','finger', 'Fraudulin']:
                if find(text, phrase) > -1:
                    self.notify('IndexEntry', (phrase, self.page))

# Main 
delta = 15.8
centered = PS(name = 'centered',
    fontSize = 20,
    leading = 16,
    alignment = 1,
    spaceAfter = 20)
h1 = PS(name = 'Heading1',
    fontName='Times-Bold',
    fontSize = 14,
    alignment = 1,
    leading = 16)
h2 = PS(name = 'Heading2',
    fontName='Times-Bold',
    fontSize = 12,
    leading = 14)
#,
#    leftIndent = delta)
h3 = PS(name = 'Heading3',
    fontName='Times-Bold',
    fontSize=10,
    leading=12)

bd = PS(name = 'body')

# Build story.
story = []
doFirstPage()
doTableOfContents()
#doSimpleIndex()
doDocStorys()
story.append(SimpleIndex())

doc = DocTemplate('mintoc.pdf')
doc.multiBuild(story)
