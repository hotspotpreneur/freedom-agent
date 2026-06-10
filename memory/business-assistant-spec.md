# Business Assistant (BA) - Technical Specification

## Overview

**BA** is an AI Business Assistant for local businesses that handles customer communications and administrative tasks autonomously.

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Business Assistant (BA)                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Call Agent  │  │ Email Agent│  │Calendar Agt│          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Invoice Agt │  │ Bookkeep   │  │  Scraper   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│                    Unified Memory / State                   │
├─────────────────────────────────────────────────────────────┤
│                 Integration Layer (APIs)                     │
└─────────────────────────────────────────────────────────────┘
```

## Agent Specs

### 1. Call Agent
- **Role:** AI receptionist for inbound calls
- **Capabilities:**
  - Answer out-of-hours/unanswered calls
  - FAQ triage (answer common questions)
  - Book appointments directly
  - Request callbacks for non-urgent
  - Alert owner for urgent jobs (SMS/priority)
- **Tech:** Voice AI (ElevenLabs + STT), call handling via Twilio/Vonage

### 2. Email Agent
- **Role:** Manage business email communications
- **Capabilities:**
  - Read and classify inbound emails (lead, inquiry, urgent)
  - Auto-respond with templated answers
  - Flag high-value leads for owner review
  - Triage and prioritize inbox
- **Tech:** IMAP/SMTP integration, email parsing

### 3. Calendar Agent
- **Role:** Appointment scheduling and management
- **Capabilities:**
  - Check availability in real-time
  - Book, reschedule, cancel appointments
  - Send confirmations and reminders
  - Handle scheduling conflicts
- **Tech:** CalDAV/Cal.com integration, iCal

### 4. Invoice Agent
- **Role:** Generate and send invoices
- **Capabilities:**
  - Create invoices from bookings/jobs
  - Send to clients via email
  - Track payment status
  - Follow up on overdue payments
- **Tech:** PDF generation, payment tracking

### 5. Bookkeeping Agent
- **Role:** Financial record keeping
- **Capabilities:**
  - Categorize transactions
  - Track expenses and income
  - Generate reports for tax
  - Summarize financial health
- **Tech:** Bank API integration, accounting basics

### 6. Scraper Agent
- **Role:** Lead generation through web research
- **Capabilities:**
  - Find local businesses by category/location
  - Research business details (name, contact, services)
  - Build lead lists for outreach
  - Monitor for new businesses
- **Tech:** Web scraping, data enrichment APIs

## Integration Layer

- **CRM:** Store customer data, interactions, leads
- **Storage:** File storage for invoices, recordings
- **APIs:** Twilio (voice), Stripe (payments), calendar APIs

## Deployment

- Each agent runs as an isolated sub-agent
- Shared memory/state via unified storage
- Configurable per business (hours, services, pricing)
- Deployable on cloud (Railway/Render) or edge

## MVP Priority

1. **Call Agent** - most value, immediate pickup
2. **Calendar Agent** - essential for bookings
3. **Scraper Agent** - lead generation for Paul
4. **Email Agent** - secondary communication
5. **Invoice Agent** - add later
6. **Bookkeeping Agent** - add later

## Next Steps

- [ ] Design agent communication protocol
- [ ] Build Call Agent prototype (voice + FAQ)
- [ ] Build Scraper Agent for lead generation
- [ ] Define business config schema
- [ ] Set up deployment pipeline