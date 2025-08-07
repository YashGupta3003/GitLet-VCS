#!/usr/bin/env python3



import difflib
import pathlib
import hashlib
from readline import get_current_history_length
import sys
import os
import logging
import json
from datetime import datetime
from difflib import unified_diff
from termcolor import colored

class Gitlet:
    def __init__(self, repo_path=""):
        self.repo_path = pathlib.Path(repo_path) / ".gitlet"
        self.objects_path = self.repo_path / "objects"
        self.head_path = self.repo_path / "HEAD"
        self.index_path = self.repo_path / "index"
        self.init()
    
    def init(self):
        self.repo_path.mkdir(parents=True, exist_ok=True)
        self.objects_path.mkdir(parents=True, exist_ok=True)
        self.head_path.touch(exist_ok=True)
        if not self.index_path.exists() or self.index_path.stat().st_size == 0:
            self.index_path.write_text("[]")

    def hash_Object(self,content):
        return hashlib.sha1(content.encode()).hexdigest() #sha1 is a hash function, 40 digit hexadecimal number, need to encode str o bytes before hashing

    def add(self,file_path):
        fileData = open(file_path,"r").read() #reading file as str
        fileHash = self.hash_Object(fileData) #hashing file content to get name of file where data will be stored in the objects directory
        print(fileHash) #logging the hash to the console
        newHashedfilePath=self.objects_path / fileHash #.gitlet/objects/fileHash
        newHashedfilePath.touch(exist_ok=True) #creating/updating the file
        newHashedfilePath.write_bytes(fileData.encode()) #writing the file data to the file as bytes thats why encoded

        #TODO : Add file to staging area
        self.updateStagingArea(file_path,fileHash)

        print(f"Added {file_path} to objects directory")

    def updateStagingArea(self,file_path,fileHash):
        indexArr= json.load(open(self.index_path,"r"))
        tempArr = {"path": file_path, "hash": fileHash}
        indexArr.append(tempArr)
        json.dump(indexArr, open(self.index_path,"w"))

    def commit(self,message):
        index = json.load(open(self.index_path,"r"))
        parentCommit=self.getCurrentHead()

        commitData={
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message,
            "files": index,
            "parent": parentCommit
        }

        commitHash = self.hash_Object(str(json.dumps(commitData)))
        commitPath = self.objects_path / commitHash
        commitPath.write_bytes(json.dumps(commitData).encode())
        self.head_path.write_bytes(commitHash.encode())
        self.index_path.write_text("[]")
        print("Commit succcessfully created",commitHash)


    def getCurrentHead(self):
        try:
            return open(self.head_path,"r").read()
        except:
            print("NO head file path found")
            return None

    def gitLog(self):
        currentCommitHash= self.getCurrentHead()
        while(currentCommitHash):
            commitData=self.getCommitData(currentCommitHash)
            print("Commit:",currentCommitHash,"\n","Date&Time:",commitData.get('timestamp'),"\n Message",commitData.get('message'),"\n")
            print("-----------------------------------------------------------------------")
            currentCommitHash=commitData.get('parent')
        print("No more commits")

    def showCommitDiff(self,commitHash):
        commitData=self.getCommitData(commitHash)
        if not commitData:
            print("Commit Not Found")
            return
        for file in commitData.get('files'):
            print("IN FILE: ",file.get('path'))
            fileContent = self.getFileData(file.get('hash'))
            #print("File Content", fileContent)
            if(commitData.get("parent")):
                parentCommitData = self.getCommitData(commitData.get("parent"))
                parentFileContent=self.getParentFileData(parentCommitData,file.get("path"))
                print("DIFFERENCES:(if empty then no differences)")
                if parentFileContent:
                    #print("Parent File Content",parentFileContent)
                    self.show_diff_termcolor(parentFileContent,fileContent)
                else:
                    self.show_diff_termcolor("",fileContent)


    def getParentFileData(self,parentCommitData,filepath):
        files = parentCommitData.get("files")
        for file in files:
            if file.get("path") == filepath:
                return self.getFileData(file.get("hash"))
        return None
        
    def show_diff_termcolor(self,parent_content, current_content):
        diff = difflib.unified_diff(
            parent_content.splitlines(keepends=True),
            current_content.splitlines(keepends=True),
            fromfile='parent',
            tofile='current'
        )
        
        for line in diff:
            if line.startswith('+'):
                print(colored(line, 'green'))  # Added lines in green
            elif line.startswith('-'):
                print(colored(line, 'red'))     # Removed lines in red
            elif line.startswith('@'):
                print(colored(line, 'cyan'))    # Header in cyan
            else:
                print(line)                     # Context lines in default color

    def getCommitData(self,commitHash):
        commitPath = self.objects_path / commitHash
        return json.loads(open(commitPath,"r").read())

    def getFileData(self,fileHash):
        filepath = self.objects_path / fileHash
        return open(filepath,"r").read()

# gitlet = Gitlet()
# gitlet.add("sample.txt")
# gitlet.commit('third Commit')
#gitlet.gitLog()
# gitlet.showCommitDiff('e15cd84cf9190aac20b6143e7336cdc8f42e2114')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./gitlet.py <command> [args...]")
        print("Commands: init, add <file>, commit <message>, log, diff <commit>")
        sys.exit(1)
    
    command = sys.argv[1]
    gitlet = Gitlet()
    
    if command == "init":
        print("Gitlet repository initialized")
    elif command == "add" and len(sys.argv) > 2:
        gitlet.add(sys.argv[2])
    elif command == "commit" and len(sys.argv) > 2:
        gitlet.commit(sys.argv[2])
    elif command == "log":
        gitlet.gitLog()
    elif command == "diff" and len(sys.argv) > 2:
        gitlet.showCommitDiff(sys.argv[2])
    else:
        print("Invalid command or missing arguments")
