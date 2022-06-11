require(MASS)
data("Boston")

View(Boston)

# El dataset Boston del paquete MASS recoge la mediana del valor de la vivienda en 506 áreas 
# residenciales de Boston. Junto con el precio, se han registrado 13 variables adicionales.
# 
# crim: ratio de criminalidad per cápita de cada ciudad.
# zn: Proporción de zonas residenciales con edificaciones de más de 25.000 pies cuadrados.
# indus: proporción de zona industrializada.
# chas: Si hay río en la ciudad (= 1 si hay río; 0 no hay).
# nox: Concentración de óxidos de nitrógeno (partes per 10 millón).
# rm: promedio de habitaciones por vivienda.
# age: Proporción de viviendas ocupadas por el propietario construidas antes de 1940.
# dis: Media ponderada de la distancias a cinco centros de empleo de Boston.
# rad: Índice de accesibilidad a las autopistas radiales.
# tax: Tasa de impuesto a la propiedad en unidades de $10,000.
# ptratio: ratio de alumnos/profesor por ciudad.
# black: 1000(Bk - 0.63)^2 donde Bk es la proporción de gente de color por ciudad.
# lstat: porcentaje de población en condición de pobreza.
# medv: Valor mediano de las casas ocupadas por el dueño en unidades de $1000s.

### Modelo lineal simple ###

modelo_simple <- lm(data = Boston,formula = medv ~ lstat)
summary(modelo_simple)

# El p-valor de la variable nos indica que el pocentaje de población en condiciones de pobreza es muy significativa para explicar
# el valor de las viviendas.

# Residual standar error (RSE): En promedio, cualquier predicción del modelo se aleja 6.216 unidades del verdadero valor.

# El predictor lstatus empleado en el modelo es capaz de explicar el 54.44% de la variabilidad observada en el precio de las viviendas.

# ¿Cómo se interpreta el intercept?
# ¿Cuál es beta 1? ¿Cómo se interpreta?

# Intervalo de confianza: Devuelve un intervalo para el valor promedio de todas las viviendas que se 
# encuentren en una población con un determinado porcentaje de pobreza, supóngase lstat=10.

predict(object = modelo_simple, newdata = data.frame(lstat = c(10, 20)),
        interval = "confidence", level = 0.95)

# Intervalo de predicción: Devuelve un intervalo para el valor esperado de una vivienda 
# en particular que se encuentre en una población con un determinado porcentaje de pobreza.

predict(object = modelo_simple, newdata = data.frame(lstat = c(10, 20)),
        interval = "prediction", level = 0.95)

# Representación gráfica (2 dimensiones)

attach(Boston)
plot(x = lstat, y = medv, main = "medv vs lstat", pch = 20, col = "grey30")
abline(modelo_simple, lwd = 3, col = "red")






### Modelo lineal múltiple ###

modelo_multiple <- lm(formula = medv ~ ., data = Boston)
summary(modelo_multiple)

# ¿En qué se diferencia Multiple R-squared y Adjusted R-squared? 

# The fundamental point is that when you add predictors to your model, the multiple Rsquared will always increase, 
# as a predictor will always explain some portion of the variance. Adjusted Rsquared controls against this increase,
# and adds penalties for the number of predictors in the model.

# ¿Cómo eliminar las variables que no son significativas?

step(modelo_multiple, direction = "both", trace = 1)

# Por tanto quitamos age y indus y obtenemos el modelo final

modelo_multiple <- lm(formula = medv ~ crim + zn + chas +  nox + rm +  dis + rad + tax + ptratio + black + lstat, 
                      data = Boston)

summary(modelo_multiple)



# Validación del modelo

par(mfrow = c(1,2))
plot(modelo_multiple)

# Los residuos confirman que los datos no se distribuyen de forma lineal, ni su varianza constante (plot1). 
# Además se observa que la distribución de los residuos no es normal (plot2).

# Análisis de correlaciones:

require(car)
vif(modelo_multiple)

# Los indices VIF son bajos o moderados, valores entre 5 y 10 indican posibles problemas 
# y valores mayores o iguales a 10 se consideran muy problemáticos.