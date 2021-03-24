# -*- coding: utf-8 -*-
"""BoVW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oeKcdt754KzS5QLn5avjy_xQQjzI8j5s
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
import cv2
import random
import math
import os
import time, sys
import pickle
# %matplotlib inline

from google.colab import drive
drive.mount('/content/drive')

File="/content/drive/My Drive/Deeplearning/Group31_Assignment1/"

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10, 10)

def printProgressBar(i,max,postText):
    n_bar =70 #size of progress bar
    j= (i+1)/max
    sys.stdout.write('\r')
    sys.stdout.write(f"{i+1}/{max}[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = mpimg.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def load_images_from_folder(sigmoid,folder):
    
    images = []
    y=[]
    
    if sigmoid:
        oneHot1=[1.0,-1.0,-1.0]
        oneHot2=[-1.0,1.0,-1.0]
        oneHot3=[-1.0,-1.0,1.0]
        
    else:
        oneHot1=[1.0,0.0,0.0]
        oneHot2=[0.0,1.0,0.0]
        oneHot3=[0.0,0.0,1.0]
    
    Folder=[]
    for filename in os.listdir(folder):
        if not filename.startswith('.'):
            Folder.append(folder+filename)
    File=[os.listdir(filename) for filename in Folder]
#     print(File)
    
    i=0
    
    for  filename in Folder:
#         print(i)
        i=i+1
        
        for file in os.listdir(filename):
    
        
            if not file.startswith('.'):
                img = cv2.imread(filename+'/'+file)
                
                if img is not None:
                    images.append(img)
                    if i==1:
                        y.append(oneHot1)
                    elif i==2:
                        y.append(oneHot2)
                    elif i==3:
                        y.append(oneHot3)
            
    return images, np.array(y)

sigmoid=1
train_img,train_label=load_images_from_folder(sigmoid,File+"Group31/Classification/Image_Group31/train/")

test_img,test_label=load_images_from_folder(sigmoid,File+"Group31/Classification/Image_Group31/test/")

x=20
print(train_label[x])
plt.imshow(train_img[x])

def find_paches(image):
    
    W=32
    
    a=W-int(image.shape[0]%W)
    b=W-int(image.shape[1]%W)

    for i in range(a):
        image=np.append(image, image[-1:], axis=0)

    for i in range(b):
        image=np.append(image, image[:,-1:], axis=1)
        
    patches1=[]
    patches2=[]
    patches3=[]

    height,width,channel=image.shape
#     print(str(height)+' , '+str(width))

    for c in range(channel): 
        for i in range(0,height,W):

            for j in range(0,width,W):

                if c==0:
                    patches1.append(image[i:i+W,j:j+W,c])
                elif c==1:
                    patches2.append(image[i:i+W,j:j+W,c])
                else:
                    patches3.append(image[i:i+W,j:j+W,c])
                    
                
    return patches1,patches2,patches3

l1,l2,l3=find_paches(train_img[12])

plt.imshow(l1[0])

i=30
rgb = np.dstack((l1[i],l2[i],l3[i]))
plt.imshow(rgb)

# histogram, bin_edges = np.histogram(l1[1], bins=8, range=(0, 255))

def histogram(img, bins,ranges):
    W=32
    nums=int(ranges/bins)

    histogram=np.zeros(bins)
    for i in range(W):
        for j in range(W):

            count=img[i][j]
            l=0
            m=0
            for k in range(nums, ranges+1,nums):
                if count>=l and count < k:
                    histogram[m]=histogram[m]+1
                l=k
                m=m+1
    return histogram

def patch_histogram(l1,l2,l3):
    
    length=len(l1)
    features=[]
    
    for i in range(length):
        histogram1=histogram(l1[i],8,256)
        histogram2=histogram(l2[i],8,256)
        histogram3=histogram(l3[i],8,256)
        his=np.append(histogram1,histogram2)
        his=np.append(his,histogram3)
        features.append(his)
    
    return features

patch_hist=patch_histogram(l1,l2,l3)

x=40
patch_hist[x]

plt.bar([i for i in range(len(patch_hist[x]))],patch_hist[x])

def feature_vector_all_imgs(images):
    
    hist_all_imgs=[]
    
    for i in range(len(images)):
        printProgressBar(i,len(images),'Completed')
        l1,l2,l3=find_paches(images[i])
    
        hist_all_imgs.append(patch_histogram(l1,l2,l3))
        
    return hist_all_imgs

def k_mean(all_img):
    means=np.array([[random.seed(i+j) or random.randint(0, 1024) for i in range(24)] for j in range(32)])

    iteration=10
    for k in range(iteration):
        
        printProgressBar(k,iteration,'Completed')


        

        label=[1024 for i in range(32)]
        cluster=[[] for i in range(32)]

        for i in range(all_img.shape[0]):
            for j in range(32):
                euclidean=means[j]-all_img[i]
                euclidean=np.sqrt(np.sum(euclidean*euclidean))
                label[j]=euclidean

            cluster[np.argmin(label)].append(list(all_img[i]))

        
        for i in range(32):

            if cluster[i] !=  []:
                means[i]=np.mean(cluster[i],axis=0)

        
        
    return means



# hist_all_imgs=feature_vector_all_imgs(train_img[:])

# hist_test_imgs=feature_vector_all_imgs(test_img[:])

# hist_all_con=np.concatenate(hist_all_imgs)

# with open(File+'Saved/hist_all', 'wb') as fp:
#     pickle.dump(hist_all_imgs, fp)



# with open(File+'Saved/hist_test_imgs', 'wb') as fp:
#     pickle.dump(hist_test_imgs, fp)

# means=k_mean(hist_all)

# with open('means', 'wb') as fp:
#     pickle.dump(means, fp)



with open (File+'Saved/means', 'rb') as fp:
    means_saved = pickle.load(fp)

with open (File+'Saved/hist_all', 'rb') as fp:
    train_saved = pickle.load(fp)

with open (File+'Saved/hist_test_imgs', 'rb') as fp:
    test_saved = pickle.load(fp)

def create_bags(means,img):


    label=[1024 for i in range(32)]
    cluster=[0 for i in range(32)]



    for i in range(len(img)):
        for j in range(32):
            euclidean=means[j]-img[i]
            euclidean=np.sqrt(np.sum(euclidean*euclidean))
            label[j]=euclidean


        cluster[np.argmin(label)]=cluster[np.argmin(label)]+1

       
        
    return cluster

def find_codebook(means, images):

  codebook=[]

  for i in range(len(images)):

    printProgressBar(i,len(images),'Completed')
    
    code=create_bags(means,images[i])
    codebook.append(code)

  return codebook

codebook_train=find_codebook(means_saved,train_saved)

codebook_test=find_codebook(means_saved,test_saved)

def label_bags(codebook,data,label):

  book=codebook.copy()

  for i in range(len(book)):

    length=len(data[i])
    book[i]=[x/length for x in book[i]]

  normalized_arr = preprocessing.normalize(book)

  bags=[]
  for i in range(len(label)):

    c=book[i]
    bags.append(np.concatenate((np.array([1]),np.array(c[:]),label[i]),axis=0))

  return bags

bags_train=label_bags(codebook_train,train_saved,train_label)

bags_test=label_bags(codebook_test,test_saved,test_label)

x=1
plt.bar([i for i in range(len(bags_train[x][:-3]))],bags_train[x][:-3])



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
        weight=np.array([[random.seed(i+j) or random.random() for i in range(archicture[h]+1)] for j in range(archicture[h+1])])
        weights.append(weight)
        
    Error_epoch=list()
    
    
    
    for j in range(epoch):
        
        
        output=list()
        expected=list()
        np.random.shuffle(data)
        
        for i in range(len(data)):
            
            input_data=np.copy(data[i][:-3])
            
            network_outputs=[]
            network_outputs.append(input_data) 
            
            #Calculation of the weighted sum at the every layer of the neural network
            for h in range(len(archicture)-1):
                output_vector=perceptron(weights[h],input_data,sigmoid)
                input_data=np.concatenate(([1],output_vector))
                network_outputs.append(input_data) 
           
            #Send the data for backpropogation 
            target=np.copy(data[i][-3:])
            weights=back_propagate(archicture,target,network_outputs,weights, learning_rate,sigmoid) 
            output.append(network_outputs[-1][1:])
            expected.append(list(data[i][-3:]))
            
            
        #Calculate the MSE for the every epoch  
        error_output=np.array(expected)-np.array(output)
        cost=(np.sum(error_output*error_output,axis=0)/len(error_output))
        Etotal=np.sum(cost)
        Error_epoch.append(Etotal)
        
        #print the error of every output neuron in every 100 epochs
        if (j+1)%100==0 or j==0:
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
    
    inputss=np.copy(np.array(data))
    error_output,weights=network(inputss,archicture,epoch,sigmoid,learning_rate)
    
    plt.plot(error_output)
    plt.xlabel("Epochs")  
    plt.ylabel("Error") 
    plt.title("Error Plot")  
    plt.show()
    
    
    return weights

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
    
    
    return M,V





#archicture[no_of_input,no_of_neuron_h1,no_of_neuron_h2,no_of_output]
#archicture[no_of_input,no_of_neuron_h1,no_of_output]
#sigmoid=0 means logistic and sigmoid=1 means tanh


archicture=[32,10,3]
sigmoid=1
learning_rate=0.1
epoch=1000
k=1 # k=1, 2, 3, 4 for the cross validation, where 1 is Fold-1

Train,Validation=cross_validation(k,bags_train)

#Send to the classifier
Weights=classifier(Train,archicture,epoch,sigmoid,learning_rate)



test(np.array(Train),archicture,Weights,sigmoid,'Training Accuracy')

test(np.array(Validation),archicture,Weights,sigmoid,'Validation Accuracy')

test(np.array(bags_test),archicture,Weights,sigmoid,'Testing Accuracy')

