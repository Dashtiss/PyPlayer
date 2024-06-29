import vt
import os
from ..error import error
try:
    client = vt.Client(os.environ["VirusTotalAPIKEY"])
    VirusTotal = True
except KeyError:
    error("VirusTotalAPIKEY is not in .env file or inputted in UploadaFiles.py.    VirusTotal Scan Disabled")
    VirusTotal = False


async def ScanURL(URL: str) -> bool:
    """
    This function performs a VirusTotal scan on the given URL and returns a boolean value indicating whether the URL is safe or not.

    Parameters:
    - URL (str): The URL to be scanned.

    Returns:
    - bool: True if the URL is safe, False if it is not.
    """
    # Check if VirusTotal scanning is enabled
    if VirusTotal:
        # Print a message to indicate that the file is being loaded
        print("Loading File")
        # Scan the URL and wait for the completion of the scan
        file = await client.scan_url_async(URL, wait_for_completion=True)
        # Get the ID of the URL from VirusTotal
        url_id = vt.url_id(URL)
        # Get the information about the URL from VirusTotal
        url = await client.get_object_async("/urls/{}", url_id)
        # Check if the URL is considered malicious or suspicious
        if (url.last_analysis_stats['malicious'] + url.last_analysis_stats["suspicious"]) < url.last_analysis_stats['harmless']:
            # Return True if the URL is safe
            return True
        else:
            # Return False if the URL is not safe
            return False
    else:
        # If VirusTotal scanning is disabled, return True to indicate that the URL is safe
        return True
