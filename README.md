# Tools

This repository contains various tools for different purposes. Below is an overview of each tool along with instructions on how to use them.

## Geocoding

### Description
This tool provides geocoding functionality using the OpenCage and Google Geocoding API. It takes a location as input and returns its latitude, longitude, and formatted address.

### How to Use
1. **Get an API key:**
   - Get an API key from [OpenCage](https://opencagedata.com/) or [Google](https://developers.google.com/maps/documentation/geocoding/get-api-key).

2. **Configure API keys:**
   - Open the `Geocoding/OpenCage/geocoding.py` file and replace `'YOUR_API_KEY'` with your actual OpenCage API key.
   - Open the `Geocoding/Google/geocoding.py` file and replace `'YOUR_API_KEY'` with your actual Google API key.

3. **Run the script:**
   - Choose the appropriate geocoding provider by running the script from either the OpenCage or Google subfolder.
   - Provide the location you want to geocode.


## Resume_Parser

### Description
Resume_Parser is a tool for parsing information from resumes/CVs. It's designed to extract key details from resumes for further analysis.

### How to Use
1. Open the `Resume_Parser/resume_parser.py` file.
2. Run the script and provide the path to the resume file you want to parse.
3. Extracted information will be displayed or saved as needed.



