# Utils Folder

This folder contains utility scripts for setup, maintenance, and fixes.

## Setup Scripts

### Initial Setup
- `setup_admin.py` - Create admin user account
- `setup_test_users.py` - Create test users (students, teachers)
- `setup_test_meeting.py` - Create test meeting data

## Fix Scripts

### Camera Fixes
- `fix_camera_7.py` - Fix specific camera issues
- `fix_droidcam_path.py` - Fix DroidCam path configuration

### Camera Control
- `pause_camera.py` - Pause/resume camera streaming

## Profile Management
- `update_profiles.py` - Update user profile data

## Usage

Run any utility script from the project root:
```bash
python utils/setup_admin.py
```

Or from within the utils folder:
```bash
cd utils
python setup_admin.py
```

## Notes

- Setup scripts should be run once during initial configuration
- Fix scripts are for troubleshooting specific issues
- Always backup your database before running fix scripts
