usage="---------------------------------------------------
SFEDA UI Setup Script

Usage: ./$(basename "$0").sh <absolute-path-to-sfeda>

This script will setup the Sfeda UI and start all the required containers. It assumes that you pass the absolute path of the sfeda directory.

Example: ./SetupUI.sh /home/theasis/software/sfeda/
----------------------------------------------------"

if [ -z "$1" ]; then
    echo "$usage"
    exit 1
fi

echo "Please wait until script is complete. Do NOT interrupt!"

# Change dir to the sfeda directory
cd $1

# Start docker
sudo -S systemctl start docker

# Create docker network
docker network create -d bridge sfeda-net

# Setup RTMP streaming server
cd $1/extras/rtmp2hls/
docker build -t nginx-rtmp-to-hls .
docker run -itd --network=sfeda-net -p 1935:1935 -p 8082:8082 --name=rtmp2hls nginx-rtmp-to-hls

# Setup Graphhopper
cd $1/extras/graphhopper/
chmod 0700 graphhopper.sh
if test ! -f "greece-latest.osm.pbf"; then
    wget https://download.geofabrik.de/europe/greece-latest.osm.pbf
fi
docker run -t -v "$(pwd):/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/greece-latest.osm.pbf
docker run -t -v "$(pwd):/data" osrm/osrm-backend osrm-partition /data/greece-latest.osrm
docker run -t -v "$(pwd):/data" osrm/osrm-backend osrm-customize /data/greece-latest.osrm
docker build -t graphhopper:master .
docker run -itd --network=sfeda-net -p 8989:8989 -v "$(pwd):/data" --name=graphhopper graphhopper:master

# Setup OpenMapTiles
cd $1/extras/openmaptiles
docker pull klokantech/openmaptiles-server 
docker run -itd --network=sfeda-net -p 8083:80 -v "$(pwd):/data" --name=openmaptiles-server klokantech/openmaptiles-server

# Starting the UI
cd $1
docker build -t sfeda .
docker run -itd --network=sfeda-net -p 1234:1234 --name=sfeda sfeda:latest
