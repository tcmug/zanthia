#!/bin/bash

ssh-add shared/git_rsa
git clone ssh://gitolite@localhost:2222/testing
cd testing
cp -rf ../skeleton/* .
git add .
git commit -m "TEST"
git push origin master
