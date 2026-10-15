from repairbot.user_handler.user_handler import UserHandler

uh = UserHandler()


def test_add_true():
    uh.remove_user("TEST", "test")
    assert uh.add_user("TEST", "test") == True


def test_add_false():
    assert uh.add_user("TEST", "test") == False


def test_remove():
    assert uh.remove_user("TEST", "test") == True


def test_remove_no_user():
    assert uh.remove_user("TEST", "test") == False


def test_add_after_remove():
    assert uh.add_user("TEST", "test") == True


def test_authenticate_true():
    assert uh.authenticate_user("TEST", "test") == True


def test_authenticate_false():
    assert uh.authenticate_user("TEST", "alma") == False


def test_authenticate_no_user():
    assert uh.authenticate_user("ALMA", "barack") == False

def test_remove_end():
    assert uh.remove_user("TEST", "test") == True