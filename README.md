# david-annotation
Use DAVID API to get a functional annotation chart report.

Before using this tool, see the information about licensing at the DAVID web:
https://david.ncifcrf.gov/content.jsp?file=Licensing.html

## Usage
1. Register your email at
http://david.abcc.ncifcrf.gov/webservice/register.htm
2. Install suds >= 0.4:
```
pip install suds
```
3. Edit `chart_report.py` and change `USER` variable to your registered email address.
4. Edit `chart_report.py` and change the call to `david_enrich` with your parameters. Alternatively use and call `david_enrich` from another module.
