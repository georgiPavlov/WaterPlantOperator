"""
Unit tests for Email Sender.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import smtplib
import ssl
from run.email_sender.sender import Sender


class TestSender:
    """Test cases for Sender class."""

    @pytest.fixture
    def sender(self):
        """Create a Sender instance for testing."""
        return Sender()

    def test_sender_initialization(self, sender):
        """Test Sender initialization."""
        assert hasattr(sender, 'EMAIL_MESSAGES')
        assert 'last_watered' in sender.EMAIL_MESSAGES
        assert 'check_water_level' in sender.EMAIL_MESSAGES
        
        # Check message structure
        last_watered_msg = sender.EMAIL_MESSAGES['last_watered']
        assert 'subject' in last_watered_msg
        assert 'message' in last_watered_msg
        assert last_watered_msg['subject'] == 'Raspberry Pi: Plant Watering Time'
        assert last_watered_msg['message'] == 'Your plant was last watered at'
        
        check_water_msg = sender.EMAIL_MESSAGES['check_water_level']
        assert 'subject' in check_water_msg
        assert 'message' in check_water_msg
        assert check_water_msg['subject'] == 'Raspberry Pi: Check Water Level'
        assert check_water_msg['message'] == 'Check your water level!'

    @patch('run.email_sender.sender.smtplib.SMTP_SSL')
    def test_send_email_with_time(self, mock_smtp_ssl, sender):
        """Test sending email with time_last_watered."""
        mock_server = Mock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server
        
        time_last_watered = "2023-01-15 10:30:00"
        subject = "Test Subject"
        message = "Test message"
        
        sender.send_email(time_last_watered, subject, message)
        
        # Verify SMTP connection was established
        mock_smtp_ssl.assert_called_once()
        call_args = mock_smtp_ssl.call_args
        assert call_args[0][0] == "smtp.gmail.com"
        assert call_args[0][1] == 465
        
        # Verify login was called
        mock_server.login.assert_called_once_with("YOUR_EMAIL@gmail.com", "YOUR_PASSWORD")
        
        # Verify sendmail was called
        mock_server.sendmail.assert_called_once()
        call_args = mock_server.sendmail.call_args
        assert call_args[0][0] == "YOUR_EMAIL@gmail.com"  # FROM
        assert call_args[0][1] == "YOUR_EMAIL@gmail.com"  # TO
        assert "Test Subject" in call_args[0][2]  # Message content
        assert "Test message" in call_args[0][2]
        assert "2023-01-15 10:30:00" in call_args[0][2]

    @patch('run.email_sender.sender.smtplib.SMTP_SSL')
    def test_send_email_without_time(self, mock_smtp_ssl, sender):
        """Test sending email without time_last_watered."""
        mock_server = Mock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server
        
        subject = "Test Subject"
        message = "Test message"
        
        sender.send_email(False, subject, message)
        
        # Verify sendmail was called
        mock_server.sendmail.assert_called_once()
        call_args = mock_server.sendmail.call_args
        assert "Test Subject" in call_args[0][2]
        assert "Test message" in call_args[0][2]
        # Should not contain time information
        assert "2023-01-15" not in call_args[0][2]

    @patch('run.email_sender.sender.smtplib.SMTP_SSL')
    def test_send_email_with_none_time(self, mock_smtp_ssl, sender):
        """Test sending email with None time_last_watered."""
        mock_server = Mock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server
        
        subject = "Test Subject"
        message = "Test message"
        
        sender.send_email(None, subject, message)
        
        # Verify sendmail was called
        mock_server.sendmail.assert_called_once()
        call_args = mock_server.sendmail.call_args
        assert "Test Subject" in call_args[0][2]
        assert "Test message" in call_args[0][2]

    @patch('run.email_sender.sender.smtplib.SMTP_SSL')
    def test_send_last_watered_email(self, mock_smtp_ssl, sender):
        """Test sending last watered email."""
        mock_server = Mock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server
        
        time_last_watered = "2023-01-15 14:30:00"
        
        sender.send_last_watered_email(time_last_watered)
        
        # Verify sendmail was called with correct content
        mock_server.sendmail.assert_called_once()
        call_args = mock_server.sendmail.call_args
        message_content = call_args[0][2]
        
        assert "Raspberry Pi: Plant Watering Time" in message_content
        assert "Your plant was last watered at" in message_content
        assert "2023-01-15 14:30:00" in message_content

    @patch('run.email_sender.sender.smtplib.SMTP_SSL')
    def test_send_check_water_level_email(self, mock_smtp_ssl, sender):
        """Test sending check water level email."""
        mock_server = Mock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server
        
        sender.send_check_water_level_email()
        
        # Verify sendmail was called with correct content
        mock_server.sendmail.assert_called_once()
        call_args = mock_server.sendmail.call_args
        message_content = call_args[0][2]
        
        assert "Raspberry Pi: Check Water Level" in message_content
        assert "Check your water level!" in message_content

    @patch('run.email_sender.sender.smtplib.SMTP_SSL')
    def test_send_email_smtp_exception(self, mock_smtp_ssl, sender):
        """Test sending email with SMTP exception."""
        mock_smtp_ssl.side_effect = smtplib.SMTPException("SMTP error")
        
        # Should raise the exception
        with pytest.raises(smtplib.SMTPException):
            sender.send_email("2023-01-15 10:00:00", "Test", "Message")

    @patch('run.email_sender.sender.smtplib.SMTP_SSL')
    def test_send_email_authentication_error(self, mock_smtp_ssl, sender):
        """Test sending email with authentication error."""
        mock_server = Mock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, "Authentication failed")
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server
        
        # Should raise the exception
        with pytest.raises(smtplib.SMTPAuthenticationError):
            sender.send_email("2023-01-15 10:00:00", "Test", "Message")

    def test_email_messages_structure(self, sender):
        """Test that email messages have the correct structure."""
        for message_type, message_data in sender.EMAIL_MESSAGES.items():
            assert isinstance(message_data, dict)
            assert 'subject' in message_data
            assert 'message' in message_data
            assert isinstance(message_data['subject'], str)
            assert isinstance(message_data['message'], str)
            assert len(message_data['subject']) > 0
            assert len(message_data['message']) > 0

    @patch('run.email_sender.sender.smtplib.SMTP_SSL')
    def test_send_email_message_formatting(self, mock_smtp_ssl, sender):
        """Test email message formatting."""
        mock_server = Mock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server
        
        time_last_watered = "2023-01-15 10:30:00"
        subject = "Test Subject"
        message = "Test message"
        
        sender.send_email(time_last_watered, subject, message)
        
        # Get the actual message content
        call_args = mock_server.sendmail.call_args
        message_content = call_args[0][2]
        
        # Check message format
        assert message_content.startswith("Subject: Test Subject")
        assert "Test message 2023-01-15 10:30:00" in message_content

    @patch('run.email_sender.sender.smtplib.SMTP_SSL')
    def test_send_email_without_time_message_formatting(self, mock_smtp_ssl, sender):
        """Test email message formatting without time."""
        mock_server = Mock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server
        
        subject = "Test Subject"
        message = "Test message"
        
        sender.send_email(False, subject, message)
        
        # Get the actual message content
        call_args = mock_server.sendmail.call_args
        message_content = call_args[0][2]
        
        # Check message format
        assert message_content.startswith("Subject: Test Subject")
        assert "Test message" in message_content
        # Should end with just the message (no time appended)
        assert message_content.endswith("Test message")
