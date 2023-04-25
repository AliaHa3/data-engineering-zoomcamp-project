terraform {
  required_version = ">=1.0"
  backend "local" {}
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

resource "google_compute_instance" "airflow_vm_instance" {
  name                      = "earthquake-instance"
  machine_type              = "e2-standard-4"
  zone         = var.zone
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = var.vm_image
      size  = 60
    }
  }

  network_interface {
    network = var.network
    access_config {
    }
  }
}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region
  force_destroy = true
  storage_class = var.storage_class

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 # days
    }
  }
}

resource "google_storage_bucket" "data-lake-tmp-bucket" {
  name          = "${local.data_lake_bucket}_tmp_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region
  force_destroy = true
  storage_class = var.storage_class

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 # days
    }
  }
}


resource "google_bigquery_dataset" "stg_dataset" {
  dataset_id                 = var.stg_bq_dataset
  project                    = var.project
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "prod_dataset" {
  dataset_id                 = var.prod_bq_dataset
  project                    = var.project
  location                   = var.region
  delete_contents_on_destroy = true
}
