#!/bin/bash

pwd=$(pwd)


# Make sure the builds directory exists.

mkdir -p builds

export ZANTHIA_BUILDS_DIR=$pwd/builds/

# Initialize local git repository and add the Zanthia post-receive hook.

git init --bare local_remote
ln -s $pwd/post-receive $pwd/local_remote/hooks/post-receive

# Create local repository and push the skeleton there.

git init local_test
cp -rf skeleton/* local_test/
cd local_test
git remote add origin $pwd/local_remote
git add .
git commit -m "Initial commit."
git push origin master
cd -
