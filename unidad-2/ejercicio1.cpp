/*
 * Sistema de Turnos con impresión recursiva del tiempo de espera
 */

#include <iostream>
#include <queue>
#include <string>
#include <ctime>

using namespace std;


struct Cliente {
    string nombre;
    int turno;
    time_t horaLlegada;   // momento en que se registró
};


void imprimirEsperas(queue<Cliente> cola) {
    // Caso base
    if (cola.empty()) {
        return;
    }

    Cliente c = cola.front();
    cola.pop();

    // Tiempo de espera: diferencia entre "ahora" y hora de llegada
    time_t ahora    = time(nullptr);
    double segundos = difftime(ahora, c.horaLlegada);

    cout << "  Turno " << c.turno
         << " | "      << c.nombre
         << " | Espera: " << (int)segundos << " seg" << endl;

    // Llamada recursiva con el resto de la cola
    imprimirEsperas(cola);
}


void sistemaTurnos() {
    queue<Cliente> cola;
    int contadorTurno = 1;
    int opcion;

    cout << "\n========================================" << endl;
    cout << "   SISTEMA DE TURNOS - BOX DE ATENCIÓN  " << endl;
    cout << "========================================" << endl;

    do {
        cout << "\n--- MENÚ ---" << endl;
        cout << "1. Registrar cliente" << endl;
        cout << "2. Proximo cliente (Box N°1)" << endl;
        cout << "3. Ver turnos en espera" << endl;
        cout << "4. Ver tiempos de espera (recursivo)" << endl;
        cout << "0. Salir" << endl;
        cout << "Opcion: ";
        cin >> opcion;
        cin.ignore();

        switch (opcion) {
            case 1: {
                Cliente c;
                cout << "Nombre del cliente: ";
                getline(cin, c.nombre);
                c.turno       = contadorTurno++;
                c.horaLlegada = time(nullptr);
                cola.push(c);
                cout << "Turno asignado: " << c.turno << endl;
                break;
            }
            case 2: {
                if (cola.empty()) {
                    cout << "No hay clientes en espera." << endl;
                } else {
                    Cliente c = cola.front();
                    cola.pop();
                    cout << "\n>>> PRÓXIMO CLIENTE - BOX N°1 <<<" << endl;
                    cout << "    Turno " << c.turno
                         << " | "       << c.nombre << endl;
                }
                break;
            }
            case 3: {
                if (cola.empty()) {
                    cout << "No hay clientes en espera." << endl;
                } else {
                    queue<Cliente> copia = cola;
                    cout << "\nClientes en orden de llegada:" << endl;
                    while (!copia.empty()) {
                        Cliente c = copia.front();
                        copia.pop();
                        cout << "  Turno " << c.turno
                             << " | "      << c.nombre << endl;
                    }
                }
                break;
            }
            case 4: {
                if (cola.empty()) {
                    cout << "No hay clientes en espera." << endl;
                } else {
                    cout << "\nTiempos de espera (calculado recursivamente):" << endl;
                    imprimirEsperas(cola);
                }
                break;
            }
            case 0:
                cout << "Saliendo del sistema de turnos." << endl;
                break;
            default:
                cout << "Opción inválida." << endl;
        }

    } while (opcion != 0);
}


int main() {
    sistemaTurnos();
    return 0;
}
