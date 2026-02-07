"""
Invoice Processing Workflow Template.
Automates invoice data extraction, validation, and payment processing.
"""

import time
from datetime import datetime

# Mock invoice database
invoice_db = {}
approval_db = {}

# Approval rules
APPROVAL_THRESHOLD = 5000  # Amounts over this need manager approval
MANAGER_EMAIL = "manager@company.com"
ACCOUNTING_EMAIL = "accounting@company.com"

def read_invoice_data():
    """
    Step 1: Read invoice data from source
    """
    print(f"\n[Step 1] Reading invoice data...")
    time.sleep(0.5)
    
    # Mock invoice data
    invoices = [
        {
            "invoice_id": "INV-2024-001",
            "vendor": "Office Supplies Co",
            "amount": 1250.00,
            "date": "2024-01-15",
            "items": ["Paper", "Pens", "Folders"],
            "payment_terms": "Net 30"
        },
        {
            "invoice_id": "INV-2024-002",
            "vendor": "Cloud Services Inc",
            "amount": 8500.00,
            "date": "2024-01-20",
            "items": ["AWS Services", "Database Hosting"],
            "payment_terms": "Net 15"
        },
        {
            "invoice_id": "INV-2024-003",
            "vendor": "Marketing Agency",
            "amount": 3200.00,
            "date": "2024-01-22",
            "items": ["Social Media Campaign", "Content Creation"],
            "payment_terms": "Net 30"
        }
    ]
    
    print(f"  ✓ Read {len(invoices)} invoices")
    for inv in invoices:
        print(f"    - {inv['invoice_id']}: ${inv['amount']:.2f} from {inv['vendor']}")
    
    return invoices

def validate_invoice_amounts(invoice):
    """
    Step 2: Validate invoice amounts and data
    """
    print(f"\n[Step 2] Validating invoice {invoice['invoice_id']}...")
    time.sleep(0.3)
    
    validation_results = {
        "valid": True,
        "issues": []
    }
    
    # Check amount is positive
    if invoice['amount'] <= 0:
        validation_results['valid'] = False
        validation_results['issues'].append("Amount must be positive")
    
    # Check amount is reasonable (not too high)
    if invoice['amount'] > 100000:
        validation_results['valid'] = False
        validation_results['issues'].append("Amount exceeds maximum limit")
    
    # Check required fields
    required_fields = ['invoice_id', 'vendor', 'amount', 'date']
    for field in required_fields:
        if not invoice.get(field):
            validation_results['valid'] = False
            validation_results['issues'].append(f"Missing required field: {field}")
    
    if validation_results['valid']:
        print(f"  ✓ Invoice validation passed")
        print(f"  ✓ Amount: ${invoice['amount']:.2f}")
        print(f"  ✓ Vendor: {invoice['vendor']}")
    else:
        print(f"  ❌ Validation failed: {', '.join(validation_results['issues'])}")
    
    return validation_results

def check_approval_rules(invoice):
    """
    Step 3: Check if invoice requires manager approval
    """
    print(f"\n[Step 3] Checking approval rules for {invoice['invoice_id']}...")
    time.sleep(0.3)
    
    requires_approval = invoice['amount'] > APPROVAL_THRESHOLD
    
    if requires_approval:
        print(f"  ⚠️  Amount ${invoice['amount']:.2f} exceeds threshold ${APPROVAL_THRESHOLD:.2f}")
        print(f"  ✓ Manager approval required")
    else:
        print(f"  ✓ Amount within auto-approval limit")
        print(f"  ✓ No manager approval needed")
    
    return requires_approval

def send_for_approval(invoice):
    """
    Step 4: Send invoice for manager approval if needed
    """
    print(f"\n[Step 4] Processing approval for {invoice['invoice_id']}...")
    time.sleep(0.4)
    
    requires_approval = check_approval_rules(invoice)
    
    if requires_approval:
        # Send to manager
        print(f"  ✓ Approval request sent to: {MANAGER_EMAIL}")
        print(f"  ✓ Invoice: {invoice['invoice_id']}")
        print(f"  ✓ Amount: ${invoice['amount']:.2f}")
        print(f"  ✓ Vendor: {invoice['vendor']}")
        
        # Mock approval (auto-approve for demo)
        approval_status = "pending"
        print(f"  ⏳ Status: {approval_status.upper()}")
    else:
        # Auto-approve
        approval_status = "auto-approved"
        print(f"  ✓ Status: {approval_status.upper()}")
    
    approval_db[invoice['invoice_id']] = {
        "status": approval_status,
        "timestamp": datetime.now().isoformat(),
        "approver": MANAGER_EMAIL if requires_approval else "system"
    }
    
    return approval_status

def update_accounting_system(invoice, approval_status, validation_results):
    """
    Step 5: Update accounting system with invoice details
    """
    print(f"\n[Step 5] Updating accounting system for {invoice['invoice_id']}...")
    time.sleep(0.4)
    
    if not validation_results['valid']:
        print(f"  ❌ Cannot update - validation failed")
        return False
    
    # Create accounting record
    accounting_record = {
        "invoice_id": invoice['invoice_id'],
        "vendor": invoice['vendor'],
        "amount": invoice['amount'],
        "date": invoice['date'],
        "approval_status": approval_status,
        "payment_status": "scheduled" if approval_status == "auto-approved" else "pending",
        "updated_at": datetime.now().isoformat()
    }
    
    invoice_db[invoice['invoice_id']] = accounting_record
    
    print(f"  ✓ Accounting record created")
    print(f"  ✓ Payment status: {accounting_record['payment_status'].upper()}")
    print(f"  ✓ Notification sent to: {ACCOUNTING_EMAIL}")
    
    return True

def workflow():
    """
    Main invoice processing workflow
    
    Returns:
        Dictionary with processing results
    """
    print("="*60)
    print("INVOICE PROCESSING WORKFLOW")
    print("="*60)
    print(f"Approval threshold: ${APPROVAL_THRESHOLD:.2f}")
    print("="*60)
    
    try:
        # Step 1: Read invoice data
        invoices = read_invoice_data()
        
        processed_invoices = []
        
        # Process each invoice
        for invoice in invoices:
            print("\n" + "-"*60)
            print(f"Processing invoice: {invoice['invoice_id']}")
            print("-"*60)
            
            # Step 2: Validate amounts
            validation_results = validate_invoice_amounts(invoice)
            
            if validation_results['valid']:
                # Step 3 & 4: Check rules and send for approval
                approval_status = send_for_approval(invoice)
                
                # Step 5: Update accounting system
                updated = update_accounting_system(invoice, approval_status, validation_results)
                
                processed_invoices.append({
                    "invoice_id": invoice['invoice_id'],
                    "amount": invoice['amount'],
                    "vendor": invoice['vendor'],
                    "validation": "passed",
                    "approval_status": approval_status,
                    "accounting_updated": updated
                })
            else:
                print(f"  ❌ Invoice rejected due to validation errors")
                processed_invoices.append({
                    "invoice_id": invoice['invoice_id'],
                    "validation": "failed",
                    "issues": validation_results['issues']
                })
        
        print("\n" + "="*60)
        print("✅ INVOICE PROCESSING COMPLETED")
        print("="*60)
        print(f"\nSummary:")
        print(f"  Total invoices: {len(invoices)}")
        print(f"  Successfully processed: {len([i for i in processed_invoices if i.get('validation') == 'passed'])}")
        print(f"  Failed validation: {len([i for i in processed_invoices if i.get('validation') == 'failed'])}")
        
        total_amount = sum(inv['amount'] for inv in invoices 
                          if any(p['invoice_id'] == inv['invoice_id'] and p.get('validation') == 'passed' 
                                for p in processed_invoices))
        print(f"  Total amount processed: ${total_amount:.2f}")
        
        return {
            "status": "success",
            "invoices_processed": len(processed_invoices),
            "total_amount": total_amount,
            "invoices": processed_invoices
        }
        
    except Exception as e:
        print(f"\n❌ Error processing invoices: {str(e)}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # Test the workflow
    result = workflow()
    
    print(f"\nFinal Result: {result['status']}")
    print(f"Total Amount: ${result.get('total_amount', 0):.2f}")
