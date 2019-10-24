def lfsr_D(lfsr_arr):


    #### Creates array of 255 TVs for "D" case 
    #### each index - one TV of length 36 - 4,5 bytes, each -  msb to the right 
    #### every 8 bits repeat within index 
    #### next index - result of lfsr calculation 

    lfsr_arr_D= [0]*255
    for j in range (0,255):
        s = ""
        for i in range(0,5):
            s=lfsr_arr[j]+s
        s = s[4:] 
        lfsr_arr_D[j]= s
    return lfsr_arr_D
