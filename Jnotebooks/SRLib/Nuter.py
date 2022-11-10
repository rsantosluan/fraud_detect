from sklearn.model_selection import StratifiedShuffleSplit
class nuter(  ):
    ###Cleaning for data
    def data_cleaner( data ):
        '''
        This function, rename all columns
        '''
        ##rename columns
        cols_name = {
        'nameOrig' : 'name_orig', 'oldbalanceOrg' : 'old_balance_orig', 'newbalanceOrig' : 'new_balance_orig', 'nameDest' : 'name_dest',
        'oldbalanceDest' : 'old_balance_dest', 'newbalanceDest' : 'new_balance_dest', 'isFraud' : 'is_fraud', 'isFlaggedFraud' : 'is_flagged_fraud'
        }
        data.rename( columns = cols_name, inplace=True )
        return data
    ###-    

    ###Split Stratified
    def stratified_split (data , feature, validation_size): 
        '''
        data      : Dataset for spliting
        feature   : Characteristic to be analyzed for proportionality
        test_size : Validation Dataset size __-- ex: 0.10, 0.50 ... --__
        '''   
        split = StratifiedShuffleSplit(n_splits=1, test_size = validation_size, random_state = 42)
    
        for train_index, test_index in split.split( data, data[feature] ):
            train_set = data.loc[train_index].reset_index(drop=True)
            validation_set = data.loc[test_index].reset_index(drop=True)
        return train_set, validation_set 

    ###Values ​​in the bar graph
    def plot_values_vbar( ax ):
        for i in ax.patches:
            ax.annotate(
            #Texto a ser plotado
            round(i.get_height()),
            #Posição horizontal
            (i.get_x() + i.get_width() /2, i.get_height() + i.get_height() /80 ),
            ha       = 'center' ,   
            color    = 'black',
            fontsize = 15
    );  
        return None
    


    ###-