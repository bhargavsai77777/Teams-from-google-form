#!/usr/local/bin/python3
# assign2.py : Assign people to teams
#
# Code by: surgudla-sgaraga-bgogineni
#
# Based on skeleton code by R. Shah and D. Crandall, January 2021
#

import heapq
import copy
from time import *
from queue import PriorityQueue
import sys



#the input file will be loaded here and the students preferences and non preferences will be recorded into variables.
def readingPrefernces(inputFileName):
    with open(inputFileName) as inputfile:
        seperated_preferencelist = []
        cost=0
        prefernces=[]
        k=[]
        users = []

        for line in inputfile:
            temp = line.strip().split(' ')
            seperated_preferencelist = temp[1].split("-")
            temp.append(len(seperated_preferencelist))
            prefernces.append(seperated_preferencelist)

            users.append(temp[0])
            temp.append(cost)
            k.append(temp)

    return (k,prefernces,users)



#Caluclate the cost of every team assigned according to the number of complaints
def cost1function(groups,tempList):
    Total_group_cost=0
    Each_member_cost=0
    total_cost=0
    l = 0
    p = []
    np = []
    for onegroup in groups:
        if onegroup != 'zzz':
            for k in tempList:
                if k[0] == onegroup:
                    l = k[-2]
                    p = k[1].split("-")
                    np1 = k[2].split(",")
                    np.append(np1)

            #check length
            if len(groups) != l:
                Each_member_cost += 1
            # check preference
            for p1 in p:
                if p1 not in groups and p1!='zzz':
                    Each_member_cost += 1
            # check non-preference groups
            for i in np:
                if i in groups:
                    Each_member_cost += 2
            Total_group_cost += Each_member_cost
    total_cost += Total_group_cost
    return total_cost




#Randomly make some initial group which serves as a starting point for successors
def Initial_state(Data_set,seperated,List_of_students):
    # print(templist)
    for i in Data_set:
        preference = i[1].split("-")
        y = [x for x in preference if x != 'zzz']
        i[-1] = cost1function(y, Data_set)

    avilable_students=List_of_students
    Dataset_sorted=(sorted(Data_set, key = lambda x: x[-1]))
    initial_state=[]


    for group in Dataset_sorted:
        g = group[1].split("-")
        z = [x for x in g if x != 'zzz']

        for member in z:
            if member in avilable_students:
                avilable_students.remove(member)
        initial_state.append(z)

    tmp_list = [avilable_students[x:x + 3] for x in range(0, len(avilable_students), 3)]
    for group1 in tmp_list: initial_state.append(group1)
    return initial_state


import random



def successor1(state , Data_set):
    List_of_students = []
    for i in Data_set:
        List_of_students.append(i[0])
    user=random.choice(List_of_students)
    sucss_states=[]

    valid="No"
    for i in range(len(state)):
        new_state=copy.deepcopy(state)
        valid="No"
        list=[]
        j=0
        while(j!=len(new_state)):
            list.append((j,new_state[j]))
            j+=1
        for k in range(0,len(list)):

            if user in list[k][1]:
                list[k][1].remove(user)
                if len(list[k][1]) == 0:
                    new_state.remove(list[k][1])
                if i == list[k][0]:
                    new_state.append([user])
                    valid = "Yes"
                    break
            elif len(list[k][1]) <= 2 and i == list[k][0]:
                list[k][1].append(user)
                valid = "Yes"
        if valid=="Yes":
            sucss_states.append(new_state)

    return sucss_states





def is_goal(state,templist):
    students= []
    [students.append(i[0]) for i in templist]
    assigned_students = []
    [[assigned_students.append(user) for user in groups]for groups in state]


    for user in students:
        if user not in assigned_students:
            return False
    return True





def solver(input_file):


    Data_set, seperated_preferencelist, List_of_students = readingPrefernces(input_file)
    initial_state = Initial_state(Data_set, seperated_preferencelist, List_of_students )
    next_cost = 0
    for inistate in initial_state:
        pre_cost = cost1function(inistate, Data_set)
        next_cost += pre_cost
    succ_states = successor1(initial_state, Data_set)

    minimum_cost = float("inf")
    time_break = time() + 120

    while True:
        fringe = []
        cost_new1 = 0
        for states in succ_states:
            for state in states:
                cost_new = cost1function(state, Data_set)
                cost_new1 += cost_new
            heapq.heappush(fringe, (cost_new1, states))

        a=heapq.heappop(fringe)
        next_cost = a[0]
        min_cost_state = a[1]

        succ_states = successor1(min_cost_state, Data_set)

        if next_cost < minimum_cost:
            best_group = ["-".join(i) for i in min_cost_state]
            minimum_cost = next_cost
            yield ({"assigned-groups": best_group,
                    "total-cost": minimum_cost})

        if time_break < time():
            break




if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
