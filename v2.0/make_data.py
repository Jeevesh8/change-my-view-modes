#Script to first make OP-wise split of the AMPERSAND data and then choose train-test-valid set from it
import argparse
import os
from shutil import copyfile, rmtree

from bs4 import BeautifulSoup

def get_thread_ids_to_filenames(root_folder="./v2.0/"):
    thread_ids_to_filenames= {}
    for t in ["negative", "positive"]:
        root = root_folder + t + "/"
        for f in os.listdir(root):
            filename = os.path.join(root, f)
            if os.path.isfile(filename) and f.endswith(".xml"):
                with open(filename, "r") as g:
                    xml_str = g.read()
                parsed_xml = BeautifulSoup(xml_str, "xml")
                thread_id = parsed_xml.find('thread')['ID']
                if thread_id not in thread_ids_to_filenames.keys():
                    thread_ids_to_filenames[thread_id] = []
                thread_ids_to_filenames[thread_id].append(filename)

    with open('./op_wise_split.txt', 'w+') as f:
        for v in thread_ids_to_filenames.values():
            f.write(str(v)+'\n')
    
    return thread_ids_to_filenames

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_sz", required=True, type=int, help="Number of threads to use for train set.")
    parser.add_argument("--test_sz", required=True, type=int, help="Number of threds in test set.")
    parser.add_argument("--data_folder", default="./", help="The folder that has negative/ and positive/ subfolders having threads.")
    parser.add_argument("--save_folder", default="data/", help="Folder to store final data.")
    args = parser.parse_args()
    
    thread_ids_to_filenames = get_thread_ids_to_filenames(args.data_folder)
    
    for split in ["train", "test", "valid"]:
        if os.path.isdir(os.path.join(args.data_folder, args.save_folder, split)):
            rmtree(os.path.join(args.data_folder, args.save_folder, split))
        os.makedirs(os.path.join(args.data_folder, args.save_folder, split), exist_ok=True)
    
    j=0
    for elem in thread_ids_to_filenames.values():
        if j<args.test_sz:
            for filename in elem:
                copyfile(filename, os.path.join(args.data_folder, args.save_folder, "test", filename.split('/')[-2]+'_'+filename.split('/')[-1]))
                j+=1
        elif args.test_sz<=j<args.train_sz+args.test_sz:
            for filename in elem:
                copyfile(filename, os.path.join(args.data_folder, args.save_folder, "train", filename.split('/')[-2]+'_'+filename.split('/')[-1]))
                j+=1
        else:
            for filename in elem:                
                copyfile(filename, os.path.join(args.data_folder, args.save_folder, "valid", filename.split('/')[-2]+'_'+filename.split('/')[-1]))
                j+=1
