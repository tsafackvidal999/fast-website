
from pymesomb.operations import PaymentOperation
from pymesomb.utils import RandomGenerator
from datetime import datetime

operation = PaymentOperation('2e4de0586e2689e6cd5a1cf152ca19ecf4302b9c', '962085e2-5f3e-460b-b0ec-d9c007722b4c', 'eb52d60b-3265-4f83-a7ee-e888eff3a3b8')
response = operation.make_deposit({
    'amount': 500,
    'service': 'MTN',
    'receiver': '674579282',
    'date': datetime.now(),
    'nonce': RandomGenerator.nonce(),
    'trxID': '1'
})
print(response.is_operation_success())
print(response.is_transaction_success())
