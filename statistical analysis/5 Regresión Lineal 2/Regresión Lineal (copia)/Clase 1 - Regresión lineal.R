m = data.frame(altura = c(1.65, 1.84, 1.72, 1.92, 1.55, 1.78, 1.90, 1.80, 1.92, 1.70),
               peso = c(60, 80, 65, 90, 48, 70, 75, 78, 82, 63))


plot(m$altura, m$peso)


model = lm(peso~altura, m)
summary(model)


m = data.frame(nota = c(8, 3, 1, 4, 8.2, 9.5, 8, 7.5, 8.5, 5),
               horas_estudio = c(11, 2, 1, 4, 12, 15, 9, 8, 8, 6))


plot(m$nota, m$horas_estudio)


model = lm(nota~horas_estudio, m)
summary(model)
