# Analytical Platform Adhoc Scripts
This repository is intended to store useful one off scripts 

## Current adhoc scripts
### **`repositories.py`**
### **`repo_search.py`**

###   Script Name : **`repositories.py`**  
####  Description:
This script searches repositories for workkflows containing artifacts, downloads them, then scans with gitleaks for secrets.

The list of repositories is extracted from the file  **`data-platform-github-access/analytical-platform-repositories.tf`** 

####  Running
As this script uses the github api  it requires an access token to run successfully.

Generate a Github access token with the follow permissions; repo, workflow, read:packages and SSO configured.

Create an environment variable with ``` export   GITHUB_TOKEN=your_github_token ```

Run with ```python repositories.py```

###   Script Name : **`repo_search.py`**  
####  Description:
This script searches the ```ministryofjustice``` organisation for repositories  ```analytical-platform*``` repositories containing the phrase upload-artifact and reports the repository and file in which it is found.

####  Running
As this script uses the github api  it requires an access token to run successfully.

Generate a Github access token with the follow permissions; repo, workflow, read:packages and SSO configured.

Create an environment variable with ``` export   GITHUB_TOKEN=your_github_token ```

Run with ```python repo_search.py```