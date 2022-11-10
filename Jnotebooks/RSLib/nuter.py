### Essenciais
import pandas as pd

### Save
import pickle as pkl

### ML
from sklearn.preprocessing   import RobustScaler, MinMaxScaler, OneHotEncoder
from sklearn.ensemble        import ExtraTreesClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from xgboost                 import XGBClassifier


class preparacao_dados:

    ### Filtro de dados irrelevante levantados na EDA 1º ciclo
    def filtro_dados( data_raw ):
        data_aux = data_raw[data_raw.type.isin( ['CASH_OUT', 'TRANSFER'] )].copy()

        return data_aux


    ### Feature Engineering
    def feature_eng( data_raw ):
        data_raw['dif_balance_origin'] = data_raw[['oldbalanceOrg', 'newbalanceOrig', 'amount']].apply( lambda x : x['oldbalanceOrg'] - x['amount'] - x['newbalanceOrig'], axis = 1 )        
        data_raw['dif_balance_dest'] = data_raw[['oldbalanceDest', 'newbalanceDest', 'amount']].apply( lambda x : x['oldbalanceDest'] + x['amount'] - x['newbalanceDest'], axis = 1 )

        return data_raw


    ### Normalização dos dados    
    def rescaling( data_raw, rs = '', mms = ''):
        '''
        1- Devido aos outliers, primeiro será aplicado um Robust Scaler (que será treinado e salvo caso não inserido);
        2- Os dados numpericos serão submetidos ao MinMaxScaler;
        '''
        ## Separando numéricos e categóricos
        x_num = data_raw.select_dtypes( include = ['float64', 'int64'] )
        x_cat = data_raw[['type']].copy()

        ###--- Robust Scaler ---###
        if rs == '':
            rs = RobustScaler().fit( x_num )
            pkl.dump( rs, open( '../data/pickle/rescaling/robust_scaler.sav', 'wb' ) )                        
        data_num = pd.DataFrame( rs.transform( x_num ) )

        ###--- MinMax Scaler ---###
        if mms == '':
            mms = MinMaxScaler().fit( x_num )
            pkl.dump( mms, open( '../data/pickle/rescaling/minmax_scaler.sav', 'wb' ) )
        data_num = pd.DataFrame( mms.transform( x_num ) )          

        ###--- One Hot Encoder ---###
        x_cat['TRANSFER'] = x_cat['type'].apply( lambda x : 1 if x == 'TRANSFER' else 0 ).copy()   
        x_cat['CASH_OUT'] = x_cat['type'].apply( lambda x : 1 if x == 'CASH_OUT' else 0 ).copy()   

        ## Renomeando colunas do DataFrame numérico
        data_num.columns = x_num.columns

        ## Concatenando DF numérico e categórico
        x_cat.reset_index( inplace = True )
        x_num.reset_index( inplace = True )
        data = x_cat.merge( x_num, how = 'inner', on = 'index' )    
        data.index = data['index']
        data.drop( columns = ['index', 'type'], inplace = True )

        return data, rs, mms     


class ML_process:
    def fine_tuning():
        ### Escolha dos parâmetros a serem testados
        param = {
            'booster'          : ['gbtree', 'gblinear', 'gbtree', 'dart'],
            'max_depth'        : [1, 6, 10, 20, 26, 30, 50],
            'learning_rate'    : [0.001, 0.1, 0.2, 0.3, 0.8, 1],
            'min_child_weight' : [0, 1, 3, 5, 10, 20, 50 ],
            'subsample'        : [0.1, 0.3, 0.5, 0.8, 1],
            'colsample_bytree' : [0.1, 0.3, 0.5, 0.8, 1]

        }

        ### Modelo
        xgb = XGBClassifier()

        ### GridSearch
        gs_xgb = GridSearchCV(
            estimator  = xgb,
            param_grid = param,
            cv         = StratifiedKFold( n_splits=5, shuffle = True ), 
            refit      = True,
            n_jobs     = -1,

        )              

    def feature_importance( x, y ):
        ### Criando e treinando modelo para extrair um coeficiente de importância da features
        etc = ExtraTreesClassifier()
        etc.fit( x, y )     

        ### Criando dataframe contendo nome e a importância das features para o modelo
        df_aux = pd.DataFrame()
        #povoando df com nome e importância da feature
        for i, j in zip( x, etc.feature_importances_ ):
            aux = pd.DataFrame( {'Feature' : i, 'Importance' : j}, index=[0] )
            df_aux = pd.concat( [df_aux, aux], axis=0 )

        df_aux.sort_values( 'Importance', ascending=False, inplace=True )

        return df_aux

 