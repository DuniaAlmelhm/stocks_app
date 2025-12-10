resource "hcloud_server" "stocks1" {
  name        = "stocks1"
  image       = "ubuntu-24.04"
  server_type = "cx23"
}