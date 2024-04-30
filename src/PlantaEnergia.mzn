% Este código de MiniZinc representa el modelado de un problema de optimización
% de un conjunto de plantas de energía.
% Su objetivo es determinar la producción óptima de energía de cada central eléctrica
% para maximizar la ganancia neta, considerando varios parámetros y restricciones.

% Nota: Este código asume que los parámetros de entrada ya están definidos (ingresados manualmente o mediante archivo de datos) y se utiliza la declaración de resolución para encontrar la solución óptima.

% Parámetros
int: num_clientes; % Número de clientes a abastecer
int: num_dias; % Número de días en el horizonte de planificación
int: num_plantas = 3; % Número de plantas: Se puede generalizar a más de las 3 plantas del enunciado
int: min_porcent_demanda; % Porcentaje mínimo de demanda a satisfacer
int: reg_alto_porcent = 80; % Porcentaje de producción a partir del cual se considera que la central hidroeléctrica opera en régimen alto
int: reg_alto_dias = 2; % Número de días consecutivos a partir de los cuales no está permitido producir en régimen alto

array[1..num_plantas] of int: costo;  % Costo por MW producido en cada planta
array[1..num_plantas] of int: capacidad;  % Capacidad diaria en cada planta, en MW
array[1..num_clientes] of int: pago; % Pago por MW de cada cliente
array[1..num_clientes, 1..num_dias] of int: demanda; % Demanda de cada cliente por día

%% Cálculados
int: max_capacidad =  sum(p in 1..num_plantas) (capacidad[p]); % Capacidad máxima total (suma) de todas las plantas

% Variables de decisión
array[1..num_clientes, 1..num_dias, 1..num_plantas] of var 0..max_capacidad : produccion; % Producción de energía por cada planta de energía para cada cliente y cada día

array[1..num_dias] of var bool: en_regimen_alto; % Arreglo booleano que indica si la central hidroeléctrica opera en régimen alto para cada día en el horizonte de planificación

% Restricciones

% Restricción de capacidad de la planta: Para cada día y cada planta, la producción total de la planta
% (la suma de la producción para todos los clientes) no debe exceder su capacidad diaria.
constraint forall(n in 1..num_dias, p in 1..num_plantas) (
  sum(s in 1..num_clientes) (produccion[s,n,p]) <= capacidad[p]
);

% Restricción de demanda del cliente: Para cada día y cada cliente, la producción total
% para el cliente (la suma de la producción de todas las plantas) no debe exceder la demanda del cliente para ese día
constraint forall(n in 1..num_dias, s in 1..num_clientes) (
  sum(p in 1..num_plantas) (produccion[s,n,p]) <= demanda[s, n]
);

% Restricción de demanda mínima: Para cada día y cada cliente, la producción total para el cliente
% debe ser al menos un cierto porcentaje (min_porcent_demanda) de la demanda del cliente.
constraint forall(n in 1..num_dias, s in 1..num_clientes) (
  sum(p in 1..num_plantas) (produccion[s,n,p]) >= demanda[s,n]*(min_porcent_demanda/100)
);

% Restricción de suplir la totalidad de la demanda: Si la demanda total para un día no excede
% la capacidad máxima total de todas las plantas, entonces la producción total debe ser igual a la demanda total
constraint forall(n in 1..num_dias) (
  sum(s in 1..num_clientes) (demanda[s,n]) <= max_capacidad ->
  sum(p in 1..num_plantas, s in 1..num_clientes) (produccion[s,n,p]) == sum(s in 1..num_clientes)(demanda[s,n])
);

% Restricción de no negatividad de la producción: Para cada día, la producción de las plantas
% para cada cliente debe ser no negativa.
% Por definición de la variable de decisión, la producción no puede ser negativa
% constraint forall(s in 1..num_clientes, n in 1..num_dias, p in 1..num_plantas) (produccion[s,n,p]) >= 0;

% Restricción adicional para la planta hidroeléctrica. Si la producción de la central hidroeléctrica
% supera el porcentaje definido como regimen alto de su capacidad productiva en un día, entonces
% no puede producir en regimen alto durante más días consecutivos definidos como permitidos.

%% Restricción que popula el arreglo en_regimen_alto
constraint forall(d in 1..num_dias) (
  if sum(s in 1..num_clientes) (produccion[s,d,2]) > (capacidad[2] * (reg_alto_porcent / 100)) then
    en_regimen_alto[d] = true
  else
    en_regimen_alto[d] = false
  endif
);


% Verifica si el subarray desde d hasta d+H contiene un false, para todo d=true en el arreglo en_regimen_alto
% desde 1 hasta num_dias-reg_alto_dias
constraint forall(d in 1..(num_dias-reg_alto_dias)) (
  exists(i in d..d+reg_alto_dias) (not en_regimen_alto[i])
  );

% Función Objetivo
% Se busca maximizar la ganancia neta, que se calcula como la suma de
% los ingresos por ventas de energía menos el costo de producción
var int: ganancia_neta = sum(d in 1..num_dias, c in 1..num_clientes) (
  sum(p in 1..num_plantas) (produccion[c,d,p] * pago[c]) - sum(p in 1..num_plantas) (produccion[c,d,p]*costo[p])
);

solve maximize ganancia_neta;

% Salida de la solución
output [show(ganancia_neta), "&", show(produccion)]