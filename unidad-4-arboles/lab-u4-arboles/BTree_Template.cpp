/*Prototipo de la plantilla de la clase ArbolBinario. De esta manera,
en la clase NodoArbol se podrá hacer referencia a ella. */
template < class T>
	class ArbolBinario;
/*Declaración de la clase NodoArbol. Cada nodo almacena la información
(que es la razón de ser de la estructura tipo árbol) y las direcciones
de sus hijos izquierdo y derecho. En la sección pública se establece la
relación de amistad entre esta clase y la clase ArbolBinario para que los
métodos de esta última puedan tener acceso a sus miembros privados. */
template < class T>
	class NodoArbol
	{
		private:
			T Info;
		NodoArbol<T> *HijoIzq;
		NodoArbol<T> *HijoDer;
		public:
			NodoArbol();
		T RegresaInfo();
		friend class ArbolBinario<T> ;
	};
/*Declaración del método constructor por omisión. Inicializa las ligas
a los subárboles con el valor de NULL, indicando que están vacías. */
template < class T>
	NodoArbol<T>::NodoArbol()
	{
		HijoIzq = NULL;
		HijoDer = NULL;
	}

/*Método que permite conocer la información almacenada en el nodo. */
template < class T>
	T NodoArbol<T>::RegresaInfo()
	{
		return Info;
	}

/*Declaración de la clase ArbolBinario. Su atributo es un puntero al
nodo raíz. */
template < class T>
	class ArbolBinario
	{
		private:
			NodoArbol<T> *Raiz;
		public:
			ArbolBinario();
		/*En esta sección se declaran los métodos de acceso y
		➥modificación a los miembros de la clase. */
	};
/*Declaración del método constructor. Inicializa el puntero a la raíz con
el valor NULL, indicando que el árbol está vacío (no tiene nodos). */
template < class T>
	ArbolBinario<T>::ArbolBinario()
	{
		Raiz = NULL;
	}
