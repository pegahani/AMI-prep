for id in {1..151}
	do
		name = "meet_$id.txt"
		echo $name
		if [ -s name ]
		then 
  			echo "File is NOT empty"
		else
  			echo "File is empty"
			echo $name
		fi
	done
