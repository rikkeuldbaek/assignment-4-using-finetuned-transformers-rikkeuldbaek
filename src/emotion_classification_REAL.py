### Language Assignment 4
## Cultural Data Science - Language Analytics 
# Author: Rikke Uldbæk (202007501)
# Date: 13th of April 2023

#--------------------------------------------------------#
################# EMOTION CLASSIFICATION #################
##################### REAL NEWS DATA #####################
#--------------------------------------------------------#

# (please note that some of this code has been adapted from class sessions)

# Install packages
from transformers import pipeline
import pandas as pd
import os
import matplotlib.pyplot as plt

########################## DATA ##########################
file = os.path.join(os.getcwd(), "data", "fake_or_real_news.csv")
data = pd.read_csv(file, index_col=0)


##################### CLASSIFICATION #####################
#Define classifier
classifier = pipeline("text-classification", 
                      model="j-hartmann/emotion-english-distilroberta-base",
                      return_all_scores=True)

# Subset to REAL data only
data = data[data["label"] == "REAL"]

# Running the model on data
max_score_df = [] #contains emotion label with max score for each headline

# Loop
for i in data[["title"]]: 
    for j in data[i]: # loop over all headlines
        emotion = classifier(j) # extract the 7 emotion scores for each headline
        
        # Extract max score 
        for emotion_dicts in emotion: # Loop over emotion dictionaries

            # make emotion dictionaries for each headline into a list
            emotion_list = emotion_dicts #list
            
            # Find emotion with largest score for each headline 
            max_score = max(emotion_list, key=lambda x:x['score']) # max score
            max_score_df.append(max_score) # append to pre existing df


# Overwrite and make max_score_df into a pandas dataframe
max_score_df = pd.DataFrame(max_score_df)

# Count occurrences for each emotion
plot_df =  max_score_df['label'].value_counts()  # count occurrences
plot_df = pd.DataFrame(plot_df) # make a dataframe
plot_df = plot_df.reset_index() # reset index to include label column


####################### PLOTTING #########################
# Create a predefined colour list
colors = {"anger": "red", "fear": "black", "joy": "yellow", "disgust": "green", 
         "neutral": "grey", "surprise": "pink", "sadness": "blue"}

# Creating a bar plot of distribution of emotions across all data
plt.bar(plot_df["label"], plot_df["count"], color=plot_df['label'].map(colors),
        width = 0.4)
plt.xlabel("Emotion labels")
plt.ylabel("Count")
plt.title("Emotion classification for every real news headline", fontsize=10)
plt.suptitle("Distribution of emotions across real news data", fontsize=14)
plt.show()
plt.savefig('out/emotion_distribution_real.png') #save figure in folder "out"

