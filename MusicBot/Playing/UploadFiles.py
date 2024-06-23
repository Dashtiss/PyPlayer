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
    if VirusTotal:
        print("Loading File")
        file = await client.scan_url_async(URL, wait_for_completion=True)
        url_id = vt.url_id(URL)
        url = await client.get_object_async("/urls/{}", url_id)
        if (url.last_analysis_stats['malicious'] + url.last_analysis_stats["suspicious"]) < url.last_analysis_stats['harmless']:
            return True
        else:
            return False
    else:
        return True
