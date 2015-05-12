#!/usr/bin/env python

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle as PS
from reportlab.platypus import PageBreak, flowables, Spacer, Table
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents, SimpleIndex
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib import fonts,colors
from optparse import OptionParser
from string import find
from commands import getoutput
import sys
import os
import commands

def HeaderFooter(canvas, doc):
    canvas.saveState()
    styleN = PS('nomal', fontName='Times-Roman', leading=9, fontSize=9)
    P = Paragraph("This is a multi-line footer or header", styleN)
    w, h = P.wrap(doc.width, doc.bottomMargin)
    #print doc.width, doc.bottomMargin
    #print w, h
    #print dir(doc)
    #print dir(canvas)
    global pageNum
    if doc.page < pageNum:
        global ChapterName
        ChapterName = 'Table of contents'

    #print doc.page
    #print ChapterName
    pageNum = doc.page

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
        P = Paragraph("User Guide", styleN)
        w, h = P.wrap(doc.width, doc.bottomMargin)
        P.drawOn(canvas, doc.leftMargin, h+789)
        P = Paragraph(ChapterName, PS('nomal', fontName='Times-Roman', fontSize=9, alignment = TA_RIGHT, leading=9))
        w, h = P.wrap(doc.width, doc.bottomMargin)
        P.drawOn(canvas, doc.rightMargin, h+789)

        P = Paragraph("Page %d" % doc.page, PS('nomal', fontName='Times-Roman', fontSize=9, alignment = 1))
        w, h = P.wrap(doc.width, doc.bottomMargin)
        P.drawOn(canvas, doc.leftMargin, h)
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
    text = 'Table of contents'
    doHeading( text, PS(name = 'Heading1', fontName='Times-Bold', fontSize = 18, alignment = 1, leading = 16 ))
    story.append(Spacer(1,6))
    story.append(toc)
    story.append(PageBreak())

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
def doStoryChapter( chapter_name ):
    doHeading( chapter_name, h1)
    #story.append(Spacer(1,6))
    #story.append(Paragraph('For boot testing and bootcheck', bd))
    story.append(Spacer(1,6))

def doStoryContent( dict_r=None ):
    if dict_r is None:
        return
    doHeading(dict_r['part_name'], h2)
    story.append(Spacer(1,6))
    story.append(Paragraph('Description', h3))
    story.append(Spacer(1,6))
    story.append(Paragraph(dict_r['description'], bd))
    story.append(Spacer(1,6))
    story.append(Paragraph('Precondition', h3))
    story.append(Spacer(1,6))
    story.append(Paragraph(dict_r['precondition'], bd))
    story.append(Spacer(1,6))
    story.append(Paragraph('Test Steps', h3))
    stylesheet=getSampleStyleSheet()
    story.append(Spacer(1,6))
    data = []
    data.append(['Test Steps','Expect Result'])
    ts=[('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BOX', (0,0), (-1,-1), 0.5, colors.green),
        ('FONT', (0,0), (-1,-1), 'Times-Bold'),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black)]

    table = Table(data, 220, 18, ts)
    story.append(table)

    data = []
    lines_a = len(dict_r['steps'].split('\n'))
    lines_b = len(dict_r['results'].split('\n'))
    lines = lines_a if lines_a > lines_b else lines_b
    data.append([dict_r['steps'], dict_r['results']])
    ts=[('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BOX', (0,0), (-1,-1), 0.5, colors.green),
        ('FONT', (0,0), (-1,-1), 'Times-Roman'),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black)]
    table = Table(data, 220, 12*lines, ts)
    story.append(table)
    story.append(Spacer(1,6))
    if dict_r.has_key('notes'):
        story.append(Paragraph('NOTE', h3))
        story.append(Spacer(1,6))
        story.append(Paragraph(dict_r['notes'], bd))
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
                global ChapterName
                ChapterName = text
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

def get_home_dir():
    current_dir = os.getcwd()
    home_dir = commands.getoutput("echo %s |awk -Fwr-testing '{print $1}'" %current_dir)
    return home_dir

def get_testcase_dir(domain,testcase):
    testcase_dir = commands.getoutput('find %s/wr-testing/%s -name %s' %(home_dir,domain,testcase))
    for i in testcase_dir.split():
        if os.path.isfile('%s/test.cfg' %i):
            return os.path.abspath(i)
    else:
        return None

def get_all_testcase_feature(domain):
    all_testcase_feature = {}
    for cfg in commands.getoutput('find %s/wr-testing/%s -name test.cfg' %(home_dir,domain)).split():
	feature = commands.getoutput("cat %s |awk -F'=| ' '/Feature/{print $NF}'" %cfg)
        testcase_dirname = os.path.split(cfg)[0]
        testcase_name = os.path.basename(testcase_dirname)
	readme = '%s/README' %testcase_dirname
        if os.path.isfile(readme):
             all_testcase_feature[testcase_name]=feature
    return all_testcase_feature

def get_feature_testcase(domain):
    global feature
    feature = []
    feature_testcase = {} 
    all_testcase_feature = get_all_testcase_feature(domain)
    for i in all_testcase_feature:
	feature.append(all_testcase_feature[i])
    feature=list(set(feature))
    feature=sorted(filter(None,feature))
    for elem_f in feature:
	feature_testcase[elem_f]=[]
        for elem_t in all_testcase_feature:
            if all_testcase_feature[elem_t] == elem_f:
                 feature_testcase[elem_f].append(elem_t)
	feature_testcase[elem_f] = sorted(feature_testcase[elem_f])
    return feature,feature_testcase

def get_doman_readme():
    global home_dir
    home_dir=get_home_dir()
    domain='bts-dev'
    readme = commands.getoutput('find %s/wr-testing/%s -maxdepth 1 -name README' %(home_dir,domain))
    ptitles = ['BTS: Wind River BSP testing layer','Dependencies','Maintenance','Building the BTS layer','License']
    readme_list = []
    readme_list.append(getoutput("sed -n '/BTS:/,/Dependencies/p' %s |sed '$d' |sed '1,2d'" %readme))
    readme_list.append(getoutput("sed -n '/Dependencies/,/Maintenance/p' %s |sed '$d' |sed '1,2d'" %readme))
    readme_list.append(getoutput("sed -n '/Maintenance/,/Building the BTS layer/p' %s |sed '$d' |sed '1,2d'" %readme))
    readme_list.append(getoutput("sed -n '/Building the BTS layer/,/License/p' %s |sed '$d' |sed '1,2d'" %readme))
    readme_list.append(getoutput("sed '1,/License/d' %s |sed '1d'" %readme))

    chapter_name = 'Chapter 1 Introduction'
    doStoryChapter(chapter_name)

    i = 0
    for elem in ptitles:
        story.append(Paragraph(elem, h3))
        story.append(Spacer(1,6))
        story.append(Paragraph(readme_list[i], bd))
        story.append(Spacer(1,6))
        i += 1

def format_box_contents( contents ):
    r_str = ''
    chars = 49
    #width = 194
    #styb = PS('nomal', fontName='Times-Roman')
    s_list = contents.replace('\\','').split('\n')
    for elem in s_list:
        ielem = elem
    #    P = Paragraph(ielem, styb)
    #    while P.minWidth() > width:
        while len(ielem) >= chars:
            if ielem[:chars].rfind(' ') > 40:
                ri = ielem[:chars].rfind(' ')
                r_str += ielem[:ri+1].lstrip() + '\n'
                ielem = ielem[ri+1:].lstrip()
            elif ielem[:chars].rfind('/') > 39:
                ri = ielem[:chars].rfind('/')
                r_str += ielem[:ri+1] + '\n'
                ielem = ielem[ri+1:]
            elif ielem[:chars].rfind('_') > 30:
                ri = ielem[:chars].rfind('_')
                r_str += ielem[:ri+1] + '\n'
                ielem = ielem[ri+1:]
            elif ielem[:chars].rfind(' ') > 20:
                ri = ielem[:chars].rfind(' ')
                r_str += ielem[:ri+1].lstrip() + '\n'
                ielem = ielem[ri+1:].lstrip()
            else:
                break
#            P = Paragraph(ielem, styb)
        r_str += ielem.lstrip() + '\n'
    return r_str

def get_tests_readme_dic():
    global home_dir
    home_dir=get_home_dir()
    domain='bts-dev'
    global testcase_readme_dic
    testcase_readme_dic={}
    readme_dic = {}
    global feature_testcase
    feature,feature_testcase = get_feature_testcase(domain)
    j=0
    for cfg in sorted(commands.getoutput('find %s/wr-testing/%s -name test.cfg' %(home_dir,domain)).split()):
        j=j+1
        testcase_dirname = os.path.split(cfg)[0]
        #print testcase_dirname
        testcase_name = os.path.basename(testcase_dirname)
        readme = '%s/README' %testcase_dirname
        #print readme
        if os.path.isfile(readme):
            readme_dic = {} 
            readme_dic['description'] = getoutput("sed -n '/Description/,/Preconditions/p' %s |sed '$d' |sed '1,2d'" %readme) 
            readme_dic['precondition'] = getoutput("sed -n '/Preconditions/,/Test Steps/p'  %s |sed '$d' |sed '1,2d'" %readme) 
            readme_dic['steps'] = format_box_contents(getoutput("sed -n '/Test Steps/,/Expects Results/p' %s |sed '$d' |sed '1,2d'" %readme))
            readme_dic['results'] = format_box_contents(getoutput("sed -n '/Expects Results/,/References/p' %s |sed '$d' |sed '1,2d'" %readme))
            print str(readme_dic['steps'])
            print str(readme_dic['results'])
            readme_dic['refernence'] = getoutput("sed -n '/References/,/Notes/p' %s |sed '$d' |sed '1,2d'" %readme) 
            readme_dic['notes'] = getoutput("sed '1,/Notes/d' %s |sed '1d'" %readme) 
            testcase_readme_dic[testcase_name] = readme_dic

# Main 
def main():
    global story
    global h1
    global h2
    global h3
    global bd
    global ChapterName
    global pageNum
    ChapterName = 'Table of contents'
    pageNum = 0
    delta = 15.8
    h1 = PS(name = 'Heading1',
        fontName='Times-Bold',
        fontSize = 14,
        alignment = 1,
        leading = 16)
    h2 = PS(name = 'Heading2',
        fontName='Times-Bold',
        fontSize = 12,
        leading = 14)
    h3 = PS(name = 'Heading3',
        fontName='Times-Bold',
        fontSize=10,
        leading=12)

    bd = PS(name = 'body')

    # Build story.
    story = []
    doFirstPage()
    doTableOfContents()
    get_doman_readme()
    get_tests_readme_dic()

    chapter_i = 1
    for elem_f in feature:
        chapter_i += 1
        chapter_name = 'Chapter %d '%chapter_i + elem_f
        doStoryChapter(chapter_name)
        dict_r = {}
        part_i = 0
        for name in feature_testcase[elem_f]:
            part_i += 1
            part_name = '%d.%d '%(chapter_i,part_i) + name
            dict_r = testcase_readme_dic[name]
            dict_r['part_name'] = part_name
            doStoryContent(dict_r=dict_r)
    story.append(SimpleIndex())

    doc = DocTemplate('Wind River Linux BSP Testing User Guide.pdf')
    doc.multiBuild(story)

if __name__ == "__main__":
    main()
