#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import glob
import matplotlib.pyplot as plt


# In[34]:


lane_width = 3.7
ego_width = 1.905
tolerance = 1.30*(0.5*lane_width - 0.5*ego_width)


# In[2]:


#Importing and printing all .xlsx the files in the lane change folder
file_list = glob.glob("F:\GoogleData\segregated_data\Waymo Filtered\GapAcceptance/*.xlsx")
#file_list
len(file_list)


# In[3]:


print(file_list[0])
t = file_list[0]
print(t[59:])


# In[4]:


#Give the address of the global data (folders with subfolders)
path_global = r"F:\GoogleData\UnzippedYonohubData\GlobalData"


# In[5]:


my_address_list = [] #list of the address of global data of corresponding lane change files
for x in file_list:
    #print(x[56:])
    xlsx_files = glob.glob(path_global + "/**/"+ x[59:], recursive = True)
    #print(type(xlsx_files))
    my_address_list.append(xlsx_files)
print(len(my_address_list))

my_address_list=[str(i) for i in my_address_list]
len(my_address_list)


# In[55]:


#Address for saving figures
save_path = r"C:\Users\hp\OneDrive - UNSW\AhmedYonohub\Results\Gap Acceptance"


# for i in my_address_list:
#     print(i)

# for i in my_address_list:
#     #print(i[-81:-20])
#     i = i[:-25]
#     i = i[-48:]
#     print(i)

# In[7]:


segment_name =['segment-10212406498497081993_5300_000_5320_000_',
'segment-10231929575853664160_1160_000_1180_000_',
'segment-10391312872392849784_4099_400_4119_400_',
'segment-11928449532664718059_1200_000_1220_000_',
'segment-12848519977617081063_2488_000_2508_000_',
'segment-12858738411692807959_2865_000_2885_000_',
'segment-12988666890418932775_5516_730_5536_730_',
'segment-13178092897340078601_5118_604_5138_604_',
'segment-13415985003725220451_6163_000_6183_000_',
'segment-13830510593707564159_5575_000_5595_000_',
'segment-1416654423768444853_2660_000_2680_000_',
'segment-14561791273891593514_2558_030_2578_030_',
'segment-1505698981571943321_1186_773_1206_773_',
'segment-15266427834976906738_1620_000_1640_000_',
'segment-15903544160717261009_3961_870_3981_870_',
'segment-16331619444570993520_1020_000_1040_000_',
'segment-16651261238721788858_2365_000_2385_000_',
'segment-17860546506509760757_6040_000_6060_000_',
'segment-17874036087982478403_733_674_753_674_',
'segment-18305329035161925340_4466_730_4486_730_',
'segment-2506799708748258165_6455_000_6475_000_',
'segment-3698685523057788592_4303_630_4323_630_',
'segment-3911646355261329044_580_000_600_000_',
'segment-4277109506993614243_1648_000_1668_000_',
'segment-4490196167747784364_616_569_636_569_',
'segment-5076950993715916459_3265_000_3285_000_',
'segment-5121298817582693383_4882_000_4902_000_',
'segment-7768517933263896280_1120_000_1140_000_',
'segment-8822503619482926605_1080_000_1100_000_',
'segment-9509506420470671704_4049_100_4069_100_',]


# In[35]:


j=-1
for i in my_address_list:
    j = j+1
    file_name = i[2:-2]
    df = pd.read_excel(file_name)
    print(len(df))
    df = df.loc[(df['objY'] <= tolerance) & 
                    (df['objY'] > -1*tolerance)]
    
    # Get names of indexes for which column 'objX' has negative value
    indexNames = df[ df['objX'] <= 0 ].index
    # Delete these row indexes from dataFrame
    df.drop(indexNames , inplace=True)
    print(len(df))
        
    #df_groupbyFrame = df.groupby('frame no').first()
    df_groupbyFrame = df.groupby(['frame no'], sort=True).first()
    Y = []
    X = []
    Z = []
    for i in range (1, len(df_groupbyFrame)):
        y_axis = (df_groupbyFrame.iloc[i,3])
        Y.append(y_axis)
        x_axis = i/10
        X.append(x_axis)
        z_axis = df_groupbyFrame.iloc[i,21]
        Z.append(z_axis)
        
    # create figure and axis objects with subplots()
    fig,ax = plt.subplots(figsize=(15,10))

    fig.suptitle('Gap Acceptance', fontsize=24)
    ax.set_title(segment_name[j], fontsize = 15)
    # make a plot
    l1 = ax.plot(X,Y, color = "red", label = "Gap")

    # set x-axis label
    ax.set_xlabel("Time(sec)",fontsize=20)
    # set y-axis label
    ax.set_ylabel("Gap (m)",fontsize=20)

    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    l2 = ax2.plot(X, Z, color = "blue", label = "Speed")
    ax2.set_ylabel("Speed (m/sec)",fontsize=20)
    #ax.legend(loc=4)
    #aax2.legend(loc=5)
    #ax.legend([l1, l2],["Lateral Displacement","Speed"],loc="upper right")
    plt.show()
    # save the plot as a file
    #fig.savefig(save_path+ '/'+segment_name[j]+'.jpg',format='jpeg',dpi=150)


# In[36]:


j=-1
for i in my_address_list:
    j = j+1
    file_name = i[2:-2]
    df = pd.read_excel(file_name)
    print(len(df))
    
    # Get names of indexes for which column 'objX' has negative value
    indexNames = df[ df['objX'] <= 0 ].index
    # Delete these row indexes from dataFrame
    df.drop(indexNames , inplace=True)
    print(len(df))
        
    #df_groupbyFrame = df.groupby('frame no').first()
    df_groupbyFrame = df.groupby(['frame no'], sort=True).first()
    Y = []
    X = []
    Z = []
    for i in range (1, len(df_groupbyFrame)):
        y_axis = abs((df_groupbyFrame.iloc[i,4]))
        Y.append(y_axis)
        x_axis = i/10
        X.append(x_axis)
        z_axis = abs(df_groupbyFrame.iloc[i,21])
        Z.append(z_axis)
        
    # create figure and axis objects with subplots()
    fig,ax = plt.subplots(figsize=(15,10))

    fig.suptitle('Gap Acceptance', fontsize=24)
    ax.set_title(segment_name[j], fontsize = 15)
    # make a plot
    l1 = ax.plot(X,Y, color = "red", label = "Gap")

    # set x-axis label
    ax.set_xlabel("Time(sec)",fontsize=20)
    # set y-axis label
    ax.set_ylabel("Gap (m)",fontsize=20)

    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    l2 = ax2.plot(X, Z, color = "blue", label = "Speed")
    ax2.set_ylabel("Speed (m/sec)",fontsize=20)
    #ax.legend(loc=4)
    #aax2.legend(loc=5)
    #ax.legend([l1, l2],["Lateral Displacement","Speed"],loc="upper right")
    plt.show()
    # save the plot as a file
    #fig.savefig(save_path+ '/'+segment_name[j]+'.jpg',format='jpeg',dpi=150)


# In[57]:


j=-1
for i in my_address_list:
    j = j+1
    file_name = i[2:-2]
    df = pd.read_excel(file_name)
    print(len(df))
    
    # Get names of indexes for which column 'objX' has negative value
    indexNames = df[ df['objX'] <= 0 ].index
    # Delete these row indexes from dataFrame
    df.drop(indexNames , inplace=True)
    print(len(df))
        
    #df_groupbyFrame = df.groupby('frame no').first()
    df_groupbyFrame = df.groupby(['frame no'], sort=True).first()
    Y = []
    X = []
    Z = []
    A = []
    J = []
    for i in range (1, len(df_groupbyFrame)):
        y_axis = abs((df_groupbyFrame.iloc[i,4]))
        Y.append(y_axis)
        x_axis = i/10
        X.append(x_axis)
        z_axis = abs(df_groupbyFrame.iloc[i,22])
        Z.append(z_axis)
        Acceleration = df_groupbyFrame.iloc[i,22] - df_groupbyFrame.iloc[(i-1),22]
        Acceleration = Acceleration/0.1
        A.append(Acceleration)
        #Jerk = A[i]-A[i-1]
        #Jerk = Jerk/0.1
        #J.append(Jerk)
        
    # create figure and axis objects with subplots()
    fig,ax = plt.subplots(figsize=(15,10))

    fig.suptitle('Gap Acceptance', fontsize=24)#, pad = 20 )
    #ax.set_title(segment_name[j], fontsize = 15)
    ax.set_title(segment_name[j] +"      Maximum Deceleration: "+ str(min(A)), fontsize = 15, loc = 'left')
    
    
    #ax.set_title('Gap Acceptance', fontsize=24, pad =40)
    #fig.suptitle("Maximum Deceleration: "+ str(min(A)), fontsize = 20)
    #ax.text(2,2,"Maximum Deceleration: "+ str(min(A)))
    #fig.text("Maximum Jerk: " + min(J))
    
    # make a plot
    l1 = ax.plot(X,Y, color = "red", label = "Gap")

    # set x-axis label
    ax.set_xlabel("Time(sec)",fontsize=20)
    # set y-axis label
    ax.set_ylabel("Gap (m)",fontsize=20)

    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    l2 = ax2.plot(X, Z, color = "blue", label = "Speed")
    ax2.set_ylabel("Speed (m/sec)",fontsize=20)
    #ax.legend(loc=4)
    #aax2.legend(loc=5)
    #ax.legend([l1, l2],["Lateral Displacement","Speed"],loc="upper right")
   # ax3 = ax.twiny()
    #ax3.set_xlabel(segment_name[j], fontsize = 15)
    plt.show()
    # save the plot as a file
    #fig.savefig(save_path+ '/'+segment_name[j]+'.jpg',format='jpeg',dpi=150)
    fig.savefig(save_path+'\jpeg\Y'+'\GapAcceptance'+segment_name[j]+'.jpg',format='jpeg',dpi=150)


# In[ ]:





# In[21]:


i = my_address_list[0]
file_name = i[2:-2]

df = pd.read_excel(file_name)
df
print(len(df))


# In[22]:


df = df.loc[(df['objY'] <= tolerance) & 
                    (df['objY'] > -1*tolerance)]
print(len(df))


# In[23]:


#df.iloc[1,4]
#df =- df[df$objX >= 0, ]
#df = df[df['objX'] >= 0]
# Get names of indexes for which column Age has value 30
indexNames = df[ df['objX'] <= 0 ].index
# Delete these row indexes from dataFrame
df.drop(indexNames , inplace=True)

print(len(df))
df


# In[25]:





# In[28]:


df_groupbyFrame = df.groupby(['frame no'], sort=True).first()


# In[29]:


df_groupbyFrame


# In[31]:


df_groupbyFrame.iloc[1,3]


# In[32]:


Y = []
X = []
Z = []
for i in range (1, len(df_groupbyFrame)):
    y_axis = (df_groupbyFrame.iloc[i,3])
    print(y_axis)
    Y.append(y_axis)
    x_axis = i/10
    X.append(x_axis)
    z_axis = df_groupbyFrame.iloc[i,21]
    Z.append(z_axis)
        
# create figure and axis objects with subplots()
fig,ax = plt.subplots(figsize=(15,10))

fig.suptitle('Lane Change Dynamics', fontsize=24)
ax.set_title(segment_name[j], fontsize = 15)
# make a plot
l1 = ax.plot(X,Y, color = "red", label = "Headway")

# set x-axis label
ax.set_xlabel("Time(sec)",fontsize=20)
# set y-axis label
ax.set_ylabel("Headway (m)",fontsize=20)

# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
l2 = ax2.plot(X, Z, color = "blue", label = "Speed")
ax2.set_ylabel("Speed (m/sec)",fontsize=20)
#ax.legend(loc=4)
#aax2.legend(loc=5)
#ax.legend([l1, l2],["Lateral Displacement","Speed"],loc="upper right")
plt.show()


# indexNames = df[ df['objX'] >= 0 ].index
# # Delete these row indexes from dataFrame
# df.drop(indexNames , inplace=True)
# 
# print(len(df))
# df

# In[ ]:





# In[ ]:
