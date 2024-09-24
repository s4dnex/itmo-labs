# 1. create folders and files
mkdir lab0
cd lab0

mkdir golduck4
cd golduck4
touch sneasel
echo "nweigth:61.7 height=35.0 atk=10 def=6" >> sneasel
mkdir krokorok
touch delcatty
echo -e "Способности\nLast Chance Cute Charm Normalize" >> delcatty
cd ..

mkdir magcargo6
cd magcargo6
mkdir monferno
touch growlithe
echo "Способности Bite Roar
Ember Leer Odor Sleuth Helping Hand Flame Wheel Reversal Fire Fang
Take Down Flame Burst Agility Retaliate Flamethrower Crunch Heat Wave
Outrage Flare Blitz" >> growlithe
touch exeggcute
echo "Способности Barrage Hypnosis Uproar
Reflect Leech Seed Bullet Seed Stun Spore Poisonpowder Steep Powder
Confusion Worry Seed Natural Gift Solarbeam Extrasensory
Bestow" >> exeggcute
cd ..

touch nidoranF7
echo "Тип покемона  POISON NONE" >> nidoranF7

touch petilil3
echo -e "Развитые\nспособности Leaf Guard" >> petilil3

touch pichu0
echo -e "Развитые способности\nLightningrod" >> pichu0

mkdir wormadam7
cd wormadam7
mkdir pansage
touch donphan
echo "Развитые способности  Sand Veil" >> donphan
touch mienshao
echo "Ходы
Bounce Drain Punch Dual Chop Helping Hand Knock Off Low Kick Role Play
Sleep Talk Snore" >> mienshao
touch ferrothorn
echo "Способности Rollout Curse Metal Claw Pin
Rissile Gyro Bau Iron Defense Mirror Shot Ingrain selfdestruct power
Whip Iron Head payback Flash Cannon Explosion" >> ferrothorn
cd ..

# 2. set permissions
chmod 750 golduck4
chmod u-rwx,g-rwx,o+rw-x golduck4/sneasel
chmod u+rx-w,g+rwx,o+rx-w golduck4/krokorok
chmod u+r-wx,g+r-wx,o-rwx golduck4/delcatty
chmod u+rwx,g+wx-r,o+rw-x magcargo6
chmod u+wx-r,g+x-rw,o+w-rx magcargo6/monferno
chmod u+r-wx,g-rwx,o-rwx magcargo6/growlithe
chmod 006 magcargo6/exeggcute
chmod u+rw-x,g+w-rx,o-rwx nidoranF7
chmod u+rw-x,g+w-rx,o-rwx petilil3
chmod u-rwx,g-rwx,o+rw-x pichu0
chmod 751 wormadam7
chmod u+rx-w,g+rwx,o+rwx wormadam7/pansage
chmod 006 wormadam7/donphan
chmod 400 wormadam7/mienshao
chmod u+r-wx,g+r-wx,o+r-wx wormadam7/ferrothorn

# 3. copy and link files
ln -s nidoranF7 golduck4/sneaselnidoranF
cat magcargo6/exeggcute magcargo6/exeggcute > nidoranF7_47
ln petilil3 golduck4/sneaselpetilil
cp pichu0 golduck4/delcattypichu
cp nidoranF7 magcargo6/monferno/nidoranF7
cp -r wormadam7 golduck4/krokorok
ln -s wormadam7 Copy_97

# 4. find and filter files

mkdir tmp
touch tmp/log
chmod 777 tmp/log
for f in golduck4/*; do
if [[ -f $f ]]
then
echo $(wc -l $f 2>> tmp/log) 2>> tmp/log
fi
done | grep . | sort -n

set +e
