#### ! O Contexto a seguir é completamente fictício !

![](https://www.bosch.com.br/media/stories/aiot/cyber_security/cyber_security_bosch_banner.png)
# <center> Projeto de Detecção de fraudes financeiras -- Fraud Protect Company -- </center>

## Contextualização
<p>A FPC é uma empresa especializada na detecção de fraudes em transações financeiras. <br>
Dentre outros, a empresa possui um serviço que garante o bloqueio de transações fraudulentas baseado em um modelo de negócio do tipo serviço com monetização fixa por performance do modelo de detecção. Recebendo uma taxa fixa sobre o sucesso na detecção de fraude nas transações de clientes. Por ser uma empresa em fase de expansão, adotou uma estratégia agressiva que funciona da seguinte forma: </p>

1. A empresa recebe 25% do valor de cada transação fraudulenta detectada. 
2. A empresa deve arcar com uma multa de 5% do valor de cada transação detectada como fraude, porém a transação é legítima. 
3. A empresa deve devolver 100% do valor para o cliente em cada transação detectada como legítima, porém a transação é na verdade uma fraude. 

<p><br> Para a empresa, além de conseguir muitos clientes com essa estratégia arriscada em garantir 100 % de reembolso  em casos de falha na detecção de fraudes, ela depende somente da precisão e da acurácia dos modelos construídos para alcançar bons resultados. </p>

### Desafio:
- Criar um modelo de alta precisão e acurácia na detecção de fraudes de transações feitas através de dispositivos móveis.
- Ao final da consultoria, será entregue ao CEO da empresa, o senhor Obi-Wan Pereira, um relatório reportando a performance e os resultados do modelo com relação a custos, retorno e lucro que a empresa terá caso utilize o modelo prodduzido.

### Exigências
Frente a exigências previamente acordadas, o relatório deve conter as seguintes informações:
1. Qual a precisão na detecção de fraudes possui o modelo?
2. Qual a confiabilidade do modelo em classificar as transações legítimas?
3. Qual faturamento esperado pela empresa caso todas as classificações forem feitas pelo modelo?

### Relatorio:
<p>Frente a demanda relatada préviamente em reunião, retorno-lhe o seguinte documento contendo resultados de análise feitas na base de dados e resultados do modelo com relação a custos, retorno e lucro previstos caso o modelo seja colocado em produção.</p>

---

### Resumo da análise dos dados
- Total de dados transacionais analisados = 6.362.620
- A análise completa pode ser acessado por este [link](https://github.com/rsantosluan/fraud_detect/blob/master/Jnotebooks/eda.ipynb)
<p>No decorrer da Análise Exploratória dos Dados, foram levantadas hipóteses com intuito de conhecer melhor os dados e gerar percepções (insights) valiosas para o negócio. Dentre elas, podemos elencar como destaques:

1. <b>A maior incidência de fraudes, tende a ocorrer em transações do tipo 'CASH_OUT' por dificultar o rastreio das transações. </b>
    Além de validar a hipótese podemos observar que, por padrão, as fraudes ocorrem apenas em dois tipos de transação: 'CASH_OUT' e 'TRANSFER'. O que reduz significativamente a quantidade de dados a serem analisados. Tomando como referência a base de dados atual, a redução no montante de dados a serem analisados fica em torno de 43%, poupando assim poder de processamento e seus eventuais custos a empresa. </br>
![Transações fraudulentas por tipo](/img/h1.png)
2. <b>Contas de origem, tendem a ser zeradas em fraudes. </b>
    Apesar de a análise da hipótese em si não trazer grande relevância para o modelo, ao validá-la foi percebido uma incoerência nos dados transacionais, onde os valores do <b>|</b>balanço pré-transferência<b>|</b> subtraído do <b>|</b>valor transacional<b>|</b> - <b>|</b>balanço pós-transferência<b>|</b> difere de 0 demonstrando inconsistência nas transações. O que foi fortemente relevante para refinar o desempenho do modelo. <i>!Mais detalhes na seção de criação de features(recursos)!.</i>
![Distribuição dos dados em caso de fraude](/img/h2.png)
 </p>

 <p>Ao final desta etapa, foram excluídos os dados elencados na hipótese 1 bem como algumas variáveis(colunas) categóricas que serão melhor avaliadas em segundo ciclo de desenvolvimento.</p>

---

### Resumo da preparação dos dados e embasamento da escolha do modelo
A preparação e modelagem completas pode ser acessado por este [link](https://github.com/rsantosluan/fraud_detect/blob/master/Jnotebooks/EDA_basica-C2.ipynb)

- Primeiramente os dados forma divididos em: treino, teste e validação. Em suma, essa separação é feita para garantir a generalização do modelo em dados nunca 'vistos' por ele. Reproduzindo assim um ambiente muito parecido com quando o modelo for colocado em produção.
- Em seguida os dados foram normalizados. O que garante que todos os dados numéricos sejam remodelados para uma escala padrão, evitando assim o viés do modelo para dados de maiores escalas.
- Como os modelos de Machine Learning não trabalham bem com variáveis categóricas, usando ferramentas adequadas, os dados foram devidamente convertidos para padrões numéricos.


#### -Testes de modelos
<p>Foram testados nesta etapa 4 modelos. Sendo dois baseados em em árvore de decisão e os demais baseados em análise de regressão linear.
Como resultado da performance dos modelos, foi gerada as seguintes matrizes(Confusion Matrix):

<br>
<sub> <i> As matrizes de confusão, trazem os dados dispostos da seguinte maneira: </br></sub>
<sub> <b>- Quadrante superior esquerdo</b>: Quantos registros previstos pelo modelo como <b>não fraudulentos</b>, realmente não são. </br> </sub>
<sub> <b>- Quadrante inferior esquerdo</b>: Quantos registros previstos pelo modelo como <b>não fraudulentos</b>, na verdade são fraudes.  </br></sub>
<sub> <b>- Quadrante superior direito</b> : Quantos registros previstos pelo modelo como <b>fraudulentos</b>, na verdade não são fraudes. </br> </sub>
<sub> <b>- Quadrante inferior direito</b> : Quantos registros previstos pelo modelo como não <b>fraudulentos</b>, realmente são. </br> </p> </sub>
</i> 

![Teste dos modelos](/img/m_perf.png)
<b> <center> Pela melhor performance frente a análise da matriz de confusão, o modelo utilizado será o XGBoost.</b></center>
<br>



#### -Fine Tuning(Ajuste dos parâmetros modelo) e Feature Selection(seleção de variáveis) 
<p>
- <b>Fine Tuning:</b> Foram feitos diversos ajustes diferentes na tentativa de melhorar a performance do modelo nesta etapa mas, os parâmetros padrões, obtiveram resultados com uma melhor performance. 
- <b>Feature Selection:</b> O modelo se mostrou melhor com a utilização de todas as features, com exceção de 'isFlaggedFraud'.
</p> 

#### -Feature Engineering(Criação de novas variáveis)
<p>
Levando em cosideração as análises da segunda hipótese, foram criadas 2 novas features 'dif_balance_origin' e 'dif_balance_dest' que notoriamente, tiveram um papel fundamental na melhora da acecrtividade do modelo:

![Teste dos modelos](/img/fs_perf.png)

#### -Performance do modelo com dados de validação
<p> 
O modelo teve um desempenho excelente na detecção das fraudes tendo baixímos índices de erro alcançando uma média de 99% de acertividade nas previsões de fraudes detectadas:

![Teste dos modelos](/img/mfinal_perf.png)

--- 

### -Métricas de negócio
<p> Cálculo baseado no conjunto de dados de validação. </p>


Valores Monetários
| Métrica                                         | Valor
| :------------------                             | :----------: 
| Retoorno (Positivos reais)                      | 164.455.817,68        
| Custos (falsos positivos e negativos)           | 1.214.523,61        
| Lucro esperado (retorno - custo)                | 163.241.294,07     
| Valor total movimentado                         | 70.688.438.278,38       



| Métrica                                                                                                              | Valor real   | %                  |
| :------------------                                                                                                  | :----------: | -----------------: | 
| Erro quanto a previsões indicando <b> fraudes</b> quando a transação <b>não era fraudulenta</b>(falsos positivos)    |      4       |      0.00181%      |                     
| Erro quanto a previsões indicando <b>não fraudes</b> quando a transação <b>era fraudulenta</b>(falsos negativos)      |      1       |      0.000453%    |                     

