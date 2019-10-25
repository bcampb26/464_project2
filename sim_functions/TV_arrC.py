def TV_C(usr_input):


    #### Creates array of 255 TVs for "C" case 
    #### each index - one TV of length 36 - 4,5 bytes, each -  msb to the right 
    TV_arr_C= [0]*255
    ctr_arr = [0]*255

    # Code to convert hex to binary 
    res = bin(int(usr_input, 16)).zfill(8) 
    res = res[2:] 
    res_int = int (res,2)

    for i in range(0,255):
        res_int = res_int +1
        res_bin = bin(res_int)
        #res_bin = bin(int(res_int, 10)).zfill(8) 
        res_bin = res_bin[2:] 
        #reverse string
        stringlength=len(res_bin) # calculate length of the list
        res_reversed=res_bin[stringlength::-1] # slicing 
        res_bin = res_reversed
        ctr_arr[i]= res_bin


    for j in range (0,255):
        s = ""
        for i in range(0,5):
            s=ctr_arr[j]+s
        s = s[4:] 
        TV_arr_C[j]= s
    return TV_arr_C
