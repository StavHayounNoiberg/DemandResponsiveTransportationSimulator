from datetime import datetime, timedelta


def get_datetimes_between(start_date: datetime, end_date: datetime) -> list[datetime]:
    """
    Generate a list of datetimes at midnight between two dates, including those dates
    
    Args:
        start_date: The start date
        end_date: The end date
    
    Returns:
        A list of datetimes at midnight between the start and end dates
    """
    date_list = [start_date]
    # Calculate the next midnight after the start_time
    current_date = start_date.replace(
        hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    # Add midnights until the day before the end_time
    while current_date < end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    # Add the end_time
    date_list.append(end_date)
    return date_list


def get_day_number(date: datetime):
    """
    Get the day number (1 for Sunday, 2 for Monday, ..., 7 for Saturday) from a datetime object
    
    Args:
        date: The datetime object
    
    Returns:
        The day number
    """
    return (date.weekday() + 1) % 7 + 1
