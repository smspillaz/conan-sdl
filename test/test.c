#include <stdio.h>
#include <SDL.h>

int main() {
  if (SDL_Init(SDL_INIT_EVENTS)) return 1;
  SDL_Quit();
  return 0;
}
