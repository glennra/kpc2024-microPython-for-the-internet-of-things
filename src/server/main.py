import tkinter as tk
import simplepyble

def get_ble_adapters():
    print(f"Running on {simplepyble.get_operating_system()}")

    adapters = simplepyble.Adapter.get_adapters()

    if len(adapters) == 0:
        print("No adapters found")

    for adapter in adapters:
        print(f"Adapter: {adapter.identifier()} [{adapter.address()}]")

def main():
    window = tk.Tk()
    window.mainloop()



if __name__ == "__main__":
    main()
    #get_ble_adapters()
