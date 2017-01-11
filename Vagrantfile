 

# Only change these if possible:
INSTANCE_NAME     = "zanthia"
INSTANCE_HOSTNAME = "zanthia.local"
INSTANCE_MEM      = "1024"
INSTANCE_CPUS     = "2"
INSTANCE_IP       = "192.168.123.123"
ANSIBLE_INVENTORY = "ansible/inventory"

dir = File.dirname(__FILE__) + '/'

# Write the inventory file for ansible
FileUtils.mkdir_p dir + ANSIBLE_INVENTORY
File.open(dir + ANSIBLE_INVENTORY + "/hosts", 'w') { |file| file.write("[vagrant]\n" + INSTANCE_IP) }

# And never anything below this line
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

	########################################
	# Default configuration
	########################################

	config.vm.hostname = INSTANCE_HOSTNAME
	config.vm.box      = "debian/jessie64"

	config.vm.network :private_network, ip: INSTANCE_IP

	# Sync folders
	config.vm.synced_folder ".", "/vagrant", type: :nfs
	# config.vm.synced_folder "~/.ssh", "/home/vagrant/.ssh_host", type: :nfs

	# Vagrant cachier
	if Vagrant.has_plugin?("vagrant-cachier")
		config.cache.scope = :box
		config.cache.synced_folder_opts = {type: :nfs}
	end

	########################################
	# Configuration for virtualbox
	########################################

	config.vm.provider :virtualbox do |vb|
		vb.name = INSTANCE_NAME
		vb.customize ["modifyvm", :id, "--memory", INSTANCE_MEM, "--cpus", INSTANCE_CPUS, "--ioapic", "on", "--rtcuseutc", "on", "--natdnshostresolver1", "on"]
	end

	########################################
	# Configuration for vmware_fusion
	########################################

	config.vm.provider "vmware_fusion" do |vb|
		vb.name = INSTANCE_NAME
		vb.vmx["memsize"]  = INSTANCE_MEM
		vb.vmx["numvcpus"] = INSTANCE_CPUS
	end

	########################################
	# Provisioning
	########################################

	config.vm.provision "ansible" do |ansible|
		#ansible.verbose = "vvvv"
		ansible.inventory_path = ANSIBLE_INVENTORY
		#ansible.extra_vars = "ansible/vagrant.yml"
		ansible.playbook = "ansible/site.yml"
		ansible.limit = "all"
		# ansible.raw_arguments = "--check"
	end



end
