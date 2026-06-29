
#include <iostream>
#include <list>
#include <string>
#include <algorithm>

using namespace std;

// ESTRUCTURA PACIENTE

struct Paciente {
    int    id;
    string nombre;
    int    edad;
    string diagnostico;
};

// FUNCIONES DEL SISTEMA
// Genera el próximo ID disponible
int nuevoId(const list<Paciente>& lista) {
    return (int)lista.size() + 1;
}

// Muestra los datos de un paciente
void mostrarPaciente(const Paciente& p) {
    cout << "  ID          : " << p.id          << endl;
    cout << "  Nombre      : " << p.nombre      << endl;
    cout << "  Edad        : " << p.edad        << endl;
    cout << "  Diagnostico : " << p.diagnostico << endl;
}

// ── REGISTRAR — push_back() inserta al final en O(1) ────────
void registrar(list<Paciente>& lista) {
    Paciente p;
    p.id = nuevoId(lista);
    cin.ignore();
    cout << "Nombre: ";
    getline(cin, p.nombre);
    cout << "Edad: ";
    cin >> p.edad;
    cin.ignore();
    cout << "Diagnostico: ";
    getline(cin, p.diagnostico);

    lista.push_back(p);
    cout << "Paciente registrado correctamente (ID: " << p.id << ")." << endl;
}

// ── BUSCAR por ID usando iterador ────────────────────────────
// std::list no tiene acceso aleatorio — se recorre con iterador
list<Paciente>::iterator buscarPorId(list<Paciente>& lista, int id) {
    for (auto it = lista.begin(); it != lista.end(); ++it) {
        if (it->id == id)
            return it;
    }
    return lista.end();  // no encontrado
}

// ── MODIFICAR ────────────────────────────────────────────────
void modificar(list<Paciente>& lista) {
    if (lista.empty()) {
        throw string("La lista esta vacia. No hay pacientes para modificar.");
    }

    int id;
    cout << "ID del paciente a modificar: ";
    cin >> id;

    auto it = buscarPorId(lista, id);
    if (it == lista.end()) {
        cout << "No se encontro un paciente con ID " << id << "." << endl;
        return;
    }

    cout << "\nDatos actuales:" << endl;
    mostrarPaciente(*it);

    cout << "\nIngrese los nuevos datos:" << endl;
    cin.ignore();
    cout << "Nuevo nombre: ";
    getline(cin, it->nombre);
    cout << "Nueva edad: ";
    cin >> it->edad;
    cin.ignore();
    cout << "Nuevo diagnostico: ";
    getline(cin, it->diagnostico);

    cout << "Paciente modificado correctamente." << endl;
}

// ── ELIMINAR — erase() elimina en O(1) con iterador ─────────
void eliminar(list<Paciente>& lista) {
    if (lista.empty()) {
        throw string("La lista esta vacia. No hay pacientes para eliminar.");
    }

    int id;
    cout << "ID del paciente a eliminar: ";
    cin >> id;

    auto it = buscarPorId(lista, id);
    if (it == lista.end()) {
        cout << "No se encontro un paciente con ID " << id << "." << endl;
        return;
    }

    lista.erase(it);
    cout << "Paciente con ID " << id << " eliminado correctamente." << endl;
}

// ── LISTAR — recorre con iterador begin() → end() ────────────
void listar(const list<Paciente>& lista) {
    if (lista.empty()) {
        cout << "No hay pacientes registrados." << endl;
        return;
    }

    cout << "\n========== LISTADO DE PACIENTES ==========" << endl;
    for (const auto& p : lista) {
        mostrarPaciente(p);
        cout << "------------------------------------------" << endl;
    }
    cout << "Total de pacientes: " << lista.size() << endl;
}

// MENU
void menu(list<Paciente>& lista) {
    int opcion;

    do {
        cout << "\n========== CLINICA LOCAL — SISTEMA DE PACIENTES (STL) ==========" << endl;
        cout << "1. Registrar paciente"  << endl;
        cout << "2. Modificar paciente"  << endl;
        cout << "3. Eliminar paciente"   << endl;
        cout << "4. Listar pacientes"    << endl;
        cout << "0. Salir"               << endl;
        cout << "Opcion: ";
        cin >> opcion;

        switch (opcion) {
            case 1:
                registrar(lista);
                break;
            case 2:
                try {
                    modificar(lista);
                } catch (const string& e) {
                    cerr << "Error: " << e << endl;
                }
                break;
            case 3:
                try {
                    eliminar(lista);
                } catch (const string& e) {
                    cerr << "Error: " << e << endl;
                }
                break;
            case 4:
                listar(lista);
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
    list<Paciente> lista;
    menu(lista);
    return 0;
}
