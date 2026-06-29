#include <iostream>
#include <stack>
#include <string>

using namespace std;

// REGISTRO DE LLAMADA

struct Llamada {
    string numero;
    string nombre;   // contacto (puede quedar como "Desconocido")
};

// FUNCIONES

// ── Registrar llamada: push() apila en O(1) ──────────────
void registrarLlamada(stack<Llamada>& historial) {
    Llamada ll;
    cin.ignore();
    cout << "Numero de telefono: ";
    getline(cin, ll.numero);
    cout << "Nombre del contacto (Enter si desconocido): ";
    getline(cin, ll.nombre);
    if (ll.nombre.empty()) ll.nombre = "Desconocido";

    historial.push(ll);
    cout << "Llamada a " << ll.nombre
         << " (" << ll.numero << ") registrada." << endl;
}

// ── Volver: pop() desapila la última llamada ─────────────
// Equivale al botón Back: retrocede en el historial
void volver(stack<Llamada>& historial) {
    if (historial.empty()) {
        cout << "El historial esta vacio. No hay llamadas anteriores." << endl;
        return;
    }
    Llamada ll = historial.top();
    historial.pop();
    cout << "\n<<< LLAMADA ANTERIOR >>>" << endl;
    cout << "  Contacto : " << ll.nombre  << endl;
    cout << "  Numero   : " << ll.numero  << endl;
}

// ── Ver última: top() sin pop() ──────────────────────────
void verUltima(const stack<Llamada>& historial) {
    if (historial.empty()) {
        cout << "El historial esta vacio." << endl;
        return;
    }
    const Llamada& ll = historial.top();
    cout << "Ultima llamada registrada:" << endl;
    cout << "  Contacto : " << ll.nombre  << endl;
    cout << "  Numero   : " << ll.numero  << endl;
}

// ── Recorrer historial completo (copia de la pila) ───────
// Muestra desde la más reciente hasta la más antigua
void verHistorial(stack<Llamada> copia) {
    if (copia.empty()) {
        cout << "El historial esta vacio." << endl;
        return;
    }
    cout << "\n======= HISTORIAL DE LLAMADAS =======" << endl;
    cout << "  (mas reciente → mas antigua)"          << endl;
    int pos = 1;
    while (!copia.empty()) {
        Llamada ll = copia.top();
        copia.pop();
        cout << "  " << pos++ << ". "
             << ll.nombre << " — " << ll.numero << endl;
    }
}

// MENÚ

void menu() {
    stack<Llamada> historial;
    int opcion;

    do {
        cout << "\n====== HISTORIAL DE LLAMADAS ======" << endl;
        cout << "1. Registrar nueva llamada"             << endl;
        cout << "2. Volver (llamada anterior)"           << endl;
        cout << "3. Ver ultima llamada"                  << endl;
        cout << "4. Ver historial completo"              << endl;
        cout << "0. Salir"                               << endl;
        cout << "Opcion: ";
        cin >> opcion;

        switch (opcion) {
            case 1:
                registrarLlamada(historial);
                break;
            case 2:
                volver(historial);
                break;
            case 3:
                verUltima(historial);
                break;
            case 4:
                verHistorial(historial);
                break;
            case 0:
                cout << "Saliendo del historial." << endl;
                break;
            default:
                cout << "Opcion invalida." << endl;
        }
    } while (opcion != 0);
}

// MAIN

int main() {
    menu();
    return 0;
}
