#include <Keypad.h>



// ===[ VARIABLES ]=== //
const byte cantidad_de_filas = 4;
const byte cantidad_de_columnas = 4;

const byte pines_filas[cantidad_de_filas] = {2, 3, 4, 5};
const byte pines_columnas[cantidad_de_columnas] = {6, 7, 8, 9};

char lista_botones_teclado[cantidad_de_filas * cantidad_de_columnas];
const char botones_teclado[cantidad_de_filas][cantidad_de_columnas] = 
{
  {'A', 'B', 'C', 'D'},
  {'E', 'F', 'G', 'H'},
  {'I', 'J', 'K', 'L'},
  {'M', 'N', 'O', 'P'}
};

Keypad teclado = Keypad(makeKeymap(botones_teclado), pines_filas, pines_columnas, cantidad_de_filas, cantidad_de_columnas);

const byte vidas_jugador_por_defecto = 3;
const unsigned int tiempo_limite_por_defecto = 3000;

int puntos_jugador;
byte vidas_jugador;
unsigned int tiempo_limite;



// ===[ FUNCIONES DE ARDUINO ]=== //
void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));

  for (int i = 0; i < cantidad_de_filas; i++) {
    for (int j = 0; j < cantidad_de_columnas; j++) {
      lista_botones_teclado[(i * cantidad_de_columnas) + j] = botones_teclado[i][j];
    }
  }

  reiniciar_juego();
}

void loop() {
  char boton_con_topo = lista_botones_teclado[random(0, (cantidad_de_filas * cantidad_de_columnas))];

  Serial.println(obtener_agujeros(boton_con_topo));
  bool presiono_correctamente = esperar_tiempo_limite_y_detectar_teclado(boton_con_topo);
  Serial.println(obtener_resultados(presiono_correctamente));
  
  delay(3000);
}



// ===[ FUNCIONES LOCALES ]=== //
String obtener_agujeros(char agujero_con_topo) {
  int agujero_con_topo_indice = -1;
  for (int i = 1; i <= (cantidad_de_filas * cantidad_de_columnas); i++) {
    char agujero;
    if (lista_botones_teclado[i - 1] == agujero_con_topo) {
      agujero_con_topo_indice = i;
      break;
    }
  }
  return String("game_started," + String(cantidad_de_filas) + "," + String(cantidad_de_columnas) + "," + String(agujero_con_topo_indice));
}

bool esperar_tiempo_limite_y_detectar_teclado(char boton_con_topo) {
  unsigned long tiempo_inicio = millis();
  while (millis() - tiempo_inicio < tiempo_limite) {
    char boton_presionado = teclado.getKey();
    if (boton_presionado) {
      if (boton_presionado == boton_con_topo) {
        return true;
      }
      return false;
    }
  }
  return false;
}

String obtener_resultados(bool presiono_correctamente) {
  if (presiono_correctamente == true) {
    puntos_jugador += 100;

    if (tiempo_limite > 100) {
      tiempo_limite -= 100;
    }
  }
  else {
    vidas_jugador -= 1;
  }
  
  if (vidas_jugador < 1) {
    String resultados = String("game_over," + String(vidas_jugador) + "," + String(puntos_jugador));
    reiniciar_juego();
    return resultados;
  }

  return String("game_results," + String(vidas_jugador) + "," + String(puntos_jugador));
}

void reiniciar_juego() {
  puntos_jugador = 0;
  vidas_jugador = vidas_jugador_por_defecto;
  tiempo_limite = tiempo_limite_por_defecto;
}