from collections import Counter
import copy
import random


# 1. PUSH TO GITHUB
# 2. break up code into segments with common functionality - 
# 2. Clean up the code in main() to create functions
# 

f = open('studentschedules.csv', 'r')
# g = open('version2.csv', 'r')
g = open('version2_sem2.csv', 'r')
schedules = list(f)
openCourselist1 = list(g)



# outputs the different items in the two lists
"""
outputs the different items in the two lists
Args: 
    -li1: list that contains ndsf
    -li2: list that contains jsndfosd
Returns:
    - gndsfng
Note: corner cases

"""
def Diff(li1, li2): 

    li2_modify = copy.deepcopy(li2)
    for i in li1:
        for j in li2:
            if i in j and j in li2_modify:
                if len(i) == 3:
                    li2_modify.remove(j)
                    j = i[0] + i[1]
                    if j in li2_modify:
                        li2_modify.remove(j)
                        for k in li2_modify:
                            if i[0] in k:
                                if i[1] in k:
                                    li2_modify.remove(k)
                    j = i[0] + i[2]
                    if j in li2_modify:
                        li2_modify.remove(j)
                        for z in li2_modify:
                            if i[0] in z:
                                if i[2] in z:
                                    li2_modify.remove(z)

                if len(i) == 2:
                    for l in li2_modify:
                        if i[0] in l:
                            if i[1] in l:
                                li2_modify.remove(l)
                
                else:
                    if j in li2_modify:
                        li2_modify.remove(j)

    return li2_modify


def main():

    val = input("Enter the semester number please: ")  
    allBlocks = []
    allId = []
    updatedSchedules = []
    courseTermsection = []
    semLinenumbers = []
    idLimits = []
    allStudentbusyblocks = {}
    open_blocks = []
    available_list = []
    possible_courses = {}
    course = []
    all_courses = []
    allStudentcourse = {}
    name = []
    unique = []

    # this deletes the first row in the schedules file which is just the description of what each column in the file is
    schedules.pop(0)


    # this list consists of all block possibilities in a possible CA schedule
    block_possibilities = ["A", "B", "C", "D", "E", "F", "G", "AS", "A12", "A13", "A23", "B12", "B13", "B23", "C12", "C13", "C23", "D12", "D13", "D23", "E12", "E13", "E23", "F12", "F13", "F23", "G12", "G13", "G23", "H1", "A1", "A2", "A3","B1", "B2", "B3","C1", "C2", "C3","D1", "D2", "D3","E1", "E2", "E3","F1", "F2", "F3","G1", "G2", "G3"]

    # appending the course, term, and section for each course in the student schedules file
    count = 0
    for j in range(0, len(schedules)):
        courseTermsection.append((((schedules[j].split(",")[3]).split("-"))))


    # together, these for loops append to a list which consists the name of each student at CA    
    for i in schedules:
        name.append(i.split(",")[1])
    
    for i in name:
        if i not in unique:
            unique.append(i)


    # this for loop deals with the file which has the student schedules for the whole year 
    # the for loop appends the row numbers which have the current schedules of the students for ONLY the appropriate semester (sem1 or sem2)
    # ultimately, this list only has the current schedules for each of the students for the applciable semester
    for k in courseTermsection:
        count += 1
        # the one represents which semester we want to analyze; possible options include 1 or 2 (sem1 or sem2)
        if k[1] == val: 
            semLinenumbers.append(count)


    # appends the current courses for each the students for the applicable semester
    for i in semLinenumbers:
      for j in schedules:
          if ((schedules.index(j) + 1) == i):
              updatedSchedules.append(j)

    # appends the ids of the students in the allId list
    count = 0
    for i in updatedSchedules:
        allId.append((updatedSchedules[count].split(",")[0]))
        # grade[((updatedSchedules[count].split(",")[0]))] = ((updatedSchedules[count].split(",")[2]))
        count += 1

    # appends to idLimits list with the last row number with a course for that semester for each of the students
    # appends to allBlocks list with all the busy blocks for each of the students
    # appends to all_courses list with all the courses for that appropriate semester for each of the students
    count = 0
    for i in updatedSchedules:
        idLimits.append(allId.index(updatedSchedules[count].split(",")[0]))
        allBlocks.append((updatedSchedules[count].split(",")[4]))
        all_courses.append(((updatedSchedules[count].split(",")[3]).split("-")[0]))
        count += 1

    # transforms the list above into a dictionary so we can identify the courses and busy blocks for each of the students
    idLimits.append(len(updatedSchedules))
    count = 0
    for i in range(len(updatedSchedules)):
        for j in sorted(set(idLimits)):
            allStudentbusyblocks[updatedSchedules[count].split(",")[0]] = allBlocks[idLimits[i]: idLimits[i + 1]]
            allStudentcourse[updatedSchedules[count].split(",")[0]] = all_courses[idLimits[i]: idLimits[i + 1]]
        count += 1

    # appends to a list with all the blocks for the courses in the current open course list
    for i in openCourselist1:
        open_blocks.append(i.split(",")[3])

    # removes the "." next to the blocks for sem2
    if val == "2":
        for i in allStudentbusyblocks.values():
            for j in i:
                index = i.index(j)
                j = j[1:]
                i[index] = j

    # figures out the free blocks for each of the students using the difference function defined above
    for i in allStudentbusyblocks.values():
        available_list.append(Diff(i, block_possibilities))

    # together, these two blocks of code eliminate some of the blocks because the student is actually busy during those blocks
    # ex. a student may be busy during C12; that means that the student is NOT free during C block itself

    count = 0
    for i in available_list:
        cop = copy.deepcopy(i)
        for j in cop:
            if len(j) == 1:
                for k in cop:
                    if j in k:
                        count += 1
                if count < 7:
                    i.remove(j)
                
            count = 0

    for i in available_list:
        cop1 = copy.deepcopy(i)
        for j in cop1:
            if j not in open_blocks:
                i.remove(j)


    # appends to available_list with four block offerings which should be possible free blocks for each of the students
    for i in available_list:
        if "TBA" not in i:
            i.append("TBA")
        if "AS" not in i:
            i.append("AS")
        if ".AS" not in i:
            i.append(".AS")
        if "H1+AS" not in i:
            i.append("H1+AS")


    # this finds courses in the open course list for each of the free blocks for each of the students
    count = 0
    for i in available_list:
        for j in i:
            for k in openCourselist1:
                if (((k.split(",")[3]).find(j)) != -1):
                    if (k.split(",")[0]) not in course:
                        course.append(((k.split(",")[0])))
                        # blocks.append(k.split(",")[3])
        possible_courses[count] = course
        # blockdict[count] = blocks
        course = []
        # blocks = []
        count += 1

    # filters out MATH courses which the student CANNOT take
    count = -1
    for z in allStudentcourse.values():
        for k in z:
            if k[0:3] == "MAT":
                for i in possible_courses.values():
                    copyy = copy.deepcopy(i)
                    for l in copyy:
                        if list(allStudentcourse.values()).index(z) == list(possible_courses.values()).index(i):
                            if l[0:3] == "MAT":
                                if int(k[3:6]) + 50 < int(l[3:6]) or int(k[3:6]) > int(l[3:6]):
                                    i.remove(l)


    # filters out ENGLISH courses which the student CANNOT take
    for z in allStudentcourse.values():
        for k in z:
            if k[0:3] == "ENG":
                for i in possible_courses.values():
                    copyy = copy.deepcopy(i)
                    for j in copyy:
                        if list(allStudentcourse.values()).index(z) == list(possible_courses.values()).index(i):
                            if j[0:3] == "ENG":
                                if int(k[3:4]) == int(2):
                                    if int(j[3:4]) != int(2):
                                        i.remove(j)
                                if int(k[3:4]) == int(1):
                                    if int(j[3:4]) != int(1):
                                        i.remove(j)
                                if int(k[3:4]) >= int(3): 
                                    if int(j[3:4]) == int(1) or int(j[3:4]) == int(2):
                                        i.remove(j)


    # filters out HISTORY courses which the student CANNOT take
    for j in allStudentcourse.values():
        for k in j:
            if k[0:3] == "HIS":
                for i in possible_courses.values():
                    copyyyy = copy.deepcopy(i)
                    for z in copyyyy:
                        if list(allStudentcourse.values()).index(j) == list(possible_courses.values()).index(i):
                            if z[0:3] == "HIS":
                                if (int(k[3:4]) < int(z[3:4]) and int(k[3:4]) == int(1)):
                                    i.remove(z)
                                elif (int(k[3:4]) < int(z[3:4]) and int(k[3:4]) == int(2)):
                                    i.remove(z)
                                elif (int(k[3:4]) > int(z[3:4]) and int(k[3:4]) == int(2)):
                                    i.remove(z)
                                elif (int(k[3:4]) > int(z[3:4]) and int(k[3:4]) == int(3)):
                                    i.remove(z)

    # print(possible_courses)

    # filters out LANGUAGE courses which the student CANNOT take
    for j in allStudentcourse.values():
        for k in j:
            if k[0:3] == "FRE" or k[0:3] == "GER" or k[0:3] == "LAT" or k[0:3] == "SPA" or k[0:3] == "MAN":
                for i in possible_courses.values():
                    copyy = copy.deepcopy(i)
                    for z in copyy:
                        if list(allStudentcourse.values()).index(j) == list(possible_courses.values()).index(i):
                            if z[0:3] == k[0:3]:
                                if (int(k[3:6]) != int(z[3:6]) and int(k[3:4]) < 4 and int(z[3:4]) <= 4):
                                    i.remove(z)
                                if (int(k[3:4]) != int(z[3:4]) and int(k[3:4]) == 4 and int(z[3:4]) != 9):
                                    i.remove(z)
                                if (int(k[3:4]) != int(z[3:4]) and int(k[3:4]) == 9):
                                    i.remove(z)
                            else:
                                if ((int(k[3:4]) != int(z[3:4])) and (z[0:3] != k[0:3]) and (z[0:3] == "FRE" or z[0:3] == "GER" or z[0:3] == "LAT" or z[0:3] == "SPA" or z[0:3] == "MAN")):
                                    i.remove(z)


    # filters out SCIENCE courses which the student CANNOT take
    for j in allStudentcourse.values():
        for k in j:
            if k[0:3] == "BIO" or k[0:3] == "CHE" or k[0:3] == "ENV" or k[0:3] == "PHY" or k[0:3] == "ENR":
                for i in possible_courses.values():
                    copyyy = copy.deepcopy(i)
                    for z in copyyy:
                        if list(allStudentcourse.values()).index(j) == list(possible_courses.values()).index(i):
                            if z[0:3] == "BIO":
                                if k[0:3] == "BIO":
                                    if (int(k[3:6]) < int(z[3:6]) and int(k[3:4]) == 1):
                                        i.remove(z)
                                    if (int(k[3:6]) > int(z[3:6]) and int(k[3:4]) != 1):
                                        i.remove(z)
                                else:
                                    if int(z[3:4]) == 1:
                                        i.remove(z)
                            if z[0:3] == "CHE":
                                if k[0:3] == "CHE":
                                    if (int(k[3:6]) < int(z[3:6]) and int(k[3:4]) == 2):
                                        i.remove(z)
                                    if (int(k[3:6]) > int(z[3:6]) and int(k[3:4]) != 2):
                                        i.remove(z)
                                else:
                                    if k[0:3] == "BIO" and int(k[3:4]) == 1:
                                        i.remove(z)
                                    if (z[0:4] == "CHE2") and (k[0:3] == "PHY" or k[0:3] == "ENR"):
                                        i.remove(z)

                            if z[0:3] == "PHY" or z[0:3] == "ENR" or z[0:3] == "ENV":
                                if (k[0:3] == "BIO" and int(k[3:4]) == 1):
                                    i.remove(z)
                            
                            if z[0:3] == "PHY" or z[0:3] == "ENR":
                                if k[0:4] == "CHE2":
                                    i.remove(z)
                            
                            if z[0:3] == "ENV":
                                if (int(z[3:4]) == 3 or int(z[3:4]) == 4):
                                    if k[0:4] == "BIO1" or k[0:4] == "CHE2":
                                        if z in i:
                                            i.remove(z)

    # filters out COMPSCI courses which the student CANNOT take
    for j in allStudentcourse.values():
        for k in j:
            if k[0:3] == "CST":
                for i in possible_courses.values():
                    copyy = copy.deepcopy(i)
                    for z in copyy:
                        if list(allStudentcourse.values()).index(j) == list(possible_courses.values()).index(i):
                            if z[0:3] == "CST":
                                if int(k[3:6]) == 101 and z[0:6] != "CST101":
                                    i.remove(z)
                                if int(k[3:6]) != 101 and z[0:6] == "CST101":
                                    i.remove(z)


    # filters out HEALTH courses which the student CANNOT take
    for j in allStudentcourse.values():
        for k in j:
            if k[0:3] == "HEA":
                for i in possible_courses.values():
                    copyy = copy.deepcopy(i)
                    for z in copyy:
                        if list(allStudentcourse.values()).index(j) == list(possible_courses.values()).index(i):
                            if z[0:3] == "HEA":
                                if int(k[3:6]) == 101 and int(z[3:6]) != 101:
                                    i.remove(z)
                                if int(k[3:6]) == 201 and int(z[3:6]) != 201:
                                    i.remove(z)
                                if int(k[3:6]) == 301 and int(z[3:6]) != 301:
                                    i.remove(z)


    # filters out THEATER/DANCE courses which the student CANNOT take
    for l in allStudentcourse.values():
        for k in l:
            if k[0:3] == "THE" or k[0:3] == "DAN":
                for i in possible_courses.values():
                    copyy = copy.deepcopy(i)
                    for j in copyy:
                        if list(allStudentcourse.values()).index(l) == list(possible_courses.values()).index(i):
                            if j[0:3] == "DAN":
                                if k[0:3] == "DAN":
                                    if int(k[3:6]) != int(j[3:6]):
                                        i.remove(j)
                            if j[0:3] == "THE":
                                if k[0:3] == "THE":
                                    if int(k[3:6]) != int(j[3:6]):
                                        i.remove(j)

    # filters out VISUAL ARTS courses which the student CANNOT take                            
    for z in allStudentcourse.values():
        for k in z:
            if k[0:3] == "DRA" or k[0:3] == "VIS" or k[0:3] == "PAI" or k[0:3] == "CER" or k[0:3] == "PHO" or k[0:3] == "FIL":
                for i in possible_courses.values():
                    copyy = copy.deepcopy(i)
                    for j in copyy:
                        if list(allStudentcourse.values()).index(z) == list(possible_courses.values()).index(i):
                            if j[0:3] == "DRA":
                                if k[0:3] == "DRA":
                                    if (k[0:6]) != (j[0:6]):
                                        i.remove(j)
                                else:
                                    if k[3:4] != j[3:4]:
                                        i.remove(j) 

                            if j[0:3] == "CER":
                                if k[0:3] == "CER":
                                    if (k[0:6]) != (j[0:6]):
                                        i.remove(j)
                                else:
                                    if k[3:4] != j[3:4]:
                                        i.remove(j) 

                            if j[0:3] == "PAI":
                                if k[0:3] == "PAI":
                                    if (k[0:6]) != (j[0:6]):
                                        i.remove(j)
                                else:
                                    if k[3:4] != j[3:4]:
                                        i.remove(j) 

                            if j[0:3] == "PHO":
                                if k[0:3] == "PHO":
                                    if (k[0:6]) != (j[0:6]):
                                        i.remove(j)
                                else:
                                    if k[3:4] != j[3:4]:
                                        i.remove(j) 

                            if j[0:3] == "FIL":
                                if k[0:3] == "FIL":
                                    if (k[0:6]) != (j[0:6]):
                                        i.remove(j)
                                else:
                                    if k[3:4] != j[3:4]:
                                        i.remove(j)

                            # don't know what to do for VIS



    # appends the possible courses and the blocks that the course is available to a list
    list99 = []
    for j in possible_courses.values():
        for k in j:
            for i in openCourselist1:
                if k in i.split(",")[0]:
                    list99.append(k)
                    list99.append(i.split(",")[3])

    # transforms list99 into a dictionary - key is one of the possible courses, value is a list with the block(s) that the course is offered in
    d = {}
    list78 = []
    index = 0
    for i in list99:
        if index % 2 == 0:
            if index + 2 < len(list99):
                if i == list99[(index + 2)]:
                    if i not in d:
                        list78 = []
                        list78.append(list99[(index + 1)])
                        d[i] = set(list78)
                    else:
                        list78.append(list99[(index + 1)])
                        d[i] = set(list78)
                else:
                    if i not in d:
                        if len(i) > 5:
                            list78.append(list99[(index + 1)])
                            d[i] = set(list78)
                    if i in d and len(d.get(i)) >= 1 and len(i) > 5:
                        list78.append(list99[(index + 1)])
                        d[i] = set(list78)
                        list78 = []
        index += 1


    # this changes the data type (to a list) of each of the items in the list - this list is the value for the possible courses dictionary
    newlist = []
    count = 0
    possible_courses1 = {}
    for i in possible_courses.values():
        for k in i:
            if i.index(k) == len(i)-1:
                split = k.split(",")
                newlist.append(split)
                possible_courses1[count] = newlist
                newlist = []
            else:
                split = k.split(",")
                newlist.append(split)
        count += 1

    # combines the possible courses for the students with the block(s) that each course is offered in - final output
    list556 = []
    count = 0
    possible_courses2 = {}
    for i in possible_courses1.values():
        for j in i:
            if j[0] in list(d.keys()):
                for z in d.get(j[0]):
                    if z in available_list[list(possible_courses1.values()).index(i)]:
                        index = list(list(possible_courses1.values())[list(possible_courses1.values()).index(i)]).index(j)
                        thething = ((list(list(possible_courses1.values())[list(possible_courses1.values()).index(i)][index])))
                        thething.append(z)
                        list556.append(thething)

        
        possible_courses2[unique[count]] = list556
        count += 1
        list556 = []
    print(possible_courses2)

    # transforms the possible courses dictionary into a csv file and writes to it
    with open('test.csv', 'w') as f:
        for key in possible_courses2.keys():
            f.write("%s,%s\n"%(key,possible_courses2[key]))

# calls the main function
if __name__ == "__main__":
    main()   
