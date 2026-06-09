----------------------------------------------------------ejercicio1-----------------------------------------------------------
Sistema de Turnos con tiempo de espera recursivo en C++ 
El objetivo es extender el sistema de gestión de turnos incorporando una función recursiva que recorra la cola de clientes e 
imprima el tiempo de espera de cada uno sin modificar la estructura original.

__________________________________________________________IMPORTANTE____________________________________________________________
El sistema mantiene una cola FIFO de clientes registrados con su hora de llegada. 
+La función imprimirEsperas() recorre esa cola de forma recursiva. 
La cola original nunca se modifica porque se pasa por valor (copia). 
El tiempo de espera se calcula en segundos con difftime() contra el momento actual.

Se usa: --- queue<Cliente> de la STL como estructura principal --- time_t y time()  del header <ctime> para capturar la hora 
de llegada

--- difftime() para calcular la diferencia en segundos 
--- Recursión directa: imprimirEsperas() se llama a sí misma

------------------------------------------------------Lo que hace cada parte-----------------------------------------------------
--- struct Cliente : almacena nombre, número de turno y hora de llegada (horaLlegada)
--- imprimirEsperas(queue<Cliente> cola) : función recursiva — caso base: cola vacía → return; 
--- paso recursivo: imprime cabeza y se llama con el resto
--- sistemaTurnos() : menú principal con 4 opciones — registrar, llamar próximo, ver lista, ver esperas
--- main() : punto de entrada, llama a sistemaTurnos()

____________________________________________________RELACIÓN DE RECURRENCIA______________________________________________________
--- imprimirEsperas(cola) = imprimir cabeza + imprimirEsperas(resto)
--- Caso base: cola vacía → no hace nada
--- Cada llamada genera un nuevo frame en el stack con su propia copia de cola
Ejemplo de bobinado con 3 clientes en cola [Ana, Luis, Marta]:
imprimirEsperas([Ana, Luis, Marta]) → imprime Ana → imprimirEsperas([Luis, Marta]) → imprime Luis → imprimirEsperas([Marta]) → 
imprime Marta → imprimirEsperas([]) ← caso base, retorna

________________________________________________________EJECUCIÓN________________________________________________________________

1 Abrir terminal y navegar hasta la carpeta del proyecto
2 Compilar: g++ -o ejercicio1 ejercicio1.cpp
3 Ejecutar: ./ejercicio1
4 Registrar clientes con la opción 1 (asigna turno y captura hora de llegada automáticamente)
5 Seleccionar opción 4 para ver tiempos de espera calculados recursivamente. 
El sistema imprime por cada cliente: Turno | Nombre | Espera: N seg



_________________________________________________________________________________________________________________________________
_________________________________________________________________________________________________________________________________
_________________________________________________________________________________________________________________________________


----------------------------------------------------------ejercicio2-----------------------------------------------------------

Funciones mutuamente recursivas par(n) e impar(n) en C++
El objetivo es determinar la paridad de un número natural usando únicamente las reglas del enunciado,
sin operadores aritméticos ni módulo. Las dos funciones se llaman entre sí — eso es recursión mutua (indirecta).

__________________________________________________________ IMPORTANTE ____________________________________________________________

Las únicas reglas permitidas son las dadas por el enunciado: 1 es impar; el antecesor de un impar es par;
el antecesor de un par es impar. No se usa % 2 ni ningún otro operador.
Cada función tiene su propio caso base en n == 1.
Se necesita una forward declaration porque par() llama a impar() que todavía no fue definida en ese punto del archivo.
Se usa: --- Recursión mutua (indirecta): par() llama a impar() y impar() llama a par()
--- Forward declaration: bool impar(int n); antes de definir par()
--- Caso base único en n == 1 para cada función

------------------------------------------------------Lo que hace cada parte-----------------------------------------------------

--- bool impar(int n) : si n == 1 → true (caso base); si n > 1 → llama a par(n-1)
--- bool par(int n)   : si n == 1 → false (caso base, 1 no es par); si n > 1 → llama a impar(n-1)
--- main()            : prueba ambas funciones del 1 al 10 e imprime PAR o IMPAR

__________________________________________________ RELACIONES DE RECURRENCIA _________________________________________________

--- impar(n): n == 1 → true  | n > 1 → par(n-1)   [el antecesor de un impar es par]
--- par(n):   n == 1 → false | n > 1 → impar(n-1) [el antecesor de un par es impar]
Ejemplo de bobinado para par(4):
par(4) → impar(3) → par(2) → impar(1) → true  ← caso base
desenrollado: par(2) devuelve true → impar(3) devuelve true → par(4) devuelve true 

________________________________________________________EJECUCIÓN________________________________________________________________
1 Abrir terminal y navegar hasta la carpeta del proyecto
2 Compilar: g++ -o ejercicio2 ejercicio2.cpp
3 Ejecutar: ./ejercicio2
4 La salida esperada es:
  1 es IMPAR
  2 es PAR
  3 es IMPAR
  4 es PAR
  5 es IMPAR
  6 es PAR
  7 es IMPAR
  8 es PAR
  9 es IMPAR
  10 es PAR
