from model.game import Game
from service.ai_service import AIService

result = AIService.compute_solution_efficiency(Game.current_word_file)
print(result)
