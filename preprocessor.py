import re
import pandas as pd

def preprocess(data):
    # Pattern to detect WhatsApp datetime headers
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*[APap][Mm]\s*-\s*'

    # Split messages and extract dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create initial DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert date strings to datetime objects
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%m/%d/%y, %I:%M %p - ',
        errors='coerce'  # avoids crash if a line doesn’t match
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate user and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract datetime components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name
    df['only_date'] = df['date'].dt.date

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
