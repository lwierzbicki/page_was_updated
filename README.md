# page_was_updated
Simple checker to verify if there is a new content on defined list of pages (URL). It checks if page was modified.

If page was changed, it generates console output that page was changed.
It iterates through list of pages from pages_to_check.txt.

Run 
```bash
python3 checker.py
```

Files:
- checker.py - python program to perform action
- pages_to_check.txt - file with list of pages (URLs) to check. One URL per line.
- stored_data.json - file where program keeps data about checked pages. It contains URL and hash of page obtained during check.