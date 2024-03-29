from private.menu import Menu
from private.controller import Controller

menu = Menu(2201861, "Zachary Leong", 2214241, "Ethan Pang", "DAAA/2B/01")
controller = Controller()


def main():
    menu.add(controller.assign, 1, "Add/Modify assignment statement")
    menu.add(controller.display, 2, "Display current assignment statement")
    menu.add(controller.evaluate, 3, "Evaluate a single variable")
    menu.add(controller.read_file, 4, "Read assignment statement from file")
    menu.add(controller.sort_file, 5, "Sort assignment statement")
    menu.add(controller.option1, 6, "Save,Load,Delete")
    menu.add(controller.option2, 7, "Search by value")
    menu.add(controller.option3, 8, "Graphical Plotter")
    menu.add(controller.option4, 9, "Simplifier")
    menu.add(menu.exit_menu, 10, "Exit")
    menu.intro()


if __name__ == "__main__":
    main()