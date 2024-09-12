# Analytical Platform Adhoc Scripts
This repository is intended to store useful one off scripts 

## Current adhoc script

###   Script Name :
    -  **`repositories.py`**  
####  Description:
    - This script searches repositories for workkflows containing artifacts and downloads and them scans with gitleaks for secrets
    - The list of repositories is extracted from the file  **`data-platform-github-access/analytical-platform-repositories.tf`** 
####  Running
    - As this script uses the github api  it requires an access token to run successfully .
    - Generate a Github access token with the follow permissions; repo, workflow, read:packages and SSO configured 
    - Create an environment variable with ``` export   GITHUB_TOKEN=your_github_token ```
    - then run with ```python repositories.py```
        
