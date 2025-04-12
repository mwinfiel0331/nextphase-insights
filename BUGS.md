# Known Issues and Enhancement Requests

## High Priority

### Client Intake Form
- [ ] **Bug**: Duplicate submit buttons appear in review section
  - **Impact**: User confusion and potential duplicate submissions
  - **Location**: `src/pages/intake_form.py` in `show_review()`
  - **Status**: Needs investigation

- [ ] **Bug**: Tool selections don't persist after edit mode
  - **Impact**: Users lose their selections when editing
  - **Location**: `src/pages/intake_form.py` in Tools Assessment section
  - **Status**: In progress

### Firebase Integration
- [ ] **Bug**: Index creation failing silently
  - **Impact**: Missing indexes affect query performance
  - **Location**: `scripts/manage_indexes.py`
  - **Status**: Needs investigation

## Medium Priority

### Documentation
- [ ] **Enhancement**: Add validation for file uploads
  - **Impact**: Better user feedback for document submissions
  - **Location**: `src/pages/intake_form.py` in `show_documentation()`
  - **Status**: Not started

### Authentication
- [ ] **Bug**: Firebase credentials requiring repeated authentication
  - **Impact**: Developer experience during initialization
  - **Location**: Multiple initialization scripts
  - **Status**: Under review