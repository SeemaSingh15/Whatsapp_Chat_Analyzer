import re
import pandas as pd


def preprocess(data):
    # Detect if the chat uses AM/PM (12-hour format) or 24-hour format
    if re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s', data):
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
        date_formats = ['%d/%m/%Y, %I:%M %p - ', '%m/%d/%Y, %I:%M %p - ']
    else:
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        date_formats = ['%d/%m/%Y, %H:%M - ', '%m/%d/%Y, %H:%M - ']

    df = pd.DataFrame({'user_message': re.split(pattern, data)[1:],
                       'message_date': re.findall(pattern, data)})

    # Ensure date parsing works for both formats
    df['date'] = None  # Initialize column

    for fmt in date_formats:
        try:
            df['date'] = pd.to_datetime(df['message_date'], format=fmt, errors='coerce')
            if df['date'].notna().all():  # Stop if all values are successfully parsed
                break
        except Exception as e:
            print(f"Error parsing date with format {fmt}: {e}")

    # If still NaT (Not a Time), print for debugging
    if df['date'].isna().sum() > 0:
        print("Some dates could not be parsed! Check input format.")

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)

        if len(entry) > 1:  # Normal user message
            users.append(entry[1].strip())
            messages.append(entry[2].strip())
        else:  # Group system messages (e.g., "You were added to the group")
            users.append('group_notification')
            messages.append(entry[0].strip())

    df['user'] = users
    df['message'] = messages

    # Ensure date column is valid
    if df['date'].isna().all():
        print("🚨 ERROR: All dates are NaT! The chat file format may be incorrect.")

    # Extract date/time components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create time period labels
    df['period'] = df['hour'].apply(lambda h: f"{h}-00" if h == 23 else f"00-{h + 1}" if h == 0 else f"{h}-{h + 1}")

    # Drop unnecessary columns
    df.drop(columns=['user_message', 'message_date'], inplace=True)

    return df
