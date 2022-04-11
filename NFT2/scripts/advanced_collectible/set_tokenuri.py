from brownie import AdvancedCollectible, network, accounts, config 
from scripts.helpful_scripts import get_star
from datetime import datetime 


star_meta_dic={
    "RECEIPT1" :"ipfs://QmbYrefwkYAQ5fCbjjbNHArjtiVfCqcdyvvzWgRzuXxcrG?filename=0-RECEIPT1.json",
    "RECEIPT2" :"ipfs://QmYztbnkG83mKKbyh1roi3dxVZVor6nZZAoGaBXtELNkds?filename=2-RECEIPT2.json",
    "RECEIPT3" :"ipfs://QmT5zRzfreH6mJ1ikYr14ZN9PTzeQfy3t5eDzmHgTPHBJo?filename=1-RECEIPT3.json"

}

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def main():
    print ("working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible)-1]
    number_of_advacned_collectibles = advanced_collectible.tokenCounter()
    print("The number of tokens you have deployed is :" + str(number_of_advacned_collectibles))

    for token_id in range(number_of_advacned_collectibles):
        star = get_star (advanced_collectible.tokenIdToStar(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, advanced_collectible, star_meta_dic[star])
        else: 
            print ("skipping {}, we have set the tokenURI".format(token_id))

def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    current_time = datetime.now()
    print (
        "You can view your NFT at {} at {}".format(
            OPENSEA_FORMAT.format (nft_contract.address, token_id),
            current_time
        )
    )
    print("Please give up to 20 minutes, and hit the refresh button!")
