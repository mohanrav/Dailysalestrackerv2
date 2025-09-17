<<<<<<< HEAD
provider "azurerm" {
  features = {}
}

resource "azurerm_resource_group" "demo" {
  name     = "defender-demo-rg"
  location = "East US"
}

resource "azurerm_virtual_network" "demo_vnet" {
  name                = "demo-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
}

resource "azurerm_subnet" "demo_subnet" {
  name                 = "demo-subnet"
  resource_group_name  = azurerm_resource_group.demo.name
  virtual_network_name = azurerm_virtual_network.demo_vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_interface" "demo_nic" {
  name                = "demo-nic"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.demo_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.demo_pip.id
  }
}

resource "azurerm_public_ip" "demo_pip" {
  name                = "demo-pip"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  allocation_method   = "Static"
}

resource "azurerm_network_security_group" "demo_nsg" {
  name                = "demo-nsg"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name

  security_rule {
    name                       = "Allow-SSH-All"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_interface_security_group_association" "demo_nic_nsg" {
  network_interface_id      = azurerm_network_interface.demo_nic.id
  network_security_group_id = azurerm_network_security_group.demo_nsg.id
}

resource "azurerm_linux_virtual_machine" "demo_vm" {
  name                = "demo-vm"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  size                = "Standard_B1s"
  admin_username      = "azureuser"

=======
provider "azurerm" {
  features = {}
}

resource "azurerm_resource_group" "demo" {
  name     = "defender-demo-rg"
  location = "East US"
}

resource "azurerm_virtual_network" "demo_vnet" {
  name                = "demo-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
}

resource "azurerm_subnet" "demo_subnet" {
  name                 = "demo-subnet"
  resource_group_name  = azurerm_resource_group.demo.name
  virtual_network_name = azurerm_virtual_network.demo_vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_interface" "demo_nic" {
  name                = "demo-nic"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.demo_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.demo_pip.id
  }
}

resource "azurerm_public_ip" "demo_pip" {
  name                = "demo-pip"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  allocation_method   = "Static"
}

resource "azurerm_network_security_group" "demo_nsg" {
  name                = "demo-nsg"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name

  security_rule {
    name                       = "Allow-SSH-All"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_interface_security_group_association" "demo_nic_nsg" {
  network_interface_id      = azurerm_network_interface.demo_nic.id
  network_security_group_id = azurerm_network_security_group.demo_nsg.id
}

resource "azurerm_linux_virtual_machine" "demo_vm" {
  name                = "demo-vm"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  size                = "Standard_B1s"
  admin_username      = "azureuser"

>>>>>>> 6d2736c471e8a2cba069ee9b9c7e05c9108831c2
  admin_password      = "P@ssword