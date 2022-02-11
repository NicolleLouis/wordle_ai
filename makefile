run:
	PYTHONPATH=. python main.py

dictionnaire:
	PYTHONPATH=. python larousse_main.py

test:
	PYTHONPATH=. pytest model/

cheat:
	PYTHONPATH=. python __main_cheat__.py
