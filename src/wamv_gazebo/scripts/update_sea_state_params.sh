if [ "$#" -eq  "0" ]
then
  echo "Usage: ./update_sea_state_params.sh [wave_gain] [wave_period] [wind_speed]"
  exit 1
fi

wave_gain=$1
wave_period=$2
wind_speed=$3

DIR="$( cd "$( dirname "$0" )" && pwd )"

# Update all wave gain params
find $DIR/../models -type f -exec sed -i  '/<wavefield>/,/<\/wavefield>/ s|<gain>[0-9a-z.]\{1,\}</gain>|<gain>'"$wave_gain"'</gain>|g' {} \;
find $DIR/../worlds -maxdepth 1 -type f -exec sed -i  '/<wavefield>/,/<\/wavefield>/ s|<gain>[0-9a-z.]\{1,\}</gain>|<gain>'"$wave_gain"'</gain>|g' {} \;


# Update all wave period params
find $DIR/../models -type f -exec sed -i  '/<wavefield>/,/<\/wavefield>/ s|<period>[0-9a-z.]\{1,\}</period>|<period>'"$wave_period"'</period>|g' {} \;
find $DIR/../worlds -maxdepth 1 -type f -exec sed -i  '/<wavefield>/,/<\/wavefield>/ s|<period>[0-9a-z.]\{1,\}</period>|<period>'"$wave_period"'</period>|g' {} \;

# Update wind linear vel param
find $DIR/../worlds -maxdepth 1 -type f -exec sed -i ':a;N;$!ba;s/\(<wind>.*\)<linear_velocity>.*<\/linear_velocity>\(.*<\/wind\)/\1<linear_velocity>'"$wind_speed"'<\/linear_velocity>\2/g' {} \;


# find $DIR/../../vrx_urdf/wamv_gazebo/urdf/dynamics -type f -exec sed -i  '/<wavefield>/,/<\/wavefield>/ s|<gain>[0-9a-z.]\{1,\}</gain>|<gain>'"$wave_gain"'</gain>|g' {} \;
# find $DIR/../../vrx_urdf/wamv_gazebo/urdf/dynamics -type f -exec sed -i  '/<wavefield>/,/<\/wavefield>/ s|<period>[0-9a-z.]\{1,\}</period>|<period>'"$wave_period"'</period>|g' {} \;
