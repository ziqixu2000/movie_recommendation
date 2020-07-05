import numpy as np
import pandas as pd
import math
np.seterr(divide='ignore', invalid='ignore')

datadictiondary = {}
userlist=[]
movielist=[]
moviedic={}
file = open('ratings.csv','r')
#skip the headings
for content in file.readlines()[1:]:
#store all data in a dictionary of dictionary. In the first dictionary, key is user id, value is the 
#second dictionary. In the second dictionary, key is movie id, value is rating.
    content = content.strip().split(',')
    if content[0] not in userlist:
        userlist.append(content[0])
    if content[1] not in movielist:
        movielist.append(content[1])
    if content[0] not in datadictiondary.keys():
        datadictiondary[content[0]]={content[1]:content[2]}
    else:
        datadictiondary[content[0]][content[1]]=content[2]
file.close()

file = open('movies.csv','r')
for content in file.readlines()[1:]:
    content = content.strip().split(',')
    if content[0] not in moviedic.keys():
        moviedic[content[0]] = content[1]
file.close()
    



#calculate the similarity among different users
def Pearson(userOne,userTwo):
    dataOne = datadictiondary[userOne]
    dataTwo = datadictiondary[userTwo]
    common=[]
    for elements in dataOne.keys():
        if elements in dataTwo.keys():
            common.append((elements,dataOne[elements],dataTwo[elements]))
    common = pd.DataFrame(common,columns=['movie','userOne','userTwo'])
    common = common.apply(lambda x:x.astype(float))
    pc = common['userOne'].corr(common['userTwo'])
    if math.isnan(pc):
        return 0
    else:
        return pc

def top20(user):
    result=[]
    for users in userlist:
        if users!= user:
            pc = Pearson(users,user)
            result.append((users,pc))
    result.sort(key=lambda val:val[1])
    result.reverse()
    return result[:20]

def takeSecond(elem):
    return elem[1]

def topmovies(similar_user):
    allusers=[]
    allpcs=[]
    result=[]
    for elements in similar_user:
        allusers.append(elements[0])
        allpcs.append(float(elements[1]))
    for singlemovie in movielist:
        for singleuser in allusers:
            info = datadictiondary[singleuser]
            score = 0
            totalpc = 0
            if singlemovie in info.keys():
                score += float(info[singlemovie])*allpcs[allusers.index(singleuser)]
                totalpc += allpcs[allusers.index(singleuser)]
        if totalpc != 0:
            finalresult = score/totalpc
            result.append((singlemovie,finalresult))
    result.sort(key=takeSecond,reverse=True)
    print result[:30]
    return result[:30]

def topmovienames(toplist):
    result = []
    for element in toplist:
        movieid = element[0]
        result.append(moviedic[movieid])
    print(result)
    return result

temp=top20(userlist[2])
topmovienames(topmovies(temp))




            
            
            
            
                





    

