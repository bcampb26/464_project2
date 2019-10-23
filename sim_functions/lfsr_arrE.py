def lfsr_E(lfsr_arr):


    #### Creates array of 255 TVs for "E" case 
    #### each index - one TV of length 36 - 4,5 bytes, each -  msb to the right 
    lfsr_arr_E= [0]*255
    for j in range (0,255):
        s = ""
        for i in range(0,5):
            s=lfsr_arr[i+j]+s
        s = s[4:] 
        lfsr_arr_E[j]= s
    return lfsr_arr_E
