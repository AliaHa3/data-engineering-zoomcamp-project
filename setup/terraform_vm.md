## Terraform Infra Setup


# Install Terraform

```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform
```

# Make sure you have alreadey cloneed the repository in your local machine.

```bash
cd data-engineering-zoomcamp-project/terraform
```

# Spin up the Infra -

- Initiate terraform and download the required dependencies-

  ```bash
  terraform init
  ```

- View the Terraform plan

  You will be asked to enter the GCP Project ID. Use the same values throughout the project. 

  ```bash
  terraform plan
  ```

- Terraform plan should show the creation of following services

- Apply the infra. **Note** - Billing will start as soon as the apply is complete.

  ```bash
  terraform apply
  ```

- Once you are done with the project. Teardown the infra using-

  ```bash
  terraform destroy
  ```