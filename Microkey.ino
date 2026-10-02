#include <Keyboard.h>

void setup() {
  // Start USB keyboard
  Keyboard.begin();

  // Give the computer time to recognize the MicroKey
  delay(3000);

  // Type the test sentence
  Keyboard.print("The quick brown fox jumps over the lazy dog.");

  // Release the keyboard
  Keyboard.releaseAll();

  // Stop sending keyboard input
  Keyboard.end();
}

void loop() {
  // Nothing else happens
}