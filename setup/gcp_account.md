
**Note: Google provides 300USD free credit available for 90 days to new accounts.**

# Create the Project
---
Start in your GCP Account. At the top click the projects drop down and then select +New Project
![NewProjectGCP](https://user-images.githubusercontent.com/7443591/160303897-0491326d-90c5-4be2-8189-1347c0d1955a.png)<br>

You can call the project whatever you would like. We will need to use this name later.
![NameProject](https://user-images.githubusercontent.com/7443591/160303944-c85df7fd-3d34-4e09-80fa-690cec7f274a.png)<br>

Once the new project has been created click the project drop down again and switch to the new project you just created.
![SwitchToNewProject](https://user-images.githubusercontent.com/7443591/160303955-10725499-016a-49a0-a75e-2d2a172af1c0.png)<br>

Click to Enable for the Compute Engine API. This will take a few moments.
![EnableCloudComputeAPI](https://user-images.githubusercontent.com/7443591/160304015-1359de1b-d1f5-45cf-b1af-29f50c365e44.png)<br>

# Create Service Account
---
In GCP scroll down to IAM & Admin and select IAM<br>
![IAM](https://user-images.githubusercontent.com/7443591/160307298-2d6f0f75-179d-4110-8eaf-5a88437cd39c.png)<br>


Scroll down to Service Accounts<br>
![ServiceAccount](https://user-images.githubusercontent.com/7443591/160307321-c48b5677-9f11-43cc-9a9c-c6a168b43de5.png)<br>

Select Create Service Account<br>
![CreateServiceAccount](https://user-images.githubusercontent.com/7443591/160307333-a1975b81-eb75-47cf-ab0d-917dbdece8e4.png)<br>

Name it whatever you would like and click Create and Continue<br>
![NameServiceAccount](https://user-images.githubusercontent.com/7443591/160307376-bb4f191e-3a02-43b0-955b-cd8094163cf7.png)<br>

Give the service account the following roles (Storage Admin + Storage Object Admin + BigQuery Admin)<br>
![serviceAccountRoles](https://user-images.githubusercontent.com/7443591/160307396-10560756-84cd-489e-9dbe-e2d05e22d8dc.png)<br>

Click continue and then done. You should now see the service account. Click the three dot elipse on the right hand side and choose manage keys.<br>
![ManageKeys](https://user-images.githubusercontent.com/7443591/160307479-af264fdc-5500-440e-bef1-c0773541091b.png)<br>

Choose Add Key then Create New Key<br>
![AddKey](https://user-images.githubusercontent.com/7443591/160307539-aa50578a-514c-4e6a-9483-9a24353e544c.png)<br>

Click create and it will download the .json key to your computer<br>
![CreateKey](https://user-images.githubusercontent.com/7443591/160307568-b6bfcb42-d053-432a-8982-374c9b23f1da.png)<br>
