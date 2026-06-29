#include <iostream>
#include <queue>
#include <string>

using namespace std;

// ESTRUCTURA CLIENTE

struct Cliente {
    int    turno;
    string nombre;
};

// FUNCIONES DEL SISTEMA

// ── Registrar: push() agrega al rear en O(1) ─────────────
void registrar(queue<Cliente>& cola, int& proximoTurno) {
    string nombre;
    cin.ignore();
    cout << "Nombre del cliente: ";
    getline(cin, nombre);

    Cliente c;
    c.turno  = proximoTurno++;
    c.nombre = nombre;
    cola.push(c);

    cout << "Turno asignado: N°" << c.turno
         << " — " << c.nombre << endl;
}

// ── Próximo cliente: front() + pop() en O(1) ─────────────
void proximoCliente(queue<Cliente>& cola, int box) {
    if (cola.empty()) {
        cout << "No hay clientes en espera." << endl;
        return;
    }
    Cliente c = cola.front();
    cola.pop();
    cout << "\n>>> PROXIMO CLIENTE — BOX N°" << box << " <<<" << endl;
    cout << "    Turno N°" << c.turno << " — " << c.nombre << endl;
}

// ── Listar: recorre una copia de la cola ─────────────────
void listar(queue<Cliente> copia) {
    if (copia.empty()) {
        cout << "No hay clientes en espera." << endl;
        return;
    }
    cout << "\n======= CLIENTES EN ESPERA =======" << endl;
    int pos = 1;
    while (!copia.empty()) {
        Cliente c = copia.front();
        copia.pop();
        cout << "  " << pos++ << ". Turno N°" << c.turno
             << " — " << c.nombre << endl;
    }
}

// ── Ver próximo sin llamar: front() sin pop() ────────────
void verProximo(const queue<Cliente>& cola) {
    if (cola.empty()) {
        cout << "No hay clientes en espera." << endl;
        return;
    }
    const Cliente& c = cola.front();
    cout << "Proximo en ser llamado: Turno N°"
         << c.turno << " — " << c.nombre << endl;
}

// MENÚ

void menu() {
    queue<Cliente> cola;
    int proximoTurno = 1;
    int opcion;
    int box = 1;

    do {
        cout << "\n====== SISTEMA DE TURNOS (STL) ======" << endl;
        cout << "1. Registrar cliente"                   << endl;
        cout << "2. Proximo cliente — Box N°" << box     << endl;
        cout << "3. Ver clientes en espera"              << endl;
        cout << "4. Ver proximo sin llamar"              << endl;
        cout << "0. Salir"                               << endl;
        cout << "Opcion: ";
        cin >> opcion;

        switch (opcion) {
            case 1:
                registrar(cola, proximoTurno);
                break;
            case 2:
                proximoCliente(cola, box);
                break;
            case 3:
                listar(cola);
                break;
            case 4:
                verProximo(cola);
                break;
            case 0:
                cout << "Saliendo del sistema." << endl;
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
