import yaml 
import math
import numpy as np
import os



user_list = {}
arr = os.listdir("./ipl")

vec = np.zeros([0,24])
outcome = np.zeros([0,1])
inningsnum = 0

totbatdata = {}
totbowldata = {}
totbowltobatdata = {}

def createfullvec(s):
    global vec
    global outcome
    global inningsnum
    global totbatdata
    global totbowldata
    global totbowltobatdata
    pathname = ".\ipl\\" + s
    with open(pathname , "r") as file:
        user_list = yaml.load(file,Loader = yaml.FullLoader)
        
        # winner = user_list['outcome']['winner']
        

    if 'winner' not in user_list['info']['outcome']:
        return
    winner = user_list['info']['outcome']['winner']
    targetruns = 0
    
    def inningsextract(innings):

        dum_list = user_list['innings']
        var = 0
        if innings == '2nd innings':
            var = 1
        
        dum_list_beta = dum_list[var]
        
        win = 0

        dum_list_pota = dum_list_beta[innings]
        # print(dum_list_pota['team'])
        if dum_list_pota['team'] == winner:
            win = 1

        batsmen = set([])
        bowlers = set([])


        for i in range(len(dum_list_pota['deliveries'])):
            for key , value in dum_list_pota['deliveries'][i].items():
                # print(key , value)
                batsmen.add(value['batsman'])
                batsmen.add(value['non_striker'])
                bowlers.add(value['bowler'])

        batsdata = {}
        bowldata = {}

        for i in batsmen:
            bowlertemp = {}
            for j in bowlers: 
                bowlertemp[j] = 0
            batsdata[i] = {'runs': 0 , 'balls' :0, 'bowlname' : bowlertemp}

        for i in bowlers:
            batsmenname = {}
            for j in batsmen: 
                batsmenname[j] = 0
            bowldata[i] = {'balls' : 0, 'runs': 0 , 'wickets' : [],'batsname' : batsmenname}




        for i in range(len(dum_list_pota['deliveries'])):
            for key , value in dum_list_pota['deliveries'][i].items():
                #adding batting data
                batsdata[value['batsman']]['runs'] += value['runs']['total']
                batsdata[value['batsman']]['balls'] += 1
                batsdata[value['batsman']]['bowlname'][value['bowler']] += value['runs']['total']

                #adding bowling data
                bowldata[value['bowler']]['balls'] += 1
                bowldata[value['bowler']]['runs'] += value['runs']['total']
                bowldata[value['bowler']]['batsname'][value['batsman']] += value['runs']['total']

                if 'wicket' in value:
                    bowldata[value['bowler']]['wickets'].append(value['wicket']['player_out'])

        return dum_list_pota,win





    # for i in bowldata:
    #     # print(i,' ',bowldata[i])
            
    # # CURRENT MATCH    
    # # (general stuff)   ✅ 
    # 1 bowl number ✅✅
    # 2 run rate ✅✅
    # 3 Required run rate(0 for 1st innings) ✅
    # 4 wicket array ✅
    # # bowler's performance ✅
    # 5 current economy (runs /balls)✅
    # 6 wicket performance (total wickets taken)✅
    # batsmen✅
    # 7 strike rate(runs / ball * 100)✅
    # 8 total runs✅
    # #batsmen vs bowler✅
    # 9 runs/balls✅

    # #PREVIOUS DATA

    # batsmen  
    # 10 strike rate(average)✅
    # 11 runs(sigma runs discounted)✅

    # bowler vs batsmen
    # 14 balls vs Runs (balls / runs (discounted))
    # 15 wickets (sigma wickets) (discounted)

    # bowler perf
    # 12 economy (runs / balls (disc))
    # 13 wickets (sigma wickets (disc))

    
    target = 0
    def vectorcreate(dum_list_pota):
        global inningsnum
        totruns = 0 
        bowlnum = 0
        global target
        if inningsnum == 0:
            target = 0
        

        

        wickets = np.zeros(10)
        wicketct = 0
        wickets[0] = 1
        bowlerperf = {}
        dumdictb = {}
        batsmanperf = {}

        for i in range(len(dum_list_pota['deliveries'])):
            for key , value in dum_list_pota['deliveries'][i].items():
                bowlnum += 1
        
        # for i in range(len(dum_list_pota['deliveries'])):
        #     for key , value in dum_list_pota['deliveries'][i].items():
        #         print(key , ' ' ,value)
        
        # print()
        
        vec = np.zeros([bowlnum,24])
        dumbwlct = bowlnum
        bowlnum = 0
        

        for i in range(len(dum_list_pota['deliveries'])):
            for key , value in dum_list_pota['deliveries'][i].items():
                bowlername = value['bowler']
                batsmanname = value['batsman']
                dumdictb[batsmanname + ' to ' + bowlername] = [0,0]
                bowlerperf[bowlername] = [0,0,0]
                batsmanperf[batsmanname] = [0,0]


        # print(bowlerperf)

        for i in range(len(dum_list_pota['deliveries'])):
            for key , value in dum_list_pota['deliveries'][i].items():
                # print(key,' ',value)
                bowlnum += 1
                totruns += value['runs']['total']
                vec[bowlnum - 1][0] = bowlnum

                vec[bowlnum - 1][1] = totruns/(bowlnum)

                vec[bowlnum - 1][2] = ((target - totruns)/((dumbwlct  + 1 - bowlnum)))*(inningsnum)
                flg = 0

                if 'wicket' in value:
                    wickets[wicketct] = 0
                    wicketct += 1
                    flg = 1
                    if wicketct == 10:
                        break

                    wickets[wicketct] = 1

                for j in range(10):
                    vec[bowlnum-1][3+j] = wickets[j]

                bowlername = value['bowler']
                batsmanname = value['batsman']

                bowlerperf[bowlername][0] += value['runs']['total']
                bowlerperf[bowlername][1] += flg
                bowlerperf[bowlername][2] += 1
                
                dumdictb[batsmanname + ' to ' + bowlername][0] += value['runs']['total']
                dumdictb[batsmanname + ' to ' + bowlername][1] += 1
                
                # current economy (runs /balls)
                vec[bowlnum - 1][13] = bowlerperf[bowlername][0]/bowlerperf[bowlername][2]

                # wicket performance (total wickets taken)
                vec[bowlnum - 1][14] = bowlerperf[bowlername][1]
                

                batsmanperf[batsmanname][0] += value['runs']['total']
                batsmanperf[batsmanname][1] += 1

                # strike rate(runs / ball * 100)
                vec[bowlnum - 1][15] = (batsmanperf[batsmanname][0]/batsmanperf[batsmanname][1])*100.00
                
                # total runs
                vec[bowlnum - 1][16] = batsmanperf[batsmanname][0]

                # runs/balls
                if dumdictb[batsmanname + ' to ' + bowlername][0] != 0:
                    vec[bowlnum - 1][17] = dumdictb[batsmanname + ' to ' + bowlername][0]/dumdictb[batsmanname + ' to ' + bowlername][0]
                

                if batsmanname in totbatdata:
                    # # strike rate 
                    if totbatdata[batsmanname][1] != 0:
                        vec[bowlnum - 1][18] = totbatdata[batsmanname][0]/totbatdata[batsmanname][1]
                    # total runs
                        vec[bowlnum - 1][19] = totbatdata[batsmanname][0]
                
                st = bowlername + ' to ' + batsmanname
                if st in totbowltobatdata:
                    if totbowltobatdata[st][1] != 0:
                        vec[bowlnum - 1][20] = (totbowltobatdata[st][0]/totbowltobatdata[st][1])
                
                if bowlername in totbowldata:
                    if totbowldata[bowlername][2] != 0:
                        vec[bowlnum - 1][22] = totbowldata[bowlername][0]/totbowldata[bowlername][2]

                    vec[bowlnum - 1][23] = totbowldata[bowlername][1]

                

                
                
                

                

                

        if inningsnum == 0:
            target = totruns
        return vec, batsmanperf, bowlerperf, dumdictb
        


    dum_list_pota1, winfg1 = inningsextract('1st innings')
    dum_list_pota2, winfg2 = inningsextract('2nd innings')   

    vec1,btsmperf,bwlrperf,bowltobat = vectorcreate(dum_list_pota1)
    
    vec = np.concatenate((vec, vec1), axis= 0)
    inningsnum = 1
    vec2,btsmperf1,bwlrperf1,bowltobat1 = vectorcreate(dum_list_pota2)
    vec = np.concatenate((vec, vec2), axis= 0)
    
    btsmperf.update(btsmperf1)
    bwlrperf.update(bwlrperf1)
    bowltobat.update(bowltobat1)
   
    
    
    
    inningsnum = 0

    sz1 = np.shape(vec1)[0]
    sz2 = np.shape(vec2)[0]


    outcome1 = np.zeros([(sz1 + sz2),1])

    for i in range(sz1 + sz2):
        if i < sz1 : 
            outcome1[i] = winfg1
        else :
            outcome1[i] = winfg2
    
    outcome = np.concatenate((outcome, outcome1), axis= 0)
    
    
    for key in btsmperf:
        
        if key in totbatdata:
            totbatdata[key][0] += btsmperf[key][0]
            totbatdata[key][1] += btsmperf[key][1]
        else:
            totbatdata[key] = btsmperf[key]

    
    
    for key in bwlrperf:
        if key in totbowldata:
            totbowldata[key][0] += bwlrperf[key][0]
            totbowldata[key][1] += bwlrperf[key][1]
            totbowldata[key][2] += bwlrperf[key][2]
        else:
            totbowldata[key] = bwlrperf[key]

    for key in bowltobat:
        if key in totbowltobatdata:
            totbowltobatdata[key][0] += bowltobat[key][0]
            totbowltobatdata[key][1] += bowltobat[key][1]
        else:
            totbowltobatdata[key] = bowltobat[key]

    

    
    


start = 335982
matches = 0


for i in arr: 
    print(matches ,' ',i)
    createfullvec(i)

    matches += 1
    if matches == 500:
      break
 
# print(totbatdata)
# print(totbowltobatdata['S Dhawan to S Aravind'])
num, dum = np.shape(vec)
num = (num*80)//100
traindata = vec[0: num]
trainoutcome = outcome[0:num]
testdata = vec[num:]
testoutcome = outcome[num:]

print(np.shape(traindata))
print(np.shape(testdata))


 
 





    








        
        
        





# for i in range(len(dum_list_pota['deliveries'])):
#     for key , value in dum_list_pota['deliveries'][i].items():
#         print(key,' ',value)
#         




# for i in range(20):
#     print(vec[i])
    


# print(vec[10000])