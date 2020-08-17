maxvalue = int(999999999)
one_19_lst=['', 'One ', 'Two ', 'Three ', 'Four ', 'Five ', 'Six ', 'Seven ', 'Eight ', 'Nine ', 'Ten ',
            'Eleven ', 'Twelve ', 'Thirteen ', 'Fourteen ', 'Fifteen ', 'Sixteen ', 'Seventeen ',
            'Nineteen ']
tens_lst=['', 'Ten ', 'Twenty ', 'Thirty ', 'Forty ', 'Fifty ','Sixty ','Seventy ', 'Eighty ', 'Ninety ']
HTMB_lst=['', 'Thousand ', 'Million ', 'Billion ', 'Trillion ', 'Quadrillion ']

number_text_out = []    #output line
OneTens1_chr = ''; Hund2_char = ''; TMB3_chr = ''   # Temp variables

print('Convert Amount in Numbers to Amount in Words')
num_inpt_fl = 0.0                                   # Numeric input
num_inpt_chr = ''                                   # Char of num input
num_inpt_fl = str(input('Number to convert xxxx.yy 930 digits max)  '))     # input number
if float(num_inpt_fl) > maxvalue + 0.99:            # Check for max size
    print('Number too large')
    sys.exit()                                      # Exit nicely if too big

split_chr = str(num_inpt_fl).split('.')             # split str of float at decimal
if len(split_chr) == 1:                             # If split == 1 then no decimal numbers
    num_inpt_rght = 0                               # Set decimal numbers to zero
else:
    num_inpt_rght = int(split_chr[1])               # Fraction as number
    num_inpt_rght_chr = str(split_chr[1])           # Fraction as character

if num_inpt_rght <= 0:                              # If decimal is 0, then char = 'no'
    num_inpt_rght_chr = ' NO'                       # No cents condition

num_inpt_left = int(split_chr[0])                   # Integer part as number
num_inpt_left_chr = str(split_chr[0])               # Integer as character
num_inpt_len = len(num_inpt_left_chr)               # lenght of left side
setsof3_int = int(num_inpt_len/3)                   # Sets of 3 = number setsof3
remain = int(len(str(num_inpt_left))) % 3           # Odd left numbers 0, 1, 2
if remain >0:
    setsof3_int += 1                                # 1 more loop for odd left numbs
    for y in range(0,3-remain):                     # pad inputs to mult of 3
        num_inpt_left_chr = '0' + num_inpt_left_chr

HTMB_lst_int = setsof3_int-1                        # Thou, Mil, Bill ... counter

## Main
for x in range(0, num_inpt_len, 3):                 # From 0 to num len by groups of 3
    if int(num_inpt_left_chr[x]) <= 0:              # if hundreds is 0, skip
        None                                        # No output
    else:
        number_text_out.append(one_19_lst[int(num_inpt_left_chr[x])] + ' Hundred ')

    tmp = num_inpt_left_chr[x+1:x+3]                # Get the 10s and 1's digits
    if int(tmp) <= 0:                               # if xx = 0, skip
        None                                        # no output
    else:
        if int(tmp) <= 19:                          # if xx in range 0-19
            number_text_out.append(one_19_lst[int(tmp)])    # Append value to output
        else:
            number_text_out.append(tens_lst[int(tmp[0])])   # Else if >19 use both digits
            number_text_out.append(one_19_lst[int(tmp[1])]) # To create number

    number_text_out.append(HTMB_lst[HTMB_lst_int])          # add TMB to output
    HTMB_lst_int -= 1                                       # decrement TMB

print(*number_text_out, sep='', end='');
#print('Dollars &, num_inpt_rght_chr, end='')
























