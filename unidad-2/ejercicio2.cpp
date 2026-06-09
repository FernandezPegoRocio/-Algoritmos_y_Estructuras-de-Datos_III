

//   1. 1 es impar.
//   2. Si un número es impar, su antecesor es par; y viceversa.
//
// Relaciones de recurrencia:
//   impar(n):  si n == 1 → true (caso base)
//              si n  > 1 → par(n - 1)      [el antecesor de un impar es par]
//
//   par(n):    si n == 1 → false (caso base: 1 no es par)
//              si n  > 1 → impar(n - 1)    [el antecesor de un par es impar]
// ------------------------------------------------------------

bool impar(int n);  // declaración adelantada (forward declaration)

bool par(int n) {
    if (n == 1) return false;       // caso base: 1 es impar, no par
    return impar(n - 1);            // el antecesor de un par es impar
}

bool impar(int n) {
    if (n == 1) return true;        // caso base: 1 es impar
    return par(n - 1);              // el antecesor de un impar es par
}

void probarParImpar() {
    cout << "\n========================================" << endl;
    cout << " EJERCICIO 2 - par(n) / impar(n)        " << endl;
    cout << "========================================" << endl;

    for (int i = 1; i <= 10; i++) {
        cout << "  " << i << " es "
             << (par(i) ? "PAR" : "IMPAR") << endl;
    }
}


int main() {
    sistemaTurnos();
    probarParImpar();
    return 0;
}
