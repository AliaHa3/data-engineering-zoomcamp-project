

# Setup SSH to VM
---
In your terminal run the command<br>
```ssh-keygen -t rsa -f ~/.ssh/<whatever you want to call your key> -C <the username that you want on your VM> -b 2048```
<br>
ex:
```ssh-keygen -t rsa -f ~/.ssh/gcp -C john -b 2048```

Once the command runs succesfully cd to the .ssh directory. Cat the contents of the <whatever you called your key>.pub. Copy the output to your clipboard.

In GCP click the hamburger icon again and scroll down to select Metadata
![Metadata](https://user-images.githubusercontent.com/7443591/160304715-63365049-f62c-4ad0-beef-48571a2abfb5.png)<br>
  
Select SSH Key and then click ADD SSH KEY.
![SelectAddSSHKey](https://user-images.githubusercontent.com/7443591/160304738-c1859228-b734-49eb-a68c-a0c7b1fd21b5.png)<br>
  
Paste the public key you copied into the blank provided and then click save.
![SSH_PasteAndSave](https://user-images.githubusercontent.com/7443591/160304842-5f4a2d15-51fc-48e3-92dc-1ae49b8ec3c2.png)

Go to the VM, check the check box and press start if it's not already running. Copy the External IP address that is displayed once it starts. You can then create a config file in your .ssh directory and add the following entry:<br>


![StartVMExternalIP](https://user-images.githubusercontent.com/7443591/160305325-562a85f4-a079-424a-99d9-2f716cb7ca41.png)

  
```
  Host <name to use when connecting
    HostName <public IP address>
    User <User name you chose when running the ssh-keygen command>
    IdentityFile /home/<local user name>/.ssh/<your private key>
```

# Connecting and setting up
---
Install Visual Studio Code if you don't have it already. Search Extensions for SSH and install Remote-SSH from Microsoft.
  
![InstallSSHExtension](https://user-images.githubusercontent.com/7443591/160305404-99508aa5-82fd-46a1-9e09-c1061a5f378d.png)<br>
  
  
Then in the lower left hand corner click the green icon to Open a Remote Window.
![OpenARemoteWindow](https://user-images.githubusercontent.com/7443591/160305492-d771aee3-3c50-4790-b9e1-e9f0a89109ad.png)<br>
  

Then at the top choose Connect to Host and choose the name you gave the VM in the config file. Just click continue if it prompts you.
![ConnectToHost](https://user-images.githubusercontent.com/7443591/160305604-eeef8024-b846-46f9-8cd0-ee4eb394d9be.png)<br>
  

# GCP SDK credentials

Create a folder `.google/credentials` under the `${HOME}`directory and upload the json file with the credentials generated through Google Cloud when creating the service account.  
If you use Visual Studio Code, just drag and drop the file.  
Example: `${HOME}/.google/credentials/google_credentials.json`  
```
  ${HOME}/.google/credentials/google_credentials.json
```

# Activate google cloud library

```
  export GOOGLE_APPLICATION_CREDENTIALS=~/.google/credentials/google_credentials.json
  gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```
