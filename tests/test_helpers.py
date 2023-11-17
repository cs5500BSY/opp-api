import pytest
from starlette.exceptions import HTTPException
from routers.helpers import check_user_authentication  

def test_check_user_authentication_with_user():
    user = {"username": "testuser", "id": 1}  
    try:
        check_user_authentication(user)
        assert True  
    except HTTPException:
        pytest.fail("HTTPException was raised unexpectedly")

def test_check_user_authentication_without_user():
    with pytest.raises(HTTPException) as excinfo:
        check_user_authentication(None)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Authentication Failed"

