'''
*****************************************************************************************
*
*        		===============================================
*           		GeoGuide(GG) Theme (eYRC 2023-24)
*        		===============================================
*
*  This script is to implement Task 1A of GeoGuide(GG) Theme (eYRC 2023-24).
*  
*  This software is made availabl+e on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ GG_1613 ]
# Author List:		[Diya Chaudhary, Divyansh Singhal, Shaarun Eswar, Vartika Sharma ]
# Filename:			task_1a.py
# Functions:	    [`ideantify_features_and_targets`, `load_as_tensors`,
# 					 `model_loss_function`, `model_optimizer`, `model_number_of_epochs`, `training_function`,
# 					 `validation_functions` ]

####################### IMPORT MODULES #######################
import pandas as pd
import torch
import numpy as np
###################### Additional Imports ####################
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import StepLR

'''
You can import any additional modules that you require from 
torch, matplotlib or sklearn. 
You are NOT allowed to import any other libraries. It will 
cause errors while running the executable
'''
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

##############################################################

def data_preprocessing(task_1a_dataframe):

	''' 
	Purpose:
	---
	This function will be used to load your csv dataset and preprocess it.
	Preprocessing involves cleaning the dataset by removing unwanted features,
	decision about what needs to be done with missing values etc. Note that 
	there are features in the csv file whose values are textual (eg: Industry, 
	Education Level etc)These features might be required for training the model
	but can not be given directly as strings for training. Hence this function 
	should return encoded dataframe in which all the textual features are 
	numerically labeled.
	
	Input Arguments:
	---
	`task_1a_dataframe`: [Dataframe]
						  Pandas dataframe read from the provided dataset 	  
	
	Returns:
	---
	`encoded_dataframe` : [Dataframe]
						  Pandas dataframe that has all the features mapped to 
						  numbers starting from zero

	Example call:
	---
	encoded_dataframe = data_preprocessing(task_1a_dataframe)
	'''

	#################	ADD YOUR CODE HERE	##################
	label_encoders = {}
	categorical_columns = ['Education', 'City', 'EverBenched', 'Gender']

	for col in categorical_columns:
		L = LabelEncoder()
		task_1a_dataframe[col] = L.fit_transform(task_1a_dataframe[col])
		encoded_dataframe = task_1a_dataframe
	
	##########################################################

	return encoded_dataframe

def identify_features_and_targets(encoded_dataframe):
	'''
	Purpose:
	---
	The purpose of this function is to define the features and
	the required target labels. The function returns a python list
	in which the first item is the selected features and second 
	item is the target label

	Input Arguments:
	---
	`encoded_dataframe` : [ Dataframe ]
						Pandas dataframe that has all the features mapped to 
						numbers starting from zero
	
	Returns:
	---
	`features_and_targets` : [ list ]
							python list in which the first item is the 
							selected features and second item is the target label

	Example call:
	---
	features_and_targets = identify_features_and_targets(encoded_dataframe)
	'''

	#################	ADD YOUR CODE HERE	##################
	X = encoded_dataframe.iloc[:,0:7]
	y = encoded_dataframe.LeaveOrNot

	features_and_targets = [X, y]
	##########################################################

	return features_and_targets


def load_as_tensors(features_and_targets):
    ''' 
    Purpose:
    ---
    This function aims at loading your data (both training and validation)
    as PyTorch tensors. Here you will have to split the dataset for training 
    and validation, and then load them as as tensors. 
    Training of the model requires iterating over the training tensors. 
    Hence the training sensors need to be converted to iterable dataset
    object.
    
    Input Arguments:
    ---
    `features_and_targets` : [ list ]
                            python list in which the first item is the 
                            selected features and second item is the target label
    
    Returns:
    ---
    `tensors_and_iterable_training_data` : [ list ]
                                            Items:
                                            [0]: X_train_tensor: Training features loaded into Pytorch array
                                            [1]: X_test_tensor: Feature tensors in validation data
                                            [2]: y_train_tensor: Training labels as Pytorch tensor
                                            [3]: y_test_tensor: Target labels as tensor in validation data
                                            [4]: Iterable dataset object and iterating over it in 
                                                 batches, which are then fed into the model for processing
    Example call:
    ---
    tensors_and_iterable_training_data = load_as_tensors(features_and_targets)
    '''
    
    features_df = features_and_targets[0]
    target_df = features_and_targets[1]
    
    features_scaled = MinMaxScaler().fit_transform(features_df)
    X = torch.tensor(features_df.values, dtype=torch.float32)
    y = torch.tensor(target_df.values, dtype=torch.float32)

    X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor = train_test_split(X, y, test_size=0.2, random_state=42)

    tensors_and_iterable_training_data = [X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor]

    return tensors_and_iterable_training_data



class Salary_Predictor(nn.Module):
    '''
    Purpose:
    ---
    The architecture and behavior of your neural network model will be
    defined within this class that inherits from nn.Module. Here you
    also need to specify how the input data is processed through the layers. 
    It defines the sequence of operations that transform the input data into 
    the predicted output. When an instance of this class is created and data
    is passed through it, the `forward` method is automatically called, and 
    the output is the prediction of the model based on the input data.
    
    Returns:
    ---
    `predicted_output` : Predicted output for the given input data
    '''
    
    def __init__(self):
        super(Salary_Predictor, self).__init__()
        '''
        Define the type and number of layers
        '''
        #######    ADD YOUR CODE HERE    #######
        self.fc1 = nn.Linear(7, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 16)
        self.fc4 = nn.Linear(16, 1)

        # self.fc1 = nn.Linear(7, 64)
        # self.fc2 = nn.Linear(64, 32)
        # self.fc3 = nn.Linear(32, 1)
        self.dropout = nn.Dropout(0.2)

        # self.bn1 = nn.BatchNorm1d(240)
        # self.bn2 = nn.BatchNorm1d(128)
        # self.bn3 = nn.BatchNorm1d(64)
        
        # self.dropout1 = nn.Dropout(0.2)
        # self.dropout2 = nn.Dropout(0.2)
        # self.dropout3 = nn.Dropout(0.2)
        ###################################    

    def forward(self, x):
        '''
        Define the activation functions
        '''
        #######    ADD YOUR CODE HERE    #######
        # x = F.leaky_relu(self.fc1(x), negative_slope=0.01)
        # x = self.dropout1(x)
        # x = F.leaky_relu(self.fc2(x), negative_slope=0.01)
        # x = self.dropout2(x)
        # x = F.sigmoid(self.fc3(x))
        # x = self.dropout3(x)
        # x = torch.sigmoid(self.fc4(x))

        x = F.leaky_relu(self.fc1(x), negative_slope=0.01)
        x = self.dropout(x)
        x = F.sigmoid(self.fc2(x))
        x = self.dropout(x)
        x = torch.sigmoid(self.fc3(x))
        #predicted_output = x
        ###################################

        return x


def model_loss_function(outputs, targets):
    '''
    Purpose:
    ---
    To define the loss function for the model. Loss function measures 
    how well the predictions of a model match the actual target values 
    in training data.
    
    Input Arguments:
    ---
    None

    Returns:
    ---
    `loss_function`: This can be a pre-defined loss function in PyTorch
                    or can be user-defined

    Example call:
    ---
    loss_function = model_loss_function()
    '''
    
    #################    ADD YOUR CODE HERE    ##################
    criterion = nn.BCELoss()
    loss_function = criterion(outputs, targets)
    ##########################################################
    
    return loss_function


def model_optimizer(model):
    '''
    Purpose:
    ---
    To define the optimizer for the model. Optimizer is responsible 
    for updating the parameters (weights and biases) in a way that 
    minimizes the loss function.
    
    Input Arguments:
    ---
    `model`: An object of the 'Salary_Predictor' class

    Returns:
    ---
    `optimizer`: Pre-defined optimizer from Pytorch

    Example call:
    ---
    optimizer = model_optimizer(model)
    '''
    #################    ADD YOUR CODE HERE    ##################
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=0.01)
    scheduler = StepLR(optimizer, step_size=50, gamma=0.5)
    
    return optimizer, scheduler


def model_number_of_epochs():
	'''
	Purpose:
	---
	To define the number of epochs for training the model

	Input Arguments:
	---
	None

	Returns:
	---
	`number_of_epochs`: [integer value]

	Example call:
	---
	number_of_epochs = model_number_of_epochs()
	'''
	#################	ADD YOUR CODE HERE	##################
	number_of_epochs = 100
	##########################################################

	return number_of_epochs

def training_function(model, number_of_epochs, tensors_and_iterable_training_data, loss_function, optimizer, scheduler):
    '''
    Purpose:
    ---
    All the required parameters for training are passed to this function.

    Input Arguments:
    ---
    1. `model`: An object of the 'Salary_Predictor' class
    2. `number_of_epochs`: For training the model
    3. `tensors_and_iterable_training_data`: list containing training and validation data tensors 
                                             and iterable dataset object of training tensors
    4. `loss_function`: Loss function defined for the model
    5. `optimizer`: Optimizer defined for the model

    Returns:
    ---
    trained_model

    Example call:
    ---
    trained_model = training_function(model, number_of_epochs, iterable_training_data, loss_function, optimizer)

    '''    
    #################    ADD YOUR CODE HERE    ##################
    batch_size = 16
    X_train_tensor = tensors_and_iterable_training_data[0]
    y_train_tensor = tensors_and_iterable_training_data[2]
    X_val_tensor = tensors_and_iterable_training_data[1]
    y_val_tensor = tensors_and_iterable_training_data[3]

    early_stopping_patience = 10  # Number of epochs to wait for improvement
    no_improvement_count = 0  # Initialize the counter
    best_val_loss = float('inf')
    
    for epoch in range(number_of_epochs):
        for i in range(0, len(X_train_tensor), batch_size):
            X_batch = X_train_tensor[i:i + batch_size]
            outputs = model(X_batch)
            y_batch = y_train_tensor[i:i + batch_size].view(-1, 1)
            loss = loss_function(outputs, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        scheduler.step()

        val_outputs = model(X_val_tensor)
        val_loss = loss_function(val_outputs, y_val_tensor.view(-1, 1))

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        if no_improvement_count >= early_stopping_patience:
            break

    trained_model = model
    ##########################################################

    return trained_model



def validation_function(trained_model, tensors_and_iterable_training_data):
    '''
    Purpose:
    ---
    This function will utilize the trained model to do predictions on the
    validation dataset. This will enable us to understand the accuracy of
    the model.

    Input Arguments:
    ---
    1. `trained_model`: Returned from the training function
    2. `tensors_and_iterable_training_data`: list containing training and validation data tensors 
                                             and iterable dataset object of training tensors

    Returns:
    ---
    model_accuracy: Accuracy on the validation dataset

    Example call:
    ---
    model_accuracy = validation_function(trained_model, tensors_and_iterable_training_data)

    '''    
    #################    ADD YOUR CODE HERE    ##################
    model.eval()

    X_val = tensors_and_iterable_training_data[1]
    y_val = tensors_and_iterable_training_data[3]
    with torch.no_grad():
        outputs = trained_model(X_val)
        predicted_labels = (outputs >= 0.5).float()
        correct = (predicted_labels == y_val.view(-1, 1)).sum().item()
        total = len(y_val)
        model_accuracy = correct / total 
    ##########################################################

    return model_accuracy


########################################################################
########################################################################
######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	
'''
	Purpose:
	---
	The following is the main function combining all the functions
	mentioned above. Go through this function to understand the flow
	of the script

'''
if __name__ == "__main__":

	# reading the provided dataset csv file using pandas library and 
	# converting it to a pandas Dataframe
	task_1a_dataframe = pd.read_csv('task_1a_dataset.csv')

	# data preprocessing and obtaining encoded data
	encoded_dataframe = data_preprocessing(task_1a_dataframe)

	# selecting required features and targets
	features_and_targets = identify_features_and_targets(encoded_dataframe)

	# obtaining training and validation data tensors and the iterable
	# training data object
	tensors_and_iterable_training_data = load_as_tensors(features_and_targets)
	
	# model is an instance of the class that defines the architecture of the model
	model = Salary_Predictor()

	# obtaining loss function, optimizer and the number of training epochs
	# loss_function = model_loss_function()
	optimizer, scheduler = model_optimizer(model)
	number_of_epochs = model_number_of_epochs()

	# training the model
	trained_model = training_function(model, number_of_epochs, tensors_and_iterable_training_data, model_loss_function, optimizer, scheduler)

	# validating and obtaining accuracy
	model_accuracy = validation_function(trained_model,tensors_and_iterable_training_data)
	print(f"Accuracy on the test set = {model_accuracy}")

	X_train_tensor = tensors_and_iterable_training_data[0]
	x = X_train_tensor[0]
	jitted_model = torch.jit.save(torch.jit.trace(model, (x)), "task_1a_trained_model.pth")