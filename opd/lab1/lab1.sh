# Author: Nikita "sadnex" Ryazanov
# Variant: 5013

# 1. create folders and files
mkdir lab0
cd lab0

mkdir golduck4
cd golduck4
touch sneasel
echo "nweigth:61.7 height=35.0 atk=10 def=6" > sneasel
mkdir krokorok
touch delcatty
echo -e "Способности\nLast Chance Cute Charm Normalize" > delcatty
cd ..

mkdir magcargo6
cd magcargo6
mkdir monferno
touch growlithe
echo "Способности Bite Roar
Ember Leer Odor Sleuth Helping Hand Flame Wheel Reversal Fire Fang
Take Down Flame Burst Agility Retaliate Flamethrower Crunch Heat Wave
Outrage Flare Blitz" > growlithe
touch exeggcute
echo "Способности Barrage Hypnosis Uproar
Reflect Leech Seed Bullet Seed Stun Spore Poisonpowder Steep Powder
Confusion Worry Seed Natural Gift Solarbeam Extrasensory
Bestow" > exeggcute
cd ..

touch nidoranF7
echo "Тип покемона  POISON NONE" > nidoranF7

touch petilil3
echo -e "Развитые\nспособности Leaf Guard" > petilil3

touch pichu0
echo -e "Развитые способности\nLightningrod" > pichu0

mkdir wormadam7
cd wormadam7
mkdir pansage
touch donphan
echo "Развитые способности  Sand Veil" > donphan
touch mienshao
echo "Ходы
Bounce Drain Punch Dual Chop Helping Hand Knock Off Low Kick Role Play
Sleep Talk Snore" > mienshao
touch ferrothorn
echo "Способности Rollout Curse Metal Claw Pin
Rissile Gyro Bau Iron Defense Mirror Shot Ingrain selfdestruct power
Whip Iron Head payback Flash Cannon Explosion" > ferrothorn
cd ..


# 2. set permissions
chmod 750 golduck4
chmod u=,g=,o=rw golduck4/sneasel
chmod u=wx,g=rwx,o=wx golduck4/krokorok
chmod u=r,g=r,o= golduck4/delcatty
chmod u=rwx,g=wx,o=rw magcargo6
chmod u=wx,g=x,o=w magcargo6/monferno
chmod u=r,g=,o= magcargo6/growlithe
chmod 006 magcargo6/exeggcute
chmod u=rw,g=w,o= nidoranF7
chmod u=rw,g=w,o= petilil3
chmod u=,g=,o=rw pichu0
chmod 751 wormadam7
chmod u=rx,g=rwx,o=rwx wormadam7/pansage
chmod 006 wormadam7/donphan
chmod 400 wormadam7/mienshao
chmod u=r,g=r,o=r wormadam7/ferrothorn


# 3. copy and link files

# 3.1
cd golduck4
ln -s ../nidoranF7 sneaselnidoranF
cd ..

# 3.2
chmod u=rwx magcargo6/exeggcute
cat magcargo6/exeggcute magcargo6/exeggcute > nidoranF7_47
chmod 006 magcargo6/exeggcute

# 3.3
ln petilil3 golduck4/sneaselpetilil

# 3.4
chmod u=rwx pichu0
cat pichu0 > golduck4/delcattypichu
chmod 006 pichu0

# 3.5
cp nidoranF7 magcargo6/monferno

# 3.6
chmod -R u=rwx wormadam7
cp -R wormadam7 golduck4/krokorok
chmod u=rx,g=rwx,o=rwx wormadam7/pansage
chmod 006 wormadam7/donphan
chmod 400 wormadam7/mienshao
chmod u=r,g=r,o=r wormadam7/ferrothorn

# 3.7
ln -s wormadam7 Copy_97


# print directory tree of lab0

echo "directory tree of lab0 after 1-3"
ls -l -R
echo ""


# 4. find and filter files

mkdir /tmp 2>> /dev/null
touch /tmp/log
chmod 777 /tmp/log

# 4.1
echo "4.1"
cd golduck4
# ls -L --zero -p 2>> /tmp/log | grep -v "/$" -z | wc -l --total=never --files0-from=- 2>> /tmp/log | sort -g
wc -l $( ls -L -p | grep -v "/$" ) 2>> /tmp/log | grep -v "total$"
cd ..
echo ""

# 4.2
echo "4.2"
ls -R -l -h -p -L 2>> /dev/null | grep -v "^$" | grep -v ":$" | grep -v "^total" | grep -v "/$" | sort -u | sort -r -h -k 5 | tail -n 3
echo ""

# 4.3
echo "4.3"
cat golduck4/* 2>&1 | grep "li" --color=never
echo ""

# 4.4
echo "4.4"
cat golduck4/sneasel golduck4/delcatty magcargo6/growlithe magcargo6/exeggcute wormadam7/donphan 2>> /dev/null | grep -v -i -n "e$"
echo ""

# 4.5
echo "4.5"
ls -R -o -h -p -t 2>> /dev/null | grep "n$" --color=never | head -n 2
echo ""

# 4.6
echo "4.6"
grep -R --include=p* -n -h "" 2>> /dev/null | sort -u | sort -d
echo ""
# grep -n -h "" $( ls -R -p -L 2>> /dev/null | grep -v "^$" | grep -v ":$" | grep -v "/$" | sort -u | grep "^p" ) 2>> /dev/null | sort -d


# 5. delete files and links

chmod 777 nidoranF7
rm nidoranF7
chmod -R 777 golduck4
rm golduck4/sneasel
rm golduck4/sneaselnidora*
rm golduck4/sneaselpetil*
rm -rf golduck4
rmdir wormadam7/pansage


# print directory tree of lab0

echo "directory tree of lab0 after 1-5"
ls -l -R
echo ""