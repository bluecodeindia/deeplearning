# -*- coding: utf-8 -*-
"""NonLinearlySeperableDataWithMLFFN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14KeI1KOyHZ58FTHyI4HPEJs8JXBk03ca
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
# %matplotlib inline

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10, 10)

from google.colab import drive
drive.mount('/content/drive')

File="/content/drive/My Drive/Deeplearning/Group31_Assignment1/"

def readData(Folder,file):
    data=pd.read_csv(Folder+"/"+str(file)+".txt"," ",header=None)
    data=np.array(data.values)
    return data

def train_test_split(arr, sigmoid, test,OneHot):
    
    w=np.full(len(arr),1)
    
    if sigmoid:
        x=np.full(len(arr),1 if OneHot ==1 else -1)
        y=np.full(len(arr),1 if OneHot ==2 else -1)
        z=np.full(len(arr),1 if OneHot ==3 else -1)
        
    else:
        x=np.full(len(arr),1 if OneHot ==1 else 0)
        y=np.full(len(arr),1 if OneHot ==2 else 0)
        z=np.full(len(arr),1 if OneHot ==3 else 0)
        
    
    train=     np.array([w[:-int(len(arr)*(test))],arr[:-int(len(arr)*(test)),0],arr[:-int(len(arr)*(test)),1],x[:-int(len(arr)*(test))],y[:-int(len(arr)*(test))],z[:-int(len(arr)*(test))]])
    test=      np.array([w[-int(len(arr)*test): ],arr[-int(len(arr)*test): ,0],arr[-int(len(arr)*test): ,1],x[-int(len(arr)*test): ],y[-int(len(arr)*test): ],z[-int(len(arr)*test): ]])
    
    return train.T, test.T

def plot_data(red,green, blue,title):
    plt.scatter(red[0],red[1],color='red')
    plt.scatter(green[0],green[1],color='green')
    plt.scatter(blue[0],blue[1],color='blue')
    plt.title(title)
    plt.savefig(title)
    plt.show()

def plot_all_data(file):
    
    Folder=[file+"Group31/Classification/NLS_Group31"]
#     plt.rcParams['axes.facecolor']='w'

    for k in Folder:

        folder=k
        red=  readData(k,'Class1')
        green=readData(k,'Class2')
        blue= readData(k,'Class3')
        
    plt.scatter(red[:,0],red[:,1],marker='D',color='#EAA358',edgecolors='black')
    plt.scatter(green[:,0],green[:,1],marker='X',color='#65993a',edgecolors='black')
    plt.scatter(blue[:,0],blue[:,1],marker='o',color='#4486B7',edgecolors='black')
    plt.xlabel("x1")  # add X-axis label 
    plt.ylabel("x2") 
    plt.savefig('data.png',bbox_inches = 'tight')
    plt.show()

plot_all_data(File)

def data_format(sigmoid,file):
    
    Folder=[file+"Group31/Classification/NLS_Group31"]

    for k in Folder:

        folder=k
        red=  readData(k,'Class1')
        green=readData(k,'Class2')
        blue= readData(k,'Class3')

        red,      test_red=  train_test_split(red, sigmoid, 0.20,1)
        green,  test_green=  train_test_split(green,sigmoid,0.20,2)
        blue,    test_blue=  train_test_split(blue,sigmoid ,0.20,3)
    
    data=np.concatenate((red,green,blue))
    data_size=[len(red),len(green),len(blue)]
    y=np.concatenate((np.full(len(red), 0),  np.full(len(green),1),np.full(len(blue),2)))
    
    test_data=np.concatenate((test_red,test_green,test_blue))
    test_size=[len(test_red),len(test_green),len(test_blue)]
    test_y=np.concatenate((np.full(len(test_red), 0),  np.full(len(test_green),1),np.full(len(test_blue),2)))
    
    return data,data_size,test_data,test_size

# Decision boundary
def generate_values_boundary(data,data_size,archicture,weights,sigmoid,ttl):
    min_x=min(data[:,1])
    max_x=max(data[:,1])
    min_y=min(data[:,2])
    max_y=max(data[:,2])

    x_mesh = np.linspace(min_x-1, max_x+1, 500)
    y_mesh = np.linspace(min_y-1 ,max_y+1, 500)

    red_bound = [];
    green_bound = [];
    blue_bound = [];
    for i in range(x_mesh.size):
            for j in range(y_mesh.size):
                
                input_data=np.copy(np.array([1,x_mesh[i],y_mesh[j]]))
                
                for h in range(len(archicture)-1):

                    output_vector=perceptron(weights[h],input_data,sigmoid)
                    input_data=np.concatenate(([1],output_vector))
                    
                a=np.argmax(output_vector)
                

                if (a==0):
                    red_bound.append([x_mesh[i], y_mesh[j]])
                elif (a==1):
                    green_bound.append([x_mesh[i], y_mesh[j]])
                elif (a==2):
                    blue_bound.append([x_mesh[i], y_mesh[j]])
                    
    boundR = np.asarray(red_bound)
    boundG = np.asarray(green_bound)
    boundB = np.asarray(blue_bound)
    if(boundR.size==0):
        boundR = np.asarray([[0, 0],[0, 0]])
    if(boundG.size==0):
        boundG = np.asarray([[0, 1],[0, 0]])
    if(boundB.size==0):
        boundB = np.asarray([[1, 0],[0, 0]])


    plt.scatter(boundR[:,0], boundR[:,1], color='#99C2DE')
    plt.scatter(boundG[:,0], boundG[:,1], color='#FFC593')
    plt.scatter(boundB[:,0], boundB[:,1], color='#75993a')
    
    plt.scatter(data[:data_size[0],1],data[:data_size[0],2],marker='D',color='#EAA358',edgecolors='black')
    plt.scatter(data[data_size[0]:data_size[0]+data_size[1],1],data[data_size[0]:data_size[0]+data_size[1],2],marker='X',color='#65993a',edgecolors='black')
    plt.scatter(data[data_size[0]+data_size[1]:,1],data[data_size[0]+data_size[1]:,2],marker='o',color='#4486B7',edgecolors='black')
    plt.title(ttl)
    plt.xlabel("x1")  # add X-axis label 
    plt.ylabel("x2") 
    plt.savefig(ttl+'.png',bbox_inches = 'tight')
    plt.show()

def test(test_data,archicture,weights,sigmoid,ttl):   
    cls=3  
  
    # Confusion Matrix
    confusion = np.zeros((3,3))
    network_outputs=[]
    for i in range(test_data.shape[0]):

        z=np.argmax(test_data[i][-3:])
        input_data=np.copy(test_data[i][:-3])
        
        
        for h in range(len(archicture)-1):

            output_vector=perceptron(weights[h],input_data,sigmoid)
            network_outputs.append(output_vector)
            input_data=np.concatenate(([1],output_vector))

        a=np.argmax(output_vector)


        

        if z==0:
            confusion[0][a]=confusion[0][a]+1
        if z==1:
            confusion[1][a]=confusion[1][a]+1
        if z==2:
            confusion[2][a]=confusion[2][a]+1
                
           
    # Accuracy
    acc = (confusion[0][0]+confusion[1][1]+confusion[2,2])/np.sum(confusion.flatten())*100

    # Recall
    rec1 = (confusion[0][0])/(confusion[0][0]+(confusion[0][1])+(confusion[0][2]))*100
    rec2 = (confusion[1][1])/(confusion[1][0]+(confusion[1][1])+(confusion[1][2]))*100
    rec3 = (confusion[2][2])/(confusion[2][0]+(confusion[2][1])+(confusion[2][2]))*100
    avg_rec = (rec1 + rec2 + rec3)/3

    # Precision
    prec1 = (confusion[0][0])/(confusion[0][0]+(confusion[1][0])+(confusion[2][0]))*100
    prec2 = (confusion[1][1])/(confusion[0][1]+(confusion[1][1])+(confusion[2][1]))*100
    prec3 = (confusion[2][2])/(confusion[0][2]+(confusion[1][2])+(confusion[2][2]))*100
    avg_prec = (prec1 + prec2 + prec3)/3

    #F-score
    fscore1 = 2*(prec1 * rec1)/(prec1 + rec1)
    fscore2 = 2*(prec2 * rec2)/(prec2 + rec2)
    fscore3 = 2*(prec3 * rec3)/(prec3 + rec3)
    avg_fscore = (fscore1 + fscore2 + fscore3)/3
    print()
    print('--------------------------------------')
    print (ttl)
    print('--------------------------------------')
    print()
    print ('Confusion Matrix \n')
    print (confusion)
    print(' ')
    print('Accuracy '+str(acc))

    print ('\n\nRecall (C1) : ', rec1)
    print ('Recall (C2) : ', rec2)
    print ('Recall (C3) : ', rec3)
    print ('Average Recall : ', avg_rec)

    print ('\n\nPrecision (C1) : ', prec1)
    print ('Precision (C2) : ', prec2)
    print ('Precision (C3) : ', prec3)
    print ('Average Precision : ', avg_prec)

    print ('\n\nF-Score (C1) : ', fscore1)
    print ('F-Score (C2) : ', fscore2)
    print ('F-Score (C3) : ', fscore3)
    print ('Average F-Score : ', avg_fscore)
    
    
    return network_outputs



def logistic(input):
    x=np.array(input,dtype=np.float128)
    return 1/(1+np.exp(-x))

def perceptron(weights,input,sigmoid):
    
    predict=np.dot(weights,input)
    
    if(sigmoid):
        predict=np.tanh(predict)
        
    else:
        predict=logistic(predict)
        
    return predict

def activation_derivative(x,sigmoid):
    
    if sigmoid:
        t=(np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))
        dt=1-t**2
    
    else:
        dt= x * (1.0 - x)
        
    return dt

def calculate_delta(a,b):
    
    c=np.zeros(a.shape)
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):

            if j!=0:
                c[i][j]=a[i][j]*b[i]
    
    return np.sum(c,axis=0)[1:]

def network(data,archicture,epoch,sigmoid,learning_rate):
    
    weights=[]

    for h in range(len(archicture)-1):
        weight=np.array([[0.1+(i+j)/10 for i in range(archicture[h]+1)] for j in range(archicture[h+1])])
        weights.append(weight)
        
    Error_epoch=list()
    
    
    for j in range(epoch):
        

        output=list()
        expected=list()
        np.random.shuffle(data)
        
        for i in range(len(data)):
            
            input_data=np.copy(data[i][:3])
        
            network_outputs=[]
            network_outputs.append(input_data) 
            
            #Calculation of the weighted sum at the every layer of the neural network
            for h in range(len(archicture)-1):

                output_vector=perceptron(weights[h],input_data,sigmoid)
                input_data=np.concatenate(([1],output_vector))
                network_outputs.append(input_data) 
           
            #Send the data for backpropogation 
            target=np.copy(data[i][3:])  
            weights=back_propagate(archicture,target,network_outputs,weights, learning_rate,sigmoid) 
            output.append(network_outputs[-1][1:])
            expected.append(list(data[i][3:]))
            
            
        #Calculate the MSE for the every epoch  
        error_output=np.array(expected)-np.array(output)
        cost=(np.sum(error_output*error_output,axis=0)/len(error_output))
        Etotal=np.sum(cost)
        Error_epoch.append(Etotal)
        
        #print the error of every output neuron in every 100 epochs
        if  (j+1)%100==0 or j==0:
            print('Epoch',j+1,': ',cost)

        
    
    return Error_epoch,weights

def back_propagate(archicture,target,network_outputs,weights, learning_rate,sigmoid):
    
    Delta=[]
    length=len(archicture)
    
    #Calculate the delta for the final output layer
    Do=-(target-network_outputs[-1:][0][1:])*activation_derivative(network_outputs[-1:][0][1:],sigmoid)
    Delta.append(Do)

    #Claculate the delta for all internal layers
    for h in reversed (range(1,length-1)):
        new_Delta=calculate_delta(weights[h],Delta[-1])
        new_Delta=new_Delta*activation_derivative(network_outputs[h-length][1:],sigmoid)
        Delta.append(new_Delta)
    Delta.reverse()
    
    #Calculate the new updated value for the weights   
    
    k=-1
    for W in weights:
        k=k+1
        for i in range(W.shape[0]):
            for j in range(W.shape[1]):
                W[i][j]=W[i][j]-learning_rate*network_outputs[k][j]*Delta[k][i]
        
    return weights

def classifier(data,archicture,epoch,sigmoid,learning_rate):
    
    error_output,weights=network(np.copy(data),archicture,epoch,sigmoid,learning_rate)
    
    plt.plot(error_output)
    plt.xlabel("Epochs")  # add X-axis label 
    plt.ylabel("Error")  # add Y-axis label 
    plt.title("Error Plot")  # add title 
    plt.savefig('LS_Error.png',bbox_inches = 'tight')


    
    return weights

def cross_validation(k,Arr):

    Arr1=[]
    Arr2=[]
    Arr3=[]
    for i in range(len(Arr)):

      cls=np.argmax(Arr[i][-3:])

      if cls==0:
        Arr1.append(Arr[i])
      if cls==1:
        Arr2.append(Arr[i])
      if cls==2:
        Arr3.append(Arr[i])

    length1=int(len(Arr1)*0.25)
    length2=int(len(Arr2)*0.25)
    length3=int(len(Arr3)*0.25)
    
    M11,M12,M13,M14=Arr1[:length1],Arr1[length1:2*length1],Arr1[2*length1:3*length1],Arr1[3*length1:4*length1]
    M21,M22,M23,M24=Arr2[:length2],Arr2[length2:2*length2],Arr2[2*length2:3*length2],Arr2[3*length2:4*length2]
    M31,M32,M33,M34=Arr3[:length3],Arr3[length3:2*length3],Arr3[2*length3:3*length3],Arr3[3*length3:4*length3]
    
    if k==1:
        M=np.concatenate((M12,M13,M14,M22,M23,M24,M32,M33,M34))
        V=np.concatenate((M11,M21,M31))
    if k==2:
        M=np.concatenate((M11,M13,M14,M21,M23,M24,M31,M33,M34))
        V=np.concatenate((M12,M22,M32))
    if k==3:
        M=np.concatenate((M11,M12,M14,M21,M22,M24,M31,M32,M34))
        V=np.concatenate((M13,M23,M33))
    if k==4:
        M=np.concatenate((M11,M12,M13,M21,M22,M23,M31,M32,M33))
        V=np.concatenate((M14,M24,M34))

    train_s=[len(Arr1)-length1,len(Arr2)-length2,len(Arr3)-length3]
    valid_s=[length1,length2,length3]
    
    
    return M, V, train_s, valid_s

#archicture[no_of_input,no_of_neuron_h1,no_of_neuron_h2,no_of_output]
#archicture[no_of_input,no_of_neuron_h1,no_of_output]
#sigmoid=0 means logistic and sigmoid=1 means tanh

archicture=[2,8,3]
sigmoid=0
learning_rate=0.1
epoch=500
k=1 # k=1, 2, 3, 4 for the cross validation, where 1 is Fold-1

data,train_size,Test,test_size=data_format(sigmoid,File)
Train, Validation, T_size, V_size=cross_validation(k,data)
Weights=classifier(Train,archicture,epoch,sigmoid,learning_rate)

generate_values_boundary(Train,T_size,archicture,Weights,sigmoid,'Training Data')
generate_values_boundary(Validation,V_size,archicture,Weights,sigmoid,'Validation Data')
generate_values_boundary(Test,test_size,archicture,Weights,sigmoid,'Test Data')

output1=test(Train,archicture,Weights,sigmoid,'Training Accuracy')
output2=test(Validation,archicture,Weights,sigmoid,'Validation Accuracy')
output3=test(Test,archicture,Weights,sigmoid,'Testing Accuracy')

def neuron_output(data,output,neuron,hidden,file,ttl):

  plt.rcParams['figure.figsize'] = (20, 30)
  # plt.rcParams['axes.facecolor']='w'
  fig = plt.figure()
  axs=[]
  a=int((neuron/2)+0.5)

  for i in range(neuron):

    b=100*a+20+i+1

    ax = fig.add_subplot(b, projection='3d')
    axs.append(ax)


  # axs=[ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]

  for j in range(len(axs)):
      axs[j].set_xlabel('X Input')
      axs[j].set_ylabel('Y Input')
      axs[j].set_zlabel('Z Output') 

  for j in range(len(axs)):

      for i in range (len(Train)):

          # Data for three-dimensional scattered points
          r=j+1
          l=r-1
          
          zdata = output[2*i+hidden][l:r] #hidden=0 for the hidden layer 1, and hidden=1 for the output layer
          xdata = data[i][1:2]
          ydata = data[i][2:3]
          axs[j].scatter(xdata, ydata, zdata, c=zdata, cmap='autumn',edgecolors='black');


  plt.savefig(file+'Figure/'+ttl+'.png',bbox_inches = 'tight')

neuron_output(Train,output1,8,0,File,'NLS_Hidden_Neuron_Train')

neuron_output(Train,output1,3,1,File,'NLS_Output_Neuron_Train')

