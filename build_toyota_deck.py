import sys
import os

# Import the branded-pptx-deck toolkit
sys.path.insert(0, r"C:\Users\sheke\.gemini\config\skills\branded-pptx-deck\scripts")
from pptxkit import Deck, Inches, Pt, PP_ALIGN

def build_toyota_presentation():
    # Initialize the Branded Deck Builder
    d = Deck(footer="sales-research-pipeline · Toyota Strategy Briefing | 2026")
    b = d.b

    # 1. TITLE SLIDE (Navy Background)
    s1 = d.slide(fill=b.NAVY)
    d.text(s1, "SITUATION ASSESSMENT & SALES STRATEGY", d.M, Inches(1.2), Inches(10), Inches(0.4), size=14, color=b.TEAL, bold=True)
    d.text(s1, "Toyota US Digital Platform & Fleet Strategy", d.M, Inches(1.8), Inches(11.5), Inches(2.2), size=40, color=b.WHITE, bold=True, shrink=True)
    d.text(s1, "Automated pre-call briefing prepared for Toyota Digital & Fleet Operations", d.M, Inches(4.2), Inches(10), Inches(0.5), size=16, color=b.SOFT, italic=True)
    d.footer(s1, 1, 4, dark=True)

    # 2. CURRENT INVENTORY & LEASING SPECIFICS
    s2 = d.slide(fill=b.WHITE)
    d.header(s2, "Toyota 2026 Product Pipeline & Active Campaigns", "BLUF: Competitive lease campaigns and financing are driving model volume across SUV, Truck, and EV lines.")
    
    # Left Column: SUV & Performance Listings
    d.text(s2, "SUV & PERFORMANCE UTILITIES", d.M, Inches(1.8), Inches(5.8), Inches(0.4), size=14, color=b.NAVY, bold=True)
    suv_bullets = [
        {"text": "2026 4Runner Lease Campaign: Currently promoted at $409/month for 36 months ($3,699 due at signing) to capture off-road enthusiast segment.", "bullet": True, "space_before": 8, "size": 13},
        {"text": "2026 Grand Highlander: Core family utility model advertised at $449/month for 36 months ($4,639 due at signing) to drive high-capacity sales.", "bullet": True, "space_before": 8, "size": 13},
        {"text": "2026 GRMN Corolla Performance Marketing: 'Born on the Nürburgring' performance hatchback building brand engagement with younger demographics.", "bullet": True, "space_before": 8, "size": 13}
    ]
    d.text(s2, suv_bullets, d.M, Inches(2.3), Inches(5.8), Inches(4.5), color=b.INK, shrink=True)

    # Right Column: Trucks & EVs Financing
    d.text(s2, "TRUCKS & EV INCENTIVES", d.M + Inches(6.2), Inches(1.8), Inches(5.8), Inches(0.4), size=14, color=b.NAVY, bold=True)
    truck_bullets = [
        {"text": "2026 Tacoma Truck Lineup: Supported by a 3.99% APR financing offer for 48 months to maintain light-truck segment leadership.", "bullet": True, "space_before": 8, "size": 13},
        {"text": "2026 bZ Series EV Incentives: Offered at aggressive 0% APR for 72 months to accelerate battery-electric vehicle (BEV) fleet adoption.", "bullet": True, "space_before": 8, "size": 13},
        {"text": "Localized Special Checkout: Leads route to regional dealer incentives tables based on user ZIP codes, introducing drop-off friction.", "bullet": True, "space_before": 8, "size": 13}
    ]
    d.text(s2, truck_bullets, d.M + Inches(6.2), Inches(2.3), Inches(5.8), Inches(4.5), color=b.INK, shrink=True)
    
    d.footer(s2, 2, 4)

    # 3. TENSION: LEAD GENERATION & CONVERSATIONAL GAPS
    s3 = d.slide(fill=b.WHITE)
    d.header(s3, "The Digital Opportunity: Bridging Special Offers to Leads", "High-intent users searching regional lease specials experience checkout and redirect friction.")
    
    # Left Column: User Flow Analysis
    d.text(s3, "CURRENT USER FLOW FRICTION", d.M, Inches(1.8), Inches(5.8), Inches(0.4), size=14, color=b.NAVY, bold=True)
    flow_bullets = [
        {"text": "Static Lease Specials: Shoppers must manually browse multi-row tables to calculate payments and verify local dealer specials.", "bullet": True, "space_before": 8, "size": 13},
        {"text": "Disconnected Booking Paths: Transitioning from vehicle configurator to scheduling a local test drive requires starting a new form path.", "bullet": True, "space_before": 8, "size": 13},
        {"text": "B2B Fleet Drop-offs: Fleet/Tacoma business inquiries are routed to generic dealer contact sheets, adding 24h-48h lead response delays.", "bullet": True, "space_before": 8, "size": 13}
    ]
    d.text(s3, flow_bullets, d.M, Inches(2.3), Inches(5.8), Inches(4.5), color=b.INK, shrink=True)

    # Right Column: AI Automation Solution
    d.text(s3, "AI-POWERED ENGAGEMENT ARCHITECTURE", d.M + Inches(6.2), Inches(1.8), Inches(5.8), Inches(0.4), size=14, color=b.NAVY, bold=True)
    ai_bullets = [
        {"text": "Conversational Lease Assistants: Deploy interactive AI assistants on lease special landing pages to instantly qualify shopper intent.", "bullet": True, "space_before": 8, "size": 13},
        {"text": "Direct-to-Dealer Booking: Seamlessly coordinate available vehicle test drives directly with local dealership APIs.", "bullet": True, "space_before": 8, "size": 13},
        {"text": "Real-time Fleet Qualification: Automated B2B routing paths to immediately qualify and schedule sales calls for commercial accounts.", "bullet": True, "space_before": 8, "size": 13}
    ]
    d.text(s3, ai_bullets, d.M + Inches(6.2), Inches(2.3), Inches(5.8), Inches(4.5), color=b.INK, shrink=True)

    d.footer(s3, 3, 4)

    # 4. ACTION PLAN & RECOMMENDATIONS
    s4 = d.slide(fill=b.WHITE)
    d.header(s4, "Proposed Pilot Initiative & Execution Roadmap", "Implementing high-intent pre-sales automation pilots with measurable performance metrics.")

    # Table layout for actions
    y_offset = Inches(1.8)
    
    actions = [
        {
            "num": "01",
            "title": "Conversational Pre-qualification Widget",
            "action": "Deploy conversational qualify-and-match widget on regional lease special pages.",
            "owner": "Digital Marketing Dir.",
            "date": "Q3 2026",
            "metric": "+18% Lead Conv."
        },
        {
            "num": "02",
            "title": "B2B Fleet Lead Routing Automation",
            "action": "Implement real-time qualification paths for commercial truck/Tacoma buyers.",
            "owner": "Sales Ops Manager",
            "date": "Q3 2026",
            "metric": "Response < 5 Mins"
        },
        {
            "num": "03",
            "title": "Re-engagement Cart Drop-out Flows",
            "action": "Trigger automated CRM/email follow-up sequences for users dropping out of configuration.",
            "owner": "CRM Lead",
            "date": "Q4 2026",
            "metric": "12% Re-engage"
        }
    ]

    for item in actions:
        # Box background
        d.rect(s4, d.M, y_offset, d.CW, Inches(1.3), b.SOFT, radius=0.03)
        
        # Circle / Badge
        d.rect(s4, d.M + Inches(0.2), y_offset + Inches(0.25), Inches(0.8), Inches(0.8), b.TEAL, radius=0.5)
        d.text(s4, item["num"], d.M + Inches(0.2), y_offset + Inches(0.4), Inches(0.8), Inches(0.5), size=18, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        
        # Title and Description
        text_content = [
            {"text": item["title"].upper(), "bold": True, "size": 12, "color": b.NAVY},
            {"text": "\n" + item["action"], "size": 13, "color": b.INK}
        ]
        d.text(s4, text_content, d.M + Inches(1.2), y_offset + Inches(0.2), Inches(6.0), Inches(0.9))
        
        # Owner & Date
        owner_content = [
            {"text": "OWNER: " + item["owner"], "bold": True, "size": 10, "color": b.MUTED},
            {"text": "\nDATE: " + item["date"], "size": 11, "color": b.INK}
        ]
        d.text(s4, owner_content, d.M + Inches(7.5), y_offset + Inches(0.2), Inches(2.2), Inches(0.9))
        
        # Metric
        metric_content = [
            {"text": "TARGET METRIC", "bold": True, "size": 10, "color": b.NAVY},
            {"text": "\n" + item["metric"], "bold": True, "size": 14, "color": b.TEAL}
        ]
        d.text(s4, metric_content, d.M + Inches(9.8), y_offset + Inches(0.2), Inches(2.0), Inches(0.9))
        
        y_offset += Inches(1.5)

    d.footer(s4, 4, 4)

    # Save presentation
    out_path = os.path.abspath("prospects/toyota_com/Toyota_Strategy_Deck.pptx")
    d.save(out_path)
    print(f"[+] Saved branded deck to: {out_path}")

if __name__ == '__main__':
    build_toyota_presentation()
