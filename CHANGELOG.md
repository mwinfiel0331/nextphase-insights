# Changelog

All notable changes to NextPhase Insights will be documented in this file.

## [1.3.0] - 2025-04-13

### Added
- Company information form with validation
- Session state management for form data
- Two-column layout for company and contact details
- Industry selection dropdown
- Company size slider
- Required field indicators
- Help text for form fields
- Debug logging for form submissions

### Changed
- Improved form field organization
- Enhanced data persistence in session state
- Updated industry options list
- Optimized form validation logic

### Fixed
- Session state initialization issues
- Form data persistence bugs
- Field validation feedback

## [1.2.1] - 2025-04-12

### Added
- Dashboard metrics for user and intake tracking
- User status toggle functionality
- Intake review system
- Safe field access with fallbacks
- Enhanced error logging and display

### Changed
- Improved admin dashboard interface
- Enhanced user management display
- Updated intake review process
- Modified data retrieval with safety checks

### Fixed
- User data retrieval and display issues
- Intake form field access errors
- Dashboard metrics calculation
- Status toggle persistence

## [1.2.0] - 2025-04-12

### Added
- Multi-step client intake form with progress tracking
- Draft saving functionality for intake forms
- Review and edit capability before submission
- Tool selection interface with customizable categories
- Process documentation file upload support
- Workflow status tracking system
- Enhanced form validation and error handling

### Changed
- Separated database initialization and index management
- Improved Firebase credentials handling
- Updated tool categories configuration
- Enhanced logging system for better debugging
- Reorganized initialization scripts for modularity

### Fixed
- Permission issues with Firestore Admin access
- Index creation error handling
- Form navigation and state management
- Tool selection persistence in review mode
- Documentation upload validation

## [1.1.0] - 2024-04-12

### Added
- AI-powered process analysis using OpenAI GPT-3.5
- Process recommendation system with caching
- Automation potential scoring
- Input validation for process details
- Response caching to reduce API calls
- Error handling and logging system

### Fixed
- Resolved unhashable type errors in caching mechanism
- Fixed process validation in automation scoring
- Improved cache key generation for lists and dictionaries
- Addressed API rate limiting issues

## [1.0.0] - 2024-04-12

### Added
- Initial release
- Firebase integration for data storage
- Client intake form
- Session management
- Process optimization dashboard
- Firestore security rules
- Basic data visualization

[1.3.0]: https://github.com/yourusername/nextphase-insights/releases/tag/v1.3.0
[1.2.1]: https://github.com/yourusername/nextphase-insights/releases/tag/v1.2.1
[1.2.0]: https://github.com/yourusername/nextphase-insights/releases/tag/v1.2.0
[1.1.0]: https://github.com/yourusername/nextphase-insights/releases/tag/v1.1.0
[1.0.0]: https://github.com/yourusername/nextphase-insights/releases/tag/v1.0.0