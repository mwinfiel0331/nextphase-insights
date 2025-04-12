[BUG] Admin - not showing admin dashboard

**Description**
When logging in as as admin (melissa.bolcar@gmail.com), the portal admindashboard.py should be displayed,  but it is not.

**To Reproduce**
1. Execute streamlit run app.py
2. Enter credentials for melissa.bolcar@gmail.com

**Expected Behavior**
Admin portal should be displayed

**Current Behavior**
- It asks me to create a client intake form

**Impact**
High: Blocks core functionality

**Additional Context**
- File: src/pages/admindashboard.py
