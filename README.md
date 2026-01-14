# Introduction
This is a tool capable of creating video ideas, from the scripts, to audio to video then subtitles and merge it all in one to post to your Youtube and Facebook page.

>[!NOTE]
>Follow the steps given with upmost precision.

>[!WARNING]
>I am not responsible for the misuse of this tool and it is only intended for educational purposes to showcase the pipeline process of how automation meets API.

## Step 1 GETTING REQUIRED API's
+ Head over to https://huggingface.co/ and create a free account.
+ After creating head over to your profile and click settings.
+ After clicking on settings you will see a list of option on the left side, click on the one that says **Access Tokens**.
+ Then click **Create new token**.
+ Set the token type to **READ**, give it a name and click create.
+ You will be given an access toke looking like something like this **(hf_wIvGjlwNyrhJHuGFOHbgbfB)**.
+ Copy the token you are given and save it somewhere on like a notepad.

>[!NOTE]
>The hugging face access token is important make sure not to share it with anyone and keep it safe, it will be required down the line in the following steps to come.

+ Head over to https://www.cloudflare.com/ and create a free account, you should be taken to your dashboard if you are done with the sign up process.
+ At the left side you will see something called **Compute and Ai**, the a bunch of options should show then look for **Workers and Page** and click it.
+ At the buttom right you will see something that says **account ID** copy and save.
+ At the top right conner, you should see a profile button, click it and select profile.
+ Then at the left hand side you will see a section called **API Tokens**, click it.
+ Click on **Create Token**, You will be taken to a new page, you will see something called **API token templates**, then click on **Use template** for **Worker AI** (5th option).
+ Don't do anything just scroll down till you see **Account Resources**, you will see two boxes next to each other, the left says *'include'* and the right says *'select...'*.
+ Click on select and a drop down menu will appear and select you account *(you will see the email you registed with click that)*.
+ Scroll down and click **Continue to summary**, then you will be taken to another page, there click on create token.
+ You will be take to a page showing you the API key, copy it and keep it somewhere save **(Key looks like a compination of random letters and numbers)**.
+ Now go to https://console.cloud.google.com/ and create an account.
+ Create a new poject and give it name, tho the welcome screen should say you are working on one called **my first project** but if you want to create a new one, at the top click on something that says **My first project** then a small box should appear, at the top right of said box you will see a blue higlited text that says **Create project**. Click it and give it a name and create.
+ You should be greeted with a welcome screen, look for **API and services** and then click it.
+ At the right side you should see **Library** click that and search for **YouTube Data API v3**, once you get the result click it and then you will see an **enable** button, click enable.
+ Now go back to the **API and services** page and on the right side click on **OAuth Consent Screen**
+ In the overview part click on get started and then start to file. In the app information give the app a name eg(testing) and selected your email.
+ Then you will move to Audience, select external. Then you move to contact info, fill with your email address, Then in the finish section select you agree and click **continue** and the **Create**.
+ On the right side of the screen where you have, *Overview, Branding, Audience etc.*, click on **Audience** and scroll down to **Test Users**, click on add users, add your email address and the email you plan to use for your Youtube channel if by chance they are not the same.
+ Check Filter below add user to see if the email is already added.
+ Go back to the **API and services** page and click on **Credentials** (At the right side).
+ Click on **Create Credentials**, you will see some options pick **OAuth client ID**
+ Make the Application type a desktop app and click create.
+ You will be greated with a mini screen, scroll down and click on the **download JSON**
+ Now you have a .JSON file named (client_secret...).

>[!IMPORTANT]
>Technically you should have 3 keys and one JSON file, one form HUGGING face and two from CLOUDFLARE and one from goggle. Make sure you keep them save cause we will be using them soon.


## Step 2 GETTING PICKLE STRING
+ Open the root project folder in your computer text editor (VS Code recommended).
+ Add the JSON file you downloaded inside the root folder.
+ Rename the JSON file to **client_secret.json**.
+ Create a virtual environment *(If you don't know how search how to create a virtual environment and activate it in VS code).
+ Open vs code terminal and run:
```python
pip install -r requirements.txt
```
+ After it done, run:
```python
python get_pickle.py
```
+ Wait a while amd you will see a file in your project dir that has been created called **token.pickle**
+ In your terminal run:
```python
python get_pickle_string.py
```
+ Copy the long text it shows on the terminal and save it somewhere safe.
>[!WARNING]
>DO NOT ATEMPT TO RUN ANY OTHER FILE EXCEPT THE ONE YOU WERE TOLD TO RUN IN STEP 2.

## Step 3 RUNNING ON GITHUB
+ Create a private github repo and give it a name *(Remember not to check the add README, just create a blank repo)*.
+ On VS code push the project dir to the repo *(If you dont know how look it up)*
+ After pushing go to Github and go to repo settings not account settings Repo settings (You will find it wher you have code, actions, insight etc. This is if you are on desktop).
+ Scroll down to **Secrets and variable** and click **Actions**.
+ Scroll down and create **new repository secrets**.
+ You will need to create 4 secrets if you plan to run for youtube only but 6 if facebook is added to the mix.
+ Here are what you should create:
+ | Tables   |      Are      |
|----------|:-------------:|
| col 1 is |  left-aligned |
| col 2 is |    centered   |
| col 3 is | right-aligned |