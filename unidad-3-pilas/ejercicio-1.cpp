

#include <iostream>
#include <string>

using namespace std;

// NODO DE CLIENTE

struct Cliente {
    int    turno;
    string nombre;
};

// CLASE COLA PROPIA

class Cola {
private:
    static const int MAX = 50;
    Cliente datos[MAX];
    int     front;
    int     rear;
    int     contador;
    int     proximoTurno;

public:
    Cola() : front(-1), rear(-1), contador(0), proximoTurno(1) {}

    // ── isEmpty: front == rear indica cola vacía ─────────────
    bool isEmpty() const {
        return front == rear;
    }

    // ── isFull ───────────────────────────────────────────────
    bool isFull() const {
        return rear == MAX - 1;
    }

    int size() const {
        return contador;
    }

    // ── enqueue: agrega al rear ──────────────────────────────
    // Costo O(1)
    void enqueue(const string& nombre) {
        if (isFull()) {
            cout << "Error: la cola de turnos esta llena." << endl;
            return;
        }
        Cliente c;
        c.turno  = proximoTurno++;
        c.nombre = nombre;
        datos[++rear] = c;
        if (front == -1) front = 0;
        contador++;
        cout << "Turno asignado: N°" << c.turno
             << " — " << c.nombre << endl;
    }

    // ── dequeue: elimina del front (próximo cliente) ─────────
    // Costo O(1)
    Cliente dequeue() {
        if (isEmpty()) {
            throw string("No hay clientes en espera.");
        }
        Cliente c = datos[front];
        if (front == rear) {
            // último elemento: resetear
            front = rear = -1;
        } else {
            front++;
        }
        contador--;
        return c;
    }

    // ── getFront: ver quién es el próximo sin eliminarlo ─────
    Cliente getFront() const {
        if (isEmpty()) {
            throw string("No hay clientes en espera.");
        }
        return datos[front];
    }

    // ── listar todos los clientes en cola ────────────────────
    void listar() const {
        if (isEmpty()) {
            cout << "No hay clientes en espera." << endl;
            return;
        }
        cout << "\n======= CLIENTES EN ESPERA =======" << endl;
        for (int i = front; i <= rear; i++) {
            cout << "  Turno N°" << datos[i].turno
                 << " — " << datos[i].nombre << endl;
        }
        cout << "Total en espera: " << contador << endl;
    }
};

// MENÚ PRINCIPAL

void menu(Cola& cola) {
    int opcion;
    int box = 1;

    do {
        cout << "\n====== SISTEMA DE TURNOS ======" << endl;
        cout << "1. Registrar cliente"              << endl;
        cout << "2. Proximo cliente — Box N°" << box << endl;
        cout << "3. Ver clientes en espera"         << endl;
        cout << "4. Ver proximo sin llamar"         << endl;
        cout << "0. Salir"                          << endl;
        cout << "Opcion: ";
        cin >> opcion;
        cin.ignore();

        switch (opcion) {
            case 1: {
                string nombre;
                cout << "Nombre del cliente: ";
                getline(cin, nombre);
                cola.enqueue(nombre);
                break;
            }
            case 2: {
                try {
                    Cliente c = cola.dequeue();
                    cout << "\n>>> PROXIMO CLIENTE — BOX N°" << box
                         << " <<<" << endl;
                    cout << "    Turno N°" << c.turno
                         << " — " << c.nombre << endl;
                } catch (const string& e) {
                    cout << "Error: " << e << endl;
                }
                break;
            }
            case 3:
                cola.listar();
                break;
            case 4: {
                try {
                    Cliente c = cola.getFront();
                    cout << "Proximo en ser llamado: Turno N°"
                         << c.turno << " — " << c.nombre << endl;
                } catch (const string& e) {
                    cout << "Error: " << e << endl;
                }
                break;
            }
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
    Cola cola;
    menu(cola);
    return 0;
}
