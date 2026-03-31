import re

def clean_event_data(raw_blob):
    """
    Takes the messy 'blob' from BiblioCommons and returns a clean date and time.
    """
    try:
        # Find the Date (e.g., April 11, 2026)
        # Looks for: Month Name + Space + Day + Comma + Space + 4-digit Year
        date_match = re.search(r"[A-Z][a-z]+\s+\d{1,2},\s+\d{4}", raw_blob)
        event_date = date_match.group(0) if date_match else "Unknown Date"

        # Find the Time (e.g., 2:00pm)
        # Looks for: Digits + : + Digits + am/pm
        time_match = re.search(r"\d{1,2}:\d{2}[ap]m[^\d]*\d{1,2}:\d{2}[ap]m", raw_blob)
        event_time = time_match.group(0) if time_match else "Unknown Time"

        return event_date, event_time
        
    except Exception as e:
        print(f"Error extracting data: {e}")
        return "Error", "Error"