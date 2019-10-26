def TV_A(usr_input):


    #### Creates array of 255 TVs for "C" case 
    #### each index - one TV of length 36 - 4,5 bytes, each -  msb to the right 
    TV_arr_A= [0]*255
    ctr_arr = [0]*260

    # Code to convert hex to binary 
    res = bin(int(usr_input, 16)).zfill(8) 
    res = res[2:] 
    res_int = int (res,2)
    #reverse string
    stringlength=len(res) # calculate length of the list
    res_reversed=res[stringlength::-1] # slicing 
    res = res_reversed


    ctr_arr[0] = res
    for i in range(1,260):
        res_int = res_int +1

        res_bin = bin(res_int)
        #res_bin = bin(int(res_int, 10)).zfill(8) 
        res_bin = res_bin[-8:] 
        #reverse string
        stringlength=len(res_bin) # calculate length of the list
        res_reversed=res_bin[stringlength::-1] # slicing 
        res_bin = res_reversed
        ctr_arr[i]= res_bin


    for j in range (0,255):
        s = ""
        s="0000000000000000000000000000"+ ctr_arr[j]
        TV_arr_A[j]= s
    return TV_arr_A
