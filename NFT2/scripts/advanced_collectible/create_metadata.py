from brownie import AdvancedCollectible, network 
from metadata import sample_metadata
from scripts.helpful_scripts import get_star
from pathlib import Path 
import os 
import requests
import json 

star_meta_dic={
    "RECEIPT1":"ipfs://QmPVhHQyAE1eY6BsbbETFTfK5QUe39MDxhmeiWj7Tk6a71?filename=RECEIPT1.png",
    "RECEIPT2":"ipfs://Qmd4DAbhigJ42yxXPQkcm9yK38SRE7zDLPiKHDP8DyCkQK?filename=RECEIPT2.png",
    "RECEIPT3":"ipfs://QmNbqYMu2HZdMhDiAivG1SSwzqUFBqwZEup5gsZevUkY6s?filename=RECEIPT3.png"
}


def main():
    print ("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible)-1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print("The number of tokens you've deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, advanced_collectible)

def write_metadata(number_of_tokens, nft_contract):
    for token_id in range (number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        star = get_star(nft_contract.tokenIdToStar(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active()) +str(token_id)
            +"-"+star +".json"
        )
        if Path(metadata_file_name).exists():
            print ("{} already found !".format(metadata_file_name))
        else : 
            print ("Creating Metadata File: {}".format(metadata_file_name))
            collectible_metadata["name"] = get_star(nft_contract.tokenIdToStar(token_id))
            collectible_metadata["description"]= "{} is formed".format(collectible_metadata["name"])
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(star)
                image_to_upload = upload_to_ipfs(image_path)
            # image_to_upload = (star_meta_dic[star] if not image_to_upload 
            # else image_to_upload)
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

            
    
def upload_to_ipfs(filepath) : 
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file":image_binary})
        ipfs_hash = response.json () ["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "ipfs://{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri



