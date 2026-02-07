"""
Employee Onboarding Workflow Template.
Automates employee onboarding process including account creation, access provisioning, and notifications.
"""

import time
from datetime import datetime, timedelta

# Mock employee database
employee_db = {}
mentor_pool = [
    {"name": "Sarah Johnson", "department": "Engineering", "experience": 5},
    {"name": "Mike Chen", "department": "Engineering", "experience": 8},
    {"name": "Lisa Brown", "department": "Product", "experience": 6},
    {"name": "David Kim", "department": "Sales", "experience": 4}
]

def send_welcome_email(employee_name, employee_email, start_date):
    """
    Step 1: Send welcome email to new employee
    """
    print(f"\n[Step 1] Sending welcome email...")
    time.sleep(0.5)
    
    email_content = f"""
    Welcome to the company, {employee_name}!
    Your start date is {start_date}.
    We're excited to have you on the team!
    """
    
    print(f"  ✓ Email sent to: {employee_email}")
    print(f"  ✓ Subject: Welcome to the Team!")
    return True

def create_slack_account(employee_name, employee_email, department):
    """
    Step 2: Create Slack account and add to channels
    """
    print(f"\n[Step 2] Creating Slack account...")
    time.sleep(0.5)
    
    username = employee_email.split('@')[0]
    channels = ["#general", "#announcements", f"#{department.lower()}"]
    
    print(f"  ✓ Slack account created: @{username}")
    print(f"  ✓ Added to channels: {', '.join(channels)}")
    
    return {"username": username, "channels": channels}

def assign_mentor(employee_name, department):
    """
    Step 3: Assign appropriate mentor based on department
    """
    print(f"\n[Step 3] Assigning mentor...")
    time.sleep(0.5)
    
    # Find mentor from same department
    suitable_mentors = [m for m in mentor_pool if m["department"] == department]
    
    if suitable_mentors:
        mentor = suitable_mentors[0]
    else:
        # Fallback to any available mentor
        mentor = mentor_pool[0]
    
    print(f"  ✓ Mentor assigned: {mentor['name']}")
    print(f"  ✓ Department: {mentor['department']}")
    print(f"  ✓ Experience: {mentor['experience']} years")
    
    return mentor

def schedule_first_week_meetings(employee_name, mentor_name, start_date):
    """
    Step 4: Schedule orientation and team meetings for first week
    """
    print(f"\n[Step 4] Scheduling first week meetings...")
    time.sleep(0.5)
    
    meetings = [
        {"day": "Monday 9:00 AM", "title": "HR Orientation", "duration": "2 hours"},
        {"day": "Monday 2:00 PM", "title": "IT Setup & Security Training", "duration": "1 hour"},
        {"day": "Tuesday 10:00 AM", "title": f"Meet Your Mentor - {mentor_name}", "duration": "1 hour"},
        {"day": "Wednesday 11:00 AM", "title": "Team Introduction", "duration": "1 hour"},
        {"day": "Friday 3:00 PM", "title": "Week 1 Check-in", "duration": "30 minutes"}
    ]
    
    print(f"  ✓ Scheduled {len(meetings)} meetings:")
    for meeting in meetings:
        print(f"    - {meeting['day']}: {meeting['title']} ({meeting['duration']})")
    
    return meetings

def workflow(employee_name, employee_email, department, start_date):
    """
    Main employee onboarding workflow
    
    Args:
        employee_name: Full name of new employee
        employee_email: Email address
        department: Department (Engineering, Product, Sales, etc.)
        start_date: Start date (YYYY-MM-DD format)
    
    Returns:
        Dictionary with onboarding results
    """
    print("="*60)
    print("EMPLOYEE ONBOARDING WORKFLOW")
    print("="*60)
    print(f"Employee: {employee_name}")
    print(f"Email: {employee_email}")
    print(f"Department: {department}")
    print(f"Start Date: {start_date}")
    print("="*60)
    
    try:
        # Step 1: Send welcome email
        email_sent = send_welcome_email(employee_name, employee_email, start_date)
        
        # Step 2: Create Slack account
        slack_info = create_slack_account(employee_name, employee_email, department)
        
        # Step 3: Assign mentor
        mentor = assign_mentor(employee_name, department)
        
        # Step 4: Schedule meetings
        meetings = schedule_first_week_meetings(employee_name, mentor["name"], start_date)
        
        # Store in employee database
        employee_db[employee_email] = {
            "name": employee_name,
            "department": department,
            "start_date": start_date,
            "slack_username": slack_info["username"],
            "mentor": mentor["name"],
            "meetings_scheduled": len(meetings)
        }
        
        print("\n" + "="*60)
        print("✅ ONBOARDING COMPLETED SUCCESSFULLY")
        print("="*60)
        
        return {
            "status": "success",
            "email_sent": email_sent,
            "slack_username": slack_info["username"],
            "mentor_assigned": mentor["name"],
            "meetings_scheduled": len(meetings)
        }
        
    except Exception as e:
        print(f"\n❌ Error during onboarding: {str(e)}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # Test the workflow
    result = workflow(
        employee_name="Alex Martinez",
        employee_email="alex.martinez@company.com",
        department="Engineering",
        start_date="2024-02-01"
    )
    
    print(f"\nFinal Result: {result}")
