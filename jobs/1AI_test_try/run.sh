#!/bin/bash

# 创建并启动容器

cp evaluator.py ../../

cd ../../
LOCAL_DIR=$(pwd)
docker run -i -v $LOCAL_DIR:/workspace --name AITest mypytorch << EOF
python ./evaluator.py
exit
EOF




# 删除容器
docker stop AITest
docker rm AITest
rm ./evaluator.py
