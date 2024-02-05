class Menu:
    options = []

    def __init__(
        self,
        author_id1=int,
        author_name1=str,
        author_id2=int,
        author_name2=str,
        author_class=str,
    ):
        self.author_id1 = author_id1
        self.author_id2 = author_id2
        self.author_name1 = author_name1
        self.author_name2 = author_name2
        self.author_class = author_class
        self.width = 66

    def intro(self):
        print("*" * self.width)
        text = " ST1507 DSAA: Evaluator & Sorting Assignment Statement"
        print(f"*{text}{' ' * (self.width-len(text)-2)}*")
        print(f"*{' ' * (self.width-2)}*")
        print(f"*{' ' * (self.width-2)}*")
        text = f"    - Done by: {self.author_name1}({self.author_id1}) & {self.author_name2}({self.author_id2})"
        print(f"*{text}{' ' * (self.width-len(text)-2)}*")
        text = f"    - Class {self.author_class}"
        print(f"*{text}{' ' * (self.width-len(text)-2)}*")
        print(f"*{' ' * (self.width-2)}*")
        print("*" * self.width)
        self.select_option()

    def add(self, redirect, value, message):
        self.options.append((redirect, value, message))

    def print_menu(self):
        valid_choices = ",".join(str(i) for i in range(1, len(self.options) + 1))
        printmenu = f"\nPlease select your choice: ({valid_choices})\n\t"
        for option in self.options:
            _, value, message = option
            printmenu += f"{value}. {message}\n\t"
        print(printmenu)

    def select_option(self):
        input("Press enter key, to continue....")
        self.print_menu()
        choice = input("Enter the number of your choice: ")
        print()
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.options):
                redirect, _, _ = self.options[choice - 1]
                if callable(redirect):
                    redirect()
                else:
                    print(f"Function not callable: {redirect}")
            else:
                print("Invalid choice. Please select a valid option.")
                self.select_option()
        except ValueError:
            print("Invalid input. Please enter a number.")
            self.select_option()

    def exit_menu(self):
        print(
            "Bye, thanks for using ST1507 DSAA: Assignment Statement Evaluator & Sorter"
        )
