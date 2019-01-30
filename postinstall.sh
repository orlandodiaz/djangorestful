echo "Post install script initialized" 
FOLDER="frontend"
URL="https://github.com/orlandodiaz/redux-auth.git"
if [ ! -d "$FOLDER" ] ; then
    git clone $URL $FOLDER
else
    cd "$FOLDER"
    git pull $URL
fi

cd frontend
npm run build


# git clone https://github.com/orlandodiaz/redux-auth.git frontend
# cd frontend
#npm run build
