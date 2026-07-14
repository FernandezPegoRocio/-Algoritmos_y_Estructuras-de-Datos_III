/*Plantilla del método que crea un árbol binario. Recibe como parámetro un apuntador a un subárbol. La primera vez es la raíz del árbol la cual se inicializó con el valor NULL, indicando que el árbol está vacío. */
template < class T>
	void ArbolBinario<T>::CreaArbol(NodoArbol<T> *Apunt)
	{
		char Resp;
		/*Se crea un nodo. */
		Apunt = new NodoArbol<T> ;
		cout << ”\n\ nIngrese la información a almacenar: ”;
		cin >> Apunt– > Info;
		cout << ”\n\ n” << Apunt– > Info << ”¿Tiene hijo izquierdo(S / N) ? ”;
		cin >> Resp;
		if (Resp == ‘s’)
		{
			/*Se invoca al método con el subárbol izquierdo. Se usa la definición recursiva de un árbol. */
			CreaArbol(Apunt– > HijoIzq);
			Apunt– > HijoIzq = Raiz;
		}

		cout << ”\n\ n” << Apunt– > Info << ”¿Tiene hijo derecho(S / N) ? ”;
		cin >> Resp;
		if (Resp == ‘s’)
		{
			/*Se invoca al método con el subárbol derecho. Se usa la definición recursiva de un árbol. */
			CreaArbol(Apunt– > HijoDer);
			Apunt– > HijoDer = Raiz;
		}

		Raiz = Apunt;
	}