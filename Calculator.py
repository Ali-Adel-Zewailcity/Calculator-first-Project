import tkinter as tk
from PIL import Image

root = tk.Tk()
root.configure(bg="#1F1F1F")
root.title("Calculator")
root.iconbitmap("C:/Users/Lenovo/Pictures/Icons/Ico/calculator.ico")

input = tk.Entry(root, bg="#383838", fg="#FFFFFF", width=36, borderwidth=5)
input.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

global pre_calculation_num
global post_calculation_num
global result_num

def CalculatorInput(number):
    input.insert("end", int(number))

def Clear():
    input.delete(0, tk.END)

def Calculate(sign):
    sign_lists = "/*-+"
    pre_calculation_num = input.get()
    if (len(pre_calculation_num) == 0) and (sign in sign_lists):
        if sign == "-":
            input.insert("end",sign)
        else:
            return 0
    else:
        if sign == "-":
            if len(pre_calculation_num) == 0:
                input.insert("end", sign)
            elif len(pre_calculation_num) == 1 and pre_calculation_num[0] == "-":
                return 0
            elif (pre_calculation_num[-1] in sign_lists) and (pre_calculation_num[-2] not in sign_lists):
                if pre_calculation_num[-1] != "+":
                    input.insert("end",sign)
                elif pre_calculation_num[-1] == "+":
                    input.delete(len(pre_calculation_num)-1,tk.END)
                    input.insert("end",sign)
            elif (pre_calculation_num[-1] in sign_lists) and (pre_calculation_num[-2] in sign_lists):
                return 0
            elif pre_calculation_num[-1] not in sign_lists:
                condition =  any(i in pre_calculation_num for i in sign_lists)
                if condition == False:
                    if pre_calculation_num[-1] == ".":
                        input.insert("end", "0"+sign)
                    else:
                        input.insert("end", sign)
                elif condition == True:
                    sign_count = 0
                    for i in pre_calculation_num:
                        if i in sign_lists:
                            sign_count += 1
                    if sign_count == 3:
                        Equal()
                        input.insert("end", sign)
                    elif sign_count == 2:
                        Equal()
                        input.insert("end", sign)
                    elif sign_count == 1:
                        if pre_calculation_num[0] == "-":
                            if pre_calculation_num[-1] == ".":
                                input.insert("end", "0"+sign)
                            else: 
                                input.insert("end", sign)
                        elif pre_calculation_num[0] != "-":
                            Equal()
                            input.insert("end", sign)
        elif sign != ".":
            if pre_calculation_num[-1] == sign:
                return 0
            elif pre_calculation_num[-1] in sign_lists:
                if pre_calculation_num[-1] == "-" and len(pre_calculation_num) == 1:
                    return 0
                else:
                    if not(pre_calculation_num[-1] == "-" and pre_calculation_num[-2] in sign_lists):
                        pre_calculation_num = pre_calculation_num[:-1]
                        input.delete(0, tk.END)
                        input.insert("end",pre_calculation_num)
                        input.insert("end",sign)
            else:    
                condition = bool(any(item in pre_calculation_num for item in sign_lists))
                if condition == False:
                    if pre_calculation_num[-1] == ".":
                        input.insert("end","0"+sign)
                    else:
                        input.insert("end",sign)
                else:
                    if pre_calculation_num[0] == "-":
                        neg_condition = bool(any(item in pre_calculation_num[1:] for item in sign_lists))
                        if neg_condition == True:
                            Equal()
                            input.insert("end", sign)
                        else:
                            input.insert("end", sign)
                    elif pre_calculation_num[0] != "-":
                        Equal()
                        input.insert("end",sign)
        elif sign == ".":
            if len(pre_calculation_num) == 0:
                input.insert("end","0"+sign)
            elif pre_calculation_num[-1] == ".":
                return 0
            elif pre_calculation_num[-1] in sign_lists:
                input.insert("end","0"+sign)
            elif pre_calculation_num[-1] not in sign_lists:
                opp_pre_calculation_num = pre_calculation_num[-1::-1]
                dot_place = opp_pre_calculation_num.find(".")
                if dot_place == -1:
                    input.insert("end",sign)
                for i in sign_lists:
                    final_checker = False
                    Calc_sign_place = 9999
                    Calc_sign_place = opp_pre_calculation_num.find(i)
                    if (Calc_sign_place != -1) and (Calc_sign_place != 9999):
                        final_checker = True
                        break
                if final_checker != True:
                    return 0
                elif final_checker == True:
                    if dot_place < Calc_sign_place:
                        return 0
                    else:
                        input.insert("end",sign)
                    

        
def Equal():
    sign_calculation_lists = "/*+-"
    whole_number = input.get()
    if len(whole_number) == 0:
        return 0
    else:
        condition = bool(any(item in whole_number[0:-1] for item in sign_calculation_lists))
        if condition == True and whole_number[0] != "-":
            for i in sign_calculation_lists:
                Calc_type = whole_number.find(i)
                if Calc_type != -1:
                    pre_calculation_num = float(whole_number[0:Calc_type])
                    post_calculation_num = float(whole_number[Calc_type+1:])
                    sign_type = whole_number[Calc_type]
                    break
            checker = sign_calculation_lists.find(sign_type)
            if checker == 0:
                result_num = pre_calculation_num / post_calculation_num
            elif checker == 1:
                result_num = pre_calculation_num * post_calculation_num
            elif checker == 2:
                result_num = pre_calculation_num + post_calculation_num
            elif checker == 3:
                result_num = pre_calculation_num - post_calculation_num
            input.delete(0,tk.END)
            input.insert(0,result_num)
        elif whole_number[-1] in sign_calculation_lists:
            return 0
        elif condition == True and whole_number[0] == "-":
            non_neg_num = whole_number[1:]
            for i in sign_calculation_lists:
                Calc_type = non_neg_num.find(i)
                if Calc_type != -1:
                    pre_calculation_num = float(whole_number[0:Calc_type+1])
                    post_calculation_num = float(whole_number[Calc_type+2:])
                    sign_type = non_neg_num[Calc_type]
                    break
            if Calc_type != -1:
                checker = sign_calculation_lists.find(sign_type)
                if checker == 0:
                    result_num = pre_calculation_num / post_calculation_num
                elif checker == 1:
                    result_num = pre_calculation_num * post_calculation_num
                elif checker == 2:
                    result_num = pre_calculation_num + post_calculation_num
                elif checker == 3:
                    result_num = pre_calculation_num - post_calculation_num
                input.delete(0,tk.END)
                input.insert(0,result_num)
            else: 
                return 0
        else:
            return 0


def abs_button():
    whole_number = input.get()
    sign_calculation_lists = "/*-+"
    if len(whole_number) == 0:
        return 0
    elif len(whole_number) == 1 and whole_number[0] == "-":
        input.delete(0, tk.END)
    elif (len(whole_number) > 1) and (whole_number[-1] in sign_calculation_lists):
        whole_number = whole_number[:-1]
        whole_number = float(whole_number)
        if whole_number > 0 or whole_number == 0:
            return 0
        elif whole_number < 0:
            whole_number = abs(whole_number)
            input.delete(0, tk.END)
            input.insert("end", whole_number)
    elif any(i in whole_number for i in sign_calculation_lists):
        if (whole_number.find("-") == 0):
            whole_number = abs(float(whole_number))
            input.delete(0, tk.END)
            input.insert("end",whole_number)
        else:
            return 0
    else:
        return 0


# Defining Buttons
button_change_sign = tk.Button(root, text="|x|", padx=28, pady=10, bg="#35BA37", command=abs_button)
button_clear = tk.Button(root, text="C", padx=28, pady=10, bg="#35BA37", command=Clear)
button_47 = tk.Button(root, text="/", padx=28, pady=10, bg="#35BA37", command=lambda: Calculate("/"))
button_42 = tk.Button(root, text="*", padx=28, pady=10, bg="#35BA37", command=lambda: Calculate("*"))
button_7 = tk.Button(root, text=7, padx=30, pady=10, bg="#35BA37", command=lambda: CalculatorInput(7))
button_8 = tk.Button(root, text=8, padx=29, pady=10, bg="#35BA37", command=lambda: CalculatorInput(8))
button_9 = tk.Button(root, text=9, padx=27, pady=10, bg="#35BA37", command=lambda: CalculatorInput(9))
button_45 = tk.Button(root, text="-", padx=28, pady=10, bg="#35BA37", command=lambda: Calculate("-"))
button_4 = tk.Button(root, text=4, padx=30, pady=10, bg="#35BA37", command=lambda: CalculatorInput(4))
button_5 = tk.Button(root, text=5, padx=29, pady=10, bg="#35BA37", command=lambda: CalculatorInput(5))
button_6 = tk.Button(root, text=6, padx=27, pady=10, bg="#35BA37", command=lambda: CalculatorInput(6))
button_43 = tk.Button(root, text="+", padx=26, pady=10, bg="#35BA37", command=lambda: Calculate("+"))
button_1 = tk.Button(root, text=1, padx=30, pady=10, bg="#35BA37", command=lambda: CalculatorInput(1))
button_2 = tk.Button(root, text=2, padx=29, pady=10, bg="#35BA37", command=lambda: CalculatorInput(2))
button_3 = tk.Button(root, text=3, padx=27, pady=10, bg="#35BA37", command=lambda: CalculatorInput(3))
button_0 = tk.Button(root, text=0, padx=71, pady=10, bg="#35BA37", command=lambda: CalculatorInput(0))
button_46 = tk.Button(root, text=".", padx=29, pady=10, bg="#35BA37", command=lambda: Calculate("."))
button_61 = tk.Button(root, text="=", padx=24, pady=37, bg="#383838", fg="#35BA37",font="B" , command=Equal)


# Settle Buttons down
button_change_sign.grid(row=1, column=0)
button_clear.grid(row=1, column=1, pady=2)
button_47.grid(row=1, column=2, pady=2)     #/
button_42.grid(row=1, column=3, pady=2)     #*
button_7.grid(row=2, column=0, pady=2)
button_8.grid(row=2, column=1, pady=2)
button_9.grid(row=2, column=2, pady=2)
button_45.grid(row=2, column=3, pady=2)     #-
button_4.grid(row=3, column=0, pady=2)
button_5.grid(row=3, column=1, pady=2)
button_6.grid(row=3, column=2, pady=2)
button_43.grid(row=3, column=3, pady=2)     #+
button_1.grid(row=4, column=0, pady=2)
button_2.grid(row=4, column=1, pady=2)
button_3.grid(row=4, column=2, pady=2)
button_61.grid(row=4, column=3, rowspan=2, pady=2)   #=
button_0.grid(row=5, column=0, columnspan=2, pady=2)
button_46.grid(row=5, column=2, pady=2)     #.


root.mainloop()