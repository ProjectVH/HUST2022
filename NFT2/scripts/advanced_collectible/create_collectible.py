#!/usr/bin/python3
from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_star, fund_with_link, listen_for_event
import time


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    fund_with_link(advanced_collectible.address)
    transaction = advanced_collectible.createCollectible("None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    # time.sleep(35)
    listen_for_event(
        advanced_collectible, "ReturnedCollectible", timeout=200, poll_interval=10
    )
    requestId = transaction.events["RequestedCollectible"]["requestId"]
    token_id = advanced_collectible.requestIdToTokenId(requestId)
    star = get_star(advanced_collectible.tokenIdToStar(token_id))
    print("receipt of tokenId {} is {}".format(token_id, star))
