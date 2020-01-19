import ArduinoFunctions


# *** weather station data handling
def weatherData():
    
    if(name1=="Moteino"):
            BATst = ArduinoFunctions.getBatStatus(data1[6])
            hum = ArduinoFunctions.data1[1]                             #humidity
            photoresistor = data1[7]                                    #photoresistor
            rainy = ArduinoFunctions.getRainVolume(data1[2])            #precipitation
            temp = ArduinoFunctions.data1[0]                            #temperature
            precipitation = ArduinoFunctions.getSnow(data1[5])          #snow fall
            windD = ArduinoFunctions.getWindDirection(data1[4])         #wind direction
            windSpeed = ArduinoFunctions.getWindSpeed(data1[3])         #wind speed
        
            windy = (windD,windSpeed,"mi/hr")                           #format for wind output

    elif(name2=="Moteino"):
            BATst = ArduinoFunctions.getBatStatus(data2[6]) 
            hum = ArduinoFunctions.data2[1]                             #humidity
            photoresistor = data2[7]                                    #photoresistor
            rainy = ArduinoFunctions.getRainVolume(data2[2])            #precipitation
            temp = ArduinoFunctions.data2[0]                            #temperature
            precipitation = ArduinoFunctions.getSnow(data2[5])          #snow fall
            windD = ArduinoFunctions.getWindDirection(data2[4])         #wind direction
            windSpeed = ArduinoFunctions.getWindSpeed(data2[3])         #wind speed
        
            windy = (windD,windSpeed,"mi/hr")                           #format for wind output