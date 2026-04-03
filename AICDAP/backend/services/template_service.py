import os
import logging
from typing import Dict, List, Any, Optional
from jinja2 import Environment, BaseLoader, Template
from datetime import datetime

logger = logging.getLogger(__name__)


class TemplateService:
    def __init__(self):
        self.templates = self._load_templates()
        self.landing_templates = self._load_landing_templates()
        self.jinja_env = Environment(loader=BaseLoader())

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available email templates"""
        return list(self.templates.values())

    def get_template(self, template_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific email template by ID"""
        return self.templates.get(template_id)

    def get_landing_template(self, template_id: str) -> Optional[Template]:
        """Get a specific landing page template by ID"""
        template_str = self.landing_templates.get(template_id)
        if template_str:
            return self.jinja_env.from_string(template_str)
        return None

    def personalize_template(
        self,
        template: Dict[str, Any],
        target: Dict[str, Any],
        tracking_urls: Dict[str, str],
    ) -> Dict[str, str]:
        """Personalize email content using Jinja2"""
        try:
            # Prepare context for template rendering
            context = {
                "employee_name": target.get("name", "there"),
                "employee_email": target.get("email"),
                "department": target.get("department", "your department"),
                "tracking_urls": tracking_urls,
                "current_time": datetime.utcnow().strftime("%I:%M %p"),
            }

            # Render subject
            subject_template = self.jinja_env.from_string(template["subject"])
            personalized_subject = subject_template.render(context)

            # Render HTML content
            html_template = self.jinja_env.from_string(template["html_content"])
            personalized_html = html_template.render(context)

            return {
                "subject": personalized_subject,
                "html": personalized_html,
            }
        except Exception as e:
            logger.error(f"Error personalizing template: {str(e)}")
            # Fallback to generic content
            return {
                "subject": template["subject"],
                "html": template["html_content"],
            }

    def _load_templates(self) -> Dict[int, Dict[str, Any]]:
        """Load all email templates"""
        return {
            1: {
                "template_id": 1,
                "name": "Google Login Phishing",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Google login page to test credential awareness",
                "preview": "You have new messages in your Google account. Please log in to view them.",
                "subject": "New messages in your Google account",
                "html_content": self._get_google_template(),
            },
            2: {
                "template_id": 2,
                "name": "GitHub Security Alert",
                "type": "Security Alert",
                "difficulty": "High",
                "description": "Simulated security breach notification",
                "preview": "Suspicious activity detected on your GitHub account. Immediate action required.",
                "subject": " GitHub Security Alert - Immediate Action Required",
                "html_content": self._get_github_template(),
            },
            3: {
                "template_id": 3,
                "name": "Microsoft Office Update",
                "type": "Software Update",
                "difficulty": "Low",
                "description": "Fake software update notification",
                "preview": "Microsoft Office requires an urgent security update. Click to download.",
                "subject": "Microsoft Office Security Update Required",
                "html_content": self._get_microsoft_template(),
            },
            4: {
                "template_id": 4,
                "name": "Zoom Account Verification Phishing",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Zoom sign-in page to test credential awareness",
                "preview": "Your Zoom session has expired. Please sign in again to continue.",
                "subject": "Your Zoom session has expired",
                "html_content": self._get_zoom_template(),
            },
            5: {
                "template_id": 3,
                "name": "Dropbox Shared Document Phishing",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Dropbox file-sharing notification to test link awareness",
                "preview": "You’ve received a shared document via Dropbox.",
                "subject": "A document was shared with you via Dropbox",
                "html_content": self._get_dropbox_template(),
            },
            6: {
                "template_id": 4,
                "name": "Notion Workspace Invite Phishing",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Notion workspace invitation to test access control awareness",
                "preview": "You have been invited to collaborate on a Notion workspace.",
                "subject": "You’ve been invited to join a Notion workspace",
                "html_content": self._get_notion_template(),
            },
            7: {
                "template_id": 5,
                "name": "Webex Meeting Alert Phishing",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Webex meeting notification to test urgency-based phishing detection",
                "preview": "You have an upcoming Webex meeting starting shortly.",
                "subject": "Reminder: Webex Meeting Starting in 15 Minutes",
                "html_content": self._get_webex_template(),
            },
            8: {
                "template_id": 6,
                "name": "Stack Overflow Security Alert Phishing",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Stack Overflow security alert to test developer awareness",
                "preview": "Suspicious activity detected on your Stack Overflow account.",
                "subject": "Security Alert: Suspicious Login Attempt",
                "html_content": self._get_stackoverflow_template(),
            },
            9: {
                "template_id": 9,
                "name": "AWS Billing Suspension Phishing",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake AWS billing alert to test financial and cloud credential awareness",
                "preview": "Your AWS account has been temporarily restricted due to a billing issue.",
                "subject": "Action Required: AWS Account Billing Issue",
                "html_content": self._get_aws_template(),
            },
            10: {
                "template_id": 10,
                "name": "GCP IAM Policy Change Phishing",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake GCP IAM modification alert to test cloud security awareness",
                "preview": "An IAM role in your Google Cloud project has been modified.",
                "subject": "Security Alert: IAM Role Updated in Your Project",
                "html_content": self._get_gcp_template(),
            },
            11: {
                "template_id": 11,
                "name": "Docker Repository Access Phishing",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Docker repository access notification to test developer vigilance",
                "preview": "A new collaborator has been added to your Docker repository.",
                "subject": "New Collaborator Added to Your Docker Repository",
                "html_content": self._get_docker_template(),
            },
            12: {
                "template_id": 12,
                "name": "Azure Subscription Security Alert",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Azure subscription alert to test enterprise cloud awareness",
                "preview": "Unusual sign-in activity detected in your Azure subscription.",
                "subject": "Microsoft Azure: Unusual Sign-in Activity Detected",
                "html_content": self._get_azure_template(),
            },
            13: {
                "template_id": 13,
                "name": "Zoho Mail Quota Exceeded Phishing",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Zoho mail storage warning to test account verification awareness",
                "preview": "Your Zoho mailbox has exceeded its storage limit.",
                "subject": "Zoho Mail: Storage Limit Exceeded",
                "html_content": self._get_zoho_template(),
            },
            14: {
                "template_id": 14,
                "name": "Intercom Account Access Alert",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Intercom login notification to test SaaS credential awareness",
                "preview": "New login detected in your Intercom workspace.",
                "subject": "New Login to Your Intercom Workspace",
                "html_content": self._get_intercom_template(),
            },
            15: {
                "template_id": 15,
                "name": "Salesforce Permission Update Phishing",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Salesforce permission modification alert",
                "preview": "Your Salesforce role permissions have been updated.",
                "subject": "Action Required: Salesforce Role Permissions Updated",
                "html_content": self._get_salesforce_template(),
            },
            16: {
                "template_id": 16,
                "name": "Pipedrive Deal Assignment Alert",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Pipedrive deal assignment notification",
                "preview": "You have been assigned a new deal in Pipedrive.",
                "subject": "New Deal Assigned to You",
                "html_content": self._get_pipedrive_template(),
            },
            17: {
                "template_id": 17,
                "name": "Marketo Campaign Approval Required",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Marketo campaign approval request",
                "preview": "A marketing campaign requires your approval.",
                "subject": "Marketo: Campaign Pending Approval",
                "html_content": self._get_marketo_template(),
            },
            18: {
                "template_id": 18,
                "name": "HubSpot Contact Import Alert",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake HubSpot data import notification",
                "preview": "A new contact list has been imported into your HubSpot account.",
                "subject": "HubSpot: New Contact List Imported",
                "html_content": self._get_hubspot_template(),
            },
            19: {
                "template_id": 19,
                "name": "Google Analytics Traffic Spike Alert",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Google Analytics anomaly alert",
                "preview": "Unusual traffic spike detected in your Analytics property.",
                "subject": "Alert: Unusual Traffic Activity Detected",
                "html_content": self._get_google_analytics_template(),
            },
            20: {
                "template_id": 20,
                "name": "Canva Team Invitation Phishing",
                "type": "Social Engineering",
                "difficulty": "Easy",
                "description": "Fake Canva team invitation notification",
                "preview": "You’ve been invited to collaborate on Canva designs.",
                "subject": "You’ve Been Invited to Join a Canva Team",
                "html_content": self._get_canva_template(),
            },
            21: {
                "template_id": 21,
                "name": "Buffer Scheduled Post Alert",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Buffer scheduled post failure alert",
                "preview": "Your scheduled post failed to publish.",
                "subject": "Buffer: Scheduled Post Failed",
                "html_content": self._get_buffer_template(),
            },
            22: {
                "template_id": 22,
                "name": "WordPress Plugin Vulnerability Alert",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake WordPress security vulnerability alert",
                "preview": "Critical vulnerability detected in your WordPress installation.",
                "subject": "Critical Security Alert for Your WordPress Site",
                "html_content": self._get_wordpress_template(),
            },
            23: {
                "template_id": 23,
                "name": "LinkedIn Suspicious Login Alert",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake LinkedIn login alert to test professional account awareness",
                "preview": "New login detected from an unfamiliar location.",
                "subject": "LinkedIn: New Sign-in Detected",
                "html_content": self._get_linkedin_template(),
            },
            24: {
                "template_id": 24,
                "name": "Twitter/X Account Lock Alert",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Twitter/X account restriction alert",
                "preview": "Your account has been temporarily locked due to suspicious activity.",
                "subject": "Action Required: Your X Account is Locked",
                "html_content": self._get_twitter_template(),
            },

            25: {
                "template_id": 25,
                "name": "Facebook Security Verification",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Facebook security verification request",
                "preview": "We noticed unusual activity on your Facebook account.",
                "subject": "Facebook Security Alert",
                "html_content": self._get_facebook_template(),
            },

            26: {
                "template_id": 26,
                "name": "Instagram Copyright Violation Notice",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Instagram copyright infringement notice",
                "preview": "Your post has been reported for copyright violation.",
                "subject": "Instagram: Copyright Violation Warning",
                "html_content": self._get_instagram_template(),
            },

            27: {
                "template_id": 27,
                "name": "Adobe Creative Cloud Subscription Expired",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Adobe Creative Cloud subscription renewal alert",
                "preview": "Your Creative Cloud subscription has expired.",
                "subject": "Adobe: Subscription Renewal Required",
                "html_content": self._get_adobe_template(),
            },

            28: {
                "template_id": 28,
                "name": "Hootsuite Social Account Reconnect",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Hootsuite account reconnection alert",
                "preview": "Your connected social account requires reauthorization.",
                "subject": "Hootsuite: Reconnect Your Social Account",
                "html_content": self._get_hootsuite_template(),
            },

            29: {
                "template_id": 29,
                "name": "PayPal Unauthorized Transaction Alert",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake PayPal transaction alert to test financial awareness",
                "preview": "You sent a payment of $489.99. Was this you?",
                "subject": "PayPal: Confirm Your Recent Transaction",
                "html_content": self._get_paypal_template(),
            },

            30: {
                "template_id": 30,
                "name": "Razorpay Payment Failure Notification",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Razorpay payment processing failure notice",
                "preview": "Your recent payment attempt could not be processed.",
                "subject": "Razorpay: Payment Failed",
                "html_content": self._get_razorpay_template(),
            },

            31: {
                "template_id": 31,
                "name": "Google Pay Transaction Verification",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Google Pay suspicious transaction alert",
                "preview": "A payment request requires your confirmation.",
                "subject": "Google Pay: Confirm Payment Request",
                "html_content": self._get_googlepay_template(),
            },

            32: {
                "template_id": 32,
                "name": "HDFC Bank KYC Update Required",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake HDFC KYC compliance update request",
                "preview": "Your bank account will be restricted due to incomplete KYC.",
                "subject": "HDFC Bank: Update Your KYC Details",
                "html_content": self._get_hdfc_template(),
            },

            33: {
                "template_id": 33,
                "name": "SBI Account Suspension Warning",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake SBI account suspension notice",
                "preview": "Your SBI account has been flagged for unusual activity.",
                "subject": "SBI: Immediate Action Required",
                "html_content": self._get_sbi_template(),
            },

            34: {
                "template_id": 34,
                "name": "Amazon Order Confirmation Issue",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Amazon order verification notice",
                "preview": "Problem with your recent Amazon order.",
                "subject": "Amazon: Confirm Your Recent Order",
                "html_content": self._get_amazon_template(),
            },

            35: {
                "template_id": 35,
                "name": "Flipkart Delivery Failed Notice",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Flipkart delivery failure alert",
                "preview": "Your delivery could not be completed.",
                "subject": "Flipkart: Delivery Attempt Failed",
                "html_content": self._get_flipkart_template(),
            },

            36: {
                "template_id": 36,
                "name": "eBay Account Verification Required",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake eBay account verification request",
                "preview": "Your eBay account requires verification.",
                "subject": "eBay: Verify Your Account",
                "html_content": self._get_ebay_template(),
            },

            37: {
                "template_id": 37,
                "name": "Indeed Application Status Update",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Indeed job application update",
                "preview": "Your job application status has changed.",
                "subject": "Indeed: Update on Your Application",
                "html_content": self._get_indeed_template(),
            },

            38: {
                "template_id": 38,
                "name": "Sketch License Expiration Alert",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Sketch license expiration notice",
                "preview": "Your Sketch license is about to expire.",
                "subject": "Sketch: License Renewal Required",
                "html_content": self._get_sketch_template(),
            },

            39: {
                "template_id": 39,
                "name": "Figma Team Access Notification",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Figma team access notification",
                "preview": "You have been added to a Figma team.",
                "subject": "Figma: Team Invitation",
                "html_content": self._get_figma_template(),
            },

            40: {
                "template_id": 40,
                "name": "ADP Payroll Processing Alert",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake ADP payroll processing issue notice",
                "preview": "There was an issue processing your payroll information.",
                "subject": "ADP: Payroll Information Update Required",
                "html_content": self._get_adp_template(),
            },
            41: {
                "template_id": 41,
                "name": "Discord Account Verification Required",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Discord account verification alert",
                "preview": "Your Discord account requires verification due to unusual activity.",
                "subject": "Discord: Verify Your Account",
                "html_content": self._get_discord_template(),
            },

            42: {
                "template_id": 42,
                "name": "iCloud Storage Suspension Notice",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake iCloud storage limit warning",
                "preview": "Your iCloud storage is almost full.",
                "subject": "Apple iCloud: Storage Almost Full",
                "html_content": self._get_icloud_template(),
            },

            43: {
                "template_id": 43,
                "name": "OneDrive File Share Notification",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake OneDrive shared file notification",
                "preview": "A file has been shared with you via OneDrive.",
                "subject": "OneDrive: File Shared With You",
                "html_content": self._get_onedrive_template(),
            },

            44: {
                "template_id": 44,
                "name": "Jenkins Build Failure Alert",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Jenkins build failure notification",
                "preview": "Build pipeline failed in your Jenkins project.",
                "subject": "Jenkins: Build Failure Notification",
                "html_content": self._get_jenkins_template(),
            },

            45: {
                "template_id": 45,
                "name": "PhonePe Payment Request Alert",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake PhonePe payment request notification",
                "preview": "You have received a new payment request.",
                "subject": "PhonePe: Payment Request Pending",
                "html_content": self._get_phonepe_template(),
            },

            46: {
                "template_id": 46,
                "name": "Tally License Expiration Notice",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Tally software license expiration alert",
                "preview": "Your Tally license is about to expire.",
                "subject": "Tally: License Renewal Required",
                "html_content": self._get_tally_template(),
            },

            47: {
                "template_id": 47,
                "name": "YouTube Copyright Strike Warning",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake YouTube copyright strike notification",
                "preview": "Your video has received a copyright strike.",
                "subject": "YouTube: Copyright Claim Notice",
                "html_content": self._get_youtube_template(),
            },

            48: {
                "template_id": 48,
                "name": "Udemy Course Access Suspended",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Udemy account access suspension notice",
                "preview": "Your Udemy course access has been restricted.",
                "subject": "Udemy: Account Access Issue",
                "html_content": self._get_udemy_template(),
            },

            49: {
                "template_id": 49,
                "name": "Coursera Certificate Verification Required",
                "type": "Social Engineering",
                "difficulty": "Medium",
                "description": "Fake Coursera certificate verification alert",
                "preview": "Verify your certificate details to avoid revocation.",
                "subject": "Coursera: Certificate Verification Needed",
                "html_content": self._get_coursera_template(),
            },

            50: {
                "template_id": 50,
                "name": "Power BI Report Access Alert",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Power BI report access notification",
                "preview": "A confidential report has been shared with you.",
                "subject": "Power BI: New Report Shared",
                "html_content": self._get_powerbi_template(),
            },

            51: {
                "template_id": 51,
                "name": "Tableau Dashboard Access Alert",
                "type": "Social Engineering",
                "difficulty": "Hard",
                "description": "Fake Tableau dashboard access notification",
                "preview": "You have been granted access to a Tableau dashboard.",
                "subject": "Tableau: Dashboard Access Granted",
                "html_content": self._get_tableau_template(),
            },

        }

    def _load_landing_templates(self) -> Dict[str, str]:
            """Load landing page templates"""
            return {
                "1": self._get_google_landing_page(),
                "2": self._get_github_landing_page(),
                "3": self._get_microsoft_landing_page(),
                "4": self._get_zoom_landing_page(),
                "5": self._get_dropbox_landing_page(),
                "6": self._get_notion_landing_page(),
                "7": self._get_webex_landing_page(),
                "8": self._get_stackoverflow_landing_page(),
                "9": self._get_aws_landing_page(),
                "10": self._get_gcp_landing_page(),
                "11": self._get_docker_landing_page(),
                "12": self._get_azure_landing_page(),
                "13": self._get_zoho_landing_page(),
                "14": self._get_intercom_landing_page(),
                "15": self._get_salesforce_landing_page(),
                "16": self._get_pipedrive_landing_page(),
                "17": self._get_marketo_landing_page(),
                "18": self._get_hubspot_landing_page(),
                "19": self._get_google_analytics_landing_page(),
                "20": self._get_canva_landing_page(),
                "21": self._get_buffer_landing_page(),
                "22": self._get_wordpress_landing_page(),
                "23": self._get_linkedin_landing_page(),
                "24": self._get_twitter_landing_page(),
                "25": self._get_facebook_landing_page(),
                "26": self._get_instagram_landing_page(),
                "27": self._get_adobe_landing_page(),
                "28": self._get_hootsuite_landing_page(),
                "29": self._get_paypal_landing_page(),
                "30": self._get_razorpay_landing_page(),
                "31": self._get_googlepay_landing_page(),
                "32": self._get_hdfc_landing_page(),
                "33": self._get_sbi_landing_page(),
                "34": self._get_amazon_landing_page(),
                "35": self._get_flipkart_landing_page(),
                "36": self._get_ebay_landing_page(),
                "37": self._get_indeed_landing_page(),
                "38": self._get_sketch_landing_page(),
                "39": self._get_figma_landing_page(),
                "40": self._get_adp_landing_page(),
                "41": self._get_discord_landing_page(),
                "42": self._get_icloud_landing_page(),
                "43": self._get_onedrive_landing_page(),
                "44": self._get_jenkins_landing_page(),
                "45": self._get_phonepe_landing_page(),
                "46": self._get_tally_landing_page(),
                "47": self._get_youtube_landing_page(),
                "48": self._get_udemy_landing_page(),
                "49": self._get_coursera_landing_page(),
                "50": self._get_powerbi_landing_page(),
                "51": self._get_tableau_landing_page(),
        }

    def _get_google_template(self) -> str:
        """Google Login Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #4285f4; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #4285f4; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Google</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> You have unread messages in your Google account that require immediate attention.
            </div>

            <p>We've detected that you have {{ message_count | default('3') }} new important messages waiting in your Google account. These messages may contain time-sensitive information that requires your immediate review.</p>

            <p>For your security, please verify your identity to access these messages:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & View Messages
                </a>
            </div>

            <p><strong>Message Preview:</strong></p>
            <ul>
                <li>Account verification required (2 hours ago)</li>
                <li>Important security update (1 hour ago)</li>
                <li>New sign-in from unknown device (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, your account may be temporarily suspended for security reasons.</p>

            <p>Best regards,<br>
            Google Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Google LLC. All rights reserved.</p>
            <p>This message was sent to verify your account security as part of our ongoing security measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_github_template(self) -> str:
        """GitHub Security Alert Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Security Alert</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; margin: 0; padding: 0; background-color: #f6f8fa; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #d1d9e0; }
        .header { background-color: #24292e; padding: 20px; color: white; }
        .content { padding: 30px; }
        .alert-danger { background-color: #f8d7da; border: 1px solid #f1aeb5; color: #721c24; padding: 15px; border-radius: 6px; margin: 20px 0; }
        .button-danger { display: inline-block; padding: 12px 30px; background-color: #d73a49; color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }
        .code-block { background-color: #f6f8fa; border: 1px solid #e1e4e8; padding: 15px; border-radius: 6px; font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px; }
        .footer { background-color: #f6f8fa; padding: 20px; font-size: 12px; color: #586069; border-top: 1px solid #e1e4e8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0; font-size: 24px;">
                <span style="margin-right: 10px;">🐙</span>
                GitHub Security Alert
            </h1>
        </div>
        <div class="content">
            <p>Hello {{ employee_name }},</p>

            <div class="alert-danger">
                <strong>🚨 Critical Security Alert</strong><br>
                Suspicious activity has been detected on your GitHub account.
            </div>

            <p>We've detected potentially malicious activity associated with your GitHub account <strong>{{ employee_email }}</strong>. Our security systems have identified the following concerning activities:</p>

            <div class="code-block">
                <strong>Detected Issues:</strong><br>
                • Multiple failed login attempts from IP: 185.220.101.32<br>
                • Unauthorized access attempt to private repositories<br>
                • Suspicious API token usage detected<br>
                • Account accessed from new location: Moscow, Russia
            </div>

            <p>To protect your repositories and sensitive code, we've temporarily restricted certain account functions. Please verify your identity immediately to restore full access:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button-danger">
                    🔒 Verify Account & Review Security
                </a>
            </div>

            <p><strong>What you should do:</strong></p>
            <ol>
                <li>Click the verification button above</li>
                <li>Review your recent account activity</li>
                <li>Update your password if necessary</li>
                <li>Enable two-factor authentication</li>
            </ol>

            <p><strong>Timeline of suspicious activity:</strong></p>
            <ul>
                <li><strong>{{ current_time | default('2:30 PM') }}:</strong> Multiple failed login attempts</li>
                <li><strong>{{ current_time | default('2:45 PM') }}:</strong> Unusual API requests detected</li>
                <li><strong>{{ current_time | default('3:00 PM') }}:</strong> Account access from foreign IP</li>
            </ul>

            <p>If you don't take action within the next 2 hours, we may need to suspend your account to prevent potential data breaches.</p>

            <p>Stay secure,<br>
            The GitHub Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e1e4e8;">
            <p style="font-size: 12px; color: #586069;">
                This alert was sent to {{ employee_email }} because your account security settings require immediate attention.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>GitHub, Inc. • San Francisco, CA</p>
            <p>This is an automated security notification. For more information, visit our security center.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_microsoft_template(self) -> str:
        """Microsoft Office Update Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft Office Update</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #f3f2f1; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background: linear-gradient(90deg, #0078d4 0%, #106ebe 100%); padding: 20px; color: white; }
        .content { padding: 30px; }
        .update-box { background-color: #fff4ce; border-left: 4px solid #ffb900; padding: 15px; margin: 20px 0; }
        .button-update { display: inline-block; padding: 12px 30px; background-color: #0078d4; color: white; text-decoration: none; border-radius: 2px; margin: 20px 0; }
        .version-info { background-color: #f3f2f1; padding: 15px; border-radius: 4px; margin: 15px 0; }
        .footer { background-color: #f3f2f1; padding: 20px; font-size: 12px; color: #605e5c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0; font-size: 24px;">
                <span style="margin-right: 10px;"></span>
                Microsoft Office
            </h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">Security Update Required</p>
        </div>
        <div class="content">
            <p>Hello {{ employee_name }},</p>

            <div class="update-box">
                <strong>⚠️ Critical Update Available</strong><br>
                A critical security update for Microsoft Office is now available and requires immediate installation.
            </div>

            <p>Microsoft has released an important security update for Office applications that addresses several critical vulnerabilities. This update is essential for maintaining the security and stability of your Office suite.</p>

            <div class="version-info">
                <strong>Update Details:</strong><br>
                <strong>Current Version:</strong> Microsoft Office 2021 (16.0.14931.20764)<br>
                <strong>New Version:</strong> Microsoft Office 2021 (16.0.15726.20202)<br>
                <strong>Size:</strong> 127.8 MB<br>
                <strong>Type:</strong> Security & Performance Update
            </div>

            <p><strong>This update addresses:</strong></p>
            <ul>
                <li>Security vulnerability in Excel macro processing</li>
                <li>Word document parsing security flaw</li>
                <li>PowerPoint remote code execution vulnerability</li>
                <li>Outlook email attachment security issue</li>
                <li>Performance improvements and bug fixes</li>
            </ul>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button-update">
                    📥 Download & Install Update
                </a>
            </div>

            <div class="update-box">
                <strong>Important:</strong> This update must be installed within 48 hours to maintain compliance with your organization's security policies.
            </div>

            <p><strong>Installation Instructions:</strong></p>
            <ol>
                <li>Click the download button above</li>
                <li>Close all Office applications</li>
                <li>Run the update installer as administrator</li>
                <li>Restart your computer when prompted</li>
            </ol>

            <p>If you experience any issues during installation, please contact your IT department immediately.</p>

            <p>Best regards,<br>
            Microsoft Office Update Service</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e1dfdd;">
            <p style="font-size: 12px; color: #605e5c;">
                This update notification was sent to {{ employee_email }} based on your current Office installation.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Microsoft Corporation. All rights reserved.</p>
            <p>Microsoft Office | Redmond, WA 98052 | <a href="#" style="color: #0078d4;">Privacy Policy</a></p>
        </div>
    </div>
</body>
</html>
        """
    def _get_zoom_template(self) -> str:
        """Zoom Account Verification Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zoom Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #2D8CFF; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #2D8CFF; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Zoom</div>
        </div>
        <div class="content">
            <h2>Important Account Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Zoom account that requires verification.
            </div>

            <p>Our system identified {{ meeting_count | default('2') }} recent meeting activities that require your confirmation. These may include meeting access from a new device or location.</p>

            <p>For your security, please verify your identity to review your account activity and ensure uninterrupted access to your meetings and recordings:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                     Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Recent Activity Summary:</strong></p>
            <ul>
                <li>New sign-in from unrecognized device (1 hour ago)</li>
                <li>Meeting joined from unknown location (45 minutes ago)</li>
                <li>Password change request initiated (30 minutes ago)</li>
            </ul>

            <p>If you do not verify your account within 24 hours, your meeting hosting privileges may be temporarily restricted for security purposes.</p>

            <p>Best regards,<br>
            Zoom Trust & Safety Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you did not attempt to access your Zoom account, please secure your account immediately.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Zoom Video Communications, Inc. All rights reserved.</p>
            <p>This message was sent as part of Zoom’s ongoing account security monitoring.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_dropbox_template(self) -> str:
        """Dropbox Shared File Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dropbox File Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #0061FF; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #0061FF; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Dropbox</div>
        </div>
        <div class="content">
            <h2>New File Shared With You</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>Action Required:</strong> A file has been shared with you and is awaiting your review.
            </div>

            <p>You have received {{ file_count | default('1') }} new shared document(s) in your Dropbox account. The file may contain important updates that require your immediate attention.</p>

            <p>Please verify your identity to securely access the shared file:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 View Shared File
                </a>
            </div>

            <p><strong>File Details:</strong></p>
            <ul>
                <li>File Name: Project_Update_Q1_2026.pdf</li>
                <li>Shared By: HR Department</li>
                <li>Shared: 2 hours ago</li>
            </ul>

            <p>This shared link will expire within 24 hours for security reasons.</p>

            <p>Best regards,<br>
            Dropbox Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you were not expecting this file, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Dropbox, Inc. All rights reserved.</p>
            <p>This message was sent to notify you of file activity in your Dropbox account.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_notion_template(self) -> str:
        """Notion Workspace Invitation Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notion Workspace Invitation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #000000; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #000000; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Notion</div>
        </div>
        <div class="content">
            <h2>Workspace Invitation & Access Verification</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> You have been invited to collaborate on a Notion workspace that requires account verification.
            </div>

            <p>You’ve received {{ invite_count | default('1') }} new workspace invitation(s). These workspaces may contain shared documents, databases, task boards, and internal project resources that require secure access.</p>

            <p><strong>Workspace Details:</strong></p>
            <ul>
                <li>Workspace Name: Q1 Strategy & Planning</li>
                <li>Invited By: Operations Team</li>
                <li>Access Role: Editor</li>
                <li>Invitation Sent: 1 hour ago</li>
            </ul>

            <p>For security reasons, please verify your account before accessing shared content. This helps us ensure that only authorized collaborators can view sensitive company data.</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Accept Invitation
                </a>
            </div>

            <p>If you do not accept this invitation within 48 hours, the workspace access request may expire automatically.</p>

            <p>Best regards,<br>
            The Notion Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you were not expecting this invitation, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Notion Labs, Inc. All rights reserved.</p>
            <p>This notification was sent regarding activity in your Notion account.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_webex_template(self) -> str:
        """Webex Account Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webex Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #1BA0D7; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #1BA0D7; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Webex by Cisco</div>
        </div>
        <div class="content">
            <h2>Important Webex Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual meeting activity associated with your Webex account.
            </div>

            <p>Our monitoring system identified {{ meeting_count | default('2') }} recent meeting-related activities that require verification. This may include new device access or meeting host changes.</p>

            <p>To maintain secure access to your meetings, recordings, and collaboration spaces, please verify your account immediately:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Webex Account
                </a>
            </div>

            <p><strong>Recent Activity Summary:</strong></p>
            <ul>
                <li>New login from unrecognized browser (1 hour ago)</li>
                <li>Meeting host privileges modified (45 minutes ago)</li>
                <li>Password reset attempt initiated (30 minutes ago)</li>
            </ul>

            <p>If you do not verify your account within 24 hours, your meeting scheduling and hosting privileges may be temporarily restricted.</p>

            <p>Best regards,<br>
            Cisco Webex Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you did not attempt to access your Webex account, please secure your account immediately.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Cisco Systems, Inc. All rights reserved.</p>
            <p>This message was sent as part of Webex account security monitoring.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_stackoverflow_template(self) -> str:
        """Stack Overflow Security Alert Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stack Overflow Security Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #F48024; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #F48024; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Stack Overflow</div>
        </div>
        <div class="content">
            <h2>Security Alert: Account Activity Detected</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> A new login attempt was detected on your Stack Overflow account.
            </div>

            <p>We noticed {{ login_attempts | default('1') }} recent login attempt(s) from an unfamiliar device or location. If this was not you, your account credentials may be at risk.</p>

            <p>Please verify your account activity to ensure your profile, reputation points, and saved content remain secure:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Review Account Activity
                </a>
            </div>

            <p><strong>Login Details:</strong></p>
            <ul>
                <li>Location: Frankfurt, Germany</li>
                <li>Browser: Chrome on Windows</li>
                <li>Time: 35 minutes ago</li>
            </ul>

            <p>If you do not verify your account within 24 hours, temporary restrictions may be applied to protect your account.</p>

            <p>Best regards,<br>
            Stack Overflow Trust & Safety Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you did not initiate this login attempt, please secure your account immediately.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Stack Exchange Inc. All rights reserved.</p>
            <p>This notification was sent as part of Stack Overflow's account security monitoring.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_aws_template(self) -> str:
        """AWS Billing Alert Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #FF9900; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #FF9900; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Amazon Web Services</div>
        </div>
        <div class="content">
            <h2>Important Billing Notification</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We were unable to process your recent AWS payment.
            </div>

            <p>Your AWS account shows {{ resource_count | default('3') }} active service(s) that may be affected due to a billing issue. To avoid service interruption, please update your billing information.</p>

            <p>Verify your account to prevent suspension of EC2 instances, S3 storage, and other cloud services:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Update Billing Information
                </a>
            </div>

            <p><strong>Affected Services:</strong></p>
            <ul>
                <li>EC2 Compute Instance</li>
                <li>S3 Storage Bucket</li>
                <li>RDS Database Service</li>
            </ul>

            <p>If no action is taken within 24 hours, your services may be temporarily suspended.</p>

            <p>Best regards,<br>
            AWS Billing Support</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your AWS account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Amazon Web Services, Inc. All rights reserved.</p>
            <p>This message was sent as part of AWS account management services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_gcp_template(self) -> str:
        """Google Cloud Platform Security Alert Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Cloud Platform Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #1A73E8; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #1A73E8; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Google Cloud</div>
        </div>
        <div class="content">
            <h2>Security Alert: IAM Role Updated</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> An IAM role in your project has been modified.
            </div>

            <p>We detected {{ change_count | default('1') }} recent change(s) in your Google Cloud project permissions. Unauthorized modifications may impact service security.</p>

            <p>Please review this activity immediately:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Review IAM Activity
                </a>
            </div>

            <p><strong>Project Affected:</strong></p>
            <ul>
                <li>Project ID: production-data-analytics</li>
                <li>Role Modified: Owner → Editor</li>
                <li>Time: 45 minutes ago</li>
            </ul>

            <p>If this change was not authorized, secure your account immediately.</p>

            <p>Best regards,<br>
            Google Cloud Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your Google Cloud account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Google Cloud. All rights reserved.</p>
            <p>This message was sent as part of Google Cloud security monitoring.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_docker_template(self) -> str:
        """Docker Repository Access Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Docker Repository Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #2496ED; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #2496ED; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Docker</div>
        </div>
        <div class="content">
            <h2>Repository Access Notification</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> A new collaborator has been added to your repository.
            </div>

            <p>Your repository "{{ repo_name | default('backend-service-api') }}" has been accessed from a new device.</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Review Repository Activity
                </a>
            </div>

            <ul>
                <li>New collaborator added</li>
                <li>Image pushed 30 minutes ago</li>
                <li>Access from unknown IP address</li>
            </ul>

            <p>If you did not authorize this activity, please secure your Docker account immediately.</p>

            <p>Best regards,<br>
            Docker Security Team</p>

            <hr style="margin: 30px 0; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your Docker account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Docker, Inc. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_azure_template(self) -> str:
        """Microsoft Azure Security Alert Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft Azure Security Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #0078D4; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #0078D4; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Microsoft Azure</div>
        </div>
        <div class="content">
            <h2>Important Security Notification</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual sign-in activity in your Azure subscription.
            </div>

            <p>Our security monitoring systems identified {{ login_attempts | default('2') }} recent sign-in attempt(s) associated with your Azure Active Directory account. These attempts originated from a new device and geographic location.</p>

            <p>To protect your virtual machines, storage accounts, databases, and cloud resources, we recommend verifying your identity immediately.</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Review Sign-in Activity
                </a>
            </div>

            <p><strong>Sign-in Details:</strong></p>
            <ul>
                <li>Location: Singapore</li>
                <li>Device: Chrome on Windows</li>
                <li>IP Address: 52.187.xxx.xxx</li>
                <li>Time: 25 minutes ago</li>
            </ul>

            <p>If this activity is not verified within 24 hours, temporary access restrictions may be applied to your Azure subscription as a precautionary measure.</p>

            <p>Best regards,<br>
            Microsoft Azure Security Team</p>

            <hr style="margin: 30px 0; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your Azure subscription security.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Microsoft Corporation. All rights reserved.</p>
            <p>This notification was generated automatically as part of Azure’s security monitoring system.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_zoho_template(self) -> str:
        """Zoho Mail Storage Alert Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zoho Mail Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #E42527; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #E42527; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Zoho</div>
        </div>
        <div class="content">
            <h2>Mailbox Storage Capacity Alert</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> Your Zoho Mail storage has exceeded the recommended usage limit.
            </div>

            <p>Your mailbox is currently at {{ storage_usage | default('98%') }} capacity. Once the storage limit is reached, incoming emails will be rejected and sending functionality may be restricted.</p>

            <p>To ensure uninterrupted communication and access to your business emails, please verify your account and upgrade your storage allocation if necessary.</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Manage Mailbox Storage
                </a>
            </div>

            <p><strong>Storage Summary:</strong></p>
            <ul>
                <li>Storage Used: 4.9 GB</li>
                <li>Total Allocation: 5 GB</li>
                <li>Last Login: 1 hour ago</li>
                <li>Plan: Business Starter</li>
            </ul>

            <p>If no action is taken within 24 hours, certain mail services may be temporarily restricted.</p>

            <p>Best regards,<br>
            Zoho Mail Support Team</p>

            <hr style="margin: 30px 0; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your Zoho account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Zoho Corporation Pvt. Ltd. All rights reserved.</p>
            <p>This message was generated as part of Zoho's account monitoring services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_intercom_template(self) -> str:
        """Intercom Account Activity Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intercom Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #1F8DED; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #1F8DED; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Intercom</div>
        </div>
        <div class="content">
            <h2>Important Workspace Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual login activity in your Intercom workspace.
            </div>

            <p>Our monitoring system identified {{ login_attempts | default('2') }} recent access attempts from a new browser session. This may impact access to customer conversations and automation workflows.</p>

            <p>To maintain secure access to your inbox, live chat, and customer support tools, please verify your account immediately.</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Review Workspace Activity
                </a>
            </div>

            <ul>
                <li>New login from unknown device</li>
                <li>Conversation export attempted</li>
                <li>Admin settings accessed</li>
            </ul>

            <p>If no action is taken within 24 hours, temporary restrictions may be applied.</p>

            <p>Best regards,<br>
            Intercom Security Team</p>

            <hr style="margin: 30px 0; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This message was sent to {{ employee_email }} regarding your Intercom account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Intercom, Inc. All rights reserved.</p>
            <p>This notification was generated automatically for account security purposes.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_salesforce_template(self) -> str:
        """Salesforce Permission Change Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Salesforce Security Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #00A1E0; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #00A1E0; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">Salesforce</div>
    </div>
    <div class="content">
        <h2>Role & Permission Update Notice</h2>
        <p>Hello {{ employee_name }},</p>

        <div class="alert-box">
            <strong>⚠️ Action Required:</strong> Your Salesforce role permissions were recently modified.
        </div>

        <p>We detected {{ change_count | default('1') }} recent change(s) affecting access to CRM records, reports, or dashboards.</p>

        <p>Please verify this activity to ensure your sales data and customer records remain secure.</p>

        <div style="text-align: center;">
            <a href="{{ tracking_urls.click }}" class="button">
                🔐 Review Permission Changes
            </a>
        </div>

        <ul>
            <li>Profile access updated</li>
            <li>New API token generated</li>
            <li>Report export initiated</li>
        </ul>

        <p>If this modification was unauthorized, secure your account immediately.</p>

        <p>Best regards,<br>
        Salesforce Trust Team</p>

        <hr style="margin: 30px 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            Sent to {{ employee_email }} regarding Salesforce account activity.
        </p>
    </div>
    
    <!-- Report Phishing Button -->
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
        <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
            Report Phishing
        </a>
    </div>
    <div class="footer">
        <p>© 2024 Salesforce, Inc. All rights reserved.</p>
    </div>
</div>
</body>
</html>
        """
    def _get_pipedrive_template(self) -> str:
        """Pipedrive Deal Activity Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pipedrive Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #2ECC71; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #2ECC71; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">Pipedrive</div>
    </div>
    <div class="content">
        <h2>Deal Assignment Notification</h2>
        <p>Hello {{ employee_name }},</p>

        <div class="alert-box">
            <strong>⚠️ Action Required:</strong> A new deal has been assigned to your account.
        </div>

        <p>The deal "{{ deal_name | default('Enterprise Renewal Q1') }}" requires your immediate review and action.</p>

        <div style="text-align: center;">
            <a href="{{ tracking_urls.click }}" class="button">
                🔐 View Deal Details
            </a>
        </div>

        <ul>
            <li>Pipeline Stage Updated</li>
            <li>New note added</li>
            <li>Activity scheduled</li>
        </ul>

        <p>Please confirm this assignment to ensure accurate reporting.</p>

        <p>Best regards,<br>
        Pipedrive Support Team</p>

        <hr style="margin: 30px 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            Sent to {{ employee_email }} regarding CRM activity.
        </p>
    </div>
    
    <!-- Report Phishing Button -->
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
        <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
            Report Phishing
        </a>
    </div>
    <div class="footer">
        <p>© 2024 Pipedrive OÜ. All rights reserved.</p>
    </div>
</div>
</body>
</html>
        """
    def _get_marketo_template(self) -> str:
        """Marketo Campaign Approval Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Marketo Campaign Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #5C4EE5; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #5C4EE5; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">Marketo</div>
    </div>
    <div class="content">
        <h2>Campaign Approval Required</h2>
        <p>Hello {{ employee_name }},</p>

        <div class="alert-box">
            <strong>⚠️ Action Required:</strong> A marketing automation campaign is pending approval.
        </div>

        <p>The campaign "{{ campaign_name | default('Product Launch Series') }}" requires your verification before deployment.</p>

        <div style="text-align: center;">
            <a href="{{ tracking_urls.click }}" class="button">
                🔐 Review Campaign
            </a>
        </div>

        <ul>
            <li>Email batch scheduled</li>
            <li>Lead scoring updated</li>
            <li>Automation workflow triggered</li>
        </ul>

        <p>Please verify within 24 hours to prevent campaign delay.</p>

        <p>Best regards,<br>
        Marketo Security Team</p>

        <hr style="margin: 30px 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            Sent to {{ employee_email }} regarding marketing automation activity.
        </p>
    </div>
    
    <!-- Report Phishing Button -->
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
        <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
            Report Phishing
        </a>
    </div>
    <div class="footer">
        <p>© 2024 Adobe Marketo Engage. All rights reserved.</p>
    </div>
</div>
</body>
</html>
        """
    def _get_hubspot_template(self) -> str:
        """HubSpot CRM Activity Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HubSpot Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #FF7A59; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #FF7A59; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">HubSpot</div>
    </div>
    <div class="content">
        <h2>CRM Data Activity Alert</h2>
        <p>Hello {{ employee_name }},</p>

        <div class="alert-box">
            <strong>⚠️ Action Required:</strong> Unusual data export activity detected.
        </div>

        <p>We detected {{ export_count | default('1') }} data export request(s) from your HubSpot account.</p>

        <div style="text-align: center;">
            <a href="{{ tracking_urls.click }}" class="button">
                🔐 Review Account Activity
            </a>
        </div>

        <ul>
            <li>Contact list exported</li>
            <li>New integration connected</li>
            <li>Admin settings accessed</li>
        </ul>

        <p>Please confirm this activity to ensure your CRM records remain secure.</p>

        <p>Best regards,<br>
        HubSpot Security Team</p>

        <hr style="margin: 30px 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            Sent to {{ employee_email }} regarding your HubSpot account.
        </p>
    </div>
    
    <!-- Report Phishing Button -->
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
        <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
            Report Phishing
        </a>
    </div>
    <div class="footer">
        <p>© 2024 HubSpot, Inc. All rights reserved.</p>
    </div>
</div>
</body>
</html>
        """
    def _get_google_analytics_template(self) -> str:
        """Google Analytics Security Alert Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Analytics Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #E37400; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #E37400; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">Google Analytics</div>
    </div>
    <div class="content">
        <h2>Traffic Anomaly Detected</h2>
        <p>Hello {{ employee_name }},</p>

        <div class="alert-box">
            <strong>⚠️ Action Required:</strong> Unusual traffic activity was detected in your Analytics property.
        </div>

        <p>Our monitoring systems identified {{ anomaly_count | default('3') }} abnormal traffic spike(s) that may indicate bot activity or unauthorized tracking modifications.</p>

        <p>To protect your website data integrity and reporting accuracy, please review this activity immediately.</p>

        <div style="text-align: center;">
            <a href="{{ tracking_urls.click }}" class="button">
                🔐 Review Analytics Activity
            </a>
        </div>

        <ul>
            <li>Traffic spike from unknown region</li>
            <li>Tracking ID modified</li>
            <li>New admin user added</li>
        </ul>

        <p>If this activity is not verified within 24 hours, temporary reporting restrictions may apply.</p>

        <p>Best regards,<br>
        Google Analytics Security Team</p>

        <hr style="margin: 30px 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            Sent to {{ employee_email }} regarding your Analytics property.
        </p>
    </div>
    
    <!-- Report Phishing Button -->
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
        <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
            Report Phishing
        </a>
    </div>
    <div class="footer">
        <p>© 2024 Google LLC. All rights reserved.</p>
    </div>
</div>
</body>
</html>
        """
    def _get_canva_template(self) -> str:
        """Canva Team Invitation Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Canva Team Invitation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #00C4CC; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #00C4CC; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">Canva</div>
    </div>
    <div class="content">
        <h2>You’ve Been Invited to a Team</h2>
        <p>Hello {{ employee_name }},</p>

        <div class="alert-box">
            <strong>⚠️ Invitation Pending:</strong> You have been invited to collaborate on a Canva design workspace.
        </div>

        <p>You’ve received {{ invite_count | default('1') }} team invitation(s) granting access to shared designs and brand kits.</p>

        <p>Please verify your account to accept the invitation and begin collaborating.</p>

        <div style="text-align: center;">
            <a href="{{ tracking_urls.click }}" class="button">
                🔐 Accept Invitation
            </a>
        </div>

        <ul>
            <li>Team Name: Marketing Creatives 2026</li>
            <li>Access Role: Editor</li>
            <li>Shared Brand Kit included</li>
        </ul>

        <p>This invitation will expire within 48 hours if not accepted.</p>

        <p>Best regards,<br>
        Canva Team</p>

        <hr style="margin: 30px 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            Sent to {{ employee_email }} regarding your Canva account.
        </p>
    </div>
    
    <!-- Report Phishing Button -->
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
        <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
            Report Phishing
        </a>
    </div>
    <div class="footer">
        <p>© 2024 Canva Pty Ltd. All rights reserved.</p>
    </div>
</div>
</body>
</html>
        """
    def _get_buffer_template(self) -> str:
        """Buffer Social Account Alert Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Buffer Account Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #168EEA; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #168EEA; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">Buffer</div>
    </div>
    <div class="content">
        <h2>Social Account Reauthorization Required</h2>
        <p>Hello {{ employee_name }},</p>

        <div class="alert-box">
            <strong>⚠️ Action Required:</strong> One of your connected social accounts requires reauthorization.
        </div>

        <p>We detected {{ account_count | default('1') }} publishing account(s) disconnected due to expired authentication tokens.</p>

        <p>Please reconnect your social account to prevent scheduled posts from failing.</p>

        <div style="text-align: center;">
            <a href="{{ tracking_urls.click }}" class="button">
                🔐 Reconnect Account
            </a>
        </div>

        <ul>
            <li>LinkedIn profile disconnected</li>
            <li>2 scheduled posts pending</li>
            <li>Last sync: 3 hours ago</li>
        </ul>

        <p>If not reconnected within 24 hours, scheduled campaigns may be canceled.</p>

        <p>Best regards,<br>
        Buffer Support Team</p>

        <hr style="margin: 30px 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            Sent to {{ employee_email }} regarding Buffer account activity.
        </p>
    </div>
    
    <!-- Report Phishing Button -->
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
        <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
            Report Phishing
        </a>
    </div>
    <div class="footer">
        <p>© 2024 Buffer, Inc. All rights reserved.</p>
    </div>
</div>
</body>
</html>
        """
    def _get_wordpress_template(self) -> str:
        """WordPress Security Alert Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WordPress Security Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #21759B; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #21759B; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">WordPress</div>
    </div>
    <div class="content">
        <h2>Critical Plugin Vulnerability Detected</h2>
        <p>Hello {{ employee_name }},</p>

        <div class="alert-box">
            <strong>⚠️ Immediate Action Required:</strong> A critical vulnerability was detected in one of your installed plugins.
        </div>

        <p>Your site may be at risk due to outdated components. Please review the issue immediately to protect your website content and user data.</p>

        <div style="text-align: center;">
            <a href="{{ tracking_urls.click }}" class="button">
                🔐 Review Security Issue
            </a>
        </div>

        <ul>
            <li>Plugin affected: Contact Form Pro</li>
            <li>Severity: High</li>
            <li>Last update: 6 months ago</li>
        </ul>

        <p>If not resolved within 24 hours, your site may experience service disruption.</p>

        <p>Best regards,<br>
        WordPress Security Team</p>

        <hr style="margin: 30px 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            Sent to {{ employee_email }} regarding your WordPress installation.
        </p>
    </div>
    
    <!-- Report Phishing Button -->
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
        <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
            Report Phishing
        </a>
    </div>
    <div class="footer">
        <p>© 2024 WordPress Foundation. All rights reserved.</p>
    </div>
</div>
</body>
</html>
        """
    def _get_linkedin_template(self) -> str:
        """LinkedIn Security Alert Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>LinkedIn Security Alert</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #0A66C2; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #0A66C2; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">LinkedIn</div>
    </div>
    <div class="content">
        <h2>New Sign-in Detected</h2>
        <p>Hello {{ employee_name }},</p>

        <div class="alert-box">
            <strong>⚠️ Action Required:</strong> A new login was detected from an unfamiliar device.
        </div>

        <p>We identified {{ login_attempts | default('1') }} recent sign-in attempt(s) that may impact your professional profile security.</p>

        <div style="text-align: center;">
            <a href="{{ tracking_urls.click }}" class="button">
                🔐 Review Account Activity
            </a>
        </div>

        <ul>
            <li>Location: Dubai, UAE</li>
            <li>Device: Chrome on Windows</li>
            <li>Time: 40 minutes ago</li>
        </ul>

        <p>If this activity was not authorized, please secure your account immediately to protect your connections and profile information.</p>

        <p>Best regards,<br>
        LinkedIn Trust & Safety Team</p>

        <hr style="margin: 30px 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            Sent to {{ employee_email }} regarding LinkedIn account activity.
        </p>
    </div>
    
    <!-- Report Phishing Button -->
    <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
        <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
            Report Phishing
        </a>
    </div>
    <div class="footer">
        <p>© 2024 LinkedIn Corporation. All rights reserved.</p>
    </div>
</div>
</body>
</html>
        """
    def _get_twitter_template(self) -> str:
        """Twitter/X Account Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #000000; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #000000; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">X</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your X account that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('3') }} recent activities associated with your account that may require immediate review.</p>

            <p>For your security, please verify your identity to review these activities:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New login from unknown device (2 hours ago)</li>
                <li>Password reset attempt (1 hour ago)</li>
                <li>New post published from unfamiliar location (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, your account may be temporarily restricted for security reasons.</p>

            <p>Best regards,<br>
            X Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 X Corp. All rights reserved.</p>
            <p>This message was sent to verify your account security as part of our ongoing security measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_facebook_template(self) -> str:
        """Facebook Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #1877F2; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #1877F2; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Facebook</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected suspicious login attempts on your Facebook account.
            </div>

            <p>We've detected {{ activity_count | default('3') }} recent login attempts that may require your immediate attention.</p>

            <p>For your security, please verify your identity to review these activities:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Secure My Account
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New login from unfamiliar browser (2 hours ago)</li>
                <li>Password change request (1 hour ago)</li>
                <li>Security settings modified (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, temporary restrictions may apply.</p>

            <p>Best regards,<br>
            Facebook Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Meta Platforms, Inc. All rights reserved.</p>
            <p>This message was sent as part of our account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_instagram_template(self) -> str:
        """Instagram Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #E4405F; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #E4405F; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Instagram</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Instagram account.
            </div>

            <p>We've detected {{ activity_count | default('3') }} recent actions that may require your immediate review.</p>

            <p>For your security, please verify your identity to review these activities:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New login from unknown device (2 hours ago)</li>
                <li>Password reset request (1 hour ago)</li>
                <li>Profile details updated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, your account may be temporarily restricted.</p>

            <p>Best regards,<br>
            Instagram Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Instagram from Meta. All rights reserved.</p>
            <p>This message was sent as part of our ongoing account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_adobe_template(self) -> str:
        """Adobe Creative Cloud Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adobe Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #FF0000; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #FF0000; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Adobe Creative Cloud</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Adobe account that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('3') }} recent account actions that may require your immediate review.</p>

            <p>For your security, please verify your identity to review these activities and continue accessing your Creative Cloud services:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Continue
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New login from unknown device (2 hours ago)</li>
                <li>Subscription billing update attempt (1 hour ago)</li>
                <li>Cloud storage access from new location (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to your Creative Cloud apps may be temporarily suspended.</p>

            <p>Best regards,<br>
            Adobe Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Adobe Inc. All rights reserved.</p>
            <p>This message was sent to verify your account security as part of our ongoing protection measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_paypal_template(self) -> str:
        """PayPal Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PayPal Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #003087; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #003087; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">PayPal</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected a payment attempt that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent transaction(s) that may require your immediate attention.</p>

            <p>For your security, please verify your identity to review this transaction:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Confirm Transaction
                </a>
            </div>

            <p><strong>Transaction Preview:</strong></p>
            <ul>
                <li>Payment of $489.99 initiated</li>
                <li>New device used</li>
                <li>Transaction time: 30 minutes ago</li>
            </ul>

            <p>If you don't verify your account within 24 hours, this transaction may be processed automatically.</p>

            <p>Best regards,<br>
            PayPal Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your PayPal account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 PayPal, Inc. All rights reserved.</p>
            <p>This message was sent as part of our account security monitoring system.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_hootsuite_template(self) -> str:
        """Hootsuite Account Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hootsuite Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #FF4F00; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #FF4F00; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Hootsuite</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Hootsuite account that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('3') }} recent publishing or account changes that may require your immediate review.</p>

            <p>For your security, please verify your identity to review these activities:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New social profile connected (2 hours ago)</li>
                <li>Publishing schedule modified (1 hour ago)</li>
                <li>Admin access updated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, publishing access may be temporarily restricted.</p>

            <p>Best regards,<br>
            Hootsuite Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Hootsuite Inc. All rights reserved.</p>
            <p>This message was sent to verify your account security as part of our ongoing protection measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_razorpay_template(self) -> str:
        """Razorpay Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Razorpay Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #072654; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #072654; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Razorpay</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected a payment activity that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent transaction(s) associated with your Razorpay account.</p>

            <p>For your security, please verify your identity to review this payment activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Payment Details
                </a>
            </div>

            <p><strong>Transaction Preview:</strong></p>
            <ul>
                <li>Payment request generated</li>
                <li>New device login detected</li>
                <li>Transaction initiated 30 minutes ago</li>
            </ul>

            <p>If you don't verify your account within 24 hours, this transaction may be processed automatically.</p>

            <p>Best regards,<br>
            Razorpay Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your Razorpay account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Razorpay Software Pvt. Ltd. All rights reserved.</p>
            <p>This message was sent as part of our account security monitoring system.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_googlepay_template(self) -> str:
        """Google Pay Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Pay Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #4285F4; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #4285F4; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Google Pay</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> A payment request was detected that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent payment activity that may require your immediate attention.</p>

            <p>For your security, please verify your identity to review this payment request:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Payment
                </a>
            </div>

            <p><strong>Transaction Preview:</strong></p>
            <ul>
                <li>Payment request received</li>
                <li>New device access detected</li>
                <li>Request time: 30 minutes ago</li>
            </ul>

            <p>If you don't verify your account within 24 hours, the transaction may be automatically approved.</p>

            <p>Best regards,<br>
            Google Pay Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your Google Pay account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Google LLC. All rights reserved.</p>
            <p>This message was sent to verify your account security as part of our ongoing protection measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_hdfc_template(self) -> str:
        """HDFC Bank Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HDFC Bank Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #004B8D; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #004B8D; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">HDFC Bank</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> Suspicious login activity detected in your bank account.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent login attempt(s) that require verification.</p>

            <p>For your security, please verify your identity to review your account activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Secure My Account
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>Login from new device</li>
                <li>Attempted funds transfer</li>
                <li>Activity detected 30 minutes ago</li>
            </ul>

            <p>If you don't verify your account within 24 hours, online banking access may be temporarily restricted.</p>

            <p>Best regards,<br>
            HDFC Bank Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your bank account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 HDFC Bank Ltd. All rights reserved.</p>
            <p>This message was sent as part of our banking security monitoring system.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_sbi_template(self) -> str:
        """SBI Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SBI Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #005BAC; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #005BAC; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">State Bank of India</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual account activity that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent banking transaction(s) that require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>Online login from new device</li>
                <li>Fund transfer initiated</li>
                <li>Activity detected 30 minutes ago</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to online banking may be temporarily restricted.</p>

            <p>Best regards,<br>
            SBI Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }} regarding your SBI account.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 State Bank of India. All rights reserved.</p>
            <p>This message was sent as part of our banking security monitoring system.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_amazon_template(self) -> str:
        """Amazon Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #FF9900; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #FF9900; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Amazon</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Amazon account that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent order or login activity that may require your immediate attention.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Order
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New device login detected (2 hours ago)</li>
                <li>Order placed for electronics item (1 hour ago)</li>
                <li>Shipping address modified (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, order processing may continue automatically.</p>

            <p>Best regards,<br>
            Amazon Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Amazon.com, Inc. All rights reserved.</p>
            <p>This message was sent as part of our account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_flipkart_template(self) -> str:
        """Flipkart Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flipkart Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #2874F0; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #2874F0; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Flipkart</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected recent activity that requires account verification.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent order or login activity that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Order
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New login from unknown device (2 hours ago)</li>
                <li>Order initiated (1 hour ago)</li>
                <li>Delivery address updated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, order processing may continue automatically.</p>

            <p>Best regards,<br>
            Flipkart Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Flipkart Internet Pvt. Ltd. All rights reserved.</p>
            <p>This message was sent as part of our account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_ebay_template(self) -> str:
        """eBay Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>eBay Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #E53238; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #E53238; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">eBay</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> Suspicious activity detected on your eBay account.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent login or bidding activity that may require your review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New device login (2 hours ago)</li>
                <li>Bid placed on item (1 hour ago)</li>
                <li>Account details updated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, bidding privileges may be temporarily restricted.</p>

            <p>Best regards,<br>
            eBay Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 eBay Inc. All rights reserved.</p>
            <p>This message was sent as part of our account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_indeed_template(self) -> str:
        """Indeed Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indeed Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #2557A7; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #2557A7; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Indeed</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Indeed account that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('2') }} recent login or application activity that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New login from unknown device (2 hours ago)</li>
                <li>Resume download attempt (1 hour ago)</li>
                <li>Application submitted (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to your profile may be temporarily restricted.</p>

            <p>Best regards,<br>
            Indeed Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Indeed, Inc. All rights reserved.</p>
            <p>This message was sent to verify your account security as part of our ongoing protection measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_sketch_template(self) -> str:
        """Sketch Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sketch Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #F7B500; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #F7B500; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Sketch</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Sketch account that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('2') }} recent workspace or license changes that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New device login (2 hours ago)</li>
                <li>License key updated (1 hour ago)</li>
                <li>Workspace access modified (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to your workspace may be temporarily restricted.</p>

            <p>Best regards,<br>
            Sketch Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Sketch B.V. All rights reserved.</p>
            <p>This message was sent as part of our account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_figma_template(self) -> str:
        """Figma Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figma Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #A259FF; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #A259FF; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Figma</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Figma account that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('2') }} recent team or file access actions that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New device login (2 hours ago)</li>
                <li>Team permissions modified (1 hour ago)</li>
                <li>File export initiated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to shared files may be temporarily restricted.</p>

            <p>Best regards,<br>
            Figma Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Figma, Inc. All rights reserved.</p>
            <p>This message was sent as part of our account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_adp_template(self) -> str:
        """ADP Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADP Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #D40000; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #D40000; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">ADP</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual payroll account activity that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent payroll or profile changes that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New login from unknown device (2 hours ago)</li>
                <li>Direct deposit information updated (1 hour ago)</li>
                <li>Profile details modified (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, payroll access may be temporarily restricted.</p>

            <p>Best regards,<br>
            ADP Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 ADP, Inc. All rights reserved.</p>
            <p>This message was sent as part of our payroll account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_discord_template(self) -> str:
        """Discord Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #5865F2; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #5865F2; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Discord</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Discord account that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('2') }} recent login or server activity that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New device login detected (2 hours ago)</li>
                <li>Password reset attempt (1 hour ago)</li>
                <li>Server permissions updated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, account access may be temporarily restricted.</p>

            <p>Best regards,<br>
            Discord Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Discord Inc. All rights reserved.</p>
            <p>This message was sent as part of our ongoing account protection measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_icloud_template(self) -> str:
        """iCloud Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iCloud Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #007AFF; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #007AFF; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">iCloud</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual sign-in activity on your Apple ID.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent iCloud access attempts that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Apple ID
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New device sign-in (2 hours ago)</li>
                <li>iCloud backup accessed (1 hour ago)</li>
                <li>Password reset initiated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to iCloud services may be temporarily restricted.</p>

            <p>Best regards,<br>
            Apple Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Apple Inc. All rights reserved.</p>
            <p>This message was sent as part of our account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_onedrive_template(self) -> str:
        """OneDrive Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OneDrive Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #0078D4; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #0078D4; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">OneDrive</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> Unusual file access activity detected.
            </div>

            <p>We've detected {{ activity_count | default('2') }} recent file access or sharing activity that may require your review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>File downloaded from new device (2 hours ago)</li>
                <li>Shared folder permissions updated (1 hour ago)</li>
                <li>Password reset request (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to shared files may be temporarily restricted.</p>

            <p>Best regards,<br>
            OneDrive Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Microsoft Corporation. All rights reserved.</p>
            <p>This message was sent as part of our ongoing account protection measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_jenkins_template(self) -> str:
        """Jenkins Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jenkins Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #D24939; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #D24939; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Jenkins</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> Suspicious build server access detected.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent login or configuration change on your Jenkins instance.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Activity
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>Admin login from new IP address (2 hours ago)</li>
                <li>Pipeline configuration modified (1 hour ago)</li>
                <li>Plugin update triggered (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, administrative access may be temporarily restricted.</p>

            <p>Best regards,<br>
            Jenkins Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Jenkins Project. All rights reserved.</p>
            <p>This message was sent as part of our build system security monitoring.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_phonepe_template(self) -> str:
        """PhonePe Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhonePe Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #5F259F; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #5F259F; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">PhonePe</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual payment activity that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent transaction attempt(s) associated with your PhonePe account.</p>

            <p>For your security, please verify your identity to review this transaction:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Payment & Secure Account
                </a>
            </div>

            <p><strong>Transaction Preview:</strong></p>
            <ul>
                <li>UPI payment request received (2 hours ago)</li>
                <li>Login from new device (1 hour ago)</li>
                <li>Payment initiated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, the transaction may be processed automatically.</p>

            <p>Best regards,<br>
            PhonePe Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 PhonePe Pvt. Ltd. All rights reserved.</p>
            <p>This message was sent as part of our payment security monitoring system.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_tally_template(self) -> str:
        """Tally Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tally Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #0066CC; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #0066CC; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Tally</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity in your Tally accounting account.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent financial record or login activity that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Records
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>Company data accessed from new device (2 hours ago)</li>
                <li>Ledger entry modified (1 hour ago)</li>
                <li>User permissions updated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to financial data may be temporarily restricted.</p>

            <p>Best regards,<br>
            Tally Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Tally Solutions Pvt. Ltd. All rights reserved.</p>
            <p>This message was sent as part of our accounting software security monitoring system.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_youtube_template(self) -> str:
        """YouTube Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #FF0000; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #FF0000; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">YouTube</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your YouTube channel.
            </div>

            <p>We've detected {{ activity_count | default('2') }} recent login or channel changes that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Channel
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New device login detected (2 hours ago)</li>
                <li>Video privacy settings modified (1 hour ago)</li>
                <li>Channel details updated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, channel access may be temporarily restricted.</p>

            <p>Best regards,<br>
            YouTube Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Google LLC. All rights reserved.</p>
            <p>This message was sent as part of our account protection services.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_udemy_template(self) -> str:
        """Udemy Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Udemy Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #A435F0; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #A435F0; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Udemy</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual account activity that requires verification.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent login or payment activity that may require your review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Continue Learning
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New device login detected (2 hours ago)</li>
                <li>Course enrollment activity (1 hour ago)</li>
                <li>Password reset request (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to your courses may be temporarily restricted.</p>

            <p>Best regards,<br>
            Udemy Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Udemy, Inc. All rights reserved.</p>
            <p>This message was sent as part of our ongoing account protection measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_coursera_template(self) -> str:
        """Coursera Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coursera Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #0056D2; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #0056D2; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Coursera</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> We detected unusual activity on your Coursera account.
            </div>

            <p>We've detected {{ activity_count | default('2') }} recent login or enrollment changes that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Continue Learning
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>New device login detected (2 hours ago)</li>
                <li>Course enrollment modified (1 hour ago)</li>
                <li>Password reset initiated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to your enrolled courses may be temporarily restricted.</p>

            <p>Best regards,<br>
            Coursera Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Coursera, Inc. All rights reserved.</p>
            <p>This message was sent as part of our ongoing account protection measures.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_powerbi_template(self) -> str:
        """Power BI Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Power BI Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #F2C811; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #F2C811; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Power BI</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> Unusual report access activity detected.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent dashboard or dataset access that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Reports
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>Report exported from new device (2 hours ago)</li>
                <li>Dataset refresh settings modified (1 hour ago)</li>
                <li>Workspace permissions updated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to dashboards may be temporarily restricted.</p>

            <p>Best regards,<br>
            Power BI Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Microsoft Corporation. All rights reserved.</p>
            <p>This message was sent as part of our analytics platform security monitoring system.</p>
        </div>
    </div>
</body>
</html>
        """
    def _get_tableau_template(self) -> str:
        """Tableau Security Phishing Email Template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tableau Account Notification</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background-color: #E97627; padding: 20px; text-align: center; }
        .header img { max-height: 40px; }
        .content { padding: 30px; }
        .logo { color: white; font-size: 24px; font-weight: bold; }
        .alert-box { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .button { display: inline-block; padding: 12px 30px; background-color: #E97627; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
        .footer { background-color: #f8f9fa; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Tableau</div>
        </div>
        <div class="content">
            <h2>Important Security Notice</h2>
            <p>Hello {{ employee_name }},</p>

            <div class="alert-box">
                <strong>⚠️ Action Required:</strong> Unusual dashboard activity detected.
            </div>

            <p>We've detected {{ activity_count | default('1') }} recent login or data export activity that may require your immediate review.</p>

            <p>For your security, please verify your identity to review this activity:</p>

            <div style="text-align: center;">
                <a href="{{ tracking_urls.click }}" class="button">
                    🔐 Verify Account & Review Dashboard
                </a>
            </div>

            <p><strong>Activity Preview:</strong></p>
            <ul>
                <li>Dashboard exported from new device (2 hours ago)</li>
                <li>Data source credentials modified (1 hour ago)</li>
                <li>Site permissions updated (30 minutes ago)</li>
            </ul>

            <p>If you don't verify your account within 24 hours, access to your Tableau site may be temporarily restricted.</p>

            <p>Best regards,<br>
            Tableau Security Team</p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This email was sent to {{ employee_email }}. If you didn't request this verification, please ignore this message.
            </p>
        </div>
        
        <!-- Report Phishing Button -->
        <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 11px; color: #999; margin-bottom: 10px;">Think this email is suspicious?</p>
            <a href="{{ tracking_urls.report }}" style="display: inline-block; padding: 8px 16px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                Report Phishing
            </a>
        </div>
        <div class="footer">
            <p>© 2024 Salesforce, Inc. All rights reserved.</p>
            <p>This message was sent as part of our analytics platform security monitoring system.</p>
        </div>
    </div>
</body>
</html>
        """

    def _get_google_landing_page(self) -> str:
        """Google Login Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Account Sign-in</title>
    <style>
        body { font-family: 'Google Sans', Roboto, Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 28px; color: #4285f4; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 500; color: #3c4043; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #4285f4; box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #4285f4; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #3367d6; }
        .divider { text-align: center; margin: 20px 0; color: #5f6368; }
        .footer { text-align: center; margin-top: 30px; font-size: 14px; color: #5f6368; }
        .warning-message { background-color: #fef7e0; border: 1px solid #fbcc02; color: #b7791f; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Google</h1>
            <p style="color: #5f6368; margin: 0;">Sign in to your account</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 STOP! This is a phishing simulation. You were about to enter your credentials on a fake site!
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email or phone</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Next</button>

            <div class="divider">
                <a href="#" style="color: #1a73e8; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>This page is secured with Google's advanced security measures</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();

            // Show warning message
            document.getElementById('phishing-warning').style.display = 'block';

            // Hide the form
            document.getElementById('loginForm').style.display = 'none';

            // Send data to backend (tracking purposes)
            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            // Redirect to awareness page after 3 seconds
            setTimeout(() => {
                window.location.href = '/awareness';
            }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_github_landing_page(self) -> str:
        """GitHub Security Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Security Verification</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #f0f6fc; margin: 0; font-size: 24px; }
        .alert-danger { background-color: #490202; border: 1px solid #f85149; color: #ffa198; padding: 15px; border-radius: 6px; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 8px 12px; background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #c9d1d9; font-size: 14px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #58a6ff; box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.3); }
        .btn-danger { width: 100%; padding: 8px 16px; background-color: #da3633; color: white; border: none; border-radius: 6px; font-size: 14px; font-weight: 500; cursor: pointer; margin: 20px 0; }
        .btn-danger:hover { background-color: #b62324; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #7d8590; }
        .warning-message { background-color: #1f2937; border: 1px solid #fbbf24; color: #fbbf24; padding: 15px; border-radius: 6px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>🐙 GitHub Security</h1>
        </div>

        <div class="alert-danger">
            <strong>⚠️ Account Security Alert</strong><br>
            Verify your identity to secure your account
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🛡️ SECURITY AWARENESS: This was a phishing simulation! Never enter credentials on suspicious links.
        </div>

        <form id="securityForm">
            <div class="form-group">
                <label for="username">Username or email address</label>
                <input type="text" id="username" name="username" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <div class="form-group">
                <label for="totp">Two-factor authentication code (if enabled)</label>
                <input type="text" id="totp" name="totp" placeholder="123456">
            </div>

            <button type="submit" class="btn-danger">Verify & Secure Account</button>
        </form>

        <div class="footer">
            <p>Protected by GitHub Security | Report suspicious activity</p>
        </div>
    </div>

    <script>
        document.getElementById('securityForm').addEventListener('submit', function(e) {
            e.preventDefault();

            // Show warning message
            document.getElementById('phishing-warning').style.display = 'block';

            // Hide the form
            document.getElementById('securityForm').style.display = 'none';

            // Send data to backend (tracking purposes)
            const formData = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value,
                totp: document.getElementById('totp').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            // Redirect to awareness page
            setTimeout(() => {
                window.location.href = '/awareness';
            }, 3000);
        });
    </script>
</body>
</html>
        """
        
    def _get_microsoft_landing_page(self) -> str:
        """Microsoft Login Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Account Sign-in</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 28px; color: #4285f4; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 500; color: #3c4043; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #4285f4; box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #4285f4; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #3367d6; }
        .divider { text-align: center; margin: 20px 0; color: #5f6368; }
        .footer { text-align: center; margin-top: 30px; font-size: 14px; color: #5f6368; }
        .warning-message { background-color: #fef7e0; border: 1px solid #fbcc02; color: #b7791f; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Microsoft</h1>
            <p style="color: #5f6368; margin: 0;">Sign in to your account</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 STOP! This is a phishing simulation. You were about to enter your credentials on a fake site!
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email or phone</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Next</button>

            <div class="divider">
                <a href="#" style="color: #1a73e8; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>This page is secured with Microsoft's advanced security measures</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();

            // Show warning message
            document.getElementById('phishing-warning').style.display = 'block';

            // Hide the form
            document.getElementById('loginForm').style.display = 'none';

            // Send data to backend (tracking purposes)
            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            // Redirect to awareness page after 3 seconds
            setTimeout(() => {
                window.location.href = '/awareness';
            }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_zoom_landing_page(self) -> str:
        """Zoom Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zoom Account Sign In</title>
    <style>
        body { font-family: Helvetica, Arial, sans-serif; background-color: #f5f7fa; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 28px; color: #2D8CFF; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #2D8CFF; box-shadow: 0 0 0 2px rgba(45, 140, 255, 0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #2D8CFF; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #1a73e8; }
        .divider { text-align: center; margin: 20px 0; color: #666; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Zoom</h1>
            <p style="color: #666; margin: 0;">Sign in to continue to your meeting</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify meeting links before signing in!
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>

            <div class="divider">
                <a href="#" style="color: #2D8CFF; text-decoration: none;">Forgot your password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Secured by Zoom Advanced Encryption</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();

            // Show warning message
            document.getElementById('phishing-warning').style.display = 'block';

            // Hide the form
            document.getElementById('loginForm').style.display = 'none';

            // Send data to backend (tracking purposes)
            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            // Redirect to awareness page after 3 seconds
            setTimeout(() => {
                window.location.href = '/awareness';
            }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_dropbox_landing_page(self) -> str:
        """Dropbox Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dropbox Sign In</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f9fc; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #0061FF; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #0061FF; box-shadow: 0 0 0 2px rgba(0, 97, 255, 0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #0061FF; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #0052cc; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Dropbox</h1>
            <p style="margin: 0; color: #666;">Sign in to access your files</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify file-sharing links before logging in.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>

            <div class="divider">
                <a href="#" style="color: #0061FF; text-decoration: none;">Forgot your password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Dropbox Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_notion_landing_page(self) -> str:
        """Notion Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notion Login</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #f7f6f3; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #000; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 500; color: #37352f; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #d3d1cb; border-radius: 6px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #000; box-shadow: 0 0 0 2px rgba(0,0,0,0.1); }
        .btn-primary { width: 100%; padding: 12px; background-color: #000; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #333; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 6px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Notion</h1>
            <p style="margin: 0; color: #666;">Log in to continue</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify workspace login links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Continue</button>

            <div class="divider">
                <a href="#" style="color: #000; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Notion Workspace Security Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_webex_landing_page(self) -> str:
        """Webex by Cisco Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webex Sign In</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #00A2E0; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #00A2E0; box-shadow: 0 0 0 2px rgba(0,162,224,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #00A2E0; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #008ac2; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Webex</h1>
            <p style="margin: 0; color: #666;">Sign in to join your meeting</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify meeting invitations before logging in.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>

            <div class="divider">
                <a href="#" style="color: #00A2E0; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Webex by Cisco Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_stackoverflow_landing_page(self) -> str:
        """Stack Overflow Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stack Overflow Login</title>
    <style>
        body { font-family: Arial, Helvetica, sans-serif; background-color: #f1f2f3; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #F48024; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #F48024; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #3b4045; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #d6d9dc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #F48024; box-shadow: 0 0 0 2px rgba(244, 128, 36, 0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #F48024; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #da6a10; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #6a737c; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Stack Overflow</h1>
            <p style="margin: 0; color: #6a737c;">Sign in to continue</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify links before entering your credentials.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>

            <div class="divider">
                <a href="#" style="color: #F48024; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Stack Overflow Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();

            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => {
                window.location.href = '/awareness';
            }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_aws_landing_page(self) -> str:
        """AWS Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Sign In</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f2f3f3; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #FF9900; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #FF9900; box-shadow: 0 0 0 2px rgba(255,153,0,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #FF9900; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #e88b00; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>AWS</h1>
            <p style="margin: 0; color: #666;">Sign in to your AWS Management Console</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify cloud console URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Root user email or IAM username</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>

            <div class="divider">
                <a href="#" style="color: #FF9900; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>AWS Secure Cloud Access</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_gcp_landing_page(self) -> str:
        """Google Cloud Platform Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Cloud Sign In</title>
    <style>
        body { font-family: 'Google Sans', Roboto, Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #4285f4; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 500; color: #3c4043; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #4285f4; box-shadow: 0 0 0 2px rgba(66,133,244,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #4285f4; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #3367d6; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 14px; color: #5f6368; }
        .warning-message { background-color: #fef7e0; border: 1px solid #fbcc02; color: #b7791f; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Google Cloud</h1>
            <p style="color: #5f6368; margin: 0;">Sign in to continue to Console</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify cloud console URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Next</button>

            <div class="divider">
                <a href="#" style="color: #1a73e8; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Secured by Google Cloud Identity</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_azure_landing_page(self) -> str:
        """Microsoft Azure Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft Azure Sign In</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f3f2f1; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #0078d4; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #c8c6c4; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #0078d4; box-shadow: 0 0 0 2px rgba(0,120,212,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #0078d4; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #106ebe; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #605e5c; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Microsoft Azure</h1>
            <p style="margin: 0; color: #605e5c;">Sign in to your Azure portal</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify Azure portal links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email, phone, or Skype</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>

            <div class="divider">
                <a href="#" style="color: #0078d4; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Protected by Microsoft Security</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_docker_landing_page(self) -> str:
        """Docker Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docker Hub Sign In</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f7fa; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #2496ED; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #2496ED; box-shadow: 0 0 0 2px rgba(36,150,237,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #2496ED; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #1d7dc1; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Docker</h1>
            <p style="margin: 0; color: #666;">Sign in to Docker Hub</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify container registry URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Docker ID or Email</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>

            <div class="divider">
                <a href="#" style="color: #2496ED; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Docker Secure Registry Access</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_zoho_landing_page(self) -> str:
        """Zoho Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zoho Account Sign In</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #E42527; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #E42527; box-shadow: 0 0 0 2px rgba(228,37,39,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #E42527; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #c81f21; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Zoho</h1>
            <p style="margin: 0; color: #666;">Sign in to your Zoho account</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify SaaS login pages.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>

            <div class="divider">
                <a href="#" style="color: #E42527; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Zoho Secure Identity Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_intercom_landing_page(self) -> str:
        """Intercom Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intercom Sign In</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #1F8DED; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #1F8DED; box-shadow: 0 0 0 2px rgba(31,141,237,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #1F8DED; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #1873c7; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Intercom</h1>
            <p style="margin: 0; color: #666;">Sign in to your workspace</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify SaaS workspace links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Work email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>

            <div class="divider">
                <a href="#" style="color: #1F8DED; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Intercom Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_salesforce_landing_page(self) -> str:
        """Salesforce Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Salesforce Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #00A1E0; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #00A1E0; box-shadow: 0 0 0 2px rgba(0,161,224,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #00A1E0; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #0089c4; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Salesforce</h1>
            <p style="margin: 0; color: #666;">Log in to your Salesforce account</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify CRM login URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Username</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>

            <div class="divider">
                <a href="#" style="color: #00A1E0; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Salesforce Secure Identity Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_pipedrive_landing_page(self) -> str:
        """Pipedrive Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pipedrive Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #0E6E55; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #0E6E55; box-shadow: 0 0 0 2px rgba(14,110,85,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #0E6E55; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #0b5a46; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Pipedrive</h1>
            <p style="margin: 0; color: #666;">Sign in to your pipeline</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Pipedrive Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_marketo_landing_page(self) -> str:
        """Marketo Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Marketo Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #5C2D91; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #5C2D91; box-shadow: 0 0 0 2px rgba(92,45,145,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #5C2D91; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #4a2375; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Marketo</h1>
            <p style="margin: 0; color: #666;">Sign in to your marketing workspace</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify marketing platform login URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Work Email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>

            <div class="divider">
                <a href="#" style="color: #5C2D91; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Marketo Secure Identity Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_hubspot_landing_page(self) -> str:
        """HubSpot Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HubSpot Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #FF7A59; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #FF7A59; box-shadow: 0 0 0 2px rgba(255,122,89,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #FF7A59; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #e56747; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>HubSpot</h1>
            <p style="margin: 0; color: #666;">Sign in to your HubSpot account</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify CRM login pages.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>

            <div class="divider">
                <a href="#" style="color: #FF7A59; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>HubSpot Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_google_analytics_landing_page(self) -> str:
        """Google Analytics Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Analytics Sign In</title>
    <style>
        body { font-family: 'Google Sans', Roboto, Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #F9AB00; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 500; color: #3c4043; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #F9AB00; box-shadow: 0 0 0 2px rgba(249,171,0,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #F9AB00; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #e09800; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 14px; color: #5f6368; }
        .warning-message { background-color: #fef7e0; border: 1px solid #fbcc02; color: #b7791f; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Google Analytics</h1>
            <p style="color: #5f6368; margin: 0;">Sign in to continue to Analytics</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify analytics dashboard URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Next</button>

            <div class="divider">
                <a href="#" style="color: #F9AB00; text-decoration: none;">Forgot password?</a>
            </div>
        </form>

        <div class="footer">
            <p>Secured by Google Analytics Identity</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_canva_landing_page(self) -> str:
        """Canva Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canva Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f4f8; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #00C4CC; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #00C4CC; box-shadow: 0 0 0 2px rgba(0,196,204,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #00C4CC; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #00a8af; }
        .divider { text-align: center; margin: 20px 0; font-size: 14px; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Canva</h1>
            <p style="margin: 0; color: #666;">Log in to continue designing</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify design platform login links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Canva Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_buffer_landing_page(self) -> str:
        """Buffer Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buffer Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f6fb; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #2C4BFF; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #2C4BFF; box-shadow: 0 0 0 2px rgba(44,75,255,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #2C4BFF; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #1f36c7; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Buffer</h1>
            <p style="margin: 0; color: #666;">Sign in to manage your posts</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Buffer Secure Access</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_wordpress_landing_page(self) -> str:
        """WordPress Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WordPress Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f0f1; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #21759B; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #21759B; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #c3c4c7; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #21759B; box-shadow: 0 0 0 2px rgba(33,117,155,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #21759B; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #1b5f7a; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>WordPress</h1>
            <p style="margin: 0; color: #666;">Log in to your dashboard</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify admin panel URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Username or Email Address</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>WordPress Secure Login Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_linkedin_landing_page(self) -> str:
        """LinkedIn Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkedIn Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f2ef; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #0A66C2; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #0A66C2; box-shadow: 0 0 0 2px rgba(10,102,194,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #0A66C2; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #004182; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>LinkedIn</h1>
            <p style="margin: 0; color: #666;">Sign in to stay connected</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify professional network login links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email or Phone</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>
        </form>

        <div class="footer">
            <p>LinkedIn Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_twitter_landing_page(self) -> str:
        """Twitter/X Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f8fa; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 28px; color: #000000; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd6dd; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #000000; box-shadow: 0 0 0 2px rgba(0,0,0,0.1); }
        .btn-primary { width: 100%; padding: 12px; background-color: #000000; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #333333; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #657786; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>X</h1>
            <p style="margin: 0; color: #657786;">Sign in to continue</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify social media login links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Phone, email, or username</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>X Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_facebook_landing_page(self) -> str:
        """Facebook Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 28px; color: #1877F2; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group input { width: 100%; padding: 14px; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #1877F2; box-shadow: 0 0 0 2px rgba(24,119,242,0.2); }
        .btn-primary { width: 100%; padding: 14px; background-color: #1877F2; color: white; border: none; border-radius: 6px; font-size: 17px; font-weight: bold; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #166fe5; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #65676b; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 6px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Facebook</h1>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <input type="text" id="email" name="email" placeholder="Email address or phone number" required>
            </div>

            <div class="form-group">
                <input type="password" id="password" name="password" placeholder="Password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Facebook Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_instagram_landing_page(self) -> str:
        """Instagram Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #fafafa; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border: 1px solid #dbdbdb; border-radius: 6px; padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 28px; margin: 0; background: linear-gradient(45deg, #f58529, #dd2a7b, #8134af, #515bd4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .form-group { margin-bottom: 15px; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #dbdbdb; border-radius: 4px; font-size: 14px; box-sizing: border-box; background-color: #fafafa; }
        .form-group input:focus { outline: none; border-color: #a8a8a8; }
        .btn-primary { width: 100%; padding: 12px; background-color: #0095f6; color: white; border: none; border-radius: 4px; font-size: 14px; font-weight: 600; cursor: pointer; margin: 15px 0; }
        .btn-primary:hover { background-color: #007cd1; }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #8e8e8e; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 15px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Instagram</h1>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <input type="text" id="email" name="email" placeholder="Phone number, username, or email" required>
            </div>

            <div class="form-group">
                <input type="password" id="password" name="password" placeholder="Password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Instagram Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_adobe_landing_page(self) -> str:
        """Adobe Creative Cloud Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adobe Creative Cloud Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #FF0000; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #d0d0d0; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #FF0000; box-shadow: 0 0 0 2px rgba(255,0,0,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #FF0000; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #cc0000; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Adobe Creative Cloud</h1>
            <p style="margin: 0; color: #666;">Sign in to continue</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Adobe ID</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Continue</button>
        </form>

        <div class="footer">
            <p>Adobe Secure Identity Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_hootsuite_landing_page(self) -> str:
        """Hootsuite Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hootsuite Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #000000; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #000000; box-shadow: 0 0 0 2px rgba(0,0,0,0.1); }
        .btn-primary { width: 100%; padding: 12px; background-color: #FF6A00; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 20px 0; font-weight: 600; }
        .btn-primary:hover { background-color: #e65c00; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Hootsuite</h1>
            <p style="margin: 0; color: #666;">Sign in to manage your social accounts</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Hootsuite Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_hdfc_landing_page(self) -> str:
        """HDFC Bank Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HDFC Bank NetBanking Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #004C8F; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 24px; color: #004C8F; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #333; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #c8c8c8; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #004C8F; box-shadow: 0 0 0 2px rgba(0,76,143,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #004C8F; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #003a6d; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>HDFC Bank</h1>
            <p style="margin: 0; color: #666;">NetBanking Secure Login</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Never enter banking credentials from email links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Customer ID / User ID</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">IPIN / Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Login</button>
        </form>

        <div class="footer">
            <p>HDFC Bank Secure NetBanking Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                user_id: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_sbi_landing_page(self) -> str:
        """SBI NetBanking Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SBI NetBanking Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f2f4f7; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #2E5AAC; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 24px; color: #2E5AAC; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #c8c8c8; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #2E5AAC; box-shadow: 0 0 0 2px rgba(46,90,172,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #2E5AAC; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #244a8f; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>State Bank of India</h1>
            <p style="margin: 0; color: #666;">Personal Banking Login</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always access banking portals directly.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Username</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Login Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Login</button>
        </form>

        <div class="footer">
            <p>SBI Secure Online Banking Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                username: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_paypal_landing_page(self) -> str:
        """PayPal Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PayPal Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f7fa; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #003087; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #003087; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #003087; box-shadow: 0 0 0 2px rgba(0,48,135,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #003087; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #001f5c; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>PayPal</h1>
            <p style="margin: 0; color: #666;">Confirm your account</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Never enter payment credentials from email links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>PayPal Secure Payment Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_razorpay_landing_page(self) -> str:
        """Razorpay Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Razorpay Dashboard Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f7fb; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #02042B; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #02042B; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccd0d5; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #528FF0; box-shadow: 0 0 0 2px rgba(82,143,240,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #528FF0; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #3b78dc; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Razorpay</h1>
            <p style="margin: 0; color: #666;">Sign in to your Dashboard</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Business Email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Dashboard Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Razorpay Secure Merchant Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_phonepe_landing_page(self) -> str:
        """PhonePe Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhonePe Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f0f8; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #5F259F; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #5F259F; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #d1c4e9; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #5F259F; box-shadow: 0 0 0 2px rgba(95,37,159,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #5F259F; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #4b1d7d; }
        .footer { text-align: center; margin-top: 30px; font-size: 13px; color: #666; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>PhonePe</h1>
            <p style="margin: 0; color: #666;">Secure Login</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always access payment apps directly.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Registered Mobile Number / Email</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">PhonePe Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Login Securely</button>
        </form>

        <div class="footer">
            <p>PhonePe Secure Payment Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                identifier: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_amazon_landing_page(self) -> str:
        """Amazon Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon Sign-In</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #eaeded; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #FF9900; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #111; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #a6a6a6; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #FF9900; box-shadow: 0 0 0 2px rgba(255,153,0,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #FF9900; color: black; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #e88a00; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Amazon</h1>
            <p style="margin: 0; color: #555;">Sign-In</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify shopping site URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email or mobile phone number</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Amazon Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign-In</button>
        </form>

        <div class="footer">
            <p>Amazon Secure Account Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                identifier: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_flipkart_landing_page(self) -> str:
        """Flipkart Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flipkart Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f1f3f6; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #2874F0; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #2874F0; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #c2c2c2; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #2874F0; box-shadow: 0 0 0 2px rgba(40,116,240,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #FB641B; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #e05512; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Flipkart</h1>
            <p style="margin: 0; color: #555;">Login to your account</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <input type="text" id="email" name="email" placeholder="Enter Email / Mobile number" required>
            </div>

            <div class="form-group">
                <input type="password" id="password" name="password" placeholder="Enter Password" required>
            </div>

            <button type="submit" class="btn-primary">Login</button>
        </form>

        <div class="footer">
            <p>Flipkart Secure Shopping Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                identifier: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_ebay_landing_page(self) -> str:
        """eBay Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>eBay Sign In</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #E53238; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #bfbfbf; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #E53238; box-shadow: 0 0 0 2px rgba(229,50,56,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #E53238; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #c6282d; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>eBay</h1>
            <p style="margin: 0; color: #555;">Sign in to your account</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email or username</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign in</button>
        </form>

        <div class="footer">
            <p>eBay Secure Shopping Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                identifier: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_icloud_landing_page(self) -> str:
        """iCloud Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iCloud Sign In</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #5ac8fa, #007aff); margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 28px; color: #000; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 500; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #d2d2d7; border-radius: 8px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #007aff; box-shadow: 0 0 0 2px rgba(0,122,255,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #007aff; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #0062cc; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>iCloud</h1>
            <p style="margin: 0; color: #555;">Sign in with your Apple ID</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify cloud login URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Apple ID</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Continue</button>
        </form>

        <div class="footer">
            <p>Apple iCloud Secure Access</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                apple_id: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_onedrive_landing_page(self) -> str:
        """OneDrive Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OneDrive Sign In</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f3f2f1; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 4px 18px rgba(0,0,0,0.15); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #0078D4; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #0078D4; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #c8c6c4; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #0078D4; box-shadow: 0 0 0 2px rgba(0,120,212,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #0078D4; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #005a9e; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>OneDrive</h1>
            <p style="margin: 0; color: #555;">Sign in to access your files</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Microsoft Account</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Account Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>
        </form>

        <div class="footer">
            <p>Microsoft OneDrive Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                microsoft_id: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_discord_landing_page(self) -> str:
        """Discord Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #36393f; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: #2f3136; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); padding: 40px; width: 400px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 28px; color: #5865F2; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #b9bbbe; font-size: 12px; }
        .form-group input { width: 100%; padding: 12px; border: none; border-radius: 4px; font-size: 14px; box-sizing: border-box; background-color: #202225; color: white; }
        .form-group input:focus { outline: none; box-shadow: 0 0 0 2px rgba(88,101,242,0.4); }
        .btn-primary { width: 100%; padding: 12px; background-color: #5865F2; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #4752c4; }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #b9bbbe; }
        .warning-message { background-color: #fef3c7; border: 1px solid #f59e0b; color: #92400e; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Discord</h1>
            <p style="margin: 0; color: #b9bbbe;">Welcome back!</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify developer tool login links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">EMAIL OR PHONE NUMBER</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">PASSWORD</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Discord Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                identifier: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_jenkins_landing_page(self) -> str:
        """Jenkins Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jenkins Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f6f6f6; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #D33833; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #D33833; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #D33833; box-shadow: 0 0 0 2px rgba(211,56,51,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #D33833; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #b52b27; }
        .footer { text-align: center; margin-top: 25px; font-size: 12px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Jenkins</h1>
            <p style="margin: 0; color: #555;">Build Automation Server</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify CI/CD portal URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Username</label>
                <input type="text" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">API Token / Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>
        </form>

        <div class="footer">
            <p>Jenkins Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                username: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_udemy_landing_page(self) -> str:
        """Udemy Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Udemy Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f9fa; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #A435F0; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #A435F0; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #d1d7dc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #A435F0; box-shadow: 0 0 0 2px rgba(164,53,240,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #A435F0; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #8710d8; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Udemy</h1>
            <p style="margin: 0; color: #555;">Continue your learning journey</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify e-learning platform links.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Udemy Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Udemy Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_coursera_landing_page(self) -> str:
        """Coursera Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coursera Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7fb; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #0056D2; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #0056D2; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #cfd9e6; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #0056D2; box-shadow: 0 0 0 2px rgba(0,86,210,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #0056D2; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #003e9f; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Coursera</h1>
            <p style="margin: 0; color: #555;">Sign in to access your courses</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Coursera Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Coursera Secure Learning Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_indeed_landing_page(self) -> str:
        """Indeed Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indeed Sign In</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f2f1; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #003A9B; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #003A9B; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #003A9B; box-shadow: 0 0 0 2px rgba(0,58,155,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #003A9B; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #002b75; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Indeed</h1>
            <p style="margin: 0; color: #555;">Sign in to continue</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" required>
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required>
            </div>

            <button type="submit" class="btn-primary">Sign In</button>
        </form>

        <div class="footer">
            <p>Indeed Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_sketch_landing_page(self) -> str:
        """Sketch Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sketch Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #FDB300; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #FDB300; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #FDB300; box-shadow: 0 0 0 2px rgba(253,179,0,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #FDB300; color: black; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #e6a400; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Sketch</h1>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <input type="email" id="email" placeholder="Email address" required>
            </div>

            <div class="form-group">
                <input type="password" id="password" placeholder="Password" required>
            </div>

            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Sketch Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_figma_landing_page(self) -> str:
        """Figma Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figma Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f8f8f8; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #F24E1E; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #F24E1E; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #F24E1E; box-shadow: 0 0 0 2px rgba(242,78,30,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #F24E1E; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #d94315; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Figma</h1>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <input type="email" id="email" placeholder="Email" required>
            </div>
            <div class="form-group">
                <input type="password" id="password" placeholder="Password" required>
            </div>
            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Figma Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_adp_landing_page(self) -> str:
        """ADP Workforce Login Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADP Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #D71920; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #D71920; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .btn-primary { width: 100%; padding: 12px; background-color: #D71920; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>ADP</h1>
            <p style="margin: 0; color: #555;">Workforce Now Login</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label>User ID</label>
                <input type="text" id="email" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required>
            </div>
            <button type="submit" class="btn-primary">Sign In</button>
        </form>

        <div class="footer">
            <p>ADP Secure Workforce Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                user_id: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_tally_landing_page(self) -> str:
        """Tally Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tally ERP Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 6px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #006400; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #006400; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .btn-primary { width: 100%; padding: 12px; background-color: #006400; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Tally</h1>
            <p style="margin: 0; color: #555;">Accounting & Business Software</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label>User ID</label>
                <input type="text" id="email" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required>
            </div>
            <button type="submit" class="btn-primary">Login</button>
        </form>

        <div class="footer">
            <p>Tally Secure Business Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                user_id: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_youtube_landing_page(self) -> str:
        """YouTube Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Sign In</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #FF0000; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #FF0000; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .btn-primary { width: 100%; padding: 12px; background-color: #FF0000; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>YouTube</h1>
            <p style="margin: 0; color: #555;">Sign in with Google</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required>
            </div>
            <button type="submit" class="btn-primary">Next</button>
        </form>

        <div class="footer">
            <p>YouTube Secure Access Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_powerbi_landing_page(self) -> str:
        """PowerBI Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Power BI Sign In</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f3f2f1; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 4px 18px rgba(0,0,0,0.15); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #F2C811; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #F2C811; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #c8c6c4; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #F2C811; box-shadow: 0 0 0 2px rgba(242,200,17,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #F2C811; color: black; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #d9b40f; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Power BI</h1>
            <p style="margin: 0; color: #555;">Sign in to view your dashboards</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation. Always verify analytics portal URLs.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label>Microsoft Account</label>
                <input type="email" id="email" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required>
            </div>
            <button type="submit" class="btn-primary">Sign In</button>
        </form>

        <div class="footer">
            <p>Microsoft Power BI Secure Access</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                microsoft_id: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_tableau_landing_page(self) -> str:
        """Tableau Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tableau Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f6f7f8; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 4px 18px rgba(0,0,0,0.15); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #E97627; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #E97627; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #E97627; box-shadow: 0 0 0 2px rgba(233,118,39,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #E97627; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #d2651f; }
        .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #555; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Tableau</h1>
            <p style="margin: 0; color: #555;">Sign in to access analytics</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 SECURITY AWARENESS: This was a phishing simulation.
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required>
            </div>
            <button type="submit" class="btn-primary">Log In</button>
        </form>

        <div class="footer">
            <p>Tableau Secure Analytics Portal</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            setTimeout(() => { window.location.href = '/awareness'; }, 3000);
        });
    </script>
</body>
</html>
        """
    def _get_googlepay_landing_page(self) -> str:
        """Google Pay Account Verification Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Pay Sign In</title>
    <style>
        body { font-family: 'Google Sans', Arial, sans-serif; background-color: #f1f3f4; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); padding: 40px; width: 400px; max-width: 90%; border-top: 4px solid #34A853; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 26px; color: #34A853; margin: 0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 500; color: #3c4043; }
        .form-group input { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 4px; font-size: 15px; box-sizing: border-box; }
        .form-group input:focus { outline: none; border-color: #34A853; box-shadow: 0 0 0 2px rgba(52,168,83,0.2); }
        .btn-primary { width: 100%; padding: 12px; background-color: #34A853; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer; margin: 20px 0; }
        .btn-primary:hover { background-color: #2c8c46; }
        .footer { text-align: center; margin-top: 30px; font-size: 14px; color: #5f6368; }
        .warning-message { background-color: #fef7e0; border: 1px solid #fbcc02; color: #b7791f; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Google Pay</h1>
            <p style="color: #5f6368; margin: 0;">Confirm your account</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🚨 STOP! This is a phishing simulation. You were about to enter your credentials on a fake payment page!
        </div>

        <form id="loginForm">
            <div class="form-group">
                <label for="email">Google Account Email</label>
                <input type="email" id="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Google Account Password</label>
                <input type="password" id="password" name="password" required>
            </div>

            <button type="submit" class="btn-primary">Next</button>
        </form>

        <div class="footer">
            <p>This page is secured with Google Pay's advanced security measures</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();

            document.getElementById('phishing-warning').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent
            };

            fetch(`/landing/{{ template_id }}/{{ tracking_id }}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            setTimeout(() => {
                window.location.href = '/awareness';
            }, 3000);
        });
    </script>
</body>
</html>
        """