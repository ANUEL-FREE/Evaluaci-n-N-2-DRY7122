import urllib.parse
import requests

# Configuración de la API de MapQuest
# NOTA: Reemplaza este valor con tu token real generado en el laboratorio
API_KEY = "Fi6ak3qo646FAjs9MnA41zTe3Oyk5Hxt"
MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"


def obtener_ruta(origen, destino):
    # Construir la URL de consulta de forma segura
    url = MAIN_API + urllib.parse.urlencode({"key": API_KEY, "from": origen, "to": destino})
    
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
    except Exception as e:
        print(f"\n[Error] No se pudo conectar con la API: {e}")
        return

    # Verificar el estado de la respuesta de MapQuest (0 significa éxito)
    status_code = datos["info"]["statuscode"]
    
    if status_code == 0:
        ruta = datos["route"]
        
        # 1. Distancia en kilómetros (MapQuest por defecto puede entregar millas, validamos/convertimos)
        # Si la API se configura en millas, multiplicamos por 1.60934
        # Nota: Usamos las unidades que entrega la API por defecto (usualmente millas si no se especifica)
        distancia_millas = ruta["distance"]
        distancia_km = distancia_millas * 1.60934
        
        # 2. Duración del viaje (la API lo entrega en segundos)
        segundos_totales = ruta["time"]
        horas = segundos_totales // 3600
        minutos = (segundos_totales % 3600) // 60
        segundos = segundos_totales % 60
        
        # Mostrar Resultados con 2 decimales según requerimiento
        print("\n" + "="*40)
        print(f" VIAJE: {origen.title()} ➔ {destino.title()}")
        print("="*40)
        print(f"• Distancia: {distancia_km:.2f} km")
        print(f"• Duración: {horas} hrs, {minutos} min, {segundos} sec")
        print("-"*40)
        
        # 3. Narrativa del viaje (Maniobras paso a paso)
        print(" NARRATIVA DEL VIAJE:")
        for leg in ruta["legs"]:
            for maneuver in leg["maneuvers"]:
                narrativa = maneuver["narrative"]
                dist_maniobra_km = maneuver["distance"] * 1.60934
                print(f" ➔ {narrativa} ({dist_maniobra_km:.2f} km)")
        print("="*40 + "\n")
        
    elif status_code == 402:
        print("\n[Error] Entrada inválida o ruta no encontrada. Intenta con otras ciudades.\n")
    else:
        print(f"\n[Error] Código de estado de MapQuest: {status_code}. Mensaje: {datos['info']['messages']}\n")


def main():
    print("=============================================")
    print("  Planificador de Viajes - MapQuest API")
    print("=============================================")
    
    while True:
        print("Escriba 'q' en cualquier momento para salir.")
        origen = input("Ciudad de Origen: ").strip()
        if origen.lower() == 'q':
            print("Saliendo del programa...")
            break
            
        destino = input("Ciudad de Destino: ").strip()
        if destino.lower() == 'q':
            print("Saliendo del programa...")
            break
            
        # Validar que no estén vacíos
        if not origen or not destino:
            print("\n[!] Por favor, ingrese ciudades válidas.\n")
            continue
            
        obtener_ruta(origen, destino)

if __name__ == "__main__":
    main()
