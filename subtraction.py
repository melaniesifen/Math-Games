from tkinter import *
import tkinter.messagebox
from random import choice

end_results = []

def play(frame, correct = 0):
    global num_correct
    num_correct = correct
    if num_correct < 10:
        numbers = get_nums()
        display_nums(frame, numbers)
        answer_box(frame, numbers)
    
# get numbers to add
def get_nums(amount = 2):
    nums = [i for i in range(11)]
    choices = [choice(nums) for i in range(amount)]
    return sorted(choices)[::-1]

def display_nums(frame, nums):
    x = 0.38
    for i in range(len(nums)): # default is 2
        name = str(i)
        frame.name = Label(frame, text=" " + str(nums[i]) + " ", font=("Courier", 50)).place(relx=x, rely=0.25, anchor=CENTER)
        if i != len(nums) - 1:
            plus = Label(frame, text=" - ", font=("Courier", 50)).place(relx=x+0.1, rely=0.25, anchor=CENTER)
        x += 0.2

def answer_box(frame, nums, repeat = 0):
    ans_label = Label(frame, text="Answer: ", font=("Courier", 30), bg=g_color).place(relx=0.3, rely=0.5, anchor=CENTER)
    ans_text = Text(frame, height=1, width=30, bd=2)
    ans_text.place(relx=0.5, rely=0.5, anchor=CENTER)
    enter_bn = Button(frame, text="Go!", font=("Courier", 15), bg='Red', command=lambda:check_ans(frame, nums, ans_text, repeat))
    enter_bn.place(relx=0.68, rely=0.5, anchor=CENTER)
    gui.bind('<Return>', lambda event:check_ans(frame, nums, ans_text, repeat))
    
def dot_picture(frame, nums):
    y = 0.38
    for i in range(len(nums)): # default is 2
        num_dots = nums[i]
        dot_str = str(nums[i]) + "\t" + " ".join("." for j in range(num_dots))
        frame.dots = Label(frame, text=dot_str, font=("Courier", 15), bg=g_color).place(relx=0.38, rely=y, anchor='w')
        y += 0.05

def diff(num_list):
    total = num_list[0]
    for num in num_list[1:]:
        total -= num
    return total

def check_ans(frame, nums, ans_text, repeat_num):
    global num_correct
    inp = ans_text.get("1.0",END).strip()
    correct_ans = diff(nums)
    if not inp.isdigit():
        tkinter.messagebox.showinfo("", "Enter a number")
        answer_box(frame, nums, repeat = repeat_num)
        return
    elif int(inp) != correct_ans:
        nums_str = " - ".join(str(num) for num in nums)
        if repeat_num == 0:
            repeat_num += 1
            try_again_label = Label(frame, text='Try again', fg='Red', bg=g_color, font=("Courier", 30)).place(relx=0.5, rely=0.6, anchor=CENTER)
            count_dots_instructions_label = Label(frame, text='Count the dots without a pair', bg=g_color, fg="Red", font=("Courier", 30)).place(relx=0.5, rely=0.7, anchor=CENTER)
            dot_picture(frame, nums)
            answer_box(frame, nums, repeat = repeat_num)
            return
        else:
            clear_frame(frame)
            end_results.append(nums)
            correct = Label(frame, text='No', fg='Red', bg=g_color, font=("Courier", 200)).place(relx=0.5, rely=0.4, anchor=CENTER)
            correct_ans_label = Label(frame, text=nums_str + " = " + str(correct_ans), bg=g_color, font=("Courier", 80)).place(relx=0.5, rely=0.7, anchor=CENTER)
    else:
        clear_frame(frame)
        correct = Label(frame, text='Yes', fg='Green', bg=g_color, font=("Courier", 250)).place(relx=0.5, rely=0.5, anchor=CENTER)
        num_correct += 1
        num_correct_label = Label(frame, text=f"Correct: {num_correct}/10", font=("Courier", 30), bg=g_color).place(relx=0.5, rely=0.7, anchor=CENTER)
    if num_correct < 10:
        next_bn = Button(frame, text="Next", font=("Courier", 15), bg=g_color, command=lambda:cleanup(frame)).place(relx=0.5, rely=0.8, anchor=CENTER)
    else:
        clear_frame(frame)
        done_label = Label(frame, text="Finished!", font=("Courier", 100), bg=g_color).place(relx=0.5, rely=0.5, anchor=CENTER)
        write_to_log(end_results)
    
def cleanup(frame):
    clear_frame(frame)
    play(frame, correct = num_correct)
    
def set_background(frame, color):
    global g_color
    g_color = color
    frame.configure(bg=color)
    clear_frame(frame)
    #frame.choice_bn = Button(frame, text="Choose your color", font=("Courier", 10), command=lambda:choose_background_bn(frame)).place(relx=0.9, rely=0.05, anchor=CENTER)
    start_bn = Button(frame, text="Play!", font=("Courier", 30), command=lambda:[start_bn.destroy(), play(frame)])
    start_bn.place(relx=0.5, rely=0.5, anchor=CENTER)
    
def clear_frame(frame, keep = []):
    for widget in frame.winfo_children():
        if widget in keep:
            continue
        widget.place_forget()

def choose_background_bn(frame1):
    frame1.choice_label = Label(frame1, text="Choose your color", font=("Courier", 30)).place(relx=0.5, rely=0.25, anchor=CENTER)
    frame1.white_button = Button(frame1, text="white", font=("Courier", 15), bg='White', command=lambda:set_background(frame1, "White")).place(relx=0.3, rely=0.6, anchor=CENTER)
    frame1.pink_button = Button(frame1, text="pink", font=("Courier", 15), bg='Pink', command=lambda:set_background(frame1, "Pink")).place(relx=0.4, rely=0.6, anchor=CENTER)
    frame1.blue_button = Button(frame1, text="blue", font=("Courier", 15), bg='LightBlue', command=lambda:set_background(frame1, "LightBlue")).place(relx=0.6, rely=0.6, anchor=CENTER)
    frame1.green_button = Button(frame1, text="green", font=("Courier", 15), bg='SpringGreen3', command=lambda:set_background(frame1, "SpringGreen3")).place(relx=0.5, rely=0.6, anchor=CENTER)
    frame1.purple_button = Button(frame1, text="purple", font=("Courier", 15), bg="Orchid3", command=lambda:set_background(frame1, "Orchid3")).place(relx=0.7, rely=0.6, anchor=CENTER)
    
def write_to_log(end_results):
    if end_results:
        outf = open("addition_log.txt", "a")
        for res in end_results:
            s = " ".join(str(num) for num in res)
            outf.write(s)
            outf.write("\n")
        outf.close()  
       
def main():
    global gui
    gui = Tk(className='Addition')# set window size and color
    gui.bind('<Escape>', lambda event: gui.state('normal'))
    gui.bind('<F11>', lambda event: gui.state('zoomed'))
    gui.configure(bg='White')
    gui.geometry("1000x600")
        
    # set up game
    frame1 = Frame(gui)
    frame1.pack(side="top", expand=True, fill="both")
    
    # choose background color
    choose_background_bn(frame1) 
    
    # begin
    gui.mainloop() 
    
main()
