[BUG] Forgot Password

**Description**
Does not send email when clicking the forgot password link.

**To Reproduce**
1. Execute streamlit run app.py
2. Click forgot password

**Expected Behavior**
Link shoudl be sent to email.

**Current Behavior**
It does nothing

**Impact**
High: Blocks core functionality

**Additional Context**
- File: src/pages/clientdashboard.py
