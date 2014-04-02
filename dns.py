import rumps
from rumps import *
import os

class DNSStatusBarApp(rumps.App):
    def __init__(self):
        super(DNSStatusBarApp, self).__init__("DNS")
        self.title = None
        self.icon = 'dns-small.png'
        self.interfaces = {}
        self.dns = 'Google'
        self.interface = self.get_active_interface()

        self.dns_list = {
            'Google': '8.8.8.8 8.8.4.4',
            'OpenDNS': '208.67.222.222 208.67.220.220',
            '(default)': 'empty'
        }

        self.build_menu()


    # Build the Menu itself
    def build_menu(self):
        self.build_interface_menu()

        menu = []

        for dns_str in self.dns_list:
            item = MenuItem(dns_str, callback=self.click_dns)
            menu.append(item)

        menu.append(None)
        menu.append({'Interfaces': self.interfaces.values() })
        menu.append(None)

        self.menu = menu

        self.set_active_interface_in_menu()
        self.set_current_dns_in_menu()

    # Create Dict for interfaces and buttons. {"Wi-Fi": menu_item}
    def build_interface_menu(self):
        interfaces = self.all_networks_services()

        for interface_str in interfaces:
            item = MenuItem(interface_str, callback=self.click_interface)
            self.interfaces[interface_str] = item

    def set_active_interface_in_menu(self):
        current_interface = self.get_active_interface()
        buttons = self.interfaces.values()

        for item in buttons:
            if item.title == current_interface:
                item._menuitem.setState_(True)
            else:
                item._menuitem.setState_(False)

    def set_current_dns_in_menu(self):
        current_dns = self.get_current_dns_for_interface(self.interface)

        for item in self.menu:
            if current_dns == item.title:
                self.menu[item]._menuitem.setState_(True)
            else:
                self.menu[item]._menuitem.setState_(False)


    # Triggers for click buttons
    def click_interface(self, sender):
        self.set_interface(sender.title)

        if self.get_current_dns_for_interface(sender.title) != self.dns:
            self.set_dns(self.dns)

        self.unset_all_interfaces_checkbox()

    def click_dns(self, sender):
        self.set_dns(sender.title)
        self.unset_all_dns_checkbox()

    # Get all available interfaces
    def all_networks_services(self):
        cmd = 'networksetup listallnetworkservices'
        tmp = os.popen(cmd).read()
        splited = tmp.split("\n")

        list = []
        for item in splited:
            if item != "" and not item.startswith("An asterisk"):
                list.append(item)

        return list

    # Unset the checkbox on all items in Main Menu
    def unset_all_interfaces_checkbox(self):
        # get the menuItems
        buttons = self.interfaces.values()

        for item in buttons:
            item._menuitem.setState_(False)

        # Check
        self.interfaces[self.interface]._menuitem.setState_(True)

    # Unset the checkbox on all items in Main Menu
    def unset_all_dns_checkbox(self):
        # Uncheck
        for item in self.menu:
            self.menu[item]._menuitem.setState_(False)

        # Check
        self.menu[self.dns]._menuitem.setState_(True)

    def set_interface(self, interface_str):
        if self.interface != interface_str:
            self.interface = interface_str

    def set_dns(self, dns_str):
        self.dns = dns_str
        os.system('networksetup -setdnsservers "'+self.interface+'" '+self.dns_list[dns_str])

    def get_current_dns_for_interface(self, interface_str):
        cmd = 'networksetup -getdnsservers "'+self.interface+'"'
        tmp = os.popen(cmd).read()
        splited = tmp.split("\n")

        list = []
        for item in splited:
            if item != "":
                list.append(item)

        return " ".join(list)

    def get_active_interface(self):
        _interface_str = None

        for interface_str in self.all_networks_services():
            cmd = 'networksetup -getinfo "'+interface_str+'"'
            tmp = os.popen(cmd).read()
            splited = tmp.split("\n")

            for item in splited:
                if item.startswith('IP address:'):
                    _interface_str = interface_str

        return _interface_str


if __name__ == "__main__":
    app = DNSStatusBarApp()
    app.run()
