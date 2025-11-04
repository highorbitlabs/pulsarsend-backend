from fastapi import status

from api.v1.depends import get_current_user, get_privy_id_from_token
from main import app
from schemas.enums import UserRoleEnum
from schemas.user_schemas import UserDetailSchema


def test_get_current_user_returns_user_details(test_client) -> None:
    stub_user = UserDetailSchema(
        id=1,
        privy_id="privy-user-123",
        email="tester@example.com",
        role=UserRoleEnum.customer,
        first_name="Test",
        last_name="User",
    )

    async def override_get_current_user() -> UserDetailSchema:
        return stub_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = test_client.get("/api/v1/user/current_user")

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["privy_id"] == "privy-user-123"
    assert payload["email"] == "tester@example.com"
    assert payload["role"] == UserRoleEnum.customer.value


def test_get_user_balance_returns_aggregated_value(test_client, monkeypatch) -> None:
    expected_privy_id = "privy-user-456"

    async def override_privy_id_from_token() -> str:
        return expected_privy_id

    async def fake_get_user_balance_usecase(privy_id: str) -> float:
        assert privy_id == expected_privy_id
        return 42.25

    app.dependency_overrides[get_privy_id_from_token] = override_privy_id_from_token
    monkeypatch.setattr(
        "usecases.users.user_usecase.get_user_balance_usecase",
        fake_get_user_balance_usecase,
    )

    response = test_client.get("/api/v1/user/balance")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"balance": 42.25}
