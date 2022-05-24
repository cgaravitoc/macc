# Seleccionamos directorio

setwd("C:/Users/maria/Desktop")

options(scipen = 999)


# Librerías

library(dplyr)
library(ggpubr)


# Leemos dataset

superservicios <- read.csv('Superservicios.csv')

names(superservicios) <- c("id_empresa", "nombre", "periodo", "año",
                           "cod_localidad", "tipo_tecnologia", "km_red_interconexion", "capacidad_kw",
                           "fecha", "horas_servicio", "energia_entregada")

# Convertimos categóricos a numéricos

superservicios$capacidad_kw = as.numeric(gsub(",", "", superservicios$capacidad_kw))
superservicios$energia_entregada = as.numeric(gsub(",", "", superservicios$energia_entregada))




# 1. Estudie si en las ZNI (zonas no interconectadas) la energía suministrada, la capacidad de suministro 
# y los km de interconexión han cambiado en el tiempo.

# Energía suministrada

energia_suministrada <- superservicios %>% group_by(año) %>% summarise(mean = mean(energia_entregada, na.rm = TRUE), 
                                                                       sd = sd(energia_entregada, na.rm = TRUE))


ggboxplot(superservicios, x = "año", y = "energia_entregada", 
          color = "año",
          ylab = "Energía Entregada", xlab = "Año")


# Quitamos outliers

superservicios <- superservicios %>% mutate(energia_entregada = ifelse(energia_entregada > 100, NA, energia_entregada))

energia_suministrada <- superservicios %>% group_by(año) %>% summarise(mean = mean(energia_entregada, na.rm = TRUE), 
                                                                       sd = sd(energia_entregada, na.rm = TRUE))


ggboxplot(superservicios, x = "año", y = "energia_entregada", 
          color = "año",
          ylab = "Energía Entregada", xlab = "Año")


# Supongamos que no tiene outliers

res.aov <- aov(energia_entregada ~ año, data = superservicios)
summary(res.aov)




# ¿Es la capacidad instalada de generación de energía igual en todas los departamentos?

res.aov <- aov(capacidad_kw ~ cod_localidad, data = superservicios)
summary(res.aov)

var.test((superservicios %>% filter(cod_localidad==9500100000002))$capacidad_kw,
         (superservicios %>% filter(cod_localidad==4427902100022))$capacidad_kw)

capacidad_kw <- superservicios %>% group_by(cod_localidad) %>% summarise(mean = mean(capacidad_kw, na.rm = TRUE), 
                                                                                 sd = sd(capacidad_kw, na.rm = TRUE))


ggboxplot(superservicios, x = "año", y = "energia_entregada", 
          color = "año",
          ylab = "Energía Entregada", xlab = "Año")


# Quitamos outliers

superservicios <- superservicios %>% mutate(energia_entregada = ifelse(energia_entregada > 100, NA, energia_entregada))

energia_suministrada <- superservicios %>% group_by(año) %>% summarise(mean = mean(energia_entregada, na.rm = TRUE), 
                                                                       sd = sd(energia_entregada, na.rm = TRUE))


ggboxplot(superservicios, x = "año", y = "energia_entregada", 
          color = "año",
          ylab = "Energía Entregada", xlab = "Año")


# Supongamos que no tiene outliers

res.aov <- aov(energia_entregada ~ año, data = superservicios)
summary(res.aov)
