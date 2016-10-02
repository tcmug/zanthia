#!/bin/bash

ansible-playbook live.yml -c ssh -i inventory/hosts
