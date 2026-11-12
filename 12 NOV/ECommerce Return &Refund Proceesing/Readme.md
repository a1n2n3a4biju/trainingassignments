# E-Commerce Returns & Refund Processing System

## Project Overview

A graph-based multi-agent application built using Microsoft Agent Framework, Azure AI Foundry and Python to automate the initial review of e-commerce return and refund requests.

The application uses specialized AI agents for eligibility checking, risk assessment and customer communication, with deterministic business rules and human-in-the-loop approval.

## Technology Stack

- Python
- Microsoft Agent Framework
- Azure AI Foundry
- OpenAI Chat Client
- JSON

## Agents

1. Eligibility Agent – Reviews return requests against company policy.
2. Risk Agent – Identifies suspicious and high-risk requests.
3. Customer Response Agent – Generates customer communication drafts.

## Workflow

Customer Request → Eligibility Agent → Risk Agent → Approval Gateway → Customer Response Agent → Final Output.

## Business Rules

Automatic approval requires all six conditions:

- Product amount below ₹25,000.
- Return within 30 days.
- Invoice available.
- Item unopened or damaged with supporting photographs.
- Fewer than three previous returns within 90 days.
- No HIGH-risk concern.

Other requests are escalated for human review.

## Human-in-the-Loop

The workflow pauses for manager approval when automatic approval conditions are not satisfied. The manager can approve or reject the request.

## Project Structure

- returns_workflow.py
- returns.json
- requirements.txt
- .env.example
- README.md
- screenshots/

## Installation and Execution

1. Create and activate a Python virtual environment.
2. Install dependencies using `pip install -r requirements.txt`.
3. Configure Azure AI Foundry credentials in `.env`.
4. Run `python returns_workflow.py`.

## Important Note

This is a demonstration application. No actual payments, refunds, customer messages or product replacements are processed.