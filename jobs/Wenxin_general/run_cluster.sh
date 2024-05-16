#!/bin/bash

# 创建并启动容器

# 记录开始时间
start_time=$(date +%s)
cp process_cluster.py ../../

cd ../../
LOCAL_DIR=$(pwd)
docker run -i -v $LOCAL_DIR:/workspace --name AITest mypytorch << EOF
python ./process_cluster.py
exit
EOF


# 删除容器
docker stop AITest
docker rm AITest
rm ./process_cluster.py

# 记录结束时间
end_time=$(date +%s)

# 计算并打印运行时间
run_time=$((end_time - start_time))
echo "运行时间: $run_time 秒"
