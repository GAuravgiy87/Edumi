# Tests Folder

This folder contains all test scripts and utilities for debugging the DigiRoom application.

## Test Scripts

### Camera Tests
- `test_camera_service.py` - Test camera service on port 8001
- `test_camera_feed_direct.py` - Test direct camera feed access
- `test_camera_permissions.py` - Test camera permission system
- `check_all_cameras.py` - Check status of all cameras
- `check_mobile_camera.py` - Check mobile camera connections

### DroidCam Tests
- `test_droidcam.py` - Test DroidCam integration
- `test_droidcam_feed.py` - Test DroidCam feed streaming
- `test_droidcam_direct.py` - Test direct DroidCam connection
- `check_droidcam_html.py` - Check DroidCam HTML interface

### Feed Tests
- `test_feed_auth.py` - Test feed authentication
- `test_feed_url.py` - Test feed URL generation
- `test_feed_now.py` - Quick feed test
- `test_direct_stream.py` - Test direct streaming
- `test_browser_feed.html` - Browser-based feed test
- `test_feed_simple.html` - Simple HTML feed test

### Service Tests
- `test_services.py` - Test all services
- `check_services.py` - Check service status
- `check_status.py` - Overall status check
- `test_full_app.py` - Full application test

### Network Tests
- `test_network_access.py` - Test network accessibility

### Profile Tests
- `test_profile_save.py` - Test profile save functionality

### Other Tests
- `test_pause_resume.py` - Test camera pause/resume

## Usage

Run any test script from the project root:
```bash
python tests/test_camera_service.py
```

Or from within the tests folder:
```bash
cd tests
python test_camera_service.py
```
