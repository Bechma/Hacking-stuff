// 3 en raya
#include <iostream>
using namespace std;

class Raya{
	string jugador1, jugador2;
	int tablero[3][3];
	int ganadas1 = 0, ganadas2 = 0;
	//Jugador 1 son las X
	//Jugador 2 son las O
	
	void LimpiarTablero(){
		for(int i = 0; i < 9; i++)
			tablero[0][i] = 0;
	}
	
	void TableroLleno(){
		int contador = 0;
		for(int i = 0; i < 9; i++)
			if(tablero[0][i] != 0)
				contador++;
		
		if(contador == 9)
			LimpiarTablero();
	}
	
	public:
		Raya() : jugador1("Pepe"), jugador2("Pablo") {LimpiarTablero(); }
		
		Raya(string uno, string dos) : jugador1(uno), jugador2(dos) {
			LimpiarTablero();
		}
		
		string Ganador(){
			int cont_uno, cont_dos, i;
			bool encontrado = false;
			string adevolver;
			
			//Comprobar Horizontal
			for(i = 0, cont_uno = 0, cont_dos = 0; i < 3 && !encontrado; i++){
				for(int j = 0; j < 3; j++)
					if(tablero[i][j] != 0){
						if(tablero[i][j] == 1)
							cont_uno++;
						else
							cont_dos++;
					}
				
				if(cont_uno == 3){
					adevolver = jugador1;
					encontrado = true;
					ganadas1++;
					LimpiarTablero();
				}
				else
					cont_uno = 0;
				if(cont_dos == 3){
					adevolver = jugador2;
					encontrado = true;
					ganadas2++;
					LimpiarTablero();
				}
				else
					cont_dos = 0;
			}
			
			//Comprobar Vertical
			for(i = 0, cont_uno = 0, cont_dos = 0; i < 3 && !encontrado; i++){
				for(int j = 0; j < 3; j++)
					if(tablero[j][i] != 0){
						if(tablero[j][i] == 1)
							cont_uno++;
						else
							cont_dos++;
					}
				
				if(cont_uno == 3){
					adevolver = jugador1;
					encontrado = true;
					ganadas1++;
					LimpiarTablero();
				}
				else
					cont_uno = 0;
				if(cont_dos == 3){
					adevolver = jugador2;
					encontrado = true;
					ganadas2++;
					LimpiarTablero();
				}
				else
					cont_dos = 0;
			}
			
			//Comprobar Diagonal
			if(	(tablero[0][0] == tablero[1][1]) && (tablero[0][0] == tablero[2][2])	){
				if(tablero[0][0] == 1){
					adevolver = jugador1;
					ganadas1++;
					LimpiarTablero();
				}
				if(tablero[0][0] == 2){
					adevolver = jugador2;
					ganadas2++;
					LimpiarTablero();
				}
			}
			if(	(tablero[2][0] == tablero[1][1]) && (tablero[2][0] == tablero[0][2])	){
				if(tablero[2][0] == 1){
					adevolver = jugador1;
					ganadas1++;
					LimpiarTablero();
				}
				if(tablero[2][0] == 2){
					adevolver = jugador2;
					ganadas2++;
					LimpiarTablero();
				}
			}
			
			TableroLleno();
			
			return adevolver;
		}
		
		void CrearTablero(string name){
			for(int i = 0; i < 3; i++){
				cout << "||";
				for(int j = 0; j < 3; j++){
					if(tablero[i][j] == 1)
						cout << "\tX";
					else if (tablero[i][j] == 2)
						cout << "\tO";
					else if (tablero[i][j] == 0)
						cout << "\t";
					cout << "\t||";
				}
				
				cout << endl << "--------------------------------------------------" << endl;
			}
			
			cout << "\n\n" << "Ficha X ..." << jugador1 << " lleva ganadas: " << ganadas1 << endl;
			cout << "Ficha O ..." << jugador2 << " lleva ganadas: " << ganadas2 << endl;
			
			cout << "Turno de " << name << endl;
		}
		
		int gettab(int i) const{
			return tablero[0][i];
		}
		
		int getganadas1() const{
			return ganadas1;
		}
		
		int getganadas2() const{
			return ganadas2;
		}
		
		string getjugador1() const{
			return jugador1;
		}
		
		string getjugador2() const{
			return jugador2;
		}
		
		void settab(int introducir, int aux){
			if(introducir >= 0 && introducir < 9 && (aux == 1 || aux == 2))
				tablero[0][introducir] = aux;
		}
		
		
};

void Instrucciones(){
	cout << "Introduce un numero para poner tu ficha en la cuadricula" << endl << "Dicha cuadricula se divide de esta forma:" << endl;
	
	int cont = 6;
	for(int i = 1; i <= 9; i++){
		cout << i+cont << "\t";
		if(i % 3 == 0){
			cout << endl;
			cont-=6;
		}
	}
}

int main (void){
	string uno, dos;
	char basura;
	
	cout << "Introduce el nombre del jugador 1: ";
	cin >> uno;
	
	do{
		cout << "Introduce otro nombre para el jugador 2: ";
		cin >> dos;
	}while(uno == dos);
	
	Raya juego(uno, dos);
	
	cout << "Almacenando..." << endl; cin.get(basura); system("clear");
	
	Instrucciones(); cin.get(basura); system("clear");
	
	string turno = uno;
	
	while(true){
		int introducir;
		
		do{
			system("clear");
			juego.CrearTablero(turno);
			cin.clear();
			cin.ignore();
			cin >> introducir;
		}while(cin.fail());
		
		if(introducir == 1 || introducir == 2 || introducir == 3)
				introducir += 6;
			else
				if(introducir == 7 || introducir == 8 || introducir == 9)
					introducir -= 6;
			
		introducir--;
		
		if(!((introducir < 0 || introducir > 8)	|| juego.gettab(introducir) != 0)){
			
			if(turno == juego.getjugador1())
				juego.settab(introducir, 1);
			else
				juego.settab(introducir, 2);
			
			string aux = juego.Ganador();
			if(aux != ""){
				cout << "Ha ganado: " << aux << endl;
				cin.get(basura);
			}
			if (turno == uno)
				turno = dos;
			else
				turno = uno;
		}
		
	}
	
	return 0;
}
