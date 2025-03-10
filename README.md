
# 🎮 Clon de DOOM 🎯

  🎮 Este es un **shooter en primera persona** inspirado en el clásico DOOM, desarrollado en **Python y Pygame** como parte de un proyecto académico.  

⚠️ **Atención:** Todo el código del proyecto, incluyendo la implementación del Árbol de Comportamiento y el Algoritmo A*, fue programado por mí desde cero. Utilicé los videos como referencia para desarrollar la lógica del juego, pero toda la estructura y funcionalidad fueron implementadas manualmente.  

🔹 **Incluye:**  
✅ Árbol de Comportamiento para la IA de los enemigos 🤖  
✅ Algoritmo A* para la navegación de los NPCs 🧐  
✅ Soporte para control de Xbox y Playstation🎮  🏹  
✅ Movimiento fluido en 3D con raycasting 🏃  
✅ Sonidos y sprites 🎧🎨  

---

## 🎯 **Cómo Jugar**
1. **Ejecuta el juego** con:
   ```sh
   python main.py
   ```
2. **Controles:**  
   🔼 **WASD** / **Joystick Izquierdo** → Moverse  
   🎯 **Mouse / Joystick Derecho** → Girar la cámara  
   🏹 **Click Izquierdo / Gatillo del mando** → Disparar  
   ⏹ **ESC** → Salir  

3. **Objetivo:**  
   🔥 Sobrevive eliminando a todos los enemigos en la arena.  
   💀 Si mueres, regresarás al menú principal.  

---

## 🏭️ **Estructura del Proyecto**

```
📚 Parcial-IA-DOOM/
├── main.py → Lógica principal del juego
├── player.py → Control del jugador
├── npc.py → IA de los enemigos (Árbol de Comportamiento + A*)
├── pathfinding.py → Algoritmo A* para movimiento de NPCs
├── weapon.py → Manejo de armas y disparos
├── map.py → Generación del entorno de juego
├── raycasting.py → Renderizado 3D con raycasting
├── settings.py → Configuración del juego
├── sound.py → Sistema de sonidos 🎵
├── object_handler.py → Manejo de objetos en el mapa
├── sprite_object.py → Gestión de sprites y texturas
├── object_renderer.py → Renderizado de objetos en el mundo
├── resources/ → 📁 **Sprites, texturas y sonidos del juego**
```

---

## 🎨 **Recursos Utilizados**

🖼️ **Sprites y Texturas:**  
✅ [The Spriters Resource](https://www.spriters-resource.com/)  
✅ [The Textures Resource](https://www.textures-resource.com/)  
✅ [Sprite Database](https://spritedatabase.net/game/760)  

🎧 **Sonidos:**  
✅ [The Sounds Resource](https://www.sounds-resource.com/)  

⚠️ **Todos los derechos de los sprites, texturas y sonidos pertenecen a sus respectivos creadores. Este proyecto es solo para fines educativos.**  

---

## 🔧 **Requisitos**
Para ejecutar el juego, necesitas instalar `pygame`. Puedes hacerlo con:
```sh
pip install -r requirements.txt
```

---

## 📺 **Videos de Referencia**  
### 🎥 Videos de los que me guié:  
- [Desarrollo de la lógica del juego](https://www.youtube.com/watch?v=ECqUrT7IdqQ&t=837s)  
- [Como hacer el RayCasting](https://www.youtube.com/watch?v=SmKBsArp2dI)  

---



👉 **Repositorio en GitHub:** [https://github.com/Laionealll/Parcial-IA-DOOM](https://github.com/Laionealll/Parcial-IA-DOOM)  


