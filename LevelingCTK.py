import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.minsize(540, 320)
        self.maxsize(540, 320)
        self.title("LEVEL UP")


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill='both')


class HeadFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        self.columnconfigure((0, 1, 2), weight=1)

        self.number_dropdown = ctk.CTkOptionMenu(self,
                                                 values=['1', '5', '10'],
                                                 anchor='center',
                                                 width=70,
                                                 font=('Arial', 20))

        self.level_label = ctk.CTkLabel(self, width=380, anchor='w', font=('Arial', 20))
        self.experience_label = ctk.CTkLabel(self, width=380, anchor='w', font=('Arial', 20))

        self.level_label.grid(row=1, column=0, padx=5)
        self.experience_label.grid(row=2, column=0, padx=5, pady=5)
        self.number_dropdown.grid(row=2, column=2, sticky='e', padx=5)


class BodyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=520, fg_color='#2c2a28')
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.place(in_=master, x=0, y=110)


class Levelling:
    xp_multiplier = 1

    def __init__(self, level):
        self.level = level
        self.xp_required = 0
        self.xp_level()

    def xp_level(self):
        if self.level < 5:
            self.xp_required += 150
        elif 5 <= self.level < 10:
            self.xp_required += 550
        elif 10 <= self.level < 15:
            self.xp_required += 1100
        elif 15 <= self.level < 20:
            self.xp_required += 1650

    @staticmethod
    def multiplier():
        if 5 <= player.level < 10:
            Levelling.xp_multiplier = 2
        elif 10 <= player.level < 15:
            Levelling.xp_multiplier = 4
        elif 15 <= player.level < 20:
            Levelling.xp_multiplier = 6
        return Levelling.xp_multiplier


class Player:
    def __init__(self, level, xp_gained, xp_needed, del_money, ama_money):
        self.level = level
        self.xp_gained = xp_gained
        self.xp_needed = xp_needed
        self.del_money = del_money
        self.ama_money = ama_money

        head.level_label.configure(text=f'Level {self.level}')
        head.experience_label.configure(text=f'{self.xp_gained} / {self.xp_needed} XP')

    def rewards(self):
        for r_key, r_val in rewards.items():
            if self.level == r_key:
                return [r_val.game_time, r_val.del_mon, r_val.ama_mon]

    def level_up(self):
        for num in range(1, 50):
            levels2 = {
                num: Levelling(num + 1)
            }
            for k, v in levels2.items():
                if self.level == k:
                    if self.xp_gained >= self.xp_needed:
                        self.level = v.level
                        self.xp_needed += v.xp_required
                        self.del_money += self.rewards()[1]
                        self.ama_money += self.rewards()[2]
                        head.level_label.configure(text=f'Level {self.level}')
                        head.experience_label.configure(text=f'{self.xp_gained} / {self.xp_needed} XP')


class Item:
    def __init__(self, task_name, task_xp):
        self.task_name = task_name
        self.task_xp = task_xp
        self.counter = 0

        self.counter_label = None
        self.item_label = None
        self.exp_worth_label = None
        self.minus_button = None
        self.plus_button = None

    # stop xp from decreasing more than current xp
    def minus(self):
        as_num = int(head.number_dropdown.get())

        if self.counter >= as_num:
            self.counter -= as_num
            player.xp_gained -= (self.task_xp * as_num) * Levelling.multiplier()
        elif as_num > self.counter:
            remain = self.counter
            self.counter -= remain
            player.xp_gained -= (self.task_xp * remain) * Levelling.multiplier()

        self.counter_label.configure(text=self.counter)
        head.experience_label.configure(text=f'{player.xp_gained} / {player.xp_needed} XP')

    def plus(self):
        as_num = int(head.number_dropdown.get())
        self.counter += as_num

        player.xp_gained += (self.task_xp * as_num) * Levelling.multiplier()
        self.counter_label.configure(text=self.counter)
        head.experience_label.configure(text=f'{player.xp_gained} / {player.xp_needed} XP')
        player.level_up()

    def create_widgets(self, row):
        self.item_label = ctk.CTkLabel(body, text=self.task_name, width=200, height=10, anchor='center', wraplength=200,
                                       font=('Arial', 20))
        self.exp_worth_label = ctk.CTkLabel(body, text=self.task_xp, width=10, anchor='w', font=('Arial', 20))
        self.counter_label = ctk.CTkLabel(body, text=self.counter, width=10, height=10, anchor='w', font=('Arial', 20))
        self.minus_button = ctk.CTkButton(body, text='-', width=50, command=self.minus, font=('Arial', 20))
        self.plus_button = ctk.CTkButton(body, text='+', width=50, command=self.plus, font=('Arial', 20))

        self.item_label.grid(row=row, column=0)
        self.exp_worth_label.grid(row=row, column=1)
        self.minus_button.grid(row=row, column=2)
        self.counter_label.grid(row=row, column=3)
        self.plus_button.grid(row=row, column=4)


class Achievements:
    def __init__(self, phrase, reward):
        self.phrase = phrase
        self.reward = reward


class Rewards:
    def __init__(self, game_time, del_mon, ama_mon):
        self.game_time = game_time
        self.del_mon = del_mon
        self.ama_mon = ama_mon

    def display(self):
        first = f'Deliveroo: £{self.del_mon}'
        second = f'Amazon: £{self.ama_mon}'
        both = f'Deliveroo: £{self.del_mon}\nAmazon: £{self.ama_mon}'

        if self.del_mon != 0 and self.ama_mon != 0:
            return both
        elif self.del_mon != 0:
            return first
        elif self.ama_mon != 0:
            return second


if __name__ == '__main__':
    app = App()
    main = MainFrame(app)
    head = HeadFrame(main)
    body = BodyFrame(main)

    item_list = [
        Item('Per Dish', 1),
        Item('Make Bed', 1),
        Item('Open Curtains (Per 3)', 3),
        Item('Make Meal', 10),
        Item('Laundry (IN)', 15),
        Item('Laundry (HANG)', 15),
        Item('Laundry (AWAY)', 15),
        Item('Remove Rubbish', 15),
        Item('Hoover Per Room', 15),
        Item('Remove Recycling', 15),
        Item('Brush Teeth', 25),
        Item('Strength (5 reps)', 25),
        Item('Cardio (1 min)', 40),
        Item('Shower', 50),
        Item('Go Shop', 50),
        Item('Upload to GitHub', 100),
        Item("1 Minute Gaming Before 6pm", -1),
        Item("Ordering Simple Things", -10),
        Item("Eating Junk Food", -10),
        Item("Ordering Takeaways", -20),
        Item("Eating After 6pm", -20),
    ]

    rewards = {
        2: Rewards(1, 1, 0),
        3: Rewards(1, 0, 1),
        4: Rewards(1, 1, 0),
        5: Rewards(2, 1, 1),
        6: Rewards(1, 1, 0),
        7: Rewards(1, 0, 1),
        8: Rewards(1, 1, 0),
        9: Rewards(1, 0, 1),
        10: Rewards(2, 2, 2),
    }

    achievements = [
        Achievements('clean 10 dishes', 1),
        Achievements('clean 100 dishes', 10),
        Achievements('clean 1000 dishes', 100),
        Achievements('make bed 10 times', 1),
        Achievements('make bed 100 times', 10),
        Achievements('make bed 1000 times', 100),
        Achievements('open curtains 10 times', 100),
        Achievements('open curtains 100 times', 100),
        Achievements('open curtains 1000 times', 100),
    ]

    player = Player(1, 0, 75, 0, 0)

    for i in range(len(item_list)):
        item_list[i].create_widgets(i)

    app.mainloop()
