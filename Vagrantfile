# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.network "forwarded_port", guest: 3306, host: 3306
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.provision "shell", inline: $shell
end

$shell = <<-'CONTENTS'
  apt-get update
  apt install -y mysql-server
CONTENTS

###############
# Custom File #
###############

# 2018.10.24-DEA
