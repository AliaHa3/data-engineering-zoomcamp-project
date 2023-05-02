## Clone the repository in your local machine
---
```bash
git clone https://github.com/AliaHa3/data-engineering-zoomcamp-project.git
```

```bash
cd data-engineering-zoomcamp-project/terraform
```

## Spin up the Infra
---
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