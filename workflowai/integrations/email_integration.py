"""Real Email Integration for WorkflowAI"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailIntegration:
    """Real Email SMTP integration"""
    
    def __init__(self, use_mock: bool = False):
        """
        Initialize Email client
        
        Args:
            use_mock: If True, use mock responses (for demo safety)
        """
        self.use_mock = use_mock
        
        if not use_mock:
            self.email_address = os.getenv('EMAIL_ADDRESS')
            self.email_password = os.getenv('EMAIL_PASSWORD')
            self.smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
            self.smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
            
            if not self.email_address or not self.email_password:
                raise ValueError("Email credentials required. Set EMAIL_ADDRESS and EMAIL_PASSWORD env vars.")
    
    def send_email(self, 
                   to: str, 
                   subject: str, 
                   body: str,
                   html: bool = False,
                   cc: Optional[List[str]] = None,
                   bcc: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Send email
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text or HTML)
            html: If True, body is HTML
            cc: Optional CC recipients
            bcc: Optional BCC recipients
            
        Returns:
            Response dict with status
        """
        if self.use_mock:
            return self._mock_send_email(to, subject, body)
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_address
            msg['To'] = to
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Attach body
            mime_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, mime_type))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(self.email_address, self.email_password)
                
                recipients = [to]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                
                server.sendmail(self.email_address, recipients, msg.as_string())
            
            return {
                'success': True,
                'message': f"✅ Email sent to {to}",
                'to': to,
                'subject': subject
            }
            
        except smtplib.SMTPAuthenticationError:
            return {
                'success': False,
                'error': 'authentication_failed',
                'message': '❌ Email authentication failed. Check EMAIL_ADDRESS and EMAIL_PASSWORD in .env'
            }
        except smtplib.SMTPException as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ SMTP error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Failed to send email: {str(e)}'
            }
    
    def send_html_email(self,
                       to: str,
                       subject: str,
                       html_body: str,
                       plain_body: Optional[str] = None) -> Dict[str, Any]:
        """
        Send HTML email with plain text fallback
        
        Args:
            to: Recipient email
            subject: Email subject
            html_body: HTML version of email
            plain_body: Plain text fallback (optional)
            
        Returns:
            Response dict
        """
        if self.use_mock:
            return self._mock_send_email(to, subject, html_body)
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_address
            msg['To'] = to
            
            # Plain text version
            if plain_body:
                msg.attach(MIMEText(plain_body, 'plain'))
            
            # HTML version
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, [to], msg.as_string())
            
            return {
                'success': True,
                'message': f"✅ HTML email sent to {to}",
                'to': to,
                'subject': subject
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Failed to send HTML email: {str(e)}'
            }
    
    # Mock method for fallback
    def _mock_send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Mock email sending"""
        return {
            'success': True,
            'message': f"🔷 [MOCK] Email sent to {to}: {subject}",
            'to': to,
            'subject': subject,
            'mock': True
        }


# Convenience function for workflows
def send_email_notification(to: str, subject: str, body: str, use_mock: bool = False) -> str:
    """
    Simple helper for sending email notifications
    
    Usage in generated code:
        from integrations.email_integration import send_email_notification
        result = send_email_notification(
            to='user@example.com',
            subject='Workflow Complete',
            body='Your task finished successfully!'
        )
        print(result)
    """
    email = EmailIntegration(use_mock=use_mock)
    result = email.send_email(to, subject, body)
    return result['message']
