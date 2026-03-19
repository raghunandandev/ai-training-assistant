import pandas as pd
import os
from datetime import datetime

class ComplianceTracker:
    def __init__(self, db_file="compliance_log.csv"):
        """Initializes the CSV database. Creates it if it doesn't exist."""
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            df = pd.DataFrame(columns=["Timestamp", "Employee_Name", "SOP_Title", "Score"])
            df.to_csv(self.db_file, index=False)

    def log_score(self, employee_name: str, sop_title: str, score: str):
        """Appends a new quiz score record to the database."""
        new_record = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Employee_Name": employee_name,
            "SOP_Title": sop_title,
            "Score": score
        }])
        # Append to existing CSV
        new_record.to_csv(self.db_file, mode='a', header=False, index=False)