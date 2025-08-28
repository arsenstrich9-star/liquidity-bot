import pytest

from main import main

def test_main_run_once_does_not_raise():
    # Sollte eine Iteration komplett durchlaufen, ohne Exceptions
    main(run_once=True)
