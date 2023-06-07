from google.oauth2.credentials import Credentials
import gspread
import pandas as pd
from dateutil.parser import parse as dt
from datetime import datetime

def portal(sheet_url, sheet_name):

    scopes = ["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_authorized_user_file('token.json', scopes)
    client = gspread.authorize(creds)
    ws = client.open_by_url(sheet_url).worksheet(sheet_name)
    
    # Creating Pandas DataFrame:
    df = pd.DataFrame(ws.get_values("B3:G"), columns = "Date Day Time Module Topic Venue".split())

    #Product ID:
    df["product"] = "115"
    product = df["product"].unique()[0]

    #Course Name:
    course_name = df["Module"].unique()[0]

    #Specific Changes to the Spreadsheet:
    df["Lesson Date"] = df["Date"].apply(lambda x:f'{dt(x.split("-")[0]).date().strftime("%Y%m%d")}')

    # Retrieve Lesson Dates from EVERY Row:
    lesson_date = [df["Lesson Date"][i] for i in range(0, len(df))]

    # Retrieve Lesson Time from EVERY Row:
    lesson_time = [df["Time"][i] for i in range(0, len(df))]

    # Retrieve Venue from EVERY Row:
    location = [df["Venue"][i] for i in range(0, len(df))]

    # Transpose this into a new DataFrame:
    df_1 = pd.DataFrame(    
        {"lesson_date": [product] + [course_name] + lesson_date + lesson_time + location,}
        ).T.reset_index(drop = True)
    
    # Creating the Column Names based upon the number of Classes (e.g. if 12, then lesson1_date - lesson12_date)
    original = ['course_title' if i == 0 else f'lesson{i}_date' for i in range(len(lesson_time)+1)]
    time_lesson = [f'lesson{i}_time' for i in range(1, len(lesson_time) + 1)]
    venue = [f'lesson{i}_location' for i in range(1, len(lesson_time) + 1)]

    # Renaming the Column Names for df_1:
    df_1.columns = ["product"] + original + time_lesson + venue

    # Printing the DataFrame to see progress:
    print(df_1)

    # df_1.to_csv(f"{course_name}.csv", index = False)
    df_1.to_csv(f"bootcamp.csv", index = False)

    return df_1

portal("https://docs.google.com/spreadsheets/d/16Jx56t_n1eVLxFa6HlifJlY9IUvQlmrrAFBX0cVEyAU/edit#gid=1828694328",
       "Class Schedule & Attendance")

#Hello world

