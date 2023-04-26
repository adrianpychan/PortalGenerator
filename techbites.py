from google.oauth2.credentials import Credentials
import gspread
import pandas as pd
from dateutil.parser import parse as dt
from datetime import datetime

def techbites_sheets():
    sheets_url = "https://docs.google.com/spreadsheets/d/1r3KcVVeshJx7NzCBtAFf0oqEevN-mEQwHoVzsAlMrpk/edit#gid=0"
    sheet_name = "TechBites Payment Logging"
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_authorized_user_file('token.json', scopes)
    client = gspread.authorize(creds)
    ws = client.open_by_url(sheets_url).worksheet(sheet_name)

    # Creating Pandas DataFrame:
    df = pd.DataFrame(ws.get_values("A3:L"), columns = "nomad_id nomad_tier nomad_name contact_number techbite_date_start start_time end_time hours type payment_per_hour total_payment Remarks".split())
    df = df[df["techbite_date_start"] != ""].sort_values(by=['techbite_date_start', "start_time", "end_time"], ascending=True).reset_index(drop = True)

    #Specific Changes to the Spreadsheet:
    df["month"] = df["techbite_date_start"].apply(lambda x:int(float(x.split("-")[1])))
    df["techbite_date_start"] = df["techbite_date_start"].apply(lambda x:x.replace('-', ""))
    df["techbite_time"] = df["start_time"] + "-" + df["end_time"]
    df["location"] = "18/F, Tower 535, 535 Jaffe Road, Causeway Bay, Hong Kong"
    df["Course Name"] = f"{datetime.now().strftime('%Y %B')} - TechBites Schedule"

    #Retrieve Information from current Month only.

    this_month = df[df["month"] == datetime.now().month][["nomad_name", "techbite_date_start", "techbite_time", "location", "Course Name"]].reset_index(drop = True)

    # Retrieve TechBites Dates from every Row:
    techbites_date = [this_month["techbite_date_start"][i] for i in range(0, len(this_month))]

    # Retrieve Lesson Time from every Row:
    lesson_time = [this_month["techbite_time"][i] for i in range(0, len(this_month))]

    # Retrieve Venue from every Row:
    location = [this_month["location"][i] for i in range(0, len(this_month))]

    # Transpose this into a new DataFrame:

    df_1 = pd.DataFrame({
        "lesson_date": ["FALSE"] + [this_month["Course Name"].unique()[0]] + techbites_date + lesson_time + location,
        }).T.reset_index(drop = True)
        
    # Creating the Column Names based upon the number of Classes (e.g. if 12, then lesson1_date - lesson12_date)
    display = ["display" for i in range(len(this_month)+1) if i == 0]
    original = ['course_title' if i == 0 else f'lesson{i}_date' for i in range(len(this_month)+1)]
    time_lesson = [f'lesson{i}_time' for i in range(1, len(this_month) + 1)]
    venue = [f'lesson{i}_location' for i in range(1, len(this_month) + 1)]

    # Renaming the Column Names for df_1:
    df_1.columns = display + original + time_lesson + venue

    # Printing the DataFrame to see progress:
    print(df_1)

    # Exporting to .csv:
    techbites_string = f"{datetime.now().strftime('%Y%b')}-TechBites_Schedule.csv"
    df_1.to_csv(techbites_string, index = False)

    return df_1

techbites_sheets()