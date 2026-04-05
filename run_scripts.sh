set -e

DIR_PATH_BASE="./Task4-5/knowledge_base"
DIR_PATH_CHROMA="./Task4-5/.chroma"

if [ -d "$DIR_PATH_BASE" ]; then
  rm -rf "$DIR_PATH_BASE"
  echo "Директория $DIR_PATH_BASE будет пересоздана."
else
  echo "Директория $DIR_PATH_BASE не существует. Будет создана с нуля"
fi

if [ -d "$DIR_PATH_CHROMA" ]; then
  rm -rf "$DIR_PATH_CHROMA"
  echo "Директория $DIR_PATH_CHROMA будет пересоздана."
else
  echo "Директория $DIR_PATH_CHROMA не существует. Будет создана с нуля"
fi

python3 ./Task2/create_knowledge_base.py
python3 ./Task3/build_index.py
docker-compose up