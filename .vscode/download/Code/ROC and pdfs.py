#This is adapted from the excellent article here: 
#   https://towardsdatascience.com/receiver-operating-characteristic-curves-demystified-in-python-bd531a4364d0
#The article is well worth reading as an overview of the relationship between the prediction 
#   probability distributions, the prediction decision threshold, and the ROC curve.
#I suspect there is an issue with the AUC calculation in the plot_roc function (e.g., look at 
#   the final plot), but I have not investigated this. The plots serve their conceptual function 
#   as-is.

#simulating a binary classification problem, create two normally distributed distributions, 
#   one for the "good" class and one for the "bad" class. The "bad" class will have mean = 0.6
#   and the "good" class will have mean = 0.4
import numpy as np
import matplotlib.pyplot as plt

def pdf(x, std, mean):
    cons = 1.0 / np.sqrt(2*np.pi*(std**2))
    pdf_normal_dist = cons*np.exp(-((x-mean)**2)/(2.0*(std**2))) #note typo in the original
    return pdf_normal_dist

x = np.linspace(0, 1, num=100)
good_pdf = pdf(x,0.1,0.4)
bad_pdf = pdf(x,0.1,0.6)

#create a function to plot the distributions
def plot_pdf(good_pdf, bad_pdf, ax):
    ax.fill(x, good_pdf, "g", alpha=0.5)
    ax.fill(x, bad_pdf,"r", alpha=0.5)
    ax.set_xlim([0,1])
    ax.set_ylim([0,5])
    ax.set_title("Probability Distribution", fontsize=14)
    ax.set_ylabel('Counts', fontsize=12)
    ax.set_xlabel('P(X="bad")', fontsize=12)
    ax.legend(["good","bad"])
    
#and plot them
fig, ax = plt.subplots(1,1, figsize=(10,5))
plot_pdf(good_pdf, bad_pdf, ax)
#The x-axis represents the predicted probability that an observation is in the "bad" class. The green
#   pdf represents the probability distribution of the predicted probabilities of the actual "good" 
#   observations, while the red pdf represents the probability distribution of the predicted probabilities
#   of the actual "bad" class. By default, whenever P(X="bad") < 0.5, we are going to predict "good." This 
#   means that every part of the green pdf> 0.5 represents actual "good" observations that we predict to 
#   be "bad." Similarly, every part of the red pdf <0.5 represents actual "bad" observations that we predict
#   to be "good." 
#But we ulimately control the 0.5 threshold. We could instead set the threshold at 0.4. In that case,
#   everything above 0.4 would be predicted to be "bad" and everything below 0.4 would be predicted to be 
#   good. If we did that, think about what would happen to accuracy, TPR, and FPR.

#Using the intuition above about moving the prediciton decision threshold, let's define a function
#   that produces an ROC curve for this dataset
def plot_roc(good_pdf, bad_pdf, ax):
    #Total
    total_bad = np.sum(bad_pdf)
    total_good = np.sum(good_pdf)
    #Cumulative sum
    cum_TP = 0
    cum_FP = 0
    #TPR and FPR list initialization
    TPR_list=[]
    FPR_list=[]
    #Iteratre through all values of x
    for i in range(len(x)):
        #We are only interested in non-zero values of bad
        if bad_pdf[i]>0:
            cum_TP+=bad_pdf[len(x)-1-i]
            cum_FP+=good_pdf[len(x)-1-i]
        FPR=cum_FP/total_good
        TPR=cum_TP/total_bad
        TPR_list.append(TPR)
        FPR_list.append(FPR)
    #Calculating AUC, taking the 100 timesteps into account
    auc=np.sum(TPR_list)/100
    #Plotting final ROC curve
    ax.plot(FPR_list, TPR_list)
    ax.plot(x,x, "--")
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])
    ax.set_title("ROC Curve", fontsize=14)
    ax.set_ylabel('TPR', fontsize=12)
    ax.set_xlabel('FPR', fontsize=12)
    ax.grid()
    ax.legend(["AUC=%.3f"%auc])

#And plot the associated ROC for our data
fig, ax = plt.subplots(1,1, figsize=(5,5)) #note that I changed the figsize so x and y axes are similar
plot_roc(good_pdf, bad_pdf, ax)

#Now let's plot the two graphs next to one another
fig, ax = plt.subplots(1,2, figsize=(6,3)) #I changed the size so things are a bit easier to see in the console
plot_pdf(good_pdf, bad_pdf, ax[0])
plot_roc(good_pdf, bad_pdf, ax[1])
plt.tight_layout()

#Now let's alter the predicted probability pdfs for the two classes. We'll create three variants: in one,
#   the pdfs will be identical; in another, they will be the same as our original distributions; and
#   in the third, they'll be more separated than in our original example.
x = np.linspace(0, 1, num=100)
fig, ax = plt.subplots(3,2, figsize=(8,12)) #I made the plot narrower to preserve symmetry in the ROC
means_tuples = [(0.5,0.5),(0.4,0.6),(0.3,0.7)]
i=0
for good_mean, bad_mean in means_tuples:
    good_pdf = pdf(x, 0.1, good_mean)
    bad_pdf  = pdf(x, 0.1, bad_mean)
    plot_pdf(good_pdf, bad_pdf, ax[i,0])
    plot_roc(good_pdf, bad_pdf, ax[i,1])
    i+=1
plt.tight_layout()

#Each ROC curve corresponds to the class probability distributions to its left. The more separable
#   the actual classes, the faster the TPR rises, and the greater the AUC. So optimizing on AUC is 
#   a way to search for models that provide good TPR/FPR trade-offs. 

