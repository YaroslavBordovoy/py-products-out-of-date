import datetime
from unittest import mock

import pytest

from app.main import outdated_products


@pytest.fixture()
def products() -> list[dict]:
    yield [
        {
            "name": "salmon",
            "expiration_date": datetime.date(2022, 2, 10),
            "price": 600
        },
        {
            "name": "chicken",
            "expiration_date": datetime.date(2022, 2, 5),
            "price": 120
        },
        {
            "name": "duck",
            "expiration_date": datetime.date(2022, 2, 1),
            "price": 160
        }
    ]


@pytest.mark.parametrize(
    "mocked_time,expected",
    [
        (datetime.date(2022, 6, 10), ["salmon", "chicken", "duck"]),
        (datetime.date(2022, 1, 1), []),
        (datetime.date(2022, 2, 3), ["duck"]),
        (datetime.date(2022, 2, 11), ["salmon", "chicken", "duck"]),
        (datetime.date(2022, 2, 10), ["chicken", "duck"])
    ]
)
def test_outdated_products(products: list[dict],
                           mocked_time: datetime.date,
                           expected: list) -> None:
    with mock.patch("app.main.datetime.date") as mock_date:
        mock_date.today.return_value = mocked_time
        assert outdated_products(products) == expected
