import logging
import os
import random
from typing import cast

from web3 import Web3, HTTPProvider
from web3.exceptions import ContractLogicError
from web3.middleware import Middleware, SignAndSendRawMiddlewareBuilder

from . import tasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("starter_kit")

w3 = Web3(HTTPProvider(os.environ["RPC_URL"]))

sender_account = w3.eth.account.from_key(os.environ["SENDER_PRIVATE_KEY"])

# Set `sender_account` as the sender of all transactions
w3.eth.default_account = sender_account.address

# Set `sender_account` as the signer of all transactions
signer_middleware = cast(
    Middleware, SignAndSendRawMiddlewareBuilder.build(sender_account)
)
w3.middleware_onion.add(signer_middleware)

"""
try:
    tasks.swap_exact_tokens_for_tokens(w3)
except ContractLogicError as e:
    # Contract execution reverted
    logger.warning(e)

exit()
"""

task_list = tasks.tasks

while True:
    task = random.choice(task_list)
    logger.info(task.__name__)
    try:
        task(w3)
    except ContractLogicError as e:
        # Contract execution reverted
        logger.warning(e)
