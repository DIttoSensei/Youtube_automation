# Introduction
This is a tool capable of creating video ideas, from the scripts, to audio to video then subtitles and merge it all in one to post to your Youtube and Facebook page.

>[!NOTE]
>Follow the steps given with upmost precision.

>[!WARNING]
>I am not responsible for the misuse of this tool and it is only intended for educational purposes to showcase the pipeline process of how automation meets API.

## Step 1
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

>[!IMPORTANT]
>Technically you should have 3 keys, one form HUGGING face and two from CLOUDFLARE. MAke sure you keep them save cause we will dive deeper soon.


## Step 2
+ Open the root project folder in your computer text editor (VS Code recommended).
+ 