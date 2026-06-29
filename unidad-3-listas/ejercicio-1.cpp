

#include <iostream>
#include <string>
#include <cassert>

using namespace std;

// NODO — contiene los datos del paciente y punteros prev/next

struct Paciente {
    int    id;
    string nombre;
    int    edad;
    string diagnostico;
};

struct Nodo {
    Paciente dato;
    Nodo*    prev;
    Nodo*    next;

    Nodo(Paciente p) : dato(p), prev(nullptr), next(nullptr) {}
};

// LISTA DOBLEMENTE VINCULADA

class ListaPacientes {
private:
    Nodo* head;
    Nodo* tail;
    int   contador;

public:
    ListaPacientes() : head(nullptr), tail(nullptr), contador(0) {}

    ~ListaPacientes() {
        Nodo* tmp = head;
        while (tmp != nullptr) {
            Nodo* sig = tmp->next;
            delete tmp;
            tmp = sig;
        }
    }

    bool isEmpty() const {
        return head == nullptr;
    }

    int size() const {
        return contador;
    }

    // ── REGISTRAR paciente (inserción al final) ──────────────
    // Costo O(1) gracias al puntero tail
    void registrar(Paciente p) {
        Nodo* nuevo = new Nodo(p);

        if (isEmpty()) {
            head = tail = nuevo;
        } else {
            nuevo->prev = tail;
            tail->next  = nuevo;
            tail        = nuevo;
        }
        contador++;
        cout << "Paciente registrado correctamente (ID: " << p.id << ")." << endl;
    }

    // ── BUSCAR por ID (para modificar / eliminar) ────────────
    // Costo O(n) — recorre desde head hasta encontrar el nodo
    Nodo* buscarPorId(int id) {
        Nodo* tmp = head;
        while (tmp != nullptr) {
            if (tmp->dato.id == id)
                return tmp;
            tmp = tmp->next;
        }
        return nullptr;
    }

    // ── MODIFICAR paciente ───────────────────────────────────
    void modificar(int id) {
        if (isEmpty()) {
            throw string("La lista esta vacia. No hay pacientes para modificar.");
        }

        Nodo* nodo = buscarPorId(id);
        if (nodo == nullptr) {
            cout << "No se encontro un paciente con ID " << id << "." << endl;
            return;
        }

        cout << "\nDatos actuales del paciente:" << endl;
        mostrarPaciente(nodo->dato);

        cout << "\nIngrese los nuevos datos:" << endl;
        cin.ignore();
        cout << "Nuevo nombre: ";
        getline(cin, nodo->dato.nombre);
        cout << "Nueva edad: ";
        cin >> nodo->dato.edad;
        cin.ignore();
        cout << "Nuevo diagnostico: ";
        getline(cin, nodo->dato.diagnostico);

        cout << "Paciente modificado correctamente." << endl;
    }

    // ── ELIMINAR paciente ────────────────────────────────────
    // Lista doble: O(1) una vez localizado el nodo
    void eliminar(int id) {
        if (isEmpty()) {
            throw string("La lista esta vacia. No hay pacientes para eliminar.");
        }

        Nodo* nodo = buscarPorId(id);
        if (nodo == nullptr) {
            cout << "No se encontro un paciente con ID " << id << "." << endl;
            return;
        }

        // Reconectar vecinos
        if (nodo->prev != nullptr)
            nodo->prev->next = nodo->next;
        else
            head = nodo->next;  // era el primero

        if (nodo->next != nullptr)
            nodo->next->prev = nodo->prev;
        else
            tail = nodo->prev;  // era el último

        delete nodo;
        contador--;
        cout << "Paciente con ID " << id << " eliminado correctamente." << endl;
    }

    // ── LISTAR todos los pacientes ───────────────────────────
    void listar() const {
        assert(!isEmpty()); // manejo de error — aborta si lista vacía

        cout << "\n========== LISTADO DE PACIENTES ==========" << endl;
        Nodo* tmp = head;
        while (tmp != nullptr) {
            mostrarPaciente(tmp->dato);
            cout << "------------------------------------------" << endl;
            tmp = tmp->next;
        }
        cout << "Total de pacientes: " << contador << endl;
    }

    // ── MOSTRAR un paciente (auxiliar) ───────────────────────
    void mostrarPaciente(const Paciente& p) const {
        cout << "  ID          : " << p.id          << endl;
        cout << "  Nombre      : " << p.nombre      << endl;
        cout << "  Edad        : " << p.edad        << endl;
        cout << "  Diagnostico : " << p.diagnostico << endl;
    }

    // ── GENERAR ID autoincremental ───────────────────────────
    int nuevoId() const {
        return contador + 1;
    }
};

// MENU
void menu(ListaPacientes& lista) {
    int opcion;

    do {
        cout << "\n========== CLINICA LOCAL — SISTEMA DE PACIENTES ==========" << endl;
        cout << "1. Registrar paciente"   << endl;
        cout << "2. Modificar paciente"   << endl;
        cout << "3. Eliminar paciente"    << endl;
        cout << "4. Listar pacientes"     << endl;
        cout << "0. Salir"                << endl;
        cout << "Opcion: ";
        cin >> opcion;

        switch (opcion) {
            case 1: {
                Paciente p;
                p.id = lista.nuevoId();
                cin.ignore();
                cout << "Nombre: ";
                getline(cin, p.nombre);
                cout << "Edad: ";
                cin >> p.edad;
                cin.ignore();
                cout << "Diagnostico: ";
                getline(cin, p.diagnostico);
                lista.registrar(p);
                break;
            }
            case 2: {
                int id;
                cout << "ID del paciente a modificar: ";
                cin >> id;
                try {
                    lista.modificar(id);
                } catch (const string& e) {
                    cerr << "Error: " << e << endl;
                }
                break;
            }
            case 3: {
                int id;
                cout << "ID del paciente a eliminar: ";
                cin >> id;
                try {
                    lista.eliminar(id);
                } catch (const string& e) {
                    cerr << "Error: " << e << endl;
                }
                break;
            }
            case 4: {
                if (lista.isEmpty()) {
                    cout << "No hay pacientes registrados." << endl;
                } else {
                    lista.listar();
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
    ListaPacientes lista;
    menu(lista);
    return 0;
}
