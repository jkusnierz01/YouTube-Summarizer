#!/bin/bash
if [ -d ./llm ]; then
    if [ ! -d ./llm/models ]; then
        mkdir lmm/models
    fi;
    else
        mkdir llm
        mkdir llm/models
fi;
