# Neurito – My Artificial Brain

## Experimentos

### 1. Dos necesidades fijas y una variable

Se dejaron dos necesidades fijas y la tercera se movió de 0 a 1. La acción predicha cambia cuando la necesidad que se mueve supera a la más alta de las otras dos. Con energía 0,8 y aburrimiento 0,3, el hambre cambia la acción de JUGAR a COMER en 0,30. Con hambre 0,3 y aburrimiento 0,4, la energía cambia de DORMIR a JUGAR en 0,60, porque el cansancio (`1 - energía`) tiene que ser mayor que 0,4. Y con hambre 0,3 y energía 0,8, el aburrimiento cambia de COMER a JUGAR en 0,30.

Antes de ese punto la acción no cambia, lo que cambia es qué tan segura está la red. Por ejemplo, con hambre 0,25 JUGAR tiene 63,7%, con 0,30 casi se empatan (COMER 48,4% y JUGAR 44,5%) y con 0,35 COMER sube a 71,1%. En los tres casos la red coincide con la regla.

### 2. Prioridades casi iguales

Cuando las tres prioridades son iguales (0,5) Softmax reparte la probabilidad casi en tercios: 35,2%, 33,4% y 31,3%. Con una ventaja de solo 0,02 en el hambre, COMER sube a 44,3%. Cuando empatan dos prioridades altas y la tercera es baja (0,8, 0,8 y 0,2), la probabilidad se divide casi 50/50 (49,1% y 50,9%) y la tercera queda en 0%.

En ese último caso la red dio DORMIR y la regla COMER, pero no es un error real, porque la regla desempata con `argmax` y siempre toma la primera opción. De hecho, los 6 errores que tuvo la red en las 1.000 muestras de prueba tenían una diferencia de 0,014 o menos entre sus dos prioridades más altas. Esto da entender que Softmax muestra qué tan segura está la red y que se pone dudosa justo cerca de los empates.

### 3. Capa oculta de 3, 6, 10 y 20 neuronas

| Neuronas | Pérdida (semilla 42) | Precisión (semilla 42) | Precisión promedio de 5 semillas |
|---|---|---|---|
| 3 | 0,1618 | 96,30% | 95,98% |
| 6 | 0,1225 | 99,40% | 97,82% |
| 10 | 0,1262 | 99,30% | 98,98% |
| 20 | 0,1220 | 98,80% | 99,10% |

Con 3 neuronas la red queda por debajo en todas las semillas, probablemente porque no tiene capacidad suficiente. De 6 a 10 mejora el promedio, y de 10 a 20 casi no hay diferencia. Con la semilla 42, 6 neuronas parecen mejores que 20, pero eso es suerte de esa semilla, ya que en el promedio 6 neuronas es lo más inestable (entre 96,8% y 99,4%). Además, el conjunto de prueba tiene solo 1.000 muestras, así que un error cambia la precisión en 0,1 puntos.

### 4. Épocas y tasa de aprendizaje

**Épocas** (tasa 0,1): con 50 épocas la precisión es de 60,6%, con 200 de 91,8%, con 600 de 98,6%, con 1.200 de 99,4% y con 6.000 de 99,6%. El entrenamiento mejora rápido al inicio y después se estanca: entre 1.200 y 6.000 épocas la pérdida baja de 0,1225 a 0,0484, pero la precisión solo sube 0,2 puntos, porque los errores que quedan son empates.

**Tasa de aprendizaje** (1.200 épocas): con 0,001 y 0,01 es demasiado lenta (41,8% y 82,9%). Entre 0,05 y 0,5 es estable (de 98,6% a 99,6%). Con 1 y 2 empieza a ser inestable (98,7% y 97,3%, y con 2 la pérdida llega a subir hasta 1,479). Con 5 o más el entrenamiento falla: la precisión queda en 33,8%, que es lo mismo que adivinar, y casi todas las neuronas ReLU quedan apagadas.

### 5. Cuarta acción

Una cuarta acción necesita, primero, un dato nuevo de entrada. Por ejemplo, BAÑARSE con una necesidad de suciedad entre 0 y 1. Si no hay una entrada nueva, la red no tiene forma de distinguir la acción nueva de las otras. Después necesita una etiqueta nueva: la regla pasaría a ser `argmax([hambre, 1 - energía, aburrimiento, suciedad])`, con ejemplos suficientes de las cuatro clases (con datos uniformes quedó cerca de 25% cada una).

La red también cambia de forma: `W1` pasa de 3×6 a 4×6, `W2` de 6×3 a 6×4 y `b2` de 1×3 a 1×4. Se probó así y dio 97,80% de precisión con 6 neuronas y 98,10% con 10, un poco menos que con tres acciones, probablemente porque hay más empates posibles. Además, habría que agregar la tecla, la barra y los sprites en la interfaz.

## Explica tus resultados

### 1. ¿En qué se diferencian pesos y sesgos?

Los pesos (`W1` y `W2`) multiplican cada entrada y definen cuánto influye cada necesidad en cada neurona. Los sesgos (`b1` y `b2`) se suman al resultado y no dependen de la entrada, así que mueven el punto desde donde parte cada neurona o cada salida. Por ejemplo, si las tres necesidades valen 0, `W1` no aporta nada y la red depende de los sesgos y de `W2`: en ese caso predice DORMIR con 99,996%. Además, en el código los sesgos empiezan en cero y los pesos en valores aleatorios, porque si todos los pesos fueran iguales todas las neuronas aprenderían lo mismo.

### 2. ¿Por qué el cansancio es `1 - energía`?

Porque para comparar cuál necesidad es más urgente las tres tienen que ir en el mismo sentido. El hambre y el aburrimiento ya lo hacen: mientras más altos, más urgente. La energía va al revés, ya que energía alta significa que la mascota está descansada. Sin la inversión, `argmax` elegiría DORMIR justo cuando la energía es más alta. Con `1 - energía`, energía 0,9 es cansancio 0,1 y energía 0,1 es cansancio 0,9. Esta inversión solo está en la regla que crea las etiquetas, la red recibe la energía tal cual y tiene que aprenderla sola.

### 3. ¿Qué hace ReLU y qué hace Softmax?

ReLU es `max(0, x)`: deja pasar los valores positivos y vuelve cero los negativos. Se usa en la capa oculta para que la red no sea solo una operación lineal. Se comprobó que un modelo sin capa oculta llega a 95,70% de precisión, contra 99,40% de la red con ReLU. Softmax se usa en la salida y convierte los tres puntajes en probabilidades que van de 0 a 1 y suman 100%. Así la red no solo da una acción, sino también qué tan segura está de cada una.

### 4. ¿Por qué una precisión alta puede ser engañosa?

Porque el 99,40% solo mide qué tan bien la red copia una regla inventada, no si esa regla sirve para cuidar una mascota. También cuenta solo la acción ganadora y no la seguridad: la confianza promedio fue de 89,8% en los aciertos y de 51,1% en los errores. Además, el número global esconde dónde falla: con diferencias menores a 0,02 entre prioridades la precisión es de 90%, y en el resto de 100%. Si una clase fuera el 95% de los datos, una red que siempre responda esa clase tendría 95% sin haber aprendido nada. Y como la prueba tiene solo 1.000 muestras, diferencias como 99,4% contra 99,3% no significan mucho.
