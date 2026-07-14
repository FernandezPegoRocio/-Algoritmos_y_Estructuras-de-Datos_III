# Ejercicio 2 — Eliminaciones iterativas del árbol

**Árbol inicial del Ejercicio 1:**


              G
           /     \
          B       Q
         / \     / \
        A   C   K   R
             \   \
              F   P
             /   /
            D   H
             \
              E


---

## a) Eliminar E

**Caso:** E es un **nodo hoja** (no tiene hijos).

**Procedimiento:** se elimina directamente sin necesidad de reestructurar.

E es hijo derecho de D → se desconecta D del nodo E.


              G
           /     \
          B       Q
         / \     / \
        A   C   K   R
             \   \
              F   P
             /   /
            D   H

## b) Eliminar C

**Caso:** C tiene **un solo hijo** (su hijo derecho F).

**Procedimiento:** se reemplaza C por su único hijo. El padre de C (que es B) ahora apunta directamente a F.

              G
           /     \
          B       Q
         / \     / \
        A   F   K   R
           /     \
          D       P
                 /
                H


## c) Eliminar G

**Caso:** G es la **raíz** y tiene **dos hijos**.

**Procedimiento:** al eliminar un nodo con dos hijos se busca su **sucesor inorden** — el nodo con el valor mínimo del subárbol derecho, que es el nodo más a la izquierda de ese subárbol.

El subárbol derecho de G está encabezado por Q. El mínimo de ese subárbol es **H** (recorriendo: Q → K → P → H).

**Pasos:**
1. Se copia el valor de H en el lugar de G (la raíz pasa a ser H).
2. Se elimina el nodo H original del lugar donde estaba (hijo izquierdo de P).
3. H era nodo hoja → se elimina directamente.

              H
           /     \
          B       Q
         / \     / \
        A   F   K   R
           /     \
          D       P
