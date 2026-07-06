/*Método que realiza el recorrido preorden de un árbol binario. Se usa el recorrido para imprimir la información almacenada en cada uno de sus nodos. Recibe como parámetro el nodo a visitar. La primera vez es la raíz del árbol, luego será la raíz del subárbol izquierdo y la raíz del subárbol derecho y así hasta llegar a las hojas. */
template < class T>
	void ArbolBinario<T>::Preorden(NodoArbol<T> *Apunt)
	{
		if (Apunt)
		{
			cout << Apunt– > Info << ””;
			Preorden(Apunt– > HijoIzq);
			Preorden(Apunt– > HijoDer);
		}
	}

/*Método que realiza el recorrido inorden de un árbol binario. Se usa
el recorrido para imprimir la información almacenada en cada uno de sus
nodos. Recibe como parámetro el nodo a visitar. La primera vez es la
raíz del árbol, luego será la raíz del subárbol izquierdo y la raíz del
subárbol derecho y así hasta llegar a las hojas. */
template < class T>
	void ArbolBinario<T>::Inorden(NodoArbol<T> *Apunt)
	{
		if (Apunt)
		{
			Inorden(Apunt– > HijoIzq);
			cout << Apunt– > Info << ””;
			Inorden(Apunt– > HijoDer);
		}
	}

/*Método que realiza el recorrido postorden de un árbol binario. Se usa
el recorrido para imprimir la información almacenada en cada uno de sus
nodos. Recibe como parámetro el nodo a visitar. La primera vez es la
raíz del árbol, luego será la raíz del subárbol izquierdo y la raíz del
subárbol derecho y así hasta llegar a las hojas. */
template < class T>
	void ArbolBinario<T>::Postorden(NodoArbol<T> *Apunt)
	{
		if (Apunt)
		{
			Postorden(Apunt– > HijoIzq);
			Postorden(Apunt– > HijoDer);
			cout << Apunt– > Info << ””;
		}
    }