from tkinter import Tk, Label, Toplevel, Entry, END, BOTH
from tkinter import ttk
from datetime import datetime
from datetime import date


root = Tk()
root.title('Data about people')
root.geometry('800x600+330+100')


def add_person():
    add_root = Toplevel()
    add_root.title('Data entry')
    add_root.geometry('500x300+480+250')

    label_full_name = Label(add_root, text='Enter full name')
    label_full_name.pack()
    entry_surname = Entry(add_root)
    entry_surname.pack()
    entry_name = Entry(add_root)
    entry_name.pack()
    entry_patronymic = Entry(add_root)
    entry_patronymic.pack()

    label_birth_date = Label(add_root, text='Enter date of birth')
    label_birth_date.pack()
    entry_birth_date = Entry(add_root)
    entry_birth_date.pack()

    label_death_date = Label(add_root, text='Enter the date of death')
    label_death_date.pack()
    entry_death_date = Entry(add_root)
    entry_death_date.pack()

    label_gender = Label(add_root, text='Select gender')
    label_gender.pack()
    gender_list = ['male', 'female']
    combobox = ttk.Combobox(add_root, values=gender_list, state='readonly')
    combobox.pack()

    def add_data():

        new_birth_date = None
        new_death_date = None
        date_formats = ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%d %m %Y']
        for format in date_formats:
            try:
                change_birth_date = datetime.strptime(entry_birth_date.get(),
                                                      format)
                new_birth_date = datetime.strftime(change_birth_date,
                                                   '%d.%m.%Y')
                change_death_date = datetime.strptime(entry_death_date.get(),
                                                      format)
                new_death_date = datetime.strftime(change_death_date,
                                                   '%d.%m.%Y')
                break
            except ValueError:
                pass

        surname = entry_surname.get()
        name = entry_name.get()
        patronymic = entry_patronymic.get()
        birth_date = new_birth_date
        death_date = new_death_date if new_death_date is not None else ''
        gender = combobox.get()

        def count_age():
            if death_date != '':
                age_of_death = (change_death_date.year -
                                change_birth_date.year -
                                ((change_death_date.month,
                                  change_death_date.day) <
                                 (change_birth_date.month,
                                  change_birth_date.day)))
                return age_of_death
            else:
                today = date.today()
                age_of_alive = today.year - change_birth_date.year - (
                               (today.month, today.day) <
                               (change_birth_date.month,
                                change_birth_date.day))
                return age_of_alive

        age = count_age()

        tree.insert('', END, values=(surname, name, patronymic,
                                     birth_date, death_date, gender, age))

        gender = combobox.get()
        add_root.destroy()

    add_data_btn = ttk.Button(add_root, text='Add', command=add_data)
    add_data_btn.pack()


columns = ('surname', 'name', 'patronymic', 'birth date',
           'death date', 'gender', 'age')
tree = ttk.Treeview(columns=columns, show='headings')
tree.pack(fill=BOTH, expand=1)

tree.heading('surname', text='Surname')
tree.heading('name', text='Name')
tree.heading('patronymic', text='Patronymic')
tree.heading('birth date', text='Birth date')
tree.heading('death date', text='Death date')
tree.heading('gender', text='Gender')
tree.heading('age', text='Age')

tree.column('surname', stretch=True, width=100)
tree.column('name', stretch=True, width=100)
tree.column('patronymic', stretch=True, width=100)
tree.column('birth date', stretch=True, width=100)
tree.column('death date', stretch=True, width=100)
tree.column('gender', stretch=True, width=50)
tree.column('age', stretch=True, width=100)


def search():
    search_data = search_box.get()
    if not search_data:
        return
    found_items = 0
    for item in tree.get_children():
        values = tree.item(item, 'values')[:3]
        if any(search_data.lower() in str(value).lower() for value in values):
            tree.selection_add(item)
            found_items += 1
        else:
            tree.selection_remove(item)


add_person_btn = ttk.Button(root, text='Add data', command=add_person)
add_person_btn.pack()
search_box = ttk.Entry(root)
search_box.pack()
search_btn = ttk.Button(root, text='Search', command=search)
search_btn.pack()


root.mainloop()
