"""
Unit tests for Camera sensor.
"""
import pytest
from unittest.mock import Mock, patch
from run.sensor.camera_sensor import Camera


class TestCamera:
    """Test cases for Camera class."""

    @pytest.fixture
    def mock_camera_instance(self):
        """Create a mock camera instance for testing."""
        camera = Mock()
        camera.start_preview = Mock()
        camera.stop_preview = Mock()
        camera.capture = Mock()
        return camera

    def test_camera_initialization(self, mock_camera_instance):
        """Test Camera initialization."""
        photos_dir = "/tmp/photos"
        wait_before_still = 5
        
        camera = Camera(mock_camera_instance, photos_dir, wait_before_still)
        
        assert camera.camera_instance == mock_camera_instance
        assert camera.photos_dir == photos_dir
        assert camera.wait_before_still_in_seconds == wait_before_still

    @patch('run.sensor.camera_sensor.sleep')
    def test_take_photo(self, mock_sleep, mock_camera_instance):
        """Test taking a photo."""
        photos_dir = "/tmp/photos"
        wait_before_still = 3
        photo_name = "test_photo"
        
        camera = Camera(mock_camera_instance, photos_dir, wait_before_still)
        camera.take_photo(photo_name)
        
        # Verify camera operations
        mock_camera_instance.start_preview.assert_called_once()
        mock_camera_instance.stop_preview.assert_called_once()
        mock_camera_instance.capture.assert_called_once_with(f"{photos_dir}/{photo_name}.jpg")
        
        # Verify sleep was called
        mock_sleep.assert_called_once_with(wait_before_still)

    @patch('run.sensor.camera_sensor.sleep')
    def test_take_photo_different_names(self, mock_sleep, mock_camera_instance):
        """Test taking photos with different names."""
        photos_dir = "/tmp/photos"
        wait_before_still = 2
        
        camera = Camera(mock_camera_instance, photos_dir, wait_before_still)
        
        photo_names = ["photo1", "plant_2023_01_15", "test-image", "camera_shot"]
        
        for photo_name in photo_names:
            camera.take_photo(photo_name)
            
            # Verify capture was called with correct path
            expected_path = f"{photos_dir}/{photo_name}.jpg"
            mock_camera_instance.capture.assert_called_with(expected_path)

    @patch('run.sensor.camera_sensor.sleep')
    def test_take_photo_different_directories(self, mock_sleep, mock_camera_instance):
        """Test taking photos in different directories."""
        wait_before_still = 1
        photo_name = "test_photo"
        
        directories = ["/tmp/photos", "/home/user/images", "/var/cache/camera", "/opt/plant_photos"]
        
        for photos_dir in directories:
            camera = Camera(mock_camera_instance, photos_dir, wait_before_still)
            camera.take_photo(photo_name)
            
            # Verify capture was called with correct path
            expected_path = f"{photos_dir}/{photo_name}.jpg"
            mock_camera_instance.capture.assert_called_with(expected_path)

    @patch('run.sensor.camera_sensor.sleep')
    def test_take_photo_different_wait_times(self, mock_sleep, mock_camera_instance):
        """Test taking photos with different wait times."""
        photos_dir = "/tmp/photos"
        photo_name = "test_photo"
        
        wait_times = [0, 1, 3, 5, 10]
        
        for wait_time in wait_times:
            camera = Camera(mock_camera_instance, photos_dir, wait_time)
            camera.take_photo(photo_name)
            
            # Verify sleep was called with correct time
            mock_sleep.assert_called_with(wait_time)

    @patch('run.sensor.camera_sensor.sleep')
    def test_take_photo_camera_operations_order(self, mock_sleep, mock_camera_instance):
        """Test that camera operations are called in correct order."""
        photos_dir = "/tmp/photos"
        wait_before_still = 2
        photo_name = "test_photo"
        
        camera = Camera(mock_camera_instance, photos_dir, wait_before_still)
        camera.take_photo(photo_name)
        
        # Verify operations were called in correct order
        assert mock_camera_instance.start_preview.called
        assert mock_sleep.called
        assert mock_camera_instance.capture.called
        assert mock_camera_instance.stop_preview.called

    @patch('run.sensor.camera_sensor.sleep')
    def test_take_photo_camera_exception_handling(self, mock_sleep, mock_camera_instance):
        """Test camera exception handling."""
        photos_dir = "/tmp/photos"
        wait_before_still = 1
        photo_name = "test_photo"
        
        # Make capture raise an exception
        mock_camera_instance.capture.side_effect = Exception("Camera error")
        
        camera = Camera(mock_camera_instance, photos_dir, wait_before_still)
        
        # Should raise the exception
        with pytest.raises(Exception, match="Camera error"):
            camera.take_photo(photo_name)
        
        # Verify start_preview was still called
        mock_camera_instance.start_preview.assert_called_once()
        mock_sleep.assert_called_once()

    def test_camera_initialization_with_none_values(self, mock_camera_instance):
        """Test Camera initialization with None values."""
        photos_dir = None
        wait_before_still = 0
        
        camera = Camera(mock_camera_instance, photos_dir, wait_before_still)
        
        assert camera.camera_instance == mock_camera_instance
        assert camera.photos_dir is None
        assert camera.wait_before_still_in_seconds == 0

    @patch('run.sensor.camera_sensor.sleep')
    def test_take_photo_with_none_directory(self, mock_sleep, mock_camera_instance):
        """Test taking photo with None directory."""
        photos_dir = None
        wait_before_still = 1
        photo_name = "test_photo"
        
        camera = Camera(mock_camera_instance, photos_dir, wait_before_still)
        camera.take_photo(photo_name)
        
        # Verify capture was called with None directory
        expected_path = f"None/{photo_name}.jpg"
        mock_camera_instance.capture.assert_called_with(expected_path)
