"""
Customer Support Workflow Template.
Automates customer support ticket routing, response generation, and escalation.
"""

import time
from datetime import datetime

# Mock ticket database
ticket_db = {}
ticket_counter = 1000

# Team members by category
team_assignments = {
    "critical": "senior-support@company.com",
    "high": "support-lead@company.com",
    "medium": "support-team@company.com",
    "low": "support-team@company.com"
}

def fetch_new_tickets():
    """
    Step 1: Fetch new support tickets from queue
    """
    print(f"\n[Step 1] Fetching new support tickets...")
    time.sleep(0.5)
    
    # Mock tickets
    new_tickets = [
        {
            "id": "T1001",
            "customer": "john@example.com",
            "subject": "Cannot login to account",
            "description": "Getting error 500 when trying to login",
            "timestamp": datetime.now().isoformat()
        },
        {
            "id": "T1002",
            "customer": "sarah@example.com",
            "subject": "Billing question",
            "description": "Need clarification on last month's invoice",
            "timestamp": datetime.now().isoformat()
        },
        {
            "id": "T1003",
            "customer": "mike@example.com",
            "subject": "URGENT: System down",
            "description": "Production system is completely down, losing revenue",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    print(f"  ✓ Fetched {len(new_tickets)} new tickets")
    for ticket in new_tickets:
        print(f"    - {ticket['id']}: {ticket['subject']}")
    
    return new_tickets

def categorize_by_urgency(ticket):
    """
    Step 2: Categorize ticket by urgency level
    """
    print(f"\n[Step 2] Categorizing ticket {ticket['id']}...")
    time.sleep(0.3)
    
    subject_lower = ticket['subject'].lower()
    description_lower = ticket['description'].lower()
    
    # Urgency detection logic
    if any(word in subject_lower or word in description_lower 
           for word in ['urgent', 'critical', 'down', 'outage', 'emergency']):
        urgency = "critical"
    elif any(word in subject_lower or word in description_lower 
             for word in ['error', 'bug', 'broken', 'not working']):
        urgency = "high"
    elif any(word in subject_lower or word in description_lower 
             for word in ['billing', 'payment', 'invoice']):
        urgency = "medium"
    else:
        urgency = "low"
    
    print(f"  ✓ Urgency level: {urgency.upper()}")
    
    return urgency

def assign_to_team_member(ticket, urgency):
    """
    Step 3: Assign ticket to appropriate team member
    """
    print(f"\n[Step 3] Assigning ticket {ticket['id']}...")
    time.sleep(0.3)
    
    assigned_to = team_assignments.get(urgency, team_assignments["low"])
    
    print(f"  ✓ Assigned to: {assigned_to}")
    print(f"  ✓ Priority: {urgency.upper()}")
    
    return assigned_to

def send_notifications(ticket, urgency, assigned_to):
    """
    Step 4: Send notifications to customer and team member
    """
    print(f"\n[Step 4] Sending notifications for ticket {ticket['id']}...")
    time.sleep(0.3)
    
    # Notify customer
    print(f"  ✓ Customer notification sent to: {ticket['customer']}")
    print(f"    Message: 'We've received your ticket and will respond soon'")
    
    # Notify assigned team member
    print(f"  ✓ Team notification sent to: {assigned_to}")
    print(f"    Message: 'New {urgency} priority ticket assigned'")
    
    return True

def log_ticket_status(ticket, urgency, assigned_to):
    """
    Step 5: Log ticket status to database
    """
    print(f"\n[Step 5] Logging ticket status...")
    time.sleep(0.3)
    
    ticket_record = {
        "ticket_id": ticket['id'],
        "customer": ticket['customer'],
        "subject": ticket['subject'],
        "urgency": urgency,
        "assigned_to": assigned_to,
        "status": "assigned",
        "created_at": ticket['timestamp'],
        "updated_at": datetime.now().isoformat()
    }
    
    ticket_db[ticket['id']] = ticket_record
    
    print(f"  ✓ Ticket logged in database")
    print(f"  ✓ Status: {ticket_record['status']}")
    
    return ticket_record

def workflow():
    """
    Main customer support ticket routing workflow
    
    Returns:
        Dictionary with processing results
    """
    print("="*60)
    print("CUSTOMER SUPPORT TICKET ROUTING WORKFLOW")
    print("="*60)
    
    try:
        # Step 1: Fetch new tickets
        tickets = fetch_new_tickets()
        
        processed_tickets = []
        
        # Process each ticket
        for ticket in tickets:
            print("\n" + "-"*60)
            print(f"Processing ticket: {ticket['id']}")
            print("-"*60)
            
            # Step 2: Categorize by urgency
            urgency = categorize_by_urgency(ticket)
            
            # Step 3: Assign to team member
            assigned_to = assign_to_team_member(ticket, urgency)
            
            # Step 4: Send notifications
            send_notifications(ticket, urgency, assigned_to)
            
            # Step 5: Log status
            ticket_record = log_ticket_status(ticket, urgency, assigned_to)
            
            processed_tickets.append(ticket_record)
        
        print("\n" + "="*60)
        print("✅ ALL TICKETS PROCESSED SUCCESSFULLY")
        print("="*60)
        print(f"\nSummary:")
        print(f"  Total tickets processed: {len(processed_tickets)}")
        
        urgency_counts = {}
        for t in processed_tickets:
            urgency_counts[t['urgency']] = urgency_counts.get(t['urgency'], 0) + 1
        
        print(f"  By urgency:")
        for urgency, count in urgency_counts.items():
            print(f"    - {urgency.upper()}: {count}")
        
        return {
            "status": "success",
            "tickets_processed": len(processed_tickets),
            "urgency_breakdown": urgency_counts,
            "tickets": processed_tickets
        }
        
    except Exception as e:
        print(f"\n❌ Error processing tickets: {str(e)}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # Test the workflow
    result = workflow()
    
    print(f"\nFinal Result: {result['status']}")
    print(f"Tickets Processed: {result.get('tickets_processed', 0)}")
