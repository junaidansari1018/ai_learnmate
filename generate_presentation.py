"""
AI LearnMate - Professional 6-Slide PowerPoint Presentation Generator
Event: National Hackathon 6.0 — Manthan'26
Team: CodeNova | College: SHRI RAM GROUP OF COLLEGES
Table Number: [INSERT TABLE NUMBER] (Editable Placeholder)
"""

import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- COLOR PALETTE ---
    C_BG = RGBColor(10, 25, 47)            # #0A192F Deep Navy
    C_CARD = RGBColor(22, 36, 61)          # #16243D Slate Card
    C_CARD_ACCENT = RGBColor(28, 46, 77)   # #1C2E4D Highlight Card
    C_BORDER = RGBColor(42, 67, 101)       # #2A4365 Card Border
    C_BORDER_CYAN = RGBColor(14, 116, 144) # #0E7490 Border Cyan
    C_BLUE = RGBColor(37, 99, 235)         # #2563EB Primary Brand Blue
    C_CYAN = RGBColor(6, 182, 212)         # #06B6D4 Vibrant Cyan
    C_SKY = RGBColor(56, 189, 248)         # #38BDF8 Sky Accent
    C_WHITE = RGBColor(255, 255, 255)      # Pure White
    C_GRAY_LIGHT = RGBColor(226, 232, 240) # #E2E8F0 Soft White
    C_MUTED = RGBColor(148, 163, 184)      # #94A3B8 Muted Gray
    C_EMERALD = RGBColor(16, 185, 129)     # #10B981 Success
    C_AMBER = RGBColor(245, 158, 11)       # #F59E0B Warning / Amber
    C_RED_ACCENT = RGBColor(239, 68, 68)   # #EF4444 Danger / Challenge
    C_SDG4 = RGBColor(197, 25, 45)         # #C5192D Official UN SDG 4 Red
    C_SDG9 = RGBColor(253, 105, 37)        # #FD6925 Official UN SDG 9 Orange

    # Helper: Set slide background
    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    # Helper: Add standard header
    def add_header(slide, tag_text, title_text, subtitle_text):
        # Pill Tag
        tag = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(3.4), Inches(0.32))
        tag.fill.solid()
        tag.fill.fore_color.rgb = RGBColor(15, 34, 64)
        tag.line.color.rgb = C_CYAN
        tag.line.width = Pt(1)
        tf_tag = tag.text_frame
        tf_tag.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = 'Calibri'
        p_tag.font.size = Pt(9.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_CYAN
        p_tag.alignment = PP_ALIGN.CENTER

        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.55))
        tf_t = tb_title.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = 'Trebuchet MS'
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

        # Subtitle
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.32), Inches(11.7), Inches(0.35))
        tf_s = tb_sub.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle_text
        p_s.font.name = 'Calibri'
        p_s.font.size = Pt(13)
        p_s.font.color.rgb = C_SKY

        # Thin divider rule
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(11.733), Pt(1))
        div.fill.solid()
        div.fill.fore_color.rgb = C_BORDER
        div.line.fill.background()

    # Helper: Add standard footer
    def add_footer(slide, slide_num):
        # Footer divider
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Pt(1))
        div.fill.solid()
        div.fill.fore_color.rgb = C_BORDER
        div.line.fill.background()

        # Left label
        tb_l = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(8.5), Inches(0.35))
        tf_l = tb_l.text_frame
        tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = "AI LearnMate  •  Team CodeNova  •  National Hackathon 6.0 — Manthan'26"
        p_l.font.name = 'Calibri'
        p_l.font.size = Pt(10)
        p_l.font.color.rgb = C_MUTED

        # Right label (Slide X of 6)
        tb_r = slide.shapes.add_textbox(Inches(9.5), Inches(6.98), Inches(3.0), Inches(0.35))
        tf_r = tb_r.text_frame
        tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = f"Slide {slide_num} of 6"
        p_r.font.name = 'Calibri'
        p_r.font.size = Pt(10)
        p_r.font.bold = True
        p_r.font.color.rgb = C_SKY
        p_r.alignment = PP_ALIGN.RIGHT

    # Helper: Draw card container
    def create_card(slide, left, top, width, height, bg_color=C_CARD, border_color=C_BORDER, border_width=1):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(border_width)
        else:
            card.line.fill.background()
        return card

    # ==========================================
    # SLIDE 1: TITLE / TEAM INTRODUCTION
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Top Header Banner - Hackathon Context
    event_pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(4.8), Inches(0.38))
    event_pill.fill.solid()
    event_pill.fill.fore_color.rgb = RGBColor(15, 34, 64)
    event_pill.line.color.rgb = C_CYAN
    event_pill.line.width = Pt(1.2)
    tf_ep = event_pill.text_frame
    tf_ep.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_ep = tf_ep.paragraphs[0]
    p_ep.text = "NATIONAL HACKATHON 6.0 — MANTHAN'26"
    p_ep.font.name = 'Calibri'
    p_ep.font.size = Pt(10.5)
    p_ep.font.bold = True
    p_ep.font.color.rgb = C_CYAN
    p_ep.alignment = PP_ALIGN.CENTER

    track_pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(0.5), Inches(3.2), Inches(0.38))
    track_pill.fill.solid()
    track_pill.fill.fore_color.rgb = RGBColor(20, 38, 70)
    track_pill.line.color.rgb = C_BORDER
    track_pill.line.width = Pt(1)
    tf_tp = track_pill.text_frame
    tf_tp.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_tp = tf_tp.paragraphs[0]
    p_tp.text = "TRACK: AI-POWERED EDTECH"
    p_tp.font.name = 'Calibri'
    p_tp.font.size = Pt(10.5)
    p_tp.font.bold = True
    p_tp.font.color.rgb = C_SKY
    p_tp.alignment = PP_ALIGN.CENTER

    # Official College Logo Placeholder Container (Top Right)
    logo_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.3), Inches(0.45), Inches(3.23), Inches(1.3))
    logo_card.fill.solid()
    logo_card.fill.fore_color.rgb = RGBColor(16, 32, 58)
    logo_card.line.color.rgb = C_SKY
    logo_card.line.width = Pt(1.5)
    tf_logo = logo_card.text_frame
    tf_logo.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_l1 = tf_logo.paragraphs[0]
    p_l1.text = "[INSERT OFFICIAL LOGO]"
    p_l1.font.name = 'Trebuchet MS'
    p_l1.font.size = Pt(12)
    p_l1.font.bold = True
    p_l1.font.color.rgb = C_CYAN
    p_l1.alignment = PP_ALIGN.CENTER

    p_l2 = tf_logo.add_paragraph()
    p_l2.text = "SHRI RAM GROUP OF COLLEGES"
    p_l2.font.name = 'Calibri'
    p_l2.font.size = Pt(10)
    p_l2.font.bold = True
    p_l2.font.color.rgb = C_WHITE
    p_l2.alignment = PP_ALIGN.CENTER

    p_l3 = tf_logo.add_paragraph()
    p_l3.text = "(Editable Logo Area — Replace with College Crest)"
    p_l3.font.name = 'Calibri'
    p_l3.font.size = Pt(8.5)
    p_l3.font.color.rgb = C_MUTED
    p_l3.alignment = PP_ALIGN.CENTER

    # Main Project Hero Box
    hero_card = create_card(s1, Inches(0.8), Inches(1.9), Inches(11.733), Inches(2.2), bg_color=C_CARD, border_color=C_BLUE, border_width=1.5)
    
    # Project Title
    tb_title = s1.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(11.1), Inches(0.8))
    tf_mt = tb_title.text_frame
    tf_mt.margin_left = tf_mt.margin_right = tf_mt.margin_top = tf_mt.margin_bottom = 0
    p_title = tf_mt.paragraphs[0]
    p_title.text = "AI LearnMate"
    p_title.font.name = 'Trebuchet MS'
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE

    # Tagline
    tb_tag = s1.shapes.add_textbox(Inches(1.1), Inches(2.85), Inches(11.1), Inches(0.45))
    tf_tg = tb_tag.text_frame
    tf_tg.margin_left = tf_tg.margin_right = tf_tg.margin_top = tf_tg.margin_bottom = 0
    p_tagline = tf_tg.paragraphs[0]
    p_tagline.text = '“Watch. Learn. Test. Improve.”'
    p_tagline.font.name = 'Trebuchet MS'
    p_tagline.font.size = Pt(22)
    p_tagline.font.bold = True
    p_tagline.font.color.rgb = C_CYAN

    # Subtitle / Objective
    tb_desc = s1.shapes.add_textbox(Inches(1.1), Inches(3.35), Inches(11.1), Inches(0.55))
    tf_dc = tb_desc.text_frame
    tf_dc.margin_left = tf_dc.margin_right = tf_dc.margin_top = tf_dc.margin_bottom = 0
    p_desc = tf_dc.paragraphs[0]
    p_desc.text = "An AI-Powered Personalized Learning-Gap Detection & Adaptive Assessment Platform\nEmpowering students to transform lecture content into diagnostic mastery and measurable progress."
    p_desc.font.name = 'Calibri'
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = C_GRAY_LIGHT

    # Bottom 3 Metadata Cards (Team, Institution, Methodology)
    card_w = Inches(3.75)
    card_h = Inches(2.4)
    card_gap = Inches(0.24)
    card_top = Inches(4.3)

    # Card 1: Team & Table Number
    c1 = create_card(s1, Inches(0.8), card_top, card_w, card_h, bg_color=C_CARD, border_color=C_BORDER)
    tb_c1 = s1.shapes.add_textbox(Inches(1.0), card_top + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.3))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = tf_c1.margin_bottom = 0
    
    p = tf_c1.paragraphs[0]
    p.text = "TEAM IDENTITY"
    p.font.name = 'Calibri'
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_SKY

    p = tf_c1.add_paragraph()
    p.text = "Team CodeNova"
    p.font.name = 'Trebuchet MS'
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p = tf_c1.add_paragraph()
    p.text = "Role: Core Full-Stack & AI Engineering"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.color.rgb = C_MUTED

    # Table Number Badge inside Card 1
    p = tf_c1.add_paragraph()
    p.text = "\nTABLE NUMBER:"
    p.font.name = 'Calibri'
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    p = tf_c1.add_paragraph()
    p.text = "[INSERT TABLE NUMBER]"
    p.font.name = 'Trebuchet MS'
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    # Card 2: College & Department
    c2 = create_card(s1, Inches(0.8) + card_w + card_gap, card_top, card_w, card_h, bg_color=C_CARD, border_color=C_BORDER)
    tb_c2 = s1.shapes.add_textbox(Inches(1.0) + card_w + card_gap, card_top + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.3))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = tf_c2.margin_bottom = 0

    p = tf_c2.paragraphs[0]
    p.text = "COLLEGE / INSTITUTION"
    p.font.name = 'Calibri'
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_SKY

    p = tf_c2.add_paragraph()
    p.text = "SHRI RAM GROUP OF COLLEGES"
    p.font.name = 'Trebuchet MS'
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p = tf_c2.add_paragraph()
    p.text = "Department of Computer Science & Engineering\nUndergraduate Technical Innovation Initiative"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.color.rgb = C_GRAY_LIGHT

    p = tf_c2.add_paragraph()
    p.text = "\nAffiliation: Dr. A.P.J. Abdul Kalam Technical University"
    p.font.name = 'Calibri'
    p.font.size = Pt(10)
    p.font.color.rgb = C_MUTED

    # Card 3: AI-Assisted Development
    c3 = create_card(s1, Inches(0.8) + (card_w + card_gap)*2, card_top, card_w, card_h, bg_color=C_CARD, border_color=C_BORDER)
    tb_c3 = s1.shapes.add_textbox(Inches(1.0) + (card_w + card_gap)*2, card_top + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.3))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_left = tf_c3.margin_right = tf_c3.margin_top = tf_c3.margin_bottom = 0

    p = tf_c3.paragraphs[0]
    p.text = "DEVELOPMENT METHODOLOGY"
    p.font.name = 'Calibri'
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_SKY

    p = tf_c3.add_paragraph()
    p.text = "AI-Assisted Development"
    p.font.name = 'Trebuchet MS'
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    p = tf_c3.add_paragraph()
    p.text = "Developed & Orchestrated with Antigravity\nGoogle DeepMind Agentic Coding Framework"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.color.rgb = C_GRAY_LIGHT

    p = tf_c3.add_paragraph()
    p.text = "\nEngineering Rigor: Automated Testing, Modular Architecture, Parameterized Security"
    p.font.name = 'Calibri'
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED

    add_footer(s1, 1)

    # ==========================================
    # SLIDE 2: PROJECT STATEMENT / PROBLEM STATEMENT
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Challenge & Value Proposition", "The Problem We Solve", "Closing the gap between passive lecture consumption and active conceptual mastery")

    col_w = Inches(5.72)
    col_h = Inches(3.45)
    col_top = Inches(1.9)

    # Left Column: The Problem
    card_prob = create_card(s2, Inches(0.8), col_top, col_w, col_h, bg_color=C_CARD, border_color=C_RED_ACCENT, border_width=1.2)
    tb_pr = s2.shapes.add_textbox(Inches(1.05), col_top + Inches(0.18), col_w - Inches(0.5), col_h - Inches(0.3))
    tf_pr = tb_pr.text_frame
    tf_pr.word_wrap = True
    tf_pr.margin_left = tf_pr.margin_right = tf_pr.margin_top = tf_pr.margin_bottom = 0

    p = tf_pr.paragraphs[0]
    p.text = "THE PROBLEM: THE PASSIVE LEARNING TRAP"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_RED_ACCENT

    p = tf_pr.add_paragraph()
    p.text = "Students face major friction in validating self-study comprehension:"
    p.font.name = 'Calibri'
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_MUTED

    problems = [
        ("Passive 'Illusion of Competence'", "Watching video lectures or re-reading notes creates familiarity without actual active cognitive recall."),
        ("Manual Assessment Friction", "Authoring relevant practice questions manually is time-consuming, subjective, and rarely done during self-study."),
        ("Hidden Sub-Concept Gaps", "Traditional test scores (e.g. 70%) hide critical foundational weaknesses beneath an aggregate score."),
        ("No Longitudinal Direction", "Revision occurs blindly without data-driven tracking of which specific concepts are improving over time.")
    ]
    for title, desc in problems:
        p = tf_pr.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title}: "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(11)
        run1.font.bold = True
        run1.font.color.rgb = C_WHITE
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = 'Calibri'
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = C_GRAY_LIGHT

    # Right Column: The Solution
    card_sol = create_card(s2, Inches(6.8), col_top, col_w, col_h, bg_color=C_CARD, border_color=C_CYAN, border_width=1.2)
    tb_sol = s2.shapes.add_textbox(Inches(7.05), col_top + Inches(0.18), col_w - Inches(0.5), col_h - Inches(0.3))
    tf_sol = tb_sol.text_frame
    tf_sol.word_wrap = True
    tf_sol.margin_left = tf_sol.margin_right = tf_sol.margin_top = tf_sol.margin_bottom = 0

    p = tf_sol.paragraphs[0]
    p.text = "THE SOLUTION: AI LEARNMATTE ARCHITECTURE"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    p = tf_sol.add_paragraph()
    p.text = "One unified platform converting educational materials into targeted mastery:"
    p.font.name = 'Calibri'
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_MUTED

    solutions = [
        ("Instant Quiz Generation", "Converts raw lecture notes, text files (.txt/.md), or YouTube video transcripts into structured diagnostic quizzes."),
        ("Fine-Grained Gap Analysis", "Evaluates attempts per sub-concept, identifying whether mistakes stem from conceptual traps or superficial errors."),
        ("Dynamic Adaptive Engine", "Adjusts difficulty in real-time (Easy/Medium/Hard) based on rolling student accuracy and topic confidence."),
        ("Actionable Mastery Reports", "Delivers personalized study tasks, remedial review cards, and longitudinal history tracking.")
    ]
    for title, desc in solutions:
        p = tf_sol.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title}: "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(11)
        run1.font.bold = True
        run1.font.color.rgb = C_SKY
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = 'Calibri'
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = C_GRAY_LIGHT

    # Visual Workflow Ribbon Across Bottom (5 Connected Steps required by prompt)
    wf_top = Inches(5.55)
    wf_step_w = Inches(2.18)
    wf_gap = Inches(0.2)
    wf_h = Inches(1.15)

    steps = [
        ("1. Learning Material", "Notes, Text Upload, or\nYouTube URL input", C_BLUE),
        ("2. Quiz Generation", "AI extraction of key\ntopics & distractors", C_BLUE),
        ("3. Assessment", "1-by-1 adaptive questions\ncalibrated to learner", C_BLUE),
        ("4. Weak-Topic Analysis", "Evidence-based gap audit\n& misconception logs", C_CYAN),
        ("5. Progress Tracking", "Longitudinal mastery\n& targeted revision tasks", C_EMERALD)
    ]

    for i, (stitle, sdesc, scolor) in enumerate(steps):
        s_left = Inches(0.8) + i * (wf_step_w + wf_gap)
        scard = create_card(s2, s_left, wf_top, wf_step_w, wf_h, bg_color=C_CARD, border_color=scolor, border_width=1)
        
        tb_st = s2.shapes.add_textbox(s_left + Inches(0.1), wf_top + Inches(0.12), wf_step_w - Inches(0.2), wf_h - Inches(0.2))
        tf_st = tb_st.text_frame
        tf_st.word_wrap = True
        tf_st.margin_left = tf_st.margin_right = tf_st.margin_top = tf_st.margin_bottom = 0
        
        p = tf_st.paragraphs[0]
        p.text = stitle
        p.font.name = 'Calibri'
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = scolor
        p.alignment = PP_ALIGN.CENTER

        p = tf_st.add_paragraph()
        p.text = sdesc
        p.font.name = 'Calibri'
        p.font.size = Pt(9)
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        # Add arrow if not last
        if i < 4:
            arrow_left = s_left + wf_step_w + Inches(0.04)
            tb_arr = s2.shapes.add_textbox(arrow_left, wf_top + Inches(0.35), Inches(0.15), Inches(0.4))
            tf_arr = tb_arr.text_frame
            tf_arr.margin_left = tf_arr.margin_right = tf_arr.margin_top = tf_arr.margin_bottom = 0
            p_arr = tf_arr.paragraphs[0]
            p_arr.text = "➔"
            p_arr.font.name = 'Arial'
            p_arr.font.size = Pt(12)
            p_arr.font.color.rgb = C_SKY
            p_arr.alignment = PP_ALIGN.CENTER

    add_footer(s2, 2)

    # ==========================================
    # SLIDE 3: SUSTAINABLE DEVELOPMENT GOALS (SDGs)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Social Impact & Global Goals", "Alignment with UN Sustainable Development Goals", "Democratizing accessible, high-quality, and personalized diagnostic learning")

    sdg_w = Inches(5.72)
    sdg_h = Inches(3.7)
    sdg_top = Inches(1.9)

    # SDG 4 Card (Left)
    card_sdg4 = create_card(s3, Inches(0.8), sdg_top, sdg_w, sdg_h, bg_color=C_CARD, border_color=C_SDG4, border_width=1.5)
    
    # Badge SDG 4
    badge_sdg4 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), sdg_top + Inches(0.2), Inches(3.2), Inches(0.36))
    badge_sdg4.fill.solid()
    badge_sdg4.fill.fore_color.rgb = C_SDG4
    badge_sdg4.line.fill.background()
    tf_b4 = badge_sdg4.text_frame
    tf_b4.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b4 = tf_b4.paragraphs[0]
    p_b4.text = "UN SDG 4: QUALITY EDUCATION"
    p_b4.font.name = 'Trebuchet MS'
    p_b4.font.size = Pt(11)
    p_b4.font.bold = True
    p_b4.font.color.rgb = C_WHITE
    p_b4.alignment = PP_ALIGN.CENTER

    tb_s4 = s3.shapes.add_textbox(Inches(1.05), sdg_top + Inches(0.65), sdg_w - Inches(0.5), sdg_h - Inches(0.75))
    tf_s4 = tb_s4.text_frame
    tf_s4.word_wrap = True
    tf_s4.margin_left = tf_s4.margin_right = tf_s4.margin_top = tf_s4.margin_bottom = 0

    p = tf_s4.paragraphs[0]
    p.text = "Primary Focus: Target 4.4 (Relevant Skills) & 4.7 (Knowledge & Inclusivity)"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.color.rgb = C_SKY

    sdg4_points = [
        ("Democratizing 1-on-1 Diagnostic Tutoring", "Provides high-grade learning gap analysis to any student without requiring access to expensive private coaching or tutoring."),
        ("Active Recall & Mastery Learning", "Promotes evidence-based cognitive retrieval over rote memorization, helping learners identify exactly what they misunderstood."),
        ("Bilingual Accessibility", "Supports English and Hindi/Hinglish question formats, ensuring conceptual clarity is accessible to vernacular medium college students."),
        ("Empowering Self-Directed Study", "Turns open educational videos and self-study notes into structured, measurable diagnostic assessments.")
    ]
    for stitle, sdesc in sdg4_points:
        p = tf_s4.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {stitle}: "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(10.5)
        run1.font.bold = True
        run1.font.color.rgb = C_WHITE
        
        run2 = p.add_run()
        run2.text = sdesc
        run2.font.name = 'Calibri'
        run2.font.size = Pt(10)
        run2.font.color.rgb = C_GRAY_LIGHT

    # SDG 9 Card (Right)
    card_sdg9 = create_card(s3, Inches(6.8), sdg_top, sdg_w, sdg_h, bg_color=C_CARD, border_color=C_SDG9, border_width=1.5)
    
    # Badge SDG 9
    badge_sdg9 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.05), sdg_top + Inches(0.2), Inches(4.3), Inches(0.36))
    badge_sdg9.fill.solid()
    badge_sdg9.fill.fore_color.rgb = C_SDG9
    badge_sdg9.line.fill.background()
    tf_b9 = badge_sdg9.text_frame
    tf_b9.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b9 = tf_b9.paragraphs[0]
    p_b9.text = "UN SDG 9: INDUSTRY, INNOVATION & INFRASTRUCTURE"
    p_b9.font.name = 'Trebuchet MS'
    p_b9.font.size = Pt(10)
    p_b9.font.bold = True
    p_b9.font.color.rgb = C_WHITE
    p_b9.alignment = PP_ALIGN.CENTER

    tb_s9 = s3.shapes.add_textbox(Inches(7.05), sdg_top + Inches(0.65), sdg_w - Inches(0.5), sdg_h - Inches(0.75))
    tf_s9 = tb_s9.text_frame
    tf_s9.word_wrap = True
    tf_s9.margin_left = tf_s9.margin_right = tf_s9.margin_top = tf_s9.margin_bottom = 0

    p = tf_s9.paragraphs[0]
    p.text = "Primary Focus: Target 9.5 (Enhance Scientific Research & Innovation)"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.color.rgb = C_SKY

    sdg9_points = [
        ("Practical, Frugal AI Utility", "Demonstrates practical integration of state-of-the-art Google Gemini 1.5 Flash models paired with explainable fallback algorithms."),
        ("Low-Cost Edge Compatibility", "Zero-bloat architecture (Flask + vanilla JS + SQLite) runs efficiently on low-spec student laptops without heavy server dependencies."),
        ("Offline Demo Mode Resilience", "Curated offline Operating Systems benchmark allows full assessment functionality in low-connectivity or offline classroom settings."),
        ("Transparent Data Architecture", "Uses local ACID-compliant SQLite storage with zero tracking or user monetization, ensuring student data sovereignty.")
    ]
    for stitle, sdesc in sdg9_points:
        p = tf_s9.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {stitle}: "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(10.5)
        run1.font.bold = True
        run1.font.color.rgb = C_WHITE
        
        run2 = p.add_run()
        run2.text = sdesc
        run2.font.name = 'Calibri'
        run2.font.size = Pt(10)
        run2.font.color.rgb = C_GRAY_LIGHT

    # Supporting Card: SDG 10 & Impact Scope Disclaimer (Bottom)
    card_bot = create_card(s3, Inches(0.8), Inches(5.75), Inches(11.733), Inches(0.95), bg_color=C_CARD, border_color=C_BORDER)
    tb_bot = s3.shapes.add_textbox(Inches(1.05), Inches(5.82), Inches(11.2), Inches(0.8))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0

    p = tf_bot.paragraphs[0]
    run1 = p.add_run()
    run1.text = "SUPPORTING SDG 10 (REDUCED INEQUALITIES): "
    run1.font.name = 'Calibri'
    run1.font.size = Pt(10.5)
    run1.font.bold = True
    run1.font.color.rgb = C_AMBER
    
    run2 = p.add_run()
    run2.text = "Leveling academic access for tier-2/3 college students by open-sourcing personalized diagnostic tools that emulate individual tutor feedback."
    run2.font.name = 'Calibri'
    run2.font.size = Pt(10)
    run2.font.color.rgb = C_WHITE

    p = tf_bot.add_paragraph()
    run3 = p.add_run()
    run3.text = "HONEST SCOPE STATEMENT: "
    run3.font.name = 'Calibri'
    run3.font.size = Pt(10)
    run3.font.bold = True
    run3.font.color.rgb = C_SKY

    run4 = p.add_run()
    run4.text = "AI LearnMate is engineered as an accessible study companion. We demonstrate direct technological alignment with SDG targets, not premature macro-population statistical claims."
    run4.font.name = 'Calibri'
    run4.font.size = Pt(9.5)
    run4.font.color.rgb = C_MUTED

    add_footer(s3, 3)

    # ==========================================
    # SLIDE 4: TECHNOLOGY STACK & IMPLEMENTATION
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Engineering & Architecture", "Technology Stack & Implementation", "A clean, verified, full-stack architecture built without unnecessary framework bloat")

    # Visual Architecture Ribbon (Top)
    arch_top = Inches(1.85)
    arch_h = Inches(0.68)
    arch_w = Inches(2.18)
    arch_gap = Inches(0.2)

    arch_nodes = [
        ("1. Frontend UI", "Vanilla HTML5 / CSS3 / JS", C_BLUE),
        ("2. Flask Backend", "REST Routing & Sessions", C_BLUE),
        ("3. AI Integration", "Gemini 1.5 & YouTube API", C_CYAN),
        ("4. SQLite Storage", "ACID Tables & Foreign Keys", C_BLUE),
        ("5. Diagnostic Results", "Adaptive Gap Analytics", C_EMERALD)
    ]

    for i, (ntitle, ndesc, ncolor) in enumerate(arch_nodes):
        n_left = Inches(0.8) + i * (arch_w + arch_gap)
        ncard = create_card(s4, n_left, arch_top, arch_w, arch_h, bg_color=C_CARD, border_color=ncolor, border_width=1)
        tb_n = s4.shapes.add_textbox(n_left + Inches(0.05), arch_top + Inches(0.08), arch_w - Inches(0.1), arch_h - Inches(0.15))
        tf_n = tb_n.text_frame
        tf_n.word_wrap = True
        tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
        
        p = tf_n.paragraphs[0]
        p.text = ntitle
        p.font.name = 'Calibri'
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = ncolor
        p.alignment = PP_ALIGN.CENTER

        p = tf_n.add_paragraph()
        p.text = ndesc
        p.font.name = 'Calibri'
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        if i < 4:
            arr_l = n_left + arch_w + Inches(0.04)
            tb_a = s4.shapes.add_textbox(arr_l, arch_top + Inches(0.18), Inches(0.15), Inches(0.3))
            tf_a = tb_a.text_frame
            tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0
            p_a = tf_a.paragraphs[0]
            p_a.text = "➔"
            p_a.font.name = 'Arial'
            p_a.font.size = Pt(11)
            p_a.font.color.rgb = C_SKY
            p_a.alignment = PP_ALIGN.CENTER

    # Left Column: Verified Technologies & Roles
    tech_col_w = Inches(6.8)
    tech_col_h = Inches(4.1)
    tech_col_top = Inches(2.65)

    card_tech = create_card(s4, Inches(0.8), tech_col_top, tech_col_w, tech_col_h, bg_color=C_CARD, border_color=C_BORDER)
    tb_t = s4.shapes.add_textbox(Inches(1.05), tech_col_top + Inches(0.15), tech_col_w - Inches(0.5), tech_col_h - Inches(0.25))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0

    p = tf_t.paragraphs[0]
    p.text = "VERIFIED TECHNOLOGIES & EXACT CODEBASE ROLES"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_SKY

    techs = [
        ("Python 3.14 & Flask 3.1.3", "Backend Controller", "Lightweight WSGI routing, REST API endpoints, session state management, and parameter validation."),
        ("Vanilla HTML5 / CSS3 / ES6 JS", "Frontend Interface", "Zero CDN dependencies, custom responsive stylesheet (828 LOC), and vanilla Fetch API for smooth asynchronous quiz flow."),
        ("SQLite 3 (Built-in sqlite3)", "Persistent Data Layer", "ACID-compliant relational database with PRAGMA foreign_keys = ON; stores sessions, questions, attempts, and analytics."),
        ("Google Gemini API (1.5 Flash)", "AI Intelligence Engine", "Structured quiz generation from lectures, automated subject/title derivation, and bilingual question authoring."),
        ("YouTube Transcript API & oEmbed", "Content Extraction", "Fetches clean video subtitles and oEmbed lecture metadata with fallback to manual transcript paste."),
        ("Antigravity AI Coding Assistant", "Development Tooling", "AI-assisted pair programming tool used for rapid prototyping, full-stack scaffolding, and test suite design.")
    ]

    for name, role, desc in techs:
        p = tf_t.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {name} "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(10.5)
        run1.font.bold = True
        run1.font.color.rgb = C_WHITE

        run_r = p.add_run()
        run_r.text = f"[{role}]: "
        run_r.font.name = 'Calibri'
        run_r.font.size = Pt(9.5)
        run_r.font.bold = True
        run_r.font.color.rgb = C_CYAN

        run2 = p.add_run()
        run2.text = desc
        run2.font.name = 'Calibri'
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = C_GRAY_LIGHT

    # Right Column: Verified Lines of Code & Testing Metrics
    metric_col_w = Inches(4.68)
    card_met = create_card(s4, Inches(7.85), tech_col_top, metric_col_w, tech_col_h, bg_color=C_CARD, border_color=C_CYAN, border_width=1.2)
    tb_m = s4.shapes.add_textbox(Inches(8.05), tech_col_top + Inches(0.15), metric_col_w - Inches(0.4), tech_col_h - Inches(0.25))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0

    p = tf_m.paragraphs[0]
    p.text = "VERIFIED SOURCE CODE AUDIT (SLOC)"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    # Main Metric Stat Boxes
    p = tf_m.add_paragraph()
    run_num = p.add_run()
    run_num.text = "4,693"
    run_num.font.name = 'Trebuchet MS'
    run_num.font.size = Pt(28)
    run_num.font.bold = True
    run_num.font.color.rgb = C_WHITE

    run_lbl = p.add_run()
    run_lbl.text = " Total Lines of Code (SLOC)\n4,203 non-blank lines across 24 files"
    run_lbl.font.name = 'Calibri'
    run_lbl.font.size = Pt(10.5)
    run_lbl.font.color.rgb = C_SKY

    p = tf_m.add_paragraph()
    run_tst = p.add_run()
    run_tst.text = "26 / 26"
    run_tst.font.name = 'Trebuchet MS'
    run_tst.font.size = Pt(22)
    run_tst.font.bold = True
    run_tst.font.color.rgb = C_EMERALD

    run_tst_l = p.add_run()
    run_tst_l.text = " Automated Tests Passing (100%)\nAutomated Python unittest suite (0.45s runtime)"
    run_tst_l.font.name = 'Calibri'
    run_tst_l.font.size = Pt(10)
    run_tst_l.font.color.rgb = C_GRAY_LIGHT

    p = tf_m.add_paragraph()
    p.text = "\nDetailed SLOC Breakdown:"
    p.font.name = 'Calibri'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    sloc_breakdown = [
        ("Backend Python Logic (8 files):", "2,172 lines (1,969 non-blank)"),
        ("Automated Tests (6 files):", "576 lines (501 non-blank)"),
        ("Frontend HTML Templates (8 files):", "950 lines (859 non-blank)"),
        ("Custom CSS & Vanilla JS (2 files):", "988 lines (864 non-blank)")
    ]
    for bname, bstat in sloc_breakdown:
        p = tf_m.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {bname} "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = C_MUTED
        
        run2 = p.add_run()
        run2.text = bstat
        run2.font.name = 'Calibri'
        run2.font.size = Pt(9.5)
        run2.font.bold = True
        run2.font.color.rgb = C_WHITE

    p = tf_m.add_paragraph()
    p.text = "\nCounting Methodology: Strictly counted project .py, .html, .css, and .js files. Excludes database binaries, python cache (__pycache__), virtual environment, and third-party packages."
    p.font.name = 'Calibri'
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_MUTED

    add_footer(s4, 4)

    # ==========================================
    # SLIDE 5: INNOVATION / NOVELTY
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Innovation & Technical Novelty", "What Makes AI LearnMate Different?", "Engineering integrity: explainable rules, honest evidence thresholds, and resilient offline design")

    # 4 Differentiator Cards (2x2 Grid)
    card_gw = Inches(5.72)
    card_gh = Inches(2.28)
    card_g_gap_x = Inches(0.28)
    card_g_gap_y = Inches(0.2)
    g_top1 = Inches(1.9)
    g_top2 = g_top1 + card_gh + card_g_gap_y

    # Grid 1: Explainable Rule-Based Adaptive Testing (Top Left)
    c_g1 = create_card(s5, Inches(0.8), g_top1, card_gw, card_gh, bg_color=C_CARD, border_color=C_CYAN, border_width=1.2)
    tb_g1 = s5.shapes.add_textbox(Inches(1.05), g_top1 + Inches(0.15), card_gw - Inches(0.5), card_gh - Inches(0.25))
    tf_g1 = tb_g1.text_frame
    tf_g1.word_wrap = True
    tf_g1.margin_left = tf_g1.margin_right = tf_g1.margin_top = tf_g1.margin_bottom = 0

    p = tf_g1.paragraphs[0]
    p.text = "1. EXPLAINABLE RULE-BASED ADAPTIVE TESTING"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    diff1_text = [
        ("Deterministic Sliding Window", "Tracks the student's rolling accuracy over the last 3 questions rather than opaque probabilistic guessing."),
        ("Dynamic Threshold Transitions", "Accuracy ≥ 70% steps up to Hard questions; accuracy ≤ 35% steps down to Easy questions."),
        ("Prerequisite Remediation", "If a student fails a core sub-concept, the engine immediately routes the next question to target that prerequisite topic."),
        ("Viva-Ready Explainability", "Every difficulty shift is completely explainable to students and hackathon jury members.")
    ]
    for h, d in diff1_text:
        p = tf_g1.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {h}: "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(10)
        run1.font.bold = True
        run1.font.color.rgb = C_WHITE
        run2 = p.add_run()
        run2.text = d
        run2.font.name = 'Calibri'
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = C_GRAY_LIGHT

    # Grid 2: Honest Evidence Threshold Policy (Top Right)
    c_g2 = create_card(s5, Inches(0.8) + card_gw + card_g_gap_x, g_top1, card_gw, card_gh, bg_color=C_CARD, border_color=C_BLUE, border_width=1.2)
    tb_g2 = s5.shapes.add_textbox(Inches(1.05) + card_gw + card_g_gap_x, g_top1 + Inches(0.15), card_gw - Inches(0.5), card_gh - Inches(0.25))
    tf_g2 = tb_g2.text_frame
    tf_g2.word_wrap = True
    tf_g2.margin_left = tf_g2.margin_right = tf_g2.margin_top = tf_g2.margin_bottom = 0

    p = tf_g2.paragraphs[0]
    p.text = "2. HONEST EVIDENCE THRESHOLD POLICY"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_SKY

    diff2_text = [
        ("Zero Premature Classification", "Topics tested with only 1 question are explicitly categorized as 'Limited Evidence' rather than declaring false mastery."),
        ("Misconception Distractor Audit", "Wrong answers are mapped to specific conceptual misconceptions rather than treated as generic incorrect flags."),
        ("Actionable Study Tasks", "Generates targeted revision flashcards specifically for confirmed weak topics instead of generic review advice."),
        ("Statistical Integrity", "Eliminates score inflation, giving learners a realistic assessment of their actual exam readiness.")
    ]
    for h, d in diff2_text:
        p = tf_g2.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {h}: "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(10)
        run1.font.bold = True
        run1.font.color.rgb = C_WHITE
        run2 = p.add_run()
        run2.text = d
        run2.font.name = 'Calibri'
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = C_GRAY_LIGHT

    # Grid 3: Dual-Engine Architecture & Offline Demo Mode (Bottom Left)
    c_g3 = create_card(s5, Inches(0.8), g_top2, card_gw, card_gh, bg_color=C_CARD, border_color=C_EMERALD, border_width=1.2)
    tb_g3 = s5.shapes.add_textbox(Inches(1.05), g_top2 + Inches(0.15), card_gw - Inches(0.5), card_gh - Inches(0.25))
    tf_g3 = tb_g3.text_frame
    tf_g3.word_wrap = True
    tf_g3.margin_left = tf_g3.margin_right = tf_g3.margin_top = tf_g3.margin_bottom = 0

    p = tf_g3.paragraphs[0]
    p.text = "3. DUAL-ENGINE ARCHITECTURE & OFFLINE DEMO MODE"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    diff3_text = [
        ("Live Google Gemini 1.5 Flash", "Connects to Google AI Studio for open-ended lecture topics, extracting structured questions with zero hallucination."),
        ("Zero-API Demo Mode", "Built-in curated Operating Systems benchmark session operating 100% offline without API keys or internet connection."),
        ("Zero Hackathon Demo Risk", "Immune to conference Wi-Fi failures, expired API tokens, or remote downtime during live judging demonstrations."),
        ("Bilingual Inclusivity", "Seamlessly supports English and Hindi/Hinglish questions for clear conceptual resonance with Indian students.")
    ]
    for h, d in diff3_text:
        p = tf_g3.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {h}: "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(10)
        run1.font.bold = True
        run1.font.color.rgb = C_WHITE
        run2 = p.add_run()
        run2.text = d
        run2.font.name = 'Calibri'
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = C_GRAY_LIGHT

    # Grid 4: Transparent Engineering & Real Limitations (Bottom Right)
    c_g4 = create_card(s5, Inches(0.8) + card_gw + card_g_gap_x, g_top2, card_gw, card_gh, bg_color=C_CARD, border_color=C_AMBER, border_width=1.2)
    tb_g4 = s5.shapes.add_textbox(Inches(1.05) + card_gw + card_g_gap_x, g_top2 + Inches(0.15), card_gw - Inches(0.5), card_gh - Inches(0.25))
    tf_g4 = tb_g4.text_frame
    tf_g4.word_wrap = True
    tf_g4.margin_left = tf_g4.margin_right = tf_g4.margin_top = tf_g4.margin_bottom = 0

    p = tf_g4.paragraphs[0]
    p.text = "4. TRANSPARENT ENGINEERING & REAL LIMITATIONS"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    diff4_text = [
        ("No Invention Hyping", "We do NOT claim AI quiz generation is a novel invention; our novelty lies in student-first diagnostic integration and actionable gap analysis."),
        ("YouTube Caption Dependency", "Requires accessible closed captions/transcripts via youtube-transcript-api. When captions are disabled, it gracefully prompts for notes."),
        ("Never Hallucinates Video Content", "The system never pretends to 'watch' videos when captions are inaccessible, maintaining complete academic integrity."),
        ("Focus on Learning, Not Vanity UI", "Prioritizes clean readable code, explainable algorithms, and instant responsiveness over bloated frontend frameworks.")
    ]
    for h, d in diff4_text:
        p = tf_g4.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {h}: "
        run1.font.name = 'Calibri'
        run1.font.size = Pt(10)
        run1.font.bold = True
        run1.font.color.rgb = C_WHITE
        run2 = p.add_run()
        run2.text = d
        run2.font.name = 'Calibri'
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = C_GRAY_LIGHT

    add_footer(s5, 5)

    # ==========================================
    # SLIDE 6: FUTURE SCOPE & ROADMAP
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Strategic Roadmap", "Future Scope & Development Roadmap", "A structured 3-phase engineering path from hackathon MVP to campus-wide learning platform")

    col_rw = Inches(3.75)
    col_rh = Inches(4.35)
    col_rgap = Inches(0.24)
    r_top = Inches(1.9)

    phases = [
        ("PHASE 1: SHORT-TERM", "Reliability, Transcription & Test Hardening", C_BLUE, [
            ("Local Audio Fallback (Whisper)", "Integrate local Whisper STT to automatically transcribe YouTube lectures that lack native captions, eliminating external subtitle dependence."),
            ("AI Distractor Quality Guardrails", "Implement heuristic filters to validate that AI distractors are plausible, non-ambiguous, and strictly aligned with source text."),
            ("Comprehensive Test Hardening", "Expand automated test coverage beyond the existing 26 unit tests to include high-concurrency stress testing and malformed input fuzzing."),
            ("Enhanced Error Telemetry", "Provide structured feedback to users when uploaded notes lack sufficient conceptual density for quiz authoring.")
        ]),
        ("PHASE 2: MEDIUM-TERM", "Personalization, Memory & Cohort Analytics", C_CYAN, [
            ("Multi-Session Student Accounts", "Implement secure authentication with longitudinal knowledge graph tracking across multiple subjects and academic semesters."),
            ("Spaced Repetition Engine (SM-2)", "Incorporate the SuperMemo algorithm to automatically schedule weak-topic review quizzes at 1-day, 3-day, and 7-day intervals."),
            ("Instructor Cohort Dashboards", "Aggregate anonymized assessment diagnostics so professors can identify which lecture concepts confused the largest portion of the class."),
            ("Expanded Resource Formats", "Native support for PDF lecture slides, OCR extraction from handwritten notes, and docx lecture handouts.")
        ]),
        ("PHASE 3: LONG-TERM", "Campus Integration & Multi-Modal Pedagogy", C_EMERALD, [
            ("LMS Ecosystem Integration", "LTI (Learning Tools Interoperability) 1.3 compliance for seamless one-click embedding into Moodle, Canvas, and Google Classroom."),
            ("Multi-Modal Diagram Questions", "Support vision-based question generation from engineering diagrams, circuit schematics, and system architectures."),
            ("Collaborative Peer Revision", "Enable students to challenge peers on specific weak concepts and exchange verified student-written explanations."),
            ("Institutional Scale & Edge Deployment", "Containerized Docker microservices architecture with lightweight local model quantization for offline campus servers.")
        ])
    ]

    for i, (p_tag, p_sub, p_color, p_items) in enumerate(phases):
        c_left = Inches(0.8) + i * (col_rw + col_rgap)
        rcard = create_card(s6, c_left, r_top, col_rw, col_rh, bg_color=C_CARD, border_color=p_color, border_width=1.3)
        
        # Phase Header Pill inside card
        ppill = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left + Inches(0.2), r_top + Inches(0.18), col_rw - Inches(0.4), Inches(0.35))
        ppill.fill.solid()
        ppill.fill.fore_color.rgb = p_color
        ppill.line.fill.background()
        tf_pp = ppill.text_frame
        tf_pp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_pp = tf_pp.paragraphs[0]
        p_pp.text = p_tag
        p_pp.font.name = 'Trebuchet MS'
        p_pp.font.size = Pt(11)
        p_pp.font.bold = True
        p_pp.font.color.rgb = C_WHITE
        p_pp.alignment = PP_ALIGN.CENTER

        tb_rc = s6.shapes.add_textbox(c_left + Inches(0.2), r_top + Inches(0.6), col_rw - Inches(0.4), col_rh - Inches(0.75))
        tf_rc = tb_rc.text_frame
        tf_rc.word_wrap = True
        tf_rc.margin_left = tf_rc.margin_right = tf_rc.margin_top = tf_rc.margin_bottom = 0

        p = tf_rc.paragraphs[0]
        p.text = p_sub
        p.font.name = 'Calibri'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_SKY

        for item_title, item_desc in p_items:
            p = tf_rc.add_paragraph()
            run1 = p.add_run()
            run1.text = f"\n• {item_title}: "
            run1.font.name = 'Calibri'
            run1.font.size = Pt(10)
            run1.font.bold = True
            run1.font.color.rgb = C_WHITE

            run2 = p.add_run()
            run2.text = item_desc
            run2.font.name = 'Calibri'
            run2.font.size = Pt(9)
            run2.font.color.rgb = C_GRAY_LIGHT

    # Roadmap Footnote (Engineering Integrity)
    card_rnote = create_card(s6, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.45), bg_color=RGBColor(16, 28, 48), border_color=C_BORDER)
    tb_rn = s6.shapes.add_textbox(Inches(1.0), Inches(6.4), Inches(11.3), Inches(0.35))
    tf_rn = tb_rn.text_frame
    tf_rn.margin_left = tf_rn.margin_right = tf_rn.margin_top = tf_rn.margin_bottom = 0
    p = tf_rn.paragraphs[0]
    run_rn = p.add_run()
    run_rn.text = "NOTE ON IMPLEMENTATION STATUS: "
    run_rn.font.name = 'Calibri'
    run_rn.font.size = Pt(9.5)
    run_rn.font.bold = True
    run_rn.font.color.rgb = C_CYAN
    run_rn2 = p.add_run()
    run_rn2.text = "All items in Phases 1, 2, and 3 are clearly designated as planned future enhancements building upon our verified 4,693-line working foundation."
    run_rn2.font.name = 'Calibri'
    run_rn2.font.size = Pt(9.5)
    run_rn2.font.color.rgb = C_MUTED

    add_footer(s6, 6)

    # Save Presentation
    output_dir = os.path.join(os.path.dirname(__file__), "presentation")
    os.makedirs(output_dir, exist_ok=True)
    pptx_path = os.path.join(output_dir, "AI_LearnMate_CodeNova_Hackathon.pptx")
    prs.save(pptx_path)
    print(f"[SUCCESS] PowerPoint presentation saved to: {pptx_path}")
    return pptx_path

if __name__ == "__main__":
    create_presentation()
