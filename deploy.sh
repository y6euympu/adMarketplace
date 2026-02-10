. ./backend/.env

eval $(echo "$DATABASE_URL" | awk -F'[:/@]' '{
  print "export POSTGRES_USER=" $4
  print "export POSTGRES_PASSWORD=" $5
  print "export PGPORT=" $7
  print "export POSTGRES_DB=" $8
}')

if ! docker network ls | grep -q marketplace; then
  docker network create marketplace
fi

docker-compose up -d --build
