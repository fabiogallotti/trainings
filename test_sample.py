from trainings import Training


def test_training():
    training = Training(27, 6, 1993)
    assert training.day is 27
    assert training.month == 6
    assert training.year == 1993
