# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"
  config.vm.box_check_update = true
  config.vm.network "private_network", ip: "192.168.33.10"

  # config.vm.synced_folder "../data", "/vagrant_data"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "1024"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y mc htop python3-pip

    wget -O /tmp/d.sh https://get.docker.com
    bash /tmp/d.sh
    adduser vagrant docker
    pip3 install docker-compose

    docker pull nginx:1.13
    docker pull postgres:10
    docker pull redis
    docker pull python:3.6
    docker pull node:
  SHELL

end
