import vending_machine

if __name__ == "__main__":
    VM = vending_machine.VendingMachine(file='products.json')
    cli = vending_machine.CommandLineInterface(VM=VM)
    cli.run()