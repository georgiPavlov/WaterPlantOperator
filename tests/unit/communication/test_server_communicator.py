"""
Unit tests for ServerCommunicator.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
import http as h
from run.http_communicator.server_communicator import ServerCommunicator
from run.model.status import Status


class TestServerCommunicator:
    """Test cases for ServerCommunicator class."""

    @pytest.fixture
    def communicator(self):
        """Create a ServerCommunicator instance for testing."""
        return ServerCommunicator(device_guid="test-device-123", photos_dir="/tmp/photos")

    def test_server_communicator_initialization(self):
        """Test ServerCommunicator initialization."""
        device_guid = "test-device-456"
        photos_dir = "/tmp/test_photos"
        
        communicator = ServerCommunicator(device_guid, photos_dir)
        
        assert communicator.device_guid == device_guid
        assert communicator.photos_dir == photos_dir
        assert communicator.IP_ADDRESS == "wmeautomation.de"
        assert communicator.PORT == "444"
        assert communicator.PROTOCOL == "https"

    @patch('run.http_communicator.server_communicator.requests.get')
    def test_get_plan_success(self, mock_get, communicator):
        """Test successful plan retrieval."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = h.HTTPStatus.OK
        mock_response.json.return_value = {"plan_type": "basic", "water_volume": 200}
        mock_get.return_value = mock_response
        
        result = communicator.get_plan()
        
        assert result == {"plan_type": "basic", "water_volume": 200}
        mock_get.assert_called_once()

    @patch('run.http_communicator.server_communicator.requests.get')
    def test_get_plan_no_content(self, mock_get, communicator):
        """Test plan retrieval with no content."""
        # Mock no content response
        mock_response = Mock()
        mock_response.status_code = h.HTTPStatus.NO_CONTENT
        mock_get.return_value = mock_response
        
        result = communicator.get_plan()
        
        assert result == {}
        mock_get.assert_called_once()

    @patch('run.http_communicator.server_communicator.requests.get')
    def test_get_plan_forbidden(self, mock_get, communicator):
        """Test plan retrieval with forbidden response."""
        # Mock forbidden response
        mock_response = Mock()
        mock_response.status_code = h.HTTPStatus.FORBIDDEN
        mock_get.return_value = mock_response
        
        result = communicator.get_plan()
        
        assert result == {}
        mock_get.assert_called_once()

    @patch('run.http_communicator.server_communicator.requests.get')
    def test_get_plan_request_exception(self, mock_get, communicator):
        """Test plan retrieval with request exception."""
        # Mock request exception
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        result = communicator.get_plan()
        
        assert result == {}
        mock_get.assert_called_once()

    @patch('run.http_communicator.server_communicator.requests.request')
    def test_post_water_success(self, mock_request, communicator):
        """Test successful water level posting."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = h.HTTPStatus.CREATED
        mock_response.json.return_value = {"status": "success"}
        mock_request.return_value = mock_response
        
        result = communicator.post_water(75.5)
        
        assert result == {"status": "success"}
        mock_request.assert_called_once()

    @patch('run.http_communicator.server_communicator.requests.request')
    def test_post_water_forbidden(self, mock_request, communicator):
        """Test water level posting with forbidden response."""
        # Mock forbidden response
        mock_response = Mock()
        mock_response.status_code = h.HTTPStatus.FORBIDDEN
        mock_request.return_value = mock_response
        
        result = communicator.post_water(75.5)
        
        assert result == {}
        mock_request.assert_called_once()

    @patch('run.http_communicator.server_communicator.requests.request')
    def test_post_moisture_success(self, mock_request, communicator):
        """Test successful moisture level posting."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = h.HTTPStatus.CREATED
        mock_response.json.return_value = {"status": "success"}
        mock_request.return_value = mock_response
        
        result = communicator.post_moisture(60.0)
        
        assert result == {"status": "success"}
        mock_request.assert_called_once()

    @patch('run.http_communicator.server_communicator.requests.request')
    def test_post_plan_execution_success(self, mock_request, communicator):
        """Test successful plan execution status posting."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = h.HTTPStatus.CREATED
        mock_response.json.return_value = {"status": "success"}
        mock_request.return_value = mock_response
        
        status = Status(True, "Test message")
        result = communicator.post_plan_execution(status)
        
        assert result == {"status": "success"}
        mock_request.assert_called_once()

    @patch('run.http_communicator.server_communicator.requests.get')
    def test_get_water_level_success(self, mock_get, communicator):
        """Test successful water level retrieval."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = h.HTTPStatus.OK
        mock_response.json.return_value = {"water": 1500}
        mock_get.return_value = mock_response
        
        result = communicator.get_water_level()
        
        assert result == {"water": 1500}
        mock_get.assert_called_once()

    @patch('run.http_communicator.server_communicator.requests.get')
    def test_get_picture_success(self, mock_get, communicator):
        """Test successful picture request retrieval."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = h.HTTPStatus.OK
        mock_response.json.return_value = {"photo_id": "test_photo"}
        mock_get.return_value = mock_response
        
        result = communicator.get_picture()
        
        assert result == {"photo_id": "test_photo"}
        mock_get.assert_called_once()

    @patch('run.http_communicator.server_communicator.os.system')
    def test_post_picture(self, mock_system, communicator):
        """Test picture posting."""
        photo_name = "test_photo"
        
        communicator.post_picture(photo_name)
        
        # Verify os.system was called with curl command
        mock_system.assert_called_once()
        call_args = mock_system.call_args[0][0]
        assert "curl" in call_args
        assert photo_name in call_args
        assert communicator.device_guid in call_args

    @patch('run.http_communicator.server_communicator.socket.socket')
    def test_get_ip_address(self, mock_socket_class, communicator):
        """Test IP address retrieval."""
        # Mock socket
        mock_socket = Mock()
        mock_socket.getsockname.return_value = ("192.168.1.100", 12345)
        mock_socket_class.return_value = mock_socket
        
        result = communicator.get_ip_address()
        
        # Should return the hardcoded IP address, not the actual one
        assert result == "wmeautomation.de"
        mock_socket.connect.assert_called_with(("8.8.8.8", 80))
        mock_socket.close.assert_called_once()

    def test_build_url_for_request(self, communicator):
        """Test URL building for requests."""
        protocol = "https"
        ip = "192.168.1.100"
        request_url = "getPlan"
        
        result = communicator.build_ulr_for_request(protocol, ip, request_url)
        
        expected = f"{protocol}://{ip}:{communicator.PORT}/{communicator.APP_MASTER_URL}/{request_url}"
        assert result == expected

    def test_return_empty_json(self, communicator):
        """Test returning empty JSON."""
        result = communicator.return_emply_json()
        
        assert result == {}

    @patch('run.http_communicator.server_communicator.requests.get')
    def test_get_plan_with_different_status_codes(self, mock_get, communicator):
        """Test get_plan with various HTTP status codes."""
        test_cases = [
            (h.HTTPStatus.OK, {"plan": "test"}),
            (h.HTTPStatus.NO_CONTENT, {}),
            (h.HTTPStatus.FORBIDDEN, {}),
            (h.HTTPStatus.BAD_REQUEST, {}),
            (h.HTTPStatus.INTERNAL_SERVER_ERROR, {})
        ]
        
        for status_code, expected_result in test_cases:
            mock_response = Mock()
            mock_response.status_code = status_code
            if status_code == h.HTTPStatus.OK:
                mock_response.json.return_value = {"plan": "test"}
            mock_get.return_value = mock_response
            
            result = communicator.get_plan()
            
            assert result == expected_result

    @patch('run.http_communicator.server_communicator.requests.request')
    def test_post_methods_with_exception(self, mock_request, communicator):
        """Test POST methods with request exceptions."""
        mock_request.side_effect = requests.exceptions.RequestException("Network error")
        
        # Test all POST methods
        methods_to_test = [
            (communicator.post_water, (75.5,)),
            (communicator.post_moisture, (60.0,)),
            (communicator.post_plan_execution, (Status(True, "test"),))
        ]
        
        for method, args in methods_to_test:
            result = method(*args)
            assert result == {}
