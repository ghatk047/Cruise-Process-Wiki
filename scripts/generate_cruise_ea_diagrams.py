#!/usr/bin/env python3
"""
Cruise Process Wiki — EA Diagram Generator
Generates 10 highly detailed Enterprise Architecture diagrams for Royal Caribbean Group.
Renders PNG via mmdc, pushes to GitHub, builds wiki HTML pages.

Usage:
  python3 scripts/generate_cruise_ea_diagrams.py
  python3 scripts/generate_cruise_ea_diagrams.py --only EA-03
  python3 scripts/generate_cruise_ea_diagrams.py --dry-run
"""

import argparse, base64, os, re, subprocess, sys, time
from datetime import datetime
from html import escape
from pathlib import Path

try:
    import requests
except ImportError:
    os.system("pip3 install requests --break-system-packages -q"); import requests

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
GH_TOKEN  = os.environ.get("GH_TOKEN", "YOUR_TOKEN_HERE")  # set via env or replace
GH_REPO   = "ghatk047/Cruise-Process-Wiki"
GH_API    = "https://api.github.com"
BASE_DIR  = Path.home() / "Projects/cruise-wiki"
DIAG_DIR  = BASE_DIR / "ea-diagrams"
IMG_DIR   = BASE_DIR / "assets/img"

NOW = datetime.now().strftime("%Y-%m-%d %H:%M")

def ts():
    return datetime.now().strftime("%H:%M:%S")

def log(msg, kind="info"):
    icons = {"info":"   ","ok":"✅ ","warn":"⚠️  ","err":"❌ ","head":"🚀 ","step":"→  ","push":"📤 "}
    print(f"[{ts()}] {icons.get(kind,'   ')} {msg}", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# 10 EA DIAGRAMS — FULL MERMAID SOURCE
# ─────────────────────────────────────────────────────────────────────────────

EA_DIAGRAMS = [

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-01",
"title": "Cruise Integrated System Landscape",
"subtitle": "Full application landscape across all 12 operational domains — Royal Caribbean International reference",
"description": "The Royal Caribbean International system landscape maps every application to its operational domain. Oracle Hospitality Cruise SPMS sits at the shipboard hub, while the proprietary RES reservation system anchors shore-side booking. 14 major platforms span from external booking channels and port authorities through guest operations, onboard revenue, marine management, environmental compliance, and enterprise back-office — all interconnected via Starlink satellite linking ship and shore in near-real-time.",
"notes": [
    "RES (proprietary, 9M+ lines RPG) is the core reservation system — all bookings flow through it",
    "Oracle SPMS is the shipboard hub equivalent of an airport AODB — all ship operations reference it",
    "Starlink connectivity (98% of fleet, sub-100ms latency) enables near-real-time ship-shore data sync",
    "SAP S/4HANA handles all shore-side finance; voyage accounting journals post from SPMS nightly",
    "IDEMIA MFACE facial recognition deployed at US homeports for sub-8-second debarkation",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart TB

  subgraph EXT["🌐 External Channels & Partners"]
    direction LR
    GDS["GDS / OTAs\\nSabre · Amadeus · Expedia"]
    TRAVELAGENT["Travel Agents\\nCruising Power Portal"]
    PORT["Port Authorities\\nCBP · Coast Guard · IMO"]
    WEATHER["Weather & Nav\\nMetOcean · NAVTEX · GPS"]
    SHIPYARD["Shipyard Partners\\nGrand Bahama · Fincantieri"]
  end

  subgraph BOOKING["🎫 Booking & Reservation"]
    direction LR
    RES["RES System\\nCore Reservation (9M+ RPG lines)\\nBooking · Pricing · Inventory"]
    ROYALWEB["Royal Caribbean Web\\n& Mobile App (Guest Booking)"]
    CRM["Salesforce CRM\\nGuest Profiles · Campaign Mgmt"]
    LOYALTY["Crown & Anchor\\nLoyalty Platform (6 tiers)"]
  end

  subgraph SHIPBOARD["🚢 Shipboard Operations Hub"]
    direction LR
    SPMS["Oracle Hospitality Cruise SPMS\\nPMS · Folio · Cabin Mgmt · Manifest"]
    MICROS["Oracle MICROS Simphony\\nF&B POS · Retail · Spa · Casino POS"]
    ROYALAPP["Royal Caribbean App\\nNLP AI Chatbot · Bookings · Maps"]
    SEAPASS["SeaPass Cashless System\\nOnboard Account · RFID Card"]
    MFACE["IDEMIA MFACE\\n3D Facial Recognition · Debarkation"]
  end

  subgraph MARINE["⚙️ Marine & Technical"]
    direction LR
    NAVSYS["Integrated Navigation\\nECDIS · AIS · GMDSS · Radar"]
    PMS["Planned Maintenance System\\nEngine · Hull · Equipment"]
    ENVIRO["Environmental Systems\\nBWTS · AWTS · Scrubbers · OWS"]
    VDR["Voyage Data Recorder\\nSOLAS Mandatory · Incident Archive"]
    LNG["LNG Fuel Management\\nIcon Class Dual-Fuel"]
  end

  subgraph REVENUE["💰 Onboard Revenue"]
    direction LR
    CASINO["Club Royale Casino\\nIGT Slots · Bravo Poker · Loyalty"]
    SPA["Vitality Spa\\nBooking · POS · Therapist Schedule"]
    PHOTO["Photo & Media\\nOnboard Photography Sales"]
    EXCURSION["Shore Excursions Platform\\nCocoCay · Partner Operators"]
  end

  subgraph CONNECTIVITY["📡 Connectivity & Digital"]
    direction LR
    STARLINK["Starlink Satellite\\n98% Fleet · sub-100ms latency"]
    AZURE["Microsoft Azure AI\\nCrowd Density · Queue Mgmt"]
    MICROSERV["Mesosphere/D2iQ\\nShip-Shore Microservices"]
    OBIEE["Oracle OBIEE\\nCruise Ship Analytics · BI"]
  end

  subgraph CREW["👥 Crew & HR"]
    direction LR
    WORKDAY["Workday HCM\\nCrew Contracts · Payroll · STCW"]
    SCHEDULE["Crew Scheduling\\nRoster · Watch Keeping · Hours"]
    TRAINING["STCW Training Portal\\nCertification Tracking"]
  end

  subgraph ENTERPRISE["💼 Enterprise Back-Office"]
    direction LR
    SAP["SAP S/4HANA\\nFinance · Controlling · GL · AR/AP"]
    ARIBA["SAP Ariba\\nProcurement · Supplier Portal"]
    PORTDISB["Port Disbursement\\nAgent Invoicing · Port Fees"]
  end

  GDS         -->|"bookings · availability"| RES
  TRAVELAGENT -->|"bookings via API"| RES
  ROYALWEB    -->|"direct bookings"| RES
  RES         -->|"reservation data"| SPMS
  RES         -->|"guest profiles"| CRM
  RES         -->|"loyalty points"| LOYALTY
  CRM         -->|"marketing data"| RES

  PORT        -->|"clearance · manifests"| SPMS
  WEATHER     -->|"routing data"| NAVSYS

  SPMS  -->|"folio charges"| MICROS
  SPMS  -->|"guest account"| SEAPASS
  SPMS  -->|"manifest"| MFACE
  SPMS  -->|"ops data nightly"| OBIEE
  SPMS  -->|"voyage journal"| SAP

  MICROS  -->|"revenue postings"| SPMS
  SEAPASS -->|"spend data"| MICROS
  ROYALAPP -->|"bookings · requests"| SPMS
  ROYALAPP -->|"chat logs"| AZURE

  CASINO   -->|"revenue"| MICROS
  SPA      -->|"revenue"| MICROS
  PHOTO    -->|"revenue"| MICROS
  EXCURSION -->|"revenue"| MICROS

  NAVSYS  -->|"position data"| VDR
  NAVSYS  -->|"engine telemetry"| PMS
  PMS     -->|"maintenance costs"| SAP
  ENVIRO  -->|"compliance logs"| SAP
  LNG     -->|"fuel costs"| SAP

  STARLINK -->|"ship-shore sync"| MICROSERV
  MICROSERV -->|"data replication"| SPMS
  MICROSERV -->|"data replication"| SAP
  AZURE    -->|"operational insights"| OBIEE

  WORKDAY  -->|"crew costs"| SAP
  SCHEDULE -->|"hours data"| WORKDAY
  TRAINING -->|"cert status"| WORKDAY

  SAP   -->|"payments"| ARIBA
  ARIBA -->|"purchase orders"| PORTDISB
  OBIEE -->|"revenue reports"| SAP

  style EXT         fill:#f0f4ff,stroke:#6366f1
  style BOOKING     fill:#fff3e0,stroke:#f59e0b
  style SHIPBOARD   fill:#e0f7fa,stroke:#06b6d4
  style MARINE      fill:#f3e8ff,stroke:#8b5cf6
  style REVENUE     fill:#fce4ec,stroke:#ec4899
  style CONNECTIVITY fill:#e8f5e9,stroke:#10b981
  style CREW        fill:#fff8e1,stroke:#f59e0b
  style ENTERPRISE  fill:#e3f2fd,stroke:#3b82f6
""",
},

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-02",
"title": "Guest Journey Data Flow",
"subtitle": "End-to-end data flows from initial booking through post-cruise loyalty — Royal Caribbean International",
"description": "This diagram traces every data handoff along the complete Royal Caribbean guest journey. A booking in the RES system triggers a chain of downstream events spanning pre-cruise communications, terminal check-in, IDEMIA MFACE facial recognition, SeaPass account activation, 5+ days of onboard spend capture via Oracle MICROS, final folio settlement, IDEMIA-assisted debarkation, and Crown & Anchor loyalty accrual — all feeding back into Salesforce CRM and SAP for post-voyage accounting.",
"notes": [
    "RES is the master booking record — all downstream systems derive guest identity from it",
    "eDocs processing triggers 72 hours before departure; Royal App push notification sent",
    "IDEMIA MFACE processes facial templates uploaded at check-in; debarkation <8 seconds per guest",
    "SeaPass RFID links physical card to SPMS folio; every onboard charge posts in <2 seconds",
    "Crown & Anchor loyalty points calculated from voyage spend and posted within 48h of disembarkation",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart LR

  subgraph PRECRUISE["📋 Pre-Cruise (T-90 to T-1 days)"]
    direction TB
    BOOKING["Guest Books\\nRES System / Web / GDS"]
    EDOCS["eDocs Processing\\nRES generates boarding docs"]
    APPDOWNLOAD["Royal App\\nGuest downloads & links booking"]
    CHECKINONLINE["Online Check-In\\nPassport · Health · Photo upload"]
    FACEENROLL["Face Template\\nIDEMIA MFACE pre-enrollment"]
  end

  subgraph TERMINAL["🏢 Embarkation Terminal"]
    direction TB
    TERMCHECK["Terminal Check-In\\nOracle SPMS validates documents"]
    SEAPASSISSUE["SeaPass Card Issued\\nRFID linked to SPMS folio account"]
    FACEMATCH["IDEMIA MFACE\\nFacial match → boarding clearance"]
    MANIFEST["CBP Manifest\\nSPMS submits to US Customs"]
    LUGGAGE["Luggage Tagging\\nBag tags printed · hold linked to cabin"]
  end

  subgraph ONBOARD["🚢 Onboard (Voyage Days 1–N)"]
    direction TB
    SPMS2["Oracle SPMS\\nLive folio · cabin · manifest hub"]
    MICROS2["Oracle MICROS POS\\nEvery F&B · retail · casino charge"]
    ROYALAPP2["Royal App\\nAI chat · show bookings · excursions"]
    EXCURSION2["Shore Excursions\\nBookings linked to SeaPass folio"]
    AZURE2["Azure AI\\nCrowd flow · queue analytics"]
    OBIEE2["Oracle OBIEE\\nDaily revenue analytics"]
  end

  subgraph SETTLEMENT["💳 Voyage Settlement (Final Night)"]
    direction TB
    FOLIO["Final Folio Review\\nSPMS auto-generates statement"]
    PAYMENT["Payment Processing\\nCredit card · SeaPass settlement"]
    DISPUTE["Dispute Resolution\\nGuest Services · SPMS adjustment"]
    VOYJOURNAL["Voyage Journal\\nSPMS posts to SAP S/4HANA"]
  end

  subgraph DEBARKATION["🏁 Debarkation"]
    direction TB
    LUGTAG["Luggage Tag Distribution\\nSPMS assigns colour-coded zones"]
    FACEDEPART["IDEMIA MFACE Debarkation\\nFacial match · CBP clearance"]
    CBPCLEAR["CBP Final Clearance\\nManifest reconciliation"]
    FEEDBACK["Post-Cruise Survey\\nSalesforce · NPS scoring"]
  end

  subgraph POSTCRUISE["⭐ Post-Cruise & Loyalty"]
    direction TB
    LOYALTY2["Crown & Anchor Points\\nCalculated from voyage spend"]
    CRM2["Salesforce CRM\\nVoyage record · next cruise propensity"]
    NEXTCRUISE["Next Cruise Offer\\nPersonalised via RES pricing engine"]
    SAPAR["SAP AR\\nFinal invoice · revenue recognition"]
  end

  BOOKING     -->|"reservation record"| EDOCS
  EDOCS       -->|"doc completion"| APPDOWNLOAD
  APPDOWNLOAD -->|"check-in data"| CHECKINONLINE
  CHECKINONLINE -->|"photo + passport"| FACEENROLL
  FACEENROLL  -->|"biometric template"| FACEMATCH

  EDOCS       -->|"booking manifest"| TERMCHECK
  TERMCHECK   -->|"guest validated"| SEAPASSISSUE
  SEAPASSISSUE -->|"folio opened"| SPMS2
  FACEMATCH   -->|"boarding clearance"| MANIFEST
  LUGGAGE     -->|"bag tag data"| SPMS2

  SPMS2   -->|"charge request"| MICROS2
  MICROS2 -->|"all spend postings"| SPMS2
  ROYALAPP2 -->|"booking requests"| SPMS2
  ROYALAPP2 -->|"interaction data"| AZURE2
  EXCURSION2 -->|"excursion charges"| MICROS2
  SPMS2   -->|"daily revenue data"| OBIEE2

  SPMS2   -->|"folio balance"| FOLIO
  FOLIO   -->|"payment request"| PAYMENT
  PAYMENT -->|"settled folio"| VOYJOURNAL
  DISPUTE -->|"adjusted folio"| PAYMENT
  VOYJOURNAL -->|"journal entries"| SAPAR

  SPMS2   -->|"zone assignments"| LUGTAG
  FACEDEPART -->|"depart confirmed"| CBPCLEAR
  CBPCLEAR -->|"closed manifest"| FEEDBACK

  FEEDBACK  -->|"NPS data"| CRM2
  CRM2      -->|"voyage history"| LOYALTY2
  LOYALTY2  -->|"updated tier"| NEXTCRUISE
  NEXTCRUISE -->|"offer trigger"| BOOKING
  SAPAR     -->|"revenue posted"| VOYJOURNAL

  style PRECRUISE    fill:#e8f4fd,stroke:#3b82f6
  style TERMINAL     fill:#fff3e0,stroke:#f59e0b
  style ONBOARD      fill:#e0f7fa,stroke:#06b6d4
  style SETTLEMENT   fill:#fce4ec,stroke:#ec4899
  style DEBARKATION  fill:#f3e8ff,stroke:#8b5cf6
  style POSTCRUISE   fill:#e8f5e9,stroke:#10b981
""",
},

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-03",
"title": "Shipboard Operations Architecture",
"subtitle": "Oracle SPMS as operational hub — all shipboard systems on Icon of the Seas",
"description": "Oracle Hospitality Cruise SPMS is the shipboard equivalent of an AODB — every operational system feeds into or pulls from it. This diagram shows the full SPMS integration web: guest-facing systems (Royal App, SeaPass, MICROS POS), operational systems (housekeeping, shore excursions, spa, casino), marine interfaces (navigation, maintenance), and connectivity layer (Starlink, Azure AI). All transactions reconcile nightly to shore-side SAP S/4HANA via the Mesosphere/D2iQ microservices bridge.",
"notes": [
    "SPMS manages 7,600 guest cabins on Icon of the Seas — each cabin has a real-time folio",
    "MICROS Simphony POS covers 40+ dining venues, 20+ bars, retail, spa, and casino on Icon class",
    "Royal App processes ~35% of all onboard service requests as of 2025",
    "Ship-shore data sync occurs every 15 minutes via Starlink during voyage; full reconciliation at end of voyage",
    "Azure AI monitors 20+ crowd density zones on Icon of the Seas for flow optimisation",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart TB

  subgraph GUESTFACING["👤 Guest-Facing Layer"]
    direction LR
    ROYALAPP3["Royal Caribbean App\\nAI Chatbot · Self-Service · Maps"]
    SEAPASS3["SeaPass RFID System\\nCashless · Door Key · ID"]
    KIOSK["Self-Service Kiosks\\nAccount · Excursions · Dining"]
    MFACE3["IDEMIA MFACE\\nEmbarkation · Debarkation"]
    FIDS3["Guest Info Displays\\nSailing info · Daily programme"]
  end

  subgraph SPMSCORE["🔵 Oracle SPMS — Shipboard Hub"]
    direction LR
    CABIN["Cabin Management\\nHousekeeping · Maintenance · Status"]
    FOLIO3["Guest Folio Engine\\nReal-time charges · Settlement"]
    MANIFEST3["Manifest & Safety\\nMuster · Emergency · CBP"]
    RESOURCE["Resource Scheduling\\nDining times · Show bookings"]
    REPORTING["Shipboard Reporting\\nRevenue · Ops · Compliance"]
  end

  subgraph POS["🍽️ Point-of-Sale Layer (Oracle MICROS)"]
    direction LR
    MDR["Main Dining Room\\n& Specialty Restaurants"]
    BARS["Bars & Lounges\\n20+ venues on Icon class"]
    RETAIL["Retail Shops\\nDuty Free · Logo · Jewellery"]
    SPA3["Vitality Spa\\n& Fitness Centre"]
    CASINO3["Casino Royale\\nSlots · Tables · Poker"]
  end

  subgraph OPERATIONS["⚙️ Operations Layer"]
    direction LR
    HOUSEKEEPING["Housekeeping System\\nCabin status · Linen · Scheduling"]
    EXCURSIONS3["Shore Excursions\\nBookings · Ticketing · Buses"]
    ENTERTAINMENT["Entertainment System\\nShow bookings · Capacity · Venues"]
    KIDS["Adventure Ocean\\nYouth programme · Check-in/out"]
    PHOTO3["Photo Gallery\\nCapture · Sales · Digital delivery"]
  end

  subgraph MARINE3["⚙️ Marine Layer"]
    direction LR
    NAVSYS3["Integrated Bridge\\nECDIS · AIS · Radar · GMDSS"]
    ENGINEPMS["Engine Room PMS\\nPlanned Maintenance · Alarms"]
    ENVIRO3["Environmental\\nBWTS · Scrubbers · Waste logs"]
    VDR3["Voyage Data Recorder\\nBlack box · Incident archive"]
  end

  subgraph CONNECTIVITY3["📡 Connectivity Layer"]
    direction LR
    STARLINK3["Starlink Satellite\\nsub-100ms · 98% fleet"]
    AZURE3["Azure AI Vision\\nCrowd density · People flow"]
    MICROSERV3["D2iQ Microservices\\nShip-Shore event bus"]
    SHIPNET["Ship LAN/WiFi\\nGuest · Crew · Operations VLANs"]
  end

  subgraph SHORELINK["🏢 Shore-Side Link"]
    direction LR
    RES3["RES System\\nBooking records"]
    SAP3["SAP S/4HANA\\nVoyage accounting"]
    OBIEE3["Oracle OBIEE\\nRevenue analytics"]
    WORKDAY3["Workday HCM\\nCrew payroll"]
  end

  ROYALAPP3  -->|"service requests"| SPMSCORE
  SEAPASS3   -->|"transactions"| FOLIO3
  KIOSK      -->|"bookings · queries"| SPMSCORE
  MFACE3     -->|"biometric clearance"| MANIFEST3
  FIDS3      -->|"schedule data"| RESOURCE

  MDR      -->|"F&B charges"| FOLIO3
  BARS     -->|"beverage charges"| FOLIO3
  RETAIL   -->|"retail charges"| FOLIO3
  SPA3     -->|"spa charges"| FOLIO3
  CASINO3  -->|"gaming charges"| FOLIO3

  HOUSEKEEPING -->|"cabin status"| CABIN
  EXCURSIONS3  -->|"excursion charges"| FOLIO3
  ENTERTAINMENT -->|"show bookings"| RESOURCE
  KIDS         -->|"youth check-in/out"| MANIFEST3
  PHOTO3       -->|"photo charges"| FOLIO3

  NAVSYS3    -->|"position · heading"| VDR3
  ENGINEPMS  -->|"maintenance alerts"| REPORTING
  ENVIRO3    -->|"compliance data"| REPORTING
  VDR3       -->|"voyage log"| REPORTING

  STARLINK3  -->|"bandwidth"| SHIPNET
  SHIPNET    -->|"traffic"| MICROSERV3
  AZURE3     -->|"crowd insights"| REPORTING
  MICROSERV3 -->|"sync events"| SHORELINK

  CABIN      -->|"housekeeping tasks"| HOUSEKEEPING
  FOLIO3     -->|"nightly journal"| SAP3
  MANIFEST3  -->|"manifest data"| RES3
  REPORTING  -->|"revenue data"| OBIEE3
  REPORTING  -->|"crew hours"| WORKDAY3

  style GUESTFACING   fill:#e0f7fa,stroke:#06b6d4
  style SPMSCORE      fill:#e3f2fd,stroke:#1d4ed8,stroke-width:3px
  style POS           fill:#fff3e0,stroke:#f59e0b
  style OPERATIONS    fill:#f3e8ff,stroke:#8b5cf6
  style MARINE3       fill:#fce4ec,stroke:#ef4444
  style CONNECTIVITY3 fill:#e8f5e9,stroke:#10b981
  style SHORELINK     fill:#f8fafc,stroke:#6b7280
""",
},

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-04",
"title": "Onboard Revenue Architecture",
"subtitle": "SeaPass → MICROS POS → SPMS folio → OBIEE analytics → SAP finance",
"description": "Every dollar of onboard revenue flows through a precise chain: a guest taps their SeaPass RFID card at a POS terminal, Oracle MICROS Simphony authorises the charge in under 2 seconds, posts it to the Oracle SPMS guest folio, which feeds the Oracle OBIEE analytics engine for real-time revenue dashboards, and ultimately posts to SAP S/4HANA at voyage-end. This diagram shows the full revenue chain from 40+ revenue centres on Icon of the Seas through to shore-side financial close.",
"notes": [
    "Icon of the Seas has 40+ dining venues, 20+ bars, multiple retail shops, spa, casino, entertainment — all on MICROS",
    "SeaPass RFID tap-to-pay authorisation is under 2 seconds at any MICROS terminal",
    "Club Royale casino loyalty tiers: Choice, Prime, Signature, Masters — each with different revenue share",
    "OBIEE dashboards refresh every 15 minutes during voyage via Starlink sync",
    "Voyage-end revenue journal to SAP includes FX conversion for multi-currency voyages",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart LR

  subgraph GUESTWALLET["💳 Guest Payment Layer"]
    direction TB
    SEAPASS4["SeaPass RFID Card\\nLinked to credit card · onboard account"]
    ROYALAPP4["Royal App\\nMobile payments · pre-bookings"]
    CASH["Cash / Pre-paid\\nFX exchange · credit deposit"]
    NEXTCRUISE4["Next Cruise Deposits\\nFuture booking credits"]
  end

  subgraph REVCENTRES["🏪 Revenue Centres (40+ on Icon class)"]
    direction TB
    FB4["Food & Beverage\\nMDR · Specialty · Buffet · Room Service · Bars"]
    RETAIL4["Retail\\nDuty Free · Logo Shop · Jewellery · Art"]
    SPA4["Spa & Wellness\\nVitality Spa · Salon · Fitness"]
    CASINO4["Casino Royale\\nSlots (IGT) · Tables · Bravo Poker"]
    ENTERTAINMENT4["Entertainment\\nShow upgrades · Experiences · FlowRider"]
    EXCURSION4["Shore Excursions\\nCocoCay · Port operators · Private"]
    PHOTO4["Photo & Media\\nOnboard photography · Video packages"]
    WIFI["WiFi Packages\\nVoom internet · Starlink-backed"]
  end

  subgraph MICROS4["🟠 Oracle MICROS Simphony POS Layer"]
    direction TB
    TERMINAL["POS Terminal\\nFOH order capture · SeaPass tap"]
    KITCHEN["Kitchen Display System\\nOrder routing · prep timing"]
    INVENTORY["F&B Inventory\\nRecipe costing · waste tracking"]
    VOIDAUTH["Void & Comp Auth\\nManager approval · discount rules"]
  end

  subgraph SPMSFOLIO["🔵 Oracle SPMS Folio Engine"]
    direction TB
    GUESTFOLIO["Guest Folio\\nReal-time balance · charge history"]
    GROUPFOLIO["Group & Package Folios\\nInclusions · upgrades · overages"]
    SHIPFOLIO["Ship Revenue Ledger\\nDaily revenue by centre"]
    SETTLEMENT4["Settlement Processing\\nCard auth · disputes · refunds"]
  end

  subgraph ANALYTICS4["📊 Analytics & Reporting"]
    direction TB
    OBIEE4["Oracle OBIEE\\nLive revenue dashboards"]
    REVMGMT["Revenue Management\\nYield · spend-per-guest KPIs"]
    FORECAST["Voyage Forecast\\nActual vs budget · variance"]
    LOYALTY4["Club Royale Tracking\\nGaming spend · tier qualification"]
  end

  subgraph FINANCE4["💼 Finance & Close"]
    direction TB
    SAP4["SAP S/4HANA\\nVoyage revenue journals"]
    SAPAR4["SAP AR\\nGuest billing · FX conversion"]
    TAXCOMP["Tax & Compliance\\nVAT · casino regulations"]
    CONSOL["Fleet Consolidation\\nMulti-ship revenue roll-up"]
  end

  SEAPASS4    -->|"RFID tap"| TERMINAL
  ROYALAPP4   -->|"pre-orders"| TERMINAL
  CASH        -->|"deposit"| GUESTFOLIO
  NEXTCRUISE4 -->|"credits"| GUESTFOLIO

  FB4         -->|"F&B orders"| TERMINAL
  RETAIL4     -->|"retail sales"| TERMINAL
  SPA4        -->|"spa charges"| TERMINAL
  CASINO4     -->|"gaming markers"| TERMINAL
  ENTERTAINMENT4 -->|"activity charges"| TERMINAL
  EXCURSION4  -->|"tour charges"| TERMINAL
  PHOTO4      -->|"photo purchases"| TERMINAL
  WIFI        -->|"package activations"| TERMINAL

  TERMINAL -->|"order to kitchen"| KITCHEN
  TERMINAL -->|"item depletion"| INVENTORY
  TERMINAL -->|"charge post"| GUESTFOLIO
  VOIDAUTH -->|"approved comp"| GUESTFOLIO

  GUESTFOLIO  -->|"daily summary"| SHIPFOLIO
  GROUPFOLIO  -->|"group charges"| SHIPFOLIO
  SHIPFOLIO   -->|"revenue feed"| OBIEE4
  SETTLEMENT4 -->|"payment result"| GUESTFOLIO

  OBIEE4   -->|"KPI data"| REVMGMT
  OBIEE4   -->|"actuals"| FORECAST
  OBIEE4   -->|"gaming data"| LOYALTY4
  REVMGMT  -->|"pricing signals"| EXCURSION4

  SHIPFOLIO -->|"end-of-voyage journal"| SAP4
  SAP4      -->|"AR entries"| SAPAR4
  SAP4      -->|"tax postings"| TAXCOMP
  SAP4      -->|"fleet roll-up"| CONSOL

  style GUESTWALLET  fill:#e0f7fa,stroke:#06b6d4
  style REVCENTRES   fill:#fff3e0,stroke:#f59e0b
  style MICROS4      fill:#fff8e1,stroke:#f59e0b,stroke-width:2px
  style SPMSFOLIO    fill:#e3f2fd,stroke:#1d4ed8,stroke-width:2px
  style ANALYTICS4   fill:#f3e8ff,stroke:#8b5cf6
  style FINANCE4     fill:#e8f5e9,stroke:#10b981
""",
},

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-05",
"title": "Marine & Environmental Architecture",
"subtitle": "Bridge systems → engineering → environmental compliance → IMO CII → SAP reporting",
"description": "The marine architecture of an Icon-class ship integrates navigation, engineering, and environmental compliance into a unified operational picture. The Integrated Bridge System processes AIS, GMDSS, ECDIS, and radar feeds simultaneously. Engineering monitoring covers 4 main engines, 3 Azipod propulsors, LNG dual-fuel systems, and 20+ auxiliary systems. Environmental systems — ballast water treatment, advanced wastewater, exhaust gas scrubbers — log every reading for MARPOL compliance and IMO CII carbon intensity rating.",
"notes": [
    "Icon of the Seas has 4 Wärtsilä dual-fuel LNG main engines + 3 ABB Azipod propulsion units",
    "BWTS (Ballast Water Treatment System) mandatory under IMO BWM Convention — all logs to shore",
    "AWTS (Advanced Wastewater Treatment) exceeds MARPOL Annex IV — treated water cleaner than seawater",
    "IMO CII rating requires annual carbon intensity calculation — reported to flag state (Bahamas)",
    "EPA $475K fine (2024) for waste reporting failures — now automated direct-to-shore log push",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart TB

  subgraph EXTERNAL5["🌐 External Navigation & Regulatory"]
    direction LR
    GMDSS["GMDSS\\nGlobal Maritime Distress & Safety"]
    AIS5["AIS Network\\nAutomatic Identification System"]
    NAVTEX["NAVTEX\\nNavigational warnings · weather"]
    PORTCTRL["Port Control\\nVTS · Pilot boarding · Clearance"]
    IMO["IMO / Flag State\\nSOLAS · MARPOL · CII reporting"]
  end

  subgraph BRIDGE["🧭 Integrated Bridge System"]
    direction LR
    ECDIS["ECDIS\\nElectronic Chart Display\\n& Information System"]
    RADAR["Radar Array\\nARPA · S-band · X-band"]
    CONNING["Conning Display\\nSpeed · heading · rudder angle"]
    AUTOPILOT["Autopilot\\nAdaptive route following"]
    VDR5["Voyage Data Recorder\\nSOLAS mandatory · 12h rolling buffer"]
  end

  subgraph PROPULSION["⚙️ Propulsion & Power"]
    direction LR
    ENGINES["Wärtsilä Dual-Fuel Engines\\n4× main engines · LNG/HFO"]
    AZIPOD["ABB Azipod\\n3× electric pod propulsors"]
    LNGSTORE["LNG Fuel Storage\\nCryogenic tanks · bunkering system"]
    POWERGEN["Power Generation\\nSwitchboard · distribution · UPS"]
    THRUSTER["Bow Thrusters\\nManoeuvring · DP assist"]
  end

  subgraph ENGINEROOM["🔧 Engine Room Management"]
    direction LR
    IMOS["Integrated Monitoring\\n& Control (IAS)\\nAlarm · automation · remote"]
    PMS5["Planned Maintenance System\\nClass surveys · component PPM"]
    FUEL5["Fuel Management\\nBunkering · consumption · transfer"]
    LUBOIL["Lube Oil System\\nMonitoring · sampling · analysis"]
  end

  subgraph ENVIRO5["🌿 Environmental Systems"]
    direction LR
    BWTS["Ballast Water\\nTreatment System\\nIMO BWM Convention"]
    AWTS["Advanced Wastewater\\nTreatment System\\nMARPOL Annex IV+"]
    SCRUBBERS["Exhaust Gas Scrubbers\\nSOx reduction · open/closed loop"]
    OWS["Oily Water Separator\\n15ppm threshold · MARPOL Annex I"]
    GARBAGE["Garbage Management\\nMARPOL Annex V · log book"]
    INCINERATOR["Marine Incinerator\\nSolid waste · regulated materials"]
  end

  subgraph COMPLIANCE5["📋 Compliance & Reporting"]
    direction LR
    ELOG["Electronic Log Books\\nEngine · Oil record · Garbage"]
    CII["IMO CII Calculator\\nAnnual carbon intensity rating"]
    EPALOG["EPA Reporting\\nUS port waste · discharge logs"]
    CLASSINSP["Class Society\\nLloyds · Bureau Veritas · surveys"]
  end

  subgraph SHORE5["🏢 Shore Reporting"]
    direction LR
    SAP5["SAP S/4HANA\\nFuel costs · maintenance costs"]
    FLEETOPS["Fleet Operations Center\\nMiami HQ · 24/7 monitoring"]
    ENVREPORT["Environmental Reporting\\nRCCL sustainability dashboard"]
  end

  GMDSS   -->|"distress alerts"| BRIDGE
  AIS5    -->|"traffic picture"| ECDIS
  NAVTEX  -->|"warnings"| CONNING
  PORTCTRL -->|"berthing orders"| BRIDGE

  ECDIS    -->|"route data"| AUTOPILOT
  AUTOPILOT -->|"helm commands"| AZIPOD
  CONNING  -->|"speed order"| ENGINES
  VDR5     -->|"voyage record"| ELOG

  ENGINES  -->|"shaft power"| AZIPOD
  LNGSTORE -->|"fuel supply"| ENGINES
  POWERGEN -->|"electricity"| AZIPOD
  THRUSTER -->|"assist"| AZIPOD

  IMOS    -->|"engine alarms"| PMS5
  IMOS    -->|"consumption data"| FUEL5
  PMS5    -->|"maintenance schedule"| SAP5
  FUEL5   -->|"fuel costs"| SAP5
  LUBOIL  -->|"oil analysis"| PMS5

  BWTS   -->|"treatment logs"| ELOG
  AWTS   -->|"discharge logs"| ELOG
  SCRUBBERS -->|"SOx data"| ELOG
  OWS    -->|"oil record"| ELOG
  GARBAGE -->|"waste log"| ELOG
  INCINERATOR -->|"burn log"| ELOG

  ELOG  -->|"log data"| CII
  ELOG  -->|"discharge data"| EPALOG
  CII   -->|"annual rating"| IMO
  EPALOG -->|"US compliance"| ENVREPORT
  CLASSINSP -->|"survey results"| PMS5

  CII      -->|"fuel efficiency"| SAP5
  EPALOG   -->|"compliance status"| FLEETOPS
  ENVREPORT -->|"sustainability KPIs"| FLEETOPS
  SAP5     -->|"cost reports"| FLEETOPS

  style EXTERNAL5   fill:#f0f4ff,stroke:#6366f1
  style BRIDGE      fill:#e0f7fa,stroke:#0891b2,stroke-width:2px
  style PROPULSION  fill:#fce4ec,stroke:#ef4444
  style ENGINEROOM  fill:#f3e8ff,stroke:#8b5cf6
  style ENVIRO5     fill:#e8f5e9,stroke:#10b981,stroke-width:2px
  style COMPLIANCE5 fill:#fff3e0,stroke:#f59e0b
  style SHORE5      fill:#e3f2fd,stroke:#3b82f6
""",
},

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-06",
"title": "Crew Management & HR Integration",
"subtitle": "Workday HCM → sign-on/off → STCW → scheduling → payroll → repatriation",
"description": "Royal Caribbean manages 100,000+ seafarers across its fleet through an integrated crew management architecture centred on Workday HCM. From initial recruitment through contract generation, STCW certification tracking, sign-on biometric verification, shipboard scheduling, payroll processing, and repatriation — every step produces data that flows into SAP for cost accounting and back into Workday for workforce planning. The architecture supports 69 ships across 3 brands operating simultaneously.",
"notes": [
    "RCCL employs ~100,000 crew across 69 ships — Workday is the single source of truth for all crew",
    "STCW certification is mandatory for all seafarers — expired certs trigger automatic access block",
    "Sign-on biometric verification uses the same IDEMIA system as guest debarkation",
    "Crew payroll is processed monthly in 50+ currencies for crew from 100+ nationalities",
    "ITF (International Transport Workers Federation) compliance is audited annually per ship",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart LR

  subgraph RECRUIT["📋 Recruitment & Contracting"]
    direction TB
    CREWAGENT["Manning Agencies\\n100+ nationalities · 50+ agencies"]
    APPLICANT["Applicant Tracking\\nWorkday Recruiting"]
    CONTRACT["Contract Generation\\nWorkday · ITF CBA terms"]
    MEDCERT["Pre-Employment Medical\\nDES · PEME certification"]
    VISADOC["Visa & Documentation\\nSeaman's book · flag endorsements"]
  end

  subgraph WORKDAY6["🟡 Workday HCM — Crew Master"]
    direction TB
    CREWPROFILE["Crew Profile\\nPersonal · contract · rank · ship"]
    STCW6["STCW Certification\\nMandatory certs · expiry tracking"]
    PAYROLLWDY["Payroll Data\\nBase · overtime · allotments"]
    PERFORMANCE["Performance Management\\nAppraisals · promotion · discipline"]
    TALENT["Talent & Succession\\nHigh potential · pipeline"]
  end

  subgraph SIGNONOFF["🚢 Sign-On / Sign-Off"]
    direction TB
    PORTAUTH6["Port Authority\\nCrewman landing card · immigration"]
    BIOMETRIC6["Biometric Verification\\nIDEMIA · fingerprint · photo"]
    SPMS6["SPMS Crew Module\\nShipboard crew manifest · cabin assign"]
    MEDICAL6["Ship's Medical Centre\\nHealth declaration · fitness check"]
    SAFETY6["Safety Induction\\nMuster station · emergency duties"]
  end

  subgraph SHIPBOARD6["⚓ Shipboard Operations"]
    direction TB
    ROSTER["Crew Roster System\\nWatch keeping · rest hours · STCW"]
    SCHEDULE6["Scheduling Engine\\nDuty rosters · department coverage"]
    ACCESS6["Ship Access Control\\nDoor system · restricted areas"]
    TRAINING6["Onboard Training\\nDrills · competency records"]
    DISCIPLINE["Incident & Discipline\\nLog · hearing · record"]
  end

  subgraph PAYROLL6["💰 Payroll & Benefits"]
    direction TB
    TIMEKEEP["Time & Attendance\\nHours worked · overtime trigger"]
    PAYSLIP["Payroll Processing\\nMonthly · multi-currency · allotments"]
    ALLOTMENT["Home Allotments\\nBank transfers · 50+ countries"]
    REPATRIATION["Repatriation\\nFlight booking · end-of-contract"]
    BANKLINK["Bank Integration\\nSWIFT · local bank transfers"]
  end

  subgraph COMPLIANCE6["📋 Regulatory Compliance"]
    direction TB
    MLC["MLC 2006\\nMaritime Labour Convention"]
    ITF["ITF / CBA Compliance\\nWage scales · rest hours · repatriation"]
    FLAGSTATE6["Flag State (Bahamas)\\nCrewlist submission · casualty report"]
    PSC["Port State Control\\nInspection records · deficiencies"]
  end

  subgraph SHORE6["🏢 Shore Integration"]
    direction TB
    SAP6["SAP S/4HANA\\nCrew cost accounting"]
    SAPARIBA["SAP Ariba\\nManning agency POs"]
    FLEETHR["Fleet HR Team\\nMiami · crew welfare · IR"]
  end

  CREWAGENT  -->|"candidate profiles"| APPLICANT
  APPLICANT  -->|"offer accepted"| CONTRACT
  CONTRACT   -->|"crew record"| CREWPROFILE
  MEDCERT    -->|"medical cert"| CREWPROFILE
  VISADOC    -->|"travel docs"| CREWPROFILE

  CREWPROFILE -->|"cert register"| STCW6
  CREWPROFILE -->|"payroll setup"| PAYROLLWDY
  STCW6       -->|"cert expiry alert"| SCHEDULE6
  PERFORMANCE -->|"promotion trigger"| CREWPROFILE
  TALENT      -->|"succession plan"| FLEETHR

  CREWPROFILE -->|"sign-on data"| PORTAUTH6
  BIOMETRIC6  -->|"verified identity"| SPMS6
  SPMS6       -->|"cabin assignment"| ROSTER
  MEDICAL6    -->|"fit-for-duty"| SPMS6
  SAFETY6     -->|"induction complete"| SPMS6

  ROSTER    -->|"hours data"| TIMEKEEP
  SCHEDULE6 -->|"duty assignments"| ROSTER
  ACCESS6   -->|"access events"| SPMS6
  TRAINING6 -->|"cert updates"| STCW6
  DISCIPLINE -->|"record"| PERFORMANCE

  TIMEKEEP   -->|"approved hours"| PAYSLIP
  PAYSLIP    -->|"net pay"| ALLOTMENT
  ALLOTMENT  -->|"transfer instructions"| BANKLINK
  REPATRIATION -->|"flight costs"| SAP6
  PAYSLIP    -->|"payroll journal"| SAP6

  MLC        -->|"compliance check"| ROSTER
  ITF        -->|"wage audit"| PAYSLIP
  FLAGSTATE6 -->|"crewlist"| SPMS6
  PSC        -->|"deficiencies"| TRAINING6

  SAP6    -->|"cost per ship"| FLEETHR
  SAPARIBA -->|"agency invoices"| SAP6

  style RECRUIT    fill:#e8f4fd,stroke:#3b82f6
  style WORKDAY6   fill:#fff8e1,stroke:#f59e0b,stroke-width:2px
  style SIGNONOFF  fill:#e0f7fa,stroke:#06b6d4
  style SHIPBOARD6 fill:#f3e8ff,stroke:#8b5cf6
  style PAYROLL6   fill:#e8f5e9,stroke:#10b981
  style COMPLIANCE6 fill:#fce4ec,stroke:#ef4444
  style SHORE6     fill:#e3f2fd,stroke:#1d4ed8
""",
},

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-07",
"title": "Connectivity & Digital Infrastructure",
"subtitle": "Starlink → ship network → Royal App → Azure AI → D2iQ microservices",
"description": "Royal Caribbean's digital infrastructure is anchored by Starlink satellite providing sub-100ms latency to 98% of the fleet, enabling a cloud-native ship-shore architecture. The Royal Caribbean App serves as the primary guest interface, processing AI chatbot interactions via Azure Cognitive Services. Azure AI Vision monitors crowd density across 20+ zones on Icon-class ships. Mesosphere/D2iQ provides the microservices bus for ship-shore data replication, enabling real-time revenue visibility, crew management updates, and operational analytics from Miami headquarters.",
"notes": [
    "Starlink replaced legacy VSAT on 98% of fleet by 2025 — latency dropped from 600ms to sub-100ms",
    "Royal App achieved 35% year-on-year adoption increase — now primary service channel on new ships",
    "Azure AI Vision monitors 20+ crowd density zones on Icon of the Seas — feeds flow optimisation",
    "D2iQ (formerly Mesosphere) provides Kubernetes-based microservices for ship-shore event streaming",
    "Ship WiFi runs on three segregated VLANs: guest internet, crew welfare, and operational systems",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart TB

  subgraph SATNET["🛰️ Satellite Connectivity Layer"]
    direction LR
    STARLINK7["Starlink LEO\\n98% fleet · sub-100ms · multi-beam"]
    VSAT["Legacy VSAT\\nBackup · remote ports"]
    CELLULAR["4G/5G Shore\\nIn-port cellular offload"]
    LBAND["L-Band (Inmarsat)\\nGMDSS · EPIRB · safety only"]
  end

  subgraph SHIPNET7["🌐 Ship Network Layer"]
    direction LR
    COREROUTER["Core Router/Firewall\\nPalo Alto · Cisco · segmentation"]
    GUESTVLAN["Guest WiFi VLAN\\nVoom internet · bandwidth managed"]
    CREWVLAN["Crew Welfare VLAN\\nPersonal internet · social media"]
    OPSVLAN["Operations VLAN\\nSPMS · MICROS · Nav systems"]
    IOTNET["IoT Sensor Network\\nCabin sensors · environmental · energy"]
  end

  subgraph ROYALAPP7["📱 Royal Caribbean App Platform"]
    direction LR
    APPCLIENT["Mobile App\\niOS · Android · 7,600 guest capacity"]
    APICACHE["API Gateway\\nAzure API Management · rate limiting"]
    CHATBOT["NLP AI Chatbot\\nAzure Cognitive Services · 35% adoption"]
    PUSHNOTIF["Push Notifications\\nPre-cruise · onboard · itinerary alerts"]
    APPBOOKING["In-App Bookings\\nDining · shows · excursions · spa"]
  end

  subgraph AZUREAI["☁️ Microsoft Azure AI Layer"]
    direction LR
    AZURECV["Azure Computer Vision\\nCrowd density · people counting"]
    AZURENLP["Azure Cognitive Services\\nNLP · sentiment · chatbot"]
    AZUREIOT["Azure IoT Hub\\nShip sensor telemetry"]
    AZUREML["Azure ML\\nDemand forecasting · yield"]
    AZUREDASH["Azure Dashboard\\nOps analytics · alerts"]
  end

  subgraph MICROSERV7["⚙️ D2iQ Microservices Platform"]
    direction LR
    EVENTBUS["Event Bus\\nKafka · ship-shore event stream"]
    DATAREPLIC["Data Replication\\nSPMS → shore · near-real-time"]
    APIORCH["API Orchestration\\nShip-side service mesh"]
    CONFIGMGMT["Config Management\\nFleet-wide software deployment"]
  end

  subgraph SHIPCORE7["🔵 Shipboard Core Systems"]
    direction LR
    SPMS7["Oracle SPMS\\nShipboard hub"]
    MICROS7["Oracle MICROS\\nPOS network"]
    NAVSYS7["Navigation Systems\\nBridge · ECDIS · AIS"]
    ENVIRO7["Environmental Sensors\\nBWTS · scrubbers · OWS"]
  end

  subgraph SHORE7["🏢 Shore-Side Systems (Miami HQ)"]
    direction LR
    RES7["RES System\\nBooking & inventory"]
    SAP7["SAP S/4HANA\\nFinance · HR costs"]
    OBIEE7["Oracle OBIEE\\nRevenue analytics"]
    FLEETMGMT["Fleet Ops Centre\\n24/7 monitoring"]
    CYBERSOC["Cyber SOC\\nThreat monitoring · SIEM"]
  end

  STARLINK7 -->|"primary bandwidth"| COREROUTER
  VSAT      -->|"failover link"| COREROUTER
  CELLULAR  -->|"in-port offload"| COREROUTER
  LBAND     -->|"safety circuits"| NAVSYS7

  COREROUTER -->|"guest traffic"| GUESTVLAN
  COREROUTER -->|"crew traffic"| CREWVLAN
  COREROUTER -->|"ops traffic"| OPSVLAN
  COREROUTER -->|"sensor data"| IOTNET

  GUESTVLAN -->|"app requests"| APICACHE
  APPCLIENT -->|"API calls"| APICACHE
  APICACHE  -->|"chatbot queries"| CHATBOT
  CHATBOT   -->|"NLP processing"| AZURENLP
  APPBOOKING -->|"booking events"| SPMS7
  PUSHNOTIF -->|"app push"| APPCLIENT

  IOTNET    -->|"telemetry"| AZUREIOT
  OPSVLAN   -->|"video feeds"| AZURECV
  AZURECV   -->|"crowd alerts"| AZUREDASH
  AZUREIOT  -->|"sensor stream"| AZUREML
  AZUREML   -->|"demand signals"| OBIEE7

  OPSVLAN   -->|"ops data"| EVENTBUS
  EVENTBUS  -->|"SPMS events"| DATAREPLIC
  DATAREPLIC -->|"replicated data"| SHORE7
  APIORCH   -->|"service calls"| SPMS7
  CONFIGMGMT -->|"software updates"| SHIPCORE7

  SPMS7   -->|"ops events"| EVENTBUS
  MICROS7 -->|"revenue events"| EVENTBUS
  NAVSYS7 -->|"position events"| EVENTBUS
  ENVIRO7 -->|"compliance events"| EVENTBUS

  DATAREPLIC -->|"booking sync"| RES7
  DATAREPLIC -->|"financial data"| SAP7
  DATAREPLIC -->|"analytics data"| OBIEE7
  DATAREPLIC -->|"ops stream"| FLEETMGMT
  COREROUTER -->|"security events"| CYBERSOC

  style SATNET      fill:#e0f7fa,stroke:#06b6d4,stroke-width:2px
  style SHIPNET7    fill:#f3e8ff,stroke:#8b5cf6
  style ROYALAPP7   fill:#fff3e0,stroke:#f59e0b
  style AZUREAI     fill:#e8f4fd,stroke:#3b82f6
  style MICROSERV7  fill:#fce4ec,stroke:#ef4444
  style SHIPCORE7   fill:#e3f2fd,stroke:#1d4ed8
  style SHORE7      fill:#e8f5e9,stroke:#10b981
""",
},

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-08",
"title": "Finance & Procurement Architecture",
"subtitle": "SAP S/4HANA · SAP Ariba · voyage accounting · port disbursements · fleet consolidation",
"description": "Royal Caribbean's finance architecture centres on SAP S/4HANA for all enterprise accounting across 69 ships and 3 brands. Each voyage generates a distinct profit centre in SAP, with revenues flowing from Oracle SPMS and costs from Workday (crew), SAP Ariba (procurement), and port disbursement agents. The architecture supports multi-currency consolidation across 1,000+ port calls annually, regulatory compliance for a Bahamas-flagged, NYSE-listed company, and the Perfecta Programme financial targets of 20% CAGR Adjusted EPS through 2027.",
"notes": [
    "Each voyage is a distinct profit centre in SAP — revenue and costs matched at voyage level",
    "SAP Ariba manages 10,000+ suppliers globally — food, fuel, equipment, services",
    "Port disbursement agents in 1,000+ ports submit invoices through Ariba supplier portal",
    "FX exposure is significant — multi-currency voyages settle in USD but costs in 50+ currencies",
    "Perfecta Programme (2025-2027) targets 20% CAGR Adjusted EPS — CFO dashboards built on SAP Analytics",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart LR

  subgraph REVENUE8["💳 Revenue Sources"]
    direction TB
    SPMS8["Oracle SPMS\\nVoyage revenue journals"]
    NEXTCRUISE8["Next Cruise Deposits\\nFuture booking income"]
    LOYALTY8["Loyalty Revenue\\nPartner commissions"]
    INSURANCE8["Travel Protection\\nAon / travel insurance"]
  end

  subgraph COSTS["💸 Cost Sources"]
    direction TB
    WORKDAY8["Workday HCM\\nCrew payroll · benefits"]
    ARIBA8["SAP Ariba\\nAll procurement POs"]
    PORTDISB8["Port Disbursements\\n1,000+ port agents · fees"]
    FUEL8["Fuel Procurement\\nLNG · HFO · MGO bunkering"]
    CHARTER["Charter & Lease\\nPort terminal · private destination"]
  end

  subgraph SAPCORE["🔵 SAP S/4HANA Core"]
    direction TB
    GL["General Ledger\\nMulti-entity · IFRS · US GAAP"]
    AR["Accounts Receivable\\nGuest billing · agent commissions"]
    AP["Accounts Payable\\nSupplier payments · port agents"]
    CO["Controlling\\nVoyage profit centres · cost centres"]
    ASSETACCT["Asset Accounting\\nShip depreciation · dry dock capitalisation"]
    TAXGL["Tax Management\\nVAT · GST · port taxes · casino levies"]
  end

  subgraph ARIBA["🟠 SAP Ariba Procurement"]
    direction TB
    SOURCING["Strategic Sourcing\\nSupplier RFP · contracts"]
    PO["Purchase Orders\\nAutomatic PO from requisition"]
    SUPPLIER["Supplier Portal\\n10,000+ suppliers · self-service"]
    INVOICE["Invoice Processing\\nOCR · 3-way match · auto-approval"]
    CATALOG["Procurement Catalogue\\nPre-approved items · bundles"]
  end

  subgraph TREASURY["🏦 Treasury & FX"]
    direction TB
    CASHPOOL["Cash Pooling\\nMulti-entity notional pool"]
    FXHEDGE["FX Hedging\\nForward contracts · fuel hedges"]
    BANKING["Banking Integration\\nSWIFT · multi-bank portal"]
    INTERCO["Intercompany\\nRCL brands · eliminations"]
  end

  subgraph REPORTING8["📊 Reporting & Analytics"]
    direction TB
    SAPANALYTICS["SAP Analytics Cloud\\nCFO dashboards · Perfecta KPIs"]
    VOYAGEREPORT["Voyage P&L\\nPer-ship · per-voyage profitability"]
    FLEETCONSOLN["Fleet Consolidation\\n69-ship roll-up · brand segment"]
    SEC["SEC Reporting\\nNYSE 10-Q · 10-K · Reg-FD"]
    AUDIT["Internal Audit\\nSOX compliance · control testing"]
  end

  SPMS8      -->|"revenue journal"| GL
  NEXTCRUISE8 -->|"deferred revenue"| GL
  LOYALTY8   -->|"partner income"| AR
  INSURANCE8 -->|"premium revenue"| AR

  WORKDAY8  -->|"payroll journal"| GL
  ARIBA8    -->|"AP invoices"| AP
  PORTDISB8 -->|"disbursement claim"| AP
  FUEL8     -->|"fuel invoices"| AP
  CHARTER   -->|"lease payments"| AP

  AR -->|"guest payments"| CASHPOOL
  AP -->|"supplier payments"| BANKING
  GL -->|"cost allocation"| CO
  GL -->|"ship assets"| ASSETACCT
  GL -->|"tax entries"| TAXGL
  CO -->|"voyage P&L"| VOYAGEREPORT

  SOURCING -->|"awarded contract"| PO
  PO       -->|"goods receipt"| INVOICE
  SUPPLIER -->|"supplier invoice"| INVOICE
  INVOICE  -->|"matched invoice"| AP
  CATALOG  -->|"approved spend"| PO

  CASHPOOL -->|"funding"| FXHEDGE
  FXHEDGE  -->|"hedge settlements"| GL
  BANKING  -->|"bank statements"| GL
  INTERCO  -->|"eliminations"| FLEETCONSOLN

  VOYAGEREPORT -->|"voyage data"| SAPANALYTICS
  FLEETCONSOLN -->|"consolidated P&L"| SAPANALYTICS
  SAPANALYTICS -->|"Perfecta metrics"| SEC
  SAPANALYTICS -->|"control data"| AUDIT

  style REVENUE8   fill:#e8f5e9,stroke:#10b981
  style COSTS      fill:#fce4ec,stroke:#ef4444
  style SAPCORE    fill:#e3f2fd,stroke:#1d4ed8,stroke-width:2px
  style ARIBA      fill:#fff8e1,stroke:#f59e0b,stroke-width:2px
  style TREASURY   fill:#f3e8ff,stroke:#8b5cf6
  style REPORTING8 fill:#e0f7fa,stroke:#06b6d4
""",
},

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-09",
"title": "Safety, Security & Medical Architecture",
"subtitle": "SOLAS compliance · medical centre · MEDEVAC · outbreak management · port health clearance",
"description": "Safety and medical architecture on a modern cruise ship is a distinct operational domain with life-critical systems. The Muster 2.0 digital safety drill system replaced traditional muster in 2020. The ship's medical centre — equivalent to a small hospital — handles 50-100 consultations daily on Icon of the Seas, with MEDEVAC coordination via GMDSS and MedAire telemedicine for serious cases. Environmental health monitoring is critical following the Explorer of the Seas norovirus outbreak (689 sick, 2014) and the White Island volcanic eruption (Ovation of the Seas, 2019).",
"notes": [
    "Muster 2.0: guests complete safety briefing on Royal App before departure — no assembly required",
    "Icon of the Seas medical centre: 2 doctors, 4 nurses, ICU-capable, defibrillators throughout ship",
    "MedAire (now AXA Partners) provides 24/7 telemedicine consultation for serious cases at sea",
    "MEDEVAC coordination: Captain → GMDSS → US Coast Guard / local coast guard → helicopter or tender",
    "CDC Vessel Sanitation Programme (VSP) inspects all US-homeport ships — score published publicly",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart TB

  subgraph EXTERNAL9["🌐 External Safety Authorities"]
    direction LR
    USCG["US Coast Guard\\nMEDEVAC · port security · PSC"]
    CDC["CDC Vessel Sanitation\\nVSP inspection · score"]
    PORTHLTH["Port Health Authority\\nPre-arrival health declaration"]
    MEDAIRE["MedAire / AXA Partners\\n24/7 maritime telemedicine"]
    INSURER["P&I Club Insurer\\nLiability · medical cost cover"]
  end

  subgraph MUSTERSYS["🆘 Safety Management System"]
    direction LR
    MUSTER20["Muster 2.0 System\\nRoyal App safety briefing\\nPre-departure digital completion"]
    SAFETYMGMT["ISM Safety Management\\nSMS · drills · incident reporting"]
    EMERGPLAN["Emergency Response Plans\\nAbandon ship · fire · flooding · MOB"]
    SAFETYDRILLS["Drill Management\\nFire · lifeboat · medical · security"]
    BRIDGEALERT["Bridge Alert System\\nCritical alarm management"]
  end

  subgraph MEDICAL9["🏥 Medical Centre Operations"]
    direction LR
    TRIAGE["Medical Triage\\nGuest & crew initial assessment"]
    EMRMEDICAL["EMR System\\nElectronic medical records · HIPAA"]
    PHARMACY["Pharmacy Management\\nDrug inventory · controlled substances"]
    ISOLATION["Isolation Protocol\\nNorovirus · COVID · outbreak rooms"]
    LAB["Diagnostic Lab\\nBlood · urine · rapid tests"]
    MORGUE["Mortuary Procedures\\nOnboard storage · port repatriation"]
  end

  subgraph MEDEVAC9["🚁 MEDEVAC & Emergency"]
    direction LR
    GMDSS9["GMDSS\\nMayday · PAN PAN · urgent marine info"]
    CAPTAIN9["Master & Bridge Team\\nEmergency command"]
    COASTGUARD["Coast Guard Coordination\\nHelicopter · cutter · SAR"]
    PORTDIVER["Port Diversion\\nNearest port with medical facility"]
    AIRAMBULANCE["Air Ambulance\\nMedAire · international coordination"]
  end

  subgraph OUTBREAKQ["🦠 Outbreak & Public Health"]
    direction LR
    ENHANCE["Enhanced Cleaning Protocol\\nNorovirus · quarantine areas"]
    CASETRACK["Case Tracking\\nSymptom log · contact tracing"]
    CDCREPORT["CDC Reporting\\nGI illness threshold 3%"]
    PORTNOTIFY["Port Health Notification\\nPre-arrival declaration"]
    ISOLATION2["Guest Isolation\\nCabin restriction · meal delivery"]
  end

  subgraph SECURITY9["🛡️ Ship Security"]
    direction LR
    ISPS["ISPS Code Compliance\\nPort facility security plan"]
    CCTV9["CCTV System\\n2,000+ cameras on Icon class"]
    ACCESSCTRL["Access Control\\nCrew/guest area segregation"]
    SEAMARSHAL["Dedicated Security Team\\nArmed / unarmed · MSOG training"]
    GANGWAY["Gangway Control\\nAll persons logged in/out · ID scan"]
  end

  subgraph SPMSMED["🔵 SPMS & Systems Integration"]
    direction LR
    SPMS9["Oracle SPMS\\nManifest · cabin · emergency list"]
    MUSAPP["Royal App\\nMuster 2.0 completion tracking"]
    INCIDENTLOG["Incident Reporting\\nSAFER database · near-miss"]
    REGULATORY9["Regulatory Reporting\\nSOLAS · IMO · flag state"]
  end

  MUSTER20  -->|"completion data"| MUSAPP
  MUSAPP    -->|"muster status"| SPMS9
  SAFETYMGMT -->|"drill records"| INCIDENTLOG
  EMERGPLAN -->|"activation"| CAPTAIN9
  BRIDGEALERT -->|"critical alarms"| CAPTAIN9

  TRIAGE   -->|"case record"| EMRMEDICAL
  EMRMEDICAL -->|"consultation"| MEDAIRE
  PHARMACY -->|"medication log"| EMRMEDICAL
  ISOLATION -->|"case count"| CASETRACK
  LAB      -->|"test results"| EMRMEDICAL

  CASETRACK -->|"GI cases"| CDCREPORT
  CASETRACK -->|"outbreak trigger"| ENHANCE
  ENHANCE   -->|"cabin restriction"| ISOLATION2
  CDCREPORT -->|"inspection trigger"| CDC
  PORTNOTIFY -->|"health declaration"| PORTHLTH

  CAPTAIN9    -->|"MAYDAY"| GMDSS9
  GMDSS9      -->|"distress signal"| COASTGUARD
  COASTGUARD  -->|"response"| PORTDIVER
  MEDAIRE     -->|"evac decision"| AIRAMBULANCE
  PORTDIVER   -->|"hospital transfer"| INSURER

  ISPS     -->|"access matrix"| ACCESSCTRL
  CCTV9    -->|"footage"| SEAMARSHAL
  GANGWAY  -->|"manifest update"| SPMS9
  INCIDENTLOG -->|"reports"| REGULATORY9
  REGULATORY9 -->|"compliance data"| USCG

  style EXTERNAL9  fill:#f0f4ff,stroke:#6366f1
  style MUSTERSYS  fill:#fff3e0,stroke:#f59e0b
  style MEDICAL9   fill:#fce4ec,stroke:#ef4444,stroke-width:2px
  style MEDEVAC9   fill:#f3e8ff,stroke:#8b5cf6
  style OUTBREAKQ  fill:#fef3c7,stroke:#92400e
  style SECURITY9  fill:#e8f4fd,stroke:#1d4ed8
  style SPMSMED    fill:#e0f7fa,stroke:#06b6d4
""",
},

# ══════════════════════════════════════════════════════════════════════════════
{
"id": "EA-10",
"title": "Loyalty & CRM Architecture",
"subtitle": "Crown & Anchor · Club Royale · Salesforce CRM · RES pricing · next-cruise intelligence",
"description": "Royal Caribbean operates two distinct loyalty ecosystems: Crown & Anchor Society for sailing guests (6 tiers, 30M+ members) and Club Royale for casino guests (4 tiers), plus a Hard Rock Unity partnership. Both feed into Salesforce CRM for unified guest intelligence. The architecture integrates booking history from RES, spend data from SPMS/MICROS, survey scores from post-cruise feedback, and predictive propensity models from Azure ML to deliver personalised next-cruise offers — the primary driver of repeat bookings which represent ~60% of RCCL revenue.",
"notes": [
    "Crown & Anchor Society: Gold, Platinum, Emerald, Diamond, Diamond Plus, Pinnacle Club (7+ nights threshold each)",
    "Club Royale: Choice, Prime, Signature, Masters — casino spend tracked across all sailings",
    "Hard Rock Unity partnership: Club Royale points transferable to Hard Rock rewards and vice versa",
    "Status match (June 2024): Crown & Anchor ↔ Celebrity Captain's Club ↔ Silversea Venetian Society",
    "Next Cruise consultants onboard sell future sailings at exclusive onboard pricing — significant revenue stream",
],
"mmd": """\
%%{init: {'theme':'base','themeVariables':{'fontSize':'12px','fontFamily':'Inter, Arial, sans-serif'}}}%%
flowchart LR

  subgraph DATAFEEDS["📥 Guest Data Sources"]
    direction TB
    RES10["RES System\\nBooking history · cabin category · spend"]
    SPMS10["Oracle SPMS\\nOnboard behaviour · folio summary"]
    MICROS10["Oracle MICROS\\nDetailed spend by venue · category"]
    SURVEY["Post-Cruise Survey\\nNPS · satisfaction · issues"]
    SOCIALMEDIA["Social & Digital\\nReviews · mentions · sentiment"]
    NEXTCRUISE10["Next Cruise Onboard\\nFuture deposit · interest"]
  end

  subgraph CROWNANCHOR["👑 Crown & Anchor Society"]
    direction TB
    CAPLATFORM["C&A Loyalty Platform\\nPoints engine · tier rules · benefits"]
    CATIERS["Tier Management\\nGold · Platinum · Emerald · Diamond · Diamond+ · Pinnacle"]
    CABENEFITS["Benefits Engine\\nPriority boarding · OBC · discounts · events"]
    CASTATMATCH["Status Match\\nCelebrity ↔ Silversea ↔ C&A (June 2024)"]
  end

  subgraph CLUBROYALE["🎰 Club Royale Casino Loyalty"]
    direction TB
    CRTIERS["CR Tiers\\nChoice · Prime · Signature · Masters"]
    CRENGINE["Casino Points Engine\\nSlots · tables · poker earn rates"]
    CRBENEFITS["CR Benefits\\nFree cruises · cash back · priority"]
    HARDROCK["Hard Rock Unity\\nBi-directional points transfer"]
  end

  subgraph CRM10["🟠 Salesforce CRM — Unified Guest Profile"]
    direction TB
    GUESTPROFILE["360° Guest Profile\\nAll sailings · spend · preferences · feedback"]
    SEGMENTATION["Segmentation Engine\\nRFM · demographic · behavioural clusters"]
    JOURNEY["Customer Journey\\nPre · during · post cruise touchpoints"]
    CASES["Service Cases\\nComplaints · resolutions · follow-up"]
    AGENTDESK["Agent Desktop\\nCall centre · email · chat · social"]
  end

  subgraph ANALYTICS10["📊 Analytics & Intelligence"]
    direction TB
    AZUREML10["Azure ML\\nChurn prediction · propensity models"]
    OBIEE10["Oracle OBIEE\\nLoyalty KPIs · revenue per member"]
    LTVCALC["LTV Calculator\\nLifetime value · upsell potential"]
    NEXTBESTOFFER["Next Best Offer\\nPersonalised cabin · itinerary · package"]
  end

  subgraph ACTIVATION["📣 Offer Activation Channels"]
    direction TB
    EMAIL["Email Marketing\\nSalesforce Marketing Cloud"]
    APP10["Royal App\\nPush · in-app personalisation"]
    CALLCENTRE["Call Centre\\nCruising Power · direct sales"]
    TRAVELAGENT10["Travel Agent Portal\\nCruising Power · agent incentives"]
    ONBOARD10["Onboard Next Cruise\\nConsultant · deposit · OBC incentive"]
  end

  subgraph BOOKING10["🎫 Booking Conversion"]
    direction TB
    RES10B["RES Booking Engine\\nPersonalised pricing · availability"]
    REVENUE10["Revenue Management\\nDynamic pricing · yield"]
    ATTRIBUTION["Attribution Tracking\\nWhich channel drove booking"]
  end

  RES10       -->|"sailing history"| GUESTPROFILE
  SPMS10      -->|"onboard behaviour"| GUESTPROFILE
  MICROS10    -->|"spend detail"| GUESTPROFILE
  SURVEY      -->|"NPS & feedback"| GUESTPROFILE
  SOCIALMEDIA -->|"sentiment data"| GUESTPROFILE
  NEXTCRUISE10 -->|"deposit intent"| GUESTPROFILE

  GUESTPROFILE -->|"sailing credits"| CAPLATFORM
  CAPLATFORM   -->|"tier update"| CATIERS
  CATIERS      -->|"benefit triggers"| CABENEFITS
  CASTATMATCH  -->|"cross-brand tier"| CATIERS

  MICROS10  -->|"casino earn"| CRENGINE
  CRENGINE  -->|"tier qualification"| CRTIERS
  CRTIERS   -->|"benefit activation"| CRBENEFITS
  HARDROCK  -->|"points transfer"| CRENGINE

  GUESTPROFILE -->|"unified data"| SEGMENTATION
  SEGMENTATION -->|"segments"| AZUREML10
  AZUREML10    -->|"propensity scores"| NEXTBESTOFFER
  OBIEE10      -->|"member KPIs"| LTVCALC
  LTVCALC      -->|"value scores"| NEXTBESTOFFER

  NEXTBESTOFFER -->|"personalised offer"| EMAIL
  NEXTBESTOFFER -->|"in-app offer"| APP10
  NEXTBESTOFFER -->|"agent offer"| TRAVELAGENT10
  NEXTBESTOFFER -->|"onboard offer"| ONBOARD10
  CASES         -->|"service recovery offer"| EMAIL

  EMAIL          -->|"click through"| RES10B
  APP10          -->|"booking tap"| RES10B
  CALLCENTRE     -->|"assisted booking"| RES10B
  TRAVELAGENT10  -->|"GDS booking"| RES10B
  ONBOARD10      -->|"deposit booking"| RES10B

  RES10B     -->|"booking confirmed"| ATTRIBUTION
  REVENUE10  -->|"price signal"| RES10B
  ATTRIBUTION -->|"channel data"| CRM10

  style DATAFEEDS    fill:#e8f4fd,stroke:#3b82f6
  style CROWNANCHOR  fill:#fff8e1,stroke:#f59e0b,stroke-width:2px
  style CLUBROYALE   fill:#fce4ec,stroke:#ef4444
  style CRM10        fill:#fff3e0,stroke:#f59e0b,stroke-width:2px
  style ANALYTICS10  fill:#f3e8ff,stroke:#8b5cf6
  style ACTIVATION   fill:#e8f5e9,stroke:#10b981
  style BOOKING10    fill:#e0f7fa,stroke:#06b6d4
""",
},

]  # end EA_DIAGRAMS


# ─────────────────────────────────────────────────────────────────────────────
# GITHUB HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def gh_get_sha(path):
    r = requests.get(f"{GH_API}/repos/{GH_REPO}/contents/{path}",
                     headers={"Authorization": f"token {GH_TOKEN}",
                              "Accept": "application/vnd.github.v3+json"},
                     timeout=15)
    return r.json().get("sha") if r.status_code == 200 else None

def gh_push(path, content, message):
    headers = {"Authorization": f"token {GH_TOKEN}",
               "Accept": "application/vnd.github.v3+json"}
    sha = gh_get_sha(path)
    if isinstance(content, bytes):
        encoded = base64.b64encode(content).decode()
    else:
        encoded = base64.b64encode(content.encode()).decode()
    body = {"message": message, "content": encoded}
    if sha:
        body["sha"] = sha
    for attempt in range(3):
        r = requests.put(f"{GH_API}/repos/{GH_REPO}/contents/{path}",
                         headers=headers, json=body, timeout=60)
        if r.status_code in (200, 201):
            return True
        log(f"Push {r.status_code}: {r.text[:120]}", "warn")
        time.sleep(3)
    return False


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR HTML (EA section only — used on all EA pages)
# ─────────────────────────────────────────────────────────────────────────────
def build_ea_sidebar(active_id, depth=2):
    """Build full sidebar with all 12 process domains + EA section.
    Mirrors build_sidebar() in the main wiki generator so all pages look identical.
    depth=2 → ea-diagrams/ea-XX/ pages (../../)
    depth=1 → ea-diagrams/ index page (../)
    """
    prefix = "../" * depth

    # All 12 L1 domains with their L2 groups
    DOMAINS = [
        ("Guest Services & Embarkation",    "GS", "guest-services", [
            ("Embarkation & Check-In",       "GS-EM", "embarkation-checkin"),
            ("Debarkation & Port Ops",       "GS-DB", "debarkation"),
            ("Guest Experience",             "GS-CX", "guest-experience"),
        ]),
        ("Stateroom & Housekeeping",        "HK", "housekeeping", [
            ("Stateroom Operations",         "HK-SR", "stateroom-ops"),
            ("Laundry & Public Areas",       "HK-LP", "laundry-public"),
        ]),
        ("Food & Beverage Operations",      "FB", "food-beverage", [
            ("Restaurant & Dining",          "FB-RD", "restaurant-dining"),
            ("Culinary & Provisioning",      "FB-CP", "culinary-provisioning"),
        ]),
        ("Entertainment & Activities",      "EN", "entertainment", [
            ("Showroom & Live",              "EN-SH", "showroom-entertainment"),
            ("Activities & Adventure",       "EN-AC", "activities-adventure"),
        ]),
        ("Shore Excursions & Destinations", "SE", "shore-excursions", [
            ("Excursion Operations",         "SE-OP", "excursion-operations"),
            ("Private Destinations",         "SE-PD", "private-destinations"),
        ]),
        ("Marine & Technical Operations",   "MT", "marine-technical", [
            ("Bridge & Navigation",          "MT-BN", "bridge-navigation"),
            ("Engineering",                  "MT-EP", "engineering-propulsion"),
            ("Dry Dock",                     "MT-DS", "dry-dock-maintenance"),
        ]),
        ("Environmental & Sustainability",  "ES", "environmental", [
            ("Waste Management",             "ES-WM", "waste-management"),
            ("Env. Compliance",              "ES-EC", "environmental-compliance"),
        ]),
        ("Crew Management & HR",            "CM", "crew-management", [
            ("Crew Operations",              "CM-CO", "crew-operations"),
            ("Training & Dev",               "CM-TD", "training-development"),
        ]),
        ("Revenue & Commercial",            "RC", "revenue-commercial", [
            ("Onboard Revenue",              "RC-OR", "onboard-revenue"),
            ("Loyalty & CRM",               "RC-LC", "loyalty-crm"),
        ]),
        ("Finance & Procurement",           "FN", "finance-procurement", [
            ("Financial Ops",               "FN-FO", "financial-operations"),
            ("Procurement",                 "FN-PS", "procurement-supply"),
        ]),
        ("Technology & Cybersecurity",      "IT", "technology-it", [
            ("Ship Connectivity",            "IT-SC", "ship-connectivity"),
            ("Cybersecurity",               "IT-CY", "cybersecurity"),
        ]),
        ("Health, Safety & Medical",        "HS", "health-safety", [
            ("Medical Operations",          "HS-MD", "medical-operations"),
            ("Safety & Emergency",          "HS-SE", "safety-emergency"),
        ]),
    ]

    lines = []
    for l1_name, l1_code, l1_slug, groups in DOMAINS:
        lines.append(f'  <div class="sidebar-section">')
        lines.append(f'    <div class="sidebar-domain" data-label="{escape(l1_name)}">')
        lines.append(f'      <span class="sidebar-domain-label">{escape(l1_name)}</span><span class="chevron">▶</span>')
        lines.append(f'    </div>')
        lines.append(f'    <div class="sidebar-l2">')
        for l2_name, l2_code, l2_slug in groups:
            lines.append(
                f'      <a class="sidebar-l3-link" href="{prefix}{l1_slug}/{l2_slug}/">'
                f'<span class="pid">{l2_code}</span>{escape(l2_name)}</a>'
            )
        lines.append(f'    </div>')
        lines.append(f'  </div>')

    # EA diagrams section — always open, active item highlighted
    ea_links = "\n".join(
        f'      <a class="sidebar-l3-link{" active" if ea["id"] == active_id else ""}" '
        f'href="{prefix}ea-diagrams/{ea["id"].lower()}/">'
        f'<span class="pid">{ea["id"]}</span>{escape(ea["title"])}</a>'
        for ea in EA_DIAGRAMS
    )
    lines.append(f'  <div style="height:1px;background:#dde1e8;margin:8px 14px"></div>')
    lines.append(f'  <div class="sidebar-section">')
    lines.append(f'    <div class="sidebar-domain open" data-label="EA Diagrams">')
    lines.append(f'      <span class="sidebar-domain-label">🗺️ EA Diagrams</span><span class="chevron">▶</span>')
    lines.append(f'    </div>')
    lines.append(f'    <div class="sidebar-l2 open">')
    lines.append(f'      <a class="sidebar-l3-link" href="{prefix}ea-diagrams/">All EA Diagrams</a>')
    lines.append(ea_links)
    lines.append(f'    </div>')
    lines.append(f'  </div>')

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# BUILD EA DIAGRAM PAGE HTML
# ─────────────────────────────────────────────────────────────────────────────
def build_ea_page(ea, idx):
    eid      = ea["id"].lower()
    total    = len(EA_DIAGRAMS)
    prev_ea  = EA_DIAGRAMS[idx - 1] if idx > 0 else None
    next_ea  = EA_DIAGRAMS[idx + 1] if idx < total - 1 else None

    prev_link = (f'<a class="pn-btn" href="../../ea-diagrams/{prev_ea["id"].lower()}/">'
                 f'<span class="arrow">←</span><span>{prev_ea["id"]} · {escape(prev_ea["title"])}</span></a>'
                 if prev_ea else
                 '<a class="pn-btn" href="../../ea-diagrams/"><span class="arrow">←</span><span>All EA Diagrams</span></a>')
    next_link = (f'<a class="pn-btn next" href="../../ea-diagrams/{next_ea["id"].lower()}/">'
                 f'<span>{next_ea["id"]} · {escape(next_ea["title"])}</span><span class="arrow">→</span></a>'
                 if next_ea else '<span></span>')

    notes_html = "".join(
        f'<li style="margin-bottom:6px;font-size:12px;color:#374151">{escape(n)}</li>'
        for n in ea.get("notes", [])
    )

    sidebar_html = build_ea_sidebar(ea["id"], depth=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{ea["id"]} · {escape(ea["title"])} · Cruise Process Wiki</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/wiki.css">
</head>
<body>
<header class="topbar">
  <a href="../../" class="topbar-logo">🚢 Cruise <span>Process Wiki</span></a>
  <span class="topbar-badge">v1.0</span>
  <div class="topbar-right">
    <div class="topbar-search">
      <input type="text" id="searchBox" placeholder="Search processes… (/)" autocomplete="off">
      <div class="search-results" id="searchResults"></div>
    </div>
    <a href="../../">Home</a>
    <a href="../../ea-diagrams/">EA Diagrams</a>
    <a href="https://github.com/{GH_REPO}" class="gh-btn" target="_blank">⭐ GitHub</a>
  </div>
</header>
<nav class="sidebar" id="sidebar">
{sidebar_html}
</nav>
<button id="sidebarToggle" title="Toggle sidebar">&#9664;</button>

<main class="main">
  <div class="breadcrumb">
    <a href="../../">Home</a><span class="sep">›</span>
    <a href="../../ea-diagrams/">EA Diagrams</a><span class="sep">›</span>
    <span class="current">{ea["id"]} · {escape(ea["title"])}</span>
  </div>

  <div class="page-header">
    <div class="page-header-left">
      <h1>{escape(ea["title"])}</h1>
      <p>{escape(ea["subtitle"])} · Updated {NOW}</p>
    </div>
    <div class="page-header-meta">
      <span class="pid-badge">{ea["id"]}</span>
      <span class="status-badge complete">✅ Published</span>
      <span class="ref-line">Ref: Royal Caribbean International</span>
    </div>
  </div>

  <div class="card" id="diagram">
    <div class="card-header"><span class="icon">🗺️</span><h2>Enterprise Architecture Diagram</h2></div>
    <div class="card-body">
      <div class="diagram-wrap" id="diag-{eid}">
        <img src="../../assets/img/{eid}.png"
             alt="{ea["id"]} — {escape(ea["title"])}"
             style="max-width:100%;border-radius:6px;box-shadow:0 2px 12px rgba(0,0,0,.08);cursor:zoom-in"
             onerror="this.style.opacity='.3'">
      </div>
      <p class="diagram-hint">Click diagram to open fullscreen &nbsp;|&nbsp; Scroll to zoom &nbsp;|&nbsp; Drag to pan</p>
    </div>
  </div>

  <div class="card" id="description">
    <div class="card-header"><span class="icon">📋</span><h2>Architecture Notes</h2></div>
    <div class="card-body">
      <p style="font-size:13px;color:#374151;line-height:1.8;max-width:860px;margin-bottom:20px">{escape(ea["description"])}</p>
      {"<ul style='padding-left:20px;margin-top:0'>" + notes_html + "</ul>" if notes_html else ""}
    </div>
  </div>

  <div class="pn-nav" style="display:flex;justify-content:space-between;margin-top:8px">
    {prev_link}
    {next_link}
  </div>
</main>
<div id="bpmn-lightbox"></div>
<script src="../../assets/js/wiki.js"></script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# BUILD EA INDEX PAGE
# ─────────────────────────────────────────────────────────────────────────────
def build_ea_index():
    cards = ""
    for ea in EA_DIAGRAMS:
        eid = ea["id"].lower()
        desc_short = ea["description"][:120] + "..."
        cards += f"""      <a href="{eid}/" class="domain-card">
        <div class="domain-card-header">
          <span class="domain-icon">🗺️</span>
          <span class="domain-code">{ea["id"]}</span>
        </div>
        <h3>{escape(ea["title"])}</h3>
        <p style="font-size:11px">{escape(desc_short)}</p>
        <span class="explore-link" style="margin-top:10px">View diagram &rarr;</span>
      </a>\n"""

    sidebar_html = build_ea_sidebar("", depth=1)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>EA Diagrams · Cruise Process Wiki</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/wiki.css">
</head>
<body>
<header class="topbar">
  <a href="../" class="topbar-logo">🚢 Cruise <span>Process Wiki</span></a>
  <span class="topbar-badge">v1.0</span>
  <div class="topbar-right">
    <a href="../">Home</a>
    <a href="https://github.com/{GH_REPO}" class="gh-btn" target="_blank">⭐ GitHub</a>
  </div>
</header>
<nav class="sidebar" id="sidebar">
{sidebar_html}
</nav>
<button id="sidebarToggle" title="Toggle sidebar">&#9664;</button>

<main class="main">
  <div class="breadcrumb">
    <a href="../">Home</a><span class="sep">›</span>
    <span class="current">EA Diagrams</span>
  </div>

  <div class="page-header">
    <div class="page-header-left">
      <h1>Enterprise Architecture Diagrams</h1>
      <p>RCCL system landscape, data flows, and integration architecture — Royal Caribbean International reference · Icon of the Seas</p>
    </div>
    <div class="page-header-meta">
      <span class="pid-badge">EA</span>
      <span class="status-badge complete">10 diagrams</span>
    </div>
  </div>

  <div class="domain-grid">
{cards}  </div>
</main>
<div id="bpmn-lightbox"></div>
<script src="../assets/js/wiki.js"></script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# RENDER PNG via mmdc
# ─────────────────────────────────────────────────────────────────────────────
def render_png(ea_id, mmd_text, dry_run=False):
    eid      = ea_id.lower()
    mmd_path = DIAG_DIR / f"{eid}.mmd"
    png_path = IMG_DIR / f"{eid}.png"

    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    mmd_path.write_text(mmd_text.strip(), encoding="utf-8")

    if dry_run:
        log(f"[dry-run] Would render {mmd_path}", "info")
        return True

    cmd = [
        "mmdc", "-i", str(mmd_path), "-o", str(png_path),
        "-w", "3840", "-H", "2160", "--scale", "2",
        "--backgroundColor", "white"
    ]
    for attempt in range(3):
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and png_path.exists() and png_path.stat().st_size > 5000:
            kb = png_path.stat().st_size // 1024
            log(f"PNG rendered: {eid}.png ({kb} KB)", "ok")
            return True
        log(f"mmdc attempt {attempt+1} failed: {result.stderr[:200]}", "warn")
        time.sleep(2)

    log(f"mmdc render failed for {ea_id}", "err")
    return False


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Cruise Process Wiki — EA Diagram Generator")
    parser.add_argument("--only",    default=None, help="Generate only this EA ID e.g. EA-03")
    parser.add_argument("--dry-run", action="store_true", help="Skip mmdc and GitHub push")
    args = parser.parse_args()

    log("=" * 60, "head")
    log("Cruise Process Wiki — EA Diagram Generator", "head")
    log(f"  Repo  : https://github.com/{GH_REPO}", "head")
    log(f"  Count : {len(EA_DIAGRAMS)} EA diagrams", "head")
    log("=" * 60, "head")

    diagrams = EA_DIAGRAMS
    if args.only:
        diagrams = [ea for ea in EA_DIAGRAMS if ea["id"].upper() == args.only.upper()]
        if not diagrams:
            log(f"EA ID '{args.only}' not found", "err"); return

    ok_count = 0
    for idx, ea in enumerate(diagrams):
        global_idx = next(i for i, e in enumerate(EA_DIAGRAMS) if e["id"] == ea["id"])
        log(f"[{idx+1}/{len(diagrams)}] {ea['id']} — {ea['title']}", "step")

        # 1. Render PNG
        png_ok = render_png(ea["id"], ea["mmd"], dry_run=args.dry_run)

        # 2. Push PNG to GitHub
        if png_ok and not args.dry_run:
            eid = ea["id"].lower()
            png_bytes = (IMG_DIR / f"{eid}.png").read_bytes()
            if gh_push(f"assets/img/{eid}.png", png_bytes,
                       f"Add {ea['id']} EA diagram PNG"):
                log(f"PNG pushed: assets/img/{eid}.png", "ok")
            else:
                log(f"PNG push failed for {ea['id']}", "err")

        # 3. Push MMD source
        if not args.dry_run:
            eid = ea["id"].lower()
            gh_push(f"ea-diagrams/{eid}.mmd", ea["mmd"].strip(),
                    f"Add {ea['id']} Mermaid source")

        # 4. Build and push HTML page
        html = build_ea_page(ea, global_idx)
        if not args.dry_run:
            eid = ea["id"].lower()
            if gh_push(f"ea-diagrams/{eid}/index.html", html,
                       f"Add {ea['id']}: {ea['title']}"):
                log(f"HTML pushed: ea-diagrams/{eid}/index.html", "ok")
            else:
                log(f"HTML push failed for {ea['id']}", "err")
        else:
            log(f"[dry-run] Would push ea-diagrams/{ea['id'].lower()}/index.html", "info")

        ok_count += 1
        time.sleep(0.5)

    # 5. Push EA index page
    log("Pushing EA index page...", "push")
    ea_index = build_ea_index()
    if not args.dry_run:
        if gh_push("ea-diagrams/index.html", ea_index, "Update EA diagrams index page"):
            log("EA index pushed: ea-diagrams/index.html", "ok")
    else:
        log("[dry-run] Would push ea-diagrams/index.html", "info")

    # 6. Final .deploy marker
    if not args.dry_run:
        gh_push(".deploy",
                f"cruise-ea-diagrams\ndeployed: {NOW}\nea-diagrams: {ok_count}",
                f"Deploy marker: {ok_count} EA diagrams")

    log("=" * 60, "head")
    log(f"DONE — {ok_count}/{len(diagrams)} EA diagrams complete", "head")
    log(f"Live: https://ghatk047.github.io/Cruise-Process-Wiki/ea-diagrams/", "head")
    log("=" * 60, "head")


if __name__ == "__main__":
    main()
