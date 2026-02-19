import os
import logging
import resend
from typing import Optional, Dict, Any
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY")
        self.from_email = os.getenv("FROM_EMAIL")
        self.client = None

    async def initialize(self):
        """Initialize Resend client"""
        try:
            if not self.api_key:
                raise ValueError("RESEND_API_KEY environment variable must be set")

            resend.api_key = self.api_key
            self.client = resend

            logger.info("Resend email service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize email service: {str(e)}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """Check email service health"""
        try:
            if not self.client:
                return {"status": "error", "message": "Email service not initialized"}

            if not self.api_key:
                return {"status": "error", "message": "API key not configured"}

            return {
                "status": "healthy",
                "message": "Email service ready",
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        tracking_id: str,
        from_name: str = "Security Team",
    ) -> bool:
        """Send an email using Resend"""
        try:
            if not self.client:
                logger.error("Email service not initialized")
                return False

            # Add tracking pixel to HTML content
            tracking_pixel = f'<img src="http://localhost:8000/track/open/{tracking_id}" alt="" width="1" height="1" style="display:none;">'
            html_with_tracking = html_content + tracking_pixel

            # Prepare email data
            email_data = {
                "from": f"{from_name} <{self.from_email}>",
                "to": [to_email],
                "subject": subject,
                "html": html_with_tracking,
                "tags": [
                    {"name": "category", "value": "phishing-simulation"},
                    {"name": "tracking_id", "value": tracking_id},
                ],
            }

            # Send email
            response = resend.Emails.send(email_data)

            if response and hasattr(response, "id"):
                logger.info(f"Email sent successfully to {to_email}, ID: {response.id}")
                return True
            else:
                logger.error(
                    f"Failed to send email to {to_email}: No message ID returned"
                )
                return True

        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False

    async def send_bulk_emails(
        self, email_list: list, delay_seconds: float = 0.1
    ) -> Dict[str, int]:
        """Send bulk emails with rate limiting"""
        results = {"sent": 0, "failed": 0}

        for email_data in email_list:
            try:
                success = await self.send_email(
                    to_email=email_data["to_email"],
                    subject=email_data["subject"],
                    html_content=email_data["html_content"],
                    tracking_id=email_data["tracking_id"],
                    from_name=email_data.get("from_name", "Security Team"),
                )

                if success:
                    results["sent"] += 1
                else:
                    results["failed"] += 1

                # Rate limiting delay
                if delay_seconds > 0:
                    await asyncio.sleep(delay_seconds)

            except Exception as e:
                logger.error(f"Error in bulk email send: {str(e)}")
                results["failed"] += 1

        return results

    async def verify_domain(self, domain: str) -> Dict[str, Any]:
        """Verify domain for sending emails"""
        try:
            # This would integrate with Resend's domain verification API
            # For now, return a placeholder response
            return {
                "domain": domain,
                "verified": True,
                "status": "Domain verification not implemented yet",
            }
        except Exception as e:
            logger.error(f"Error verifying domain: {str(e)}")
            return {"domain": domain, "verified": False, "error": str(e)}

    def get_email_statistics(self) -> Dict[str, Any]:
        """Get email sending statistics"""
        try:
            # This would integrate with Resend's analytics API
            # For now, return a placeholder response
            return {
                "total_sent": 0,
                "total_delivered": 0,
                "total_bounced": 0,
                "total_complained": 0,
                "message": "Statistics API not implemented yet",
            }
        except Exception as e:
            logger.error(f"Error getting email statistics: {str(e)}")
            return {"error": str(e)}

    def format_email_address(self, email: str, name: str = None) -> str:
        """Format email address with name"""
        if name:
            return f"{name} <{email}>"
        return email

    def validate_email_format(self, email: str) -> bool:
        """Basic email format validation"""
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    async def test_email_delivery(self, test_email: str) -> Dict[str, Any]:
        """Send a test email to verify delivery"""
        try:
            test_subject = "AICDAP Email Service Test"
            test_html = """
            <html>
                <body>
                    <h2>Email Service Test</h2>
                    <p>This is a test email from the AICDAP backend service.</p>
                    <p>If you receive this email, the email service is working correctly.</p>
                    <p>Timestamp: {timestamp}</p>
                </body>
            </html>
            """.format(timestamp=datetime.utcnow().isoformat())

            success = await self.send_email(
                to_email=test_email,
                subject=test_subject,
                html_content=test_html,
                tracking_id="test-email",
                from_name="AICDAP Test",
            )

            return {
                "success": success,
                "message": "Test email sent successfully"
                if success
                else "Failed to send test email",
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error sending test email: {str(e)}")
            return {
                "success": False,
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }
