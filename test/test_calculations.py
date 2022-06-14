from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import pytest 

@pytest.fixture
def zero_bank_account():
  print("-- creating empty bank account")
  return BankAccount()

@pytest.fixture
def bank_account_with_balance():
  print("-- testing active bank account")
  return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected",[
  (3,2,5), (10,1,11), (7,10,17)
])
def test_add(num1, num2, expected):
  print("testing add function")
  assert add(num1, num2) == expected


# def test_subtract():
#   print("testing subtract function")
#   assert subtract(5, 3) == 2


def test_multiply():
  print("testing multiply function")
  assert multiply(5, 3) == 15


# def test_divide():
#   print("testing divide function")
#   assert divide(15, 3) == 5


def test_bank_default_amount():
  bank_account = BankAccount()
  assert bank_account.balance == 0


def test_bank_set_initial_amount(zero_bank_account):
  assert zero_bank_account.balance == 0


def test_withdraw(bank_account_with_balance):
  bank_account_with_balance.withdraw(20)
  assert bank_account_with_balance.balance == 30


def test_deposit(bank_account_with_balance):
  bank_account_with_balance.deposit(50)
  assert bank_account_with_balance.balance == 100


def test_deposit(bank_account_with_balance):
  bank_account_with_balance.collect_interest()
  assert round(bank_account_with_balance.balance, 4) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100), (50, 10, 40), (1200, 200,1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
  zero_bank_account.deposit(deposited)
  zero_bank_account.withdraw(withdrew)
  assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account_with_balance):
  with pytest.raises(InsufficientFunds):
    bank_account_with_balance.withdraw(200)