import os
from lib.tokenizer import Tokenizer
from lib.classes import Class

class AllTypes(object):
  plain_types = ["int", "char", "boolean"]
  class_types = ["Sys", "Screen", "Array", "Math", "String", "Memory", "Keyboard", "Output"]

class Parser(object):
  def __init__(self, filenames):
    self.tokenizer = Tokenizer()
    self.classes = []
    self.filenames = filenames

  def parse_program(self):
    for filename in self.filenames:
      self.tokenizer.load_file(filename)
      self.classes.append(self.parse_class())

  def parse_class(self):
    assert Class.is_mytype(self.tokenizer)
    c = Class(AllTypes)
    c.parse(self.tokenizer)
    AllTypes.class_types.append(c.name.val)

    return c

if __name__ == "__main__":
  #root = "unit_tests/FunctionDec/"
  #root = "unit_tests/ArrayInit/"
  #root = "unit_tests/SystemFunc/"
  #root = "unit_tests/While/"
  #root = "unit_tests/Average/"
  #root = "unit_tests/Seven/"
  #root = "unit_tests/ConvertToBin/"
  #root = "unit_tests/ComplexArrays_test/"
  root = "unit_tests/Pong/"
  
  main_file = f"{root}/Main.jack"
  ball_file = f"{root}/Ball.jack"
  bat_file = f"{root}/Bat.jack"
  game_file = f"{root}/PongGame.jack"
  

  parser = Parser([ball_file, bat_file, game_file, main_file])
  parser.parse_program()
  print("!!!!!!!!!!!!!!!!!!")
  print("!!!!!!!!!!!!!!!!!!")
  print("!!!!!!!!!!!!!!!!!!")
  print(f"Parsing File: Ball")
  ball_code = parser.classes[0].codegen()
  print(f"Parsing File: Bat")
  bat_code = parser.classes[1].codegen()
  print(f"Parsing File: Game")
  game_code = parser.classes[2].codegen()
  print(f"Parsing File: Main")
  main_code = parser.classes[3].codegen()
  
  final_code = ball_code + bat_code + game_code + main_code
  os.system("rm -f tests/*")
  with open("tests/Ball.vm", "a") as f:
    for code in ball_code:
      f.write(code + "\n") 
  with open("tests/Bat.vm", "a") as f:
    for code in bat_code:
      f.write(code + "\n") 
  with open("tests/PongGame.vm", "a") as f:
    for code in game_code:
      f.write(code + "\n") 
  with open("tests/Main.vm", "a") as f:
    for code in main_code:
      f.write(code + "\n") 
