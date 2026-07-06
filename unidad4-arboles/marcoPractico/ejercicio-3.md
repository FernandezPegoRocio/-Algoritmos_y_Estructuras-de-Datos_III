# Ejercicio 3 — Recorridos del Árbol Binario

**Árbol del Ejercicio 1**

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

## A. Recorrido Preorden

**Orden:** Raíz → Subárbol Izquierdo → Subárbol Derecho

Implementación del laboratorio:
cpp
void Preorden(NodoArbol<T> *Apunt) {
    if (Apunt) {
        cout << Apunt->Info;     // visita raíz
        Preorden(Apunt->HijoIzq); // recorre izquierda
        Preorden(Apunt->HijoDer); // recorre derecha
    }
}

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

**Resultado Preorden:** `G B A C F D E Q K P H R`


## B. Recorrido Inorden

**Orden:** Subárbol Izquierdo → Raíz → Subárbol Derecho

Implementación del laboratorio:
cpp
void Inorden(NodoArbol<T> *Apunt) {
    if (Apunt) {
        Inorden(Apunt->HijoIzq);  // recorre izquierda
        cout << Apunt->Info;      // visita raíz
        Inorden(Apunt->HijoDer);  // recorre derecha
    }
}


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

**Resultado Inorden:** `A B C D E F G H K P Q R`



## C. Recorrido Postorden

**Orden:** Subárbol Izquierdo → Subárbol Derecho → Raíz

Implementación del laboratorio:
cpp
void Postorden(NodoArbol<T> *Apunt) {
    if (Apunt) {
        Postorden(Apunt->HijoIzq); // recorre izquierda
        Postorden(Apunt->HijoDer); // recorre derecha
        cout << Apunt->Info;       // visita raíz
    }
}

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

**Resultado Postorden:** `A E D F C B H P K R Q G`
