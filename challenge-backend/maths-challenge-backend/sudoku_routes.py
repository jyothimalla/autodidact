from fastapi import APIRouter
import random

sudoku_router = APIRouter()

def generate_easy_sudoku():
    # Simple placeholder: a 4x4 grid with some cells filled
    board = [
        [1, 0, 0, 4],
        [0, 0, 3, 0],
        [0, 3, 0, 0],
        [2, 0, 0, 1],
    ]
    return board

@sudoku_router.get("/sudoku/easy")
def get_easy_sudoku():
    return {"puzzle": generate_easy_sudoku()}
