import csv
import math
from collections import Counter
import re
from collections import defaultdict

def clean_list(oldlist):
    newlist=[]
    finallist=[]
    for each_symp in oldlist:
        
        if re.search('\s*;\s*',each_symp)== None: #if no ; in term, append to newlist
            cleanedterm=each_symp.strip() #white space cleaner
            newlist.append(cleanedterm) #add term to a new list
        else:  #if finds ; in term
            for term in each_symp.split(';'): #for each term resulting in the split 
                newlist.append(term.strip()) #add term to the same new list
                
    for term in newlist: #for each term in the new list

        if re.search('\(|\d',term): #if find ( or a number (some terms did not have paranthesis before number)
            reg = re.match('(\w+)',term) #store the return of the match function on term (match the first occurance of word any letters)
            newterm=reg.group() #the new term is a group of the match (turns into a word basically)
        else: #if term doesnt have 
            newterm=term #set new term as unchanged term
        finallist.append(newterm) #add that term to a final list to return list back to main


    return finallist 


def main():
    #just for gathering info 
    with open('covidTrain.csv','r') as inputfile:
        tf=True
        ttf=True
        reader=csv.reader(inputfile)
        next(reader)
        dicLong = {} #province:Long
        dicLat = {} #province:Lat
        dicLongAvg = {}
        dicLatAvg = {}
        dicCity={}
        dicMostOccurCity={}
        dicsymptoms={}
        new_simp_dic={}
        dic_simpMETA={}
        
        for row in reader:
            city = row[3].strip()
            province = row[4].strip()
            latitude = row[6].strip()
            longitude = row[7].strip()
            simp = row[11].strip()
            
            
                    #for getting all lats and long stored into dictionary
            if re.search('[Nn][Aa][Na]',latitude) == None:
                try:
                    dicLat[province].append(float(latitude))
                except:
                    dicLat[province]=[float(latitude)]
            if (re.search('[Nn][Aa][Na]',longitude) == None):
                try:
                    dicLong[province].append(float(longitude))
                except:
                    dicLong[province]=[float(longitude)]
                    
                    
                #for getting all cities stored to dictionary per prov
            if re.search('[Nn][Aa][Na]',city) == None: #if not NaN
                try:
                    dicCity[province].append(city)
                except:
                    dicCity[province]=[city]
                    
                    
                #for getting all symptoms stored to dictionary per prov
            if re.search('[Nn][Aa][Na]',simp) == None: 
                try:
                    dicsymptoms[province].append(simp) 

                except:
                    dicsymptoms[province]=[simp]   
                    
            for prov,sympslist in dicsymptoms.items():
                new_simp_dic[prov] =  clean_list(sympslist)

            
                    
              
                
                
                    #for average lats and longs
        for keys,values in dicLat.items():
            avg = float(sum(values))/float(len(values))
            dicLatAvg[keys]=round(avg,2)
        #print('the Latitude for',keys,'is = ', avg)
        for keys,values in dicLong.items():
            avg = float(sum(values))/float(len(values))
            dicLongAvg[keys]=round(avg,2)
        inputfile.close()
        
        
        
        
        
        
            #for most occuring citties per province
        for key,value in dicCity.items(): #for each item in dicCity
            lstofcitties = list(value) #make list of all the values (cities) 

            if len(lstofcitties)==1: #if length of value list is 1, that mean only one city
                dicMostOccurCity[key]=lstofcitties[0]#add to dicMostOccurCity
            else: #if more than one ciity in list
                counter = Counter(lstofcitties)  #counter for each city in list
                counterdic={} #will save city:count in this dic

                for city,count in counter.items(): #for each item in counter methoddic
                    counterdic[city]=count #add city mapped to count in this dictionary so we can get values. (cannot get values direclty from Counter

    #now that all cities are mapped to a number of occurances 
                cities_with_same_count = [x for x in counterdic.keys() if counterdic.get(x)==max(list(counterdic.values())) ]
    #this list has x(city) if city counter is equal to max of the all occurance numbers from counterdic


                if len(cities_with_same_count) ==1: #if number of values in our newlist if 1, menaing only one element had the max number of occurances
                    dicMostOccurCity[key]=cities_with_same_count[0] #add it to new dic
                else: #if multiple cities have max count
                    alphasortlist = sorted(cities_with_same_count) #sort alphabetically
                    dicMostOccurCity[key]=alphasortlist[0] #add first item to dicMostOccurCity


            #making final province to symptom dic
        for prov,newlist in new_simp_dic.items():
            if len(set(list(newlist))) == 1: #if one term in list
                dic_simpMETA[prov]=str(newlist[0])
            else:
            
                counter = Counter(newlist) #counter dic mapping each symptom in list to occur
                Counterdic={}
            for symp,count in counter.items():
                Counterdic[symp]=count
                symp_same_count=[x for x in Counterdic.keys() if Counterdic.get(x) == max(list(Counterdic.values()))]            
            if len(symp_same_count)==1:
                dic_simpMETA[prov]=str(symp_same_count[0])
                
                
            else:
                dic_simpMETA[prov] = str(sorted(symp_same_count)[0])
                

            

        
        

    with open('covidResult.csv','w',newline='') as outputfile:
        with open('covidTrain.csv','r') as inputfile:
            reader = csv.reader(inputfile)
            writer = csv.writer(outputfile)
            header = next(reader)
            writer.writerow(header)
            
            
            
            for row in reader:
                data=row.copy()
                age=row[1].strip()
                city = row[3].strip()
                province = row[4].strip()
                latitude = row[6].strip()
                longitude = row[7].strip()
                symptoms = row[8].strip()
                hospital = row[9].strip()
                confirmation = row[10].strip()
                simp = row[11].strip()
                
                #question1
                if (re.search('-', age)!= None): #if range exists 
                    subage = row[1].split('-')
                    avgage = round((float(subage[1])+float(subage[0]))/2)
                    subage = avgage
                    data[1]=str(avgage)

                    
                    
                #question2
                sday,smonth,syear = symptoms.split('.')
                hday,hmonth,hyear = hospital.split('.')
                cday,cmonth,cyear = confirmation.split('.')
                data[8] = str(smonth + "." + sday + "." + syear)
                data[9] = str(hmonth + "." + hday + "." + hyear)
                data[10] = str(cmonth + "." + cday + "." + cyear)
                
                
                #question3
                if (re.search('[Nn][Aa][Na]',latitude) != None): #means none value is present
                    latitude = dicLatAvg.get(province) 
                    data[6] = str(latitude)
                if (re.search('[Nn][Aa][Na]',longitude) != None):
                    longitude = dicLongAvg.get(province)
                    data[7] = str(longitude)
                
                #question4
                #Fill in the missing “city” values by the most occurring city value in that province.
                #In case of a tie, use the city that appears first in alphabetical order.
                if (re.search('[Nn][Aa][Na]',city) != None): #means none value is present
                    city = dicMostOccurCity.get(province)
                    data[3] = str(city)

                #question5
                #Fill in the missing "symptom" values by the single most frequent symptom
                #in the province where the case was recorded. 
                #In case of a tie, use the symptom that appears first in alphabetical order.
                if (re.search('[Nn][Aa][Na]',simp) != None): #means none value is present
                    simp = dic_simpMETA.get(province) 
                    data[11] = str(simp)
                    
                    
                
                
                writer.writerow(data)
                
        outputfile.close()
        inputfile.close()
if __name__ == "__main__":
    main()