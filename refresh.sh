
SELFPATH=$(readlink -f "$0")
SELFDIR=$(dirname "$SELFPATH")

cd $SELFDIR

./build.sh
../cleanup.sh
./run.sh "$@"