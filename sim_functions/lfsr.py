def lfsr_fun(usr_S0):
    ini_string = usr_S0
    scale = 16
  
    # Code to convert hex to binary 
    res = bin(int(ini_string, scale)).zfill(8) 
    res = res[2:] 
    list(res)
    #reverse string
    stringlength=len(res) # calculate length of the list
    res_reversed=res[stringlength::-1] # slicing 
    res = res_reversed
    #declare an array to keep all the randomized bytes
    lfsr_arr = [0] * 260
    for i in range (0,259):

        Temp_res = [0,0,0,0,0,0,0,0]
        TempS = res[7]
        Temp_res[7]= res[6]
        Temp_res[6]= res[5]
        Temp_res[5]= res[4]
        Temp_res[4]= str(int(TempS)^int(res[3]))
        Temp_res[3]= str(int(TempS)^int(res[2]))
        Temp_res[2]= str(int(TempS)^int(res[1]))
        Temp_res[1]= res[0]
        Temp_res[0]=TempS
        #convert to a string 
        s_string = "" 
        # traverse in the string  
        for x in Temp_res: 
            s_string += x 
        lfsr_arr[i] = s_string
        res = s_string
    return lfsr_arr
