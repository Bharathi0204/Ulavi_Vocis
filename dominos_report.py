from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPDF
import os

# ─── BRAND COLORS ────────────────────────────────────────────────────────────
DOMINOS_RED   = colors.HexColor("#E31837")
DOMINOS_BLUE  = colors.HexColor("#006491")
DARK_BG       = colors.HexColor("#1A1A2E")
ACCENT_GOLD   = colors.HexColor("#F5A623")
LIGHT_GREY    = colors.HexColor("#F4F6F9")
MID_GREY      = colors.HexColor("#C8CDD5")
DARK_TEXT     = colors.HexColor("#1C1C1E")
WHITE         = colors.white
SECTION_BG    = colors.HexColor("#EEF3F8")
TABLE_HEADER  = colors.HexColor("#006491")
TABLE_ALT     = colors.HexColor("#F0F5FA")

W, H = A4

# ─── PAGE TEMPLATE ────────────────────────────────────────────────────────────
def make_canvas(c, doc):
    c.saveState()
    # Top bar
    c.setFillColor(DOMINOS_BLUE)
    c.rect(0, H - 18*mm, W, 18*mm, fill=1, stroke=0)
    # Red accent strip
    c.setFillColor(DOMINOS_RED)
    c.rect(0, H - 22*mm, W, 4*mm, fill=1, stroke=0)
    # Bottom bar
    c.setFillColor(DOMINOS_BLUE)
    c.rect(0, 0, W, 12*mm, fill=1, stroke=0)
    c.setFillColor(DOMINOS_RED)
    c.rect(0, 12*mm, W, 2*mm, fill=1, stroke=0)

    # Header text
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(WHITE)
    c.drawString(1.2*cm, H - 13*mm, "DOMINO'S PIZZA")
    c.setFont("Helvetica", 8)
    c.drawRightString(W - 1.2*cm, H - 13*mm, "Franchise Business Analysis Report")

    # Footer text
    c.setFont("Helvetica", 7.5)
    c.setFillColor(WHITE)
    c.drawString(1.2*cm, 4.5*mm, "© 2024 Franchise Intelligence Report | Confidential")
    c.drawRightString(W - 1.2*cm, 4.5*mm, f"Page {doc.page}")

    c.restoreState()

def cover_canvas(c, doc):
    c.saveState()
    # Full dark background
    c.setFillColor(DARK_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Top red stripe
    c.setFillColor(DOMINOS_RED)
    c.rect(0, H - 6*mm, W, 6*mm, fill=1, stroke=0)
    # Bottom section bg
    c.setFillColor(DOMINOS_BLUE)
    c.rect(0, 0, W, 7*cm, fill=1, stroke=0)
    # Gold accent
    c.setFillColor(ACCENT_GOLD)
    c.rect(0, 7*cm, W, 3*mm, fill=1, stroke=0)
    # Side accent bar
    c.setFillColor(DOMINOS_RED)
    c.rect(0, 0, 8*mm, H, fill=1, stroke=0)
    c.restoreState()

# ─── STYLES ───────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    s = {}

    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=38, textColor=WHITE,
        leading=44, alignment=TA_LEFT, spaceAfter=8)

    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='Helvetica', fontSize=16, textColor=ACCENT_GOLD,
        leading=22, alignment=TA_LEFT, spaceAfter=6)

    s['cover_tagline'] = ParagraphStyle('cover_tagline',
        fontName='Helvetica', fontSize=10, textColor=MID_GREY,
        leading=15, alignment=TA_LEFT)

    s['chapter_num'] = ParagraphStyle('chapter_num',
        fontName='Helvetica-Bold', fontSize=11, textColor=DOMINOS_RED,
        leading=16, alignment=TA_LEFT, spaceAfter=2)

    s['chapter_title'] = ParagraphStyle('chapter_title',
        fontName='Helvetica-Bold', fontSize=22, textColor=DOMINOS_BLUE,
        leading=28, alignment=TA_LEFT, spaceAfter=4)

    s['section_head'] = ParagraphStyle('section_head',
        fontName='Helvetica-Bold', fontSize=13, textColor=DOMINOS_BLUE,
        leading=18, spaceBefore=14, spaceAfter=5,
        borderPadding=(0,0,3,0))

    s['subsection_head'] = ParagraphStyle('subsection_head',
        fontName='Helvetica-Bold', fontSize=11, textColor=DOMINOS_RED,
        leading=16, spaceBefore=10, spaceAfter=4)

    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, textColor=DARK_TEXT,
        leading=15, spaceAfter=7, alignment=TA_JUSTIFY)

    s['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=9.5, textColor=DARK_TEXT,
        leading=14, spaceAfter=4, leftIndent=14,
        bulletIndent=4, alignment=TA_LEFT)

    s['highlight_box'] = ParagraphStyle('highlight_box',
        fontName='Helvetica', fontSize=9, textColor=DOMINOS_BLUE,
        leading=14, spaceAfter=5, alignment=TA_LEFT)

    s['stat_label'] = ParagraphStyle('stat_label',
        fontName='Helvetica', fontSize=8, textColor=WHITE,
        leading=12, alignment=TA_CENTER)

    s['stat_value'] = ParagraphStyle('stat_value',
        fontName='Helvetica-Bold', fontSize=20, textColor=WHITE,
        leading=26, alignment=TA_CENTER)

    s['caption'] = ParagraphStyle('caption',
        fontName='Helvetica', fontSize=8, textColor=colors.HexColor("#666666"),
        leading=11, alignment=TA_CENTER, spaceAfter=6)

    s['toc_title'] = ParagraphStyle('toc_title',
        fontName='Helvetica-Bold', fontSize=11, textColor=DOMINOS_BLUE,
        leading=16, spaceAfter=3)

    s['toc_item'] = ParagraphStyle('toc_item',
        fontName='Helvetica', fontSize=9.5, textColor=DARK_TEXT,
        leading=14, spaceAfter=2, leftIndent=10)

    s['quote'] = ParagraphStyle('quote',
        fontName='Helvetica-Oblique', fontSize=10, textColor=DOMINOS_BLUE,
        leading=15, spaceAfter=8, leftIndent=20, rightIndent=20,
        alignment=TA_CENTER)

    return s

# ─── HELPER FLOWABLES ─────────────────────────────────────────────────────────
class ColorBar(Flowable):
    def __init__(self, width, height, color):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)

class StatCard(Flowable):
    def __init__(self, value, label, color=DOMINOS_BLUE, width=3.8*cm, height=2.6*cm):
        super().__init__()
        self.value = value
        self.label = label
        self.color = color
        self.width = width
        self.height = height
    def wrap(self, *args):
        return self.width, self.height
    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.width/2, self.height*0.52, self.value)
        c.setFont("Helvetica", 7)
        c.drawCentredString(self.width/2, self.height*0.22, self.label)

class SectionDivider(Flowable):
    def __init__(self, width=None):
        super().__init__()
        self._width = width or (W - 4*cm)
    def wrap(self, *args):
        return self._width, 8
    def draw(self):
        c = self.canv
        c.setFillColor(DOMINOS_RED)
        c.rect(0, 4, self._width * 0.08, 3, fill=1, stroke=0)
        c.setFillColor(DOMINOS_BLUE)
        c.rect(self._width * 0.09, 4, self._width * 0.91, 1.5, fill=1, stroke=0)

def info_box(text, style_dict, bg=SECTION_BG, border=DOMINOS_BLUE):
    data = [[Paragraph(text, style_dict)]]
    t = Table(data, colWidths=[W - 4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINECOLOR', (0,0), (0,0), border),
        ('LINEBEFORE', (0,0), (0,0), 3, border),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [bg]),
    ]))
    return t

def std_table(headers, rows, col_widths=None):
    data = [headers] + rows
    if not col_widths:
        col_widths = [(W - 4*cm) / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths)
    style = [
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, MID_GREY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, TABLE_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]
    t.setStyle(TableStyle(style))
    return t


def build_report():
    S = build_styles()
    story = []

    # ════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 4.5*cm))
    story.append(Paragraph("DOMINO'S", S['cover_title']))
    story.append(Paragraph("PIZZA", ParagraphStyle('ct2', parent=S['cover_title'],
        textColor=DOMINOS_RED, spaceAfter=4)))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Franchise Business Analysis Report", S['cover_sub']))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "An In-Depth Study of Company Profile · Franchise Relationships · "
        "Statistical Insights · Trend Analysis · Challenges &amp; Key Takeaways",
        S['cover_tagline']))
    story.append(Spacer(1, 6.5*cm))

    cover_meta = [
        ["Prepared By", "Research &amp; Analytics Division"],
        ["Report Type", "Comprehensive Franchise Study"],
        ["Edition", "2024 | Updated Edition"],
        ["Classification", "Academic / Business Intelligence"],
    ]
    ct = Table(cover_meta, colWidths=[4*cm, 9*cm])
    ct.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,-1), WHITE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#FFFFFF44")),
    ]))
    story.append(ct)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("TABLE OF CONTENTS", S['chapter_title']))
    story.append(SectionDivider())
    story.append(Spacer(1, 0.4*cm))

    toc_entries = [
        ("01", "Introduction & Company Profile", "3"),
        ("02", "Franchisor–Franchisee Relationship", "6"),
        ("03", "Statistical Information", "9"),
        ("04", "Pros and Cons Faced", "13"),
        ("05", "Trend Analysis: From Inception to Present", "17"),
        ("06", "Understanding & Key Takeaways from Challenges", "21"),
        ("07", "Conclusion", "24"),
    ]
    for num, title, pg in toc_entries:
        toc_row = Table(
            [[Paragraph(f"<b>{num}</b>", S['toc_item']),
              Paragraph(title, S['toc_title']),
              Paragraph(f"Pg {pg}", S['toc_item'])]],
            colWidths=[1.2*cm, 12*cm, 1.5*cm]
        )
        toc_row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, LIGHT_GREY),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ]))
        story.append(toc_row)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CHAPTER 1 – INTRODUCTION & COMPANY PROFILE
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("CHAPTER 01", S['chapter_num']))
    story.append(Paragraph("Introduction &amp; Company Profile", S['chapter_title']))
    story.append(SectionDivider())
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("About Domino's Pizza", S['section_head']))
    story.append(Paragraph(
        "Domino's Pizza, officially known as Domino's Inc., is one of the world's largest and most recognized "
        "pizza restaurant chains. Founded in 1960 in Ypsilanti, Michigan, USA, by brothers Tom and James "
        "Monaghan, the brand has grown from a single pizza store into a global franchise empire spanning "
        "more than 90 countries with over 20,000 locations worldwide. The company's headquarter is located "
        "in Ann Arbor, Michigan, and it is publicly traded on the New York Stock Exchange (NYSE: DPZ).",
        S['body']))

    story.append(Paragraph(
        "Domino's built its reputation on a deceptively simple value proposition: delivering hot, fresh pizza "
        "quickly and reliably. This focus on delivery efficiency — rather than dine-in experience — was "
        "revolutionary for its time and became the cornerstone of its global brand identity. Today, Domino's "
        "is not merely a pizza chain; it is a technology-driven, logistics-focused franchise powerhouse.",
        S['body']))

    story.append(Paragraph("Founding Story", S['section_head']))
    story.append(Paragraph(
        "In 1960, Tom Monaghan and his brother James purchased a small pizza restaurant called 'DomiNick's' "
        "in Ypsilanti, Michigan for $500. James later traded his share of the business for a used Volkswagen "
        "Beetle, leaving Tom as the sole owner. After expanding to a second location, the original owner of "
        "the DomiNick's name refused to allow it to be used for additional stores. A delivery driver "
        "suggested 'Domino's,' and the name has endured ever since.", S['body']))

    story.append(Paragraph(
        "The company's iconic logo — a domino tile with three dots — originally represented the three stores "
        "the company operated at that time, with the intention of adding a dot for every new store opened. "
        "As the company grew exponentially, this plan became impractical, but the logo remained, symbolizing "
        "the brand's foundational heritage.", S['body']))

    # Key Facts table
    story.append(Paragraph("Corporate Snapshot", S['section_head']))
    facts = [
        ["Founded", "December 9, 1960"],
        ["Founders", "Tom Monaghan &amp; James Monaghan"],
        ["Headquarters", "Ann Arbor, Michigan, USA"],
        ["CEO (Current)", "Russell Weiner"],
        ["Ticker Symbol", "NYSE: DPZ"],
        ["Global Locations", "20,000+ in 90+ countries"],
        ["Annual Revenue", "~$4.53 Billion (2023)"],
        ["Employees", "~10,000 corporate + 200,000+ franchise"],
        ["Business Model", "Primarily Franchise-Based (~98%)"],
        ["Core Products", "Pizza, Pasta, Sandwiches, Desserts, Beverages"],
    ]
    ft = Table(facts, colWidths=[5*cm, 9.7*cm])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#EEF3F8")),
        ('BACKGROUND', (1,0), (1,-1), WHITE),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (0,-1), DOMINOS_BLUE),
        ('GRID', (0,0), (-1,-1), 0.5, MID_GREY),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [LIGHT_GREY, WHITE]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(ft)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Mission, Vision &amp; Core Values", S['section_head']))
    story.append(Paragraph("<b>Mission Statement:</b>", S['subsection_head']))
    story.append(info_box(
        '"Exceptional franchisees and team members on a mission to be the best pizza delivery company "  '
        'in the world, in every neighborhood."',
        S['quote'], bg=colors.HexColor("#EEF3F8"), border=DOMINOS_RED))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("<b>Core Values:</b>", S['subsection_head']))
    values = [
        ("Putting People First", "Prioritizing team members, franchisees, and customers in every decision."),
        ("Delivering with Integrity", "Doing the right thing even when no one is watching."),
        ("Winning Together", "Collaborative success built on mutual trust and shared goals."),
        ("Hungry to Innovate", "Continuously seeking better technology, products, and processes."),
        ("Celebrating Excellence", "Recognizing and rewarding outstanding performance."),
    ]
    for title_val, desc in values:
        story.append(Paragraph(f"<b>• {title_val}:</b> {desc}", S['bullet']))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Global Footprint", S['section_head']))
    story.append(Paragraph(
        "Domino's global reach is vast and continues to expand. The brand operates across six continents, "
        "with particularly strong presences in North America, South Asia (especially India, where Jubilant "
        "FoodWorks Limited is the master franchisee), the United Kingdom, Australia, and Latin America. "
        "Domino's India alone operates over 1,900 stores, making it one of the largest pizza chains in "
        "the Asian subcontinent.", S['body']))

    region_data = [
        ["Region", "Store Count (Approx.)", "Key Markets"],
        ["North America", "6,700+", "USA, Canada"],
        ["Asia Pacific", "5,800+", "India, Japan, Australia, China"],
        ["Europe", "3,900+", "UK, Germany, France"],
        ["Latin America", "1,800+", "Mexico, Brazil"],
        ["Middle East & Africa", "1,200+", "Saudi Arabia, South Africa"],
        ["Other Markets", "800+", "Various"],
    ]
    story.append(std_table(region_data[0], region_data[1:], [4.5*cm, 5.5*cm, 4.7*cm]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CHAPTER 2 – FRANCHISOR–FRANCHISEE RELATIONSHIP
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("CHAPTER 02", S['chapter_num']))
    story.append(Paragraph("Franchisor–Franchisee Relationship", S['chapter_title']))
    story.append(SectionDivider())
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Overview of the Franchise Model", S['section_head']))
    story.append(Paragraph(
        "Domino's Pizza operates predominantly through a franchise model, with approximately 98% of its "
        "global stores being franchisee-owned. This makes Domino's one of the most franchise-dependent "
        "major food chains in the world. Under this model, Domino's (the franchisor) grants independent "
        "business owners (franchisees) the right to operate a Domino's store using its brand, systems, "
        "recipes, and operational frameworks in exchange for fees and royalties.", S['body']))

    story.append(Paragraph("Franchise Structure: Types of Ownership", S['section_head']))
    types = [
        ("Single-Unit Franchise", "Franchisee owns and operates one store. Ideal for first-time "
         "entrepreneurs. This is the most common starting point for new Domino's franchisees."),
        ("Multi-Unit Franchise", "A proven operator who owns multiple Domino's stores under one "
         "agreement. Domino's actively encourages multi-unit ownership for scaling."),
        ("Master Franchise Agreement", "Large companies or individuals who acquire the right to "
         "develop and sub-franchise an entire country or territory. Example: Jubilant FoodWorks "
         "in India, DP Eurasia in Turkey and Russia."),
    ]
    for t, d in types:
        story.append(Paragraph(f"<b>{t}</b>", S['subsection_head']))
        story.append(Paragraph(d, S['body']))

    story.append(Paragraph("Financial Obligations of a Franchisee", S['section_head']))
    fin_data = [
        ["Fee Type", "Amount / Rate", "Frequency"],
        ["Initial Franchise Fee", "$10,000 (USA)", "One-Time"],
        ["Royalty Fee", "5.5% of gross sales", "Weekly"],
        ["Advertising Fund Contribution", "6% of gross sales", "Weekly"],
        ["Estimated Total Investment", "$150,000 – $500,000+", "Initial Setup"],
        ["Renewal Fee", "$1,500 per unit", "Every 10 Years"],
        ["Technology Fee", "~$200/month", "Monthly"],
    ]
    story.append(std_table(fin_data[0], fin_data[1:], [5.5*cm, 5.5*cm, 3.7*cm]))
    story.append(Spacer(1, 0.3*cm))
    story.append(info_box(
        "<b>Note:</b> Investment amounts vary significantly by country, location (urban vs rural), "
        "store format (delivery-only vs dine-in), and local construction/labor costs. "
        "Indian franchisee investment typically ranges between ₹30 lakh to ₹1.5 crore.",
        S['highlight_box']))

    story.append(Paragraph("Rights &amp; Responsibilities", S['section_head']))
    story.append(Paragraph("<b>What the Franchisor (Domino's) Provides:</b>", S['subsection_head']))
    franchisor_rights = [
        "Brand licensing and use of the Domino's trademark and trade dress",
        "Standardized recipes, ingredients, and proprietary food systems",
        "Comprehensive initial training program (minimum 3-4 weeks at a certified training store)",
        "Access to the Domino's PULSE point-of-sale and management system",
        "Ongoing operational support, field consulting, and quality audits",
        "National and regional advertising campaigns funded by the Ad Fund",
        "New product development and menu innovation",
        "Technology infrastructure including ordering apps and delivery tracking",
    ]
    for r in franchisor_rights:
        story.append(Paragraph(f"• {r}", S['bullet']))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("<b>Franchisee Obligations:</b>", S['subsection_head']))
    franchisee_obs = [
        "Maintain strict brand standards, store cleanliness, and product quality",
        "Use only approved suppliers for ingredients, packaging, and equipment",
        "Hire, train, and manage all store-level employees",
        "Pay all fees on time: royalties, advertising, and technology fees",
        "Participate in local store marketing (LSM) activities",
        "Adhere to Domino's operational standards and franchise agreement terms",
        "Reinvest in store improvements and technology upgrades as required",
    ]
    for o in franchisee_obs:
        story.append(Paragraph(f"• {o}", S['bullet']))

    story.append(Paragraph("Conflict Resolution &amp; Support Mechanisms", S['section_head']))
    story.append(Paragraph(
        "Domino's maintains a Franchise Advisory Council (FAC) in the United States and similar bodies "
        "in other markets. This council gives franchisees a formal voice in matters of policy, marketing "
        "spending, and product development. Disputes between the franchisor and franchisees are typically "
        "handled through structured mediation processes outlined in the Franchise Disclosure Document (FDD). "
        "Domino's has, on multiple occasions, faced legal disputes from franchisees over issues such as "
        "territory encroachment, mandatory technology upgrades, and advertising fund allocation.", S['body']))

    story.append(Paragraph("Franchisee Success: Training &amp; Development", S['section_head']))
    story.append(Paragraph(
        "Domino's invests heavily in franchisee education. The Domino's College of Pizzerology is a "
        "flagship training concept where new and existing franchisees undergo intensive learning in "
        "operations, customer service, and business management. On-the-job training at approved training "
        "stores is mandatory, and ongoing e-learning modules keep franchisees up to date with new systems "
        "and procedures. This structured approach has resulted in a relatively low franchisee failure rate "
        "compared to the broader restaurant industry.", S['body']))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CHAPTER 3 – STATISTICAL INFORMATION
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("CHAPTER 03", S['chapter_num']))
    story.append(Paragraph("Statistical Information", S['chapter_title']))
    story.append(SectionDivider())
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "This chapter presents a data-driven overview of Domino's Pizza's financial performance, "
        "store growth, operational metrics, and market position, offering quantitative context "
        "for understanding the company's scale and trajectory.", S['body']))

    # Stat cards row
    story.append(Paragraph("Key Performance Indicators at a Glance", S['section_head']))
    stats_row = Table([[
        StatCard("20,000+", "Global Stores", DOMINOS_BLUE),
        StatCard("90+", "Countries", DOMINOS_RED),
        StatCard("$4.5B", "2023 Revenue", colors.HexColor("#1A6B3C")),
        StatCard("~1M", "Orders / Day", ACCENT_GOLD),
    ]], colWidths=[3.8*cm, 3.8*cm, 3.8*cm, 3.8*cm])
    stats_row.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(stats_row)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Revenue &amp; Financial Performance (2018–2023)", S['section_head']))
    rev_data = [
        ["Year", "Revenue (USD Billion)", "Net Income (USD Million)", "Stores Worldwide"],
        ["2018", "$3.43B", "$361M", "15,914"],
        ["2019", "$3.62B", "$415M", "17,020"],
        ["2020", "$4.12B", "$491M", "17,644"],
        ["2021", "$4.36B", "$530M", "18,848"],
        ["2022", "$4.49B", "$447M", "19,519"],
        ["2023", "$4.53B", "$461M", "20,031"],
    ]
    story.append(std_table(rev_data[0], rev_data[1:], [2.5*cm, 5.2*cm, 5.5*cm, 4*cm]))
    story.append(Paragraph("Source: Domino's Pizza Annual Reports 2018–2023", S['caption']))

    story.append(Paragraph("Same-Store Sales Growth (SSSG)", S['section_head']))
    story.append(Paragraph(
        "Same-store sales growth is a critical retail and restaurant metric, measuring revenue change "
        "at established stores (open at least 12 months). Domino's has maintained consistently positive "
        "SSSG for over a decade, demonstrating the strength of its operational model and customer loyalty.",
        S['body']))

    sssg_data = [
        ["Year", "US SSSG", "International SSSG", "Global SSSG"],
        ["2018", "+6.6%", "+3.6%", "+5.1%"],
        ["2019", "+3.9%", "+1.6%", "+2.8%"],
        ["2020", "+11.5%", "+5.4%", "+8.5%"],
        ["2021", "+3.5%", "+8.9%", "+6.2%"],
        ["2022", "+2.9%", "+0.2%", "+1.6%"],
        ["2023", "+2.7%", "+2.5%", "+2.6%"],
    ]
    story.append(std_table(sssg_data[0], sssg_data[1:], [3.5*cm, 4.5*cm, 5*cm, 4*cm]))

    story.append(Paragraph("Digital &amp; Delivery Statistics", S['section_head']))
    story.append(Paragraph(
        "Domino's transformation into a technology-first company is reflected in its digital order "
        "metrics. By 2023, digital channels accounted for over 80% of all orders globally, "
        "demonstrating a fundamental shift in consumer behavior that Domino's has proactively "
        "embraced and amplified.", S['body']))

    digital_data = [
        ["Metric", "Value", "Year"],
        ["Digital Order Share (US)", ">80%", "2023"],
        ["Active Loyalty Members", "30+ Million", "2023"],
        ["Domino's App Downloads (Cumulative)", "100M+", "2023"],
        ["Average Delivery Time (US)", "~23 Minutes", "2023"],
        ["Countries with Online Ordering", "85+", "2023"],
        ["Weekly Online Transactions", "~7 Million", "2023"],
    ]
    story.append(std_table(digital_data[0], digital_data[1:], [7*cm, 4.5*cm, 3.5*cm]))

    story.append(Paragraph("Store Network Growth", S['section_head']))
    story.append(Paragraph(
        "Domino's store count has grown nearly fourfold since 2000, reflecting sustained franchise "
        "demand. The company's net unit growth strategy targets approximately 800–1,000 new stores "
        "annually, with developing markets like India, China, and Southeast Asia offering the "
        "greatest near-term expansion opportunities.", S['body']))

    growth_data = [
        ["Year", "Total Stores", "Net New Stores", "% International"],
        ["2000", "5,239", "—", "38%"],
        ["2005", "8,029", "+556/yr avg", "47%"],
        ["2010", "9,351", "+264/yr avg", "52%"],
        ["2015", "12,261", "+582/yr avg", "57%"],
        ["2020", "17,644", "+1,077/yr avg", "64%"],
        ["2023", "20,031", "+796/yr avg", "67%"],
    ]
    story.append(std_table(growth_data[0], growth_data[1:], [2.8*cm, 4*cm, 5.5*cm, 4.4*cm]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CHAPTER 4 – PROS AND CONS
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("CHAPTER 04", S['chapter_num']))
    story.append(Paragraph("Pros and Cons Faced", S['chapter_title']))
    story.append(SectionDivider())
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "Like any major global business, Domino's Pizza faces a complex landscape of advantages "
        "and disadvantages — from the perspective of the corporate entity, its franchisees, customers, "
        "and society at large. This chapter provides a balanced, comprehensive analysis.", S['body']))

    # PROS
    story.append(Paragraph("ADVANTAGES — What Makes Domino's Succeed", S['section_head']))
    story.append(ColorBar(W - 4*cm, 2.5*mm, colors.HexColor("#1A6B3C")))
    story.append(Spacer(1, 0.15*cm))

    pros = [
        ("1. Iconic Global Brand Recognition",
         "The Domino's brand is instantly recognizable in over 90 countries. Decades of consistent "
         "branding, memorable slogans ('30 minutes or it's free'), and aggressive marketing have "
         "created a brand with extraordinary recall value. New franchisees benefit from this "
         "pre-built customer trust from day one."),

        ("2. Franchise-First Business Model",
         "With ~98% franchise ownership, Domino's has a capital-light business model. The franchisor "
         "receives royalties and fees without bearing most of the operational risk. This enables rapid "
         "global expansion with lower corporate capital expenditure, benefiting shareholders."),

        ("3. Technology Leadership",
         "Domino's has consistently been a first mover in digital ordering innovation. It launched "
         "ordering via text message, smart TVs, voice assistants, and social media. The proprietary "
         "PULSE POS system and real-time GPS delivery tracking set industry standards. By 2023, "
         "80%+ of US orders were placed digitally."),

        ("4. Delivery-Focused Infrastructure",
         "Unlike competitors who retrofitted delivery onto dine-in models, Domino's was built for "
         "delivery from inception. This gives it inherent operational advantages — store layouts, "
         "supply chains, and workforce training are all optimized for fast, accurate delivery."),

        ("5. Domino's Rewards Loyalty Program",
         "With 30+ million active members in the US alone, the Domino's Rewards program drives "
         "repeat purchases, data collection, and personalization. Loyalty members order more "
         "frequently and spend more per visit than non-members."),

        ("6. Supply Chain Strength",
         "Domino's operates its own supply chain network — Domino's Pizza LLC's vertically "
         "integrated commissary system — supplying dough, sauces, and cheese directly to stores. "
         "This ensures quality consistency and reduces franchisee procurement complexity."),

        ("7. Affordable Price Point",
         "Domino's positions itself as a value brand, making it accessible during economic "
         "downturns. During recessions and inflation cycles, consumers often trade down from "
         "full-service restaurants to value-oriented QSR brands like Domino's."),
    ]
    for title_p, desc_p in pros:
        story.append(Paragraph(f"<b>{title_p}</b>", S['subsection_head']))
        story.append(Paragraph(desc_p, S['body']))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("DISADVANTAGES — Key Challenges &amp; Weaknesses", S['section_head']))
    story.append(ColorBar(W - 4*cm, 2.5*mm, DOMINOS_RED))
    story.append(Spacer(1, 0.15*cm))

    cons = [
        ("1. Intense Competition",
         "The QSR and pizza market is fiercely competitive. Domino's faces pressure from global "
         "brands (Pizza Hut, Papa John's, Little Caesars), local/regional chains, third-party "
         "delivery aggregators (DoorDash, Uber Eats, Swiggy, Zomato), and increasingly, ghost "
         "kitchens and cloud restaurants that can undercut on price."),

        ("2. Franchisee Quality Control Challenges",
         "With 20,000+ independently owned locations, enforcing uniform quality standards is "
         "an enormous operational challenge. Inconsistent product quality, hygiene issues, and "
         "service failures at individual franchise locations can damage the global brand. "
         "Franchisee turnover and financial distress also create service gaps."),

        ("3. High-Calorie Product Portfolio",
         "Growing global health consciousness has put fast food brands under scrutiny. Domino's "
         "core menu of pizzas, pasta, and desserts is calorie-dense and processed. Despite some "
         "healthier options, the brand struggles to attract health-focused consumers, and may "
         "face future regulatory pressure on nutritional labeling."),

        ("4. Dependence on Delivery Workforce",
         "Domino's relies heavily on delivery drivers, making it vulnerable to labor shortages, "
         "wage increases, and driver retention challenges. In markets with high minimum wage "
         "legislation, labor costs significantly compress franchisee margins."),

        ("5. Currency &amp; Geopolitical Risk",
         "As a company earning significant revenues internationally, Domino's is exposed to "
         "currency exchange fluctuations. Political instability, trade restrictions, or "
         "regulatory changes in key markets can adversely impact earnings. The Russia-Ukraine "
         "conflict directly impacted operations in Eastern Europe."),

        ("6. Supply Chain Inflation Sensitivity",
         "Cheese, wheat (for dough), and cooking oils — Domino's primary ingredients — are "
         "globally traded commodities subject to volatile price swings. Ingredient cost spikes "
         "directly impact margins, particularly for smaller franchisees."),

        ("7. Third-Party Delivery Platform Pressure",
         "The rise of DoorDash, Uber Eats, and Grubhub created a dilemma for Domino's. "
         "Initially resistant (preferring its own delivery), Domino's eventually partnered "
         "with Uber Eats in 2023, accepting that consumer preference for aggregator platforms "
         "required adapting its historically closed delivery model."),
    ]
    for title_c, desc_c in cons:
        story.append(Paragraph(f"<b>{title_c}</b>", S['subsection_head']))
        story.append(Paragraph(desc_c, S['body']))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CHAPTER 5 – TREND ANALYSIS
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("CHAPTER 05", S['chapter_num']))
    story.append(Paragraph("Trend Analysis: From Inception to Present", S['chapter_title']))
    story.append(SectionDivider())
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "This chapter traces Domino's evolution through distinct strategic phases — from its "
        "origins as a single-store pizza delivery operation to its current status as a "
        "technology-enabled global franchise leader.", S['body']))

    eras = [
        ("Era 1: 1960–1978 | The Foundation Years",
         "DOMINOS_RED",
         [
             "1960: Tom Monaghan purchases DomiNick's pizza for $500.",
             "1965: First franchise store opened in Ypsilanti, Michigan.",
             "1967: The name 'Domino's Pizza' is officially adopted.",
             "1975: Amstar Corp. sues over use of 'Domino' name; Domino's wins the case.",
             "1978: The 200th Domino's store opens; rapid franchise growth begins.",
             "Focus was on speed, simplicity, and delivery-only operations.",
         ]),
        ("Era 2: 1979–1997 | Rapid Domestic Expansion",
         "DOMINOS_BLUE",
         [
             "1983: First international store opens in Winnipeg, Canada.",
             "1985: Japanese market entry — among first US pizza chains in Asia.",
             "1985: The famous '30 minutes or it's free' guarantee launches.",
             "1989: 5,000th store opens globally.",
             "1993: 30-minute guarantee is retired over road safety liability concerns.",
             "1997: 1,500 international locations across 55 countries.",
         ]),
        ("Era 3: 1998–2009 | Private Equity, IPO & Digital Awakening",
         "ACCENT_GOLD",
         [
             "1998: Tom Monaghan sells 93% of Domino's to Bain Capital for $1 billion.",
             "2003: Dave Brandon becomes CEO, drives operational and brand reforms.",
             "2004: Domino's goes public on NYSE under ticker DPZ.",
             "2007: Online ordering launches — a pivotal digital milestone.",
             "2008: Domino's launches iPhone app, pioneering mobile ordering.",
             "2009: J. Patrick Doyle becomes CEO; initiates bold reinvention strategy.",
         ]),
        ("Era 4: 2010–2018 | The Pizza Turnaround & Tech Revolution",
         "DOMINOS_RED",
         [
             "2010: Public recipe reformulation — Domino's admits to old pizza failures on TV.",
             "2011: 'Domino's Tracker' real-time delivery tracking launches.",
             "2012: 5,000+ digital ordering platforms including voice, smart TV.",
             "2014: 'Zero-Click' ordering app introduced.",
             "2015: AnyWare ordering — Twitter, Google Home, Amazon Echo integration.",
             "2018: Stock price grows 2,000%+ over the decade — one of NYSE's top performers.",
         ]),
        ("Era 5: 2019–2024 | Pandemic Surge, Staffing & Aggregator Adaptation",
         "DOMINOS_BLUE",
         [
             "2020: COVID-19 pandemic drives unprecedented delivery demand — SSSG +11.5%.",
             "2021: 'Fortressing' strategy: denser store network for faster delivery.",
             "2021: Russell Weiner becomes President; CEO transition initiated.",
             "2022: Domino's exits Russia following Ukraine invasion.",
             "2022: Labor shortages challenge delivery operations; carryout promotions expanded.",
             "2023: Domino's partners with Uber Eats — historic shift from owned-delivery exclusivity.",
             "2024: Continued expansion in India, Southeast Asia, and Middle East.",
         ]),
    ]

    for era_title, era_color, bullets in eras:
        color = DOMINOS_RED if era_color == "DOMINOS_RED" else (
            DOMINOS_BLUE if era_color == "DOMINOS_BLUE" else ACCENT_GOLD)
        story.append(Paragraph(era_title, S['subsection_head']))
        era_items = [[Paragraph("• " + b, S['bullet'])] for b in bullets]
        era_table = Table(era_items, colWidths=[W - 4*cm])
        era_table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 14),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LINEBEFORE', (0,0), (0,-1), 3, color),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FC")),
        ]))
        story.append(era_table)
        story.append(Spacer(1, 0.25*cm))

    story.append(Paragraph("Stock Price Performance: A Decade of Dominance", S['section_head']))
    story.append(Paragraph(
        "Domino's is frequently cited as one of the best-performing stocks of the 2010s on the NYSE. "
        "From its IPO price of $14.00 per share in 2004, DPZ climbed to a peak of approximately "
        "$567 in 2021 — representing a 40x return for early investors. This extraordinary "
        "performance was driven by consistent earnings growth, a shareholder-friendly buyback "
        "program, rising digital revenues, and the effective franchise model that generates "
        "high-margin royalty income at scale.", S['body']))

    stock_data = [
        ["Year", "Approx. Stock Price", "Key Driver"],
        ["2004 (IPO)", "$14", "NYSE Listing"],
        ["2010", "$18", "Recipe reformulation buzz"],
        ["2013", "$55", "Digital ordering growth"],
        ["2016", "$150", "Tech-first strategy validated"],
        ["2018", "$300", "Consistent SSSG, global expansion"],
        ["2021 (Peak)", "$567", "Pandemic delivery boom"],
        ["2023", "$~380", "Post-peak normalization"],
    ]
    story.append(std_table(stock_data[0], stock_data[1:], [3.5*cm, 5.5*cm, 6*cm]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CHAPTER 6 – KEY TAKEAWAYS FROM CHALLENGES
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("CHAPTER 06", S['chapter_num']))
    story.append(Paragraph("Understanding &amp; Key Takeaways from Challenges Faced", S['chapter_title']))
    story.append(SectionDivider())
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "Every great business is shaped as much by its failures and challenges as by its successes. "
        "Domino's history offers exceptional case studies in strategic resilience, consumer-centric "
        "reinvention, and adaptive management. This chapter extracts the most important learnings.", S['body']))

    challenges = [
        {
            "title": "Challenge 1: The Pizza Quality Crisis (2008–2010)",
            "desc": "By 2008, Domino's pizza had become the butt of jokes. Consumer surveys ranked "
                    "Domino's last among major pizza chains in taste. A viral social media video by "
                    "rogue employees showing unsanitary kitchen practices went viral on YouTube, "
                    "causing significant brand damage.",
            "response": "New CEO Patrick Doyle made an unprecedented decision: Domino's publicly "
                        "acknowledged that its pizza was bad and announced a complete recipe overhaul. "
                        "A national ad campaign called 'Pizza Turnaround' aired real customers criticizing "
                        "the old pizza, followed by the reveal of the new recipe. This radical transparency "
                        "was a masterclass in brand crisis management.",
            "takeaway": "Transparency and radical honesty can transform a weakness into a marketing "
                        "advantage. Consumers reward brands that acknowledge mistakes and show genuine improvement.",
        },
        {
            "title": "Challenge 2: The '30 Minutes or Free' Liability Crisis (1993)",
            "desc": "Domino's iconic guarantee created a culture where delivery drivers felt pressure "
                    "to speed. By the early 1990s, a series of accidents involving Domino's delivery "
                    "drivers — some fatal — resulted in massive legal liabilities. A 1993 lawsuit "
                    "resulted in an $78 million judgment against the company.",
            "response": "Domino's permanently retired the 30-minute guarantee, replacing it with a "
                        "focus on 'hot, fresh pizza delivered at a time you specify.' This shifted brand "
                        "positioning from speed-above-all to quality and reliability.",
            "takeaway": "Promotional strategies must account for real-world second-order consequences. "
                        "A powerful marketing tool can create dangerous incentive structures if not "
                        "carefully managed. Brands must prioritize safety over brand promises.",
        },
        {
            "title": "Challenge 3: Digital Disruption & The Third-Party Aggregator Dilemma",
            "desc": "As DoorDash, Uber Eats, and Grubhub gained mass-market adoption, Domino's faced "
                    "a strategic dilemma. Its own delivery infrastructure was a competitive strength, "
                    "but a growing segment of customers preferred to discover and order from "
                    "aggregator platforms. Resistance to listing on these platforms risked losing "
                    "market share to competitors who embraced them.",
            "response": "After years of resistance, Domino's announced a landmark partnership with "
                        "Uber Eats in 2023, recognizing that consumer convenience preferences must "
                        "ultimately guide strategy. The company negotiated terms to protect its data "
                        "and economics while accessing new customer acquisition channels.",
            "takeaway": "Even companies with best-in-class proprietary systems must remain open to "
                        "evolving their ecosystem strategy when market forces demand it. Inflexibility "
                        "in the face of consumer preference shifts can cost market share.",
        },
        {
            "title": "Challenge 4: Labor Shortages &amp; Delivery Staffing (2021–2023)",
            "desc": "The post-pandemic labor market saw unprecedented shortages, particularly in "
                    "the restaurant and delivery sector. Domino's closed approximately 107 US stores "
                    "in 2021 due to inability to staff delivery operations. Wage pressures further "
                    "squeezed franchisee margins.",
            "response": "Domino's responded with a 'Carryout Only' promotion strategy, offering "
                        "significant discounts to customers who picked up their orders. This reduced "
                        "dependency on delivery drivers while maintaining order volumes. The company "
                        "also accelerated its investment in automation and electric delivery vehicle trials.",
            "takeaway": "Business model flexibility — being able to shift between delivery and carryout "
                        "as operational conditions change — provides vital resilience against labor "
                        "market volatility.",
        },
        {
            "title": "Challenge 5: Geopolitical Risk — Russia Exit (2022)",
            "desc": "Russia represented a significant Domino's market with hundreds of locations "
                    "operated by a master franchisee. The Russian invasion of Ukraine in February "
                    "2022 created ethical, reputational, and operational pressures on all Western "
                    "consumer brands operating in Russia.",
            "response": "The Russian master franchisee chose to re-brand all stores under a new "
                        "name rather than comply with Domino's requirement to exit the Russian market. "
                        "Domino's terminated its Russia franchise agreement, effectively losing a "
                        "substantial number of stores virtually overnight.",
            "takeaway": "Global expansion through master franchise agreements requires careful "
                        "geopolitical risk assessment and robust contractual mechanisms to manage "
                        "exit scenarios when political circumstances demand it.",
        },
        {
            "title": "Challenge 6: Nutrition &amp; Health Perception",
            "desc": "As consumer health consciousness has grown globally, fast food brands face "
                    "increasing pressure from regulators (calorie labeling laws), health advocates, "
                    "and changing consumer preferences. Domino's core menu is seen as indulgent "
                    "and calorie-dense.",
            "response": "Domino's has gradually introduced lighter options, salads, and "
                        "lower-calorie pizzas in select markets. The company has also committed "
                        "to improving nutritional transparency, providing detailed calorie and "
                        "allergen information on its ordering platforms.",
            "takeaway": "Long-term brand sustainability requires proactively adapting product "
                        "portfolios to evolving consumer values. Waiting for regulatory mandates "
                        "creates reactive brand perception rather than progressive leadership.",
        },
    ]

    for ch in challenges:
        story.append(Paragraph(ch["title"], S['subsection_head']))
        story.append(Paragraph(ch["desc"], S['body']))

        ch_table = Table([
            [Paragraph("<b>Domino's Response:</b>", S['highlight_box'])],
            [Paragraph(ch["response"], S['highlight_box'])],
        ], colWidths=[W - 4*cm])
        ch_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF4FB")),
            ('LINEBEFORE', (0,0), (0,-1), 3, DOMINOS_BLUE),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(ch_table)
        story.append(Spacer(1, 0.1*cm))

        tk_table = Table([
            [Paragraph("<b>&#128270; Key Takeaway:</b>", ParagraphStyle('kt', parent=S['highlight_box'],
                textColor=colors.HexColor("#6B3A00")))],
            [Paragraph(ch["takeaway"], ParagraphStyle('kt2', parent=S['highlight_box'],
                textColor=colors.HexColor("#4A2600")))],
        ], colWidths=[W - 4*cm])
        tk_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF8E1")),
            ('LINEBEFORE', (0,0), (0,-1), 3, ACCENT_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(tk_table)
        story.append(Spacer(1, 0.3*cm))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CHAPTER 7 – CONCLUSION
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("CHAPTER 07", S['chapter_num']))
    story.append(Paragraph("Conclusion", S['chapter_title']))
    story.append(SectionDivider())
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Synthesis &amp; Strategic Assessment", S['section_head']))
    story.append(Paragraph(
        "Domino's Pizza stands as one of the most compelling case studies in modern business history. "
        "From a single borrowed pizza store in 1960, it has grown into a $20+ billion enterprise "
        "operating across more than 90 countries — powered almost entirely by a franchise model "
        "that aligns the incentives of independent entrepreneurs with the strategic goals of "
        "a global brand.", S['body']))

    story.append(Paragraph(
        "What distinguishes Domino's from its competitors is not merely scale, but a series of "
        "deliberate, often courageous strategic decisions. Few brands in history have publicly "
        "acknowledged their product failures and rebuilt from the ground up. Fewer still have "
        "invested so heavily in becoming a technology company operating in the food business, "
        "rather than a food company dabbling in technology.", S['body']))

    story.append(Paragraph("Five Pillars of Domino's Enduring Success", S['section_head']))
    pillars = [
        ("1. The Franchise Engine", "An exceptionally well-structured franchise system that gives "
         "entrepreneurs a proven path to success while providing the corporate entity with capital-"
         "light, royalty-rich revenue at scale."),
        ("2. Technology as Competitive Moat", "Years of investment in ordering platforms, "
         "supply chain technology, and data analytics have created barriers to imitation that "
         "pure food companies cannot easily replicate."),
        ("3. Delivery DNA", "Built from inception for delivery — not adapted to it — gives "
         "Domino's inherent speed and efficiency advantages that dine-in competitors cannot easily match."),
        ("4. Radical Accountability", "The willingness to publicly acknowledge failure (the 2010 "
         "pizza reinvention) and adapt strategy to market realities (Uber Eats partnership) "
         "reflects a management culture that prioritizes long-term brand health over short-term pride."),
        ("5. Value &amp; Accessibility", "A price-competitive product portfolio ensures Domino's "
         "remains relevant across economic cycles, providing defensive characteristics that "
         "premium food brands cannot offer."),
    ]
    for pillar_title, pillar_desc in pillars:
        story.append(Paragraph(f"<b>{pillar_title}:</b> {pillar_desc}", S['bullet']))
        story.append(Spacer(1, 0.1*cm))

    story.append(Paragraph("Challenges on the Horizon", S['section_head']))
    future_challenges = [
        "Sustained labor market pressures and rising minimum wages in key markets",
        "Intensifying competition from ghost kitchens and cloud restaurant platforms",
        "Growing consumer health consciousness requiring menu evolution",
        "Managing quality consistency across 20,000+ franchise locations globally",
        "Navigating geopolitical volatility in emerging market expansions",
        "Technology maintenance and cybersecurity at global operating scale",
        "Environmental and sustainability expectations (packaging, carbon footprint)",
    ]
    for fc in future_challenges:
        story.append(Paragraph(f"• {fc}", S['bullet']))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Final Observations", S['section_head']))
    story.append(Paragraph(
        "The Domino's story demonstrates that sustainable business growth requires more than a "
        "good product — it requires adaptability, a clear value proposition, scalable systems, "
        "and the courage to make transformational decisions even when it means acknowledging "
        "past failures. For aspiring franchisees, business students, and strategic thinkers, "
        "Domino's provides a masterclass in brand resilience, franchise management, and "
        "technology-driven competitive differentiation.", S['body']))

    story.append(Paragraph(
        "As the food delivery landscape continues to evolve — with AI-driven personalization, "
        "autonomous delivery vehicles, and virtual brand proliferation reshaping the industry — "
        "Domino's appears well-positioned to leverage its foundational strengths. The company "
        "that once nearly collapsed under quality criticism now sets the standard for what a "
        "modern, technology-forward franchise network can achieve.", S['body']))

    story.append(Spacer(1, 0.4*cm))
    story.append(info_box(
        '"Domino\'s is a technology company that happens to sell pizza — '
        'and that distinction is the secret to its extraordinary success."',
        S['quote'], bg=colors.HexColor("#EEF3F8"), border=DOMINOS_RED))

    story.append(Spacer(1, 0.5*cm))

    # Final summary table
    story.append(Paragraph("Executive Summary Scorecard", S['section_head']))
    scorecard = [
        ["Dimension", "Assessment", "Rating"],
        ["Brand Strength", "Global recognition, 60+ year heritage", "⭐⭐⭐⭐⭐"],
        ["Franchise Model", "Efficient, proven, high franchisee success rate", "⭐⭐⭐⭐⭐"],
        ["Technology", "Industry-leading digital ordering ecosystem", "⭐⭐⭐⭐⭐"],
        ["Financial Performance", "Consistent revenue growth, strong margins", "⭐⭐⭐⭐"],
        ["Competitive Position", "Leader in pizza delivery, under aggregator pressure", "⭐⭐⭐⭐"],
        ["Innovation", "Strong track record; ongoing investment required", "⭐⭐⭐⭐"],
        ["Sustainability & Health", "Lagging; requires strategic investment", "⭐⭐⭐"],
        ["Global Expansion", "Robust pipeline; geopolitical risks managed", "⭐⭐⭐⭐"],
    ]
    story.append(std_table(scorecard[0], scorecard[1:], [5*cm, 7*cm, 2.7*cm]))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "This report was prepared for academic and informational purposes. All statistics and "
        "data points are drawn from publicly available Domino's annual reports, SEC filings, "
        "press releases, and credible industry research sources.",
        S['caption']))

    return story


def main():
    out = os.path.join(os.path.dirname(__file__), "Dominos_Pizza_Franchise_Report.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    doc = SimpleDocTemplate(
        out,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2.8*cm,
        bottomMargin=2.2*cm,
        title="Domino's Pizza – Franchise Business Analysis Report",
        author="Research & Analytics Division",
        subject="Franchise Analysis",
    )

    story = build_report()

    def cover_template(c, d):
        if d.page == 1:
            cover_canvas(c, d)
        else:
            make_canvas(c, d)

    doc.build(story, onFirstPage=cover_template, onLaterPages=make_canvas)
    print(f"PDF saved: {out}")

if __name__ == "__main__":
    main()
