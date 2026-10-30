terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

resource "local_file" "hello" {
  filename = "/tmp/hello.txt"
  content  = "Hello, Terraform!"
}

