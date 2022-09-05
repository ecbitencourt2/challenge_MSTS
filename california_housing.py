#Importando as bibliotecas que serão usadas nesse caso
import pandas as pd
import pyarrow as pa

#Lendo o arquivo e fazendo a análise exploratória com a função describe()
df_california = pd.read_csv('california_housing_train.csv', sep=',')
df_california.dropna(inplace = True)
desc = df_california.describe()

#Questão 1.1
#usando a transposta para definir e agrupar qual a coluna com o maior desvio padrão
desc=desc.T
print("Desvio padrão do maior para o menor:\n",desc['std'].sort_values(ascending=False))

#Questão 1.2
#Encontrando o valor máximo e mínimo da coluna median_house_value
print("o maior valor de median_house_value é:",df_california['median_house_value'].max(),"\n")
print("o menor valor de median_house_value é:",df_california['median_house_value'].min(),"\n")

#Questão 2.1
#Criando os filtros de faixa etáriadados na questão
filtro_ate_18= (df_california['housing_median_age'] <18)
filtro_ate_29= (df_california['housing_median_age']>=18) & (df_california['housing_median_age']<29)
filtro_ate_37= (df_california['housing_median_age']>=29) & (df_california['housing_median_age']<37)
filtro_acima_37= (df_california['housing_median_age'] >37)
#Atribuindo os valores as linhas de acordo com os filtros de faixa etária
df_california.loc[filtro_ate_18, 'hma_cat'] = 'de_0_ate_18'
df_california.loc[filtro_ate_29, 'hma_cat'] = 'ate_29'
df_california.loc[filtro_ate_37, 'hma_cat'] = 'ate_37'
df_california.loc[filtro_acima_37, 'hma_cat'] = 'acima_37'

#Questão 2.2
#Atribuindo os valores as linhas de acordo com os filtros de região
df_california.loc[df_california['longitude']<-119, 'c_ns']='norte'
df_california.loc[df_california['longitude']>=-119, 'c_ns']='sul'

#Questão 2.3
#Renomeando as colunas para o padrão informado na questão e criando o arquivo .parquet
df_california.rename(columns={'hma_cat': 'age', 'c_ns':'california_region'}, inplace = True)
df_california[['age','california_region','total_rooms','total_bedrooms','population','households','median_house_value']]\
    .to_parquet('california_housing_train.parquet')
df_final = pd.read_parquet('california_housing_train.parquet')

#Questão 3
#Separando as colunas pedidas
df_final = df_final[['age','california_region','population','median_house_value']]

#Usando o grupby para fazer a agregação dos dados utilizando a função sum() e mean()
df_final_sum =df_final.groupby(['age','california_region'],as_index=False).sum()
df_final_mean=df_final.groupby(['age','california_region'], as_index=False).mean()

#Imprimindo na tela as tabelas dos resultados das funções sum() e mean()
print('Tabela com a média dos valores das casas por região e idade: \n',df_final_mean,"\n")
print('Tabela com a soma da população por região e idade:\n',df_final_sum,"\n")

#Definindo a dataframe final com base nos dataframes df_final_sum e df_final_mean
df= df_final_sum
df['median_house_value']=df_final_mean['median_house_value']
df.sort_values(by='median_house_value')
df.rename(columns={'population': 's_population', 'median_house_value': 'm_median_hpuse_value'}, inplace=True)
#Criando um arquivo .parquet com o resultado final da análise
df.to_parquet('california_housing_train_analises.parquet')
print('\n',df)