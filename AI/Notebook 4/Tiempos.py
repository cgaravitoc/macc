from time import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols

def obtiene_tiempos(fun, args, num_it=100):
    tiempos_fun = []
    for i in range(num_it):
        arranca = time()
        x = fun(*args)
        para = time()
        tiempos_fun.append(para - arranca)
    return tiempos_fun

def compara_funciones(funs, arg, nombres, N=30):
    nms = []
    ts = []
    for i, fun in enumerate(funs):
        nms += [nombres[i] for x in range(N)]
        ts += obtiene_tiempos(fun, [arg], N)
    data = pd.DataFrame({'Función':nms, 'Tiempo':ts})
    # Graficando
    fig, ax = plt.subplots(1,1, figsize=(3*len(funs),3), tight_layout=True)
    sns.boxplot(data=data, x='Función', y='Tiempo')
    sns.swarmplot(data=data, x='Función', y='Tiempo', color='black', alpha = 0.5, ax=ax);
    # Anova diferencia de medias
    model = ols('Tiempo ~ C(Función)', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)
