# Ejercicio 1 — Árbol Binario de Búsqueda

**Lista de inserción:** G B Q A C K F P D E R H

- Si el valor a insertar es **menor** que el nodo actual → va al **subárbol izquierdo**
- Si el valor a insertar es **mayor** que el nodo actual → va al **subárbol derecho**


## Paso a paso
G es la primera clave → se convierte en la **raíz**.


        G

insertar B < G → va a la izquierda de G.


        G
       /
      B



insertar Q > G → va a la derecha de G.

        G
       / \
      B   Q

insertar A < G → izquierda de G → A < B → izquierda de B.

        G
       / \
      B   Q
     /
    A

insertar C < G → izquierda de G → C > B → derecha de B.


        G
       / \
      B   Q
     / \
    A   C
insertar K > G → derecha de G → K < Q → izquierda de Q.


        G
       / \
      B   Q
     / \ /
    A  C K
insertar F < G → izquierda de G → F > B → derecha de B → F > C → derecha de C.

        G
       / \
      B   Q
     / \ /
    A  C K
        \
         F


insertar P > G → derecha de G → P < Q → izquierda de Q → P > K → derecha de K.


        G
       / \
      B   Q
     / \ /
    A  C K
        \ \
         F  P

insertar D < G → izquierda de G → D > B → derecha de B → D > C → derecha de C → D < F → izquierda de F.

        G
       / \
      B   Q
     / \ /
    A  C K
        \ \
         F  P
        /
       D

insertar E < G → izq G → E > B → der B → E > C → der C → E < F → izq F → E > D → der D.

        G
       / \
      B   Q
     / \ /
    A  C K
        \ \
         F  P
        /
       D
        \
         E


insertar R > G → derecha de G → R > Q → derecha de Q.

        G
       / \
      B   Q
     / \ / \
    A  C K   R
        \ \
         F  P
        /
       D
        \
         E



insertar H > G → der G → H < Q → izq Q → H > K → der K → H < P → izq P.
arbol completo:


        G
       / \
      B   Q
     / \ / \
    A  C K   R
        \ \
         F  P
        /  /
       D  H
        \
         E

