import tkinter as tk
from tkinter import *;
from tkinter import ttk
from tkinter.messagebox import showinfo
from bot import Paka


def add_amount():
    values = amount.get().split(' ')
    for value in values:
        listbox.insert(END,value)
    
def remove_amount():
    selected_indices = listbox.curselection()
    for selected_index in selected_indices:
        listbox.delete(selected_index)

def start_bot():
    stakes = listbox.get(0,END)
    number = contact.get()
    passcode = password.get()
    odd = odds.get()
    wait_odds_value = wait_odds.get()
    wait_count_value = wait_count.get()

    paka = Paka(number,passcode)
    paka.login()

    # Wait for consecutive crashes below threshold before starting
    paka.wait_for_consecutive_crashes(float(wait_odds_value), int(wait_count_value))
    
    index = 0

    while True:
        stake = stakes[index]
        won = paka.bet(stake, odd)
        
        if won:
            index = 0
            # Wait for consecutive crashes again after a win
            print("🔄 Win detected! Waiting for consecutive crashes before next bet...")
            paka.wait_for_consecutive_crashes(float(wait_odds_value), int(wait_count_value))
        else:
            index += 1
            # If we've gone through all stakes, just reset to first stake and continue immediately
            if index >= len(stakes):
                index = 0
    
    

root = tk.Tk()

window_width = 500;
window_height = 600;  # Increased height for new fields

root.resizable(False,False)

root.title('PBOT')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


#STORE AMOUNT AND ODDS
amount = tk.StringVar()
odds = tk.StringVar()
contact = tk.StringVar()
password = tk.StringVar()
wait_odds = tk.StringVar()  # Store odds threshold
wait_count = tk.StringVar()  # Store consecutive count



contact_label = ttk.Label(root, text='CONTACT :')
contact_label.pack(fill='x',pady=5)
contact_entry = ttk.Entry(root, textvariable=contact)
contact_entry.pack(fill='x',pady=5)

password_label = ttk.Label(root, text='PASSWORD :')
password_label.pack(fill='x',pady=5)
password_entry = ttk.Entry(root, textvariable=password,show='*')
password_entry.pack(fill='x',pady=5)

odds_label = ttk.Label(root, text='ODDS :')
odds_label.pack(fill='x',pady=5)
odds_entry = ttk.Entry(root, textvariable=odds)
odds_entry.pack(fill='x',pady=5)

# NEW FIELD 1: Odds threshold to wait for
wait_odds_label = ttk.Label(root, text='WAIT FOR CRASHES BELOW ODDS:')
wait_odds_label.pack(fill='x',pady=5)
wait_odds_entry = ttk.Entry(root, textvariable=wait_odds)
wait_odds_entry.pack(fill='x',pady=5)

# NEW FIELD 2: Consecutive count
wait_count_label = ttk.Label(root, text='CONSECUTIVE CRASHES COUNT (Y):')
wait_count_label.pack(fill='x',pady=5)
wait_count_entry = ttk.Entry(root, textvariable=wait_count)
wait_count_entry.pack(fill='x',pady=5)

amount_label = ttk.Label(root,text='AMOUNT TO ADD:')
amount_label.pack(fill='x',pady=5)
amount_entry = ttk.Entry(root, textvariable=amount)
amount_entry.pack(fill='x',pady=5)


amounts_label = ttk.Label(root,text='AMOUNTS : ')
amounts_label.pack(fill='x',pady=5)
amounts = []
amounts_var = tk.StringVar(value=amounts)
listbox = tk.Listbox(root,listvariable=amounts_var,height=8,selectmode='extended')
listbox.pack(fill='both',expand=True)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

add_amount_btn = ttk.Button(root,text="Add Amount",command=add_amount)
remove_amount_btn = ttk.Button(root,text="Remove Amount",command=remove_amount)
bet_btn = ttk.Button(root,text="Bet",command=start_bot)

add_amount_btn.pack(ipadx=10,padx=5,side='left')
remove_amount_btn.pack(ipadx=10,padx=5,side='left')
bet_btn.pack(ipadx=10,padx=5,side='left')

root.mainloop()
