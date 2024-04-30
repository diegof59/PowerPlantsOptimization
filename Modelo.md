# Modelo Optimización: Plantas de energía

- Diego Botero Celi	diego.botero@correounivalle.edu.co
- Mauricio Antonio Carrillo Perdomo	mauricio.carrillo@correounivalle.edu.co
- Kevin Stuard Marin C kevin.concha@correounivalle.edu.co

## Problema a solucionar

Un proveedor de energı́a tiene un parque de centrales eléctricas. Para simplificar, consideramos que el parque incluye solo una central nuclear ($N$), una central hidroeléctrica
($H$) y una central térmica ($T$).

Los costos de producción de un MW (megawatt) en cada una de las plantas se indican mediante $c_N$ , $c_H$ y $c_T$ . Las capacidades de producción diarias son por lo general $1000MW$ para la central nuclear, $300MW$ para la central hidroeléctrica y $500MW$ para la central térmica, pero pueden llegar a variar en un futuro.

La empresa quiere planificar la producción de energı́a en un horizonte de $n$ dı́as para satisfacer la demanda diaria $d_{s,i}$
estimada (en $MW$) para cada uno de sus clientes $s$ en el dı́a $i$:

| Cliente | Día 1 | Día 2 | ... | Día n |
|---------|-------|-------|-----|-------|
| S1      | 80    | 110   | ... | 90    |
| S2      | 150   | 98    | ... | 340   |
| ...     | ...   | ...   | ... | ...   |
| Sm      | 300   | 250   | ... | 134   |

Es fundamental que, en el caso de que el proveedor de energı́a no pueda satisfacer la totalidad de la demanda en un dı́a especı́fico, se asegure de proporcionar al menos el $50\%$ ($G=0.5$) de la demanda requerida por cada uno de sus clientes.

Este porcentaje puede variar según las polı́ticas establecidas por la central eléctrica o en situaciones en las que no sea posible alcanzar el mı́nimo requerido de demanda.

Además de los costos de producción, es fundamental considerar que cada cliente realiza un pago individual $P_s$ por cada $MW$. Es importante destacar que estos pagos pueden variar de un cliente a otro, ya que cada uno maneja un valor diferenciado basado en sus acuerdos particulares con la central eléctrica.

### Objetivo

El objetivo es cubrir la producción de energı́a en el horizonte de tiempo n, donde se busca maximizar la ganancia neta $r$, la cual se calcula restando el costo de producción de la suma de los pagos realizados por la producción de energı́a entregada a cada cliente.

### Evitar desgaste de hidroeléctrica

La capacidad máxima de la central hidroeléctrica es de $300MW$. Se dice que una producción superior al $80\%$ de esta capacidad (i.e., $240M W$) está en régimen alto.

Para limitar el desgaste de las turbinas, está prohibido: Producir 2 dı́as consecutivos en régimen alto.

El porcentaje de producción en régimen alto $a_H$ y el número de días consecutivos en régimen alto $d_H$ pueden variar en el futuro.

### Definiciones

$ N := $ Central nuclear

$ H := $ Central hidroeléctrica

$ T := $ Central térmica

## Parámetros

### Planta

#### Costo producción

$ c_N := $ Costo producción / MW (Megawatt). Central nuclear

$ c_H := $ Costo producción / MW. Central hidroeléctrica

$ c_T := $ Costo producción / MW. Central térmica

$ c_N, c_H, c_T \in \mathbb{Z} $

#### Capacidad

$ cm_N := $ Capacidad máxima de producción central nuclear

$ cm_H := $ Capacidad máxima de producción central nuclear

$ cm_T := $ Capacidad máxima de producción central nuclear

$ cm_N, cm_H, cm_T \in \mathbb{Z} $

#### Generalización número de plantas

Para generalizar el modelo a más plantas de energía, se definen:

$ p := $ `num_plantas` valor default: $3$. Cantidad de plantas de energía (Permite generalizar el modelo a más plantas)

$ p \in \mathbb{Z} $

$ c_p := $ `costo` valor default:$ [c_N, c_H, c_T] $ Costos de producción / MW (Megawatt) de las plantas de energía

$ cm_p := $ `capacidad_maxima` valor default:$ [cm_N, cm_H, cm_T] $ Capacidad máxima de producción de las plantas de energía

$ c_p, cm_p \in \mathbb{Z}^p $

### Clientes y Operación

$ s := $ `num_clientes` Cantidad de clientes total

$ n := $ `num_dias` Tiempo total a abastecer, en días. Horizonte de planificación

$ n, s \in \mathbb{Z} $

$ D_{s,n} := $ `demanda` Demanda[cliente, día]

$ D \in M^2(\mathbb{Z}) $

$ G := $ `min_porcent_demanda` Mínimo porcentaje de la demanda a satisfacer para todo cliente, de no poder satisfacerse su demanda requerida en ese día

$ G \in \mathbb{Z} $

$ P_s := $ `pago` Pago del cliente $s$ por MW

$ P \in \mathbb{Z}^s $

### Régimen alto de operación hidroeléctrica

Para implementar la funcionalidad de restringir operación en régimen alto en la central hidroeléctrica, se define:

$ a_H := $ `reg_alto_porcent` valor default: $80$. Porcentaje de producción a partir del cual se considera que la central hidroeléctrica opera en régimen alto

$ d_H := $ `reg_alto_dias` valor default: $2$. Número de días consecutivos a partir de los cuales no está permitido producir en régimen alto

$ a_H, d_H \in \mathbb{Z} $

## Variables

Matríz tridimensional de producción de energía: Cada elemento de la matriz es una variable de decisión que representa la cantidad de energía (en $MW$) producida para un cliente específico $s$ en un día específico $n$ por una planta específica $p$.

$ W_{s,n,p} := $ `produccion` Matríz tridimensional de tamaño $s \cdot n \cdot p$ : `num_clientes * num_dias * num_plantas`

$ W \in M^3(\mathbb{Z}) $

Para implementar la restricción de no producir en régimen alto $d_H$ días consecutivos, se define la variable $H$ que indica si la central hidroeléctrica está en régimen alto en cualquier día dado.

$ H := $ `en_regimen_alto` Arreglo de tamaño $n$ que indica si la central hidroeléctrica está en régimen alto en cualquier día dado. Se inicializa con $false$ en todos los días.

$ H \in \{true, false\}^n $

### Variable a optimizar

$ r := $ `ganancia_neta` Ganancia neta total

$ r \in \mathbb{Z} $

## Restricciones

- Restricción de capacidad de la planta: Para cada día y cada planta, la producción total de la planta (la suma de la producción para todos los clientes) no debe exceder su capacidad diaria.

$$ \forall n , \forall p : \sum_s W[s,n,p]\leq cm_p $$

- Restricción de demanda del cliente: Para cada día y cada cliente, la producción total para el cliente (la suma de la producción de todas las plantas) no debe exceder la demanda del cliente para ese día

$$ \forall n , \forall s : \sum_p W[s,n,p] \leq D[s,n] $$

- Restricción de demanda mínima: Para cada día y cada cliente, la producción total para el cliente debe ser al menos un cierto porcentaje $G$(min_porcent_demanda) de la demanda del cliente.

$$ \forall n, \forall s : \sum_p W[s,n,p] \geq D_{s,n} \cdot \frac{G}{100} $$

- Restricción de suplir la totalidad de la demanda: Si la demanda total para un día no excede la capacidad máxima total de todas las plantas, entonces la producción total debe ser igual a la demanda total

$$ \forall n : \left( \sum_s D[s,n] \leq \sum_p cm_p \right) \rightarrow \left( \sum_p \sum_s W[s,n,p] = \sum_s D[s,n] \right) $$

- Restricción de no negatividad de la producción: Para cada día, la producción de las plantas para cada cliente debe ser no negativa.

$$ \forall n , \forall s, \forall p : W[s,n,p]  \geq 0 $$

- Restricción de capacidad de producción de la planta hidroeléctrica: La producción de la central hidroeléctrica no debe exceder el $a_H\%$ de su capacidad máxima $cm_H$ durante $d_H$ días consecutivos.

  Hemos de popular el arreglo $H$ con $true$ si la producción de la central hidroeléctrica supera el $a_H\%$ de su capacidad máxima $cm_H$ para cada día, o $false$ en caso contrario.

  $$ \forall n : \left( \sum_s W[s,n,2] > cm_h \cdot \frac{a_H}{100} \right) \rightarrow \left( H[n] = true \right) $$
  
  Si la central hidroeléctrica está en régimen alto en el día $d$, entonces no puede estar en régimen alto en todos los $d_H$ días consecutivos siguientes, por lo que debe existir al menos un día en que no opera en regimen alto.

  $$ \forall d : \left( H[d] = true \right) \rightarrow \left( \exists i \left( d \leq i \leq d+d_H \right) : H[i] = false \right) $$

## Función Objetivo

El objetivo es maximizar la ganancia neta, que se calcula como la suma de los ingresos por ventas de energía menos el costo de producción para cada cliente y día.

$$ r = \sum_n \sum_s \left( \sum_p produccion[s,n,p] \cdot pago[s] - \sum_p produccion[s,n,p] \cdot costo[p] \right) $$