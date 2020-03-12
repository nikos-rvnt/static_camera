#cd /home/theasis/software/theasis

# S1
echo "theasis2019" |sudo -S systemctl start mongodb
echo "theasis2019" |sudo -S systemctl start memcached
echo "theasis2019" |sudo -S systemctl start docker

docker container start sfeda 
docker container start rtmp2hls 
docker container start graphhopper
docker container start openmaptiles-server
sudo create_ap -n wlp0s20f0u9 Theasis
