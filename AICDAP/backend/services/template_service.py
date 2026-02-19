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
                "subject": "🔒 GitHub Security Alert - Immediate Action Required",
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
        }

    def _load_landing_templates(self) -> Dict[str, str]:
        """Load landing page templates"""
        return {
            "1": self._get_google_landing_page(),
            "2": self._get_github_landing_page(),
            "3": self._get_microsoft_landing_page(),
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
                <a href="{{ tracking_urls.landing }}" class="button">
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
                <a href="{{ tracking_urls.landing }}" class="button-danger">
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
                <span style="margin-right: 10px;">🏢</span>
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
                <a href="{{ tracking_urls.landing }}" class="button-update">
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
        <div class="footer">
            <p>© 2024 Microsoft Corporation. All rights reserved.</p>
            <p>Microsoft Office | Redmond, WA 98052 | <a href="#" style="color: #0078d4;">Privacy Policy</a></p>
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
        """Microsoft Office Update Landing Page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft Office Update</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); padding: 40px; width: 500px; max-width: 90%; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #0078d4; margin: 0; font-size: 28px; }
        .download-section { text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 8px; margin: 20px 0; }
        .btn-download { display: inline-block; padding: 15px 30px; background-color: #0078d4; color: white; text-decoration: none; border-radius: 4px; font-size: 16px; font-weight: 600; margin: 10px; }
        .btn-download:hover { background-color: #106ebe; }
        .version-info { background-color: #e8f4fd; padding: 15px; border-radius: 4px; margin: 20px 0; border-left: 4px solid #0078d4; }
        .progress-bar { width: 100%; background-color: #e0e0e0; border-radius: 10px; margin: 20px 0; }
        .progress-fill { width: 0%; height: 20px; background-color: #0078d4; border-radius: 10px; transition: width 2s ease; }
        .warning-message { background-color: #fff3cd; border: 1px solid #ffc107; color: #856404; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>🏢 Microsoft Office</h1>
            <p style="color: #666; margin: 0;">Security Update Download</p>
        </div>

        <div class="warning-message" id="phishing-warning" style="display: none;">
            🛡️ SECURITY TRAINING: This was a phishing simulation! Always verify software updates through official channels.
        </div>

        <div id="download-content">
            <div class="version-info">
                <h3>Critical Security Update Available</h3>
                <p><strong>Version:</strong> 16.0.15726.20202</p>
                <p><strong>Size:</strong> 127.8 MB</p>
                <p><strong>Release Date:</strong> Today</p>
            </div>

            <div class="download-section">
                <h3>Ready to Download</h3>
                <p>Click the button below to download the latest security update for Microsoft Office.</p>

                <button id="downloadBtn" class="btn-download">
                    📥 Download Update (127.8 MB)
                </button>

                <div class="progress-bar" id="progressBar" style="display: none;">
                    <div class="progress-fill" id="progressFill"></div>
                </div>

                <p id="downloadStatus" style="display: none; margin-top: 15px; font-weight: bold;"></p>
            </div>

            <div style="font-size: 12px; color: #666; text-align: center; margin-top: 20px;">
                <p>By downloading, you agree to the Microsoft Software License Terms</p>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('downloadBtn').addEventListener('click', function() {
            // Hide download button and show progress
            this.style.display = 'none';
            document.getElementById('progressBar').style.display = 'block';
            document.getElementById('downloadStatus').style.display = 'block';
            document.getElementById('downloadStatus').textContent = 'Initializing download...';

            // Simulate download progress
            let progress = 0;
            const progressFill = document.getElementById('progressFill');
            const statusText = document.getElementById('downloadStatus');

            const interval = setInterval(() => {
                progress += Math.random() * 20;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);

                    // Show warning after "download" completes
                    setTimeout(() => {
                        document.getElementById('download-content').style.display = 'none';
                        document.getElementById('phishing-warning').style.display = 'block';

                        // Redirect to awareness page
                        setTimeout(() => {
                            window.location.href = '/awareness';
                        }, 3000);
                    }, 1000);
                }

                progressFill.style.width = progress + '%';
                statusText.textContent = `Downloading... ${Math.floor(progress)}%`;
            }, 200);
        });
    </script>
</body>
</html>
        """
